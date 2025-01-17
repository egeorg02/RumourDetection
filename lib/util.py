"""
    @name: util.py
    @description: A module of utility functions used in Jupyter Notebooks
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
from lib.enums import TweetClass, TweetTypeColorMap

def fix_json_file(file_path):
    """Fix the JSON file by adding brackets and commas."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        # Remove any existing comments
        lines = [line for line in lines if not line.strip().startswith("#")]
        
        # Add commas between lines and wrap with brackets
        fixed_json = "[\n" + ",\n".join(line.strip() for line in lines) + "\n]"
        
        with open(file_path, "w") as file:
            file.write(fixed_json)
        
        print(f"Fixed JSON file saved to {file_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def load_file(file_path):
    """Load JSON file."""
    try:
        with open(file_path) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file: {file_path}")
        print(f"JSONDecodeError: {e}")
        print("Attempting to fix the JSON file...")
        
        # Attempt to fix the JSON file
        fix_json_file(file_path)
        
        # Try loading the file again
        try:
            with open(file_path) as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON after fixing: {file_path}")
            print(f"JSONDecodeError: {e}")
            return []

def build_tweet_graph(tweets_df):
    tweet_graph = nx.DiGraph()

    for _, tweet in tweets_df.iterrows():
        tweet_id = tweet['tweet_id']
        thread_id = tweet['thread_id']
        tweet_class = tweet['tweet_class']
        in_reply_to_status_id = tweet['in_reply_to_status_id']

        if tweet_id not in tweet_graph:
            tweet_graph.add_node(tweet_id, tweet_class=tweet_class)

        # Edge represents a reply or retweet directed to the source tweet
        if tweet_class == TweetClass.DIRECT_REPLY.value or tweet_class == TweetClass.DEEP_REPLY.value:
            tweet_graph.add_edge(tweet_id, in_reply_to_status_id)
        elif tweet_class == TweetClass.RETWEET.value:
            tweet_graph.add_edge(tweet_id, thread_id)

    return tweet_graph

def draw_tweet_network(tweet_graph):
    """Draw the tweet network graph with the corresponding color map, red if the class in unknown."""
    node_colors = []
    for node in tweet_graph.nodes:
        tweet_class = tweet_graph.nodes[node].get('tweet_class', TweetClass.UNKNOWN.value)
        node_colors.append(TweetTypeColorMap.get(TweetClass(tweet_class), 'red'))

    # Draw the graph
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(tweet_graph, k=0.1)
    nx.draw(tweet_graph, pos, with_labels=True, node_size=50, node_color=node_colors, font_size=8, font_color="black", edge_color="gray")
    plt.title("Tweets Network")
    plt.show()