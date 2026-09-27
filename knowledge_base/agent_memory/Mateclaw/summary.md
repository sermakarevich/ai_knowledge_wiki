# Technical Analysis: mateaix/mateclaw

**Repository:** https://github.com/mateaix/mateclaw
**Version analyzed:** v2.3.0 (2026-09-20)
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview

Problem space: single-person chat agents fail IT sign-off and fail at long-horizon work — no multi-user governance, no audit trail, no recovery after model outage or backend restart, and knowledge/memory/tools/channels are split across deployments (01-overview.md:37-40, 01-overview.md:99-102).

What the repo does: MateClaw ships a self-hosted, pluggable agent runtime ("second brain") as one deployment (single JAR / Docker Compose / Electron desktop) combining reasoning, LLM Wiki knowledge, workspace memory, SKILL.md/MCP/ACP tools, workflow/trigger orchestration, and multi-channel surfaces under one session/workspace/credential/approval store (01-overview.md:3, 01-overview.md:15, 01-overview.md:32).

Primary user: a team or organization deploying internal "digital employees" (six built-in templates: General Assistant, Product Assistant, Research Analyst, Customer Support, Data Analyst, Code Reviewer) that need approval-gated actions, audit, health monitoring, and channel isolation rather than an individual chatbot user (01-overview.md:29-30, 01-overview.md:15).

## 2. High-Level Architecture

```
User doors: Web Console │ Desktop (Electron+JRE21) │ Webchat <script> │ IM (DingTalk/Feishu/WeCom/WeChat/TG/Discord/QQ/Slack)
        │ ▼
Employees (Role/Goal/Backstory/avatar) ──► AgentRuntimeProvider contract ──► Native StateGraph │ DSH (dsh-jsonrpc-agent child proc)
        │ ▼                                                                    │ normalized thinking/tool/answer events, SSE IDs
Knowledge/Memory: LLM Wiki + hot cache │ AGENTS/SOUL/PROFILE/MEMORY.md + Dreaming │ Skills/MCP/ACP + Tool Guard
        │ ▼
Durable execution: Goals (checklist/leases/artifacts) │ Team Runs (runId→DAG→workers→synthesis) │ Workflows/Triggers/Wiki Transformations
        │ ▼
Persistence: PostgreSQL 16 (Docker) / H2 / MySQL 8.0+ / Kingbase + Flyway │ workspace files (skills root, MEMORY.md, progress ledgers)
        │ ▼
Ops: Admin Runtime Console + Actuator + audit trail + provider health tracker + force-recycle
```

Data-flow narrative:

1. A request enters through any surface (console, desktop, webchat, IM channel); per-channel error isolation keeps one channel failure from affecting others, and all doors share the same brain, memory, and tools (01-overview.md:28, 01-overview.md:37-40).
2. The request binds to a digital employee identity (Role, Goal, Backstory); `AgentRuntimeProvider` selects the native StateGraph runtime (ReAct, Plan-and-Execute, Goals, Team Runs) or the managed DSH external loop over authenticated JSON-RPC, validated for availability/capabilities before startup (01-overview.md:29-30, 01-overview.md:31-32).
3. Each turn resolves the model through an ordered provider chain (DashScope, OpenAI, Anthropic, Gemini, DeepSeek, Kimi, Ollama, LM Studio, MLX); the health tracker parks failing vendors in cooldown and fails over to the next healthy provider, erroring only when the chain is exhausted (01-overview.md:18-19).
4. The turn executes with injected context (LLM Wiki hot cache auto-injected into the system prompt plus workspace memory files) and bounded tools (SKILL.md packages, per-employee MCP bindings, ACP-bridged coding agents) gated by Tool Guard RBAC/approvals/path protection (01-overview.md:10, 01-overview.md:41-45).
5. Long or multi-worker work persists as Goals (checklist, continuation state, attempts, cooldowns, leases, artifacts) or Team Runs (stable `runId` linking objective, task DAG, worker executions, synthesis, deliverables on a shared board with leases, cancel-interrupt, approval gates); after a single-backend restart the supervisor reconciles from checkpoints instead of repeating (01-overview.md:8-9, 01-overview.md:35-36).
6. Outcomes project to chat (outcome surface), Agents Live (observation), Teams (history/governance), and the Admin Runtime Console (who runs, provider owner, step, tokens, force-recycle) with per-event SSE IDs for safe reconnects (01-overview.md:36, 01-overview.md:50).

Persistent state lives in the database (Goals checklist/continuation/attempts/cooldowns/leases/user input; Team Run DAG/executions; audit trail) plus workspace files (`AGENTS.md`, `SOUL.md`, `PROFILE.md`, `MEMORY.md`, daily notes, skill roots, goal progress ledgers, artifacts) and container volumes (`server_data` for `MATECLAW_SKILL_WORKSPACE_ROOT`) (01-overview.md:33-34, 01-overview.md:38-40, 02-top-level-files.md:86).

## 3. The Digital Employee and Runtime Contract

Representation: an employee is an identity record (Role, Goal, Backstory, runtime selection, avatar, color) decoupled from the execution engine by the `AgentRuntimeProvider` contract, so governance and identity stay stable across engine changes (01-overview.md:30, 01-overview.md:31-32). Execution state is not held in the employee record but in durable companions: persistent Goals and Team Runs backed by the database (01-overview.md:33-36).

Named kinds/types with file:line:

- Runtime kinds: `Native StateGraph` (ReAct, Plan-and-Execute, persistent Goals, Team Runs) vs `DSH (dsh-jsonrpc-agent)` managed external loop (01-overview.md:31-32).
- Employee templates (6): General Assistant, Product Assistant, Research Analyst, Customer Support, Data Analyst, Code Reviewer (01-overview.md:29-30).
- Goal record fields: checklist, continuation state, attempts, cooldowns, leases, busy-worker user input, JSON acceptance fields, immutable artifact versions (01-overview.md:33-34, 01-overview.md:16).
- Team Run record: `runId`, objective, task DAG, worker executions, synthesis, deliverables (01-overview.md:35-36).
- Capability kinds: SKILL.md packages, MCP (stdio/SSE/Streamable HTTP), ACP (Claude Code/Codex), Tool Guard (01-overview.md:41-45).
- Memory kinds: LLM Wiki pages with `[[links]]`, `AGENTS.md` / `SOUL.md` / `PROFILE.md` / `MEMORY.md`, daily notes (01-overview.md:38-40).
- Workflow step modes (7): `sequential` / `fan_out` / `collect` / `conditional` / `await_approval` / `dispatch_channel` / `write_memory` (01-overview.md:47).
- Trigger patterns (6): `cron` / `webhook` / `channel_message` / `agent_lifecycle` / `content_match` / `workflow_completion` (01-overview.md:48).

Key queries: the wiki pages describe behavior, not query code. The closest verbatim operational query is the goal-resumption prompt pattern (01-overview.md:34):

```
"Create a persistent Goal first. Save the plan and progress in the workspace, write in small checkpoints, resume from existing evidence after errors or restart, and call `completeGoal` only after every criterion has verifiable evidence."
```

## 4. LLM / External Service Integration

Providers: DashScope, OpenAI, Anthropic, Gemini, DeepSeek, Kimi, Ollama, LM Studio, MLX, plus vLLM (reasoning fix in v2.3.0) and a per-template model picker for Wiki Transformations; sidecar routing lets a vision model describe images for a text-only main model (01-overview.md:18-19, 01-overview.md:16, 01-overview.md:49, 01-overview.md:51). Cloud search APIs (Serper/Tavily) back the WebSearch tool with SearXNG sidecar fallback (02-top-level-files.md:67).

Required vs optional calls: every reasoning turn requires exactly one healthy provider from the ordered chain; failover on expired keys, 401s, network blips, or drained quota tries the next healthy provider and errors only when the chain is exhausted (01-overview.md:18-19). Optional calls: text-to-speech, speech-to-text, image/music/video/3D generation, document rendering (`DocxRenderTool` / `XlsxRenderTool` / `PptxRenderTool` / `PdfRenderTool`), web search, browser sidecar (CDP/Playwright) (01-overview.md:51, 02-top-level-files.md:67, 02-top-level-files.md:73-80).

Env vars: provider keys are configured in Settings → Models (ordering + live health dashboard); the template names search keys explicitly and OAuth/deployment flags implicitly affect model auth: `SERPER_API_KEY`, `TAVILY_API_KEY` (either/or/empty → SearXNG fallback), `MATECLAW_OAUTH_OPENAI_DEPLOYMENT_MODE` (`local`/`device_code`/`manual_paste`, empty auto-selects), `MATECLAW_OAUTH_OPENAI_CALLBACK_BIND_HOST` (02-top-level-files.md:67, 02-top-level-files.md:81-82, 01-overview.md:18-19).

## 5. The Durable Team Run and Goal Pipeline

Step by step (function-level file.py:line references are unavailable — the wiki covers only README-level behavior plus top-level config files, with no per-function pages; steps below cite the behavior source):

1. Request intake and employee binding — chat/trigger input binds to one employee; DSH availability/capabilities are validated before startup, installable and testable from the console (01-overview.md:31-32).
2. Provider selection with failover — ordered chain from Settings → Models; health tracker parks failing vendors in cooldown (01-overview.md:18-19).
3. Context assembly — LLM Wiki hot cache auto-injected into the system prompt plus `AGENTS.md`/`SOUL.md`/`PROFILE.md`/`MEMORY.md`/daily notes (01-overview.md:38-40).
4. Goal creation (long work) — "Create a persistent Goal first"; plan and progress saved in workspace in small checkpoints; required JSON acceptance fields bound to current requirements (01-overview.md:33-34, 01-overview.md:16).
5. Team Run fan-out (multi-worker) — one request creates one durable Team Run with stable `runId`; shared board orchestrates dependencies, parallel dispatch, prerequisite hand-off, execution leases, cancel-interrupt, human approval gates (01-overview.md:35-36).
6. Tool execution under guard — SKILL.md / per-employee MCP / ACP tools run under Tool Guard RBAC + approval flow + path protection (01-overview.md:41-45).
7. Recovery — after a single-backend restart the supervisor reconciles the interrupted attempt from checkpoints/artifacts and schedules the next safe segment; file work inspects the tail of the progress ledger and appends small verifiable units (01-overview.md:33-34).
8. Completion and evidence — `completeGoal` called only after reproducible acceptance checks; v2.3.0 records JSON acceptance plus immutable artifact versions; Team Run synthesizes into summaries/files with drill-down to tasks, evidence, approvals, read-only worker records (01-overview.md:33-34, 01-overview.md:16, 01-overview.md:35-36).
9. Projection and audit — chat as outcome surface, Agents Live for observation, Teams for history/governance, Admin Runtime Console with force-recycle; full audit trail retained (01-overview.md:35-36, 01-overview.md:50, 01-overview.md:12).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README_zh.md` | 338 | Product entry point: positioning, runtime contract, failover, wiki, surfaces, quick-start, layout, stack (02-top-level-files.md:141-146) |
| `mateclaw-server/` | dir | Spring Boot 3.5 backend: `AgentRuntimeProvider` contract, Native StateGraph + DSH, workflows/triggers/wiki-processor (02-top-level-files.md:158-163) |
| `mateclaw-ui/` | dir | Vue 3 + TypeScript admin SPA; build output packed into backend JAR (02-top-level-files.md:158-163) |
| `mateclaw-desktop/` | dir | Electron desktop, local-embedded / remote-central modes, bundled JRE 21 (02-top-level-files.md:158-163) |
| `mateclaw-webchat/` | dir | Embeddable webchat component, UMD/ES bundle, one-`<script>` install (02-top-level-files.md:158-163) |
| `mateclaw-plugin-api/` | dir | Java SDK for third-party capability packs (02-top-level-files.md:158-163) |
| `mateclaw-plugin-sample/` | dir | Reference plugin implementation (02-top-level-files.md:158-163) |
| `mateclaw-plugin-mem0/` | dir | Optional Mem0 memory provider plugin (02-top-level-files.md:158-163) |
| `mateclaw-plugin-search-sample/` | dir | Search provider SPI example (02-top-level-files.md:158-163) |
| `docker-compose.yml` | — | Docker stack (PostgreSQL 16 default, SearXNG/browser sidecars); started after `cp .env.example .env` (02-top-level-files.md:158-163) |
| `.env.example` | 166 | Single deployment template; required values fail `compose up` via `${VAR:?}` instead of defaulting (02-top-level-files.md:46-51) |
| `.dockerignore` | 28 | Lean build context: excludes git/IDE/Node/Maven/desktop/data/logs/secrets, re-includes select markdown (02-top-level-files.md:13-15) |
| `.gitattributes` | 20 | LF for `*.sh`/`*.bash`/`*.sql` (container bind-mounts, Flyway checksums); CRLF for `*.bat`/`*.cmd`/`*.ps1` (02-top-level-files.md:92-94) |
| `.gitignore` | 136 | Excludes build outputs, IDE files, local data (`mateclaw-server/data/`, `.sessions/`, `/data/`), `.env`, npm/yarn locks (02-top-level-files.md:105-110) |
| `assets/images/preview.png` | — | Product preview image referenced by README (01-overview.md:54) |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| Java | `21+` | Backend toolchain; desktop bundles JRE 21 (02-top-level-files.md:143) |
| Spring Boot | `3.5` | Backend kernel (02-top-level-files.md:172) |
| Spring AI Alibaba | `1.1` | LLM integration layer (02-top-level-files.md:172) |
| MyBatis Plus | (name only in wiki) | Persistence mapper (02-top-level-files.md:172) |
| Flyway | (name only in wiki) | SQL migration checksums; LF pinning keeps them cross-platform (02-top-level-files.md:92-94, 02-top-level-files.md:172) |
| H2 / PostgreSQL `16` / MySQL `8.0+` / Kingbase | `16`, `8.0+` | Supported databases; PostgreSQL 16 is Docker default (02-top-level-files.md:172, 02-top-level-files.md:52) |
| Spring Security + JWT | (name only in wiki) | Auth; `JWT_SECRET` signs tokens (02-top-level-files.md:68, 02-top-level-files.md:172) |
| Vue `3` / Vite / Element Plus / TailwindCSS `4` | `3`, `4` | Admin SPA stack (02-top-level-files.md:172) |
| Electron | (name only in wiki) | Desktop shell, dual local/remote modes (02-top-level-files.md:172) |
| pnpm | (pnpm-only repo; npm/yarn lockfiles ignored) | Monorepo package manager (02-top-level-files.md:136-140) |
| SearXNG sidecar | (name only in wiki) | WebSearch fallback when Serper/Tavily keys empty (02-top-level-files.md:67) |
| Chromium / Playwright | (names only in wiki) | Browser sidecar via CDP or forced channel (02-top-level-files.md:73-80) |
| dsh-jsonrpc-agent (DeepSeek Harness) | (name only in wiki) | Managed DSH external runtime loop (02-top-level-files.md:145) |

Required first: Java 21+, Spring Boot 3.5, one database (PostgreSQL 16 in Docker), pnpm for UI. Everything else (search keys, browser sidecar, OAuth modes, wiki watcher, skill caps, pip/Maven mirrors) is optional tuning in `.env.example` (02-top-level-files.md:64-91).

## 8. CLI / Usage Surface

Entry points: Web Console (admin: employees, models, skills, knowledge, security, cron, runtime console with force-recycle); Electron desktop (no Java install); Webchat widget (one `<script>`); IM channels (DingTalk, Feishu, WeChat Work, WeChat, Telegram, Discord, QQ, Slack); Plugin SDK (01-overview.md:21-28).

Commands:

| Command | Effect |
|---|---|
| `cp .env.example .env` | Create deployment env from template (02-top-level-files.md:46-50) |
| `docker compose up -d` | Start stack at `http://localhost:18080` (02-top-level-files.md:157) |
| `cd mateclaw-server && mvn spring-boot:run` | Backend dev at `http://localhost:18088` (02-top-level-files.md:147-156) |
| `cd mateclaw-ui && npm install && npm run dev` | Frontend dev at `http://localhost:5173` (02-top-level-files.md:147-156) |

Default login: `admin` / `admin123` (02-top-level-files.md:157).

Env-var and config tables:

| Variable | Required? | Purpose / default |
|---|---|---|
| `DB_HOST` / `DB_PORT=5432` / `DB_NAME` / `DB_USERNAME` / `DB_PASSWORD` / `DB_ADMIN_USERNAME` / `DB_ADMIN_PASSWORD` | Required in Docker | PostgreSQL 16 connection; least-privilege app role; change both passwords (02-top-level-files.md:52-63) |
| `SERPER_API_KEY` / `TAVILY_API_KEY` | Optional | Cloud search; empty → SearXNG sidecar (02-top-level-files.md:67) |
| `JWT_SECRET` | Optional (WARN if empty) | JWT signing; generate via `openssl rand -base64 48` in prod (02-top-level-files.md:68) |
| `MATECLAW_CORS_ALLOWED_ORIGINS` | Optional | CORS allowlist; empty allows all with WARN (02-top-level-files.md:69) |
| `MATECLAW_PUBLIC_BASE_URL` | Optional | Absolute base for agent file links; else request host / relative (02-top-level-files.md:70) |
| `MATECLAW_OPENAPI_EXPOSE_UI` | Optional, default false | Exposes Swagger UI + api-docs, admin-only (02-top-level-files.md:71) |
| `SEARXNG_SECRET` | Optional | Internal SearXNG key; 32+ random chars in prod (02-top-level-files.md:72) |
| `MATECLAW_BROWSER_CDP_URL` / `MATECLAW_BROWSER_CHROME_PATH` / `MATECLAW_BROWSER_CHANNEL` | Optional | Browser sidecar endpoint / binary / forced channel (02-top-level-files.md:73-75) |
| `PLAYWRIGHT_ALLOW_PRIVATE_NETWORK` (default `false`) / `PLAYWRIGHT_IGNORE_HTTPS_ERRORS` | Optional | SSRF guard and cert-error tolerance; keep `false` publicly (02-top-level-files.md:76-77) |
| `PLAYWRIGHT_DEFAULT_TIMEOUT_SECONDS=30` / `PLAYWRIGHT_NAVIGATION_TIMEOUT_SECONDS=30` / `PLAYWRIGHT_SNAPSHOT_MAX_LENGTH=20000` | Optional | Timeouts and snapshot truncation (`truncated:true` hint) (02-top-level-files.md:78-80) |
| `MATECLAW_OAUTH_OPENAI_DEPLOYMENT_MODE` / `MATECLAW_OAUTH_OPENAI_CALLBACK_BIND_HOST` | Optional | `local`/`device_code`/`manual_paste` selector; `0.0.0.0` + `1455:1455` for in-Docker PKCE (02-top-level-files.md:81-82) |
| `MATE_WIKI_ALLOWED_SOURCE_ROOTS` (empty = forbid all) / `MATE_WIKI_WATCHER_ENABLED=false` / `MATE_WIKI_WATCHER_INTERVAL_MS=300000` | Optional | Wiki scan allowlist (fail-closed), auto-sync master switch, 5-min interval (02-top-level-files.md:83-85) |
| `MATECLAW_SKILL_WORKSPACE_ROOT` (`/app/data/skills` in container) / `MATECLAW_SKILL_UPLOAD_MAX_ENTRY_SIZE_MB` (1MB) / `MATECLAW_SKILL_UPLOAD_MAX_TOTAL_SIZE_MB` (50MB) | Optional | Skill storage + ZIP upload caps; note Spring multipart caps 100/200MB (02-top-level-files.md:86-88) |
| `PIP_INDEX_URL` / `PIP_TRUSTED_HOST` / `MATECLAW_PIP_INDEX_URL` / `MATECLAW_PIP_TRUSTED_HOST` | Optional | Pip mirrors for skill Python deps (02-top-level-files.md:89-90) |
| `MAVEN_FLAGS` (`-Paliyun-first`, commented out) | Optional | Mainland-China repo preference (02-top-level-files.md:91) |

Console configuration (non-env): provider order in Settings → Models; DSH install/verify/test/enable/disable; runtime force-recycle at Settings → System → Runtime (01-overview.md:18-19, 01-overview.md:31-32, 01-overview.md:50).

## 9. Extensibility Points

- New agent capability pack → implement against `mateclaw-plugin-api` (Java module) using `mateclaw-plugin-sample/` as reference (02-top-level-files.md:158-163).
- New memory provider → extend the Mem0 pattern in `mateclaw-plugin-mem0/` (optional provider plugin) (02-top-level-files.md:158-163).
- New search backend → implement the search-provider SPI per `mateclaw-plugin-search-sample/` (02-top-level-files.md:158-163).
- New employee behavior without code → author a SKILL.md package (manifest + prompt + tool list + `LESSONS.md`), or run the five-step wizard with pre-flight checks; eight starter templates ship; promotion / constrained auto-binding / curator handover / snapshots / restore points govern evolution (01-overview.md:42).
- New tool wiring without code → register MCP servers (stdio/SSE/Streamable HTTP) with per-employee binding to avoid toolbox bleed; or bridge Claude Code/Codex via ACP auto skill cards (01-overview.md:43-44).
- New business process without code → author a Workflow (linear DSL over employees + approval/channel-dispatch/write-memory actions, JSON-first with Monaco + schema or NL draft) and fire it from six trigger patterns (`cron`, `webhook`, `channel_message`, `agent_lifecycle`, `content_match`, `workflow_completion`) (01-overview.md:47-48).
- New knowledge pipeline without code → author Wiki Transformation templates (map-reduce over materials/pages, reverse-citation extraction, JSON mode, per-template model picker) (01-overview.md:49).

## 10. Limitations and Gotchas

- **Exactly-once is not promised for external side effects.** Payments, sends, publishes, and destructive calls need idempotency keys or human review; recovery replays from checkpoints and can repeat an outward call (01-overview.md:34).
- **Recovery covers a single backend restart, not arbitrary multi-node failover.** The supervisor reconciles the interrupted attempt from checkpoints/artifacts; file work must keep a progress ledger, append small verifiable units, and inspect the tail after recovery (01-overview.md:33-34).
- **Empty `.env` values fail closed or warn — there are no safe silent defaults.** Required-but-unset values abort `docker compose up` via `${VAR:?}`; empty `JWT_SECRET` or CORS allowlist boots with WARN (open CORS, default signing key); empty `MATE_WIKI_ALLOWED_SOURCE_ROOTS` forbids all directory scans (02-top-level-files.md:46-51, 02-top-level-files.md:68-69, 02-top-level-files.md:83).
- **Skill uploads are tightly capped.** Per-file 1MB and whole-package 50MB defaults plus Spring multipart caps (100/200MB) bound installer memory; large skill packages need cap raises (02-top-level-files.md:86-88).
- **Browser automation is fenced by default.** `PLAYWRIGHT_ALLOW_PRIVATE_NETWORK=false` blocks loopback/private IPs and snapshot text truncates at 20000 chars with a `truncated:true` hint — intranet targets and wide scrapes need explicit tuning (02-top-level-files.md:76-80).
- **Wiki coverage in this analysis is truncated.** The multimodal paragraph cuts off mid-word at 01-overview.md:141 and `README_zh.md` loses ~3809 trailing characters (post-2.1.0 roadmap); claims beyond those cut points are unavailable (01-overview.md:51-54, 02-top-level-files.md:142-173).

## 11. How It Compares to Alternatives

- **Dify / FastGPT:** app-centric low-code agent builders with hosted flows; MateClaw instead ships a self-hosted employee runtime with native/DSH engine choice, persistent Goals, and Team Runs in one JAR rather than a flow canvas.
- **LangChain / LangGraph:** developer frameworks for ReAct/StateGraph wiring; MateClaw embeds a StateGraph runtime plus console, memory, skills, channels, and ops (health tracker, runtime console, audit) as a deployable product rather than a library.
- **OpenHands / AutoGPT-style coding agents:** single-task autonomous loops; MateClaw wraps that loop class (via ACP-bridged Claude Code/Codex plus file-producing Goals with ledgers and JSON acceptance) inside multi-user governance, approval gates, and durable multi-worker orchestration.
- **MaxKB / AnythingLLM:** knowledge-QA-first self-hosted chat over docs; MateClaw's LLM Wiki plus hot-cache injection and Transformations cover that ground but add employees, workflows/triggers, and IM/webchat/desktop doors as the primary surface.

Positioning sentence: MateClaw competes as the self-hosted, IT-sign-off-ready "whole-widget" deployment — engine, knowledge, memory, tools, channels, and durable team execution together with failover and audit — where the alternatives each cover one slice (app builder, framework, solo loop, or doc QA).

## Appendix: Selected Code Snippets

1. Docker build-context policy, `.dockerignore:1-28` (02-top-level-files.md:13-15):

```dockerignore
# Git and IDE
.git
.idea
*.iml

# Node artifacts
**/node_modules
**/dist
**/.nuxt
**/.output

# Maven build output (will be rebuilt in Docker)
**/target

# Desktop / webchat (not needed for server or sites build)
mateclaw-desktop

# Data and logs
data
*.log

# Misc
.env
*.md
!docs/**/*.md
!matevip-sites/**/*.md
!mateclaw-plugin-api/**
!mateclaw-server/**
```

2. Backend/frontend dev quick-start, `README_zh.md:163-180` (02-top-level-files.md:147-156):

```bash
# 后端
cd mateclaw-server
mvn spring-boot:run           # http://localhost:18088

# 前端
cd mateclaw-ui
npm install && npm run dev    # http://localhost:5173
```

3. Repository layout, `README_zh.md:203-217` (02-top-level-files.md:158-163):

```
mateclaw/
├── mateclaw-server/        Spring Boot 3.5 后端（Agent Runtime contract · Native StateGraph + DSH）
├── mateclaw-ui/            Vue 3 + TypeScript 管理 SPA（构建产物打进后端 JAR）
├── mateclaw-desktop/       Electron 桌面端（本地内嵌 / 远程集中双模式）
├── mateclaw-webchat/       网页嵌入式聊天组件（UMD / ES bundle）
├── mateclaw-plugin-api/    第三方能力插件的 Java SDK
├── mateclaw-plugin-sample/ 参考插件实现
├── mateclaw-plugin-mem0/   可选 Mem0 记忆 Provider 插件
├── mateclaw-plugin-search-sample/ 搜索 Provider SPI 示例
├── docker-compose.yml
└── .env.example
```

4. Goal-resumption prompt pattern, `01-overview.md:104` (01-overview.md:33-34):

```
"Create a persistent Goal first. Save the plan and progress in the workspace, write in small checkpoints, resume from existing evidence after errors or restart, and call `completeGoal` only after every criterion has verifiable evidence."
```
