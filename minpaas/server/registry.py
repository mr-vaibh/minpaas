import json
import subprocess
from pathlib import Path


# project root = two levels up from this file, then out of package
PROJECT_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = PROJECT_ROOT / "state" / "apps.json"

def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def load_registry():
    with open(REGISTRY_PATH) as f:
        data = json.load(f)
    return normalize_registry(data)

def normalize_registry(data: dict) -> dict:
    for app in data.values():
        app.setdefault("runtime", "unknown")
    return data

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

def delete_app(app_name: str):
    app = get_app(app_name)
    if not app:
        return {"error": "app not found"}

    run(f"docker rm -f {app['container']}")
    remove_app(app_name)

    return {"deleted": app_name}
