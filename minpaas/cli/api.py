import requests

DEFAULT_BASE_URL = "http://localhost:4000"

class MinPaasAPI:
    def __init__(self, base_url=DEFAULT_BASE_URL):
        self.base_url = base_url

    def deploy(self, app, runtime, repo, env):
        r = requests.post(
            f"{self.base_url}/deploy",
            json={
                "app": app,
                "runtime": runtime,
                "repo": repo,
                "env": env,
            },
        )
        r.raise_for_status()
        return r.json()

    def list_apps(self):
        r = requests.get(f"{self.base_url}/apps")
        r.raise_for_status()
        return r.json()

    def logs(self, app):
        r = requests.get(f"{self.base_url}/apps/{app}/logs")
        r.raise_for_status()
        return r.json()

    def delete(self, app):
        r = requests.delete(f"{self.base_url}/apps/{app}")
        r.raise_for_status()
        return r.json()
