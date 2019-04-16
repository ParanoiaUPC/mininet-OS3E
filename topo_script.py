# author: ParanoiaUPC
# email: 757459307@qq.com
import re, json
import networkx as nx
import sys
sys.path.append(".")
import Topology
from mininet.topo import Topo

INFO_FILE_PATH = "os3e_latlong.json"
METERS_TO_MILES = 0.000621371192


def calc_latency(weight):
    # the weight of OS3EWeightedGraph is the path length in miles
    # return delay in milliseconds ( using light speed )
    return weight / METERS_TO_MILES / (3 * 1e8) * 1000


switches = {}
hosts = {}


class OS3ETopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        g = Topology.OS3EWeightedGraph()
        i = 0
        for node in g.nodes:
            switches[node] = self.addSwitch('s'+str(i))
            i += 1
        for edge in g.edges:
            weight = g[edge[0]][edge[1]]['weight']
            delay = calc_latency(weight)
            if weight is not None:
                self.addLink(switches[edge[0]], switches[edge[1]], delay=str(delay)+'ms')
        j = 0
        for node in g.nodes:
            hosts[node] = self.addHost('h'+str(j))
            j += 1
            self.addLink(switches[node], hosts[node])


topos = {'mytopo': (lambda: OS3ETopo())}
