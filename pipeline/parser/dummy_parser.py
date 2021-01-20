from random import randint
from random import seed

import time
from components.parser import Parser
from components.parsed_obj import ParsedObj


class DummyParser(Parser):
    """ A dummy parser for testing which generate fake parsed
    objects with random timestamps
    """
    def __init__(self, data_src):
        super().__init__(data_src)
        # seed random number generator
        seed(1)
        self._delay_in_seconds = randint(3, 8)

    def _parse(self, raw_data):
        time.sleep(self._delay_in_seconds)

        obj = ParsedObj()
        obj.timestamp = randint(3, 1500)
        return obj

    def _read_data_from_file(self):
        pass



