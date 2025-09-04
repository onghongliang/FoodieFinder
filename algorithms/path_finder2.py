import osmnx as ox
import networkx as nx
from algorithms.dijkstra import dijkstra

def calculate_route_custom(start_coords, end_coords):
    # Load the graph data around the start point
    G = ox.graph_from_point(start_coords, dist=20000, network_type='walk')

    # Find the nearest nodes to the start and end points
    orig_node = ox.nearest_nodes(G, start_coords[1], start_coords[0])
    dest_node = ox.nearest_nodes(G, end_coords[1], end_coords[0])

    # Extract nodes and edges for your custom algorithm
    nodes = list(G.nodes(data=True))
    edges = list(G.edges(data=True))

    # Use your custom Dijkstra algorithm to find the shortest path
    shortest_path = dijkstra(nodes, edges, orig_node, dest_node)

    # Extract coordinates of the path
    path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
    return path_coords
