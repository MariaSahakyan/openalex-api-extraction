import json

def save_json(data, filename):
    """Save dictionary/list to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    """Load a JSON file."""
    with open(filename, "r") as f:
        return json.load(f)
