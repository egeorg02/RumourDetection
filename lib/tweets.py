import json
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

from lib.util import fix_json_file, create_and_classify_annotations

# fix_json_file("pheme-raw/annotations/en-scheme-annotations.json")
annotations_dict = create_and_classify_annotations()

class EventTweets:
    def __init__(self, event_name, output_dir="data/tweets"):
        self.event_name = event_name
        self.tweet_data_list = []
        self.output_dir = output_dir
        self.user_graph = nx.DiGraph()
        self.source_user_map = {}  # Dictionary for thread_id -> user_id
    
    def append(self, tweet, thread_id):
        def safe_int(value, default=0):
            return int(value) if value is not None else default
        
        tweet_id = tweet['id']
        tweet_class = annotations_dict.get(tweet_id, {}).get('class', 'retweet')
        user_id = tweet['user']['id']

        if tweet_class == 'source':
            self.source_user_map[thread_id] = user_id

        tweet_data = {
            'tweet_id': tweet_id,
            'thread_id': thread_id,
            'class': tweet_class,
            'in_reply_to_status_id': safe_int(tweet['in_reply_to_status_id']),
            'in_reply_to_user_id': safe_int(tweet['in_reply_to_user_id']),
            'support': annotations_dict.get(tweet_id, {}).get('support'),
            'responsetype_vs_source': annotations_dict.get(tweet_id, {}).get('responsetype-vs-source'),
            'responsetype_vs_previous': annotations_dict.get(tweet_id, {}).get('responsetype-vs-previous'),
            'favorite_count': tweet['favorite_count'],
            'retweet_count': tweet['retweet_count'],
            'favorited': tweet['favorited'],     # remove?
            'user_id': user_id,
            'created_at': tweet['created_at'],
            'place': tweet['place'],
        }
        
        self.tweet_data_list.append(tweet_data)

    def export(self):
        output_file_path = f"{self.output_dir}/{self.event_name}.csv"
        df = pd.DataFrame(data=self.tweet_data_list)
        df.to_csv(output_file_path, index=False)
        return output_file_path

    def print_data_info(self):
        print(f"Total tweets: {len(self.tweet_data_list)}")
        print(f"Event name: {self.event_name}")
        for tweet_data in self.tweet_data_list:
            print(json.dumps(tweet_data, indent=4))

    def build_user_graph(self):
        for tweet_data in self.tweet_data_list:
            tweet_class = tweet_data['class']
            user_id = tweet_data['user_id']
            in_reply_to_user_id = tweet_data['in_reply_to_user_id']
            thread_id = tweet_data['thread_id']

            # Add user as a node
            self.user_graph.add_node(user_id)

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
        plt.title(f"{self.event_name} User Interaction Network")
        plt.show()