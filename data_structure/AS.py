import numpy as np

# waiting for databases and parsers to add attributes
# keep three sets of neighbors, Customer, Peer, Provider

class AS:
    geo_location_set = ['Asia', 'US', 'Europe', 'Australia', 'Africa','SouthernAmerica']
    as_type_set = ['enterprise', 'private', 'non-profit']
    def __init__(self, as_type=None, geo_location=None, routers = None, number=None, customers=None, peers=None, providers=None, router_list=None):
        self.router_list = router_list
        return