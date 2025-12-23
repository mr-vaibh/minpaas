from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = PROJECT_ROOT / "state" / "apps.json"
NGINX_DIR = PROJECT_ROOT / "nginx"
NGINX_APPS = NGINX_DIR / "apps.conf"

def render_nginx():
    with open(STATE_FILE) as f:
        apps = json.load(f)

    lines = [
        "map $host $upstream {",
        "  default \"\";"
    ]

    for app in apps.values():
        host = f"{app['app']}.localhost"
        lines.append(f"  {host} 127.0.0.1:{app['port']};")

    lines.append("}")

    NGINX_APPS.write_text("\n".join(lines))
