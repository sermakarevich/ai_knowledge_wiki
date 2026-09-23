> [[index|Wiki]] | [[summary|Summary]]
# Brohammad/VoxForge — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** VoxForge is an open-source platform for building and operating enterprise voice agents that ships a complete self-hostable voice stack (README.md:26).
## Key points
- VoxForge ships a complete voice stack — transport, orchestration, knowledge retrieval, tool execution, per-turn evaluation, session replay, human handoff, and operator dashboard — deployable to your own infrastructure (README.md:26).
- One `VoicePipelineService` powers every transport with no duplicated business logic across WebSocket, REST onboarding, or WebRTC (README.md:44).
- The runtime pipeline is Client → Transport → `VoicePipelineService` → Agent Orchestrator (LangGraph) → MCP Tool Router + Knowledge RAG + Memory → Evaluation Engine → Replay / Handoff / Dashboard (README.md:149-157).
- It is built as a modular monolith with Clean Architecture — clear module boundaries without microservice operational overhead (README.md:171).
- Providers are swapped via environment variables with no code changes, defaulting to `mock` locally and enforcing real providers when `DEMO_ENABLED=false` (README.md:194, README.md:212).
- Local quick start needs Python 3.12+, Docker, and `uv`, plus `postgres`/`redis` via Docker Compose, `alembic upgrade head`, and `uvicorn voxforge.main:app` (README.md:77-87).
- Production deploys to Ubuntu 24.04 via `./scripts/setup-production-env.sh` plus `./deploy.sh init`, which handles env validation, Docker build, NGINX + Certbot TLS, health-gated startup, and optional workers (README.md:120-128).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repo root defines how VoxForge is configured, built, and deployed via env templates, Docker assets, a production deploy script, and repo/security policy files.
## Key points
- Three env templates separate concerns: `.env.deploy.example` holds only `TOKEN` plus optional Cloudflare DNS keys (`.env.deploy.example:1-5`), `.env.example` holds the full local-dev defaults (`.env.example:1-115`), and `.env.production.example` holds the production template validated by `scripts/validate_production_env.py` (`.env.production.example:1-3`).
- Local development defaults to mock providers (`STT_PROVIDER`/`LLM_PROVIDER`/`TTS_PROVIDER=mock`) with the public demo enabled (`DEMO_ENABLED=true`), while production keeps mocks but switches to invite-only signup and container hostnames (`.env.example:31-36`, `.env.example:117-119`, `.env.production.example:23-30`, `.env.production.example:36-40`).
- `deploy.sh` is the single production entrypoint with subcommands `init|up|down|logs|backup|renew-cert|smoke|status`, enforcing `set -euo pipefail`, env-file loading, NGINX rendering, TLS bootstrap, and optional workers (`deploy.sh:1-12`, `deploy.sh:374`, `deploy.sh:566-579`).
- `docker-compose.prod.yml` defines the production stack (`voxforge-prod`) with `postgres` (pgvector/pg16), `redis`, `app`, `livekit-worker`, `knowledge-worker`, `prometheus`, `grafana`, `nginx`, and `certbot`, with resource limits and healthchecks (`.env.production.example:78-84`, `docker-compose.prod.yml:1-6`, `docker-compose.prod.yml:589-613`, `docker-compose.prod.yml:800-824`).
- `Dockerfile.dev` is a single-stage hot-reload image with dev dependencies while `Dockerfile.prod` is a two-stage builder/runtime image that runs as non-root `appuser` with a single uvicorn worker (`.env.example:1`, `Dockerfile.dev:857-858`, `Dockerfile.dev:878`, `Dockerfile.prod:891-903`, `Dockerfile.prod:913-929`, `Dockerfile.prod:936`).
- `SECURITY.md` declares `1.0.x` supported and `0.1.x` unsupported, requires private vulnerability reporting with 72-hour acknowledgement and 14-day remediation plan, and lists a secure-deployment checklist gated by `APP_ENV=production` (`.env.production.example:4`, `SECURITY.md:1-7`, `SECURITY.md:11-24`, `SECURITY.md:77-86`).
- `alembic.ini` is the generic single-database Alembic config (`script_location = alembic`, placeholder `sqlalchemy.url`), `.gitattributes` forces `text=auto eol=lf` with binary media/font types, and `.gitignore` excludes secrets (`.env`, `.env.production`, `.env.deploy`), venvs, caches, media, and generated deploy/prometheus outputs (`alembic.ini:11-18`, `.gitattributes:1-13`, `.gitignore:25-29`, `.gitignore:49-57`).
## The system in five moves
1. VoxForge is an open-source platform for building and operating enterprise voice agents as a complete self-hostable stack.
2. One `VoicePipelineService` unifies every transport, feeding a LangGraph agent orchestrator with MCP tools, knowledge RAG, and memory, followed by per-turn evaluation into replay, handoff, and dashboard.
3. It is structured as a modular monolith with Clean Architecture, with providers swapped via environment variables defaulting to mock locally.
4. Local setup runs on Python 3.12+, Docker, and `uv` with postgres/redis, migrations, and uvicorn; production targets Ubuntu 24.04 via the setup script plus `deploy.sh init` with TLS and optional workers.
5. The repo root encodes this in layered env templates, a single `deploy.sh` entrypoint, a full `voxforge-prod` compose stack, dev/prod Docker images, and a security policy with private reporting and a production checklist.
