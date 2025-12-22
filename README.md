Below is a **complete, production-grade `README.md`** for **MinPaas** in its **final core state (Step 6)**.

This is written so that:

* an interviewer can understand it in 3–5 minutes
* a senior engineer respects the design
* future contributors know exactly what exists and what doesn’t

You can paste this **as-is** into `README.md`.

---

# MinPaas 🚀

**A Docker-First Mini Platform as a Service**

MinPaas is a **minimal, opinionated Platform as a Service (PaaS)** built from scratch to demonstrate how real PaaS systems work internally.

It is **not** a Kubernetes wrapper, not a framework demo, and not a toy Heroku clone.

MinPaas focuses on:

* container lifecycle management
* control-plane design
* runtime abstraction
* Git-based deployments
* production-grade constraints

> Think: *Heroku’s core loop, built transparently, on a single machine.*

---

## Why MinPaas Exists

Most “PaaS clone” projects:

* jump straight to Kubernetes
* hide behavior behind frameworks
* lack explainable system design
* over-engineer too early

MinPaas takes the opposite approach:

* Docker is the **only** execution boundary
* Every feature is added **incrementally**
* Every design decision is **interview-explainable**
* Constraints come **before** flexibility

---

## Core Principles

* **Docker-first**: Docker is the runtime abstraction
* **Single-machine**: No Kubernetes, no cloud dependency
* **Opinionated by design**: Platform controls builds
* **Control-plane driven**: MinPaas manages lifecycle
* **Incremental evolution**: Features are earned, not assumed

---

## Current Feature Set (Final Core)

MinPaas currently supports:

* ✅ Python & Node.js runtimes
* ✅ Platform-owned Docker build templates
* ✅ GitHub-based deployments
* ✅ Persistent control-plane state
* ✅ Deterministic port allocation
* ✅ Environment variable injection
* ✅ Safe redeploys
* ✅ Container lifecycle management
* ✅ Application logs via API

This is the **minimum complete PaaS core**.

---

## High-Level Architecture

```
Client (curl / API)
        ↓
MinPaas Control Plane (FastAPI)
        ↓
Docker CLI (subprocess)
        ↓
Docker Engine
        ↓
Application Containers
```

MinPaas is a **control plane**, not an app runner.

---

## Project Structure

```
minpaas/
├── server/
│   ├── main.py        # API entrypoint
│   ├── deploy.py      # Build & run lifecycle
│   ├── registry.py    # Persistent state
│   ├── runtimes.py    # Runtime definitions
│   └── git.py         # Git utilities
├── runtimes/
│   ├── python/Dockerfile
│   └── node/Dockerfile
├── workspace/
│   └── <app_name>/    # Cloned repositories
├── state/
│   └── apps.json      # Control-plane registry
└── README.md
```

---

## Runtime Contract (Critical)

All applications deployed on MinPaas must:

1. Run as an HTTP server
2. Listen on the port provided via:

   ```
   PORT=<number>
   ```
3. Conform to the selected runtime’s expectations

This mirrors real PaaS platforms (Heroku, Fly.io, Railway).

---

## Supported Runtimes

### Python Runtime

**Requirements:**

* `app.py`
* `requirements.txt`
* App listens on `PORT`

**Internal container port:** `8000`

---

### Node.js Runtime

**Requirements:**

* `package.json` with a `start` script
* Entry file (e.g. `index.js`)
* App listens on `PORT`

**Internal container port:** `3000`

If these contracts are violated, the build fails — intentionally.

---

## Why Dockerfiles Are Platform-Owned

Users **do not** supply Dockerfiles.

Reasons:

* deterministic builds
* predictable behavior
* simpler security model
* easier debugging
* realistic PaaS behavior

This is a deliberate and defensible design choice.

---

## Control Plane API

### Deploy an Application

```http
POST /deploy
Content-Type: application/json
```

```json
{
  "app": "my-app",
  "runtime": "node",
  "repo": "https://github.com/username/repo.git",
  "env": {
    "GREETING": "Hello from MinPaas"
  }
}
```

**What happens:**

1. Repo is cloned into managed workspace
2. Runtime Dockerfile is applied
3. Image is built
4. Container is replaced safely
5. State is persisted

---

### List Applications

```http
GET /apps
```

Returns the full registry of deployed apps.

---

### Fetch Application Logs

```http
GET /apps/{app_name}/logs
```

Returns recent container logs via Docker.

MinPaas does **not** store logs — Docker is the source of truth.

---

### Delete an Application

```http
DELETE /apps/{app_name}
```

This:

* stops the container
* removes it from Docker
* deletes the registry entry

---

## Persistent State

MinPaas stores control-plane state in:

```
state/apps.json
```

Each app record includes:

* app name
* runtime
* repo URL
* container name
* image name
* allocated port
* public URL
* environment variables

### Why JSON (for now)

* single-machine deployment
* human-readable
* zero operational overhead
* trivial migration to a database later

---

## Deterministic Port Allocation

Ports are assigned deterministically:

```
port = 10000 + hash(app_name) % 50000
```

This guarantees:

* stable URLs
* predictable redeploys
* no random port churn

---

## Environment Variables

* Env vars are provided at deploy time
* Stored in control-plane state
* Injected via `docker run -e`
* No rebuild required for config changes

This follows the **build vs config separation** used by real PaaS systems.

---

## Logging Strategy

MinPaas does **not** manage logs itself.

* Logs are stored by Docker
* MinPaas exposes them via API
* No buffering, parsing, or persistence

This keeps the platform:

* thin
* correct
* easy to reason about

---

## What MinPaas Intentionally Does NOT Do

These are **out of scope for the core**:

* Kubernetes orchestration
* Reverse proxy / shared domain
* Authentication / multi-user support
* CI pipelines or webhooks
* Metrics & tracing
* Secrets encryption
* Auto-scaling

All of these can be added **after** the foundation.

---

## Design Philosophy

> **Constraints first. Flexibility later.**

MinPaas evolves the same way real platforms do:

1. control the environment
2. enforce contracts
3. add configurability safely

---

## Roadmap (Post-Core Enhancements)

Optional next steps:

* Reverse proxy (single domain routing)
* Health checks & restart policies
* Auth & multi-tenant isolation
* Encrypted secrets
* Metrics & monitoring
* Web UI

None of these are required for MinPaas to be valid.

---

## Why This Project Matters

MinPaas demonstrates:

* real container lifecycle management
* control-plane thinking
* production-grade constraints
* senior-level system design discipline

This is **not a demo**.
It is a **minimal but real PaaS**.

---

## Author

Built by **Vaibhav Shukla**
as a serious infrastructure & platform engineering project.

---

When you’re ready, instruct me on:

* refinements
* architecture diagrams
* interview Q&A
* security hardening
* reverse proxy
* or turning this into a public GitHub release
