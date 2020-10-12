import time
import datetime
import numpy as np

# BFS using Customer > Peer > Provider order for trial() function

class Internet:
    def __init__(self, last_updated_time, AS_set, graph_component_c, graph_component_peer, graph_component_p):
        if(isinstance(last_updated_time, datetime.datetime)):
            self._time = last_updated_time
        else:
            print("Error: Internet: invalid last_updated_time passed")
        self.AS_set = np.array([], dtype = object)
        self.AS_numbers = self.set_AS_set(AS_set)
        self.set_neighbors("customer", graph_component_c)
        self.set_neighbors("peer", graph_component_peer)
        self.set_neighbors("provider", graph_component_p)
                    
    def set_neighbors(self, neighbor_type, graph_component):
        for key in graph_component:
            flag = True
            if key not in self.AS_numbers:
                flag = False
                print('Error: Internet: graph component does not match the AS numbers passed in ', key, neighbor_type)
        if flag:
            for key in graph_component:
                tmp = self.get_AS_by_number(key)
                for neighbors in graph_component[key]:
                    neighbor_tmp = self.get_AS_by_number(neighbors)
                    # one direction, can change to two direction
                    if neighbor_type == "customer":
                        tmp.set_neighbors_customer(np.array([neighbor_tmp], dtype = object))
                    elif neighbor_type == "peer":
                        tmp.set_neighbors_peer(np.array([neighbor_tmp], dtype = object))
                    elif neighbor_type == "provider":
                        tmp.set_neighbors_provider(np.array([neighbor_tmp], dtype = object))
                    else:
                        raise Exception("neighbor type wrong")
                    
    def set_AS_set(self, AS_set):
        AS_number = []
        for AS in AS_set:
            if AS.number not in AS_number:
                self.AS_set = np.append(self.AS_set, AS)
                AS_number.append(AS.number)
            else:
                print('Error: Internet: redundent AS number ', AS.number)
        return AS_number
    
    def get_AS_by_number(self, as_number):
        for AS in self.AS_set:
            if AS.number == as_number:
                return AS
        print("AS not in as set")
        return None
    
    def add_connection(self, AS1, AS2, neighbor_type):
        if AS1.number not in self.AS_numbers:
            self.AS_numbers.append(AS1.number)
            self.AS_set = np.append(self.AS_set, AS1)
        if AS2.number not in self.AS_numbers:
            self.AS_numbers.append(AS2.number)
            self.AS_set = np.append(self.AS_set, AS2)
        # one direction, can change to two direction by add following
        if neighbor_type == "customer":
            AS1.set_neighbors_customer(np.array([AS2], dtype = object))
        elif neighbor_type == "peer":
            AS1.set_neighbors_peer(np.array([AS2], dtype = object))
        elif neighbor_type == "provider":
            AS1.set_neighbors_provider(np.array([AS2], dtype = object))
        else:
            raise Exception("neighbor type wrong")
        
    def trial(self, AS1, AS2):
        queue = np.array([AS1],dtype = object)
        trial = {}
        visited = {AS1.number: 1}
        while queue.size > 0:
            current = queue[-1]
            queue = queue[:-1]
            if current.number == AS2.number:
                result = [AS2.number]
                while AS2.number in trial:
                    AS2.number = trial[AS2.number]
                    result.insert(0, AS2.number)
                return result
            for neighbor in current.neighbors_provider:
                if neighbor.number not in visited:
                    trial[neighbor.number] = current.number
                    queue = np.append(neighbor, queue)
                    visited[neighbor.number] = 1
            for neighbor in current.neighbors_peer:
                if neighbor.number not in visited:
                    trial[neighbor.number] = current.number
                    queue = np.append(neighbor, queue)
                    visited[neighbor.number] = 1
            for neighbor in current.neighbors_customer:
                if neighbor.number not in visited:
                    trial[neighbor.number] = current.number
                    queue = np.append(neighbor, queue)
                    visited[neighbor.number] = 1
        return []
    def distance(self, AS1, AS2):
        len_trial = len(self.trial(AS1, AS2))
        if len_trial > 1:
            return len_trial - 1;
        print("The input ASes are not connected, or inputs are the same")
        return 0
    
    def get_edges(self, neighbor_type = None):
        edgename = []
        for AS in self.AS_set:
            if neighbor_type == "customer":
                for neighbor in AS.neighbors_customer:
                    if {AS.number, neighbor.number} not in edgename:
                        edgename.append((AS.number, neighbor.number))
            elif neighbor_type == "peer":
                for neighbor in AS.neighbors_peer:
                    if {AS.number, neighbor.number} not in edgename:
                        edgename.append((AS.number, neighbor.number))
            elif neighbor_type == "provider":
                for neighbor in AS.neighbors_provider:
                    if {AS.number, neighbor.number} not in edgename:
                        edgename.append((AS.number, neighbor.number))
            elif neighbor_type == None:
                for neighbor in AS.neighbors_customer:
                    if {AS.number, neighbor.number} not in edgename:
                        edgename.append((AS.number, neighbor.number))
                for neighbor in AS.neighbors_peer:
                    if {AS.number, neighbor.number} not in edgename:
                        edgename.append((AS.number, neighbor.number))
                for neighbor in AS.neighbors_provider:
                    if {AS.number, neighbor.number} not in edgename:
                        edgename.append((AS.number, neighbor.number))
        return edgename
    def get_vertices(self):
        vtx = []
        for AS in self.AS_set:
            if AS.number not in self.AS_set:
                vtx.append(AS.number)
        return vtx  
    def get_prefix_set(self):
        prefixes = np.array([], dtype = object)
        for AS in self.AS_set:
            for routers in AS.routers:
                for prefix in routers.prefix_set:
                    if prefix not in prefixes:
                        prefixes = np.append(prefix, prefixes)
        return prefixes