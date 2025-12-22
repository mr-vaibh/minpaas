# MinPaas 🚀

_A Docker-first Mini Platform as a Service (PaaS)_

MinPaas is a **minimal, opinionated Platform as a Service** built from scratch to demonstrate how real PaaS systems work internally.

It focuses on **container lifecycle management**, **control-plane design**, and **production-grade constraints**, without unnecessary abstraction or orchestration frameworks.

> Think: _“Heroku core loop — but single-machine, transparent, and explainable.”_

----------

## Why MinPaas?

Most “Heroku clone” projects:

-   hide complexity behind frameworks
    
-   jump straight to Kubernetes
    
-   lack clear design reasoning
    

MinPaas is different.

It is designed to:

-   start from **first principles**
    
-   use **Docker as the core abstraction**
    
-   evolve incrementally
    
-   remain **interview-explainable at every step**
    

----------

## Core Principles

-   **Docker-first**: Docker is the execution boundary
    
-   **Single-machine**: no Kubernetes, no cloud dependencies
    
-   **Opinionated MVP**: constrained by design
    
-   **Control-plane driven**: MinPaas manages lifecycle, not users
    
-   **Incremental evolution**: flexibility is earned, not assumed
    

----------

## Current Capabilities (Step 2)

MinPaas currently supports:

-   Deploying Python HTTP apps as Docker containers
    
-   Deterministic port allocation
    
-   Persistent app registry
    
-   Safe redeploys
    
-   Listing deployed apps
    
-   Deleting apps and cleaning containers
    

----------

## Architecture Overview

```
Client (curl / API)
        ↓
MinPaas Control Plane (FastAPI)
        ↓
Docker CLI (subprocess)
        ↓
Docker Engine
        ↓
User App Containers

```

MinPaas acts as a **control plane**, not an app runner.

----------

## Project Structure

```
minpaas/
├── server/
│   ├── main.py        # API server (control plane)
│   ├── deploy.py      # Docker build/run lifecycle
│   └── registry.py    # Persistent app registry
├── state/
│   └── apps.json      # Control-plane state
├── apps/
│   └── hello-python/  # Example user app
│       ├── app.py
│       ├── requirements.txt
│       └── Dockerfile
└── README.md

```

----------

## Runtime Contract (Very Important)

MinPaas enforces a **strict runtime contract**.

All user applications must:

1.  Be HTTP servers
    
2.  Listen on the port provided via:
    
    ```
    PORT=<number>
    
    ```
    
3.  Run inside a platform-controlled Dockerfile
    

This mirrors real PaaS systems (Heroku, Fly.io, Railway).

----------

## Example User App

A minimal Python app:

```python
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8000))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from MinPaas")

HTTPServer(("", PORT), Handler).serve_forever()

```

----------

## Why the Dockerfile Is Platform-Owned

Users do **not** provide Dockerfiles.

Reasons:

-   predictable builds
    
-   controlled execution
    
-   simplified security model
    
-   easier debugging
    
-   realistic PaaS behavior
    

This is a deliberate design choice.

----------

## Control Plane API

### Deploy an App

```http
POST /deploy
Content-Type: application/json

{
  "app": "hello-python"
}

```

Response:

```json
{
  "app": "hello-python",
  "container": "minpaas-hello-python-container",
  "image": "minpaas-hello-python",
  "port": 34567,
  "url": "http://localhost:34567"
}

```

----------

### List Apps

```http
GET /apps

```

Response:

```json
{
  "hello-python": {
    "app": "hello-python",
    "container": "minpaas-hello-python-container",
    "image": "minpaas-hello-python",
    "port": 34567,
    "url": "http://localhost:34567"
  }
}

```

----------

### Delete an App

```http
DELETE /apps/{app_name}

```

This:

-   stops the container
    
-   removes it from Docker
    
-   deletes the registry entry
    

----------

## Persistent State

MinPaas stores control-plane state in:

```
state/apps.json

```

Stored data includes:

-   app name
    
-   Docker image
    
-   container name
    
-   assigned port
    
-   public URL
    

Why JSON?

-   single-machine deployment
    
-   human-readable
    
-   zero operational overhead
    
-   easy migration to DB later
    

----------

## Deterministic Port Allocation

Ports are assigned deterministically:

```
port = 10000 + hash(app_name) % 50000

```

This ensures:

-   stable URLs
    
-   safe redeploys
    
-   predictable behavior
    

----------

## What MinPaas Does NOT Do (Yet)

Intentionally excluded at this stage:

-   GitHub repo cloning
    
-   Custom run commands
    
-   `.env` injection
    
-   Multiple runtimes
    
-   Logs API
    
-   Reverse proxy
    
-   Authentication
    
-   Kubernetes
    

These will be added **only after the foundation is solid**.

----------

## Design Philosophy

MinPaas follows a strict rule:

> **Constraints first, flexibility later.**

This mirrors how real PaaS platforms evolve.

----------

## Roadmap

### Step 3 (Next)

-   `.env` support
    
-   Environment variable injection
    
-   Configurable per app
    
-   No rebuild required for env changes
    

### Step 4

-   Runtime abstraction (Python + Node.js)
    
-   Runtime templates
    

### Step 5

-   GitHub repo deployment
    
-   Source cloning
    
-   Rebuilds
    

### Step 6+

-   Logs
    
-   Restart policies
    
-   Reverse proxy
    
-   Multi-app routing
    
-   Buildpack-style detection
    

----------

## Why This Project Matters

MinPaas demonstrates:

-   real container lifecycle management
    
-   control-plane thinking
    
-   production constraints
    
-   senior-level system design discipline
    

This is **not a toy project**.  
It is a **minimal but real PaaS**.

----------

## Author

Built as a serious systems project by **Vaibhav Shukla**.

----------

If you want, next I can:

-   refine this README for public GitHub
    
-   add architecture diagrams
    
-   add interview Q&A explanations
    
-   proceed to Step 3 (`.env` support)
    

Say:

**`Proceed to Step 3`**