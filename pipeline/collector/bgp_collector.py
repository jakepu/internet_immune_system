import datetime
import sys
import os
import subprocess
from .base_collector import BaseCollector
class BGPCollector(BaseCollector):
    def __init__(self, source_url = '', local_path = ''):
        if source_url == '':
            source_url = 'rsync://archive.routeviews.org/routeviews/bgpdata/'
        if local_path == '':
            local_path = os.path.dirname(os.path.realpath(__file__)) + '/../data/bgpdata'
        self.source_url = 'rsync://archive.routeviews.org/routeviews/bgpdata/'     # actual address for deployment
        super().__init__(source_url, local_path)
        self.local_path = os.path.realpath(self.local_path)
        self.check_new_update()
    def check_new_update(self):
        # dry run: rsync -avz -n --stats rsync://archive.routeviews.org/routeviews/bgpdata/ .
        print('rsync from online server to local path:',self.local_path)
        if subprocess.check_output(["rsync","-aiz", self.source_url, self.local_path], text=True) == '':
            print('BGP Collector found no new files')
            return False
        print('BGP Collector rsynced new files')
        return True
if __name__ == '__main__':
    pass