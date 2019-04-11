import re, json
import networkx as nx
from mininet.topo import Topo

INFO_FILE_PATH = "os3e_latlong.json"

# copied from
def OS3EGraph():
    g = nx.Graph()
    g.add_path(["Vancouver", "Seattle"])
    g.add_path(["Seattle", "Missoula", "Minneapolis", "Chicago"])
    g.add_path(["Seattle", "SaltLakeCity"])
    g.add_path(["Seattle", "Portland", "Sunnyvale"])
    g.add_path(["Sunnyvale", "SaltLakeCity"])
    g.add_path(["Sunnyvale", "LosAngeles"])
    g.add_path(["LosAngeles", "SaltLakeCity"])
    g.add_path(["LosAngeles", "Tucson", "ElPaso"])
    g.add_path(["SaltLakeCity", "Denver"])
    g.add_path(["Denver", "Albuquerque", "ElPaso"])
    g.add_path(["Denver", "KansasCity", "Chicago"])
    g.add_path(["KansasCity", "Dallas", "Houston"])
    g.add_path(["ElPaso", "Houston"])
    g.add_path(["Houston", "Jackson", "Memphis", "Nashville"])
    g.add_path(["Houston", "BatonRouge", "Jacksonville"])
    g.add_path(["Chicago", "Indianapolis", "Louisville", "Nashville"])
    g.add_path(["Nashville", "Atlanta"])
    g.add_path(["Atlanta", "Jacksonville"])
    g.add_path(["Jacksonville", "Miami"])
    g.add_path(["Chicago", "Cleveland"])
    g.add_path(["Cleveland", "Buffalo", "Boston", "NewYork", "Philadelphia", "Washington"])
    g.add_path(["Cleveland", "Pittsburgh", "Ashburn", "Washington"])
    g.add_path(["Washington", "Raleigh", "Atlanta"])
    return g

def get_latency_info():
    info = None
    data_str = ""
    with open(INFO_FILE_PATH) as f:
        lines = f.readlines()
        for line in lines:
            data_str += line
    data_dict = json.loads(data_str)
    return info

class OS3ETopo(Topo):

    def __init__(self):
        Topo.__init__(self)
        self.switches = {}
        g = OS3EGraph()
        for node in g.nodes:
            self.switches[node] = self.addSwitch(node)
        for edge in g.edges:
            info = get_latency_info()
            if info is None:
                self.addLink(self.switches[edge[0]], self.switches[edge[1]])

topos = {'mytopo': (lambda: OS3ETopo())}