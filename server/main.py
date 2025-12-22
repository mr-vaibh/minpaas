from fastapi import FastAPI
from deploy import deploy_app
from registry import get_apps, delete_app

app = FastAPI()

@app.post("/deploy")
def deploy(payload: dict):
    return deploy_app(
        payload.get("app"),
        payload.get("runtime"),
        payload.get("env")
    )

@app.get("/apps")
def list_apps():
    return get_apps()

@app.delete("/apps/{app_name}")
def delete(app_name: str):
    return delete_app(app_name)
