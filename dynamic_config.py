import json
import os

CONFIG_FILE = os.getenv("CONFIG_FILE", os.path.join(os.path.dirname(__file__), "data", "config.json"))
if not os.path.exists(CONFIG_FILE) and os.path.exists("/app/data/config.json"):
    CONFIG_FILE = "/app/data/config.json"

def load_dynamic_config():
    if not os.path.exists(CONFIG_FILE):
        return {"KEYWORDS": [], "TARGET_MACHINES": [], "EXCLUDE_KEYWORDS": []}
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        if "EXCLUDE_KEYWORDS" not in data:
            data["EXCLUDE_KEYWORDS"] = ["arcade", "video game", "multigame", "bartop", "cabinet", "parts"]
        return data

def save_dynamic_config(config_data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)
