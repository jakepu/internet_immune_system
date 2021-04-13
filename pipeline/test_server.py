from collector.bgp_collector import BGPCollector
from parser.bgp_parser import BGPParser
from datetime import datetime
from datetime import timezone
from synchronizer import Synchronizer
from data_structure.internet import Internet

# BGPCollector(dry_run=True)
parsers = [BGPParser(dry_run=True, local_path = '/media/SATA/internet_ml/bgpdata/')]
start_time = datetime(year=2004, month=1, day=1, hour=1, tzinfo=timezone.utc)
end_time = datetime(year=2004, month=1, day=30, hour=23, tzinfo=timezone.utc).timestamp()
syn = Synchronizer(parsers, start_time)
curr_time = start_time.timestamp()
testing = Internet()
while (curr_time < end_time):
    update = syn.get_next_most_recent()
    curr_time = update.timestamp
    testing.build_structure(update)
end_time = datetime(year=2004, month=1, day=3, hour=2, tzinfo=timezone.utc)
print('AS activity', testing.get_AS_activity(15290, start_time, end_time))
print('Get leaking ASs', testing.get_leaking_ASs(start_time, end_time))
print('Hijacked prefix', testing.get_hijacked_prefix(start_time, end_time))