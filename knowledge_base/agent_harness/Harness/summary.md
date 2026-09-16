# Technical Analysis: majiayu000/harness
**Repository:** https://github.com/majiayu000/harness
**Version analyzed:** 0.6.34 @ 8b23adb6241b85e58b652f6ab5ec33198aa9a8a6 (2026-09-06)
**Date:** 2026-09-09

---
## 1. Overview / What Problem It Solves
Harness is a Rust workspace (13 crates, all pinned to `0.6.34` via `Cargo.toml:19-20`) that provides a persistent central control plane — an Axum HTTP server backed by Postgres — for scheduling, isolating, and reconciling work executed by pluggable agent executors running outside the request path (`wiki/01-overview-architecture.md:5`).
It separates orchestration (REST + JSON-RPC over Postgres), enforcement (policy stores queried at spawn/commit time), and observation (event log plus optional OTLP export) (`wiki/targeted.md:14`).
Work intake is a submissions API over `WorkflowInstance` + `RuntimeJob` rows with a separate `ExecPlan` plan object (`wiki/targeted.md:8`); execution is delegated to external agent CLIs under sandbox and policy constraints (`wiki/01-overview-architecture.md:91`).
Output is checked through a primary-plus-challenger review protocol, quality gates, and a signal-driven garbage-collection (GC) loop that stages rule/guard/skill fixes as adoptable drafts (`wiki/06-review-and-gc.md:4`).

## 2. High-Level Architecture
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
(adapted from `wiki/01-overview-architecture.md:71-84`)

1. Operator boots the server (`start-server.sh:376` execs `harness serve --transport http`), which builds `AppState` (`crates/harness-server/src/http/mod.rs:94-95`) and binds the Axum `Router` from `http_router::build_router` (`wiki/01-overview-architecture.md:88`).
2. Control-plane writes (project registration, task submission, workflow queries) arrive as REST routes (`crates/harness-server/src/http/http_router.rs:44-79`); agent-plane calls arrive as JSON-RPC on `/rpc` (`crates/harness-server/src/http/http_router.rs:42`) gated behind the `initialize`/`initialized` handshake (`crates/harness-server/src/router/mod.rs:22-33`) (`wiki/01-overview-architecture.md:89`).
3. Queued work flows through `task_queue`/`task_runner` and the `workflow_runtime_*` workers declared in `crates/harness-server/src/lib.rs:64-81`; startup runs one GitHub reconciliation tick before recovery (`crates/harness-server/src/http/mod.rs:179-187`) (`wiki/01-overview-architecture.md:90`).
4. Execution is delegated to agent adapters resolved via `AgentRegistry` held on `HarnessServer` (`crates/harness-server/src/server.rs:93-102`); agents run as external processes under sandbox/isolation policy, never inside the HTTP request handler (`wiki/01-overview-architecture.md:91`).
5. Results, events, and reconciliation outcomes are written back to Postgres-backed stores and re-exposed through the same REST/RPC read routes (`wiki/01-overview-architecture.md:92`).

Persistent state lives only in Postgres (image `postgres:16`, `docker-compose.yml:4`, accessed via `sqlx` with the `postgres` feature, `Cargo.toml:61`); pool construction uses `PgPoolOptions` defaulting to 8 connections and 10 s acquire timeout (`crates/harness-core/src/db_pg.rs:13-14,497-501`) (`wiki/01-overview-architecture.md:14`). The binary holds scheduling state in memory (`TaskSchedulerState`, `AppState`) rebuilt at startup (`wiki/01-overview-architecture.md:96`). Schema management uses one schema per logical store via `PgStoreContext`, a `schema_migrations` ledger with per-schema advisory lock, and a `harness_admin.schema_ownership` registry (`crates/harness-core/src/db_pg.rs:331-464,653-722`) (`wiki/07-observability-persistence.md:9`). The event store is a Postgres `events` table (eight migrations, key `(store_key, id)`, batched inserts with `ON CONFLICT DO NOTHING`, JSONL backfill, retention purges) (`wiki/07-observability-persistence.md:7`).

## 3. The Task-Turn-Workflow Core
Three levels coexist: `Thread`/`Turn` (conversation model), `RunId`/`BindingRecord` (process lineage), and `WorkflowInstance` + `RuntimeJob` (schedulable durable unit) (`wiki/02-task-turn-lifecycle.md:15`). A `Thread` (project-scoped, status `idle`/`active`/`archived`) holds ordered `Turn`s (one agent-loop iteration each: `running` → `completed`/`cancelled`/`failed`, carrying `items`, token usage, timing), defined in `crates/harness-core/src/types.rs:81-90,150-169` (`wiki/02-task-turn-lifecycle.md:5`). `RunId` is `ar-` + 26-char lowercase ULID propagated via `AGENT_RUN_ID`/`AGENT_RUN_PARENT` (`crates/harness-core/src/run_id.rs:6-16,100-151`); `BindingRecord` binds a run to native agent id, pid, cwd (`crates/harness-core/src/run_registry.rs:19-29`) (`wiki/02-task-turn-lifecycle.md:15`).
Submissions (`runtime/submission.rs:62`) map an issue to `RunPlanning` / `RunImplementation` / `WaitForDependencies` (`runtime/submission.rs:34-39`), emitting an `EnqueueActivity` command (`implement_issue` or plan activity) plus a `task_submission` evidence record (`wiki/05-workflow-runtime.md:5`). `CreateTaskRequest` carries `definition_id`, `prompt`, `issue`, `pr`, `force_execute`, `skip_triage`, `project`, `repo`, `labels`, priority capped by `MAX_TASK_PRIORITY` (`wiki/05-workflow-runtime.md:15`).
`ExecPlan` (`harness-exec/src/plan.rs:6-19`) is the plan data model (`purpose`, `project_root`, `progress` milestones, `concrete_steps`, `decision_log`, `surprises`, `validation`, `status`), built by `from_spec` and mutated by `activate`/`add_milestone`/`add_step`/`log_decision`/`complete`/`abandon` (`wiki/05-workflow-runtime.md:6`). It serializes to Markdown for cross-session recovery (`harness-exec/src/plan.rs:140-147`) (`wiki/05-workflow-runtime.md:57`).
Execution is lease-based: `RuntimeJob::claim` sets `status=running`, bumps `lease_generation`, stamps `owner` + `expires_at` (`crates/harness-workflow/src/runtime/model.rs:590-602`); the claim SQL accepts `pending` jobs or `running` jobs whose `data.lease.expires_at` has passed, so dead workers' jobs become reclaimable on expiry (`crates/harness-workflow/src/runtime/job_claim.rs:90-100,168-200`) (`wiki/02-task-turn-lifecycle.md:7`). Lease health is tri-state (`active_leased`/`expired_lease`/`missing_lease`) from `job.status` + `lease.expires_at` (`crates/harness-workflow/src/runtime/lease_state.rs:6-36`); the worker renews at half-TTL (`clamp(ttl/2, 1s, 30s)`) and on losing the lease cancels the agent and dead-letters the result instead of committing (`crates/harness-workflow/src/runtime/worker.rs:245-310,168-207`) (`wiki/02-task-turn-lifecycle.md:8`). Terminal states are definition-scoped: `WorkflowTerminalState` is only `succeeded`/`failed`/`cancelled` (`crates/harness-workflow/src/runtime/state_registry.rs:37-41`); `WorkflowCommandStatus` distinguishes `completed`/`failed`/`blocked`/`cancelled`/`skipped`/`superseded`/`handled_inline` (`wiki/02-task-turn-lifecycle.md:11`).

## 4. LLM / External Service Integration
All backends sit behind `AgentBackend: Send + Sync` (`crates/harness-core/src/agent.rs:84`), aliased as `CodeAgent` and `AgentAdapter`; one-shot CLIs implement `execute`/`execute_stream`, stateful protocols override `start_turn`/`interrupt`/`steer`/`respond_approval`, all unimplemented controls default to `Unsupported` (`wiki/04-agent-adapters.md:5`). Per-adapter executors are `ClaudeCodeAgent` (`crates/harness-agents/src/claude.rs:28`), `CodexAgent` (`crates/harness-agents/src/codex.rs:52`), `AnthropicApiAgent` (`crates/harness-agents/src/anthropic_api.rs:9`), and `OpenCodeAgent` plus `parse_opencode_run_line` (`crates/harness-agents/src/opencode.rs:48`) (`wiki/04-agent-adapters.md:8`).
`AgentRegistry` (`crates/harness-agents/src/registry.rs:19`) stores `AgentDescriptor { backend, control_backend, turn_backend_factory }` per name; lookup is `get(name)`, side-channel `get_adapter(name)`, per-turn factory `turn_execution_adapter(name)`, complexity routing `dispatch(task)` (`wiki/04-agent-adapters.md:6`). `registry_from_config` (`crates/harness-agents/src/builder.rs:135`) registers `claude`, `codex` + `CodexAdapter` turn factory, `opencode` + `OpenCodeAcpAdapter` turn factory unconditionally, and `anthropic-api` only when `ANTHROPIC_API_KEY` is present (`crates/harness-agents/src/builder.rs:182-190`) (`wiki/04-agent-adapters.md:7`). The configured `default_agent` string (`--agent` selection) resolves via `resolved_default_agent_name`/`default_agent`, falling back to the first registered backend when empty, `auto`, or unregistered (`wiki/04-agent-adapters.md:39`). No external LLM call is required for the control plane itself to boot; agent execution requires at least one CLI backend (`claude`/`codex`/`opencode`) installed, and only `anthropic-api` requires `ANTHROPIC_API_KEY` (`wiki/04-agent-adapters.md:7`).
Streaming is per-agent: Claude `--output-format stream-json` via `parse_stream_json_events` (`crates/harness-agents/src/claude_stream_json.rs:25`), Codex `exec --json` via `parse_codex_item`/`parse_codex_exec_output` (`crates/harness-agents/src/codex_exec_parser.rs:77`), OpenCode `run --format json` lines to `OpenCodeRunEvent::{Text, ToolUse, StepFinish}` (`crates/harness-agents/src/opencode.rs:25-96`) (`wiki/04-agent-adapters.md:11`). Permission shaping: Claude maps `allowed_tools`/capability profile to `--allowedTools`; Codex maps `allowed_tools == Some([])` to deny-all and forwards `approval_policy` via `-c approval_policy=...`; OpenCode merges restrictions through inlined `OPENCODE_PERMISSION` JSON env (`wiki/04-agent-adapters.md:12`). Cross-cutting guards: provider backpressure semaphore gate (`crates/harness-agents/src/provider_backpressure.rs:50-60`), scoped GitHub tokens (`crates/harness-agents/src/scoped_token.rs:7-9`), Anthropic-backed compression model reusing `AnthropicApiAgent` (`wiki/04-agent-adapters.md:12`). Env vars attested in wiki: `ANTHROPIC_API_KEY` (gates `anthropic-api` registration), `HARNESS_DATABASE_URL`, `HARNESS_DATABASE_POOL_MAX_CONNECTIONS`, `HARNESS_DATABASE_POOL_ACQUIRE_TIMEOUT_SECS`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `AGENT_RUN_ID`/`AGENT_RUN_PARENT`, `OPENCODE_PERMISSION` (inlined JSON), `CI` (disables hook enforcement) (`wiki/01-overview-architecture.md:123`, `wiki/03-policy-engine.md:10`, `wiki/04-agent-adapters.md:7,12`, `wiki/07-observability-persistence.md:6`).

## 5. The Issue-to-Merge Pipeline
1. Issue intake builds a submission decision: `build_issue_submission_decision` (`runtime/submission.rs:62-145`) yields `planning` + plan-activity command by default, `implementing` + `implement_issue` when `force_execute`, `awaiting_dependencies` with no command when `dependencies_blocked`; both paths attach `remote_fact_hash` and `submission_mode` (`Immediate`/`Deferred`, `runtime/submission.rs:9-32`) (`wiki/05-workflow-runtime.md:15`).
2. Dispatch gates before enqueue in `RuntimeCommandDispatcher::dispatch_command` (`runtime/dispatcher.rs:178-346`): skip non-runtime commands, drop terminal workflows, resolve effective profile, enforce agent-contract and isolation availability, apply the budget gate, then `enqueue_runtime_job_for_claimed_command` with `AlreadyDispatched` dedupe on `dedupe_key` (`wiki/05-workflow-runtime.md:7`). Profile selection resolves workflow-activity > activity > workflow > default (`runtime/dispatcher_profile_selector.rs:56-68`); budgets/throttle live in `budget_gate_outcome` (`runtime/dispatcher.rs:370-462`) with `daily_throttle_breach` (`runtime/dispatcher_throttle.rs:38-85`) (`wiki/05-workflow-runtime.md:8-9`).
3. Each task executes in an isolated git worktree: `WorkspaceManager` creates `config.root/<sanitized_task_id>` from `remote/base_branch` on branch `harness/<task_id>` (`harness-server/src/workspace_create.rs:8-13`), verified by `is_registered_worktree`, removed by `remove_worktree` (`harness-server/src/workspace_helpers.rs:201,478`); `WORKFLOW.md:14-18` declares `strategy: worktree`, `branch_prefix: harness/`, `cleanup: on_terminal` (`wiki/05-workflow-runtime.md:11`). Concurrency is bounded by `TaskQueue` (global `PriorityPermitQueue` + per-project queues, `task_queue/mod.rs:222-248`) and `WorkspacePool::acquire_with_capacity` (per-project semaphores, default capacity 4, `workspace_pool.rs:8,91-114`) (`wiki/05-workflow-runtime.md:10`).
4. Validators and quality gates close the loop: `TransitionRule` (`runtime/validator.rs:31-40`) constrains allowed/required commands and evidence per transition; `build_quality_gate_run_decision` (`runtime/quality_gate.rs:36-73`) enqueues `run_quality_gate`; `WORKFLOW.md:75-89` binds `implement_issue` to `cargo fmt --check`, `cargo check`, `cargo test`, `clippy -D warnings` (`wiki/05-workflow-runtime.md:12`).
5. `PostExecutionValidator` runs `pre_commit`, then `pre_push` only if the first set passed, then GitHub REST verification of claimed PR URLs, retrying up to `max_retries` (`crates/harness-server/src/post_validator.rs:14-20,220-344`) (`wiki/06-review-and-gc.md:41`). Cross-agent review runs primary first, then challenger for up to `max_rounds - 1` rounds with outstanding issues re-injected; `CONFIRMED:`/`MISSED:` form the next consensus set; empty set yields `Approved`, untagged reply yields `ProtocolFailure`, leftovers yield `NotConverged` (`crates/harness-server/src/handlers/cross_review.rs:265-339,350-395`) (`wiki/06-review-and-gc.md:15`). PR-feedback repair is capped by `MAX_FEEDBACK_REPAIR_ROUNDS = 3` (`crates/harness-workflow/src/runtime/pr_feedback.rs:13-17,86-116,368-436`); hygiene repair targets PRs with `mergeStateStatus` `DIRTY`/`BEHIND`, and merge itself is a server-executed API call with expected-head-SHA protection (`wiki/06-review-and-gc.md:41`).
6. The periodic reconciler (15 s init delay, then every `interval_secs`) closes the gap with GitHub truth for non-terminal `github_issue_pr` workflows (`done` on merged, `cancelled` on closed) and raises `ready_to_merge` aging alerts (`crates/harness-server/src/reconciliation.rs:174-252`, `crates/harness-server/src/reconciliation_periodic.rs:6-43`) (`wiki/02-task-turn-lifecycle.md:9`).

## 6. Key Files
| File | Lines | What It Does |
|---|---|---|
| `crates/harness-server/src/http/http_router.rs` | 29-112 | Axum REST surface + `/rpc` JSON-RPC mount + submissions routes |
| `crates/harness-server/src/router/mod.rs` | 1-34 | Agent-plane JSON-RPC dispatch with `initialize`/`initialized` gate |
| `crates/harness-server/src/lib.rs` | 64-81 | Worker declarations (`task_queue`, `task_runner`, `workflow_runtime_*`) |
| `crates/harness-workflow/src/runtime/worker.rs` | 13-431 | `RuntimeWorker::run_once`, lease renewal, dead-letter on lease loss |
| `crates/harness-workflow/src/runtime/model.rs` | 76-98, 521-602 | `WorkflowInstance`/`RuntimeJob` model, `claim` + `renew_lease` |
| `crates/harness-workflow/src/runtime/job_claim.rs` | 90-235 | Lease-claim SQL (pending or expired-`running`), generation reclaim |
| `crates/harness-workflow/src/runtime/dispatcher.rs` | 56-529 | Claim-then-gate-then-enqueue dispatch, budget gate, barriers |
| `crates/harness-workflow/src/runtime/submission.rs` | 9-190 | Issue→decision mapping (`RunPlanning`/`RunImplementation`/`WaitForDependencies`) |
| `crates/harness-agents/src/registry.rs` | 13-163 | `AgentRegistry`: per-name descriptors, default resolution, complexity dispatch |
| `crates/harness-agents/src/builder.rs` | 29-190 | Single assembly point (`registry_from_config`), per-agent knobs |
| `crates/harness-agents/src/spawn_contract.rs` | 45-477 | `HostSpawn`/`ContainerSpawn` selection, egress, `docker run` emission |
| `crates/harness-rules/src/exec_policy.rs` | 9-286 | `ExecDecision` three-valued policy, prefix matching, host-executable resolution |
| `crates/harness-rules/src/engine/mod.rs` | 50-769 | `RuleEngine`: markdown rules, guard scripts, exec-policy query store |
| `crates/harness-sandbox/src/lib.rs` | 28-273 | `SandboxMode`/`SandboxEngine` selection, Seatbelt/Landlock/bwrap wrapping |
| `crates/harness-server/src/handlers/cross_review.rs` | 138-424 | Primary-challenger review rounds, tag protocol, `distinct_challenger` guard |
| `crates/harness-gc/src/gc_agent.rs` | 104-373 | Signal-driven GC loop, draft persistence, checkpoint advance |
| `crates/harness-gc/src/signal_detector.rs` | 20-291 | Six detectors (`RepeatedWarn`, `ChronicBlock`, `HotFiles`, `SlowSessions`, `WarnEscalation`, `LinterViolations`) |
| `crates/harness-observe/src/otel_export.rs` | 1-527 | OTLP traces/metrics/logs pipeline, endpoint resolution, redaction |
| `crates/harness-context/src/composer.rs` | 169-653 | Budgeted context composition: quotas, `dedupe_key`, degradation levels |
| `crates/harness-core/src/db_pg.rs` | 13-722 | Pool sizing/URL precedence, per-schema migration with advisory lock |

## 7. Dependencies
| Package | Version constraint | Purpose |
|---|---|---|
| `tokio` | `1` + `full` | Async runtime |
| `axum` | `0.8` + `ws` | HTTP server + websocket |
| `tower` | `0.5` | Middleware stack |
| `tower-http` | `0.6` + `cors`, `trace` | CORS, tracing middleware |
| `serde` | `1` + `derive` | Serialization framework |
| `serde_json` | `1` | JSON payloads (RPC, events, drafts) |
| `jsonschema` | `0.52`, `default-features = false` | Output-schema validation |
| `json5` | `1.3` | Lenient JSON parsing |
| `serde_yaml` | `0.9` | YAML config/prompt parsing |
| `toml` | `0.8` | TOML config (`harness.toml`, `requirements.toml`) |
| `sqlx` | `0.8` + `runtime-tokio`, `tls-rustls-ring-webpki`, `postgres`, `sqlite`, `chrono`, `uuid` | Postgres (+sqlite legacy) persistence |
| `clap` | `4` + `derive` | CLI argument parsing |
| `dashmap` | `6` | Concurrent maps (scheduler state) |
| `tracing` | `0.1` | Structured logging facade |
| `tracing-subscriber` | `0.3` + `env-filter`, `json`, `chrono` | Log formatting/filtering |
| `opentelemetry` | `0.27` + `trace`, `metrics`, `logs` | OTel API |
| `opentelemetry_sdk` | `0.27` + `trace`, `metrics`, `logs`, `rt-tokio` | OTel SDK |
| `opentelemetry-otlp` | `0.27` + `trace`, `metrics`, `logs`, `grpc-tonic`, `http-proto`, `reqwest-client` | OTLP export (4317 gRPC / 4318 HTTP) |
| `chrono` | `0.4` + `serde` | Timestamps (`expires_at`, events) |
| `chrono-tz` | `0.8` + `serde` | Timezone handling |
| `uuid` | `1` + `v4`, `serde` | Entity IDs |
| `regex` | `1` | Pattern matching (parsing, guards) |
| `glob` | `0.3` | File-pattern discovery (rules, skills) |
| `shlex` | `1.3` | Shell tokenization for policy matching |
| `starlark` | `0.13` | Starlark dialect for exec-policy files |
| `thiserror` | `2` | Typed errors |
| `anyhow` | `1` | Ad-hoc error propagation |
| `async-trait` | `0.1` | Async `AgentBackend` trait |
| `libc` | `0.2` | OS primitives (process groups) |
| `futures` | `0.3` | Stream/combinator utilities |
| `tokio-stream` | `0.1` | Tokio stream adapters |
| `hmac` / `sha2` / `subtle` | `0.12` / `0.10` / `2` | Webhook HMAC, hashing (span IDs), constant-time compare |
| `reqwest` | `0.12` + `json`, `stream` | HTTP client (Anthropic API, GitHub REST) |
| `url` | `2` | URL parsing |
| `sysinfo` | `0.32`, `default-features = false` + `system` | Memory-pressure monitoring |
| `tempfile` | `3` | Test temp dirs |

## 8. CLI / Usage Surface
Entry points: `./target/release/harness` built via `cargo build --release -p harness-cli` (`start-server.sh:327`); local boot is `start-server.sh` (builds binary, `docker compose up -d --wait postgres` per `start-server.sh:356`, execs `harness serve --transport http` per `start-server.sh:376`); default bind `127.0.0.1:9800` (`config/default.toml.example:16`, `crates/harness-core/src/config/server.rs:259`, `start-server.sh:102-106`) (`wiki/01-overview-architecture.md:15-16`).
```
harness serve --transport http     # start control plane (Axum REST + /rpc JSON-RPC)
harness exec ...                   # execute work through agent backends
harness pr ...                     # PR operations (verify/merge/hygiene surface)
harness gc ...                     # garbage-collection loop controls
harness rule ...                   # rule inspection
harness skill ...                  # skill discovery/management
harness plan ...                   # ExecPlan operations
harness eval ...                   # evaluation runs
harness runtime ...                # runtime/workflow inspection
harness reconcile ...              # manual reconciliation tick
harness status ...                 # server/task status
harness version ...                # version (0.6.34)
harness mcp-server ...             # MCP server entry point
harness execpolicy check ...       # offline exec-policy query (serializes ExecPolicyCheckOutput as JSON)
```
(subcommand list per `crates/harness-cli/src/commands.rs:37-174`; every subcommand funnels through config load plus `configure_pg_pool_from_server`, `commands.rs:176-182`; `execpolicy check` per `commands/execpolicy.rs:62`, `exec_policy.rs:125-142`) (`wiki/01-overview-architecture.md:64,67`, `wiki/03-policy-engine.md:32`).
| Env var | Effect |
|---|---|
| `HARNESS_DATABASE_URL` | DB URL fallback when TOML value absent (`db_pg.rs:100-118`) |
| `HARNESS_DATABASE_POOL_MAX_CONNECTIONS` / `HARNESS_DATABASE_POOL_ACQUIRE_TIMEOUT_SECS` | Highest-precedence pool overrides (`db_pg.rs:146-153`) |
| `ANTHROPIC_API_KEY` | Gates `anthropic-api` backend registration (`builder.rs:182-190`) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint fallback before `127.0.0.1:4318`/`4317` defaults (`otel_export.rs:380-432`) |
| `AGENT_RUN_ID` / `AGENT_RUN_PARENT` | Run lineage propagation (`run_id.rs:6-16,100-151`) |
| `CI` | Hook enforcer passes when set (`hook_enforcer.rs:107-128`) |
| `OPENCODE_PERMISSION` | Inlined JSON permission merge for OpenCode backend (`opencode.rs:18`) |
| Config files | Purpose |
|---|---|
| `config/default.toml.example:14-30` | `[server]` block example (`transport`, `http_addr`, `database_url`, pool knobs, `data_dir`, `project_root`) |
| `harness.toml.example:1-16` | Review settings only (`vibeguard`/`refine`); contains no sandbox/policy keys |
| `requirements.toml` | Second exec-policy source; may express only `prompt`/`forbidden` (`requirements.rs:77-82`) |
| `*.star` policy files | `prefix_rule`/`host_executable` declarations (512 KiB cap, stack depth 512) |
| `AGENTS.md` / `CLAUDE.md` (+ `AGENTS.override.md`, 32 KB cap) | Static project-instruction layer under dynamic composition (`agents_md.rs:14-50`) |

## 9. Extensibility Points
- Add an agent adapter: implement `AgentBackend` (`crates/harness-core/src/agent.rs:84`) — one-shot CLIs implement `execute`/`execute_stream`, stateful protocols override `start_turn`/`interrupt`/`steer`/`respond_approval` — then register name + optional `control_backend`/`turn_backend_factory` in `registry_from_config` (`crates/harness-agents/src/builder.rs:135-190`) alongside the `claude`/`codex`/`opencode`/`anthropic-api` entries.
- Add a policy rule: write a `.star` file using only `prefix_rule`/`host_executable` builtins (`exec_policy/parser.rs:307-388`) or append `{token, any_of}` entries to `requirements.toml` (`requirements.rs:20-30`); wire paths via `rules.exec_policy_paths` / `rules.requirements_path` loaded at startup (`http/builders/engines.rs:83-88`); self-test with `match`/`not_match` examples validated at parse time (`exec_policy/parser.rs:118-153`); query offline via `harness execpolicy check` (`commands/execpolicy.rs:62`).
- Add a validator: extend `TransitionRule` constraints (`runtime/validator.rs:31-40,74-80`) or add a per-definition check beside `validator_command_rules`/`validator_evidence`/`validator_github_issue_pr`/`validator_hidden_transitions`/`validator_prompt_task` (`runtime/validator.rs:11-25`); quality-gate workflows go through `build_quality_gate_run_decision` (`runtime/quality_gate.rs:36-73`).
- Add a workflow: compile a declarative definition via `build_declarative_definition` (`runtime/declarative.rs:83-107`), enter via `build_declarative_submission_decision` (`runtime/declarative_interpreter.rs:8-44`) and `record_declarative_submission` (`workflow_runtime_submission/declarative.rs:32`); terminal-state mapping goes through the definition registry consulted by `is_terminal` (`model_workflow_instance.rs:31-37`).
- Add a guard script: drop a `*.sh` file registered by filename stem (`engine/mod.rs:570-619`); it runs as `bash <guard> <project_root> [<file>]` and `FILE:LINE:RULE_ID:MESSAGE` stdout lines become `Violation`s (`engine/mod.rs:638-649,672-703`).
- Add a skill: place Markdown + frontmatter under repo `.harness/skills/`, user `~/.harness/skills/`, or admin `/etc/harness/skills/` (tiers Repo 4 > User 3 > Admin 2 > System 1; name collisions resolve by tier in `discover()`); trigger patterns come from an HTML comment, scored at weight 2.0 vs name 0.8 / description 1.2 / content 0.25 (`wiki/07-observability-persistence.md:41`).
- Add a context provider: propose `ContextItem`s with class, priority (P0/P1/P2), `dedupe_key`, degrade chain in `crates/harness-context/src/providers.rs:45-290`; budgeting/quotas/dedup enforced in `composer.rs:169-590`.

## 10. Limitations and Gotchas
- **Hook enforcer fails open:** passes when disabled, when `CI` is set, when no guards exist, when no affected files are reported, and on scan failure; `Decision::Warn` (not block) even with violations; host-side git inspection disabled so `detect_modified_files` returns empty until agent telemetry supplies file lists (`hook_enforcer.rs:70-76,107-128,141-160`) (`wiki/03-policy-engine.md:10`).
- **Circuit breaker auto-passes:** 3 consecutive blocks open the circuit and auto-pass for 300 s, modeled on Claude Code's `stop_hook_active` (`hook_circuit_breaker.rs:6-8,65-106`, `hook_enforcer.rs:22-31`) (`wiki/03-policy-engine.md:11`).
- **Exec policy is query-only:** the only in-tree caller of `RuleEngine::check_command_policy` (`engine/mod.rs:763-769`) outside tests is the `execpolicy check` CLI; no per-tool-call inline gate on that path was found (`wiki/03-policy-engine.md:8`).
- **No startup replay recovery:** crashed workers recover only via lease-expiry reclamation (running jobs with passed `expires_at` become claimable with `lease_generation + 1`); there is no live instance reconcile-on-startup, only workspace/host restore (`workspace_reconcile.rs:57-160`, `runtime_state_store.rs:194-246`) (`wiki/02-task-turn-lifecycle.md:21`).
- **Single-model review degrades silently:** without a distinct challenger (`candidate.id() != primary.id()`), the gate returns `SingleModelDegraded`/`ApprovedDegraded`, never bare `Approved` — consumers must treat degraded approval as weaker (`cross_review.rs:194-216,416-424`) (`wiki/06-review-and-gc.md:15-17`).
- **Sandbox defaults are permissive:** `SandboxMode` defaults to `DangerFullAccess` (`config/agents/permissions.rs:94-100`), a passthrough unless token paths or network policy narrow it; operator-facing defaults live in code/docs, not in `harness.toml.example` (which has no sandbox/policy keys) (`wiki/03-policy-engine.md:12,36`).
- **Reconciler is GitHub-only and non-destructive:** covers only non-terminal `github_issue_pr` workflows; terminal rows skipped, young `ready_to_merge` skipped, failed applies surface as `reconciliation_anomaly` rather than retrying (`reconciliation_periodic.rs:50-91`) (`wiki/02-task-turn-lifecycle.md:19`).
- **OTLP off by default with probe:** `trajectory` flag defaults off (`config/misc.rs:404-417`); endpoint resolution falls back to localhost defaults followed by a TCP reachability probe that fails pipeline startup when unreachable (`otel_export.rs:380-432`) (`wiki/07-observability-persistence.md:5-6`).

## 11. How It Compares to Alternatives
- Fleet (own-shop beads-based orchestration spawning coder workers): Fleet keeps task state in a beads DB with supervisor-spawned workers, while Harness centralizes on Postgres with leased `RuntimeJob` rows, two-stage (project + global) permit scheduling, and per-task git worktrees. Fleet currently lacks lease-generation crash recovery, policy-as-data exec rules, and staged GC drafts, all of which are directly borrowable (`wiki/targeted.md:23-31`). Positioning: adopt Harness's lease columns + submissions split (plan record vs attempt records) without adopting its 13-crate server.
- Claude Code via GitHub Actions (agentic runners on push/schedule): Actions runners are ephemeral and stateless per job, with concurrency from workflow `concurrency:` groups and review via required checks; Harness instead persists `WorkflowInstance`/turn history, reconciles against GitHub truth (`done` on merged, `cancelled` on closed), and enforces primary-challenger review with no-self-review identity guards. Actions are simpler to operate (no Postgres, no Axum server) but cannot reclaim crashed turns by lease expiry or bound enforcement loops with circuit breakers. Positioning: prefer Harness's model when runs must survive worker loss and accumulate reviewable history; prefer Actions for short stateless tasks.
- OpenAI Codex cloud (hosted agent tasks with sandbox): Codex cloud executes tasks in managed sandboxes behind one provider API, while Harness is provider-neutral (`claude`/`codex`/`opencode`/`anthropic-api` behind one `AgentBackend` trait with per-turn factories and complexity routing) and self-hosts isolation (Seatbelt/Landlock/bwrap + orthogonal network policy). Codex cloud offloads operations but couples runs to one vendor's queue, auth, and retention; Harness keeps the event log, usage/cost attribution, and OTLP trajectory export locally. Positioning: choose Harness when multi-backend routing and local auditability outweigh managed execution.
- Temporal / Cadence (durable workflow engines): Temporal provides general durable execution with replay-based recovery, timers, and versioned workflows, while Harness implements a narrower domain runtime (issue→plan→implement→review→merge with `ExecPlan`, `TransitionRule` validators, quality gates, `MAX_FEEDBACK_REPAIR_ROUNDS = 3`) and recovers via lease-expiry reclamation rather than event-sourced replay. Temporal is the stronger primitive for arbitrary long-lived workflows; Harness adds agent-specific policy (Starlark exec policy, sandbox tiers, skill/context composition, GC drafts) Temporal lacks. Positioning: use Temporal semantics for generic orchestration, Harness patterns for the agent-review-merge loop on top.

## Appendix: Selected Code Snippets
Lease-claim candidate selection — expired `running` jobs become reclaimable (`crates/harness-workflow/src/runtime/job_claim.rs:90-100`):
```sql
WHERE (
    (
        job.status = 'pending'
        AND (job.not_before IS NULL OR job.not_before <= CURRENT_TIMESTAMP)
    ) OR (
        job.status = 'running'
        AND job.data ? 'lease'
        AND (job.data->'lease' ? 'expires_at')
        AND (job.data->'lease'->>'expires_at')::timestamptz <= CURRENT_TIMESTAMP
    )
)
```
Claim + generation bump — each claim increments `lease_generation` so stale completions are detectable (`crates/harness-workflow/src/runtime/model.rs:590-602`):
```rust
pub fn claim(&mut self, owner: impl Into<String>, expires_at: DateTime<Utc>) {
    self.status = RuntimeJobStatus::Running;
    self.lease_generation = self.lease_generation.saturating_add(1);
    self.renew_lease(owner, expires_at);
}

pub fn renew_lease(&mut self, owner: impl Into<String>, expires_at: DateTime<Utc>) {
    self.lease = Some(WorkflowLease {
        owner: owner.into(),
        expires_at,
    });
    self.updated_at = Utc::now();
}
```
No-self-review identity guard — a challenger resolving to the same agent identity degrades instead of double-counting (`crates/harness-server/src/handlers/cross_review.rs:416-424`):
```rust
/// Identity guard (GH-1767): a challenger resolving to the same agent
/// identity as the primary is no challenger at all — degrade instead of
/// "reviewing" with a single model twice.
fn distinct_challenger(
    primary: &Arc<dyn CodeAgent>,
    challenger: Option<Arc<dyn CodeAgent>>,
) -> Option<Arc<dyn CodeAgent>> {
    challenger.filter(|candidate| candidate.id() != primary.id())
}

/// True when any line carries one of the three protocol tag prefixes, even
/// with an empty body (which `extract_tagged` filters out).
fn has_any_tag_prefix(output: &str) -> bool {
    output.lines().map(str::trim).any(|line| {
        line.starts_with("CONFIRMED:")
            || line.starts_with("MISSED:")
            || line.starts_with("FALSE-POSITIVE:")
    })
}
```
Skill dedup by tier priority — a user-persisted skill shadows a same-named builtin (`crates/harness-skills/src/store.rs:383-410`):
```rust
    pub fn deduplicate(&mut self) {
        let mut seen: HashMap<String, usize> = HashMap::new();
        let mut to_remove = Vec::new();

        for (idx, skill) in self.skills.iter().enumerate() {
            match seen.entry(skill.name.clone()) {
                std::collections::hash_map::Entry::Vacant(slot) => {
                    slot.insert(idx);
                }
                std::collections::hash_map::Entry::Occupied(mut slot) => {
                    let existing_idx = *slot.get();
                    let existing_priority = location_priority(self.skills[existing_idx].location);
                    let new_priority = location_priority(skill.location);
                    if new_priority > existing_priority {
                        to_remove.push(existing_idx);
                        *slot.get_mut() = idx;
                    } else {
                        to_remove.push(idx);
                    }
                }
            }
        }

        to_remove.sort_unstable();
        for idx in to_remove.into_iter().rev() {
            self.skills.remove(idx);
        }
    }
```
