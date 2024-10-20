class Tweet:
    """Represents a tweet and its metadata."""
    
    def __init__(self, thread_id: str, tweet_id: int, user_id: int, event: str, tweet_class: str, 
                 in_reply_to_status_id: int, in_reply_to_user_id: int, support: str, 
                 responsetype_vs_source: str, responsetype_vs_previous: str, favorite_count: int, 
                 retweet_count: int, created_at: str, place: str):
        self.thread_id = thread_id
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.event = event
        self.tweet_class = tweet_class
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.support = support
        self.responsetype_vs_source = responsetype_vs_source
        self.responsetype_vs_previous = responsetype_vs_previous
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count
        self.created_at = created_at
        self.place = place

    @staticmethod
    def from_json(tweet_json: dict, thread_id: int, event: str, annotations: dict) -> 'Tweet':
        """Factory method to create a Tweet object from a dictionary."""
        
        def safe_int(value, default=0):
            return int(value) if value is not None else default
        
        # Debugging: Check the type of tweet_json
        if not isinstance(tweet_json, dict):
            print(f"tweet_json is not a dictionary: {tweet_json}")

        tweet_id = safe_int(tweet_json['id'])
        
        return Tweet(
            thread_id=safe_int(thread_id),
            tweet_id=tweet_id,
            user_id=safe_int(tweet_json['user']['id']),
            event=event,
            tweet_class=annotations.get(tweet_id, {}).get('tweet_class', 'retweet'),
            in_reply_to_status_id=safe_int(tweet_json.get('in_reply_to_status_id')),
            in_reply_to_user_id=safe_int(tweet_json.get('in_reply_to_user_id')),
            support=annotations.get(tweet_id, {}).get('support'),
            responsetype_vs_source=annotations.get(tweet_id, {}).get('responsetype_vs_source'),
            responsetype_vs_previous=annotations.get(tweet_id, {}).get('responsetype_vs_previous'),
            favorite_count=safe_int(tweet_json.get('favorite_count')),
            retweet_count=safe_int(tweet_json.get('retweet_count')),
            created_at=tweet_json.get('created_at'),
            place=tweet_json.get('place')
        )
