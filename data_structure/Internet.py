import time
import datetime
import numpy as np
import Host
import AS
import Prefix
import Router
# BFS using Customer > Peer > Provider order for trial() function

class Internet:
    def __init__(self):

    def get_prefix_set(self):
        prefixes = np.array([], dtype = object)
        for AS in self.AS_set:
            for routers in AS.routers:
                for prefix in routers.prefix_set:
                    if prefix not in prefixes:
                        prefixes = np.append(prefix, prefixes)
        return prefixes
    def build_structure(self, parsedObj):
        if(parsedObj.label == "shodan"):
            return self.build_structure_shodan(parsedObj)
    
    def build_structure_shodan(self, parsedObj):
        host = Host(parsedObj.data["ip_addr"], None, None, parsedObj.timestamp)
        self.AS_set[0].routers[0].prefix_set[0].append_host(host)
        
    def count_hosts(self):
        prefixes = self.get_prefix_set()
        count = 0
        for prefix in prefixes:
            for host in prefix.hosts:
                count += 1
        return count