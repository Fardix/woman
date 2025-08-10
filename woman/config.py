import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "woman")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def save_api_key(key):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": key}, f)

def load_api_key():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f).get("api_key")
    except FileNotFoundError:
        return None
