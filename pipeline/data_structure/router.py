import numpy as np
import re

class Routers:
    def __init__(self):
        self.dict = {}
class Router:
    def __init__(self, ip, prefix_set=None, AS=None):
        self.prefix_set = prefix_set if prefix_set else set()
        self.ip = ip
        self.AS = AS
        self.count = {}
        self.announce_time = []
        self.withdraw_time = []