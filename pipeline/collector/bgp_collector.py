import datetime
import sys
import os
import subprocess
from .base_collector import BaseCollector
class BGPCollector(BaseCollector):
    def __init__(self):
        self.source_url = 'rsync://archive.routeviews.org/routeviews/bgpdata/'     # actual address for deployment
        self.local_path = os.path.dirname(os.path.realpath(__file__)) + '/../data/bgpdata'
        self.local_path = os.path.realpath(self.local_path)
        self.check_new_update()
    def check_new_update(self):
        # dry run: rsync -avz -n --stats rsync://archive.routeviews.org/routeviews/bgpdata/ .
        print('rsync from online server to local path:',self.local_path)
        if subprocess.check_output(["rsync","-aiz", self.source_url, self.local_path], text=True) == '':
            return False
        return True
if __name__ == '__main__':
    pass