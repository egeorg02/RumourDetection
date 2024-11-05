import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D

def draw_3d_directed_graph(graph):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Get the positions of the nodes in 3D
    pos = nx.spring_layout(graph, dim=3)

    # Draw edges
    for edge in graph.edges():
        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        z = [pos[edge[0]][2], pos[edge[1]][2]]
        ax.plot(x, y, z, color='gray')

    # Draw nodes
    xs, ys, zs = zip(*pos.values())
    ax.scatter(xs, ys, zs, color='lightblue', s=100)  # Node size

    # Set labels and title
    ax.set_title("3D Directed Graph")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")

    # Hide the axes
    ax.set_axis_off()

    plt.show()

# Example usage:
# Create a sample directed graph
G = nx.DiGraph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (2, 5), (3, 6), (4, 5)])

# Draw the 3D directed graph
draw_3d_directed_graph(G)