from fastapi import FastAPI
from minpaas.server.deploy import deploy_app, get_logs
from minpaas.server.registry import get_apps, delete_app

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
def deploy(payload: dict):
    return deploy_app(
        payload.get("app"),
        payload.get("runtime"),
        payload.get("repo"),
        payload.get("env")
    )

@app.get("/apps")
def list_apps():
    return get_apps()

@app.get("/apps/{app_name}/logs")
def logs(app_name: str):
    return get_logs(app_name)

@app.delete("/apps/{app_name}")
def delete(app_name: str):
    return delete_app(app_name)
