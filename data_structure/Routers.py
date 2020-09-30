import numpy as np
import re
regex_IPprefix = re.compile('^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$')

class Routers:
    def __init__(self, prefix_set=None):
        self.prefix_set = np.array([], dtype = object)
        self.set_prefix_set(prefix_set)
    def set_prefix_set(self, prefix_set):
        for prefix in prefix_set:
            if(regex_IPprefix.match(prefix.prefix)):
                self.prefix_set = np.append(self.prefix_set, prefix)
            else:
                print("Error: Routers: router prefix does not fit IPV4 regex")