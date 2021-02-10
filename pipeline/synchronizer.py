from .data_structure import *
import datetime
import numpy as np


class Synchronizer:

    def __init__(self, parsers, start_time):
        self._parsers = parsers
        self._set_start_time_in_parsers(start_time)
        self.internet = None
        print('Initializing skeleton Internet')
        self._build_sleleton_Internet()
        self.count = 0

    def get_next_most_recent(self):
        """ Return the most recent parsed object among all parsers  """
        parsed_objs = [(p, p.get_data()) for p in self._parsers]

        eof_parsers = [p[0] for p in parsed_objs if p[1] is None]
        # Unregister the parsers that have no more data
        for parser in eof_parsers:
            self._unregister_parser(parser)
        # Check if all the parsers are done
        if len(self._parsers) == 0:
            return None
        # Filter out the None update
        parsed_objs = [p for p in parsed_objs if p[0] not in eof_parsers]
        # Get the most recent update
        parser, most_recent_data = min(parsed_objs, key=lambda p: p[1].timestamp)

        # Enable time order checking
        # if most_recent_data.timestamp < parser.last_parsed_timestamp:
        #     raise Exception("Got update that is prior to the previously received update from this parser")
        # parser.last_parsed_timestamp = most_recent_data.timestamp
        # Invalidate the cached copy
        parser.flush_data()
        self.count += 1
        return most_recent_data

    def _set_start_time_in_parsers(self, start_time):
        """Set the start time in all parsers"""
        for parser in self._parsers:
            parser.set_start_time(start_time)

    def fill_data_structure(self, update):
        """Update the data structure given the update"""
        self.internet.build_structure(update)

    def _build_sleleton_Internet(self):
        """This function is misplaced. It should be in the data structure"""
        host = Host(None, None, None, None)
        Host_list = np.array([host], dtype = object)
        prefix = Prefix(None,Host_list)
        Prefix_list = np.array([prefix], dtype = object)
        router = Routers(Prefix_list)
        Router_list = np.array([router], dtype = object)
        as_system = AS(None,None,Router_list, None,)
        AS_list = np.array([as_system], dtype = object)
        self.internet = Internet(datetime.datetime.now(), AS_list,)

    def _unregister_parser(self, parser):
        print("Removing parser: " + parser._data_src)
        self._parsers.remove(parser)