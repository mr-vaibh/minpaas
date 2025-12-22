import argparse
from minpaas.cli.api import MinPaasAPI

def parse_env(env_list):
    env = {}
    for item in env_list or []:
        k, v = item.split("=", 1)
        env[k] = v
    return env

def main():
    parser = argparse.ArgumentParser("minpaas")
    sub = parser.add_subparsers(dest="cmd")

    deploy = sub.add_parser("deploy")
    deploy.add_argument("--app", required=True)
    deploy.add_argument("--runtime", required=True, choices=["python", "node"])
    deploy.add_argument("--repo", required=True)
    deploy.add_argument("--env", action="append")

    sub.add_parser("apps")

    logs = sub.add_parser("logs")
    logs.add_argument("app")

    delete = sub.add_parser("delete")
    delete.add_argument("app")

    args = parser.parse_args()
    api = MinPaasAPI()

    if args.cmd == "deploy":
        env = parse_env(args.env)
        res = api.deploy(args.app, args.runtime, args.repo, env)
        print("✅ Deployed")
        print("URL:", res["url"])

    elif args.cmd == "apps":
        apps = api.list_apps()
        for name, app in apps.items():
            runtime = app.get("runtime", "unknown")
            url = app.get("url", "-")
            print(f"{name:<15} {runtime:<8} {url}")

    elif args.cmd == "logs":
        print(api.logs(args.app)["logs"])

    elif args.cmd == "delete":
        api.delete(args.app)
        print(f"🗑️ Deleted {args.app}")

    else:
        parser.print_help()
