import numpy as np
import re
regex_DNS = re.compile('^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$')
regex_IP = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

class Host:
    def __init__(self, SSL_version=None, DNS_name=None, IP=None):
        self.set_DNS_name(DNS_name)
        self.set_SSL_version(SSL_version)
        self.set_IP(IP)
    
    def set_IP(self, IP):
        if(regex_IP.match(IP)):
            self.IP = IP
        else:
            print("Error: Hosts: IP type does not match IPV4")
    def set_DNS_name(self, DNS_name):
        if(regex_DNS.match(DNS_name)):
            self.DNS_name = DNS_name
        else:
            print("Error: Hosts: DNS_name type does not match")
    def set_SSL_version(self, SSL_version):
        if(isinstance(SSL_version, float)):
            self.SSL_version = SSL_version
        else:
            print("Error: Hosts: SSL_version type does not match")
    def get_Prefix(self):
        cout_dot = 0
        result = ""
        for char in self.IP:
            if (char == '.'):
                cout_dot += 1
                if(cout_dot == 2):
                    break
            result += char
        return result + ".0.1/24"