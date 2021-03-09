import numpy as np

# waiting for databases and parsers to add attributes
# keep three sets of neighbors, Customer, Peer, Provider

class ASs():
    def __init__(self):
        self.dict = {}
class AS:
    geo_location_set = ['Asia', 'US', 'Europe', 'Australia', 'Africa','SouthernAmerica']
    as_type_set = ['enterprise', 'private', 'non-profit']
    def __init__(self, number, as_type=None, geo_location=None, routers = None, customers=None, peers=None, providers=None, router_set=None):
        self.router_set = router_set if router_set else set()
        self.number = number