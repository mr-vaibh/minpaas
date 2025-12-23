from fastapi import FastAPI
from minpaas.server.deploy import deploy_app
from minpaas.server.registry import load_registry, delete_app
from minpaas.server.containers import container_status, container_logs

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path


app = FastAPI()

UI_DIR = Path(__file__).resolve().parents[2] / "minpaas" / "ui"

app.mount("/static", StaticFiles(directory=UI_DIR), name="static")

@app.get("/")
def ui():
    return FileResponse(UI_DIR / "index.html")

@app.post("/deploy")
@app.post("/deploy")
def deploy(payload: dict):
    return deploy_app(
        payload.get("app"),
        payload.get("runtime"),
        payload.get("repo"),
        payload.get("env"),
        payload.get("command")
    )

@app.get("/apps")
def list_apps():
    apps = load_registry()

    for app in apps.values():
        app["status"] = container_status(app["container"])

    return apps

@app.get("/apps/{app_name}/logs")
def get_app_logs(app_name: str):
    apps = load_registry()
    app = apps.get(app_name)

    if not app:
        return {"error": "app not found"}

    return {
        "logs": container_logs(app["container"])
    }

@app.delete("/apps/{app_name}")
def delete(app_name: str):
    return delete_app(app_name)