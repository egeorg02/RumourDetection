import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# TODO: rename script
# TODO: tidy up a bit before submitting
# TODO: different titles for graphs?

# Function to read a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def list_files_and_folders(directory):
    # List to store all files and folders
    items = []
    
    for root, dirs, files in os.walk(directory):
        # Add folders
        for file_name in files:
            items.append(os.path.join(root, file_name))
    
    return items

def collect_time_diffs(reactions, source_time):
    '''Get the time difference (in minutes) from the creation of each retweet'''
    # Parse timestamp of source time
    timestamp_format = "%a %b %d %H:%M:%S %z %Y"
    dt_source = datetime.strptime(source_time, timestamp_format)
    differences=[]
    for reaction_path in reactions:
        reaction = read_json_file(reaction_path)
        reaction_time = reaction["created_at"]
        dt_reaction = datetime.strptime(reaction_time, timestamp_format)
        diff=dt_reaction - dt_source
        diff_minutes=diff.total_seconds() / 60
        differences.append(round(diff_minutes, 3)) # 3 floating points
    return differences

def cumulative_counts_line_chart(intervals):
    cumulative_counts = np.arange(1, len(intervals) + 1)

    plt.figure(figsize=(10, 6))
    plt.step(intervals, cumulative_counts, where='post', marker='o')
    plt.title('Reply Accumulation Over Time from the Source Tweet with the Most Activity')
    plt.xlabel('Time (minutes since source tweet)')
    plt.ylabel('Cumulative Number of Replies')
    plt.grid()
    # Set x-ticks in multiples of 60
    max_time=(intervals[-1]/60 + 1) * 60
    plt.xticks(ticks=range(0, int(max_time), 60))
    # Set the limits for both axes
    plt.xlim(0)
    plt.ylim(0)
    plt.xticks(rotation=45)
    plt.show()

def histogram(intervals):
    plt.figure(figsize=(10, 6))
    # Define bin width
    bin_width = 20
    bins = np.arange(0, max(intervals) + bin_width, bin_width)

    plt.hist(intervals, bins=bins, color='skyblue', edgecolor='black')
    plt.title('Histogram of Reply Intervals from the Source Tweet with the Most Activity')
    plt.xlabel('Time (minutes since source tweet)')
    plt.ylabel('Number of Replies')
    # Set x-ticks in multiples of 60
    max_time=(intervals[-1]/60 + 1) * 60
    plt.xticks(ticks=range(0, int(max_time), 60))
    # Set the limits for both axes
    plt.xlim(0)
    plt.ylim(0)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()


# collect all related files (reactions of tweet of interest)
ego_id="544329935943237632"
path=f"phemerumourschemedataset\\threads\\en\\sydneysiege\\" + ego_id
reactions = list_files_and_folders(path+ "\\reactions")
print('Number of reactions:', len(reactions)) # should be 102

# collect created time for source
source=read_json_file(path+"\\source-tweets\\"+ego_id+".json")
source_time=source["created_at"]
print("Source created at:", source_time) # "Mon Dec 15 03:15:44 +0000 2014"

# collect created time for each reaction
intervals = collect_time_diffs(reactions, source_time)
print('10 shortest differences (minutes):', intervals[:10])

# draw the different graphs
cumulative_counts_line_chart(intervals)
histogram(intervals)
