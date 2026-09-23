---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Brohammad/VoxForge
### Q1. What is VoxForge in one sentence, and what layers does its complete voice stack ship?
> [!tip]- Answer
> VoxForge is an open-source platform for building and operating enterprise voice agents as a complete self-hostable voice stack. It ships voice transports (WebSocket gateway, onboarding API, LiveKit WebRTC), a LangGraph orchestrator, knowledge retrieval with pgvector search and citations, builtin plus MCP-discovered tools, and operations/trust layers (dashboard, latency analytics, per-turn evaluation, signed replay links, human handoff queue). See [[wiki/01-overview|Overview]].
### Q2. What is the role of `VoicePipelineService` and what is the full runtime pipeline?
> [!tip]- Answer
> One `VoicePipelineService` powers every transport so WebSocket, REST onboarding, and WebRTC share the same business logic with no duplication. The pipeline runs Client → Transport → `VoicePipelineService` → Agent Orchestrator (LangGraph) → MCP Tool Router + Knowledge RAG + Memory → Evaluation Engine → Replay / Handoff / Dashboard. See [[wiki/01-overview|Overview]].
### Q3. What do you need for a local quick start, and how do providers work without API keys?
> [!tip]- Answer
> Local quick start needs Python 3.12+, Docker, and `uv`, then `docker compose up -d postgres redis`, `alembic upgrade head`, and `uvicorn voxforge.main:app --reload --app-dir src`. STT, LLM, TTS, and embedding providers all default to `mock` locally so `/demo` works with no API keys, and real providers (deepgram, openai, cartesia) are swapped in via environment variables like `STT_PROVIDER` with no code changes. See [[wiki/01-overview|Overview]].
### Q4. How does production deployment work on a fresh Ubuntu 24.04 VPS?
> [!tip]- Answer
> You run `./scripts/setup-production-env.sh your-domain.example`, edit `.env.production` for providers and LiveKit if needed, then `./deploy.sh init`, which validates env, builds the Docker image, sets up NGINX + Certbot TLS, and starts the stack with health-gated startup and optional workers. Day-2 commands include `./deploy.sh status`, `./deploy.sh backup` for Postgres, and `./deploy.sh smoke` for local prod validation without TLS. See [[wiki/01-overview|Overview]].
### Q5. What are the three env templates at the repo root and how do local-dev and production defaults differ?
> [!tip]- Answer
> `.env.deploy.example` holds only `TOKEN` plus optional Cloudflare DNS keys, `.env.example` holds the full local-dev defaults, and `.env.production.example` holds the production template validated by `scripts/validate_production_env.py`. Local dev defaults to mock providers with `DEMO_ENABLED=true` and open registration, while production keeps mocks available but switches to invite-only signup (`REGISTRATION_ENABLED=false`), container hostnames for postgres/redis, and `/data/knowledge` blob storage. See [[wiki/02-top-level-files|Top-level-files]].
### Q6. What do `deploy.sh`, `docker-compose.prod.yml`, and `SECURITY.md` each define?
> [!tip]- Answer
> `deploy.sh` is the single production entrypoint (`init|up|down|logs|backup|renew-cert|smoke|status`) handling env loading, NGINX rendering, TLS bootstrap, and optional workers. `docker-compose.prod.yml` defines the `voxforge-prod` stack — postgres (pgvector/pg16), redis, app (single uvicorn worker as non-root `appuser`), livekit-worker, knowledge-worker, prometheus, grafana, nginx, and certbot — with resource limits and healthchecks. `SECURITY.md` marks `1.0.x` supported and `0.1.x` unsupported, requires private vulnerability reporting with 72-hour acknowledgement and 14-day remediation plan, plus a secure-deployment checklist gated by `APP_ENV=production`. See [[wiki/02-top-level-files|Top-level-files]].
### Q7. Would you recommend VoxForge for a team evaluating self-hosted enterprise voice AI, and why?
> [!tip]- Answer
> Yes, for teams that need data sovereignty with a batteries-included product: it offers a unified voice pipeline across WebSocket and WebRTC, LangGraph orchestration with MCP tools and knowledge grounding, per-turn evaluation with replay and handoff, and a one-command TLS production deploy. The main caveats are confirming the provider matrix (deepgram/openai/cartesia) fits your needs and validating the claimed 426-test suite and `v1.0.0-rc.1` production maturity against your own pilot. See [[wiki/01-overview|Overview]].
