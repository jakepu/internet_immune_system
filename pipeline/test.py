from collector.bgp_collector import BGPCollector
from parser.bgp_parser import BGPParser
from datetime import datetime
from datetime import timezone
from synchronizer import Synchronizer
# BGPCollector(dry_run=True)
parsers = [BGPParser(dry_run=True)]
start_time = datetime(year=2003, month=4, day=2, hour=2, tzinfo=timezone.utc)
testing = Synchronizer(parsers, start_time)
testing.get_next_most_recent()
# internet = Internet()
# internet.build_structure(testing.get_next_most_recent())