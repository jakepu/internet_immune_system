import subprocess
import os
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import numpy as np
from bgp_collector import BGP_Collector
from components.parsed_obj import ParsedObj
class BGP_Parser:

    def __init__(self, collector = None): # actual deployment: collector = BGP_Collector()
        # self._data_src = collector.local_path
        self._data_src = os.path.dirname(os.path.realpath(__file__)) + '/../../../data/bgpdata'
        self._dump_exec_path = os.path.dirname(os.path.realpath(__file__)) + '/bgpdump/bgpdump'
        self._dump_exec_path = os.path.realpath(self._dump_exec_path)
        self._dump_path = os.path.realpath(self._data_src + '/../bgp_tmp/')
        self.collector = collector
        self._names =['BGP protocol','unix time in seconds','Withdraw or Announce','PeerIP','PeerAS','Prefix','AS_PATH','Origin','Next_Hop','Local_Pref','MED','Community','AtomicAGG','AGGREGATOR']
        self._delta_cap = timedelta(hours=2) # rib interval = 2 hours
        self._last_update_time = None
        self._last_update_filename = ''
    def get_data(self, start_time = None):
        if start_time is None:
            self.get_update()
        else:
            self.get_rib(start_time)
    def get_rib(self, start_time):
        """ Returns the most recent parsed object """
        #self.collector._check_new_update()
        if start_time <= datetime(2003,2,3,19,32,tzinfo=timezone.utc):
            raise LookupError('Data before 2003/02/03 19:32 UTC is in Pacific Time, algorithm not implemented for tricky data')
        self.start_time = start_time
        # Need to read and parse data from file
        df, self._last_update_filename = self._read_rib_from_file(start_time)
        self._last_update_time = self._filename_to_dt(self._last_update_filename)
        return self._parse(df)
    def get_update(self):
        if self._last_update_time is None:
            print("cannot find update")
            return None
        flag = False
        dir_name = self._data_src + '/{}.{}/UPDATES/'.format(self._last_update_time.year, self._last_update_time.month)
        for update_filename in sorted(os.listdir(dir_name)): # update_filename : updates.20200901.0000.bz2
            if flag == True:
                self._last_update_filename = update_filename
                self._last_update_time = self._filename_to_dt(self._last_update_filename)
                return self._parse(self._read_update_from_file(self._last_update_filename))
            if update_filename == self._last_update_filename:
                flag = True
        if update_filename == self._last_update_filename:
            # meaning this update is the last update in this month
            tmp_time = self._last_update_time +timedelta(weeks = 4) # go to next month by adding 28 days (potential bug)
            dir_name = self._data_src + '/{}.{}/UPDATES/'.format(tmp_time.year, tmp_time.month)
            if (os.path.isdir(dir_name)): # if next month's data is available
                for update_filename in sorted(os.listdir(dir_name)): # update_filename : updates.20200901.0000.bz2
                    self._last_update_filename = update_filename
                    self._last_update_time = self._filename_to_dt(self._last_update_filename)
                    return self._parse(self._read_update_from_file(self._last_update_filename))
        print("cannot find update") 
        return None
            
    def _parse(self, df):
        """ This call parse the raw_data into a parsed object """
        # <class 'pandas.core.frame.Pandas'>
        self._parsed = []
        for i in df.index:
            self._parsed.append(ParsedObj(df.iloc[i]['unix time in seconds'],'bgp',df.iloc[i].to_json))
        return self._parsed
    def _read_update_from_file(self, update_filename):
        update_csv_path = self._dump_path+'/'+update_filename+'.csv'
        f = open(update_csv_path,'w')
        subprocess.check_call([self._dump_exec_path, '-m', '-u', update_filename], stdout=f)
        f.close()
        df_update = pd.read_csv(update_csv_path, sep='|', names = self._names, header = None, usecols =range(len(self._names)))
        return df_update
    def _read_rib_from_file(self, start_time):
        # if start_time <= datetime(2003,2,3,19,32,tzinfo=timezone.utc):
        #     raise LookupError('Data before 2003/02/03 19:32 UTC is in Pacific Time, algorithm not implemented for tricky data')
        dir_name = self._data_src + '/{}.{}/RIBS/'.format(start_time.year, start_time.month)
        # the following two line work as an edge detector - detect the first update after start_time
        last_state = False
        state = False
        rib_filename_list = sorted(os.listdir(dir_name))
        rib_filename_list = tuple(filter(lambda rib_filename: rib_filename.endswith('.bz2'), rib_filename_list))
        for rib_filename in rib_filename_list: # rib_filename : rib.20200901.0000.bz2
            rib_timestamp = self._filename_to_dt(rib_filename)
            if start_time - rib_timestamp < self._delta_cap and start_time - rib_timestamp >= timedelta(hours=0):
                rib_csv_path = self._dump_path+'/'+rib_filename+'.csv'
                f = open(rib_csv_path,'w+')
                subprocess.check_call([self._dump_exec_path, '-m', '-u', dir_name+'/'+rib_filename], stdout=f)
                f.close()
                df = pd.read_csv(rib_csv_path, sep='|', names = self._names, header = None, usecols =range(len(self._names)), dtype={'unix time in seconds':'float64'})
                dir_name = self._data_src + '/{}.{}/UPDATES/'.format(start_time.year, start_time.month)
                for update_filename in sorted(os.listdir(dir_name)): # update_filename : updates.20200901.0000.bz2
                    update_timestamp = self._filename_to_dt(update_filename)
                    if update_timestamp >= rib_timestamp and update_timestamp < start_time:
                        state = True
                        update_csv_path = self._dump_path+'/'+update_filename+'.csv'
                        f = open(update_csv_path,'w')
                        subprocess.check_call([self._dump_exec_path, '-m', '-u', dir_name+'/'+update_filename], stdout=f)
                        f.close()
                        df_update = pd.read_csv(update_csv_path, sep='|', names = self._names, header = None, usecols =range(len(self._names)),dtype={'unix time in seconds':'float64'})
                        df_update = df_update[df_update['unix time in seconds'] <= start_time.timestamp()]
                        df = df.merge(df_update, on=('PeerAS','Prefix'), how='outer',indicator=True)
                        filter_col_x = [col for col in df if col.endswith('_x')]
                        filter_col_y = [col for col in df if col.endswith('_y')]
                        df.loc[df['_merge']=='right_only',filter_col_x] = df.loc[df['_merge']=='right_only',filter_col_y].values
                        #df.to_csv(self._dump_path+'/'+'output.csv')
                        df = df.drop(filter_col_y, axis=1)
                        df = df.drop('_merge', axis=1)
                        col_names = [col for col in df]
                        for i in range(len(col_names)):
                            if col_names[i].endswith('_x'):
                                col_names[i] = col_names[i][:-2]
                        df.columns = col_names
                        subprocess.check_call(['rm', '-f', update_csv_path])
                    else:
                        state = False
                    if last_state == True and state == False:
                        subprocess.check_call(['rm', '-f', rib_csv_path])
                        df.loc[:,'Withdraw or Announce'] = 'B'
                        return df, update_filename
                    last_state = state
                subprocess.check_call(['rm', '-f', rib_csv_path])
        return None, ''
    def _filename_to_dt(self, filename):
        date_str = filename.split('.')[1] 
        hour_str = filename.split('.')[2]
        return datetime(year=int(date_str[0:4]),month=int(date_str[4:6]), day=int(date_str[6:8]),
                                        hour=int(hour_str[0:2]), minute=int(hour_str[2:4]),tzinfo=timezone.utc)
    def flush_data(self):
        """
        This function is called when the Synchronizer determines that
        this parser has the most recent parsed object and send it downstream.
        Therefore, the local copy of the parsed object is invalidated.
        """
        self._parsed = None

if __name__ == '__main__':
    print(BGP_Parser()._read_rib_from_file(datetime(2001,10,26,23,50,tzinfo=timezone.utc))[1])