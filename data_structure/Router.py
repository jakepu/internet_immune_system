import numpy as np
import re

class Router:
    def __init__(self, prefix_list=None, ip=None):
        self.prefex_list = prefix_list
        self.ip = ip