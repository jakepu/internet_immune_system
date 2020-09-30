import time
import datetime
import numpy as np

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
            self.AS_graph = graph(graph_component, AS_set)
        for number in self.AS_numbers:
            if number not in self.AS_graph.getVertices():
                self.AS_graph.gdict[number] = []
            
    def set_AS_set(self, AS_set):
        AS_number = []
        for AS in AS_set:
            if AS.number not in AS_number:
                self.AS_set = np.append(self.AS_set, AS)
                AS_number.append(AS.number)
            else:
                print('Error: Internet: redundent AS number ', AS.number)
        return AS_number
                
    def add_connection(self, AS1, AS2):
        if AS1.number not in self.AS_numbers:
            self.AS_numbers.append(AS1.number)
            self.AS_set = np.append(self.AS_set, AS1)
        if AS2.number not in self.AS_numbers:
            self.AS_numbers.append(AS2.number)
            self.AS_set = np.append(self.AS_set, AS2)
        edge = set([AS1.number, AS2.number])
        (vrtx1, vrtx2) = tuple(edge)
        if vrtx1 in self.AS_graph.gdict:
            self.AS_graph.gdict[vrtx1].append(vrtx2)
        else:
            self.AS_graph.gdict[vrtx1] = [vrtx2]
        if vrtx2 in self.AS_graph.gdict:
            self.AS_graph.gdict[vrtx2].append(vrtx1)
        else:
            self.AS_graph.gdict[vrtx2] = [vrtx1]
        
# This graph part needs to be modified so each node represents a AS object
class graph:
    
    def __init__(self,gdict=None, AS_set=None):
        if gdict is None:
            gdict = {}
        self.gdict = gdict

    def edges(self):
        return self.findedges()

    def getVertices(self):
        return list(self.gdict.keys())

    # List the edge names
    def findedges(self):
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if {nxtvrtx, vrtx} not in edgename:
                    edgename.append({vrtx, nxtvrtx})
        return edgename
    #return the distance between two vertices
    def trial(self, v1, v2):
        queue = [v1]
        trial = {}
        visited = {v1 : 1}
        while queue:
            current = queue.pop(0)
            if current == v2:
                result = [v2]
                while v2 in trial:
                    v2 = trial[v2]
                    result.insert(0, v2)
                return result
            for neighbor in self.gdict[current]:
                if neighbor not in visited:
                    trial[neighbor] = current
                    queue.append(neighbor)
                    visited[neighbor] = 1
        return []
    def distance(self, v1, v2):
        return len(trial(self, v1, v2))