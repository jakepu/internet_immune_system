import subprocess
import os
import pandas as pd
import zipfile
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import urllib.request
import gzip
import numpy as np
from ..collector.bgp_collector import BGPCollector
from ..data_structure.parsed_obj import ParsedObj
from multiprocessing import Pool
from .base_parser import BaseParser
import csv
from multiprocessing import Pool
#Data in the csv is of the form (start_ip, end_ip, join_key, city, region, country, latitude, longitude, postal_code, timezone)
class GEOParser(BaseParser):

    def __init__(self): # actual deployment: collector = GEOCollector()
        self.collector = GEOCollector()
        self._data_src = self.collector.local_path
        self._data = None
        self.start_time = None
        self._parsed = None 
        self._labels = ['start_ip', 'end_ip', 'join_key', 'city', 'region', 'country', 'latitude', 'longitude', 'postal_code', 'timezone']
        self._curr_update_csv_f = None
        self._curr_update_reader = None
    def get_update(self):
        if self.start_time is None:
            raise RuntimeError('Geolocation parser is not initialized yet')
        if self._parsed is not None:
            # not flushed, return last result
            return self._parsed
        
        if self.collector.check_new_update():
            urllib.request.urlretrieve(self.collector.source_url, self._data_src + '/location.gz')
            
            gz = gzip.GzipFile(self._data_src + 'location.gz', 'rb')
            data = gz.read()
            gz.close()

            csv = open(self._data_src + 'location.csv', 'wb')
            csv.write(data)
            csv.close()
            data = None

            self._data = {}
            with open(self._data_src + 'location.csv', encoding='utf8') as self._curr_update_csv_f:
                self._curr_update_reader = csv.reader(self._curr_update_csv_f)
                for row in self._curr_update_reader:
                    self._data[row[0]] = [row[3], row[5], row[6], row[7]] #Chooses city, country, latitude, and longitude. Can be changed based on needs. This reduces the needed memory by not just including every field

            self._parsed = ParsedObj(timestamp = datetime.now(timezone.utc), label='geolocation', data = self._data)

            return self._parsed
        else:
            return self._parsed

    def initialize(self, start_time):
        self.start_time = start_time
        
    def flush_data(self):
        self._parsed = None

    