import networkx as nx
import json
import argparse
import matplotlib.pyplot as plt

def create_arg_parser():
    '''Creates an argument parser'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_name", type=str,
                        help="Input file to read the graph")

    args = parser.parse_args()
    return args


def read_json_file(filename):
    '''Reads the graph based on filename provided in args'''
    with open(filename) as f:
        js_graph = json.load(f)
    return nx.json_graph.node_link_graph(js_graph)

# Function to load graph from JSON file
def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    G = nx.DiGraph()
    
    # Add nodes
    for node in data['nodes']:
        G.add_node(node['id'])
    
    # Add edges
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'])
    
    return G


def get_statistics(G):
    # Calculate metrics and display results
    print("Number of vertices:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())
    print("In-degree distribution:", dict(G.in_degree()))
    print("Out-degree distribution:", dict(G.out_degree()))
    print("Centrality indices:", nx.degree_centrality(G))
    print("Clustering coefficient:", nx.clustering(G.to_undirected()))
    print("Network diameter:", nx.diameter(G.to_undirected()) if nx.is_connected(G.to_undirected()) else float('inf'))
    print("Density:", nx.density(G))
    connected_components = list(nx.weakly_connected_components(G))
    print("Number of connected components:", len(connected_components))
    print("Size of connected components:", [len(component) for component in connected_components])

def create_sample_graph():
    # Create a directed graph
    G = nx.DiGraph()

    edges = [
        (1, 2), (1, 3), (2, 3), (3, 4), 
        (4, 5), (5, 1), (5, 6), (6, 4)
        ]
    G.add_edges_from(edges)
    return G

if __name__ == '__main__':
    '''Main function to read the dataset and output information'''
    args = create_arg_parser()

    # Read file
    if args.file_name:
        G = load_graph_from_json(args.file_name)
    else:
        G=create_sample_graph()

    get_statistics(G)
    

    # Optional: Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, arrowstyle='-|>', arrowsize=20)
    plt.title("Directed Graph")
    plt.show()