# Technical Analysis: vectorize-io/hindsight

**Repository:** https://github.com/vectorize-io/hindsight
**Version analyzed:** 0.10.1 (from `package-lock.json:17-20`, `package-lock.json:141-154`)
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview

Problem space: long-horizon agent memory. Conversation-history recall, RAG retrieval, and knowledge-graph extraction retain text or triples but do not consolidate what the agent has learned about the world, the user, or its own experience across sessions. The wiki states the positioning directly: "Most agent memory systems focus on recalling conversation history. Hindsight is focused on making agents that learn, not just remember." (README.md:32), and "It eliminates the shortcomings of alternative techniques such as RAG and knowledge graph and delivers state-of-the-art performance on long term memory tasks." (README.md:36).

How the repo addresses it: Hindsight is a client-server memory system. A stateful API server (port 8888) plus UI (port 9999) sits in front of PostgreSQL + pgvector (Oracle 23ai as enterprise alternative), and clients record and query learned state through three operations — `retain` (store), `recall` (search), `reflect` (disposition-aware response) — scoped by `bank_id` (README.md:89, README.md:135, README.md:152). Zero-code-change paths exist via an LLM wrapper (`wrap_openai`, `wrap_anthropic` over LiteLLM, 100+ models) and 60+ framework/coding-agent integrations (README.md:229, README.md:257, README.md:265). Embedded no-server modes (`hindsight-all`, npm equivalent, daemon CLI) cover single-process use (README.md:199, README.md:207, README.md:221).

Primary user: an agent developer who needs persistent, queryable memory (facts, experience, mental models) shared across LLM calls, sessions, and agent frameworks, rather than per-conversation context.

Benchmark claim (as reported in wiki, not independently verified here): state-of-the-art accuracy on LongMemEval as of January 2026 (README.md:54), with live per-model accuracy/latency/cost at `benchmarks.hindsight.vectorize.io` (README.md:58) and reproduction by Virginia Tech's Sanghani Center and The Washington Post; other vendors' scores are described as self-reported (README.md:60). Production use is claimed at Fortune 500 enterprises and AI startups (README.md:62).

## 2. High-Level Architecture

```text
Agent code / LLM call
        │
        ▼
Client SDK (Python / Node / Go / CLI / REST) ──► bank_id-scoped retain / recall / reflect
        │                                         (README.md:135, README.md:152, README.md:182)
        ▼
LLM Wrapper (hindsight-litellm: wrap_openai, wrap_anthropic) ──► auto retain + recall per call
        │                                                          (README.md:229, README.md:235, README.md:257)
        ▼
Hindsight API server :8888 ──► Control-plane UI :9999
        │                       (README.md:89)
        ▼
Core engine (hindsight-api-slim: memory_engine, retain/*, search/*, embeddings,
             cross_encoder, entity_resolver, query_analyzer)
        │                       (CLAUDE.md:125-143)
        ▼
PostgreSQL + pgvector  │  Oracle 23ai (alt)  │  embedded pg0 volume
tables: banks, documents, chunks, entities, memory_units, unit_entities, memory_links
                        (CLAUDE.md:157-159, README.md:80)
```

Data-flow narrative:

1. **Configure LLM backend.** Operator sets `HINDSIGHT_API_LLM_PROVIDER`, `HINDSIGHT_API_LLM_API_KEY`, `HINDSIGHT_API_LLM_MODEL` (defaults `openai` / `gpt-4o-mini`) plus optional VLM slot, temperature, timeout, schema-compat, cache-affinity, and multi-LLM strategy variables (`.env.example:6-8`, `.env.example:11-107`, `.env.example:181-202`). Server is started via Docker, external-Postgres compose, `pip install hindsight-api` + `hindsight-api`, Helm, or hosted Cloud (README.md:80, README.md:96, README.md:105, README.md:114, README.md:125).
2. **Scope state to a bank.** Every operation takes `bank_id` (e.g. `"my-bank"`, `"user-123"`); banks are the tenancy/isolation unit over documents, chunks, entities, memory units, and links (README.md:142, README.md:207, CLAUDE.md:157-159).
3. **Retain.** Client sends content; engine runs fact extraction / linking (`retain/{orchestrator,fact_extraction,link_utils}.py`) with embeddings and the configured retain LLM, persisting to the database (CLAUDE.md:125-143, `.env.example:25-44`).
4. **Recall.** Query fans out to four parallel retrieval strategies — semantic, BM25, graph, temporal — followed by link expansion, fusion, and cross-encoder reranking (`search/{retrieval,graph_retrieval,link_expansion_retrieval,fusion,reranking}.py`, `embeddings.py`, `cross_encoder.py`, `entity_resolver.py`, `query_analyzer.py`) (CLAUDE.md:125-155).
5. **Reflect.** The reflect LLM composes a disposition-aware response grounded in recalled units, governed by `..._REFLECT` temperature/strict-schema settings and `HINDSIGHT_API_REFLECT_MAX_COMPLETION_TOKENS` (README.md:152, `.env.example:25-44`, `.env.example:97-102`).
6. **Serve and observe.** REST routers (`http.py`) and MCP server (`mcp.py`) expose the operations; the Next.js control plane (`hindsight-control-plane`) provides the UI on port 9999 (CLAUDE.md:107-155, README.md:89).

Persistent state lives in the relational database: PostgreSQL with pgvector by default, Oracle 23ai with stated feature parity as the enterprise option; Alembic migrations auto-run on startup (CLAUDE.md:157-159). Docker default persists the embedded database in the `hindsight-data:/home/hindsight/.pg0` volume (README.md:80). No other durable store is documented in the wiki scope.

## 3. Memory Banks, Facts, and Mental Models

Representation: the wiki describes three learned-state kinds — **world facts**, **experience facts**, and **mental models** — plus supporting concepts named in the README contents map: memory types, observations, knowledge pages, directives, and banks (CLAUDE.md:7-9, README.md:40 per 01-overview.md:17). Storage-level representation is relational: `banks, documents, chunks, entities, memory_units, unit_entities, memory_links` in Postgres/pgvector or Oracle 23ai, migrated via Alembic (CLAUDE.md:157-159). Chunk/attachment handling distinguishes text-only chunks (retain LLM) from chunks with inline attachments (vision-slot VLM) (`.env.example:11-17`).

Named kinds/types with file:line (as cited in wiki, not re-verified against source):

- `world facts`, `experience facts`, `mental models` — the memory model (`CLAUDE.md:7-9`).
- `bank_id` — scoping key for all three operations (README.md:142, README.md:207).
- `retain` / `recall` / `reflect` — the operation triple; recall decomposes into semantic, BM25, graph, temporal strategies plus reranking (README.md:152, CLAUDE.md:145-155).
- `observations`, `knowledge pages`, `directives` — further concept names listed in the Core Concepts map (README.md:40 per 01-overview.md:17); detail beyond the names was cut off at README.md:270 and is not covered.
- Database entities `banks, documents, chunks, entities, memory_units, unit_entities, memory_links` (CLAUDE.md:157-159).

Key queries (verbatim client usage, README.md:142):

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")

# Retain: Store information
client.retain(bank_id="my-bank", content="Alice works at Google as a software engineer")

# Recall: Search memories
client.recall(bank_id="my-bank", query="What does Alice do?")

# Reflect: Generate disposition-aware response
client.reflect(bank_id="my-bank", query="Tell me about Alice")
```

The wiki does not provide query-language or SQL-level query definitions; retrieval internals are named only as modules (`search/retrieval`, `graph_retrieval`, `link_expansion_retrieval`, `fusion`, `reranking`, `query_analyzer.py`, `entity_resolver.py`) (CLAUDE.md:125-143).

## 4. LLM / External Service Integration

The repo calls LLMs on every core path; the LLM is required, not optional. `.env.example` makes `HINDSIGHT_API_LLM_PROVIDER`, `HINDSIGHT_API_LLM_API_KEY`, and `HINDSIGHT_API_LLM_MODEL` (default `openai` / `gpt-4o-mini`) the required configuration (`.env.example:6-8`).

- **Providers (enumerated in `.env.example:5`):** `openai, openai-responses, groq, ollama, gemini, anthropic, lmstudio, vertexai, minimax, deepseek, zai, atlas, meta, volcano, openai-codex, claude-code, cursor, github-copilot`. Server docs add `bedrock`, `litellm`, `litellmrouter`, `llamacpp`, and any OpenAI-compatible endpoint (README.md:92). Subscription-backed `openai-codex`, `claude-code`, `cursor`, `github-copilot` need no API key; other providers need keys plus occasional extras (VertexAI project/region, `CODEX_HOME`, `OLLAMA_NUM_CTX`) (README.md:92, `.env.example:109-180`).
- **Required calls:** retain extraction/linking, verification, recall-time analysis, reflect composition, and consolidation each run against the configured LLM; per-operation temperature (`..._VERIFICATION` default `0.0`, `..._RETAIN` `0.1`, `..._REFLECT` `0.9`, `..._CONSOLIDATION` `0.0`) and strict-schema flags confirm distinct LLM invocations per operation (`.env.example:25-44`). Reflect has its own completion-token cap variable (`.env.example:97-102`).
- **Optional/conditional calls:** the vision slot (`HINDSIGHT_API_VLM_PROVIDER/_API_KEY/_MODEL/_BASE_URL`) is used only for retain chunks with inline attachments (`.env.example:11-17`); the mental-model refresh LLM (`HINDSIGHT_API_MENTAL_MODEL_REFRESH_LLM_*`) falls back to `REFLECT_LLM_*` then global `LLM_*` (`.env.example:79-89`).
- **Transport/compat controls:** reasoning effort (`HINDSIGHT_API_LLM_REASONING_EFFORT`), connect timeout (`HINDSIGHT_API_LLM_CONNECT_TIMEOUT`, default cap `10`), HTTP log level, structured-output forced-tool mode, `maxItems`/`pattern` schema-compat toggles for Bedrock-class backends, cache-affinity headers/fields, multi-LLM failover/round-robin/metadata routing (`HINDSIGHT_API_LLM_1_*`, `_2_*`, `_STRATEGY`), and 4xx request dumping (`.env.example:19-107`, `.env.example:181-202`).
- **Client-side wrapper:** `pip install hindsight-litellm`, then `wrap_openai` / `wrap_anthropic` with `bank_id`, `hindsight_api_url`, and per-call `hindsight_*` overrides (bank, recall budget, fact types, reflect-instead-of-recall); LiteLLM underneath covers 100+ models (README.md:231, README.md:235, README.md:257). Explicit control requires calling the SDKs/REST API directly (README.md:259).
- **Other external services:** PostgreSQL (default, incl. embedded pg0) or Oracle AI Database / Oracle 23ai (README.md:96, README.md:103, README.md:80); managed Cloud endpoint `https://api.hindsight.vectorize.io` with usage billing, dashboard, backups, 99.9% SLA (README.md:125).

## 5. The Retain / Recall / Reflect Loop

This is the primary workflow. Step-level module attribution comes from the contributor doc map (CLAUDE.md:125-155); function-level signatures were not in the wiki scope and are not stated here.

1. **Deploy the server** — Docker (`ghcr.io/vectorize-io/hindsight:latest`, ports 8888/9999, `HINDSIGHT_API_LLM_API_KEY`, `hindsight-data` volume) (README.md:80); external-Postgres compose with `HINDSIGHT_DB_PASSWORD` (README.md:96); bare metal `pip install hindsight-api` + `export HINDSIGHT_API_LLM_API_KEY` + `hindsight-api` (README.md:105); Helm with `api.llm.provider/apiKey` + `postgresql.enabled` (README.md:114); or Cloud at `https://api.hindsight.vectorize.io` (README.md:125). Oracle AI Database is the documented enterprise substitute (README.md:103).
2. **Connect a client** — `pip install hindsight-client -U`, `npm install @vectorize-io/hindsight-client`, `go get github.com/vectorize-io/hindsight/hindsight-clients/go`, or the CLI installer `curl -fsSL https://hindsight.vectorize.io/get-cli | bash` (README.md:135). Alternatively run embedded (`pip install hindsight-all -U` + `HindsightServer(llm_provider, llm_model, llm_api_key)` context manager) with no separate server (README.md:199, README.md:207).
3. **Retain (store)** — `client.retain(bank_id, content)` persists an observation; engine path is `memory_engine.py` → `retain/orchestrator` → `retain/fact_extraction` + `retain/link_utils` with `embeddings.py` and the retain LLM at temperature default `0.1` (README.md:142, CLAUDE.md:125-143, `.env.example:25-34`). Attachment-bearing chunks additionally invoke the VLM slot (`.env.example:11-17`).
4. **Recall (search)** — `client.recall(bank_id, query)` runs four parallel strategies (semantic, BM25, graph, temporal) via `search/retrieval`, `search/graph_retrieval`, `search/link_expansion_retrieval`, assisted by `query_analyzer.py` and `entity_resolver.py`, then `search/fusion` and `search/reranking` (`cross_encoder.py`) (README.md:142, CLAUDE.md:125-155).
5. **Reflect (answer)** — `client.reflect(bank_id, query)` returns a disposition-aware response composed by the reflect LLM at temperature default `0.9` under strict-schema and token-cap settings (README.md:142, `.env.example:25-44`, `.env.example:97-102`).
6. **Automate via wrapper** — replace the LLM client with `wrap_openai(OpenAI(), bank_id, hindsight_api_url)` / `wrap_anthropic(...)`; each `chat.completions.create` then recalls before and retains after the call, tunable per call with `hindsight_*` kwargs (README.md:235, README.md:257). Full SDK/REST references (Python, Node, Go, CLI, REST) are linked at README.md:182; knowledge-base, directives, and mental-model operations ride the same `http.py` / `mcp.py` layer (CLAUDE.md:145-155).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | refs to :32–:270 | Project definition, benchmark claims, server/client/embedded/wrapper entry points, platform matrix; truncated at row `Pyd` so integrations tail and Core Concepts/Use Cases/Production sections are missing |
| `.env.example` | 726 lines (visible to ~:212) | Full runtime config surface: LLM/VLM slots, temperatures, strict schema, timeouts, schema compat, cache affinity, refresh LLM, reflect cap, 4xx dumps, multi-LLM routing, API host/port |
| `CLAUDE.md` | 519 lines (visible to ~:277) | Contributor contract: memory model, monorepo map, engine/API/DB maps, dual-dialect migration rule, lint/test gates |
| `AGENTS.md` | 4 lines | Pointer to `CLAUDE.md` as the single coding-conventions source (`AGENTS.md:3`) |
| `hindsight-api-slim/hindsight_api/memory_engine.py` | n/a in wiki | Core memory engine (named in `CLAUDE.md:125-143`; internals not in scope) |
| `hindsight-api-slim/hindsight_api/retain/` (`orchestrator`, `fact_extraction`, `link_utils`) | n/a in wiki | Retain pipeline stages (named in `CLAUDE.md:125-143`) |
| `hindsight-api-slim/hindsight_api/search/` (`retrieval`, `graph_retrieval`, `link_expansion_retrieval`, `fusion`, `reranking`) | n/a in wiki | Recall pipeline stages incl. 4-strategy fan-out and rerank (named in `CLAUDE.md:125-155`) |
| `hindsight-api-slim/hindsight_api/{llm_wrapper,embeddings,cross_encoder,entity_resolver,query_analyzer}.py` | n/a in wiki | LLM invocation, vector/BM25 inputs, rerank scoring, entity linking, query analysis (named in `CLAUDE.md:125-143`) |
| `hindsight-api-slim/hindsight_api/{http,mcp}.py` | n/a in wiki | REST routers and MCP server exposing retain/recall/reflect plus knowledge-base/directives/mental-model ops (per `CLAUDE.md:145-155`) |
| `hindsight-api-slim/hindsight_api/alembic/` | n/a in wiki | Dual-dialect (`run_for_dialect` pg/oracle) Alembic migrations, auto-run on startup (`CLAUDE.md:157-168`) |
| `hindsight-api`, `hindsight-all`, `hindsight-all-slim`, `hindsight-all-npm` | n/a in wiki | Distribution/entrypoint packages: `hindsight-api`, `hindsight-worker`, `hindsight-local-mcp`, `hindsight-admin` binaries; embedded and npm bundles (`CLAUDE.md:107-123`, `package-lock.json:17-20`) |
| `hindsight-control-plane` | n/a in wiki | Next.js UI on port 9999; `npm test`, `npm run lint` (`CLAUDE.md:20-45`, `CLAUDE.md:107-123`, README.md:89) |
| `hindsight-cli` | n/a in wiki | Rust CLI (`cargo build --release`, `cargo test`) (`CLAUDE.md:20-45`, `CLAUDE.md:107-123`) |
| `hindsight-clients` (python/typescript/rust/go) | n/a in wiki | Language SDKs for retain/recall/reflect (`CLAUDE.md:107-123`, README.md:135, README.md:182) |
| `hindsight-integrations` (LiteLLM, CrewAI, LangGraph, Pydantic AI, AG2, Claude Code, coding-agents) | n/a in wiki | No-code-change framework/agent adapters; 60+ claimed (`CLAUDE.md:107-123`, README.md:265, README.md:269) |
| `ruff.toml` / `.prettierrc.json` / `.python-version` | 34 / 8 / 1 lines | Style pins: ruff `line-length 120`, `py311`, `E/W/F/I` with `E501/E402/F401/F841/F811/F821` ignored; prettier semicolons/double-quotes/width 100; Python `3.11` |
| `SECURITY.md` | 40 lines | Support/reporting policy: only `latest` patched, private GitHub Security Advisory reports, 48-hour response, coordinated disclosure |

Line counts for engine/package paths are not stated in the wiki; "n/a in wiki" marks that gap explicitly rather than estimating.

## 7. Dependencies

Only exact version strings visible in the wiki head are quoted; the bulk of manifests was truncated and is not inferred.

| Package | Version constraint | Purpose |
|---|---|---|
| `hindsight-all-npm` | `0.10.1` (exact, `package-lock.json:17-20`) | npm embedded bundle |
| `@vectorize-io/hindsight-client` | `0.10.1` (exact, `package-lock.json:141-154`) | Node.js/TypeScript client SDK |
| `@vectorize-io/hindsight-control-plane` | `0.10.1` (exact, `package-lock.json:255-258`) | Control-plane UI package |
| `python` | `3.11` (exact, `.python-version:1`; ruff `target-version = "py311"`, `ruff.toml:1-34`) | Runtime for API engine and Python clients; dev/test/lint run under `uv run` |
| `hindsight-client` (pip) | constraint not in wiki scope | Python client SDK (`pip install hindsight-client -U`, README.md:135) |
| `hindsight-api` (pip) | constraint not in wiki scope | Bare-metal server distribution (`pip install hindsight-api`, README.md:105) |
| `hindsight-all` / `hindsight-all-slim` (pip) | constraint not in wiki scope | Embedded no-server bundle; `-slim` variant required on Intel Mac (README.md:195, README.md:199, README.md:205) |
| `hindsight-litellm` (pip) | constraint not in wiki scope | LLM wrapper (`wrap_openai`, `wrap_anthropic`), 100+ models via LiteLLM (README.md:231) |
| `ghcr.io/vectorize-io/hindsight:latest` | `latest` tag (verbatim, README.md:80) | Docker server image |
| `oci://ghcr.io/vectorize-io/charts/hindsight` | chart ref, no version in scope (README.md:114) | Helm/Kubernetes install |
| `postgres + pgvector` / `Oracle 23ai` / embedded `pg0` | versions not in wiki scope | Durable vector-relational store; Oracle has stated feature parity (README.md:96, README.md:103, README.md:80, CLAUDE.md:157-159) |
| `node / npm` workspaces (`hindsight-clients/typescript`, `hindsight-control-plane`, `hindsight-docs`, `hindsight-interfig`, `hindsight-all-npm`, `hindsight-tools/hindsight-agent-sdk`) | versions not in wiki scope beyond `lockfileVersion: 3` (`package-lock.json:1-12`) | JS/TS clients, UI, docs, agent SDK |

`package-lock.json` is 35,138 lines; only the head was visible (~1.27M characters truncated), so transitive npm pins are not enumerated (02-top-level-files.md:88).

## 8. CLI / Usage Surface

Entry points (monorepo distribution binaries per `CLAUDE.md:107-123`): `hindsight-api`, `hindsight-worker`, `hindsight-local-mcp`, `hindsight-admin`; plus `HindsightServer`/`HindsightClient` embedded classes, `hindsight-cli` (Rust), per-language SDKs, REST API, MCP server, and the `hindsight-docs` skill.

| Command | Source | Effect |
|---|---|---|
| `docker run ... ghcr.io/vectorize-io/hindsight:latest` with `-p 8888:8888 -p 9999:9999` | README.md:80 | Starts API (:8888) + UI (:9999) with embedded pg0 volume |
| `docker compose up` in `docker/docker-compose` (with `HINDSIGHT_DB_PASSWORD`) | README.md:96 | Starts against external PostgreSQL |
| `pip install hindsight-api` then `hindsight-api` | README.md:105 | Bare-metal server start |
| `helm install hindsight oci://ghcr.io/vectorize-io/charts/hindsight --set api.llm.provider=openai --set api.llm.apiKey=... --set postgresql.enabled=true` | README.md:114 | Kubernetes deploy |
| `pip install hindsight-client -U` / `npm install @vectorize-io/hindsight-client` / `go get github.com/.../hindsight-clients/go` / `curl -fsSL https://hindsight.vectorize.io/get-cli \| bash` | README.md:135 | Install clients |
| `pip install hindsight-all -U` then `HindsightServer(...)` context manager | README.md:199, README.md:207 | Embedded no-server run |
| `pip install hindsight-litellm` then `wrap_openai(...)` / `wrap_anthropic(...)` | README.md:231, README.md:235 | Auto-memory LLM wrapper |
| `npx skills add https://github.com/vectorize-io/hindsight --skill hindsight-docs` | README.md:66 | Install docs skill |
| `./scripts/dev/start.sh`, `./scripts/dev/start-api.sh`, `uv run pytest tests/`, `uv run ruff check .`, `uv run ruff format .`, `uv run ty check hindsight_api/`, `npm test`, `npm run lint`, `cargo build --release`, `cargo test`, `./scripts/generate-openapi.sh`, `./scripts/generate-clients.sh`, `./scripts/hooks/lint.sh` | CLAUDE.md:20-45, CLAUDE.md:251-268 | Dev/test/lint/codegen gates |

Key env vars / config (selection; full surface is the 726-line `.env.example`):

| Variable | Default / example | Purpose |
|---|---|---|
| `HINDSIGHT_API_LLM_PROVIDER` | `openai` | Backend selector (`.env.example:6-8`) |
| `HINDSIGHT_API_LLM_API_KEY` | `your-api-key-here` | Provider credential (`.env.example:6-8`) |
| `HINDSIGHT_API_LLM_MODEL` | `gpt-4o-mini` | Default model (`.env.example:6-8`) |
| `HINDSIGHT_API_LLM_BASE_URL` | `https://api.openai.com/v1` (commented) | OpenAI-compatible override (`.env.example:20`) |
| `HINDSIGHT_API_VLM_PROVIDER/_API_KEY/_MODEL/_BASE_URL` | unset | Vision slot for attachment chunks (`.env.example:11-17`) |
| `HINDSIGHT_API_LLM_REASONING_EFFORT` | unset (`none/low/medium/high/xhigh`) | Reasoning-model effort passthrough (`.env.example:19-23`) |
| `HINDSIGHT_API_LLM_TEMPERATURE` + per-op `..._VERIFICATION/_RETAIN/_REFLECT/_CONSOLIDATION` | global unset; `0.0`/`0.1`/`0.9`/`0.0` | Global vs per-operation sampling control (`.env.example:25-34`) |
| `HINDSIGHT_API_LLM_STRICT_SCHEMA` + per-op variants | unset | `json_schema strict` grammar enforcement (`.env.example:36-44`) |
| `HINDSIGHT_API_LLM_CONNECT_TIMEOUT` | cap `10` | Connect-phase timeout (`.env.example:46-54`) |
| `HINDSIGHT_API_REFLECT_MAX_COMPLETION_TOKENS` | unset = uncapped | Reflect output cap (`.env.example:97-102`) |
| `HINDSIGHT_API_LLM_1_PROVIDER/_API_KEY/_MODEL`, `_2_*`, `_STRATEGY` | unset | Multi-LLM failover/round-robin/metadata routing (`.env.example:181-202`) |
| `HINDSIGHT_API_HOST` / `HINDSIGHT_API_PORT` / `HINDSIGHT_API_LOG_LEVEL` | `0.0.0.0` / `8888` / `info` | Server bind and logging (`.env.example:205-207`) |
| `HINDSIGHT_DB_PASSWORD` | user-chosen | External-Postgres compose credential (README.md:96) |
| `OPENAI_API_KEY` (host) → `HINDSIGHT_API_LLM_API_KEY` (container) | `sk-xxx` | Docker credential injection (README.md:80) |

Supported platforms (exact, README.md:188): Linux x86_64/ARM64 Docker/bare-metal/embedded-pg0 all supported; macOS Apple Silicon all supported; macOS Intel Docker and embedded supported but bare-metal pip degraded (use `hindsight-all-slim`); Windows x86_64 all supported (README.md:188, README.md:195, README.md:205).

## 9. Extensibility Points

- **New agent-framework / coding-agent adapter** → add to `hindsight-integrations` (houses LiteLLM, CrewAI, LangGraph, Pydantic AI, AG2, Claude Code, coding-agents); 60+ integrations already live here and most require no caller code changes (CLAUDE.md:107-123, README.md:265).
- **New client language or transport** → add to `hindsight-clients` (Python/TS/Rust/Go) and regenerate via `./scripts/generate-clients.sh` + `./scripts/generate-openapi.sh` (CLAUDE.md:20-45, CLAUDE.md:107-123).
- **New server distribution or background role** → extend `hindsight-api` entrypoints (`hindsight-api`, `hindsight-worker`, `hindsight-local-mcp`, `hindsight-admin`) (CLAUDE.md:107-123).
- **New retrieval strategy or reranker** → extend `hindsight-api-slim/hindsight_api/search/` (`retrieval`, `graph_retrieval`, `link_expansion_retrieval`, `fusion`, `reranking`) plus `embeddings.py`, `cross_encoder.py`, `entity_resolver.py`, `query_analyzer.py` (CLAUDE.md:125-143).
- **New retain/extraction behavior** → extend `hindsight-api-slim/hindsight_api/retain/` (`orchestrator`, `fact_extraction`, `link_utils`) and `memory_engine.py` / `llm_wrapper.py` (CLAUDE.md:125-143).
- **New API/MCP operation** → add routers in `http.py` / `mcp.py` alongside the existing retain/recall/reflect/knowledge-base/directives/mental-model surface (CLAUDE.md:145-155).
- **New datastore dialect** → add both arms of `run_for_dialect(pg=..., oracle=...)` in a new Alembic file under `hindsight-api-slim/hindsight_api/alembic/` (12-char hex revision, `down_revision` set); CI `tests/test_migration_shape.py` fails without the dispatcher (CLAUDE.md:163-168).
- **Packaged extensions / agent tooling** → use `hindsight-extensions` and `hindsight-tools` (`@vectorize-io/hindsight-agent-sdk`) (CLAUDE.md:107-123).

## 10. Limitations and Gotchas

- **Wiki coverage itself is truncated.** The integrations table cuts off mid-row at `Pyd` (README.md:270), and `.env.example` (~35K chars unseen past the API block), `CLAUDE.md` (~13.6K chars unseen), and `package-lock.json` (~1.27M chars unseen) are all cut; Core Concepts detail, Use Cases, Production, and Resources sections are therefore not covered and no claims are made about them (01-overview.md:129, 02-top-level-files.md:12).
- **Intel-macOS bare-metal is degraded.** The platform matrix marks macOS Intel pip installs as caution-only; the documented workaround is the `hindsight-all-slim` variant rather than the full bundle (README.md:188, README.md:195, README.md:205).
- **LLM is a hard runtime dependency with cost/latency exposure.** Every retain/recall/reflect path invokes the configured LLM (per-operation temperatures and strict-schema flags confirm separate calls), and live accuracy/latency/cost varies per model on the external benchmark page; misconfiguring provider, model, timeouts, or schema-compat flags (e.g. Bedrock `maxItems`/`pattern` rejections) breaks or slows operations (`.env.example:6-107`, README.md:58, README.md:92).
- **Only `latest` gets security patches.** The policy supports a single version line; pinned deployments must track forward to stay covered, and reports must go privately via GitHub Security Advisory with full paths, reproduction, and impact before any public disclosure (SECURITY.md:5-38).
- **Dual-dialect migration discipline is mandatory.** Every Alembic migration must implement both `_pg_upgrade` and `_oracle_upgrade` through `run_for_dialect`; omitting the dispatcher fails `tests/test_migration_shape.py` in CI, so single-dialect changes are rejected by the gate (CLAUDE.md:163-168).
- **Lint/type gates are strict and multi-language.** Python changes must pass `ruff check`, `ruff format`, and `ty check`; TS changes must pass `./scripts/hooks/lint.sh` plus `npm run lint`; `check-unused-code` blocks on ruff `F401/F841` and knip, with `/code-review` required after implementation and mandatorily before push/PR — unreviewed pushes violate the contributor contract (CLAUDE.md:251-268, CLAUDE.md:20-45, `ruff.toml:1-34`).

## 11. How It Compares to Alternatives

The wiki names technique classes rather than specific competing products; no named third-party memory system appears in the covered pages. The three contrast classes, all stated explicitly, are:

- **Conversation-history recall systems** — store and replay transcripts; Hindsight positions itself as learning (facts, experience, mental models consolidated across sessions) rather than replaying history (README.md:32).
- **RAG pipelines** — retrieve passages at query time without consolidating durable learned state or dispositions; the wiki claims Hindsight eliminates RAG's shortcomings for long-term memory tasks (README.md:36).
- **Knowledge-graph extraction systems** — triple/graph construction without the fact-plus-mental-model consolidation and four-strategy (semantic/BM25/graph/temporal) fused retrieval with reranking that Hindsight uses (README.md:36, CLAUDE.md:145-155).
- **Self-reported vendor benchmarks** — unnamed other vendors' scores are described as self-reported, versus Hindsight's LongMemEval numbers reproduced by Virginia Tech's Sanghani Center and The Washington Post with live per-model accuracy/latency/cost published externally (README.md:58, README.md:60).

Positioning sentence: within the wiki's framing, Hindsight occupies the "learning memory server" slot — a stateful retain/recall/reflect service with hybrid retrieval and per-framework adapters — against stateless recall buffers, pass-through RAG retrievers, and graph-only stores, with its differentiation argued empirically through reproduced LongMemEval results rather than API-shape comparisons.

## Appendix: Selected Code Snippets

Docker server start (README.md:80):

```bash
export OPENAI_API_KEY=sk-xxx

docker run -it --pull always --name hindsight --restart unless-stopped -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
  -v hindsight-data:/home/hindsight/.pg0 \
  ghcr.io/vectorize-io/hindsight:latest
```

Python retain/recall/reflect (README.md:142):

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")

# Retain: Store information
client.retain(bank_id="my-bank", content="Alice works at Google as a software engineer")

# Recall: Search memories
client.recall(bank_id="my-bank", query="What does Alice do?")

# Reflect: Generate disposition-aware response
client.reflect(bank_id="my-bank", query="Tell me about Alice")
```

Python embedded, no server (README.md:207):

```python
import os
from hindsight import HindsightServer, HindsightClient

with HindsightServer(
    llm_provider="openai",
    llm_model="gpt-5-mini",
    llm_api_key=os.environ["OPENAI_API_KEY"]
) as server:
    client = HindsightClient(base_url=server.url)
    client.retain(bank_id="my-bank", content="Alice works at Google")
    results = client.recall(bank_id="my-bank", query="Where does Alice work?")
```

LLM wrapper (README.md:235):

```python
from openai import OpenAI
from hindsight_litellm import wrap_openai

# Defaults to Hindsight Cloud; pass hindsight_api_url for a self-hosted server.
client = wrap_openai(
    OpenAI(),
    bank_id="user-123",
    hindsight_api_url="http://localhost:8888",
)

# and retains the conversation after it.
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "What do you know about me?"}],
)
```
