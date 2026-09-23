> PDF location (no source.pdf bundled): https://github.com/Brohammad/VoxForge
# Brohammad/VoxForge
Source: https://github.com/Brohammad/VoxForge
Kind: repo
Fetched: 2026-09-22T14:53:23.754958+00:00
Tool: git-clone

# Brohammad/VoxForge

Commit: 59843c1db48de12675367602bfaf0b821edbe902

## README

# VoxForge

[![CI](https://github.com/Brohammad/VoxForge/actions/workflows/ci.yml/badge.svg)](https://github.com/Brohammad/VoxForge/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Brohammad/VoxForge?include_prereleases&label=release)](https://github.com/Brohammad/VoxForge/releases/tag/v1.0.0-rc.1)
[![Live Demo](https://img.shields.io/badge/demo-live-38d996)](https://voxforge.brohammad.tech/demo)
[![Status](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fvoxforge.brohammad.tech%2Fapi%2Fv1%2Fhealth&query=%24.status&label=status&color=38d996)](https://voxforge.brohammad.tech/status)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-76.40%25-brightgreen)](docs/project-metrics.md)
[![Discussions](https://img.shields.io/badge/discussions-Q%26A-563d7c)](https://github.com/Brohammad/VoxForge/discussions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Production-grade Voice AI Infrastructure** — deploy, operate, and trust.

🌐 **Live:** [voxforge.brohammad.tech](https://voxforge.brohammad.tech) · [Status](https://voxforge.brohammad.tech/status) · [Demo](https://voxforge.brohammad.tech/demo) · [Dashboard](https://voxforge.brohammad.tech/dashboard) · [API](https://voxforge.brohammad.tech/api/v1/docs) · [Discussions](https://github.com/Brohammad/VoxForge/discussions)

![VoxForge demo — one-click sample call with in-browser TTS](docs/assets/screenshots/demo.gif)

*Refresh this GIF: `./scripts/generate-demo-gif.sh` (automated) or record manually and run `./scripts/capture-demo-gif.sh recording.mp4` — see [recording checklist](docs/demo/recording-checklist.md).*

VoxForge is an open-source platform for building and operating enterprise voice agents. Unlike chatbot wrappers, it ships a **complete voice stack**: transport, orchestration, knowledge retrieval, tool execution, per-turn evaluation, session replay, human handoff, and an operator dashboard — all deployable to your own infrastructure.

> **v1.0.0-rc.1** is live in production with HTTPS, automated tests, and a public demo. [Release notes →](docs/release/v1.0.0-rc.1.md)

---

## What you get

| Layer | Capabilities |
|-------|----------------|
| **Voice** | WebSocket gateway, programmatic onboarding API, LiveKit WebRTC |
| **Intelligence** | LangGraph orchestrator (planner, safety, executor + conditional tools, critic, coordinator) |
| **Knowledge** | Document upload, chunking, pgvector search, citation grounding |
| **Tools** | Builtin tools + MCP server discovery at runtime |
| **Operations** | Dashboard, latency analytics, alerts, policy presets, SAML SSO |
| **Trust** | Per-turn evaluation, signed replay links, human handoff queue |
| **Deploy** | Docker Compose, NGINX, Let's Encrypt, health/readiness probes |

One `VoicePipelineService` powers every transport — no duplicated business logic across WebSocket, REST onboarding, or WebRTC.

---

## Why VoxForge

| | VoxForge | Typical chatbot demo |
|---|----------|---------------------|
| **Deploy** | Self-hosted Docker + HTTPS | Vendor lock-in |
| **Pipeline** | STT → agent → TTS + evaluation | LLM wrapper only |
| **Operations** | Dashboard, replay, handoff queue | Logs in a black box |
| **Tests** | 426 collected (verified snapshot) — [project metrics](docs/project-metrics.md) | Unknown |
| **Extensibility** | MCP tools, swappable providers | Hardcoded integrations |

Compared to managed platforms (Vapi, Retell) you get **data sovereignty and no per-minute platform tax**. Compared to frameworks (LiveKit Agents, Pipecat, LangGraph alone) you get a **batteries-included product** with auth, dashboard, and deploy scripts.

Minimal curl walkthrough (no LiveKit): [examples/hello-voice](examples/hello-voice/README.md)

[Full competitive benchmark →](docs/benchmarks/competitive-analysis.md)

---

## Who it's for

- **Engineers** building voice agents who want a real architecture, not a prototype
- **Operators** who need replay, metrics, and escalation workflows
- **Teams** evaluating self-hosted voice AI before committing to a SaaS vendor
- **Contributors** looking for a well-tested, documented open-source codebase

---

## Quick start (15 minutes)

**Prerequisites:** Python 3.12+, Docker, [uv](https://docs.astral.sh/uv/) (recommended)

```bash
git clone https://github.com/Brohammad/VoxForge.git
cd VoxForge
cp .env.example .env
uv sync                    # or: pip install -e ".[dev,livekit]"
docker compose up -d postgres redis
alembic upgrade head
uvicorn voxforge.main:app --reload --app-dir src
```

| Surface | Local URL |
|---------|-----------|
| Landing | http://localhost:8000/ |
| Demo | http://localhost:8000/demo |
| Status | http://localhost:8000/status |
| Dashboard | http://localhost:8000/dashboard |
| API docs | http://localhost:8000/api/v1/docs |

Mock STT/LLM/TTS providers work **without API keys**. Open `/demo` and click **Start talking**, **Run trust loop**, or **Run one-click sample call**.

Detailed walkthrough: [docs/ONBOARDING.md](docs/ONBOARDING.md)

### First API calls

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

---

## Production deployment

Deploy to a fresh Ubuntu 24.04 VPS with HTTPS in one flow:

```bash
./scripts/setup-production-env.sh your-domain.example
# Edit .env.production if needed (providers, LiveKit)
./deploy.sh init
```

`deploy.sh` handles environment validation, Docker image build, NGINX + Certbot TLS, health-gated startup, and optional workers (knowledge, LiveKit, Prometheus/Grafana).

```bash
./deploy.sh status    # service health
./deploy.sh backup    # Postgres backup
./deploy.sh smoke     # local prod validation (no TLS)
```

| Guide | Description |
|-------|-------------|
| [Deployment guide](docs/deployment/guide.md) | Full VPS setup |
| [Runbook](docs/operations/runbook.md) | Day-2 operations |
| [Public deployment](docs/deployment/public-deployment-record.md) | Live instance reference |
| [Verification checklist](docs/deployment/verification-checklist.md) | Post-deploy QA |

**Reference deployment:** https://voxforge.brohammad.tech (Let's Encrypt, smoke-tested)

---

## Architecture

```text
Client
  → Transport (WebSocket / LiveKit WebRTC / REST onboarding)
  → VoicePipelineService
  → Agent Orchestrator (LangGraph)
  → MCP Tool Router + Knowledge RAG + Memory
  → Evaluation Engine
  → Replay / Handoff / Dashboard
```

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

Built as a **modular monolith** with Clean Architecture — clear module boundaries without microservice operational overhead.

[Architecture diagrams](docs/portfolio/architecture-diagrams.md) · [Voice pipeline](docs/architecture/voice-pipeline.md) · [Architecture index](docs/architecture/README.md) · [ADRs](docs/adr/README.md)

---

## Tech stack

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

---

## Voice providers

Swap providers via environment variables — no code changes:

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

Production validation enforces real providers when `DEMO_ENABLED=false`.

---

## Testing

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

| Layer | Location | Count |
|-------|----------|-------|
| Unit | `tests/unit/` | Core logic |
| Integration | `tests/integration/` | DB, Redis, providers |
| Feature | `tests/feature/` | End-to-end flows |
| Browser | `tests/browser/` | Landing, demo, dashboard, KB |
| Failure | `tests/failure/` | Provider errors, timeouts |

CI runs the full suite on every push to `main`. See the canonical
[project metrics](docs/project-metrics.md) and [testing strategy](docs/testing/testing-strategy.md).

---

## Project structure

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

---

## Documentation

**Full index:** [docs/README.md](docs/README.md)

| Topic | Link |
|-------|------|
| Quick start | [docs/ONBOARDING.md](docs/ONBOARDING.md) |
| Configuration | [docs/CONFIGURATION.md](docs/CONFIGURATION.md) |
| Deployment | [docs/deployment/](docs/deployment/) |
| Architecture | [docs/architecture/](docs/architecture/) |
| Operations | [docs/operations/](docs/operations/) |
| Testing | [docs/testing/](docs/testing/) |
| Pilot program | [docs/pilot/](docs/pilot/) |
| Demo scripts | [docs/demo/](docs/demo/) |
| FAQ | [docs/FAQ.md](docs/FAQ.md) |
| Community Q&A | [GitHub Discussions](https://github.com/Brohammad/VoxForge/discussions) |
| Roadmap | [docs/ROADMAP.md](docs/ROADMAP.md) |
| Releases | [docs/release/](docs/release/) |

---

## FAQ

**Do I need API keys locally?**  
No — mock providers work out of the box.

**Is LiveKit required?**  
No — WebSocket voice works without it. LiveKit adds browser WebRTC.

**Can I self-host in production?**  
Yes — `./deploy.sh init` on Ubuntu 24.04 with automatic HTTPS.

**What's not production-ready yet?**  
Zendesk ticketing is implemented but still needs live sandbox verification; Freshdesk is not implemented. Use `internal`/`mock` knowledge. Dashboard login uses HttpOnly cookies (JWT paste still works as Bearer override). See [known limitations](docs/release/known-limitations.md).

[Full FAQ →](docs/FAQ.md)

---

## Contributing

Contributions welcome — especially docs, tests, and provider adapters.

1. Fork the repo
2. Create a branch (`git checkout -b fix/issue`)
3. Run `make test` and `ruff check src tests`
4. Open a PR using the template

See [CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_COND

... (truncated, 416 more characters)

## pyproject.toml

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "voxforge"
version = "1.0.0rc1"
license = "MIT"
description = "Production-grade Voice AI Infrastructure Platform"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "sqlalchemy[asyncio]>=2.0.36",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "redis>=5.2.0",
    "httpx>=0.28.0",
    "websockets>=14.0",
    "openai>=1.57.0",
    "prometheus-client>=0.21.0",
    "opentelemetry-api>=1.29.0",
    "opentelemetry-sdk>=1.29.0",
    "opentelemetry-instrumentation-fastapi>=0.50b0",
    "opentelemetry-exporter-otlp>=1.29.0",
    "structlog>=24.4.0",
    "python-multipart>=0.0.18",
    "pyjwt>=2.10.0",
    "bcrypt>=4.2.0",
    "email-validator>=2.2.0",
    "langgraph>=0.3.0",
    "langchain-core>=0.3.0",
    "langchain-openai>=0.3.0",
    "signxml>=4.0.0",
    "cryptography>=43.0.0",
    "lxml>=5.0.0",
    "pypdf>=5.0.0",
]

[project.optional-dependencies]
mcp = [
    "mcp>=1.2.0",
]
livekit = [
    "livekit-api>=0.8.0",
    "livekit>=0.18.0",
    "livekit-agents>=1.6.0",
]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "pytest-playwright>=0.6.0",
    "playwright>=1.49.0",
    "ruff>=0.8.0",
    "pyright>=1.1.390",
    "httpx>=0.28.0",
    "fakeredis>=2.26.0",
    "aiosqlite>=0.20.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/voxforge"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
pythonpath = ["."]
markers = [
    "live: tests that require live API keys",
    "postgres: tests requiring PostgreSQL with pgvector",
    "feature: business-flow feature tests",
    "e2e: end-to-end production-like tests",
    "failure: failure-mode and recovery tests",
    "browser: Playwright UI journey tests",
]

[tool.coverage.run]
source = ["src/voxforge"]
branch = true
omit = [
    "*/infrastructure/livekit/worker.py",
    "*/infrastructure/knowledge/worker.py",
]

[tool.coverage.report]
show_missing = true
skip_empty = true
fail_under = 70
precision = 1

[tool.coverage.html]
directory = "htmlcov"

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = ["B008"]

[tool.ruff.lint.per-file-ignores]
"scripts/*.py" = ["E402"]
"src/voxforge/infrastructure/knowledge/worker.py" = ["E402"]
"src/voxforge/infrastructure/security/saml.py" = ["E501"]
"tests/helpers/saml_fixtures.py" = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pyright]
include = ["src/voxforge/api", "src/voxforge/core"]
exclude = ["**/__pycache__"]
pythonVersion = "3.12"
typeCheckingMode = "basic"
reportMissingImports = "warning"
reportMissingTypeStubs = false

```

## Top-level layout

- .env.deploy.example (~5 lines)
- .env.example (~115 lines)
- .env.production.example (~88 lines)
- .gitattributes (~13 lines)
- .github/ (dir, 12 files, ~640 lines)
- .gitignore (~56 lines)
- alembic/ (dir, 14 files, ~1260 lines)
- alembic.ini (~44 lines)
- CHANGELOG.md (~106 lines)
- CODE_OF_CONDUCT.md (~32 lines)
- CONTRIBUTING.md (~95 lines)
- dashboard/ (dir, 3 files, ~3265 lines)
- deploy/ (dir, 5 files, ~145 lines)
- deploy.sh (~220 lines)
- docker-compose.prod.yml (~257 lines)
- docker-compose.smoke.yml (~5 lines)
- docker-compose.yml (~77 lines)
- Dockerfile (~29 lines)
- Dockerfile.dev (~29 lines)
- Dockerfile.prod (~46 lines)
- docs/ (dir, 114 files, ~9665 lines)
- examples/ (dir, 6 files, ~1170 lines)
- infra/ (dir, 5 files, ~168 lines)
- LICENSE (~21 lines)
- Makefile (~82 lines)
- public/ (dir, 12 files, ~1604 lines)
- pyproject.toml (~122 lines)
- README.md (~311 lines)
- scripts/ (dir, 36 files, ~3712 lines)
- SECURITY.md (~51 lines)
- src/ (dir, 207 files, ~21820 lines)
- tests/ (dir, 102 files, ~9944 lines)
- uv.lock (~3792 lines)

