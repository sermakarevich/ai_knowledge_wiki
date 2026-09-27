# Agent Swarm -- Multi-Agent Self-Learning Teams (OSS)

**Article:** [Show HN: Agent Swarm – Multi-agent self-learning teams](https://news.ycombinator.com/item?id=47165046)
**Repository:** [desplega-ai/agent-swarm](https://github.com/desplega-ai/agent-swarm)
**Version:** 1.92.1  |  **Date:** 2026-06-09

---

## Human Readable TL;DR

Imagine a team of employees that not only do their jobs but also remember every mistake they made before and avoid repeating it next time. Agent Swarm is a software framework that creates virtual teams of AI workers: one manager AI delegates tasks to many specialist AIs running in isolated containers, and they all share a growing memory bank. The more tasks they complete, the smarter the whole team gets -- 95% of recent code changes in the project itself were written by the swarm. It plugs into Slack, GitHub, and Jira so it slots into existing workflows with minimal setup.

## TL;DR

Agent Swarm is an open-source TypeScript/Bun framework for orchestrating fleets of AI coding agent CLIs (Claude Code, OpenAI Codex, Devin, opencode) with compounding, persistent memory. A lead agent distributes tasks to Docker-isolated worker agents that share a vector-searchable knowledge base populated after each session. Unlike ephemeral single-session setups, it accumulates cross-session learnings through CLAUDE.md identity files, a shared SQLite+sqlite-vec store, and an LLM memory rater -- enabling the team to improve iteratively without human re-prompting.

---

## Problem & Motivation

Most agentic AI frameworks are ephemeral: every task starts from scratch with no memory of prior work, forcing engineers to repeatedly re-prompt for edge cases already encountered. Coordinating multiple agents at scale adds further friction -- credential rotation, cost tracking, task queuing, human approval gates, and integration with Slack/GitHub/Jira all need custom glue. Agent Swarm addresses both problems: it provides a coordination layer (API server + MCP endpoint) sitting between humans and AI coding agents, and a compounding memory system so each future task execution benefits from all prior work.

---

## Main Original Ideas

1. **Compounding Intelligence Layer** -- After each task, agents extract structured learnings into a shared vector store. All future workers retrieve semantically relevant memories at task start, creating a self-improving feedback loop without retraining or fine-tuning the underlying model.

2. **Persistent Agent Identity via CLAUDE.md Files** -- Each agent maintains a CLAUDE.md encoding its evolving persona, domain expertise notes, and recent session history. Workers behave consistently across restarts and accumulate specialized skills over time, surviving Docker container recycling.

3. **Hierarchical Lead/Worker Architecture with Docker Isolation** -- A single lead agent (which can be Claude Code itself acting as an MCP client) decomposes requests and dispatches workers into isolated Docker environments with full dev toolchains. Workers run in parallel, enabling concurrent execution of independent sub-tasks.

4. **DAG-based Workflow Engine with Human-in-the-Loop Gates** -- Complex multi-step tasks are modeled as directed acyclic graphs. Irreversible operations (deploys, external sends) require explicit human approval via Slack or API before proceeding, balancing automation with safety.

5. **Drain Loops Pattern** -- A single high-level ticket spawns a chain of individually reviewable sub-PRs, decomposing large tasks into auditable, human-approachable increments rather than one opaque diff.

---

## Key Findings

| Metric | Value |
|---|---|
| GitHub stars | 512 |
| Releases | 91 (latest v1.92.1) |
| Commits to main | 1,568 |
| Self-generated PRs | ~95% of recent contributions |
| Primary language | TypeScript (92.2%) |
| Backend | Bun + SQLite (WAL) + sqlite-vec |

- **Self-loop validation**: The project uses itself (the swarm) to build and maintain itself, providing a live dogfood signal.
- **Context cost tradeoff** (from HN discussion): A researcher cited findings that context/identity files add 20%+ token costs with marginal performance gains -- a real operational concern for high-volume deployments.
- **Eight production playbooks** are documented: feature development, lead prospecting, content generation, UX command center, proactive support, code health monitoring, data reporting, and release documentation.
- **HN skeptic concerns**: Critics noted this shifts engineering from stable version-controlled source code toward ephemeral prompt-based logic -- making correctness harder to audit and debug. The creator countered that daily review + HITL gates preserve oversight.
- **Five canonical patterns**: Litmus Tests (LLM-as-judge quality gates), Drain Loops, HITL Gates, Per-Customer Directories (context accumulation per account), and No-op Workflows (silent skip when no changes needed).

---

## Suggestions & Future Directions

1. **Context cost optimization** -- Selective context loading (only relevant learnings per task type) could reduce the cited 20% token overhead without sacrificing compounding gains.

2. **Distributed persistence** -- Current SQLite + sqlite-vec is adequate for single-host deployments but needs a distributed-persistent backend for multi-machine fleets where the DB file can't live on a shared filesystem.

3. **Auditability tooling** -- A structured diff/audit log of swarm-generated changes vs. human changes would address governance concerns for regulated industries and directly answer the HN "ephemeral prompting" critique.

4. **Independent benchmarks** -- No published evals comparing task quality or throughput vs. single-agent or human baselines. A rigorous benchmark would substantially accelerate enterprise adoption.

5. **Provenance tracking for memory entries** -- Memory entries should carry provenance (task ID, agent, date) so stale or incorrect learnings can be identified and pruned without resetting the entire knowledge base.

---

## Authors & Institutions

Desplega Labs (desplega-ai) -- contact@desplega.sh. Open-source; individual contributors not listed publicly. Notable: ~95% of recent commits are attributed to the swarm itself.

---

> *Note: A detailed technical codebase analysis (architecture, data flow, key files, dependencies, CLI surface, extensibility, and limitations) was previously captured for this project. The sections below preserve that analysis.*

---

---

## 1. Overview / What Problem It Solves

Running a single AI coding agent is straightforward; running a fleet of them reliably — with task queuing, credential rotation, cost tracking, graceful shutdown, resumable sessions, and human-in-the-loop approval gates — is not. `agent-swarm` addresses this by providing a coordination layer that sits between humans and AI coding agents. It exposes a single API server and MCP endpoint to which multiple worker containers connect. Humans (or lead agents) submit tasks via Slack, GitHub events, the REST API, or directly through an MCP tool call; workers claim those tasks, execute them inside a subprocess harness, and report progress and cost back to the server.

The primary users are platform/DevOps teams who want to run autonomous AI coding agents at scale under a shared infrastructure — credential pooling, per-agent and per-user daily spend budgets, durable workflows, memory retrieval, and observability (OpenTelemetry → SigNoz/Honeycomb/Tempo). Secondary users are individual developers who want a self-hosted "AI task queue" that accepts work from Slack or GitHub and executes it headlessly.

The project is a Bun/TypeScript monorepo. The server component is an MCP HTTP server plus a conventional REST API backed by SQLite in WAL mode. Workers are Docker containers running an AI coding agent CLI (Claude Code, OpenAI Codex, Pi, opencode, or Devin) under a long-polling loop. A Next.js dashboard (`ui/`) and a Fumadocs docs site (`docs-site/`) are bundled in the same repo but deployed separately.

---

## 2. High-Level Architecture

```
  Humans / Lead agents / Integrations
        │
        │  Slack / GitHub / Linear / Jira / AgentMail / Kapso
        │  REST API / MCP tools
        ▼
  ┌─────────────────────────────────────────┐
  │         API + MCP HTTP Server           │
  │  src/http/index.ts   (port 3013)        │
  │  src/server.ts       (MCP tool registry)│
  │                                         │
  │  Route handlers: tasks, poll, agents,   │
  │  memory, workflows, schedules, pages,   │
  │  scripts, kv, skills, session-data, … │
  └──────────────────┬──────────────────────┘
                     │  bun:sqlite (WAL)
                     ▼
              agent-swarm-db.sqlite
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
  Worker Container           Lead Container
  src/commands/runner.ts    src/commands/runner.ts
  (AGENT_ROLE=worker)       (AGENT_ROLE=lead)
        │                         │
        │  HTTP polling            │
        │  GET /api/poll           │
        │  POST /api/session-data  │
        ▼                         ▼
  Harness subprocess         Harness subprocess
  claude / codex / pi        claude / codex / …
  opencode / devin
```

**Data flow — task from Slack mention to completion:**

1. User mentions `@dev-swarm` in a Slack channel; the Bolt WebSocket handler in `src/slack/` parses the message, calls `createTaskWithSiblingAwareness()`, and inserts a row into `agent_tasks` with `status='pending'` and `source='slack'`.
2. A lead or worker container is polling `GET /api/poll` every ~10 s. `handlePoll()` (`src/http/poll.ts`) queries the DB for the next claimable task, evaluates budget admission (`src/be/budget-admission.ts`), and atomically transitions the row to `in_progress` inside a `db.transaction`.
3. `runWorker()` (`src/commands/runner.ts`) receives the task payload, composes a system prompt via the template registry (`src/prompts/`), optionally injects retrieved memories, then calls `createProviderAdapter()` to instantiate the appropriate harness adapter.
4. The adapter (`src/providers/claude-adapter.ts`, `codex-adapter.ts`, etc.) spawns the AI CLI as a child process via `Bun.spawn`, streams structured JSON events from stdout, and emits typed `ProviderEvent` objects back to the runner.
5. The runner throttles progress updates (every 3 s) and calls the `store-progress` MCP tool — or `POST /api/tasks/:id` — to update `progress`, `costData`, and context usage in the DB.
6. When the subprocess exits, the runner posts the final `completed` or `failed` status to the API and the business-use event graph records the terminal event.

**Persistent state:** one SQLite file at `DATABASE_PATH` (default: `./agent-swarm-db.sqlite`). WAL mode enabled at `initDb()` call in `src/be/db.ts`. Workers hold no local state; the file lives on the host running the API container. Memory embeddings use `sqlite-vec` for KNN queries inside the same DB file.

---

## 3. The Task

The central domain object is the `agent_tasks` row. Its `status` column drives every state transition in the system.

**Status lifecycle** (`src/types.ts:AgentTaskStatusSchema`):
```
backlog → unassigned → offered → reviewing → pending → in_progress
                                                           │
                                              ┌────────────┼──────────────┐
                                              ▼            ▼              ▼
                                          completed      failed      cancelled
                                              │
                                         superseded   (resume branch)
                                              │
                                           paused → resumed
```

Terminal statuses (from `src/types.ts:TERMINAL_TASK_STATUSES`): `completed`, `failed`, `cancelled`, `superseded`.

**Inbound sources** (SQL `CHECK` constraint in `src/be/migrations/001_initial.sql:78`):
`mcp`, `slack`, `api`, `github`, `agentmail`, `system`, `schedule`.

**Key `agent_tasks` columns** (`src/be/migrations/001_initial.sql:73-107`):
- `id TEXT PRIMARY KEY` — UUID
- `agentId` — FK to `agents.id`, the currently assigned worker
- `task TEXT NOT NULL` — the prompt/description
- `status TEXT` — lifecycle enum above
- `source TEXT` — where the task came from
- `parentTaskId` — for subtask hierarchies
- `epicId` — FK to `epics.id`
- `claudeSessionId` — harness resume token (Claude only)
- `slackChannelId`, `slackThreadTs` — Slack context for reply routing
- `githubRepo`, `githubNumber`, `githubUrl` — GitHub context
- `requestedByUserId` — FK to `users.id` (canonical user identity)
- `costData TEXT` — JSON blob with token/USD attribution

**Claim query** (from `handlePoll()` in `src/http/poll.ts`): an `UPDATE … RETURNING` or `SELECT … FOR UPDATE` pattern that transitions `pending` → `in_progress` atomically inside a `db.transaction`, guarded by budget admission checks.

**Configurable behavior:**
- `MAX_CONCURRENT_TASKS` — per-agent task slot count (default 1 for workers, 2 for leads)
- `SHUTDOWN_TIMEOUT` — ms to wait for task finish on SIGTERM (default 30 s)
- `BUDGET_ADMISSION_DISABLED=true` — bypass all daily spend gates

---

## 4. LLM / External Service Integration

`agent-swarm` does **not** call LLMs directly for task execution. Instead, it spawns external AI coding agent CLIs as child processes and parses their structured output. The server itself is an MCP server — the LLM running inside the harness subprocess is the MCP client.

**Harness providers** (`src/providers/` directory, dispatched from `createProviderAdapter()` in `src/providers/index.ts`):

| Provider | How invoked | Required credentials |
|---|---|---|
| `claude` | `claude` CLI via `Bun.spawn`, `--output-format stream-json -p` | `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY` |
| `codex` | `@openai/codex-sdk` subprocess session runner | Codex OAuth credentials pool |
| `pi` | `@earendil-works/pi-coding-agent` | `PI_API_KEY` or AWS Bedrock creds |
| `opencode` | `@opencode-ai/sdk` | `ANTHROPIC_API_KEY` or OpenRouter key |
| `devin` | Devin REST API (HTTP polling) | `DEVIN_API_KEY`, `DEVIN_ORG_ID` |
| `claude-managed` | Anthropic cloud sandbox via `claude-managed-setup` | `ANTHROPIC_API_KEY`, `MANAGED_AGENT_ID`, `MANAGED_ENVIRONMENT_ID` |

Selected by `HARNESS_PROVIDER` env var. Multiple providers can coexist in a fleet by deploying workers with different env files.

**Internal AI use** (API server only, not execution):
- `OPENAI_API_KEY` — used for memory embedding (`text-embedding-3-small` via `@ai-sdk/openai`) to produce 512-dim vectors stored in `sqlite-vec`. Optional; without it, memory search falls back to recency ordering.
- `OPENROUTER_API_KEY` — used by the memory rater (`MEMORY_RATER_LLM_MODEL`, default `google/gemini-3-flash-preview`) to score session summaries for long-term memory selection. Optional; without it, the rater is a no-op.

**External integrations** (event-driven, all optional via `*_DISABLE=true` env flags):
- Slack (Socket Mode via `@slack/bolt`)
- GitHub App (webhook + REST via `GITHUB_APP_PRIVATE_KEY`)
- Linear (OAuth 3LO)
- Jira (OAuth 3LO)
- AgentMail (Svix webhook)
- Kapso/WhatsApp (HMAC-verified inbound webhook + REST outbound)

---

## 5. The Worker Execution Pipeline

The worker's task loop lives in `src/commands/runner.ts` (the largest file, ~4,800 lines). It covers: credential validation, repo clone/refresh, prompt composition, harness dispatch, event streaming, progress reporting, cost tracking, and session resume.

**Step 1 — Agent registers and enters poll loop** (`src/commands/worker.ts:runWorker()`):
The worker boots, calls `POST /api/agents` to register with the server (name, role, capabilities), then enters `runWorkLoop()`.

**Step 2 — Poll for a task** (`GET /api/poll`):
Sends `X-Agent-ID` header. Server's `handlePoll()` atomically claims a task from the pool and returns its full payload, or `204 No Content` if the queue is empty. On empty, the worker increments `emptyPollCount` and backs off.

**Step 3 — Budget check** (`src/be/budget-admission.ts:canClaim()`):
Evaluated server-side before the task is returned. Checks global daily spend, per-agent daily spend, and per-user daily spend against limits stored in the `budgets` table.

**Step 4 — Repo setup** (inside `runner.ts`):
If the task has a `vcsRepo`, the runner fetches repo config from `/api/repos`, then either clones fresh (`git clone`) or refreshes the existing clone. Dirty repos are auto-stashed with a `swarm-autostash` stash message before the reset.

**Step 5 — Prompt composition** (`src/prompts/`):
`getBasePrompt()` resolves templates: `base`, `identity`, `tools`, `soul`, `memories`, `follow-up-context`, `repo-guidelines`. All text flows through `resolveTemplateAsync()` from the prompt-template registry; no string concatenation in the runner itself.

**Step 6 — Memory retrieval** (`GET /api/memory/search`):
The server fetches KNN memories relevant to the task description (cosine similarity via `sqlite-vec`), rated by importance. Retrieved memories are injected into the prompt via `renderMemoriesPrompt()`.

**Step 7 — Harness dispatch** (`createProviderAdapter()` → `adapter.runSession()`):
The adapter spawns the AI CLI subprocess, configures MCP server URL in the subprocess's `.mcp.json`, and begins streaming `ProviderEvent` objects. Events carry partial output, cost data (`CostData`), context window usage, tool calls, and error signals.

**Step 8 — Progress reporting** (throttled to 3 s):
The runner calls `POST /api/session-data` to persist `costData` + `contextUsage`. Cost is recomputed server-side against the `pricing` table using `costSource` tagging (`'harness'` | `'pricing-table'` | `'unpriced'`).

**Step 9 — Task completion** (`POST /api/tasks/:id/progress` or MCP `store-progress`):
Final status + output are written. The server transitions `in_progress` → `completed` (or `failed`). Business-use events are emitted. Slack/GitHub threads are updated with result blocks.

---

## 6. Key Files

| File | Lines (approx) | What It Does |
|---|---|---|
| `src/commands/runner.ts` | ~4,800 | Worker task execution loop: credential wait, repo clone/refresh, prompt composition, harness dispatch, progress reporting, resume |
| `src/server.ts` | ~380 | MCP server factory: registers 100+ tools, capability-gating via `CAPABILITIES` env |
| `src/http/index.ts` | ~460 | HTTP server bootstrap: route dispatch, startup subsystem init, graceful shutdown |
| `src/providers/claude-adapter.ts` | ~1,000 | Claude Code harness: subprocess spawn, stream-JSON parsing, cost/context tracking, `CLAUDE_BINARY` / bridge support |
| `src/be/db.ts` | ~3,500 (est.) | All SQLite prepared statements: tasks, agents, memory, sessions, pricing, workflows, kv, pages |
| `src/types.ts` | ~600 | Core type definitions: `AgentTaskStatus`, source enums, `ProviderName`, `RepoGuidelines`, workflow schema |
| `src/cli.tsx` | ~650 | CLI entry point: arg parsing, `worker`/`lead`/`api`/`onboard`/`connect`/`claude` commands, Ink TUI |
| `src/be/migrations/001_initial.sql` | ~280 | Collapsed baseline: 18 core tables with indexes |
| `src/be/migrations/` | ~80 files | Forward-only SQL migrations numbered `001`–`080+` |
| `src/prompts/base-prompt.ts` | ~200 | Base prompt assembly: composes identity/soul/tools/memories/context-preamble sections |
| `src/tools/send-task.ts` | ~200 | MCP `send-task` tool: creates tasks, validates schema, handles parent-context inheritance |
| `src/tools/store-progress.ts` | ~350 | MCP `store-progress`: updates progress/completion/failure/attachments, business-use events |
| `src/http/poll.ts` | ~250 | `GET /api/poll`: atomic task claim, budget gate, credential-pool selection |
| `src/http/tasks.ts` | ~600 | REST task CRUD, business-use lifecycle events |
| `src/workflows/` | ~2,500 (est.) | DAG workflow engine: node types, executor, trigger subscriptions, step journaling |
| `src/be/memory/` | ~800 (est.) | Memory write/search (sqlite-vec KNN), embedding, rater integration, GC |
| `src/scripts-runtime/` | ~600 (est.) | Sandboxed TS script executor: `ulimit`, stdin-config, `Redacted<string>`, SDK surface |
| `src/slack/` | ~1,200 (est.) | Slack Bolt app: mention handling, task creation, tree-message updates, thread routing |
| `src/github/` | ~800 (est.) | GitHub App webhooks: PR/issue/comment → task creation, review routing |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `@modelcontextprotocol/sdk` | `^1.25.1` | MCP server and transport (SSE + stdio) |
| `bun:sqlite` | (Bun built-in) | SQLite database — WAL mode, direct prepared statements |
| `sqlite-vec` | `^0.1.9` | Vector similarity search for memory KNN |
| `@anthropic-ai/sdk` | `^0.93.0` | Used by `claude-managed` provider adapter |
| `@ai-sdk/openai` | `^3.0.41` | Memory embedding via OpenAI `text-embedding-3-small` |
| `ai` | `^6.0.116` | Vercel AI SDK (stream parsing utilities) |
| `openai` | `^6.22.0` | Codex OAuth flow + OpenAI API |
| `@openai/codex-sdk` | `^0.137.0` | Codex subprocess session runner |
| `@earendil-works/pi-coding-agent` | `^0.78.1` | Pi coding agent harness |
| `@earendil-works/pi-ai` | `^0.78.1` | Pi AI core (Bedrock support) |
| `@earendil-works/pi-agent-core` | `^0.78.1` | Pi agent shared primitives |
| `@opencode-ai/sdk` | `^1.16.2` | opencode harness adapter |
| `@slack/bolt` | `^4.6.0` | Slack integration (Socket Mode) |
| `@linear/sdk` | `^77.0.0` | Linear OAuth + issue tracker sync |
| `hono` | `^4.12.3` | Used in sub-routes and middleware helpers |
| `ink` | `^6.5.1` | CLI TUI (React renderer for terminals) |
| `@inkjs/ui` | `^2.0.0` | Ink component library (Spinner, etc.) |
| `react` | `^19.2.3` | Required by Ink |
| `zod` | `^4.2.1` | Schema validation throughout |
| `zod-to-json-schema` | `^3.25.1` | Converts Zod schemas to JSON Schema for scripts argsSchema |
| `@asteasolutions/zod-to-openapi` | `^8.0.0` | OpenAPI spec generation from Zod route definitions |
| `cron-parser` | `^5.4.0` | Cron expression parsing for scheduler |
| `date-fns` | `^4.1.0` | Date formatting in runner resource usage logging |
| `e2b` | `2.26.0` | E2B sandbox lifecycle CLI (pinned exact) |
| `oauth4webapi` | `^3.8.5` | OAuth 2.0 PKCE / 3LO flows (Jira, Linear, Codex) |
| `svix` | `^1.62.0` | Svix webhook signature verification (AgentMail) |
| `@desplega.ai/business-use` | `^0.4.2` | Event flow instrumentation SDK |
| `@desplega.ai/localtunnel` | `^2.2.0` | Local tunnel for artifact service public URLs |
| `@opentelemetry/sdk-node` | `^0.218.0` | OTel trace export (OTLP) |
| `viem` | `^2.46.3` | EVM utilities for x402 payments extension |
| `@x402/core` | `^2.5.0` | x402 payments protocol (alpha, opt-in) |
| `@biomejs/biome` | `^2.3.10` | Linter + formatter (dev) |
| `@types/bun` | `latest` | Bun type declarations (dev) |

---

## 8. CLI / Usage Surface

**Entry points:**

```
bin: agent-swarm → src/cli.tsx   (package.json:bin)
```

**Commands:**

```bash
# Start the API + MCP HTTP server
agent-swarm api [--port 3013] [--key <key>] [--db <path>]

# Run a worker agent (polls for tasks, executes them)
agent-swarm worker [--yolo] [--system-prompt <text>] [-- <claude-args...>]

# Run a lead agent (worker with lead role, can delegate subtasks)
agent-swarm lead [--yolo]

# One-shot interactive wizard to bootstrap a swarm with Docker Compose
agent-swarm onboard [--dry-run] [-y] [--preset dev|content|research|solo]

# Connect a project to an existing swarm (writes .mcp.json + settings.local.json)
agent-swarm connect [--dry-run] [--restore] [-y]

# Run Claude CLI directly
agent-swarm claude [-m <message>] [--headless] [-- <claude-args...>]

# Setup and inspect tokens / auth
agent-swarm setup-token
agent-swarm token-info

# E2B sandbox operations
agent-swarm e2b start-stack|list|info|kill|logs|build|add|extend ...
```

**Environment variables:**

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `3013` | API server listen port |
| `API_KEY` / `AGENT_SWARM_API_KEY` | (empty = no auth) | Bearer token for API + worker auth; read via `getApiKey()` only |
| `HARNESS_PROVIDER` | `claude` | Which AI coding agent to run: `claude`, `pi`, `codex`, `devin`, `opencode`, `claude-managed` |
| `AGENT_ID` | (generated) | Stable worker identity across restarts |
| `AGENT_NAME` | (generated) | Display name in the dashboard |
| `AGENT_ROLE` | `worker` | `worker` or `lead` |
| `MCP_BASE_URL` | `http://localhost:3013` | API URL workers use to reach the server |
| `SWARM_URL` | `localhost` | Base domain for service discovery (`{AGENT_ID}.{SWARM_URL}`) |
| `DATABASE_PATH` | `./agent-swarm-db.sqlite` | SQLite file path (must colocate `.sqlite-wal`/`.sqlite-shm`) |
| `CAPABILITIES` | `core,task-pool,profiles,services,scheduling,memory,workflows,pages,metrics,kv` | Comma-separated capability feature flags |
| `YOLO` | `false` | Worker continues after subprocess failure instead of stopping |
| `MAX_CONCURRENT_TASKS` | `1` (worker) / `2` (lead) | Parallel task slots per agent |
| `SHUTDOWN_TIMEOUT` | `30000` | Graceful shutdown wait in ms |
| `CLAUDE_CODE_OAUTH_TOKEN` | — | OAuth token for Claude harness |
| `ANTHROPIC_API_KEY` | — | API key for Claude (fallback) or `claude-managed` |
| `OPENAI_API_KEY` | — | Enables memory vector embeddings |
| `OPENROUTER_API_KEY` | — | Enables LLM memory rater |
| `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` | — | Slack Socket Mode credentials |
| `GITHUB_APP_ID`, `GITHUB_APP_PRIVATE_KEY`, `GITHUB_WEBHOOK_SECRET` | — | GitHub App integration |
| `SECRETS_ENCRYPTION_KEY` | (auto-generated on first boot) | At-rest AES-256 encryption for `swarm_config` secrets |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | (disabled) | OpenTelemetry OTLP endpoint; omit to disable tracing |
| `BUDGET_ADMISSION_DISABLED` | `false` | Bypass all daily spend budget gates |
| `CONTEXT_MODE_DISABLED` | `false` | Hide `ctx_*` tools from worker harness |
| `SWARM_USE_CLAUDE_BRIDGE` | `false` | Route Claude sessions through `claude-bridge` tmux binary |
| `ANONYMIZED_TELEMETRY` | `true` | Opt-out of anonymized usage telemetry |

**Configuration files:**

| Path | Purpose |
|---|---|
| `.env` / `.env.example` | Main environment config (API server + local dev) |
| `.env.docker` / `.env.docker-lead` | Docker worker/lead container env |
| `.env.docker-devin.example` | Devin provider worker config reference |
| `.mcp.json` | MCP server connection config (written by `connect` command) |
| `.claude/settings.local.json` | Claude Code project settings (written by `connect`) |
| `agent-swarm-db.sqlite` | SQLite database file |
| `ecosystem.config.cjs` | PM2 process definitions (API + UI + lead + worker) |

---

## 9. Extensibility Points

- **New harness provider.** Create `src/providers/<name>-adapter.ts` implementing the `ProviderAdapter` interface (`src/providers/types.ts`). Register in `createProviderAdapter()` (`src/providers/index.ts`). Add a credential-check function and wire into `src/commands/provider-credentials.ts`. Add a `HARNESS_PROVIDER=<name>` branch in `docker-entrypoint.sh` for Docker packaging.

- **New MCP tool.** Implement the tool in `src/tools/<tool-name>.ts` exporting a `register<ToolName>Tool(server: McpServer)` function. Import and call it in `src/server.ts:createServer()`. If it has an HTTP endpoint, add a `route()` handler in `src/http/<domain>.ts` using the `route()` factory from `src/http/route-def.ts` and register it in `handleRequest()` in `src/http/index.ts`. Run `bun run docs:openapi` to regenerate `openapi.json`.

- **New integration (webhook / external trigger).** Add a handler module in `src/<integration>/`. Wire inbound webhook registration in `src/http/webhooks.ts` or a new dedicated handler. Start the integration in the `httpServer.listen()` callback in `src/http/index.ts`. Add the required env vars to `.env.example`. Add a `*_DISABLE=true` kill-switch guard.

- **New workflow node type.** Workflow nodes are defined in `src/workflows/` with executor logic per `type` string. The `trigger` schema subset supported is `type`, `required`, `properties`, `enum`, `const`, `items` (see `src/workflows/json-schema-validator.ts`). The reusable script catalog (`swarm-script` node) can be extended by adding entries to `src/be/seed/scripts.ts`.

- **New database migration.** Add `src/be/migrations/NNN_descriptive_name.sql` with the next sequential number. The runner auto-applies on server startup in order. Never modify an applied migration; add a new one. Keep `AgentTaskSourceSchema` in `src/types.ts` in sync with any new `CHECK` constraints on `agent_tasks.source`.

- **New prompt template.** Add or update a registered template in `src/prompts/`. Templates are resolved via `resolveTemplateAsync()`. Do not hardcode prompt text in runner, hooks, or providers — all system prompt content must flow through the template registry.

---

## 10. Limitations and Gotchas

- **SQLite as the sole state store.** No distributed or HA option. The DB file must live on a shared filesystem if API and workers run on different hosts. `sqlite-vec` embeddings colocate with the DB, so there is no external vector index to fail over.

- **Worker-to-API HTTP boundary is absolute.** `scripts/check-db-boundary.sh` (run in CI) rejects any `import` of `src/be/db` from worker-side code (`src/commands/`, `src/providers/`, `src/prompts/`, `src/hooks/`, `src/cli.tsx`, `src/claude.ts`). Violating this makes worker Docker containers non-functional in fleet deployments.

- **`process.env.API_KEY` access is forbidden outside `getApiKey()`.** `scripts/check-api-key-boundary.sh` enforces this. Direct env-var reads bypass the `AGENT_SWARM_API_KEY` > `API_KEY` precedence chain and will fail in deployments that only set `AGENT_SWARM_API_KEY`.

- **Scripts runtime uses subprocess execution with `ulimit` sandboxing** (`ulimit -v 524288 -t 60 -u 32 -f 65536 -n 64`, 30 s AbortController, 1 MB stdout cap). User-supplied TypeScript is typechecked at upsert time (`tsc --noEmit`) against a generated SDK `.d.ts`, but the sandbox is not a true container — a compromised script can still make network calls via `fetch`.

- **Claude bridge / `CLAUDE_BINARY` is a tmux-dependent path.** Using `SWARM_USE_CLAUDE_BRIDGE=true` requires `tmux` in the worker container (installed by `Dockerfile.worker` by default) and a pre-seeded `~/.claude.json` trust acceptance. The bridge is needed to run Claude on a subscription-pool credit plan after Anthropic's programmatic-credit split.

- **Version-pinned harness binaries drift.** `Dockerfile.worker` pins exact versions of Claude Code, pi-mono, Codex CLI, and opencode. These go stale quickly and require periodic bumps via PR; the changelog shows these happen every 2–3 weeks.

- **OpenAPI spec and Helm chart must be regenerated manually on version bumps.** CI fails with "OpenAPI Spec Freshness Check" and "chart-version sync check" if `bun run prepare-release` is not run and committed alongside a `package.json` version bump.

- **Dropped identity columns from migration 064.** The old inline `slackUserId`, `linearUserId`, `githubUsername`, `gitlabUsername` columns on agents were removed in favor of `user_external_ids`. Payloads using the old field names now fail Zod validation at runtime with no backward-compatibility shim.

- **`x402` payments module is alpha / opt-in.** `src/x402/` is in-tree but not activated by default. Production deployments should keep it gated; it pulls in `viem` and `@x402/*` adding non-trivial bundle surface.

---

## 11. How It Compares to Alternatives

**Devin (Cognition AI, SaaS).** Devin is a fully managed autonomous software engineer accessed via browser UI or API; `agent-swarm` is a self-hosted orchestration layer that can *drive* Devin as one of its harness providers. Where Devin is opinionated and single-agent, `agent-swarm` is agnostic to the underlying AI and supports fleet-scale task queuing across multiple providers simultaneously.

**HumanLayer.** HumanLayer focuses on the human-in-the-loop approval gate pattern — routing AI tool calls to humans for approval before execution. `agent-swarm` includes an approval-request MCP tool but is primarily task-queue and harness infrastructure; HumanLayer does not manage the harness subprocess lifecycle, credential pools, or persistent memory.

**CrewAI / LangGraph (Python frameworks).** These are in-process Python frameworks for multi-agent orchestration using LLM API calls directly. `agent-swarm` differs in three ways: (1) it drives existing CLI-based agents rather than making API calls, (2) the "agents" are long-lived processes polling for tasks rather than ephemeral chain nodes, and (3) coordination happens over HTTP with a persistent DB rather than in-memory Python objects.

**OpenHands (formerly OpenDevin).** OpenHands is an open-source agent that operates a coding environment (browser, terminal, file editor) for a single agent instance. `agent-swarm` does not provide the agent environment itself — it provides the coordination, queuing, and integrations layer for *whatever* agent environment is already installed in the worker container.

**Positioning statement:** `agent-swarm` occupies the infrastructure layer below the AI model and above the human — a self-hosted task queue, credential broker, and observability bus purpose-built for fleets of AI coding agent CLIs running in Docker containers.

---

## Appendix: Selected Code Snippets

**Task status enum with terminal set** (`src/types.ts:1-30`, approximately)

```typescript
export const AgentTaskStatusSchema = z.enum([
  "backlog",       // Task is in backlog, not yet ready for pool
  "unassigned",    // Task pool - no owner yet
  "offered",       // Offered to agent, awaiting accept/reject
  "reviewing",     // Agent is reviewing an offered task
  "pending",       // Assigned/accepted, waiting to start
  "in_progress",
  "paused",        // Interrupted by graceful shutdown (legacy), can resume
  "completed",
  "failed",
  "cancelled",     // Task was cancelled by lead or creator
  "superseded",    // Original terminated, replaced by a follow-up "resume" task
]);

export const TERMINAL_TASK_STATUSES = [
  "completed", "failed", "cancelled", "superseded"
] as const;

export function isTerminalTaskStatus(status: string): status is TerminalTaskStatus {
  return (TERMINAL_TASK_STATUSES as readonly string[]).includes(status);
}
```

**Budget admission guard** (`src/be/budget-admission.ts:73-139`)

```typescript
export function canClaim(
  agentId: string,
  nowUtc: Date,
  requestedByUserId?: string,
): BudgetAdmissionResult {
  if (process.env.BUDGET_ADMISSION_DISABLED === "true") {
    if (!killSwitchWarned) {
      killSwitchWarned = true;
      console.warn("[budget-admission] BUDGET_ADMISSION_DISABLED=true ...");
    }
    return { allowed: true };
  }

  const dateUtc = dateUtcFrom(nowUtc);
  const resetAt = nextUtcMidnight(nowUtc);

  // 1. Global budget gate.
  const globalBudget = getBudget("global", "");
  if (globalBudget !== null) {
    const globalSpend = getDailySpendGlobal(dateUtc);
    if (globalSpend >= globalBudget.dailyBudgetUsd) {
      return { allowed: false, cause: "global", globalSpend,
               globalBudget: globalBudget.dailyBudgetUsd, resetAt };
    }
  }

  // 2. Per-agent budget gate.
  const agentBudget = getBudget("agent", agentId);
  if (agentBudget !== null) {
    const agentSpend = getDailySpendForAgent(agentId, dateUtc);
    if (agentSpend >= agentBudget.dailyBudgetUsd) {
      return { allowed: false, cause: "agent", agentSpend,
               agentBudget: agentBudget.dailyBudgetUsd, resetAt };
    }
  }

  // 3. Per-user budget gate.
  if (requestedByUserId) {
    const userBudget = getBudget("user", requestedByUserId);
    if (userBudget !== null) {
      const userSpend = getDailySpendForUser(requestedByUserId, dateUtc);
      if (userSpend >= userBudget.dailyBudgetUsd) {
        return { allowed: false, cause: "user", userSpend,
                 userBudget: userBudget.dailyBudgetUsd, resetAt };
      }
    }
  }

  return { allowed: true };
}
```

**MCP server capability-gating** (`src/server.ts`, excerpt)

```typescript
const DEFAULT_CAPABILITIES =
  "core,task-pool,profiles,services,scheduling,memory,workflows,pages,metrics,kv";
const CAPABILITIES = new Set(
  (process.env.CAPABILITIES || DEFAULT_CAPABILITIES).split(",").map((s) => s.trim()),
);

export function hasCapability(cap: string): boolean {
  return CAPABILITIES.has(cap);
}

// Memory capability - persistent memory with vector search
if (hasCapability("memory")) {
  registerMemorySearchTool(server);
  registerMemoryGetTool(server);
  registerMemoryDeleteTool(server);
  registerMemoryRateTool(server);
  registerInjectLearningTool(server);
}
```

**Initial DB schema — agent_tasks table** (`src/be/migrations/001_initial.sql:73-107`)

```sql
CREATE TABLE IF NOT EXISTS agent_tasks (
    id TEXT PRIMARY KEY,
    agentId TEXT,
    creatorAgentId TEXT,
    task TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    source TEXT NOT NULL DEFAULT 'mcp' CHECK(source IN (
        'mcp', 'slack', 'api', 'github', 'agentmail', 'system', 'schedule'
    )),
    taskType TEXT,
    tags TEXT DEFAULT '[]',
    priority INTEGER DEFAULT 50,
    dependsOn TEXT DEFAULT '[]',
    offeredTo TEXT,
    offeredAt TEXT,
    acceptedAt TEXT,
    rejectionReason TEXT,
    slackChannelId TEXT,
    slackThreadTs TEXT,
    slackUserId TEXT,
    mentionMessageId TEXT,
    mentionChannelId TEXT,
    githubRepo TEXT,
    githubEventType TEXT,
    githubNumber INTEGER,
    githubCommentId INTEGER,
    githubAuthor TEXT,
    githubUrl TEXT,
    epicId TEXT REFERENCES epics(id) ON DELETE SET NULL,
    parentTaskId TEXT,
    claudeSessionId TEXT,
    -- ... additional columns in later migrations
);
```
