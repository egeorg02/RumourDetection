import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout

# TODO: tidy up & check code again, if we will keep it :)

events = {
    "putinmissing": {"colour": "#C62828", "descr": "Putin missing"},
    "charliehebdo": {"colour": "#1565C0", "descr": "Charlie Hebdo shooting"},
    "prince-toronto": {"colour": "#388E3C", "descr": "Prince to play in Toronto"},
    "ferguson": {"colour": "#6A1B9A", "descr": "Ferguson unrest"},
    "germanwings-crash": {"colour": "#E65100", "descr": "Germanwings plane crash"},
    "ottawashooting": {"colour": "#00796B", "descr": "Ottawa shooting"},
    "sydneysiege": {"colour": "#4E342E", "descr": "Sydney siege"},
    "gurlitt": {"colour": "#D81B60", "descr": "Gurlitt collection"},
    "ebola-essien": {"colour": "#F57F17", "descr": "Michael Essien contracted Ebola"}
}

def list_files_and_folders(directory):
    # List to store all files and folders
    items = []
    
    for root, dirs, files in os.walk(directory):
        # Add folders
        for dir_name in dirs:
            items.append(os.path.join(root, dir_name))
        # Add files
        for file_name in files:
            items.append(os.path.join(root, file_name))
    
    return items

def get_direct_children(folder_path):
    try:
        # List all entries in the folder
        entries = os.listdir(folder_path)
        
        # Filter out only directories
        children = [entry for entry in entries if os.path.isdir(os.path.join(folder_path, entry))]
        
        return children
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
# Function to recursively add edges to the graph
def add_edges(graph, parent_id, children, parent_colour):
    child_color = lighten_color(parent_colour, 0.1) # each child is 10% brighter than its parent
    if children: # proceed only if there are children
        for child_id, sub_children in children.items():
            graph.add_edge(parent_id, child_id)  # Add an edge from parent to child
            graph.nodes[child_id]['color'] = child_color  # Set child's color
            add_edges(graph, child_id, sub_children, child_color)  # Recursively process children

def create_graph(graph, parent_id, children, parent_colour):
    G.add_node(parent_id, color=parent_colour)
    graph.nodes[parent_id]['color'] = parent_colour  # Set parent's color (source)
    add_edges(graph, parent_id, children, parent_colour) # recursively add children

# Function to read a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def draw_graph (graph, event):
    plt.figure(figsize=(10, 6))# (12, 10))
    pos=nx.spring_layout(G)
    plt.title(f"Tweet replies for {event}", fontsize=10)
    nx.draw(graph,
        pos = pos,
        with_labels=False,
        node_color=[graph.nodes[node]['color'] for node in graph.nodes],
        edge_color='gray',
        node_size=20,
        arrowstyle='-|>',
        arrowsize=3)
    plt.axis('off')  # Optionally turn off the axis
    plt.show()

def draw_arrow(start, end, ax, color='gray'):
    """Draw a 3D arrow from start to end."""
    # Draw a line for the arrow
    ax.quiver(start[0], start[1], start[2], 
               end[0] - start[0], end[1] - start[1], end[2] - start[2], 
               color=color, arrow_length_ratio=0.1)

def draw_3d_directed_graph(graph):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Get the positions of the nodes in 3D
    pos = nx.spring_layout(graph, dim=3)

    # Draw edges as arrows
    for edge in graph.edges():
        start = pos[edge[0]]
        end = pos[edge[1]]
        draw_arrow(start, end, ax, color='gray')

    # Draw nodes
    xs, ys, zs = zip(*pos.values())
    ax.scatter(xs, ys, zs, 
               #color='lightblue', 
               s=100)  # Node size

    # Set labels and title
    ax.set_title("3D Directed Graph")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")

    # Hide the axes
    ax.set_axis_off()

    plt.show()

def lighten_color(color, amount=0.3):
    """
    Lighten a given color by a specified amount.
    
    Parameters:
    - color: The original color (can be a name, hex, or RGB tuple).
    - amount: The amount to lighten (0 - 1).
    
    Returns:
    - Lightened color in RGBA format.
    """
    # Convert the color to RGBA
    rgba = mcolors.to_rgba(color)
    # Lighten the color
    lightened_color = [(1 - amount) * c + amount for c in rgba[:3]] + [rgba[3]]  # Preserve alpha
    return lightened_color    

if __name__ == '__main__':
    # Specify the directory you want to list
    directory_path = 'phemerumourschemedataset\\threads'
    languages=['en'] # TODO: add de?
    for lan in languages:
        lan_path = os.path.join(directory_path, lan)
        for event in events:
            # Create a directed graph for each event
            G = nx.DiGraph()
            center_nodes=[]
            print('---------------- EVENT -----------------', event)
            event_path = os.path.join(lan_path, event)
            sources = get_direct_children(event_path)
            for source in sources:
                source_conversation = os.path.join(event_path, source, 'structure.json')
                print(source_conversation)
                # Populate the graph with edges
                json_data=read_json_file(source_conversation)
                for parent_id, children in json_data.items():
                    create_graph(G, parent_id, children, events[event]["colour"])
                    center_nodes.append(parent_id) # TODO: remove?
            # Draw the graph
            draw_graph(G, events[event]["descr"])
            # draw_3d_directed_graph(G)
    
