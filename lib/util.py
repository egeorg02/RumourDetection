"""
    @name: util.py
    @description: A module of utility functions used in Jupyter Notebooks
"""

import json

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