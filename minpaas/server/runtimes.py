RUNTIMES = {
    "python": {
        "dockerfile": "python/Dockerfile",
        "port": 8000,
        "default_command": "python app.py"
    },
    "node": {
        "dockerfile": "node/Dockerfile",
        "port": 3000,
        "default_command": "npm start"
    }
}
