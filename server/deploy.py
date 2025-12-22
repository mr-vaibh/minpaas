import subprocess
from pathlib import Path
from registry import register_app, get_app, remove_app


BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"

def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def allocate_port(app_name: str) -> int:
    return 10000 + (abs(hash(app_name)) % 50000)

def format_env(env: dict) -> str:
    return " ".join([f"-e {k}='{v}'" for k, v in env.items()])

def deploy_app(app_name: str, env: dict = None):
    env = env or {}

    app_path = APPS_DIR / app_name
    if not app_path.exists():
        return {"error": "app not found"}

    image = f"minpaas-{app_name}"
    container = f"{image}-container"
    port = allocate_port(app_name)

    # build image once
    run(f"docker build -t {image} .", app_path)

    # remove old container
    run(f"docker rm -f {container}")

    env_flags = format_env(env)

    # run with env injection
    run(
        f"docker run -d "
        f"-p {port}:8000 "
        f"{env_flags} "
        f"--name {container} "
        f"{image}"
    )

    record = {
        "app": app_name,
        "container": container,
        "image": image,
        "port": port,
        "url": f"http://localhost:{port}",
        "env": env
    }

    register_app(app_name, record)
    return record

def delete_app(app_name: str):
    app = get_app(app_name)
    if not app:
        return {"error": "app not found"}

    run(f"docker rm -f {app['container']}")
    remove_app(app_name)

    return {"deleted": app_name}
