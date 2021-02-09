from abc import ABC, abstractmethod
class BaseParser(ABC):

    def __init__(self):
        self._parsed = None

    @abstractmethod
    def get_data(self, start_time = None):
        """ Returns the most recent parsed object """
        if not self._parsed:
            # Need to read and parse data from file
            raw_data = self._read_data_from_file()
            self._parsed = self._parse(raw_data)

        print('parser ' + self._data_src +' now has ' + str(self._parsed.timestamp))
        return self._parsed

    @abstractmethod
    def _parse(self, raw_data):
        """ This call parse the raw_data into a parsed object """
        # raise NotImplementedError
        pass

    def flush_data(self):
        """
        This function is called when the Synchronizer determines that
        this parser has the most recent parsed object and send it downstream.
        Therefore, the local copy of the parsed object is invalidated.
        """
        self._parsed = None



