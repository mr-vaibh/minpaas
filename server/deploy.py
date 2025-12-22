import subprocess
import shutil
from pathlib import Path
from registry import register_app
from runtimes import RUNTIMES


BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"
RUNTIME_DIR = BASE_DIR / "runtimes"


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def allocate_port(app_name: str) -> int:
    return 10000 + (abs(hash(app_name)) % 50000)

def format_env(env: dict) -> str:
    return " ".join([f"-e {k}='{v}'" for k, v in env.items()])

def deploy_app(app_name, runtime, env=None):
    env = env or {}

    if runtime not in RUNTIMES:
        return {"error": "unsupported runtime"}

    app_path = APPS_DIR / app_name
    if not app_path.exists():
        return {"error": "app not found"}

    runtime_cfg = RUNTIMES[runtime]
    dockerfile_src = RUNTIME_DIR / runtime_cfg["dockerfile"]
    dockerfile_dst = app_path / "Dockerfile"

    shutil.copy(dockerfile_src, dockerfile_dst)

    image = f"minpaas-{app_name}"
    container = f"{image}-container"
    port = allocate_port(app_name)
    internal_port = runtime_cfg["port"]

    run(f"docker build -t {image} .", app_path)
    run(f"docker rm -f {container}")

    run(
        f"docker run -d "
        f"-p {port}:{internal_port} "
        f"{format_env(env)} "
        f"--name {container} "
        f"{image}"
    )

    record = {
        "app": app_name,
        "runtime": runtime,
        "container": container,
        "image": image,
        "port": port,
        "url": f"http://localhost:{port}",
        "env": env
    }

    register_app(app_name, record)
    return record