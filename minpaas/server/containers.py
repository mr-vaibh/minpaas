import subprocess


def container_status(container_name: str) -> str:
    """
    Returns:
      - running
      - exited
      - created
      - not_found
    """
    try:
        status = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Status}}", container_name],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return status
    except subprocess.CalledProcessError:
        return "not_found"


def container_logs(container_name: str, tail: int = 200) -> str:
    try:
        return subprocess.check_output(
            ["docker", "logs", "--tail", str(tail), container_name],
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        return e.output or "No logs available"
