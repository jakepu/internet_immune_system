import os
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
class BaseCollector(ABC):
    def __init__(self, source_url = '', local_path = ''):
        self.source_url = source_url        # actual download address
        self.local_path = local_path        # local storage directory
        
    @abstractmethod
    def check_new_update(self) -> bool:
        pass