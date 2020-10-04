import os
import pandas as pd
import datetime
class BGP_Parser:

    def __init__(self):
        self._data_src = os.path.dirname(os.path.realpath(__file__)) + '/../../../data/bgp_updates'
        self._data_src = os.path.realpath(self._data_src)
        self._dump_exec_path = os.path.dirname(os.path.realpath(__file__)) + '/../externals/bgpdump'
        self._dump_exec_path = os.path.realpath(self._dump_exec_path)
        self._dump_path = self._data_src + '/dumps/'
        self._parquet_path = self._data_src + '/parquets/'
    def get_data(self, start_time, end_time, mode):
        """ Returns the most recent parsed object """
        # Need to read and parse data from file
        raw_data = self._read_data_from_file(start_time, end_time)
        self._parsed = self._parse(raw_data)

        print('parser ' + self._data_src +' now has ' + str(self._parsed.timestamp))
        return self._parsed

    def _parse(self, raw_data):
        """ This call parse the raw_data into a parsed object """
        raise NotImplementedError

    def _read_data_from_file(self):
        os.system("cd {} && ls *.bz2 | parallel {} && rm -f *.bz2".format(self._data_src, "'bunzip2 {}'"))
        os.system("cd {} && ls updates* | parallel '~/Downloads/bgpdump-master/bgpdump -m -u {{}} > ./dumps/{{}}.txt'".format(self._data_src))
        for filename in os.listdir(self._dump_path):
            if filename.endswith(".txt"):
                names = ['BGP protocol','unix time in seconds','Withdraw or Announce','PeerIP','PeerAS','Prefix','AS_PATH','Origin','Next_Hop','Local_Pref','MED','Community','AtomicAGG','AGGREGATOR']
                df = pd.read_csv(self._dump_path + '/' + filename, sep='|', names = names, header = None, usecols =range(len(names)))
                print(df.head())
                df.to_parquet(self._parquet_path+ filename[:-4])
        

    def flush_data(self):
        """
        This function is called when the Synchronizer determines that
        this parser has the most recent parsed object and send it downstream.
        Therefore, the local copy of the parsed object is invalidated.
        """
        self._parsed = None

if __name__ == '__main__':
    BGP_Parser()._read_data_from_file()