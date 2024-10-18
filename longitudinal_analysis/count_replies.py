'''
Finds the number of replies for each source tweet, in order to find the one with the most activity
'''

import json
from collections import defaultdict


def count_replies(data):
    reply_counts = defaultdict(lambda: {'direct': 0, 'deep': 0})

    # Capture events from source tweets
    for tweet in data['source_tweets']:
        thread_id = tweet['threadid']
        reply_counts[thread_id]['event'] = tweet['event']  # Store event from source tweet

    # Count direct replies
    for reply in data['direct_replies']:
        thread_id = reply['threadid']
        reply_counts[thread_id]['direct'] += 1

    # Count deep replies
    for reply in data['deep_replies']:
        thread_id = reply['threadid']
        reply_counts[thread_id]['deep'] += 1

    # Calculate total replies and prepare list for sorting
    sorted_counts = []
    for thread_id, counts in reply_counts.items():
        total_replies = counts['direct'] + counts['deep']
        sorted_counts.append((thread_id, counts['direct'], counts['deep'], total_replies, counts['event']))

    # Sort by total replies
    sorted_counts.sort(key=lambda x: x[3], reverse=True)  # Sort by total replies

    return sorted_counts

# Function to read a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

data = read_json_file("phemerumourschemedataset\\annotations\\en-scheme-annotations.json")
reply_summary = count_replies(data)[:10] # get the top 10

# Print the results
for thread_id, direct_count, deep_count, total_count, event in reply_summary:
    print(f"Thread ID: {thread_id}, Event: {event}, Direct Replies: {direct_count}, Deep Replies: {deep_count}, Total Replies: {total_count}")