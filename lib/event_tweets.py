import pandas as pd
import networkx as nx
from lib.user import User

class EventTweets:
    def __init__(self, event):
        self.event = event
        self.user_graph = nx.DiGraph()
        self.source_user_map = {}           # Dictionary for thread_id -> user_id
        self.users = {}                     # Dictionary for user_id -> User object
        self.tweet_data_df = self.load_tweets_from_csv()
        self.build_user_graph()
    
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
    
        tweet_data_df = pd.read_csv(file_path, dtype=dtype, engine="python")
        
        # Populate users dictionary
        for _, tweet in tweet_data_df.iterrows():
            user_id = tweet['user_id']
            if user_id not in self.users:
                self.users[user_id] = User(user_id)
        
        return tweet_data_df
    
    def get_tweets(self):
        return self.tweet_data_df
    
    def get_tweet_info(self, tweet_id):
        tweet_info = self.tweet_data_df[self.tweet_data_df['tweet_id'] == tweet_id]
        if tweet_info.empty:
            return f"No tweet found with tweet_id: {tweet_id}"
        return tweet_info.to_dict('records')[0]
    
    def get_tweets_by_user_id(self, user_id):
        user_tweets = self.tweet_data_df[self.tweet_data_df['user_id'] == user_id]
        if user_tweets.empty:
            return f"No tweets found for user_id: {user_id}"
        return user_tweets.to_dict('records')

    def build_user_graph(self):
        for _, tweet in self.tweet_data_df.iterrows():
            tweet_id = tweet['tweet_id']
            tweet_class = tweet['class']
            user_id = tweet['user_id']
            in_reply_to_user_id = tweet['in_reply_to_user_id']
            thread_id = tweet['thread_id']

            # Add user as a node with tweet_id and tweet_class as attributes
            if user_id not in self.user_graph:
                self.user_graph.add_node(user_id, tweet_id=tweet_id, tweet_class=tweet_class)

            # Record the user ID of the source tweet
            if tweet_class == 'source':
                self.source_user_map[thread_id] = user_id

            # Add edge based on user interaction pointing towards the user of the original tweet
            if tweet_class == 'direct reply' or tweet_class == 'deep reply':
                self.user_graph.add_edge(user_id, in_reply_to_user_id)
            elif tweet_class == 'retweet':
                source_user_id = self.source_user_map.get(thread_id)
                self.user_graph.add_edge(user_id, source_user_id)

    def get_user_graph(self):
        return self.user_graph