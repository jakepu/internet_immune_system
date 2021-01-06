import numpy as np
import re

class Router:
    def __init__(self, prefix_list=None, host_list=None):
        self.prefex_list = prefix_list
        self.host_list = host_list