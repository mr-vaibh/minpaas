import subprocess
from pathlib import Path

def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clone_repo(repo_url: str, target_dir: Path):
    if target_dir.exists():
        run("git pull", cwd=target_dir)
    else:
        run(f"git clone {repo_url} {target_dir}")
