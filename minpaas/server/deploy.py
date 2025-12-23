import subprocess
import shutil
from pathlib import Path
from minpaas.server.registry import register_app, get_app
from minpaas.server.runtimes import RUNTIMES
from minpaas.server.git import clone_repo


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APPS_DIR = PROJECT_ROOT / "apps"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
RUNTIME_DIR = PROJECT_ROOT / "runtimes"


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def allocate_port(app_name: str) -> int:
    return 10000 + (abs(hash(app_name)) % 50000)

def format_env(env: dict) -> str:
    return " ".join([f"-e {k}='{v}'" for k, v in env.items()])

def deploy_app(app, runtime, repo, env=None, command=None):
    env = env or {}

    if runtime not in RUNTIMES:
        return {"error": "unsupported runtime"}

    app_dir = WORKSPACE_DIR / app
    clone_repo(repo, app_dir)

    runtime_cfg = RUNTIMES[runtime]
    start_cmd = command or runtime_cfg["default_command"]

    dockerfile_src = RUNTIME_DIR / runtime_cfg["dockerfile"]
    dockerfile_dst = app_dir / "Dockerfile"
    shutil.copy(dockerfile_src, dockerfile_dst)

    image = f"minpaas-{app}"
    container = f"{image}-container"
    port = allocate_port(app)
    internal_port = runtime_cfg["port"]

    run(f"docker build -t {image} .", app_dir)
    subprocess.run(
        f"docker rm -f {container}",
        shell=True,
        cwd=app_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    env_flags = format_env(env)

    run(
        f"docker run -d "
        f"-p {port}:{internal_port} "
        f"{env_flags} "
        f"--name {container} "
        f"{image} "
        f"sh -c \"{start_cmd}\""
    )

    record = {
        "app": app,
        "runtime": runtime,
        "repo": repo,
        "container": container,
        "image": image,
        "port": port,
        "url": f"http://localhost:{port}",
        "env": env,
        "command": start_cmd
    }

    register_app(app, record)

    # Updating NGINX configuration
    from minpaas.server.nginx import render_nginx
    render_nginx()

    return record

def get_logs(app_name: str, tail: int = 100):
    app = get_app(app_name)
    if not app:
        return {"error": "app not found"}

    container = app["container"]

    result = subprocess.run(
        f"docker logs --tail {tail} {container}",
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "app": app_name,
        "logs": result.stdout
    }