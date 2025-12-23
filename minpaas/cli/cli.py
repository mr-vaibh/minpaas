import argparse
import sys
from minpaas.cli.api import MinPaasAPI


def parse_env(env_list):
    env = {}
    for item in env_list or []:
        if "=" not in item:
            raise ValueError(f"Invalid env format: '{item}'. Use KEY=value")
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

    try:
        if args.cmd == "deploy":
            env = parse_env(args.env)
            res = api.deploy(args.app, args.runtime, args.repo, env)
            print("✅ Deployed successfully")
            print("URL:", res.get("url", "-"))

        elif args.cmd == "apps":
            apps = api.list_apps()

            if not apps:
                print("No apps deployed.")
                return

            print(f"{'NAME':<15} {'RUNTIME':<8} {'STATUS':<8} URL")
            for name, app in apps.items():
                runtime = app.get("runtime", "-")
                status = app.get("status", "unknown")
                url = app.get("url", "-")
                print(f"{name:<15} {runtime:<8} {status:<8} {url}")

        elif args.cmd == "logs":
            res = api.logs(args.app)
            print(res.get("logs", "No logs available"))

        elif args.cmd == "delete":
            api.delete(args.app)
            print(f"🗑️ Deleted {args.app}")

        else:
            parser.print_help()

    except ValueError as e:
        # User input errors
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    except ConnectionError:
        # MinPaas server not reachable
        print("❌ Cannot connect to MinPaas server. Is it running?", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        # Catch-all: show message, hide traceback
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
