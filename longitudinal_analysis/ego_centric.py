'''
In this script we create an ego centric network for the tweet with the most activity
'''

import networkx as nx
import matplotlib.pyplot as plt
import json
import matplotlib.colors as mcolors
import numpy as np

# Define the hierarchical data
# Function to read a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def add_edges(graph, parent_id, children):
    if children: # proceed only if there are children
        for child_id, sub_children in children.items():
            graph.add_edge(parent_id, child_id)  # Add an edge from parent to child
            add_edges(graph, child_id, sub_children)  # Recursively process children

def create_graph(parent_id, children):
    graph = nx.DiGraph()
    graph.add_node(parent_id)
    add_edges(graph, parent_id, children) # recursively add children
    return graph, children

def draw_network(G, ego, degree1_nodes):
    plt.figure(figsize=(12, 10))
    plt.title(f"Egocentric network of the tweet with the most activity (ID: {ego_id})")
    pos = nx.planar_layout(G)
    nx.draw(G, pos, node_color = "lavender", 
            node_size = 100, arrowsize=5, edge_color='gray', with_labels = False) 

    options = {"node_size": 200, "node_color": "r"} 
    nx.draw_networkx_nodes(G, pos, nodelist=[ego], **options) 

    options = {"node_size": 150, "node_color": "#ADD8E6"}  # light blue for degree 1
    nx.draw_networkx_nodes(G, pos, nodelist=degree1_nodes, **options) 
    plt.show()

# get the connections of the tweet with the most activity (found via count_replies.py)
ego_id = "544329935943237632"
path=f"phemerumourschemedataset\\threads\\en\\sydneysiege\\" + ego_id+ "\\structure.json"
data=read_json_file(path)

# Define the ego node
ego_network, children = create_graph(ego_id, data[ego_id]) # TODO i can get child otherwise

# Draw the network
draw_network(ego_network, ego_id, degree1_nodes=children)