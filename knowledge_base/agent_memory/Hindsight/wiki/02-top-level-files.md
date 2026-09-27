> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repository root files define the runtime configuration surface (`.env.example`), contributor workflow (`CLAUDE.md`, `AGENTS.md`), build ignores (`.dockerignore`, `.gitignore`), formatter/linter pins (`.prettierrc.json`, `ruff.toml`, `.python-version`), the npm lockfile (`package-lock.json`), and the vulnerability-reporting policy (`SECURITY.md`).
## Key points
- `.env.example` makes `HINDSIGHT_API_LLM_PROVIDER`, `HINDSIGHT_API_LLM_API_KEY`, and `HINDSIGHT_API_LLM_MODEL` (default `openai` / `gpt-4o-mini`) the required LLM configuration (`.env.example:6-8`).
- `.env.example` sets the API server defaults to `HINDSIGHT_API_HOST=0.0.0.0`, `HINDSIGHT_API_PORT=8888`, `HINDSIGHT_API_LOG_LEVEL=info` (`.env.example:205-207`).
- `CLAUDE.md` defines Hindsight as an agent memory system with world facts, experience facts, and mental models, plus the monorepo package map and dev/test/lint commands (`CLAUDE.md:7-9`, `CLAUDE.md:107-123`, `CLAUDE.md:20-45`).
- `CLAUDE.md` mandates the dual-dialect migration shape (`run_for_dialect` with `_pg_upgrade`/`_oracle_upgrade`) and documents the lint/test gates (`lint.sh`, `/code-review`) (`CLAUDE.md:163-224`, `CLAUDE.md:251-268`).
- `.dockerignore` excludes `node_modules`, `.next`, Python artifacts (`__pycache__`, `.venv`, `dist`, `egg-info`), `.git`, IDE/OS files, `target`, logs, and test caches from the Docker build context (`.dockerignore:2-34`).
- `ruff.toml` pins `line-length = 120`, `target-version = "py311"`, lint selects `E/W/F/I` with ignores for `E501/E402/F401/F841/F811/F821`, and double-quote space-indent formatting (`ruff.toml:1-34`).
- `SECURITY.md` supports only `latest` for patches, requires private reports via GitHub Security Advisory with a 48-hour response, and follows coordinated disclosure (`SECURITY.md:5-10`, `SECURITY.md:14-17`, `SECURITY.md:38`).
- Truncated in this chunk, so not fully covered here: `.env.example` (cut after ~212 visible lines, ~35887 more characters), `CLAUDE.md` (cut at ~277 visible lines, ~13611 more characters), and `package-lock.json` (cut near the top, ~1265578 more characters).
---
## Environment template (`.env.example`)
Visible portion documents the LLM and API surface (rest of the 726-line file was truncated in the chunk, so anything past the API block below is not covered):
```ini
HINDSIGHT_API_LLM_PROVIDER=openai
HINDSIGHT_API_LLM_API_KEY=your-api-key-here
HINDSIGHT_API_LLM_MODEL=gpt-4o-mini
# HINDSIGHT_API_LLM_BASE_URL=https://api.openai.com/v1
```
Supported providers are enumerated in a comment (`.env.example:5`):
`openai, openai-responses, groq, ollama, gemini, anthropic, lmstudio, vertexai, minimax, deepseek, zai, atlas, meta, volcano, openai-codex, claude-code, cursor, github-copilot`.

| Setting group | Variables (exact names) | Notes (from chunk) |
|---|---|---|
| Vision slot | `HINDSIGHT_API_VLM_PROVIDER`, `HINDSIGHT_API_VLM_API_KEY`, `HINDSIGHT_API_VLM_MODEL`, `HINDSIGHT_API_VLM_BASE_URL` | Only retain chunks with inline attachments use it; text-only chunks stay on the retain LLM (`.env.example:11-17`) |
| Reasoning effort | `HINDSIGHT_API_LLM_REASONING_EFFORT` | e.g. `none, low, medium, high, xhigh`; sent as given; `none` stops self-hosted reasoning models emitting thinking blocks; unset sends nothing (`.env.example:19-23`) |
| Temperature | `HINDSIGHT_API_LLM_TEMPERATURE` + per-op `..._VERIFICATION` (default `0.0`), `..._RETAIN` (`0.1`), `..._REFLECT` (`0.9`), `..._CONSOLIDATION` (`0.0`); `none` omits the parameter | Global applies to every operation; per-operation takes precedence (`.env.example:25-34`) |
| Strict schema | `HINDSIGHT_API_LLM_STRICT_SCHEMA` + per-op `..._RETAIN`, `..._REFLECT`, `..._CONSOLIDATION` | Grammar-enforces `json_schema strict` for weaker self-hosted models; per-op flags work in both directions (`.env.example:36-44`) |
| Timeouts/transport | `HINDSIGHT_API_LLM_CONNECT_TIMEOUT` (default cap `10`, `0` disables), `HINDSIGHT_API_LLM_HTTP_LOG_LEVEL` | Connect phase only; read/write/pool keep the full `LLM_TIMEOUT` budget (`.env.example:46-54`) |
| Schema compat | `HINDSIGHT_API_LLM_SUPPORTS_MAX_ITEMS` (default `true`), `HINDSIGHT_API_LLM_SUPPORTS_STRING_PATTERN` (default `false`) | For backends rejecting `maxItems` (e.g. Bedrock Converse) or `pattern` (Bedrock allowlist) (`.env.example:56-64`) |
| Cache affinity | `HINDSIGHT_API_LLM_CACHE_AFFINITY` (`auto`) + per-op `RETAIN/REFLECT/CONSOLIDATION` overrides | `auto` allowlist: x.ai/grok.com get the header, native OpenAI/Azure gets the field, others nothing (`.env.example:66-77`) |
| Mental-model refresh LLM | `HINDSIGHT_API_MENTAL_MODEL_REFRESH_LLM_PROVIDER/MODEL/TIMEOUT/MAX_CONCURRENT` | Falls back to `REFLECT_LLM_*` (then global `LLM_*`), except timeout which falls back to `LLM_TIMEOUT` (`.env.example:79-89`) |
| Structured output | `HINDSIGHT_API_LLM_STRUCTURED_OUTPUT_FORCED_TOOL` | Forced tool call instead of `response_format` for backends rejecting it (e.g. Bedrock Claude in ap-southeast-2) (`.env.example:91-95`) |
| Reflect cap | `HINDSIGHT_API_REFLECT_MAX_COMPLETION_TOKENS` | Unset = uncapped; visible length governed by prompt directive + post-hoc rewrite, not provider truncation (`.env.example:97-102`) |
| 4xx diagnostics | `HINDSIGHT_API_LLM_DEBUG_DUMP_4XX` | Logs assembled request with stripped bodies + capped previews; off by default (`.env.example:104-107`) |
| Provider examples | Anthropic (`anthropic` / `claude-sonnet-4-20250514`), GitHub Copilot (`github-copilot`, no key, Copilot CLI sign-in), VertexAI (`vertexai` + project/region/key), MiniMax, `openai-responses`, DeepSeek, z.ai, Atlas, Meta (`meta` / `muse-spark-1.3`), LM Studio, Ollama (+ `OLLAMA_NUM_CTX`), `openai-codex` (+ `CODEX_HOME`) | Commented examples only (`.env.example:109-180`) |
| Multi-LLM | `HINDSIGHT_API_LLM_1_PROVIDER/_API_KEY/_MODEL`, `HINDSIGHT_API_LLM_2_PROVIDER/...`, `HINDSIGHT_API_LLM_STRATEGY` | Indices from 1, contiguous; strategy JSON `failover` / `round-robin` (optional `weights`) / `metadata` (retain-only, first matching route wins) (`.env.example:181-202`) |
| API server | `HINDSIGHT_API_HOST=0.0.0.0`, `HINDSIGHT_API_PORT=8888`, `HINDSIGHT_API_LOG_LEVEL=info`, plus `HINDSIGHT_API_GZIP_MIN_SIZE`, `HINDSIGHT_API_LOOP_LAG_REPORT_SECONDS` | Visible tail before truncation (`.env.example:205-212`) |

## Contributor entry points (`CLAUDE.md`, `AGENTS.md`)
`AGENTS.md` is a 4-line pointer: `See [CLAUDE.md](./CLAUDE.md) for project documentation and coding conventions` (`AGENTS.md:3`).
`CLAUDE.md` (519 lines; chunk shows ~277, remainder truncated) states the project model and commands:
- Memory model: world facts, experience facts, mental models (`CLAUDE.md:7-9`).
- Local dev commands (verbatim, `CLAUDE.md:20-45`):
```bash
./scripts/dev/start.sh
./scripts/dev/start-api.sh
cd hindsight-api-slim && uv run pytest tests/
cd hindsight-api-slim && uv run pytest tests/test_http_api_integration.py -v
cd hindsight-api-slim && uv run pytest tests/test_retain.py::test_retain_with_chunks -v
cd hindsight-api-slim && uv run ruff check .
cd hindsight-api-slim && uv run ruff format .
cd hindsight-api-slim && uv run ty check hindsight_api/
cd hindsight-control-plane && npm test
cd hindsight-control-plane && npm run lint
cd hindsight-cli && cargo build --release
cd hindsight-cli && cargo test
./scripts/generate-openapi.sh
./scripts/generate-clients.sh
```
- Monorepo map (`CLAUDE.md:107-123`): `hindsight-api-slim` (core FastAPI engine), `hindsight-api` (distribution entrypoints `hindsight-api`, `hindsight-worker`, `hindsight-local-mcp`, `hindsight-admin`), `hindsight-all` / `hindsight-all-slim`, `hindsight-all-npm` (`@vectorize-io/hindsight-all`), `hindsight-control-plane` (Next.js), `hindsight-cli` (Rust), `hindsight-clients` (Python/TS/Rust/Go), `hindsight-docs`, `hindsight-integrations` (LiteLLM, CrewAI, LangGraph, Pydantic AI, AG2, Claude Code, coding-agents), `hindsight-embed`, `hindsight-system-tests`, `hindsight-system-evals`, `hindsight-integration-tests`, `hindsight-extensions`, `hindsight-tools` (`@vectorize-io/hindsight-agent-sdk`), `hindsight-dev`.
- Core engine files (`CLAUDE.md:125-143`): `memory_engine.py`, `llm_wrapper.py`, `embeddings.py`, `cross_encoder.py`, `entity_resolver.py`, `query_analyzer.py`, `retain/{orchestrator,fact_extraction,link_utils}.py`, `search/{retrieval,graph_retrieval,link_expansion_retrieval,fusion,reranking}.py`.
- API layer (`CLAUDE.md:145-155`): `http.py` (REST routers), `mcp.py` (MCP server); operations Retain / Recall (4 parallel strategies: semantic, BM25, graph, temporal + reranking) / Reflect / Knowledge Base / Directives & Mental Models.
- Database (`CLAUDE.md:157-159`): PostgreSQL with pgvector (also Oracle 23ai); Alembic migrations in `hindsight-api-slim/hindsight_api/alembic/`, auto-run on startup; tables `banks, documents, chunks, entities, memory_units, unit_entities, memory_links`.
- Migration rule (`CLAUDE.md:163-168`): every migration dispatches via `run_for_dialect(pg=..., oracle=...)`; `tests/test_migration_shape.py` fails CI if the dispatcher is omitted; file name `<revision_id>_<description>.py`, 12-char hex revision, `down_revision` set.
- Quality gates (`CLAUDE.md:251-268`): read `.claude/skills/code-review/SKILL.md` before writing code; run `./scripts/hooks/lint.sh` after Python/TS changes; CI `check-unused-code` blocks on ruff `F401/F841` + knip, advisory on vulture/unused exports; run `/code-review` after implementation and mandatorily before push/PR.

## Build ignores (`.dockerignore`, `.gitignore`)
`.dockerignore` (34 lines) excludes, verbatim patterns (`.dockerignore:2-34`):
`**/node_modules`, `**/.next`, `**/__pycache__`, `**/*.pyc`, `**/.venv`, `**/dist`, `**/*.egg-info`, `.git`, `.gitignore`, `.idea`, `.vscode`, `*.swp`, `.DS_Store`, `Thumbs.db`, `**/target`, `**/*.log`, `**/coverage`, `**/.pytest_cache`, `**/.mypy_cache`, `**/.next-*`.
`.gitignore` (79 lines) additionally ignores release-staged `LICENSE` copies under `hindsight-clients/python`, `hindsight-api-slim`, `hindsight-api`, `hindsight-all`, `hindsight-all-slim`, `hindsight-embed` (`.gitignore:9-14`); `.venv`, `node_modules` (both directory and symlink forms, `.gitignore:18-25`); secrets/local compose (`.env`, `.env.bak*`, `.env.*.bak`, `docker-compose.yml`, `docker-compose.override.yml`, `.gitignore:28-32`); data/stack dirs (`nltk_data/`, `.monitoring/`, `.pgbouncer/`, `**/longmemeval_s_cleaned.json`, `logs/`, `.gitignore:38-51`); generated docs `hindsight-docs/static/llms-full.txt` (`.gitignore:57`); benchmark results, `hindsight-cli/target`, `hindsight-clients/rust/target`, `.claude/*` (except `!.claude/skills/`), `whats-next.md`, `TASK.md`, `hindsight-integrations/_drafts/` (`.gitignore:60-73`).

## Pins and style (`.python-version`, `.prettierrc.json`, `ruff.toml`, `package-lock.json`)
- `.python-version` pins `3.11` (`.python-version:1`).
- `.prettierrc.json` (verbatim, `.prettierrc.json:1-8`):
```json
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```
- `ruff.toml` (verbatim essentials, `ruff.toml:1-34`): `line-length = 120`, `target-version = "py311"`, excludes `**/.venv/`, `**/dist/`, `**/build/`; lint excludes `tests/**`, selects `E, W, F, I`, ignores `E501, E402, F401, F841, F811, F821`; format `quote-style = "double"`, `indent-style = "space"`.
- `package-lock.json` (35138 lines; chunk shows only the head, ~1265578 characters truncated): `lockfileVersion: 3`, root `hindsight` with workspaces `hindsight-clients/typescript`, `hindsight-control-plane`, `hindsight-docs`, `hindsight-interfig`, `hindsight-all-npm`, `hindsight-tools/hindsight-agent-sdk` (`package-lock.json:1-12`); visible pinned entries include `hindsight-all-npm@0.10.1`, `@vectorize-io/hindsight-client@0.10.1`, `@vectorize-io/hindsight-control-plane@0.10.1` (`package-lock.json:17-20`, `package-lock.json:141-154`, `package-lock.json:255-258`). Contents past the head were cut, so no further claims are made.

## Security policy (`SECURITY.md`)
40 lines, fully visible. Supported versions table lists only `latest` as supported (`SECURITY.md:5-10`). Reports go privately via GitHub Security Advisory (`SECURITY.md:14-15`); response within 48 hours, patch typically within days (`SECURITY.md:17-19`); required fields: issue type, full source paths, tag/branch/commit or URL, reproduction config and steps, PoC/exploit if possible, impact/exploit description (`SECURITY.md:21-29`); English preferred (`SECURITY.md:32-34`); coordinated vulnerability disclosure per CISA (`SECURITY.md:36-38`).

**Covers:** `.dockerignore`, `.env.example`, `.gitignore`, `.prettierrc.json`, `.python-version`, `AGENTS.md`, `CLAUDE.md`, `package-lock.json`, `ruff.toml`, `SECURITY.md`
