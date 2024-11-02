from datetime import datetime
import pytz

class Tweet:
    """Represents a tweet and its metadata."""
    
    def __init__(self, thread_id: int, tweet_id: int, user_id: int, event: str, is_rumour: bool, 
                 tweet_class: str, in_reply_to_status_id: int, in_reply_to_user_id: int, support: str, 
                 responsetype_vs_source: str, responsetype_vs_previous: str, favorite_count: int, 
                 retweet_count: int, created_at, place: str, unix_ts=None, normalized_ts=None,
                 relative_ts_rumour = None, relative_ts_event=None):
        self.thread_id = thread_id
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.event = event
        self.is_rumour = is_rumour
        self.tweet_class = tweet_class
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.support = support
        self.responsetype_vs_source = responsetype_vs_source
        self.responsetype_vs_previous = responsetype_vs_previous
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count
        self.created_at = self.__parse_created_at(created_at) if isinstance(created_at, str) else created_at
        self.place = place

        # New attributes for temporal analysis
        self.unix_ts = unix_ts if unix_ts is not None else self.__get_unix_timestamp()
        self.normalized_ts = normalized_ts if normalized_ts is not None else self.__get_normalized_timestamp()
        self.relative_ts_rumour = relative_ts_rumour  # To be set later based on the start of the rumour
        self.relative_ts_event = relative_ts_event   # To be set later based on the start of the event

    def __parse_created_at(self, created_at: str) -> datetime:
        """Parse the created_at string into a datetime object."""
        return datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S%z')
        # return datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')

    def __get_unix_timestamp(self) -> float:
        """Convert created_at to Unix timestamp."""
        return self.created_at.timestamp()

    def __get_normalized_timestamp(self) -> datetime:
        """Normalize timestamp to Eastern Time (ET, UTC-5)."""
        return self.created_at.astimezone(pytz.timezone('America/New_York'))

    @staticmethod
    def from_json(tweet_json: dict, thread_id: int, event: str, is_rumour: bool, annotations: dict) -> 'Tweet':
        """Factory method to create a Tweet object from a dictionary."""
        
        def safe_int(value, default=0) -> int:
            return int(value) if value is not None else default
        
        tweet_id = safe_int(tweet_json['id'])
        
        return Tweet(
            thread_id=safe_int(thread_id),
            tweet_id=tweet_id,
            user_id=safe_int(tweet_json['user']['id']),
            event=event,
            is_rumour=is_rumour,
            tweet_class=annotations.get('tweet_class', 'retweet'),
            in_reply_to_status_id=safe_int(tweet_json.get('in_reply_to_status_id')),
            in_reply_to_user_id=safe_int(tweet_json.get('in_reply_to_user_id')),
            support=annotations.get('support'),
            responsetype_vs_source=annotations.get('responsetype_vs_source'),
            responsetype_vs_previous=annotations.get('responsetype_vs_previous'),
            favorite_count=safe_int(tweet_json.get('favorite_count')),
            retweet_count=safe_int(tweet_json.get('retweet_count')),
            created_at=tweet_json.get('created_at'),
            place=tweet_json.get('place'),
        )

    def __repr__(self):
        return f"Tweet({self.tweet_id})"