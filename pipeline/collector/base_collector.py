import os
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
class BaseCollector(ABC):
    def __init__(self):
        self.source_url = ''        # actual download address
        self.local_path = ''        # local storage directory
        self.check_new_update()
    @abstractmethod
    def check_new_update(self) -> bool:
        pass