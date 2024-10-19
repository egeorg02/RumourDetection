"""
    @name: util.py
    @description: A module of utility functions used in Jupyter Notebooks
"""

import json
import pandas as pd

def fix_json_file(file_path):
    """Fix the JSON file by adding brackets and commas."""

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        # Remove any existing comments
        lines = [line for line in lines if not line.strip().startswith("#")]
        
        # Add commas between lines and wrap with brackets
        fixed_json = "[\n" + ",\n".join(line.strip() for line in lines) + "\n]"
        
        with open(file_path, "w") as file:
            file.write(fixed_json)
        
        print(f"Fixed JSON file saved to {file_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

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

def create_and_classify_annotations():
    """Create a dictionary for quick lookups and classify tweets."""
    
    annotations = load_file("pheme-raw/annotations/en-scheme-annotations.json")
    print(f"Number of annotations: {len(annotations)}")
    
    def classify(item):
        if item.get("support"):
            return "source"
        elif item.get("responsetype-vs-source") and item.get("responsetype-vs-previous"):
            return "deep reply"
        elif item.get("responsetype-vs-source"):
            return "direct reply"
        return "unknown"
    
    # Key is tweet ID: int
    annotations_dict = {
        int(item["tweetid"]): {
            "class": classify(item),
            "support": item.get("support"),
            "responsetype-vs-source": item.get("responsetype-vs-source"),
            "responsetype-vs-previous": item.get("responsetype-vs-previous")
        }
        for item in annotations
    }
    
    return annotations_dict
