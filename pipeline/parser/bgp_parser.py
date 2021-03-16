import subprocess
import os
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import numpy as np
from multiprocessing import Pool
import csv
from multiprocessing import Pool
from collector.bgp_collector import BGPCollector
from data_structure.parsed_obj import ParsedObj
from parser.base_parser import BaseParser


class BGPParser(BaseParser):

    def __init__(self, dry_run=None): # actual deployment: collector = BGPCollector()
        # self._data_src = collector.local_path
        self.collector = BGPCollector(dry_run=dry_run)
        self._data_src = self.collector.local_path
        self._dump_exec_path = os.path.dirname(os.path.realpath(__file__)) + '/../externals/bgpdump/bgpdump'
        self._dump_exec_path = os.path.realpath(self._dump_exec_path)
        self._dump_path = os.path.realpath(self._data_src + '/../bgp_tmp/')
        if not os.path.exists(self._dump_path):
            os.makedirs(self._dump_path)
        self._names =['BGP protocol','unix time in seconds','Withdraw or Announce','PeerIP','PeerAS','Prefix','AS_PATH','Origin','Next_Hop','Local_Pref','MED','Community','AtomicAGG','AGGREGATOR']
        self._delta_cap = timedelta(hours=2) # rib interval = 2 hours
        self._last_update_time = None
        self._last_update_filename = ''
        self.start_time = None
        self._parsed_obj = None             # its data is a dict of one row
        self._curr_update_csv_f = None
        self._curr_update_reader = None
        self._rib = []
    def get_data(self):
        """ Return None if there is no update """
        if self.start_time is None:
            raise RuntimeError('BGP parser is not initialized yet')
        if self._parsed_obj is not None:
            # not flushed, return last result
            return self._parsed_obj
        if len(self._rib) != 0:
            # snapshot output
            row = self._rib.pop()
            self._parsed_obj = ParsedObj(timestamp = float(row['unix time in seconds']), label='bgp', data = row)
        elif self._curr_update_reader is None:
            # snapshot exhausted, have not loaded new update
            if self._get_update() == -1:
                # no more updates available
                return None
            return self.get_data()
        else:
            # self._curr_update_reader is not None
            # snapshot exhausted, return next row in update
            row = next(self._curr_update_reader, None)
            if row is None:
                # current update exhausted
                self._curr_update_csv_f.close()
                os.remove(self._curr_update_csv_f.name)
                self._curr_update_csv_f = None
                self._curr_update_reader = None
                return self.get_data()
            else:
                # current update has more rows
                self._parsed_obj = ParsedObj(timestamp = float(row['unix time in seconds']), label='bgp', data = row)
        return self._parsed_obj
    def set_start_time(self, start_time):
        self._get_rib(start_time)
        
    def _get_rib(self, start_time):
        """ 
        Initialize start_time if valid, apply updates to a closest rib
        to get the snapshot up to start_time.
        """
        #self.collector._check_new_update()
        if start_time <= datetime(2003,2,3,19,32,tzinfo=timezone.utc):
            raise LookupError('Data before 2003/02/03 19:32 UTC is in Pacific Time, algorithm not implemented for tricky data')
        self.start_time = start_time
        # Need to read and parse data from file
        self._rib, self._last_update_filename = self._read_rib_from_file(start_time)
        self._last_update_time = self._filename_to_dt(self._last_update_filename)
    def _get_update(self):
        """
        load new updates
        changed class variable: self._curr_update_csv_f, self._curr_update_reader,
                                self._last_update_time, self._last_update_filename
        """
        if self._last_update_time is None:
            raise RuntimeError('BGP parser is not initialized yet')
        flag = False
        dir_name = self._data_src + '/{}.{:02}/UPDATES/'.format(self._last_update_time.year, self._last_update_time.month)
        for update_filename in sorted(os.listdir(dir_name)): # update_filename : updates.20200901.0000.bz2
            if flag == True:
                self._last_update_filename = update_filename
                self._last_update_time = self._filename_to_dt(self._last_update_filename)
                self._read_update_from_file(self._last_update_filename)
                return 0
            if update_filename == self._last_update_filename:
                flag = True
        if update_filename == self._last_update_filename:
            # meaning this update is the last update in this month
            tmp_time = self._last_update_time +timedelta(weeks = 4) # go to next month by adding 28 days (potential bug)
            dir_name = self._data_src + '/{}.{:02}/UPDATES/'.format(tmp_time.year, tmp_time.month)
            if (os.path.isdir(dir_name)): # if next month's data is available
                for update_filename in sorted(os.listdir(dir_name)): # update_filename : updates.20200901.0000.bz2
                    self._last_update_filename = update_filename
                    self._last_update_time = self._filename_to_dt(self._last_update_filename)
                    self._read_update_from_file(self._last_update_filename)
                    return 0
        print("cannot find update") 
        return -1
             
    
    def _read_update_from_file(self, update_filename):
        """
        changed class variable: self._curr_update_csv_f, self._curr_update_reader,
        """
        update_csv_path = self._dump_path+'/'+update_filename+'.csv'
        dir_name = self._data_src + '/{}.{:02}/UPDATES/'.format(int(update_filename[8:12]), int(update_filename[12:14]))
        subprocess.check_call([self._dump_exec_path, '-m', '-u', '-O', update_csv_path, dir_name+update_filename])
        self._curr_update_csv_f = open(update_csv_path, 'r', newline='')
        self._curr_update_reader = csv.DictReader(self._curr_update_csv_f, fieldnames=self._names, delimiter='|')
    def _read_rib_from_file(self, start_time):
        if start_time <= datetime(2003,2,3,19,32,tzinfo=timezone.utc):
            raise LookupError('Data before 2003/02/03 19:32 UTC is in Pacific Time, algorithm not implemented for tricky data')
        dir_name = self._data_src + '/{}.{:02}/RIBS/'.format(start_time.year, start_time.month)
        # the following two line work as an edge detector - detect the first update after start_time
        rib_filename_list = sorted(os.listdir(dir_name))
        rib_filename_list = tuple(filter(lambda rib_filename: rib_filename.endswith('.bz2'), rib_filename_list))
        if start_time < self._filename_to_dt(rib_filename_list[0]):
            # if oldest rib in this month is older than the start_time, use the newest rib file from last month
            one_day_before = start_time - timedelta(days=1)
            dir_name = self._data_src + '/{}.{:02}/RIBS/'.format(one_day_before.year, one_day_before.month)
            rib_filename_list = sorted(os.listdir(dir_name))
            rib_filename_list = tuple(filter(lambda rib_filename: rib_filename.endswith('.bz2'), rib_filename_list))
            rib_filename = rib_filename_list[-1]
            rib_timestamp = self._filename_to_dt(rib_filename)
            update_dir_name = self._data_src + '/{}.{:02}/UPDATES/'.format(one_day_before.year, one_day_before.month)
        else:
            for rib_filename in rib_filename_list: # rib_filename : rib.20200901.0000.bz2
                rib_timestamp = self._filename_to_dt(rib_filename)
                if start_time - rib_timestamp < self._delta_cap and start_time - rib_timestamp >= timedelta(hours=0):
                    break
            update_dir_name = self._data_src + '/{}.{:02}/UPDATES/'.format(start_time.year, start_time.month)
        rib_csv_path = self._dump_path+'/'+rib_filename+'.csv'
        subprocess.check_call([self._dump_exec_path, '-m', '-u', '-O', rib_csv_path, dir_name+'/'+rib_filename])
        rib_rows = {}
        with open(rib_csv_path, 'r', newline='') as rib_csv:
            rib_reader = csv.DictReader(rib_csv, delimiter='|', fieldnames=self._names)
            for row in rib_reader:
                key = (row['PeerAS'], row['Prefix'])
                rib_rows[key] = row
        for update_filename in sorted(os.listdir(update_dir_name)): # update_filename : updates.20200901.0000.bz2
            update_timestamp = self._filename_to_dt(update_filename)
            if update_timestamp >= rib_timestamp and update_timestamp <= start_time:
                update_csv_path = self._dump_path+'/'+update_filename+'.csv'
                rib_rows, update_timestamp = self._update_rib(rib_rows, update_csv_path, update_dir_name, update_filename)
                if update_timestamp > start_time:
                    break
            elif update_timestamp > start_time:
                break
        if update_timestamp <= start_time:
            tmp_time = update_timestamp +timedelta(weeks = 4) # go to next month by adding 28 days (potential bug)
            update_dir_name = self._data_src + '/{}.{:02}/UPDATES/'.format(tmp_time.year, tmp_time.month)
            if os.path.isdir(update_dir_name):
                for update_filename in sorted(os.listdir(update_dir_name)): # update_filename : updates.20200901.0000.bz2
                    update_timestamp = self._filename_to_dt(update_filename)
                    if update_timestamp >= rib_timestamp and update_timestamp <= start_time:
                        update_csv_path = self._dump_path+'/'+update_filename+'.csv'
                        rib_rows, update_timestamp = self._update_rib(rib_rows, update_csv_path, update_dir_name, update_filename)
                        if update_timestamp > start_time:
                            break
                    elif update_timestamp > start_time:
                        break
        rib_rows = list(sorted(rib_rows.values(), key=lambda row: row['unix time in seconds'], reverse=True))
        subprocess.check_call(['rm', '-f', rib_csv_path])
        return rib_rows, update_filename

    def _filename_to_dt(self, filename):
        date_str = filename.split('.')[1] 
        hour_str = filename.split('.')[2]
        return datetime(year=int(date_str[0:4]),month=int(date_str[4:6]), day=int(date_str[6:8]),
                                        hour=int(hour_str[0:2]), minute=int(hour_str[2:4]),tzinfo=timezone.utc)
    def _update_rib(self, rib_rows, update_csv_path, update_dir_name, update_filename):
        f = open(update_csv_path,'w')
        subprocess.check_call([self._dump_exec_path, '-m', '-u', update_dir_name+'/'+update_filename], stdout=f)
        f.close()
        update_csv_f = open(update_csv_path, 'r', newline='')
        update_reader = csv.DictReader(update_csv_f, fieldnames=self._names, delimiter='|')
        row = next(update_reader,None)
        while row is not None:
            update_timestamp = datetime.fromtimestamp(float(row['unix time in seconds']), tz=timezone.utc)
            if update_timestamp > self.start_time:
                # there are unread rows in the update, save file handler and csv reader (iterator)
                self._curr_update_csv_f = update_csv_f
                self._curr_update_reader = update_reader
                return rib_rows, update_timestamp
            key = (row['PeerAS'], row['Prefix'])
            if row['Withdraw or Announce'] == 'W':
                try:
                    rib_rows.pop(key)
                except:
                    pass
            else:
                rib_rows[key] = row
            row = next(update_reader,None)
        # all rows in this update are applied, remove this csv
        update_csv_f.close()
        os.remove(update_csv_f.name)
        self._curr_update_csv_f = None
        self._curr_update_reader = None
        return rib_rows, update_timestamp

