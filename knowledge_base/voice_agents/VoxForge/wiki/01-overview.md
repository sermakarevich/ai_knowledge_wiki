> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** VoxForge is an open-source platform for building and operating enterprise voice agents that ships a complete self-hostable voice stack (README.md:26).
## Key points
- VoxForge ships a complete voice stack — transport, orchestration, knowledge retrieval, tool execution, per-turn evaluation, session replay, human handoff, and operator dashboard — deployable to your own infrastructure (README.md:26).
- One `VoicePipelineService` powers every transport with no duplicated business logic across WebSocket, REST onboarding, or WebRTC (README.md:44).
- The runtime pipeline is Client → Transport → `VoicePipelineService` → Agent Orchestrator (LangGraph) → MCP Tool Router + Knowledge RAG + Memory → Evaluation Engine → Replay / Handoff / Dashboard (README.md:149-157).
- It is built as a modular monolith with Clean Architecture — clear module boundaries without microservice operational overhead (README.md:171).
- Providers are swapped via environment variables with no code changes, defaulting to `mock` locally and enforcing real providers when `DEMO_ENABLED=false` (README.md:194, README.md:212).
- Local quick start needs Python 3.12+, Docker, and `uv`, plus `postgres`/`redis` via Docker Compose, `alembic upgrade head`, and `uvicorn voxforge.main:app` (README.md:77-87).
- Production deploys to Ubuntu 24.04 via `./scripts/setup-production-env.sh` plus `./deploy.sh init`, which handles env validation, Docker build, NGINX + Certbot TLS, health-gated startup, and optional workers (README.md:120-128).
---
## What you get
Layers and capabilities (README.md:34-42):

| Layer | Capabilities |
|-------|----------------|
| **Voice** | WebSocket gateway, programmatic onboarding API, LiveKit WebRTC |
| **Intelligence** | LangGraph orchestrator (planner, safety, executor + conditional tools, critic, coordinator) |
| **Knowledge** | Document upload, chunking, pgvector search, citation grounding |
| **Tools** | Builtin tools + MCP server discovery at runtime |
| **Operations** | Dashboard, latency analytics, alerts, policy presets, SAML SSO |
| **Trust** | Per-turn evaluation, signed replay links, human handoff queue |
| **Deploy** | Docker Compose, NGINX, Let's Encrypt, health/readiness probes |

> "One `VoicePipelineService` powers every transport — no duplicated business logic across WebSocket, REST onboarding, or WebRTC." (README.md:44)

## Why VoxForge
Comparison against chatbot demos (README.md:50-56):

| | VoxForge | Typical chatbot demo |
|---|----------|---------------------|
| **Deploy** | Self-hosted Docker + HTTPS | Vendor lock-in |
| **Pipeline** | STT → agent → TTS + evaluation | LLM wrapper only |
| **Operations** | Dashboard, replay, handoff queue | Logs in a black box |
| **Tests** | 426 collected (verified snapshot) — [project metrics](docs/project-metrics.md) | Unknown |
| **Extensibility** | MCP tools, swappable providers | Hardcoded integrations |

Positioning claim (README.md:58): data sovereignty and no per-minute platform tax versus managed platforms (Vapi, Retell); batteries-included product with auth, dashboard, and deploy scripts versus frameworks (LiveKit Agents, Pipecat, LangGraph alone). Minimal curl walkthrough lives at `examples/hello-voice` (README.md:60).

## Who it's for
Intended audiences (README.md:68-71):
- Engineers building voice agents who want a real architecture, not a prototype
- Operators who need replay, metrics, and escalation workflows
- Teams evaluating self-hosted voice AI before committing to a SaaS vendor
- Contributors looking for a well-tested, documented open-source codebase

## Quick start
Prerequisites (README.md:77): Python 3.12+, Docker, `uv`.

```bash
git clone https://github.com/Brohammad/VoxForge.git
cd VoxForge
cp .env.example .env
uv sync                    # or: pip install -e ".[dev,livekit]"
docker compose up -d postgres redis
alembic upgrade head
uvicorn voxforge.main:app --reload --app-dir src
```
(README.md:79-87)

Local surfaces (README.md:89-95):

| Surface | Local URL |
|---------|-----------|
| Landing | http://localhost:8000/ |
| Demo | http://localhost:8000/demo |
| Status | http://localhost:8000/status |
| Dashboard | http://localhost:8000/dashboard |
| API docs | http://localhost:8000/api/v1/docs |

Mock STT/LLM/TTS providers work without API keys; open `/demo` and click **Start talking**, **Run trust loop**, or **Run one-click sample call** (README.md:97). Detailed walkthrough: `docs/ONBOARDING.md` (README.md:99).

First API calls (README.md:103-114):

```bash
# Health
curl http://localhost:8000/api/v1/health

# Register + login (dashboard uses the same endpoints)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"your-secure-password","full_name":"You"}'

# One-click demo (no auth required when DEMO_ENABLED=true)
curl -X POST http://localhost:8000/api/v1/demo/quickstart
```

## Production deployment
Deploy flow for a fresh Ubuntu 24.04 VPS with HTTPS (README.md:120-126):

```bash
./scripts/setup-production-env.sh your-domain.example
# Edit .env.production if needed (providers, LiveKit)
./deploy.sh init
```

`deploy.sh` handles environment validation, Docker image build, NGINX + Certbot TLS, health-gated startup, and optional workers (knowledge, LiveKit, Prometheus/Grafana) (README.md:128).

```bash
./deploy.sh status    # service health
./deploy.sh backup    # Postgres backup
./deploy.sh smoke     # local prod validation (no TLS)
```
(README.md:130-134)

Guides (README.md:136-141):

| Guide | Description |
|-------|-------------|
| [Deployment guide](docs/deployment/guide.md) | Full VPS setup |
| [Runbook](docs/operations/runbook.md) | Day-2 operations |
| [Public deployment](docs/deployment/public-deployment-record.md) | Live instance reference |
| [Verification checklist](docs/deployment/verification-checklist.md) | Post-deploy QA |

Reference deployment: `https://voxforge.brohammad.tech` with Let's Encrypt and smoke tests (README.md:143). Release status: `v1.0.0-rc.1` live in production with HTTPS, automated tests, and public demo (README.md:28).

## Architecture
Pipeline (README.md:149-157):

```text
Client
  → Transport (WebSocket / LiveKit WebRTC / REST onboarding)
  → VoicePipelineService
  → Agent Orchestrator (LangGraph)
  → MCP Tool Router + Knowledge RAG + Memory
  → Evaluation Engine
  → Replay / Handoff / Dashboard
```

Module responsibilities (README.md:159-169):

| Module | Responsibility |
|--------|----------------|
| **Auth** | JWT, RBAC, organizations, API keys, SAML SSO |
| **Voice Gateway** | WebSocket streaming, session lifecycle |
| **Agent Orchestrator** | Multi-agent pipeline with safety and critic stages |
| **Knowledge** | Ingestion, embedding, semantic search, citations |
| **Memory** | Semantic retrieval, summarization (pgvector) |
| **Handoff** | Human escalation queue, signed replay URLs |
| **Evaluation** | Per-turn latency, quality, tool, and cost scoring |
| **Dashboard** | Operator UI + analytics API |
| **LiveKit Gateway** | WebRTC token generation and worker dispatch |

## Tech stack
Stack table (README.md:179-188):

| Component | Technology |
|-----------|------------|
| API | FastAPI, Uvicorn, Python 3.12 |
| Agents | LangGraph, LangChain |
| Database | PostgreSQL 16 + pgvector |
| Cache / queues | Redis |
| Observability | OpenTelemetry, Prometheus, structured logging |
| Frontend | Static dashboard + landing (no Node build step) |
| Deploy | Docker Compose, NGINX, Certbot |
| CI | pytest, Playwright, ruff, pip-audit, gitleaks |

## Voice providers
Swap providers via environment variables — no code changes (README.md:194):

| Role | Options | Default (local) |
|------|---------|-----------------|
| STT | `mock`, `deepgram` | `mock` |
| LLM | `mock`, `openai` | `mock` |
| TTS | `mock`, `cartesia` | `mock` |
| Embeddings | `mock`, `openai` | `mock` |

```bash
STT_PROVIDER=deepgram
LLM_PROVIDER=openai
TTS_PROVIDER=cartesia
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...
CARTESIA_API_KEY=...
```
(README.md:203-210)

Exact parameter names: `STT_PROVIDER`, `LLM_PROVIDER`, `TTS_PROVIDER`, `OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `CARTESIA_API_KEY`, plus `DEMO_ENABLED` gating production validation (README.md:203-212).

## Testing
Commands (README.md:218-227):

```bash
make test              # non-browser suite (see docs/project-metrics.md)
make test-browser      # Playwright UI journeys
make test-unit         # Unit tests only
make test-integration  # Integration tests
make test-feature      # Feature scenarios
make test-failure      # Failure-mode tests
make test-cov          # Coverage report (70% gate)
ruff check src tests   # Lint
```

Test layers (README.md:229-235):

| Layer | Location | Count |
|-------|----------|-------|
| Unit | `tests/unit/` | Core logic |
| Integration | `tests/integration/` | DB, Redis, providers |
| Feature | `tests/feature/` | End-to-end flows |
| Browser | `tests/browser/` | Landing, demo, dashboard, KB |
| Failure | `tests/failure/` | Provider errors, timeouts |

CI runs the full suite on every push to `main` (README.md:237).

## Project structure
Layout (README.md:244-255):

```text
src/voxforge/          Application code (Clean Architecture)
  core/                Domain interfaces and models
  modules/             Feature modules (auth, voice, knowledge, …)
  infrastructure/      Providers, HTTP, persistence, LiveKit
dashboard/             Operator UI (static HTML/JS)
public/                Landing page, demo, assets
deploy/                NGINX templates, TLS config
docs/                  Architecture, deployment, pilot guides
tests/                 Unit → browser test pyramid
scripts/               Deploy, backup, benchmarks, smoke tests
```

## Documentation, FAQ, contributing
Doc index entry point is `docs/README.md` (README.md:261); topic links include `docs/ONBOARDING.md`, `docs/CONFIGURATION.md`, `docs/deployment/`, `docs/architecture/`, `docs/operations/`, `docs/testing/`, `docs/pilot/`, `docs/demo/`, `docs/FAQ.md`, `docs/ROADMAP.md`, `docs/release/` (README.md:263-276).

FAQ answers (README.md:282-292): no API keys locally (mock providers work); LiveKit not required (WebSocket voice works without it, LiveKit adds browser WebRTC); self-hosting via `./deploy.sh init` on Ubuntu 24.04; Zendesk ticketing implemented but needs live sandbox verification, Freshdesk not implemented, dashboard login uses HttpOnly cookies with JWT paste as Bearer override.

Contributing flow (README.md:300-304): fork, create branch (`git checkout -b fix/issue`), run `make test` and `ruff check src tests`, open a PR using the template.

No truncated files were noted in this chunk; all claims above come from the README excerpt.
**Covers:** README.md (VoxForge platform overview, layers, pipeline, stack, quick start, deploy, providers, testing, layout)
