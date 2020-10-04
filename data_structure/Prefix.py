import numpy as np
import re
regex_IPprefix = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$')

# @to do: when set the hosts, check if host IP address match the prefix after mask
class Prefix:
    def __init__(self, prefix=None, hosts=None, mask = None):
        self.hosts = np.array([], dtype = object)
        self.prefix = prefix
        self.set_hosts(hosts, prefix)
    def set_hosts(self, hosts, prefix):
        for host in hosts:
            self.hosts = np.append(self.hosts, host)
    def contains(self, IP_address):
        for i in range(len(self.hosts)):
            if (self.hosts[i].IP == IP_address):
                return True
        return False
    def subnet_size(self):
        return len(self.hosts)