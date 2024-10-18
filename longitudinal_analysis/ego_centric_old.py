'''
In this script we create an ego centric network for the tweet with the most activity
'''

import networkx as nx
import matplotlib.pyplot as plt
import json

# Define the hierarchical data
# Function to read a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_ego_network(data, ego_id):
    ego_network = {
        "ego": ego_id,
        "1st_degree_connections": [],
        "1.5_degree_connections": {}
    }

    first_degree = data.get(ego_id, {})
    for connection_id in first_degree.keys():
        ego_network["1st_degree_connections"].append(connection_id)
        if first_degree[connection_id]: # check if there are replies to this tweet
            ego_network["1.5_degree_connections"][connection_id] = list(first_degree[connection_id].keys())

    return ego_network

def draw_network(ego_network, degree):
    G = nx.DiGraph()
    
    ego_id = ego_network["ego"]
    G.add_node(ego_id)

    for first_degree in ego_network["1st_degree_connections"]:
        G.add_node(first_degree)
        G.add_edge(ego_id, first_degree)

        for second_degree in ego_network["1.5_degree_connections"].get(first_degree, []):
            G.add_node(second_degree)
            G.add_edge(first_degree, second_degree)

    # Create an ego graph for the specified ego node
    ego_g = nx.ego_graph(G, ego_id, radius=degree)

    pos = nx.spring_layout(ego_g)
    plt.figure(figsize=(12, 8))
    plt.title(f"Ego-Centric Network for Node {ego_id} for degree {degree}")
    nx.draw(ego_g, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=8, font_color='black', font_weight='bold', arrows=True)
    plt.show()

# get the connections of the tweet with the most activity (found via count_replies.py)
path="phemerumourschemedataset\\threads\\en\\sydneysiege\\544329935943237632\structure.json"
data=read_json_file(path)

# Define the ego node
ego_id = "544329935943237632"
ego_network = extract_ego_network(data, ego_id)

# Print the structured ego network
print(json.dumps(ego_network, indent=4))

# Draw the network
draw_network(ego_network, degree=1)
draw_network(ego_network, degree=1.5)
draw_network(ego_network, degree=2)