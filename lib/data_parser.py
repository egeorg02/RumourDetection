import os
import pandas as pd
from typing import Dict
from lib.tweet import Tweet
from lib.util import load_file
from lib.tweet_classes import TweetClass

class DataParser:
    """Parses tweet data and generates Tweet objects, including annotation classification."""
    
    def __init__(self, annotations_file: str):
        """Initializes DataParser with the annotations dictionary."""
        self.annotations = self.create_and_classify_annotations(annotations_file)
        self.is_rumour_dict = {}

    def create_and_classify_annotations(self, file_path: str) -> Dict[int, dict]:
        """Create a dictionary for quick lookups and classify tweets based on annotations."""
        
        annotations = load_file(file_path)
        print(f"Number of annotations: {len(annotations)}")
        
        def classify(item):
            if item.get("support"):
                return TweetClass.SOURCE
            elif item.get("responsetype-vs-source") and item.get("responsetype-vs-previous"):
                return TweetClass.DEEP_REPLY
            elif item.get("responsetype-vs-source"):
                return TweetClass.DIRECT_REPLY
            else:
                print(f"Unknown tweet class: {item}")
                return TweetClass.UNKNOWN
        
        # Key is tweet ID: int
        annotations_dict = {
            int(item["tweetid"]): {
                "tweet_class": classify(item).value,
                "support": item.get("support"),
                "responsetype_vs_source": item.get("responsetype-vs-source"),
                "responsetype_vs_previous": item.get("responsetype-vs-previous")
            }
            for item in annotations
        }
        
        return annotations_dict
    
    def add_thread_annotation(self, annotation_file:str, thread_id: int):
        """Add annotations for a specific thread."""
        if os.path.exists(annotation_file):
            thread_annotations = load_file(annotation_file)
            if thread_annotations['is_rumour'] == 'rumour':
                self.is_rumour_dict[thread_id] = True
            else:
                self.is_rumour_dict[thread_id] = False

    def parse_tweet(self, tweet: dict, thread_id: int, event_name: str) -> Tweet:
        """Parses a single tweet and returns a Tweet object."""
        is_rumour = self.is_rumour_dict.get(thread_id, False)
        annotation = self.annotations.get(tweet['id'], {})
        return Tweet.from_json(tweet, thread_id, event_name, is_rumour, annotation)

    def calculate_relative_ts(self, tweets: Dict[int, Tweet]):
        """Calculate relative timestamps for tweets in a dictionary."""
        tweets_df = pd.DataFrame([{
            'tweet_id': tweet_id,
            'event': tweet.event,
            'is_rumour': tweet.is_rumour,
            'tweet_class': tweet.tweet_class,
            'unix_ts': tweet.unix_ts
        } for tweet_id, tweet in tweets.items()])
        
        # Calculate relative timestamps for each event
        for event, group in tweets_df.groupby('event'):
            # Find the earliest source tweet that is a rumour
            rumour_start_time = group[group['is_rumour'] & (group['tweet_class'] == TweetClass.SOURCE.value)]['unix_ts'].min()
            
            # Find the earliest tweet in the event
            event_start_time = group['unix_ts'].min()
            
            # Calculate relative timestamps
            tweets_df.loc[group.index, 'relative_ts_rumour'] = group['unix_ts'] - rumour_start_time
            tweets_df.loc[group.index, 'relative_ts_event'] = group['unix_ts'] - event_start_time
        
        # Update the Tweet objects with the calculated relative timestamps
        for _, row in tweets_df.iterrows():
            tweet_id = row['tweet_id']
            tweets[tweet_id].relative_ts_rumour = row['relative_ts_rumour']
            tweets[tweet_id].relative_ts_event = row['relative_ts_event']