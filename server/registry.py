import json
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "state" / "apps.json"

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def save_registry(data):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def register_app(app_name, record):
    data = load_registry()
    data[app_name] = record
    save_registry(data)

def remove_app(app_name):
    data = load_registry()
    if app_name in data:
        del data[app_name]
        save_registry(data)

def get_apps():
    return load_registry()

def get_app(app_name):
    return load_registry().get(app_name)
