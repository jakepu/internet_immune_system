import numpy as np
geo_location_set = ['Asia', 'US', 'Europe', 'Australia', 'Africa','SouthernAmerica']
as_type_set = ['enterprise', 'private', 'non-profit']

class AS:
    def __init__(self, as_type=None, geo_location=None, routers = None, number = None):
        if as_type in as_type_set:
            self.as_type = as_type
        else:
            print("Error: in AS: as_type not match")
        if geo_location in geo_location_set:
            self.geo_location = geo_location
        else:
            print("Error: in AS: geo_location not match")
        if( number >= 0 and number <= 10000):
            self.number = number
        else:
            print("Error: in AS: as_number does not match")
        self.routers = np.array([], dtype = object)
        self.set_routers_set(routers)
    def set_routers_set(self, routers):
        for router in routers:
            self.prefix_set = np.append(self.routers, router)
        