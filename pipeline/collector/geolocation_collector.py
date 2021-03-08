import datetime
from datetime import timedelta
from datetime import datetime
import sys
import os
import subprocess
from os import path
from base_collector import BaseCollector
class GEOCollector(BaseCollector):
    def __init__(self, source_url = '', local_path = ''):
        if source_url == '':
            source_url = 'https://ipinfo.io/data/beta/location.gz?token=1ab9f7e8fa8714'
        if local_path == '':
            local_path = os.path.dirname(os.path.realpath(__file__)) + '/../data/geolocationdata'
        self.source_url = 'https://ipinfo.io/data/beta/location.gz?token=1ab9f7e8fa8714'     # actual address for deployment
        super().__init__(source_url, local_path)
        self.local_path = os.path.realpath(self.local_path)
    def check_new_update(self):
        print('ipinfo online server to local path:',self.local_path)
        if os.path.exists(self.local_path + '/last_update.txt'):
            update = open(self.local_path + '/last_update.txt', "r")
            old_time_str = update.read()
            old_time = datetime.strptime(old_time_str, "%Y-%m-%d %H:%M:%S.%f")
            new_time = datetime.now(timezone.utc)
            update.close()
            if(new_time > (old_time + timedelta(weeks=1))):
                update = open(self.local_path + '/last_update.txt', "w+")
                update.write(str(datetime.now(timezone.utc)))
                update.close()
                return True
            else:
                return False

        else:
            update = open(self.local_path + '/last_update.txt', "w+")
            update.write(str(datetime.now(timezone.utc)))
            update.close()
            return True
            