# MinPaas 🚀

**A Docker-First Mini Platform as a Service (PaaS)**

MinPaas is a **minimal, production-oriented Platform as a Service** built from first principles to demonstrate how real PaaS systems work internally.

It focuses on **container lifecycle management**, **control-plane design**, and **incremental platform evolution**, without Kubernetes or unnecessary abstraction.

> Think: *the core of Heroku / Railway / Fly.io — but transparent, single-node, and explainable.*

---

## Why MinPaas?

Most “Heroku clone” projects:

* jump straight to Kubernetes
* hide logic behind frameworks
* skip lifecycle and state management
* are hard to explain in interviews

MinPaas takes the opposite approach:

* Docker is the **only execution abstraction**
* Everything runs on a **single machine**
* Each feature is added **only when justified**
* Every design decision is **explainable**

This makes MinPaas a **systems & platform engineering project**, not just a demo.

---

## Core Principles

* **Docker-first** — containers are the runtime boundary
* **Single-node** — no Kubernetes, no cloud lock-in
* **Opinionated builds** — platform owns Dockerfiles
* **Control-plane driven** — explicit lifecycle management
* **Incremental evolution** — flexibility is earned, not assumed

---

## What MinPaas Can Do (v0.1.0)

MinPaas currently supports:

* Python and Node.js runtimes
* GitHub-based deployments
* Platform-owned Docker build templates
* Environment variable injection
* Deterministic port allocation
* Safe redeploys
* Persistent control-plane state
* Application logs via API
* Fully working CLI client

This is the **minimum complete PaaS core**.

---

## High-Level Architecture

```
CLI / Web Client
        ↓
MinPaas Control Plane (FastAPI)
        ↓
Docker CLI
        ↓
Docker Engine
        ↓
Application Containers
```

MinPaas is a **control plane**, not an app framework.

---

## Project Structure

```
minpaas/
├── minpaas/              # Python package
│   ├── server/           # Control plane (FastAPI)
│   └── cli/              # CLI client
├── runtimes/             # Runtime Dockerfile templates
├── workspace/            # Cloned GitHub repos (runtime)
├── state/                # Control-plane state (runtime)
├── pyproject.toml
└── README.md
```

Only `minpaas/` is packaged as Python code.
All other directories are runtime data, by design.

---

## Runtime Contract

All deployed applications must:

1. Run as an HTTP server
2. Listen on the port provided via `PORT`
3. Conform to the selected runtime’s expectations

This mirrors real PaaS platforms like Heroku and Fly.io.

### Supported runtimes

| Runtime | Requirements                 | Internal Port |
| ------- | ---------------------------- | ------------- |
| Python  | `app.py`, `requirements.txt` | 8000          |
| Node.js | `package.json` with `start`  | 3000          |

If the contract is violated, the build fails — intentionally.

---

## CLI Usage (Primary Interface)

MinPaas is designed to be used via CLI.

### Install (local dev)

```bash
pip install -e .
```

### Start control plane

```bash
uvicorn minpaas.server.main:app --port 4000
```

### Deploy an app

```bash
minpaas deploy \
  --app my-app \
  --runtime node \
  --repo https://github.com/username/repo \
  --env DEBUG=false
```

### List apps

```bash
minpaas apps
```

### View logs

```bash
minpaas logs my-app
```

### Delete app

```bash
minpaas delete my-app
```

The CLI is a **thin HTTP client** — all logic lives in the backend.

---

## Control-Plane API (Excerpt)

* `POST /deploy` — deploy or redeploy an app
* `GET /apps` — list deployed apps
* `GET /apps/{name}/logs` — fetch container logs
* `DELETE /apps/{name}` — stop and remove app

Both CLI and future web UI use the same API.

---

## State & Configuration

* Control-plane state is stored in `state/apps.json`
* Environment variables are:

  * provided at deploy time
  * persisted in state
  * injected at container runtime
* Images are built once; config changes don’t require rebuilds

This follows the **build vs config separation** used by real PaaS systems.

---

## Logging Strategy

MinPaas does not manage logs itself.

* Docker is the source of truth
* Logs are fetched via `docker logs`
* No buffering, parsing, or storage duplication

Simple, correct, and debuggable.

---

## What MinPaas Intentionally Does NOT Do

These are out of scope for the core:

* Kubernetes orchestration
* Autoscaling
* Multi-user auth
* Reverse proxy / shared domain
* Metrics & tracing
* Encrypted secrets
* CI pipelines or webhooks

The goal is **clarity**, not feature bloat.

---

## Roadmap (Optional Enhancements)

* Web dashboard (read-only + deploy form)
* Reverse proxy (single domain routing)
* Health checks & restart policies
* Secrets encryption
* Multi-tenant auth
* Metrics & monitoring

None of these are required for MinPaas to be valid.

---

## Why This Project Matters

MinPaas demonstrates:

* real container lifecycle management
* control-plane thinking
* platform-level abstractions
* production-grade constraints
* senior-level design discipline

This is **not** a tutorial project.
It is a **minimal but real PaaS**.

---

## Author

Built by **Vaibhav Shukla**
as a serious platform engineering & DevOps project.