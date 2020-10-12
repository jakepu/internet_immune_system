import numpy as np
geo_location_set = ['Asia', 'US', 'Europe', 'Australia', 'Africa','SouthernAmerica']
as_type_set = ['enterprise', 'private', 'non-profit']

# keep three sets of neighbors, Customer, Peer, Provider

class AS:
    def __init__(self, as_type=None, geo_location=None, routers = None, number=None, customers=None, peers=None, providers=None):
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
        self.neighbors_customer = np.array([], dtype = object)
        self.neighbors_peer = np.array([], dtype = object)
        self.neighbors_provider = np.array([], dtype = object)
        self.set_routers_set(routers)
        if customers != None:
            self.set_neighbors_customer(customers)
        if peers != None:
            self.set_neighbors_peer(peers)
        if providers != None:
            self.set_neighbors_provider(providers)
    def set_routers_set(self, routers):
        for router in routers:
            self.routers = np.append(self.routers, router)
    def set_neighbors_customer(self, customers):
        for customer in customers:
            if isinstance(customer, AS):
                if customer.number != self.number and customer not in self.neighbors_customer:
                    self.neighbors_customer = np.append(self.neighbors_customer, customer)
            else:
               print("customer type not correct")
    def set_neighbors_peer(self, peers):
        for peer in peers:
            if isinstance(peer, AS):
                if peer.number != self.number and peer not in self.neighbors_peer:
                    self.neighbors_peer = np.append(self.neighbors_peer, peer)
            else:
               print("peer type not correct")
    def set_neighbors_provider(self, providers):
        for provider in providers:
            if isinstance(provider, AS):
                if provider.number != self.number and provider not in self.neighbors_provider:
                    self.neighbors_provider = np.append(self.neighbors_provider, provider)
            else:
               print("provider type not correct")