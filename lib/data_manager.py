import os
import pandas as pd
from lib.user import User
from lib.tweet import Tweet

class DataManager:
    """Manages all users and tweets, providing methods to add and retrieve data."""
    
    def __init__(self):
        self.users = {}   # user_id -> User object
        self.tweets = {}  # tweet_id -> Tweet object
        self.__load_csv('tweets-data.csv')
    
    def add_user(self, user_id: int):
        """Adds a new user if they don't already exist."""
        if user_id not in self.users:
            self.users[user_id] = User(user_id)

    def get_user(self, user_id: int) -> User:
        """Retrieves a user by their ID."""
        return self.users.get(user_id)

    def add_data(self, new_tweet: Tweet):
        """Adds a tweet and associates it with the corresponding user."""
        user_id = new_tweet.user_id
        tweet_id = new_tweet.tweet_id

        # Add user if not already present
        self.add_user(user_id)
        self.users[user_id].add_tweet(tweet_id)
        
        # Store the tweet if it doesn't already exist
        if tweet_id not in self.tweets:
            self.tweets[tweet_id] = new_tweet

    def get_tweet(self, tweet_id: int) -> Tweet:
        """Retrieves a tweet by its ID."""
        return self.tweets.get(tweet_id)

    def get_tweets_by_user_id(self, user_id: int):
        """Retrieves all tweets for a specific user."""
        user = self.get_user(user_id)
        return user.tweets if user else None
    
    def __load_csv(self, file_name: str):
        file_path = f'data/tweets/{file_name}'
        if os.path.exists(file_path):
            dtype_spec = {
                'thread_id': int,
                'tweet_id': int,
                'user_id': int,
                'event': str,
                'tweet_class': str,
                'in_reply_to_status_id': int,
                'in_reply_to_user_id': int,
                'support': str,
                'responsetype_vs_source': str,
                'responsetype_vs_previous': str,
                'favorite_count': int,
                'retweet_count': int,
                'created_at': str,
                'place': str
            }
            tweets_df = pd.read_csv(file_path, dtype=dtype_spec, low_memory=False)
            for _, row in tweets_df.iterrows():
                tweet = Tweet(
                    thread_id=row['thread_id'],
                    tweet_id=row['tweet_id'],
                    user_id=row['user_id'],
                    event=row['event'],
                    tweet_class=row['tweet_class'],
                    in_reply_to_status_id=row['in_reply_to_status_id'],
                    in_reply_to_user_id=row['in_reply_to_user_id'],
                    support=row['support'],
                    responsetype_vs_source=row['responsetype_vs_source'],
                    responsetype_vs_previous=row['responsetype_vs_previous'],
                    favorite_count=row['favorite_count'],
                    retweet_count=row['retweet_count'],
                    created_at=row['created_at'],
                    place=row['place']
                )
                self.add_data(tweet)

    def save_to_csv(self, file_path: str):
        """Saves all tweets to a CSV file."""
        tweets_df = self.get_tweets_df()
        tweets_df.to_csv(file_path, index=False)
    
    def get_tweets_df(self) -> pd.DataFrame:
        """Returns all tweets as a pandas DataFrame."""
        tweet_data = [{
            'thread_id': tweet.thread_id,
            'tweet_id': tweet.tweet_id,
            'user_id': tweet.user_id,
            'event': tweet.event,
            'tweet_class': tweet.tweet_class,
            'in_reply_to_status_id': tweet.in_reply_to_status_id,
            'in_reply_to_user_id': tweet.in_reply_to_user_id,
            'support': tweet.support,
            'responsetype_vs_source': tweet.responsetype_vs_source,
            'responsetype_vs_previous': tweet.responsetype_vs_previous,
            'favorite_count': tweet.favorite_count,
            'retweet_count': tweet.retweet_count,
            'created_at': tweet.created_at,
            'place': tweet.place
        } for tweet in self.tweets.values()]
        
        return pd.DataFrame(tweet_data)
    
    def get_event_tweets_df(self, event_name: str) -> pd.DataFrame:
        """Returns a DataFrame containing tweets for a specific event."""
        tweet_data = []
        
        if not self.tweets:
            self.__load_csv(f'{event_name}.csv')

        for tweet in self.tweets.values():
            if tweet.event == event_name:
                tweet_data.append({
                    'thread_id': tweet.thread_id,
                    'tweet_id': tweet.tweet_id,
                    'user_id': tweet.user_id,
                    'event': tweet.event,
                    'tweet_class': tweet.tweet_class,
                    'in_reply_to_status_id': tweet.in_reply_to_status_id,
                    'in_reply_to_user_id': tweet.in_reply_to_user_id,
                    'support': tweet.support,
                    'responsetype_vs_source': tweet.responsetype_vs_source,
                    'responsetype_vs_previous': tweet.responsetype_vs_previous,
                    'favorite_count': tweet.favorite_count,
                    'retweet_count': tweet.retweet_count,
                    'created_at': tweet.created_at,
                    'place': tweet.place
                })    

        return pd.DataFrame(tweet_data)
    
    def __load_followers_data(self, file_path: str):
        """Loads follower relationships from a file into the DataManager."""
        with open(file_path, 'r') as f:
            for line in f:
                follower_id, followed_id = map(int, line.strip().split())
                self.add_user(follower_id)
                self.add_user(followed_id)
                self.users[follower_id].add_following(followed_id)
                self.users[followed_id].add_follower(follower_id)

    def get_users_df(self) -> pd.DataFrame:
        """Returns a DataFrame for users and their relationships."""
        followers_file = "data/who-follows-whom.dat"
        if os.path.exists(followers_file):
            self.__load_followers_data(followers_file)

        user_data = []
        for user in self.users.values():
            user_data.append({
                'user_id': user.user_id,
                'followers_count': len(user.followers),
                'following_count': len(user.following),
                'tweets_count': len(user.tweets),
                'followers': list(user.followers),
                'following': list(user.following)
            })
        return pd.DataFrame(user_data)