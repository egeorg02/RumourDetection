import json
import pandas as pd

from lib.util import fix_json_file, create_and_classify_annotations

# fix_json_file("pheme-raw/annotations/en-scheme-annotations.json")
annotations_dict = create_and_classify_annotations()

class EventTweets:
    def __init__(self, event_name, output_dir="data/tweets"):
        self.event_name = event_name
        self.tweet_data_list = []
        self.output_dir = output_dir
    
    def append(self, tweet, thread_id):
        def safe_int(value, default=0):
            return int(value) if value is not None else default
        
        tweet_id = tweet['id']

        tweet_data = {
            'tweet_id': tweet_id,
            'thread_id': thread_id,
            'class': annotations_dict.get(tweet_id, {}).get('class', 'retweet'),
            'in_reply_to_status_id': safe_int(tweet['in_reply_to_status_id']),
            'in_reply_to_user_id': safe_int(tweet['in_reply_to_user_id']),
            'support': annotations_dict.get(tweet_id, {}).get('support'),
            'responsetype_vs_source': annotations_dict.get(tweet_id, {}).get('responsetype-vs-source'),
            'responsetype_vs_previous': annotations_dict.get(tweet_id, {}).get('responsetype-vs-previous'),
            'favorite_count': tweet['favorite_count'],
            'retweet_count': tweet['retweet_count'],
            'favorited': tweet['favorited'],  # remove?
            'user_id': tweet['user']['id'],
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
