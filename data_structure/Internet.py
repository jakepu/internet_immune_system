import time
import datetime
import numpy as np

# @to_do: do BFS using Customer > Peer > Provider order for trial() function
# @to_do: grpah component need to change to three sets to provide three kinds of neighbors
class Internet:
    def __init__(self, last_updated_time, AS_set=None, graph_component = None):
        if(isinstance(last_updated_time, datetime.datetime)):
            self._time = last_updated_time
        else:
            print("Error: Internet: invalid last_updated_time passed")
        self.AS_set = np.array([], dtype = object)
        self.AS_numbers = self.set_AS_set(AS_set)
        for key in graph_component:
            flag = True
            if key not in self.AS_numbers:
                flag = False
                print('Error: Internet: graph component does not match the AS numbers passed in ', key)
        if flag:
            for key in graph_component:
                for neighbors in graph_component[key]:
                    tmp = self.get_AS_by_number(key)
                    neighbor_tmp = self.get_AS_by_number(neighbors)
                    # one direction, can change to two direction
                    tmp.set_neighbors(np.array([neighbor_tmp], dtype = object))
                
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
    
    def add_connection(self, AS1, AS2):
        if AS1.number not in self.AS_numbers:
            self.AS_numbers.append(AS1.number)
            self.AS_set = np.append(self.AS_set, AS1)
        if AS2.number not in self.AS_numbers:
            self.AS_numbers.append(AS2.number)
            self.AS_set = np.append(self.AS_set, AS2)
        # one direction, can change to two direction by add following
        # AS2.set_neighbors(np.array([AS1], dtype = object))
        AS1.set_neighbors(np.array([AS2], dtype = object))
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
            for neighbor in current.neighbors:
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
    
    def get_edges(self):
        edgename = []
        for AS in self.AS_set:
            for neighbor in AS.neighbors:
                if {AS.number, neighbor.number} not in edgename:
                    edgename.append({AS.number, neighbor.number})
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