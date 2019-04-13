import re, json
import networkx as nx
import Topology
from mininet.topo import Topo

INFO_FILE_PATH = "os3e_latlong.json"
METERS_TO_MILES = 0.000621371192


def calc_latency(weight):
    # the weight of OS3EWeightedGraph is the path length in miles
    # return delay in milliseconds ( using light speed )
    return weight / METERS_TO_MILES / (3 * 1e8) * 1000


class OS3ETopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        self.switches = {}
        self.hosts = {}
        g = Topology.OS3EWeightedGraph()
        for node in g.nodes:
            self.switches[node] = self.addSwitch(node)
        for edge in g.edges:
            weight = g[edge[0]][edge[1]]['weight']
            delay = calc_latency(weight)
            if weight is not None:
                self.addLink(self.switches[edge[0]], self.switches[edge[1]], delay=str(delay)+'ms')
        for node in g.nodes:
            self.hosts[node] = self.addHost(node+'-host')
            self.addLink(self.switches[node], self.hosts[node])

topos = {'mytopo': (lambda: OS3ETopo())}