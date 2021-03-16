import numpy as np
import re
# to-do: need to check regex_DNS and regex_IP

class Hosts:
    def __init__(self):
        self.dict = {}
class Host:
    regex_DNS = re.compile('^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$')
    regex_IP = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    def __init__(self, IP=None, SSL_version=None, DNS_name=None, time_stamp = None):
        self.set_DNS_name(DNS_name)
        self.set_SSL_version(SSL_version)
        self.set_IP(IP)
        self.timestamp = time_stamp
    def set_IP(self, IP):
        if IP is not None and Host.regex_IP.match(IP):
            self.IP = IP
        else:
            print("Error: Hosts: IP type does not match IPV4")
    def set_DNS_name(self, DNS_name):
        if DNS_name is not None and Host.regex_DNS.match(DNS_name):
            self.DNS_name = DNS_name
        else:
            print("Error: Hosts: DNS_name type does not match")
    def set_SSL_version(self, SSL_version):
        if SSL_version is not None and isinstance(SSL_version, float):
            self.SSL_version = SSL_version
        else:
            print("Error: Hosts: SSL_version type does not match")