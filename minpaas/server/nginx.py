from pathlib import Path
import subprocess
from minpaas.server.registry import load_registry

NGINX_APPS_CONF = Path("nginx/conf.d/apps.map.conf")


def regenerate_nginx_config():
    apps = load_registry()

    blocks = []

    for name, app in apps.items():
        port = app.get("port")
        if not port:
            continue

        blocks.append(f"""
server {{
    listen 80;
    server_name {name}.localhost;

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
""")

    NGINX_APPS_CONF.write_text("\n".join(blocks))

    subprocess.run(
        ["sudo", "nginx", "-s", "reload"],
        check=True
    )
