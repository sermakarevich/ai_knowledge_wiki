# Technical Analysis: Brohammad/VoxForge

**Repository:** https://github.com/Brohammad/VoxForge
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Enterprise voice agents require more than an LLM wrapper: streaming transport, orchestration with safety, retrieval-grounded answers, tool execution, quality measurement, escalation, and operable deployment. Typical chatbot demos leave transport, replay, handoff, and metrics as an exercise, and managed voice platforms impose vendor lock-in and per-minute platform tax (README.md:50-58).

VoxForge addresses this with a complete self-hostable voice stack covering transport, orchestration, knowledge retrieval, tool execution, per-turn evaluation, session replay, human handoff, and operator dashboard, deployable to own infrastructure (README.md:26). One `VoicePipelineService` powers every transport with no duplicated business logic across WebSocket, REST onboarding, or WebRTC (README.md:44). It is structured as a modular monolith with Clean Architecture: clear module boundaries without microservice operational overhead (README.md:171). Release status cited is `v1.0.0-rc.1` live in production with HTTPS, automated tests, and public demo (README.md:28).

Primary user: engineers building self-hosted voice agents, and operators needing replay, metrics, and escalation workflows; secondary audience is teams evaluating self-hosted voice AI before committing to a SaaS vendor (README.md:68-71).

## 2. High-Level Architecture

```text
Client
  │ WebSocket / WebRTC / REST onboarding
  ▼
Transport ──────────────────────────────────► Voice Gateway (session lifecycle)
  │                                             │ VoicePipelineService (single shared path, no duplicated logic)
  ▼                                             ▼
Agent Orchestrator (LangGraph) ──────────────► MCP Tool Router + Knowledge RAG + Memory (pgvector)
  │
  ▼
Evaluation Engine (per-turn latency / quality / tool / cost)
  │
  ▼
Replay / Handoff queue / Dashboard + analytics API
```

Data-flow narrative:

1. Client connects over WebSocket streaming, LiveKit WebRTC, or REST onboarding; the Voice Gateway owns session lifecycle (README.md:149-157, README.md:159-169).
2. All transports delegate to a single `VoicePipelineService`, so STT → agent → TTS behavior is identical regardless of ingress (README.md:44, README.md:50-56).
3. The LangGraph orchestrator runs planner, safety, executor with conditional tools, critic, and coordinator stages, calling the MCP Tool Router, Knowledge RAG (document upload, chunking, pgvector search, citation grounding), and Memory (semantic retrieval, summarization) (README.md:159-169, README.md:34-42).
4. Every turn passes through the Evaluation Engine for latency, quality, tool, and cost scoring (README.md:159-169).
5. Turns feed Replay (signed links), Handoff (human escalation queue), and the Dashboard analytics API; LiveKit Gateway handles WebRTC token generation and worker dispatch (README.md:159-169, README.md:34-42).
6. In production the stack runs as Compose services behind NGINX with TLS; Postgres and Redis back state and queues, with optional knowledge, LiveKit, and monitoring workers (docker-compose.prod.yml:1-6, docker-compose.prod.yml:589-613, deploy.sh:448-469).

Persistent state lives in PostgreSQL 16 + pgvector (relational records, auth, knowledge embeddings, memory vectors) and Redis (cache/queues, session/TTL state such as handoff), plus filesystem/blob knowledge storage (`KNOWLEDGE_BLOB_PATH=/tmp/voxforge-knowledge` locally, `/data/knowledge` in production) (README.md:179-188, .env.example:66-79, .env.production.example:36-50). Deploy artifacts (Postgres backups, generated NGINX conf, generated Prometheus config) are git-ignored outputs (`.gitignore:25-29`, `.gitignore:49-57`).

## 3. VoicePipelineService — The Core Abstraction

Representation: a single shared service object that binds transport ingress to the agent graph and operations sinks. The wiki states it directly: "One `VoicePipelineService` powers every transport — no duplicated business logic across WebSocket, REST onboarding, or WebRTC." (README.md:44). Transports are variants of ingress, not separate pipelines: WebSocket gateway, programmatic onboarding API, LiveKit WebRTC (README.md:34-42).

Named kinds/types cited in the wiki:

- Transport kinds: `WebSocket / LiveKit WebRTC / REST onboarding` (README.md:149-157).
- Orchestrator stages: `planner, safety, executor + conditional tools, critic, coordinator` (README.md:34-42).
- Knowledge operations: `document upload, chunking, pgvector search, citation grounding` (README.md:34-42).
- Tool plane: `builtin tools + MCP server discovery at runtime` (README.md:34-42).
- Trust/operations: `per-turn evaluation, signed replay links, human handoff queue` and `dashboard, latency analytics, alerts, policy presets, SAML SSO` (README.md:34-42).
- Module set: `Auth, Voice Gateway, Agent Orchestrator, Knowledge, Memory, Handoff, Evaluation, Dashboard, LiveKit Gateway` with responsibilities in (README.md:159-169).

Key query (canonical pipeline form), verbatim from the wiki (README.md:149-157):

```text
Client
  → Transport (WebSocket / LiveKit WebRTC / REST onboarding)
  → VoicePipelineService
  → Agent Orchestrator (LangGraph)
  → MCP Tool Router + Knowledge RAG + Memory
  → Evaluation Engine
  → Replay / Handoff / Dashboard
```

## 4. LLM / External Service Integration

The repo calls LLM and voice APIs through swappable providers selected by environment variables with no code changes (README.md:194). Defaults are `mock` locally so no API keys are needed; production validation enforces real providers when `DEMO_ENABLED=false` (README.md:194, README.md:212, SECURITY.md:39-52).

| Role | Options | Local default | Required env when non-mock |
|------|---------|---------------|----------------------------|
| STT | `mock`, `deepgram` | `mock` | `STT_PROVIDER=deepgram`, `DEEPGRAM_API_KEY=...` (README.md:162-176) |
| LLM | `mock`, `openai` | `mock` | `LLM_PROVIDER=openai`, `OPENAI_API_KEY=sk-...` (README.md:162-176) |
| TTS | `mock`, `cartesia` | `mock` | `TTS_PROVIDER=cartesia`, `CARTESIA_API_KEY=...` (README.md:162-176) |
| Embeddings | `mock`, `openai` | `mock` | `EMBEDDING_PROVIDER` / `KNOWLEDGE_BASE_PROVIDER` (`.env.example:66-79`) |
| Ticketing/support | `mock` (+ Zendesk implemented, Freshdesk not implemented) | `mock` | `TICKETING_PROVIDER`, `SUPPORT_TOOLS_ENABLED=true` (`.env.example:66-79`, README.md:282-292) |
| WebRTC media | LiveKit optional | absent | `LIVEKIT_URL` set triggers `livekit-worker`; WebSocket voice works without it (README.md:282-292, deploy.sh:448-469) |

Required vs optional: mock STT/LLM/TTS/embeddings calls are local stubs requiring no keys and used by `/demo` flows (README.md:97). Non-mock STT/LLM/TTS/embedding calls are required in production unless the demo remains enabled; the security checklist requires real `STT_PROVIDER`/`LLM_PROVIDER`/`TTS_PROVIDER` unless `DEMO_ENABLED=true` (SECURITY.md:39-52). LiveKit, Prometheus/Grafana, Certbot/Cloudflare DNS, and knowledge-worker dispatch are optional and gated by `LIVEKIT_URL`, `METRICS_BEARER_TOKEN`, `KNOWLEDGE_ENABLED`, and cert presence (deploy.sh:448-469, .env.deploy.example:1-5). Exact parameter names include `STT_PROVIDER`, `LLM_PROVIDER`, `TTS_PROVIDER`, `OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `CARTESIA_API_KEY`, plus `DEMO_ENABLED` (README.md:203-212).

## 5. Voice-to-Evaluation Runtime and Production Deploy — The Main Pipeline

Runtime path (each step grounded in the pipeline and module tables):

1. Ingress via transport — WebSocket streaming, LiveKit WebRTC, or REST onboarding (`README.md:149-157`).
2. `VoicePipelineService` central dispatch — single shared business-logic path for all transports (`README.md:44`).
3. Agent Orchestrator (LangGraph) — planner → safety → executor with conditional tools → critic → coordinator (`README.md:34-42`, `README.md:159-169`).
4. Context and action fan-out — MCP Tool Router with runtime MCP server discovery, Knowledge RAG ingestion/search/citations, Memory semantic retrieval and summarization via pgvector (`README.md:34-42`, `README.md:159-169`).
5. Evaluation Engine — per-turn latency, quality, tool, and cost scoring (`README.md:159-169`).
6. Operations sinks — signed Replay links, Handoff escalation queue, Dashboard operator UI and analytics API; LiveKit Gateway token generation/worker dispatch for WebRTC (`README.md:159-169`, `README.md:34-42`).

Production deploy path (`deploy.sh` functions, each with location):

1. `require_env_file` — generates env from `scripts/setup-production-env.sh` when `$ENV_FILE` (default `$ROOT/.env.production`) is missing (`.env.production.example:1`, `deploy.sh:385-391`).
2. `load_env` — sources `$ENV_FILE` with `set -a`, derives `DOMAIN` from `PUBLIC_BASE_URL`, rejects placeholder `your-domain.example` (`.env.production.example:6`, `deploy.sh:393-404`).
3. `validate_env` — builds `app` and runs `python /app/scripts/validate_production_env.py` with `APP_ENV=production` in-container (`.env.production.example:3`, `deploy.sh:406-414`).
4. `render_nginx_config` — renders `voxforge-http.conf.template` / `voxforge-https.conf.template` with `sed s/${DOMAIN}/$DOMAIN/g` into `staged/`; bootstrap conf until `deploy/nginx/certs-ready` exists (`.gitignore:52-55`, `deploy.sh:416-436`).
5. `bootstrap_tls` — starts `postgres redis app nginx`, polls `http://127.0.0.1:8000/api/v1/health` 30x2s, runs `certbot certonly --webroot -w /var/www/certbot`, touches `certs-ready`, re-renders NGINX (`.gitignore:52`, `deploy.sh:471-501`).
6. `start_optional_workers` — starts `livekit-worker` with `--profile livekit` when `LIVEKIT_URL` is set, `knowledge-worker` unless `KNOWLEDGE_ENABLED=false`, `prometheus`+`grafana` with `--profile monitoring` when `METRICS_BEARER_TOKEN` is set (`.env.production.example:12`, `.env.production.example:64-73`, `deploy.sh:448-469`).
7. `cmd_status` — prints `compose ps`, probes `/api/v1/health` and `/api/v1/ready`, prints Landing/Demo/API-docs URLs (`deploy.sh:551-564`).

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| README.md | cited 26–304 | Platform overview, layers, pipeline, stack, quick start, deploy, providers, testing, layout |
| src/voxforge/ (core/, modules/, infrastructure/) | layout ref README.md:244-255 | Application code in Clean Architecture split |
| deploy.sh | cited 1-579 | Single production entrypoint: validate env, render NGINX, bootstrap TLS, start stack/workers |
| docker-compose.prod.yml | cited 1-834 | Production stack `voxforge-prod`: postgres, redis, app, workers, nginx, certbot, monitoring |
| docker-compose.smoke.yml | 1-6 | Smoke overlay publishing app port for local prod validation without TLS |
| Dockerfile.prod | 891-936 | Two-stage builder/runtime image, non-root `appuser`, single uvicorn worker |
| Dockerfile.dev | 857-885 | Single-stage hot-reload dev image with dev dependencies |
| .env.example | 1-119 | Full local-dev defaults: mock providers, demo IDs, auth, memory/tools, knowledge, handoff |
| .env.production.example | 1-89 | Production template: prod hosts, empty secrets, invite-only signup, worker flags |
| .env.deploy.example | 1-5 | Deployment-token template plus optional Cloudflare DNS keys |
| alembic.ini | 11-44 | Single-database migration config and logging levels |
| scripts/setup-production-env.sh | ref deploy.sh:385-391 | Generates `.env.production` on first `deploy.sh init` |
| scripts/validate_production_env.py | ref deploy.sh:406-414 | In-container production env validation (`APP_ENV=production`) |
| scripts/docker-entrypoint.sh | ref docker-compose.prod.yml:641-691 | Container entrypoint for `app` service |
| SECURITY.md | 1-86 | Supported versions, private reporting SLA, hardening checklist |
| docs/ONBOARDING.md | ref README.md:99 | Detailed local walkthrough beyond quick start |
| docs/deployment/guide.md | ref README.md:136-141 | Full VPS setup guide |
| docs/operations/runbook.md | ref README.md:136-141 | Day-2 operations |
| docs/project-metrics.md | ref README.md:50-56 | Verified test snapshot (426 collected) |
| dashboard/ + public/ | ref README.md:244-255 | Static operator UI/landing/demo with no Node build step |

## 7. Dependencies

Required runtime (exact constraint strings as cited in the wiki):

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| python | `3.12+` (images use `FROM python:3.12-slim`) (README.md:77, Dockerfile.dev:857-885) | Runtime for FastAPI/Uvicorn/LangGraph app |
| FastAPI | as pinned in `pyproject.toml` (component `API: FastAPI, Uvicorn, Python 3.12`) (README.md:179-188) | HTTP API |
| Uvicorn | as pinned in `pyproject.toml` (entrypoint `uvicorn voxforge.main:app --app-dir /app/src`) (README.md:79-87, docker-compose.prod.yml:641-691) | ASGI server |
| LangGraph | as pinned in `pyproject.toml` (component `Agents: LangGraph, LangChain`) (README.md:179-188) | Agent orchestration graph |
| LangChain | as pinned in `pyproject.toml` (component `Agents: LangGraph, LangChain`) (README.md:179-188) | Agent/tool primitives |
| PostgreSQL + pgvector | `pgvector/pgvector:pg16` (docker-compose.prod.yml:589-613) | Relational state, embeddings, memory vectors |
| Redis | `redis:7-alpine` (docker-compose.prod.yml:615-639) | Cache and queues |
| asyncpg driver | via `DATABASE_URL=postgresql+asyncpg://...` (.env.example:1) | Async Postgres access |
| Alembic | `script_location = alembic` (alembic.ini:13-18) | Schema migrations (`alembic upgrade head`) |
| uv | required tool (README.md:77) | Local dependency install/sync (`uv sync`) |
| Docker + Docker Compose | required tool (README.md:77, README.md:120-128) | Local postgres/redis and production stack |

Deployment/observability (required in prod stack, optional profiles otherwise):

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| NGINX | `nginx:1.27-alpine` (docker-compose.prod.yml:800-823) | Reverse proxy and TLS termination |
| Certbot | `certbot/certbot:v2.11.0` (docker-compose.prod.yml:825-834) | Let's Encrypt issuance/renewal loop every `12h` |
| Prometheus | `prom/prometheus:v2.54.1` `profiles: ["monitoring"]` (docker-compose.prod.yml:753-771) | Metrics collection |
| Grafana | `grafana/grafana:11.2.0` `profiles: ["monitoring"]` (docker-compose.prod.yml:773-798) | Metrics dashboards |
| OpenTelemetry | as pinned (component `Observability: OpenTelemetry, Prometheus, structured logging`) (README.md:179-188) | Tracing and structured logging |

Dev/test tooling:

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| pytest (+ coverage 70% gate) | via `make test*` targets (README.md:218-227) | Unit/integration/feature/failure suites |
| Playwright | via `make test-browser` (README.md:218-227) | Browser UI journeys (landing, demo, dashboard, KB) |
| ruff | via `ruff check src tests` (README.md:218-227) | Lint |
| pip-audit, gitleaks | CI refs (README.md:179-188) | Supply-chain and secret scanning |

## 8. CLI / Usage Surface

Entry points:

| Entrypoint | Command |
|------------|---------|
| App server (local) | `uvicorn voxforge.main:app --reload --app-dir src` (README.md:79-87) |
| App server (prod container) | `uvicorn voxforge.main:app --host 0.0.0.0 --port 8000 --app-dir /app/src --workers 1` (docker-compose.prod.yml:641-691, Dockerfile.prod:936) |
| LiveKit worker | `python -m voxforge.infrastructure.livekit.worker` (docker-compose.prod.yml:693-718) |
| Knowledge worker | `python -m voxforge.infrastructure.knowledge.worker` (docker-compose.prod.yml:720-751) |
| Migrations | `alembic upgrade head` (README.md:79-87) |
| Prod deploy | `./deploy.sh init\|up\|down\|logs\|backup\|renew-cert\|smoke\|status` (deploy.sh:3-12, README.md:130-134) |
| Prod bootstrap | `./scripts/setup-production-env.sh your-domain.example` then `./deploy.sh init` (README.md:120-126) |

Commands (selection):

```bash
uv sync                    # or: pip install -e ".[dev,livekit]"
docker compose up -d postgres redis
alembic upgrade head
uvicorn voxforge.main:app --reload --app-dir src
make test | make test-browser | make test-unit | make test-integration | make test-feature | make test-failure | make test-cov
ruff check src tests
./deploy.sh status | ./deploy.sh backup | ./deploy.sh smoke
curl http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/auth/register -H 'Content-Type: application/json' -d '{"email":"you@example.com","password":"your-secure-password","full_name":"You"}'
curl -X POST http://localhost:8000/api/v1/demo/quickstart
```
(README.md:79-114, README.md:218-227, README.md:130-134)

Local surfaces: `/` landing, `/demo`, `/status`, `/dashboard`, `/api/v1/docs` on `http://localhost:8000` (README.md:89-95). Health/readiness: `/api/v1/health`, `/api/v1/ready` (deploy.sh:471-501, deploy.sh:551-564).

Env-var and config tables:

| Variable | Default / example | Effect |
|----------|-------------------|--------|
| `STT_PROVIDER` / `LLM_PROVIDER` / `TTS_PROVIDER` | `mock` locally (`.env.example:99-101`) | Select `mock` vs `deepgram` / `openai` / `cartesia` (README.md:162-176) |
| `OPENAI_API_KEY` / `DEEPGRAM_API_KEY` / `CARTESIA_API_KEY` | empty locally | Required for non-mock providers (README.md:203-210) |
| `DEMO_ENABLED` | `true` locally | `true` allows no-auth `/api/v1/demo/quickstart`; `false` enforces real providers and auth (README.md:103-114, README.md:212) |
| `APP_ENV` | `development` locally / `production` in prod (`.env.example:8`, `.env.production.example:4`) | Gates secure-deployment checks |
| `DATABASE_URL` / `REDIS_URL` | localhost locally; `postgres`/`redis` hostnames + `REDIS_PASSWORD` in prod (`.env.example:1-2`, `.env.production.example:36-50`) | Data-plane wiring |
| `JWT_SECRET_KEY` / `API_KEY_HASH_PEPPER` / `HANDOFF_REPLAY_SIGNING_SECRET` / `METRICS_BEARER_TOKEN` | `change-me-in-production` locally; empty-must-fill in prod (`.env.example:30-37`, `.env.production.example:9-12`) | Auth, signing, metrics gating |
| `REGISTRATION_ENABLED` | `true` locally / `false` in prod (`.env.example:30-37`, `.env.production.example:29-34`) | Invite-only signup in production |
| `KNOWLEDGE_ENABLED` / `KNOWLEDGE_WORKER_ENABLED` / `KNOWLEDGE_BLOB_PATH` | `true` / `false` / `/tmp/voxforge-knowledge` locally; worker `true`, path `/data/knowledge` in prod (`.env.example:66-79`, `.env.production.example:36-50`) | Knowledge plane and worker dispatch |
| `MEMORY_*` (`MEMORY_ENABLED`, `MEMORY_EMBEDDING_MODEL=text-embedding-3-small`, `MEMORY_EMBEDDING_DIMENSIONS=1536`, `MEMORY_MAX_RECENT_MESSAGES=10`, `MEMORY_SUMMARIZE_AFTER_MESSAGES=20`, `MEMORY_RETRIEVAL_TOP_K=5`, `MEMORY_SIMILARITY_THRESHOLD=0.65`) | as listed (`.env.example:53-63`) | Memory retrieval/summarization tuning |
| `HANDOFF_*` (`HANDOFF_ENABLED=true`, `HANDOFF_AUTO_POLICY=true`, `HANDOFF_MIN_CONFIDENCE=0.55`, `HANDOFF_MAX_TOOL_FAILURES=2`, `HANDOFF_ESCALATE_ON_TOOL_FAILURE=true`, `HANDOFF_SESSION_TTL_SECONDS=14400`) | as listed (`.env.example:103-114`) | Escalation policy and signed-link TTL |
| `RATE_LIMIT_*` | `RATE_LIMIT_ENABLED=true`, `RATE_LIMIT_MULTIPLIER=1.0`, fail-closed categories list; deprecated `RATE_LIMIT_PER_MINUTE` (`.env.example:20-25`) | Throttle auth/voice/knowledge/replay categories |

## 9. Extensibility Points

- New voice provider (STT/LLM/TTS/embeddings): add provider implementation under the infrastructure providers layer and select via `STT_PROVIDER` / `LLM_PROVIDER` / `TTS_PROVIDER` / `EMBEDDING_PROVIDER` with keys `OPENAI_API_KEY` / `DEEPGRAM_API_KEY` / `CARTESIA_API_KEY`; no transport changes needed because all transports share `VoicePipelineService` (README.md:194, README.md:44, .env.example:99-101).
- New tool / integration: register builtin tool or expose an MCP server for runtime discovery by the MCP Tool Router; tune `TOOLS_ENABLED`, `TOOL_TIMEOUT_SECONDS=30`, `MAX_TOOL_ITERATIONS=5` (README.md:34-42, .env.example:53-63).
- New knowledge source or chunking/retrieval policy: extend the Knowledge module (ingestion, embedding, pgvector search, citations) and `KNOWLEDGE_*` settings including `KNOWLEDGE_BLOB_STORE` / `KNOWLEDGE_BLOB_PATH` and `knowledge-worker` dispatch (README.md:159-169, .env.example:66-79, docker-compose.prod.yml:720-751).
- Orchestrator behavior (planning, safety, critic): extend the Agent Orchestrator LangGraph stages (planner, safety, executor + conditional tools, critic, coordinator) without touching transports (README.md:34-42, README.md:159-169).
- Escalation and trust policy: extend the Handoff module and `HANDOFF_*` policy variables plus `HANDOFF_REPLAY_SIGNING_SECRET` TTL handling (README.md:159-169, .env.example:103-114).
- Auth and multitenancy: extend the Auth module (JWT, RBAC, organizations, API keys with `API_KEY_PREFIX=vxf_`, SAML SSO) (README.md:159-169, .env.example:30-37).
- Operator surface and alerts: extend the static `dashboard/` UI and analytics API, and monitoring profile (`prometheus`/`grafana` services) (README.md:244-255, docker-compose.prod.yml:753-798).
- Deploy and TLS: extend `deploy.sh` functions (`render_nginx_config`, `bootstrap_tls`, `start_optional_workers`) and `deploy/` NGINX templates (deploy.sh:416-501, .gitignore:52-55).

## 10. Limitations and Gotchas

- **Single uvicorn worker in production caps vertical throughput.** The prod container runs `--workers 1` (docker-compose.prod.yml:641-691, Dockerfile.prod:936); scaling beyond one process requires changing the image command or horizontal replicas, not just resources (postgres `0.30` CPU / `512M`, redis `0.10` CPU / `128M` defaults in docker-compose.prod.yml:589-639).
- **Placeholder secrets and hosts fail closed and block deploy.** Local defaults use `change-me-in-production` and `localhost` URLs (`.env.example:1-2`, `.env.example:30-37`); `load_env` rejects placeholder `your-domain.example` and `validate_env` / `validate_production_settings` block weak secrets, open metrics, and mock providers when demo is disabled (deploy.sh:393-414, SECURITY.md:26-52).
- **Mock providers hide real-provider failure modes.** Local voice works without keys or LiveKit (README.md:97, README.md:282-292), but latency, accuracy, cost, ticketing (Zendesk implemented but needing live sandbox verification; Freshdesk not implemented), and WebRTC behavior only appear with real keys and workers (README.md:282-292, SECURITY.md:39-52).
- **Docs exceed the two wiki pages analyzed; coverage here is root-scoped.** The wiki snapshot covers README and top-level env/deploy/Docker files; module internals, `docs/architecture/`, runbooks, and `src/voxforge/modules/` behavior beyond the cited tables are not grounded here (README.md:263-276, 02-top-level-files coverage statement).
- **Rate-limit and registration defaults differ sharply between envs.** Local enables open registration and a broad fail-closed category list with deprecated `RATE_LIMIT_PER_MINUTE=60` / path keys still present (`.env.example:20-25`, `.env.example:30-37`); production switches to invite-only (`REGISTRATION_ENABLED=false`) and `RATE_LIMIT_PER_MINUTE=30` (`.env.production.example:29-34), so copying `.env.example` to production weakens posture.

## 11. How It Compares to Alternatives

- **Vapi:** managed voice-agent SaaS with hosted telephony and per-minute pricing; VoxForge trades hosted convenience for self-hosting, data sovereignty, and no per-minute platform tax (README.md:58).
- **Retell AI:** managed voice API with hosted operations; VoxForge keeps replay, handoff queue, and dashboard inside the deployable stack instead of a vendor console (README.md:34-42, README.md:58).
- **LiveKit Agents:** WebRTC/media framework plus agent primitives; VoxForge uses LiveKit only as an optional WebRTC transport/worker while supplying the onboarding API, knowledge RAG, evaluation, and deploy scripts itself (README.md:34-42, README.md:282-292).
- **Pipecat (Daily):** pipeline framework for STT/LLM/TTS composition; VoxForge is positioned as a batteries-included product (auth, dashboard, replay, `deploy.sh init` on Ubuntu 24.04) rather than a framework to assemble (README.md:58, README.md:120-128). LangGraph alone is likewise a graph primitive, whereas VoxForge ships the surrounding voice, trust, and operations layers (README.md:34-42).

Positioning sentence: VoxForge occupies the self-hosted product slot — fuller than LiveKit Agents, Pipecat, or LangGraph alone, and free of Vapi/Retell platform lock-in — at the cost of operating Postgres/Redis/NGINX/TLS yourself (README.md:58, README.md:120-134).

## Appendix: Selected Code Snippets

1. Local quick start (`README.md:79-87`):

```bash
git clone https://github.com/Brohammad/VoxForge.git
cd VoxForge
cp .env.example .env
uv sync                    # or: pip install -e ".[dev,livekit]"
docker compose up -d postgres redis
alembic upgrade head
uvicorn voxforge.main:app --reload --app-dir src
```

2. Provider selection (`README.md:203-210`, keys in `README.md:203-212`):

```bash
STT_PROVIDER=deepgram
LLM_PROVIDER=openai
TTS_PROVIDER=cartesia
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...
CARTESIA_API_KEY=...
```

3. Deploy entrypoint header (`deploy.sh:3-12`):

```bash
#   ./deploy.sh init          # First-time: validate env, bootstrap TLS, start stack
#   ./deploy.sh up            # Build and start (after init)
#   ./deploy.sh down          # Stop stack
#   ./deploy.sh logs          # Tail logs
#   ./deploy.sh backup        # PostgreSQL backup to deploy/backups/
#   ./deploy.sh renew-cert    # Force certbot renewal
#   ./deploy.sh status        # Service health summary
```

4. Prod app runtime command (`Dockerfile.prod:936`, service context in `docker-compose.prod.yml:641-691`):

```bash
CMD ["uvicorn", "voxforge.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app/src", "--workers", "1"]
```
