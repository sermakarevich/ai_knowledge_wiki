> [[index|Wiki]] | [[summary|Summary]]
# mateaix/mateclaw — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** MateClaw is a self-hosted, pluggable agent runtime ("second brain") that runs digital employees over native or DSH engines with multi-provider failover, linked knowledge/memory, tools, channels, and durable team execution in one deployment.
## Key points
- MateClaw positions itself as a whole-widget deployment — reasoning, knowledge, memory, tools, and channels built together in one deployment, with automatic retry on the next healthy provider when the primary model fails (01-overview.md:43-45, 01-overview.md:51-57).
- A provider health tracker parks failing vendors in a cooldown window and only returns an error when the available chain is exhausted; providers are ordered in Settings → Models (01-overview.md:55-57).
- The `AgentRuntimeProvider` contract separates employee identity from the execution engine, offering a native StateGraph runtime (ReAct, Plan-and-Execute, Goals, Team Runs) or a managed DSH (`dsh-jsonrpc-agent`) external loop over authenticated JSON-RPC with normalized runtime events (01-overview.md:41-42, 01-overview.md:94-95).
- Persistent Goals make long work recoverable: the database preserves checklist, continuation state, attempts, cooldowns, leases, and user input, and the supervisor reconciles interrupted attempts after a single-backend restart instead of repeating the task (01-overview.md:99-102).
- One durable Team Run (`runId`) links objective, task DAG, worker executions, synthesis, and deliverables, with chat as outcome surface, Agents Live for observation, and Teams for history/governance over a shared board with parallel dispatch, leases, cancel-interrupt, and approval gates (01-overview.md:108-110).
- The LLM Wiki digests raw materials (PDF, markdown, scraped pages) into structured pages with `[[links]]` and traceable citations plus a citation drawer and hot cache auto-injected into system prompts (01-overview.md:63-65, 01-overview.md:114).
- Capability is extended three ways — SKILL.md packages (manifest + prompt + tool list + LESSONS.md), MCP (stdio/SSE/Streamable HTTP with per-employee binding), and ACP (Claude Code/Codex bridged to skill cards) — all bounded by Tool Guard RBAC, approvals, and path protection (01-overview.md:120-124).
- Enterprise posture is multi-user workspaces with approval-gated sensitive actions, full audit trail, Actuator health monitoring, per-channel error isolation, and an Admin Runtime Console (Settings → System → Runtime) with force-recycle, consistent lifecycle semantics, and per-event SSE IDs for safe reconnects (01-overview.md:37-40, 01-overview.md:135-136).

## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** Top-level files define how the MateClaw repo is configured, built, deployed, and presented — Docker build context, environment template, line-ending/checkout policy, ignored paths, and the Chinese-language product README.
## Key points
- `.dockerignore` keeps build context lean by excluding git/IDE artifacts, Node/Maven outputs, the desktop app, data/logs, secrets, and most markdown with narrow re-inclusions (`.dockerignore:1-28`).
- `.env.example` is the single copy-and-rename deployment template (`cp .env.example .env`) where every required-but-unset value fails `docker compose up` instead of shipping defaults (`.env.example:1-6`).
- `.env.example` pins the Docker stack to PostgreSQL 16 (`DB_HOST`, `DB_PORT=5432`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `DB_ADMIN_USERNAME`, `DB_ADMIN_PASSWORD`) and warns old MySQL volumes need `mysqldump`/migration (`.env.example:8-29`).
- `.env.example` documents all optional runtime tuning under exact names: search keys, `JWT_SECRET`, CORS/public-URL/OpenAPI flags, browser CDP/path/channel, Playwright SSRF/timeout/snapshot limits, OpenAI OAuth mode, wiki allowlist/watcher, skill workspace/upload caps, pip mirror, and Maven flags (`.env.example:31-165`).
- `.gitattributes` pins `*.sh`/`*.bash`/`*.sql` to LF so bind-mounted Linux init scripts and Flyway checksums survive Windows checkouts, while `*.bat`/`*.cmd`/`*.ps1` keep CRLF (`.gitattributes:1-20`).
- `.gitignore` excludes Gradle/Maven/Node/VitePress/Astro build outputs, IDE files, logs, local runtime data (`mateclaw-server/data/`, `.sessions/`, `/data/`), secrets (`.env` but not `.env.example`), SSL certs, and stray npm/yarn lockfiles in this pnpm monorepo (`.gitignore:1-136`).
- `README_zh.md` is the product entry point (v2.3.0, 2026-09-20): pluggable Agent Runtime, provider failover, LLM Wiki, five entrances, quick-start, repo layout, stack table, and roadmap — chunk content is truncated so post-2.1.0 roadmap detail is not covered here (`README_zh.md:33-270`).

## The system in five moves
1. MateClaw frames itself as a self-hosted "second brain" — one deployment bundling reasoning, knowledge, memory, tools, and channels for multi-user, approval-gated work.
2. Execution runs through a pluggable `AgentRuntimeProvider` contract: a native StateGraph engine or a managed DSH external loop, decoupled from employee identity.
3. Reliability comes from provider failover with health-tracked cooldowns plus durable Goals and Team Runs that persist checklists, leases, DAGs, and evidence across restarts.
4. Knowledge and capability grow via the LLM Wiki (digested, linked, citation-traceable pages), SKILL.md/MCP/ACP extensions bounded by Tool Guard, and workflow/trigger orchestration.
5. Deployment and presentation are pinned at the repo top level: lean Docker context, a fail-closed `.env.example` over PostgreSQL 16, LF/CRLF checkout policy, pnpm-scoped ignores, and the Chinese product README as entry point.
