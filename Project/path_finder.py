import osmnx as ox
import networkx as nx

def calculate_route(start_coords, end_coords):
    G = ox.graph_from_point(start_coords, dist=1000, network_type='walk')
    orig_node = ox.nearest_nodes(G, start_coords[1], start_coords[0])
    dest_node = ox.nearest_nodes(G, end_coords[1], end_coords[0])
    shortest_path = nx.shortest_path(G, orig_node, dest_node, weight='length')
    path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
    return path_coords
