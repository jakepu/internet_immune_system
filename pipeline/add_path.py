import sys
from pathlib import Path # if you haven't already done so
import os
def add_path():
    sys.path.append(os.path.dirname(__file__))
def remove_path():
    try:
        sys.path.remove(os.path.dirname(__file__))
    except ValueError: # Already removed
        pass

if __name__ == '__main__':
    remove_path()
    print(Path(__file__).resolve())