import datetime
import sys
import os
import subprocess
class BGP_Collector:
    bgp_url = 'rsync://archive.routeviews.org/routeviews/bgpdata/'
    def __init__(self):
        self.local_path = os.path.dirname(os.path.realpath(__file__)) + '/../../../data/bgpdata'
        self.local_path = os.path.realpath(self.local_path)
        print(self.local_path)
        self._check_new_update()
    def _check_new_update(self):
        # dry run: rsync -avz -n --stats rsync://archive.routeviews.org/routeviews/bgpdata/ .
        if subprocess.check_output(["rsync","-az", BGP_Collector.bgp_url, self.local_path], text=True) == '':
            return False
        return True
        """
        if subprocess.check_output(["rsync","-az", BGP_Collector.bgp_url, self.local_path], text=True) != '':
            fire('new_bgp_packages')
        """    
if __name__ == '__main__':
    BGP_Collector()
