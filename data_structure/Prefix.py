import numpy as np
import re
# with some code from https://medium.com/@sadatnazrul/checking-if-ipv4-address-in-network-python-af61a54d714d

class Prefix:
    regex_IP = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    def __init__(self, prefix, prefix_length = None):
        # only one param is passed, prefix is like "192.168.0.0/16"
        if prefix_length == None:
            try:
                self.str, self.prefix_len = prefix.split('/')
            except:
                raise ValueError('prefix does not fit IPv4 format')
        # two param are passed
        else:
            self.prefix_len = prefix_length
            self.str = prefix_length
        if not Prefix.regex_IP.match(self.str):
            raise ValueError('prefix does not fit IPv4 format')
        try:
            self.prefix_len = int(self.prefix_len)
        except:
            raise ValueError('prefix does not fit IPv4 format')
        self.binary = Prefix.ip_to_binary(self.str)
        self.int = int(self.binary,2)
    def ip_to_binary(ip_address):
        octet_list_int = ip_address.split(".")
        octet_list_bin = [format(int(i), '08b') for i in octet_list_int]
        binary = ("").join(octet_list_bin)
        return binary
    def get_addr_network(address, net_size):
        #Convert ip address to 32 bit binary
        ip_bin = Prefix.ip_to_binary(address)
        #Extract Network ID from 32 binary
        network = ip_bin[0:32-(32-net_size)]    
        return network
    def contain_ip(self, ip_address):
        #Get the network ID of both prefix and ip based net size
        prefix_network = Prefix.get_addr_network(self.str, self.prefix_len)
        ip_network = Prefix.get_addr_network(ip_address, self.prefix_len)
        return ip_network == prefix_network