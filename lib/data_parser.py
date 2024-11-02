from typing import Dict
from lib.tweet import Tweet
from lib.util import load_file
from lib.tweet_classes import TweetClass

class DataParser:
    """Parses tweet data and generates Tweet objects, including annotation classification."""
    
    def __init__(self, annotations_file: str):
        """Initializes DataParser with the annotations dictionary."""
        self.annotations = self.create_and_classify_annotations(annotations_file)

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

    def parse_tweet(self, tweet: dict, thread_id: int, event: str) -> Tweet:
        """Parses a single tweet and returns a Tweet object."""
        return Tweet.from_json(tweet, thread_id, event, self.annotations)