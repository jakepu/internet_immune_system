import datetime
import sys
import os
import subprocess
from base_collector import BaseCollector
class BGPCollector(BaseCollector):
    def __init__(self, source_url = '', local_path = '', dry_run = None):
        if source_url == '':
            source_url = 'rsync://archive.routeviews.org/routeviews/bgpdata/'
        if local_path == '':
            local_path = os.path.dirname(os.path.realpath(__file__)) + '/../data/bgpdata'
        self.source_url = 'rsync://archive.routeviews.org/routeviews/bgpdata/'     # actual address for deployment
        super().__init__(source_url, local_path)
        self.local_path = os.path.realpath(self.local_path)
        self.check_new_update(dry_run)
    def check_new_update(self, dry_run=None):
        # dry run: rsync -avz -n --stats rsync://archive.routeviews.org/routeviews/bgpdata/ .
        print('rsync from online server to local path:',self.local_path)
        if dry_run is None:
            dry_run = ''
        else:
            dry_run = '-n'
        if subprocess.check_output(["rsync","-aiz", dry_run, self.source_url, self.local_path], text=True) == '':
            print('BGP Collector found no new files')
            return False
        print('BGP Collector rsynced new files')
        return True
if __name__ == '__main__':
    BGPCollector(dry_run=True)