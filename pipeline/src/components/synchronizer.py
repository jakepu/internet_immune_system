class Synchronizer:

    def __init__(self, parsers):
        self._parsers = parsers

    def get_next_most_recent(self):
        """ Return the most recent parsed object among all parsers  """
        parsed_objs = [(p, p.get_data()) for p in self._parsers]

        parser, most_recent_data = min(parsed_objs, key=lambda p: p[1].timestamp)
        parser.flush_data()

        return most_recent_data
