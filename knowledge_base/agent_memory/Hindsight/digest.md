> [[index|Wiki]] | [[summary|Summary]]
# vectorize-io/hindsight — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Hindsight is an agent memory system that makes agents learn over time rather than just recall conversation history (README.md:32).
- Hindsight is an agent memory system focused on learning, explicitly positioned against recall-only history, RAG, and knowledge-graph techniques (README.md:32, README.md:36).
- It claims state-of-the-art accuracy on the LongMemEval long-term memory benchmark, with live per-model accuracy, latency, and cost published externally (README.md:54, README.md:58).
- Benchmark data was independently reproduced by Virginia Tech's Sanghani Center and The Washington Post, while other vendors' scores are self-reported (README.md:60).
- The system is deployed as a server (Docker, external PostgreSQL, pip bare metal, Helm/Kubernetes, or hosted Cloud) exposing API on port 8888 and UI on port 9999 (README.md:76, README.md:89, README.md:94, README.md:105, README.md:114, README.md:125).
- Clients connect via Python (`hindsight-client`), Node.js (`@vectorize-io/hindsight-client`), Go, CLI, REST API, or no-server embedded modes, using the three operations retain / recall / reflect against a `bank_id` (README.md:135, README.md:145, README.md:168, README.md:182).
- The LLM Wrapper (`wrap_openai`, `wrap_anthropic` via `hindsight-litellm`) auto-stores and retrieves memories on every LLM call with per-call `hindsight_*` overrides and 100+ model coverage through LiteLLM (README.md:229, README.md:257).
- It ships 60+ no-code-change integrations spanning coding agents and agent frameworks, plus a docs skill installed via `npx skills add` (README.md:66, README.md:265).

## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** The repository root files define the runtime configuration surface (`.env.example`), contributor workflow (`CLAUDE.md`, `AGENTS.md`), build ignores (`.dockerignore`, `.gitignore`), formatter/linter pins (`.prettierrc.json`, `ruff.toml`, `.python-version`), the npm lockfile (`package-lock.json`), and the vulnerability-reporting policy (`SECURITY.md`).
- `.env.example` makes `HINDSIGHT_API_LLM_PROVIDER`, `HINDSIGHT_API_LLM_API_KEY`, and `HINDSIGHT_API_LLM_MODEL` (default `openai` / `gpt-4o-mini`) the required LLM configuration (`.env.example:6-8`).
- `.env.example` sets the API server defaults to `HINDSIGHT_API_HOST=0.0.0.0`, `HINDSIGHT_API_PORT=8888`, `HINDSIGHT_API_LOG_LEVEL=info` (`.env.example:205-207`).
- `CLAUDE.md` defines Hindsight as an agent memory system with world facts, experience facts, and mental models, plus the monorepo package map and dev/test/lint commands (`CLAUDE.md:7-9`, `CLAUDE.md:107-123`, `CLAUDE.md:20-45`).
- `CLAUDE.md` mandates the dual-dialect migration shape (`run_for_dialect` with `_pg_upgrade`/`_oracle_upgrade`) and documents the lint/test gates (`lint.sh`, `/code-review`) (`CLAUDE.md:163-224`, `CLAUDE.md:251-268`).
- `.dockerignore` excludes `node_modules`, `.next`, Python artifacts (`__pycache__`, `.venv`, `dist`, `egg-info`), `.git`, IDE/OS files, `target`, logs, and test caches from the Docker build context (`.dockerignore:2-34`).
- `ruff.toml` pins `line-length = 120`, `target-version = "py311"`, lint selects `E/W/F/I` with ignores for `E501/E402/F401/F841/F811/F821`, and double-quote space-indent formatting (`ruff.toml:1-34`).
- `SECURITY.md` supports only `latest` for patches, requires private reports via GitHub Security Advisory with a 48-hour response, and follows coordinated disclosure (`SECURITY.md:5-10`, `SECURITY.md:14-17`, `SECURITY.md:38`).
- Truncated in this chunk, so not fully covered here: `.env.example` (cut after ~212 visible lines, ~35887 more characters), `CLAUDE.md` (cut at ~277 visible lines, ~13611 more characters), and `package-lock.json` (cut near the top, ~1265578 more characters).

## The system in five moves
1. Hindsight starts from a learning-over-recall premise, positioning itself against history replay, RAG, and knowledge graphs and backing the claim with LongMemEval SOTA scores reproduced by Virginia Tech and The Washington Post.
2. That memory system is delivered as a server with fixed API/UI ports across Docker, external PostgreSQL, pip, Helm/Kubernetes, and hosted Cloud deployment shapes.
3. Clients reach it through Python, Node.js, Go, CLI, REST, or no-server embedded modes using the retain / recall / reflect operations scoped to a `bank_id`.
4. The LLM Wrapper and 60+ integrations make adoption automatic, storing and retrieving memories on every LLM call across 100+ LiteLLM-covered models.
5. Underneath, the repository root pins the runtime and contributor substrate: `.env.example` LLM/API defaults, `CLAUDE.md` memory model plus monorepo, migration, and lint/test gates, build ignores, formatter pins, and a latest-only coordinated-disclosure security policy.
