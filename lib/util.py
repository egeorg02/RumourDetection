"""
    @name: util.py
    @description: A module of utility functions used in Jupyter Notebooks
"""

import json
import pandas as pd

def load_file(file_path):
    """Load JSON file."""
    try:
        with open(file_path) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file: {file_path}")
        print(f"JSONDecodeError: {e}")
        return []

def fetch_tweets(event):
    file_path = f"data/tweets/{event}.csv"
    dtype = {
        "tweet_id": int,
        "thread_id": int,
        "class": str,
        "support": str,
        "responsetype-vs-source": str,
        "responsetype-vs-previous": str,
        "favorite_count": int,
        "retweeted": bool,
        "retweet_count": int,
        "in_reply_to_user_id": str,
        "favorited": bool,
        "user_id": int,
        "created_at": str,
        "place": str,
    }
    
    return pd.read_csv(file_path, dtype=dtype, engine="python")