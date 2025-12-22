from fastapi import FastAPI
from deploy import deploy_app, delete_app
from registry import get_apps

app = FastAPI()

@app.post("/deploy")
def deploy(payload: dict):
    return deploy_app(
        payload.get("app"),
        payload.get("env")
    )

@app.get("/apps")
def list_apps():
    return get_apps()

@app.delete("/apps/{app_name}")
def delete(app_name: str):
    return delete_app(app_name)
