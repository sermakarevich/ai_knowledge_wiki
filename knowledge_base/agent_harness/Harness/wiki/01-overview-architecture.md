> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Harness Workspace and Control-Plane Architecture

**In one sentence:** Harness is a Rust workspace (13 crates) whose central design bet is a persistent central control plane — an Axum HTTP server backed by Postgres — that schedules, isolates, and reconciles work executed by pluggable agent executors (Claude Code, Codex) running outside the request path.

## Key points

- The workspace declares 13 members in `Cargo.toml:3-17` and pins them all to version `0.6.34` via `Cargo.toml:19-20` and `Cargo.toml:31-42`.
- `harness-core` holds the domain model, configuration, prompts, and agent traits (`crates/harness-core/Cargo.toml:7`); `harness-protocol` defines the JSON-RPC 2.0 method/message types (`crates/harness-protocol/Cargo.toml:5`); `harness-workflow` implements the workflow runtime state machine (`crates/harness-workflow/Cargo.toml:5`).
- `harness-server` contains the HTTP server, task runner, and workflow runtime glue (`crates/harness-server/Cargo.toml:5`); `harness-agents` adapts external agent CLIs, Claude Code and Codex (`crates/harness-agents/Cargo.toml:5`); `harness-exec` provides process-execution helpers (`crates/harness-exec/Cargo.toml:5`).
- `harness-sandbox` provides isolation primitives (`crates/harness-sandbox/Cargo.toml:5`); `harness-gc` handles garbage collection and workspace cleanup (`crates/harness-gc/Cargo.toml:5`); `harness-rules` loads and evaluates policy rules (`crates/harness-rules/Cargo.toml:5`); `harness-skills` handles skill discovery and management (`crates/harness-skills/Cargo.toml:5`).
- `harness-context` composes deterministic agent context (`crates/harness-context/Cargo.toml:5`); `harness-observe` provides logging, tracing, and metrics (`crates/harness-observe/Cargo.toml:5`); `harness-cli` is the operator command-line interface (`crates/harness-cli/Cargo.toml:5`).
- All durable state lives in Postgres (image `postgres:16`, `docker-compose.yml:4`) accessed through `sqlx` with the `postgres` feature (`Cargo.toml:61`); pool construction uses `PgPoolOptions` with per-store `max_connections` and `acquire_timeout` (`crates/harness-core/src/db_pg.rs:497-501`), defaulting to 8 connections and 10 s acquire timeout (`crates/harness-core/src/db_pg.rs:13-14`).
- The operator-facing control plane is the Axum (`Cargo.toml:48`) REST surface built in `crates/harness-server/src/http/http_router.rs:29-30` and served by binding a `TcpListener` in `crates/harness-server/src/http/mod.rs:97-98`, defaulting to `127.0.0.1:9800` (`config/default.toml.example:16`, `crates/harness-core/src/config/server.rs:259`); the agent-facing data plane is the JSON-RPC router in `crates/harness-server/src/router/mod.rs:1-8`, which explicitly excludes task submission and project registration.
- Local boot is `start-server.sh` (builds `./target/release/harness` via `cargo build --release -p harness-cli` per `start-server.sh:327`, starts Postgres with `docker compose up -d --wait postgres` per `start-server.sh:356`, then execs `harness serve --transport http` per `start-server.sh:376`).

---

## Crate map

Workspace membership (`Cargo.toml:3-17`) with approximate Rust size (lines counted via `cat $(find crates/<c> -name '*.rs') | wc -l`):

```toml
[workspace]
resolver = "2"
members = [
    "crates/harness-core",
    "crates/harness-protocol",
    "crates/harness-server",
    "crates/harness-agents",
    "crates/harness-sandbox",
    "crates/harness-gc",
    "crates/harness-rules",
    "crates/harness-skills",
    "crates/harness-exec",
    "crates/harness-context",
    "crates/harness-observe",
    "crates/harness-cli",
    "crates/harness-workflow",
]

[workspace.package]
version = "0.6.34"
edition = "2021"
license = "MIT"
rust-version = "1.88"
repository = "https://github.com/majiayu000/harness"
```

| Crate | Files | LOC (~) | Role |
|---|---|---|---|
| harness-core | 91 | 29,125 | config, domain types, Postgres pool/store layer |
| harness-protocol | 7 | 1,980 | JSON-RPC method and message types |
| harness-server | 417 | 155,916 | Axum server, task runner, reconciliation, handlers |
| harness-agents | 53 | 19,825 | Claude/Codex agent adapters and registry |
| harness-sandbox | 5 | 1,822 | isolation primitives |
| harness-gc | 7 | 2,110 | workspace garbage collection |
| harness-rules | 8 | 3,013 | rule loading and evaluation |
| harness-skills | 5 | 1,869 | skill discovery and management |
| harness-exec | 3 | 369 | process execution helpers |
| harness-context | 5 | 1,753 | deterministic context composition |
| harness-observe | 20 | 5,064 | observability (logging, tracing, metrics) |
| harness-cli | 29 | 8,547 | operator CLI (`serve`, `exec`, `pr`, `gc`, `rule`, `skill`, `plan`, `eval`, `runtime`, `reconcile`, `status`, `version`, `mcp-server`) per `crates/harness-cli/src/commands.rs:37-174` |
| harness-workflow | 222 | 82,472 | workflow runtime state machine and plan DB |

The size distribution is the architecture: `harness-server` and `harness-workflow` together hold ~238 kLOC of control-plane logic, while the executor-facing crates (`harness-agents`, `harness-exec`, `harness-sandbox`) are thin adapters. CLI dispatch funnels every subcommand through config load plus `configure_pg_pool_from_server` before running (`crates/harness-cli/src/commands.rs:176-182`).

## Control-plane data flow

```
operator CLI (harness serve/exec/pr/...)         external triggers (GitHub/Feishu webhooks, pollers)
│                                                  │
▼                                                  ▼
crates/harness-cli/src/commands.rs ──► Axum router (http/http_router.rs:29) ──► handlers/ (handlers/mod.rs:1-28)
│                                                  │
│                                                  ▼
│                                         task_queue/ + task_runner/ + workflow_runtime_* (lib.rs:64-81)
│                                                  │
│                                                  ▼
│                                         harness-agents registry ──► external agent CLIs (Claude/Codex)
│                                                  │
└─────────────────── Postgres (sqlx pools) ◄──────┘
```

End-to-end flow:

1. Operator boots the server (`start-server.sh:376` execs `harness serve --transport http`), which builds `AppState` (`crates/harness-server/src/http/mod.rs:94-95`) and binds the Axum `Router` from `http_router::build_router` (`crates/harness-server/src/http/mod.rs:95`).
2. Control-plane writes (project registration, task submission, workflow queries) arrive as REST routes (`crates/harness-server/src/http/http_router.rs:44-79`); agent-plane calls arrive as JSON-RPC on `/rpc` (`crates/harness-server/src/http/http_router.rs:42`) and are dispatched by `router::handle_request` (`crates/harness-server/src/router/mod.rs:16-34`), which gates everything behind the `initialize`/`initialized` handshake (`crates/harness-server/src/router/mod.rs:22-33`).
3. Queued work flows through `task_queue`/`task_runner` and the `workflow_runtime_*` workers declared in `crates/harness-server/src/lib.rs:64-81`; startup also runs one GitHub reconciliation tick before recovery (`crates/harness-server/src/http/mod.rs:179-187`).
4. Execution is delegated to agent adapters resolved via `AgentRegistry` held on `HarnessServer` (`crates/harness-server/src/server.rs:93-102`); agents run as external processes under sandbox/isolation policy, never inside the HTTP request handler.
5. Results, events, and reconciliation outcomes are written back to Postgres-backed stores and re-exposed through the same REST/RPC read routes, closing the loop.

## Persistent state and local boot

Postgres is the only durable store; the binary itself holds scheduling state in memory (`TaskSchedulerState`, `AppState`) rebuilt at startup. The local database definition:

```yaml
services:
  postgres:
    container_name: harness-postgres
    image: postgres:16
    environment:
      POSTGRES_DB: harness
      POSTGRES_USER: harness
      POSTGRES_PASSWORD: harness
    command: ["postgres", "-c", "max_connections=300"]
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - harness_pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U harness -d harness"]
      interval: 5s
      timeout: 5s
      retries: 6

volumes:
  harness_pg_data:
    name: harness_pg_data
```

Pool behavior: `configure_pg_pool_from_server` copies `server.database_pool_max_connections` / `server.database_pool_acquire_timeout_secs` into a global override (`crates/harness-core/src/db_pg.rs:51-57`); `pg_pool_settings` falls back to 8 connections, 10 s timeout, or 1 connection for Supabase pooler URLs (`crates/harness-core/src/db_pg.rs:65-96`); environment variables `HARNESS_DATABASE_POOL_MAX_CONNECTIONS` / `HARNESS_DATABASE_POOL_ACQUIRE_TIMEOUT_SECS` take highest precedence (`crates/harness-core/src/db_pg.rs:146-153`). URL resolution precedence is explicit TOML value, then `HARNESS_DATABASE_URL`, then config-file discovery (`crates/harness-core/src/db_pg.rs:100-118`), with the local default `postgres://harness:harness@localhost:5432/harness` (`config/default.toml.example:17`, `scripts/dev-db.sh:37`). `scripts/dev-db.sh:31-41` starts the container idempotently and recommends pool overrides of 16 connections / 60 s timeout for local work. `start-server.sh:102-106` defaults the bind address to `127.0.0.1:9800` when neither env nor config supplies `http_addr`, and `config/default.toml.example:14-30` shows the `[server]` block (`transport`, `http_addr`, `database_url`, pool knobs, `data_dir`, `project_root`).

**Covers:** Cargo.toml, docker-compose.yml, start-server.sh, scripts/dev-db.sh, config/default.toml.example, crates/ (workspace listing), crates/harness-*/Cargo.toml descriptions, crates/harness-server/src/lib.rs, crates/harness-server/src/server.rs, crates/harness-server/src/db.rs, crates/harness-server/src/http/mod.rs, crates/harness-server/src/http/init.rs, crates/harness-server/src/http/http_router.rs, crates/harness-server/src/router/mod.rs, crates/harness-server/src/handlers/mod.rs, crates/harness-cli/src/commands.rs, crates/harness-core/src/db_pg.rs, crates/harness-core/src/config/server.rs
