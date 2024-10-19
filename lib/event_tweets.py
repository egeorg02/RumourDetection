import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from itertools import takewhile
from networkx.algorithms.community import greedy_modularity_communities, girvan_newman
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.centrality import betweenness_centrality

class EventTweets:
    def __init__(self, event):
        self.event = event
        self.user_graph = nx.DiGraph()
        self.source_user_map = {}                           # Dictionary for thread_id -> user_id
        self.tweet_data_df = self.load_tweets_from_csv()
    
    def load_tweets_from_csv(self):
        file_path = f"data/tweets/{self.event}.csv"
        dtype = {
            "tweet_id": int,
            "thread_id": int,
            "class": str,
            "in_reply_to_status_id": int,
            "in_reply_to_user_id": int,
            "support": str,
            "responsetype-vs-source": str,
            "responsetype-vs-previous": str,
            "favorite_count": int,
            "retweet_count": int,
            "user_mentions": int,
            "favorited": bool,
            "user_id": int,
            "created_at": str,
            "place": str,
        }
    
        return pd.read_csv(file_path, dtype=dtype, engine="python")
    
    def get_tweets(self):
        return self.tweet_data_df

    def build_user_graph(self):
        for _, tweet in self.tweet_data_df.iterrows():
            tweet_class = tweet['class']
            user_id = tweet['user_id']
            in_reply_to_user_id = tweet['in_reply_to_user_id']
            thread_id = tweet['thread_id']

            # Add user as a node
            self.user_graph.add_node(user_id)

            # Record the user ID of the source tweet
            if tweet_class == 'source':
                self.source_user_map[thread_id] = user_id

            # Add edge based on user interaction pointing towards the user of the original tweet
            if tweet_class == 'direct reply' or tweet_class == 'deep reply':
                self.user_graph.add_edge(user_id, in_reply_to_user_id)
            elif tweet_class == 'retweet':
                source_user_id = self.source_user_map.get(thread_id)
                self.user_graph.add_edge(user_id, source_user_id)

    def analyze_communities(self):
        communities = list(greedy_modularity_communities(self.user_graph))
        print(f"Number of communities: {len(communities)}")
        for i, community in enumerate(communities):
            print(f"Community {i + 1}: {community}")

    def visualize_user_network(self):
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(self.user_graph, k=0.1)
        nx.draw(self.user_graph, pos, with_labels=True, node_size=50, font_size=8, font_color="black", edge_color="gray")
        plt.title("User Interaction Network")
        plt.show()
