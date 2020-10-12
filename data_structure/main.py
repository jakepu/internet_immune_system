from Internet import Internet
from AS import AS
from Routers import Routers
from Prefix import Prefix
from Host import Host
import time
import datetime
import numpy as np

# this function is used to test the functionality of the data structure
# run main.py will do the test
def test():
    # this function is used to test the functionality of the data structure
    # run main.py will do the test
    # this function is used to test the functionality of the data structure
    # run main.py will do the test
    host = Host(3.5, 'abc', '200.4.5.7')
    AS_list = np.array([], dtype = object)
    Host_list = np.array([], dtype = object)
    for i in range(10):
        Host_list = np.append(Host_list ,Host(3 + i/10, 'abc', '200.4.5.7'))

    a = Prefix('200.4.0.1/24',Host_list)

    a = Prefix('200.4.0.1/24',Host_list)
    a.contains('200.4.5.7')

    prefix_list = np.array([], dtype = object)
    for i in range(5):
        prefix_list = np.append(prefix_list, Prefix('200.4.0.1/24',Host_list))

    b = Routers(prefix_list).prefix_set[0].hosts[0].IP

    router_list = np.array([], dtype = object)
    for i in range(6):
        router_list = np.append(router_list, Routers(prefix_list))

    as_system1 = AS('enterprise','US',router_list, 1,)
    as_system2 = AS('private','Asia',router_list, 2,)
    as_system3 = AS('non-profit','Europe',router_list, 3,)
    as_system4 = AS('non-profit','Europe',router_list, 4,)
    as_list = np.array([as_system1, as_system2, as_system3, as_system4], dtype = object)
    graph_component = {1:[2,3],
                    3:[1, 2]}

    graph_component2 = {2:[1],
                        3:[4]}

    graph_component3 = {1:[4]}
    a = Internet(datetime.datetime.now(), as_list, graph_component, graph_component2, graph_component3)
    a.add_connection(as_system2, as_system4,  "customer")
    print(as_system1.routers)
    print(as_system3.neighbors_peer)
    as_system2.geo_location = "US"
    a.add_connection(as_system4, as_system3, "peer")
    a.get_edges()
    a.trial(as_system4, as_system1)
    print(as_system1.neighbors_peer)
    
test()