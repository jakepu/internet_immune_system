from datetime import datetime
from datetime import timedelta
from datetime import timezone
import ipaddress
from data_structure.host import Hosts, Host
from data_structure.autonomous_system import AS, ASs
from data_structure.prefix import Prefixes, Prefix
from data_structure.router import Routers, Router
import numpy as np
import pandas as pd

class Internet:
    def __init__(self):
        self.hosts = Hosts()
        self.prefixes = Prefixes()
        self.routers = Routers()
        self.ASs = ASs()
    def build_structure(self, parsed_obj):
        if(parsed_obj.label == "shodan"):
            return self.build_structure_shodan(parsed_obj)
        if(parsed_obj.label == "bgp"):
            return self.build_structure_bgp(parsed_obj)
        
    def build_structure_shodan(self, parsed_obj):
        raise NotImplementedError

    def build_structure_bgp(self, parsed_obj):
        router_ip = Internet.ip_to_uint32(parsed_obj.data['PeerIP'])
        prefix = parsed_obj.data['Prefix']
        mode = parsed_obj.data['Withdraw or Announce']
        AS_num = int(parsed_obj.data['PeerAS'])
        timestamp = float(parsed_obj.data['unix time in seconds'])
        if mode == 'A' or mode == 'B':
            # router
            if router_ip not in self.routers.dict:
                self.routers.dict[router_ip] = Router(prefix_set={prefix}, ip=router_ip, AS=AS_num)
            else:
                self.routers.dict[router_ip].prefix_set.add(prefix)
            # prefix
            if prefix not in self.prefixes.dict:
                # add only curr router or all routers on path to list?
                self.prefixes.dict[prefix] = Prefix(prefix, broadcast_router_set={router_ip})
            else:
                self.prefixes.dict[prefix].broadcast_router_set.add(router_ip)
            # AS
            if AS_num not in self.ASs.dict:
                self.ASs.dict[AS_num] = AS(number=AS_num, router_set={router_ip})
            else:
                self.ASs.dict[AS_num].router_set.add(router_ip)
            self.routers.dict[router_ip].announce_time.append(timestamp)
        else:
            # mode == 'W'
            # router
            if router_ip in self.routers.dict:
                try:
                    self.routers.dict[router_ip].prefix_set.remove(prefix)
                except KeyError:
                    pass
            # prefix
            if prefix in self.prefixes.dict:
                try:
                    self.prefixes.dict[prefix].broadcast_router_set.remove(router_ip)
                except KeyError:
                    pass
            # AS
            if AS_num not in self.ASs.dict:
                self.ASs.dict[AS_num] = AS(number=AS_num, router_set={router_ip})
            else:
                self.ASs.dict[AS_num].router_set.add(router_ip)
            # put a timestamp in router
            self.routers.dict[router_ip].withdraw_time.append(timestamp)
        return

# ways to convert ip to uint32(unsigned long)
# https://stackoverflow.com/questions/9590965/convert-an-ip-string-to-a-number-and-vice-versa
    @staticmethod
    def ip_to_uint32(ip_address):
        return int(ipaddress.ip_address(ip_address))
    
    @staticmethod
    def prefix_to_uint32(prefix):
        return int(ipaddress.IPv4Interface(prefix).ip)
    @staticmethod
    def convert_to_timestamp(start_time, end_time):
        if end_time < start_time:
            raise ValueError('end_time should be greater or equal to start_time')
        if not isinstance(start_time, datetime) and not isinstance(start_time, float):
            raise ValueError('start_time has wrong format')
        if not isinstance(end_time, datetime) and not isinstance(end_time, float):
            raise ValueError('end_time has wrong format')
        if isinstance(start_time, datetime):
            start_time = start_time.timestamp()
        if isinstance(end_time, datetime):
            end_time = end_time.timestamp()
        return start_time, end_time
    def get_AS_activity(self, AS_num, start_time, end_time):
        if AS_num not in self.ASs.dict:
            return 0
        start_time, end_time = Internet.convert_to_timestamp(start_time, end_time)
        announce = 0
        withdraw = 0
        for router in self.ASs.dict[AS_num].router_set:
            announce += np.searchsorted(self.routers.dict[router].announce_time, end_time) \
                        - np.searchsorted(self.routers.dict[router].announce_time, start_time)
            withdraw += np.searchsorted(self.routers.dict[router].withdraw_time, end_time) \
                        - np.searchsorted(self.routers.dict[router].withdraw_time, start_time)
        return announce, withdraw
    
    def get_leaking_ASs(self, start_time, end_time):
        start_time, end_time = Internet.convert_to_timestamp(start_time, end_time)
        records = {}
        for AS_num, AS in self.ASs.dict.items():
            records[AS_num] = self.get_AS_activity(AS_num, start_time, end_time)[0]
        df = pd.DataFrame(list(records.items()), columns=['AS_num', 'Announcement']).sort_values(by='Announcement', ascending=False)
        divider = df['Announcement'].quantile(q=0.90)
        return df[df.Announcement >= divider]['AS_num'].tolist()
    
    def get_hijacked_prefix(self, start_time, end_time):
        ret = []
        for _, prefix in self.prefixes.dict.items():
            if len(prefix.broadcast_router_set) > 1:
                ret.append(prefix.prefix)
        return ret
