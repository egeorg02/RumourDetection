class User:
    """Represents a Twitter user with followers, following, and their tweets."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.followers = set()  # IDs of users following this user
        self.following = set()  # IDs of users this user follows
        self.tweets = set()     # Set of tweet IDs posted by this user
    
    def add_follower(self, follower_id: int):
        """Adds a follower to this user."""
        self.followers.add(follower_id)

    def add_following(self, followee_id: int):
        """Adds a followee to this user's following list."""
        self.following.add(followee_id)

    def add_tweet(self, tweet_id: int):
        """Associates a tweet ID with this user."""
        self.tweets.add(tweet_id)