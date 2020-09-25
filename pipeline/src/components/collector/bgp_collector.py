from datetime import date
from bs4 import BeautifulSoup
import requests
import wget
import os
bgp_url = 'http://archive.routeviews.org/bgpdata/'
class bgp_collector:
    def __init__(self):
        self.last_filename = ''
        self.local_path = os.path.dirname(os.path.realpath(__file__)) + '/../../../data/bgp_updates'
        self.local_path = os.path.realpath(self.local_path)
        print(self.local_path)
        self._check_new_update()
    def _check_new_update(self):
        self.today = date.today()
        self.bgp_directory = bgp_url + str(self.today.year) +'.'+ '{:02d}'.format(self.today.month) + '/UPDATES/'
        r = requests.get(self.bgp_directory)
        soup = BeautifulSoup(r.content, features='lxml')
        if self.last_filename != soup.find_all('a')[-1].get('href'):
            self.last_filename = soup.find_all('a')[-1].get('href')          
            wget.download(self.bgp_directory + self.last_filename, out=self.local_path)
            
if __name__ == '__main__':
    bgp_collector()
