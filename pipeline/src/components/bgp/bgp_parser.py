import subprocess
import os
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
from components.bgp.bgp_collector import BGP_Collector
class BGP_Parser:

    def __init__(self, collector = BGP_Collector()):
        self._data_src = collector.local_path
        self._dump_exec_path = os.path.dirname(os.path.realpath(__file__)) + '/bgpdump'
        self._dump_exec_path = os.path.realpath(self._dump_exec_path)
        self._dump_path = os.path.realpath(self._data_src + '/../bgp_tmp/')
        self.collector = collector
        self._names =['BGP protocol','unix time in seconds','Withdraw or Announce','PeerIP','PeerAS','Prefix','AS_PATH','Origin','Next_Hop','Local_Pref','MED','Community','AtomicAGG','AGGREGATOR']
        self._delta = timedelta(hours=2) # rib interval = 2 hours
        self._last_update = ''
    def get_rib(self, start_time):
        """ Returns the most recent parsed object """
        self.collector._check_new_update()
        self.start_time = start_time
        # Need to read and parse data from file
        df, self._last_update = self._read_rib_from_file(start_time)
        return self._parse(df)
    def get_update(self):
        if self._last_update == '':
            return None
        flag = False
        dir_name = self._data_src + '/{}.{}/UPDATES/'.format([self.start_time.year, self.start_time.month])
        for update_filename in sorted(os.listdir(dir_name)): # update_filename : updates.20200901.0000.bz2
            if flag == True:
                self._last_update = update_filename
                return self._parse(self._read_update_from_file(self._last_update))
            if update_filename == self._last_update:
                flag = True
        print("cannot find update") 
        return None
            
    def _parse(self, df):
        """ This call parse the raw_data into a parsed object """
        # <class 'pandas.core.frame.Pandas'>
        return tuple(df.itertuples(index=False, name='bgp'))
    def _read_update_from_file(self, update_filename):
        update_csv_path = self._dump_path+'/'+update_filename+'.csv'
        f = open(update_csv_path,'w')
        subprocess.check_call([self._dump_exec_path, '-m', '-u', update_filename], stdout=f)
        f.close()
        df_update = pd.read_csv(update_csv_path, sep='|', names = self._names, header = None, usecols =range(len(self._names)))
        return df_update
    def _read_rib_from_file(self, start_time):
        dir_name = self._data_src + '/{}.{}/RIBS/'.format([start_time.year, start_time.month])
        # the following two line work as an edge detector - detect the first update after start_time
        last_state = False
        state = False
        for rib_filename in sorted(os.listdir(dir_name)): # rib_filename : rib.20200901.0000.bz2
            rib_date_str = rib_filename.split('.')[1] 
            rib_hour_str = rib_filename.split('.')[2]
            rib_timestamp = datetime(year=int(rib_date_str[0:4]),month=int(rib_date_str[4:6]), day=int(rib_date_str[6:8]),
                                        hour=int(rib_hour_str[0:2]), minute=int(rib_hour_str[2:4]))
            if rib_timestamp.day == start_time.day and (start_time.hour - rib_timestamp.hour) < 2 and (start_time.hour - rib_timestamp.hour) >= 0:
                rib_csv_path = self._dump_path+'/'+rib_filename+'.csv'
                f = open(rib_csv_path,'w')
                subprocess.check_call([self._dump_exec_path, '-m', '-u', rib_filename], stdout=f)
                f.close()
                df = pd.read_csv(rib_csv_path, sep='|', names = self._names, header = None, usecols =range(len(self._names)), dtype={'unix time in seconds':'float64'})
                dir_name = self._data_src + '/{}.{}/UPDATES/'.format([start_time.year, start_time.month])
                for update_filename in sorted(os.listdir(dir_name)): # update_filename : updates.20200901.0000.bz2
                    update_date_str = update_filename.split('.')[1] 
                    update_hour_str = update_filename.split('.')[2]
                    update_timestamp = datetime(year=int(update_date_str[0:4]),month=int(update_date_str[4:6]), day=int(update_date_str[6:8]),
                                                hour=int(update_hour_str[0:2]), minute=int(update_hour_str[2:4]))
                    if update_timestamp >= rib_timestamp and update_timestamp < start_time:
                        state = True
                        update_csv_path = self._dump_path+'/'+update_filename+'.csv'
                        f = open(update_csv_path,'w')
                        subprocess.check_call([self._dump_exec_path, '-m', '-u', update_filename], stdout=f)
                        f.close()
                        df_update = pd.read_csv(update_csv_path, sep='|', names = self._names, header = None, usecols =range(len(self._names)))
                        df = df.merge(df_update, on=('PeerAS','Prefix'), how='outer',indicator=True)
                        filter_col_x = [col for col in df if col.endswith('_x')]
                        filter_col_y = [col for col in df if col.endswith('_y')]
                        df.loc[df['_merge']=='right_only',filter_col_x] = df.loc[df['_merge']=='right_only',filter_col_y].values
                        df = df.drop(filter_col_y, axis=1)
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
                        return df, update_filename
                    last_state = state
        return None, ''

    def flush_data(self):
        """
        This function is called when the Synchronizer determines that
        this parser has the most recent parsed object and send it downstream.
        Therefore, the local copy of the parsed object is invalidated.
        """
        self._parsed = None

if __name__ == '__main__':
    BGP_Parser()._read_data_from_file()