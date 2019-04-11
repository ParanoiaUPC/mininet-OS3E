import geo
import networkx as nx
import json
import string
import os


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


def write_json_file(filename, data):
    '''Given JSON data, write to file.'''
    json_file = open(filename, 'w')
    json.dump(data, json_file, indent = 4)


def read_json_file(filename):
    input_file = open(filename, 'r')
    return json.load(input_file)


METERS_TO_MILES = 0.000621371192
LATLONG_FILE = "os3e_latlong.json"


def lat_long_pair(node):
    return (float(node["Latitude"]), float(node["Longitude"]))


def dist_in_miles(data, src, dst):
    '''Given a dict of names and location data, compute mileage between.'''
    src_pair = lat_long_pair(data[src])
    src_loc = geo.xyz(src_pair[0], src_pair[1])
    dst_pair = lat_long_pair(data[dst])
    dst_loc = geo.xyz(dst_pair[0], dst_pair[1])
    return geo.distance(src_loc, dst_loc) * METERS_TO_MILES


def OS3EWeightedGraph():
    data = {}
    g = OS3EGraph()
    longit = {}
    lat = {}
    # Get locations
    if os.path.isfile(LATLONG_FILE):
        print("Using existing lat/long file")
        data = read_json_file(LATLONG_FILE)
    else:
        return g

    for node in g.nodes():
        latit = float(data[node]["Latitude"])
        lon = float(data[node]["Longitude"])
        lat[node] = latit
        longit[node] = lon
    nx.set_node_attributes(g, lat, 'Latitude')
    nx.set_node_attributes(g, longit, 'Longitude')

    # Append weights
    for src, dst in g.edges():
        g[src][dst]["weight"] = dist_in_miles(data, src, dst)
        #print "%s to %s: %s" % (src, dst, g[src][dst]["weight"])
    return g
