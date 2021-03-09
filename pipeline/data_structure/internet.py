from datetime import datetime
from datetime import timedelta
from datetime import timezone
import ipaddress
from data_structure.host import Hosts, Host
import data_structure.autonomous_system import AS, ASs
import data_structure.prefix import Prefixes, Prefix
import data_structure.router import Routers, Router

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
        return

    def build_structure_bgp(self, parsed_obj):
        router_ip = Internet.ip_to_uint32(parsed_obj.data['PeerIP'])
        prefix = parsed_obj.data['Prefix']
        mode = parsed_obj.data['Withdraw or Announce']
        AS_num = int(parsed_obj.data['PeerAS'])
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
        else:
            # mode == 'W'
            # router
            if router_ip in self.routers.dict:
                self.routers.dict[router_ip].prefix_set.remove(prefix)
            # prefix
            if prefix in self.prefixes.dict:
                self.prefixes.dict[prefix].broadcast_router_set.remove(router_ip)
            # AS
            if AS_num not in self.ASs.dict:
                self.ASs.dict[AS_num] = AS(number=AS_num, router_set={router_ip})
            else:
                self.ASs.dict[AS_num].router_set.add(router_ip)
        return

# ways to convert ip to uint32(unsigned long)
# https://stackoverflow.com/questions/9590965/convert-an-ip-string-to-a-number-and-vice-versa
    @staticmethod
    def ip_to_uint32(ip_address):
        return int(ipaddress.ip_address(ip_address))
    
    @staticmethod
    def prefix_to_uint32(prefix):
        return int(ipaddress.IPv4Interface(prefix).ip)
