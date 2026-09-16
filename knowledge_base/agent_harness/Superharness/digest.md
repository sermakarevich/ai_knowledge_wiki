> [[index|Wiki]] | [[summary|Summary]]

# superharness — Digest

The whole codebase at medium depth: every component's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-shared-contract-sqlite-state|Shared Contract and SQLite State]]

**In one sentence:** One per-project SQLite `state.db` (39 migrations, Pydantic-validated contract model) is the sole runtime authority, with all task/inbox/handoff writes funneled through typed DAO boundaries and canonical `state_reader` / `state_writer` paths while YAML survives only as export/backfill material.

- Local-first, one authoritative state: tasks, inbox rows, handoffs, decisions, failures, heartbeats, dispatch context all live in one SQLite DB, never a network service (`docs/ARCHITECTURE.md:12-20`).
- Schema is 39 ordered migrations (`src/superharness/engine/db.py:20`, `src/superharness/engine/db.py:1886-1926`); `init_db` tracks `schema_migrations` + `PRAGMA user_version` and heals additive-column drift via `_ADDITIVE_COLUMN_MANIFEST` (`src/superharness/engine/db.py:271-289`, `src/superharness/engine/db.py:346-389`).
- DB path resolves to `$XDG_STATE_HOME/superharness/<project-hash>/state.db`, overridable by `SUPERHARNESS_STATE_DIR`, with fail-closed `StateDatabaseConflictError` on split-brain roots (`src/superharness/utils/paths.py:135-165`, `docs/ARCHITECTURE.md:118-131`).
- Journal mode is WAL on local disk, PERSIST rollback journal on network filesystems, with stale `-wal`/`-shm` sidecar removal and `foreign_keys=ON` + busy timeout on every connection (`src/superharness/engine/db.py:89-107`, `src/superharness/engine/db.py:161-233`).
- Handoff writes are gated at the DAO edge: `phase` in `{plan, report}` (+ legacy `done`), `status` in task lifecycle enum + `{approved, plan_confirmed}`, else `BoundaryError` (`src/superharness/engine/handoffs_dao.py:14-50`).
- Event writes validate structurally (frozen dataclass with non-empty `kind` + `task_id`), raising `TypeError`/`ValueError` synchronously before queueing; background-writer failures stay warn-only (`src/superharness/engine/events.py:70-80`, `docs/ARCHITECTURE.md:81-91`).
- Dispatch prompt ingredients are content-addressed: `context_component` keyed by sha256, `dispatch_context` per dispatch, `dispatch_context_component` ordered join; `COMPONENT_TYPES` is a closed 5-value set (`src/superharness/engine/context_dao.py:16-32`, `src/superharness/engine/db.py:1839-1883`).
- Reads go through `state_reader` (SQLite direct in production, YAML auto-ingest only under pytest); writes go through `state_writer` (transition validation, contract lock, timestamps); `BoundaryError` (caller bug, re-raised) is distinguished from `StateError` (infrastructure, swallowed by best-effort paths) (`src/superharness/engine/state_reader.py:129-173`, `src/superharness/engine/state_writer.py:367-462`, `src/superharness/engine/state_errors.py:4-39`).

## 2. [[wiki/02-queue-delegation-lifecycle|Queue-Based Delegation and Lifecycle Rules]]

**In one sentence:** Delegation is a SQLite (Structured Query Language Lite, file-based database)-backed queue (`inbox` rows) fed by `inbox_enqueue`, claimed atomically by `inbox_dispatch`, supervised by `inbox_watch`, while task progress follows a strict status graph (`next_action.py`) plus a timeout reconciler (`lifecycle_rules.py`).

- Inbox rows are a priority queue with states `pending → launched → running/paused → done/failed/stale` (`src/superharness/engine/schemas.py:48-55`, `src/superharness/engine/inbox_dao.py:34`); `stopped` is written only via the session-stop hook path (`src/superharness/engine/inbox_dao.py:417-438`), not the `InboxStatus` enum (Application Programming Interface, the allowed value list).
- Enqueue inserts one `pending` row per (`task_id`, `target_agent`) and rejects duplicates while an active row exists (`src/superharness/engine/inbox_dao.py:37-60`); `inbox_enqueue` additionally blocks non-dispatchable task statuses by workflow (`src/superharness/commands/inbox_enqueue.py:158-184`).
- Dispatch claims with a single atomic `UPDATE ... WHERE id = (SELECT ... WHERE status='pending' ...)` so concurrent watchers cannot double-claim (`src/superharness/engine/inbox_dao.py:144-176`, wrapped at `src/superharness/commands/inbox_dispatch.py:740-774`).
- Watch runs single-cycle (launchd (macOS background scheduler)/systemd (Linux background scheduler)) or foreground poll loop (`src/superharness/commands/inbox_watch.py:5381-5460`), writes a watcher heartbeat each tick (`src/superharness/commands/inbox_watch.py:610-639`), and reconciles zombies, stuck inputs, orphaned discussion inboxes, and consensus closes (`src/superharness/commands/inbox_watch.py:3673-3684`, `src/superharness/commands/inbox_watch.py:5210-5235`, `src/superharness/commands/inbox_watch.py:5250-5288`).
- Task lifecycle is a closed graph: `VALID_STATUSES` derives from `ALL_STATUSES` (`src/superharness/engine/tasks_dao.py:19`, `src/superharness/engine/next_action.py:19-38`), legal edges live in `_MAPPING` and are enforced by `validate_status_transition` (`src/superharness/engine/next_action.py:53-150`, `src/superharness/engine/next_action.py:371-392`).
- Auto-mode (non-interactive operation governed by `profile.yaml autonomy`, e.g. `ai_driven`) auto-closes reviews, auto-retries failures, and auto-archives/fails timed-out states via one rule table plus deadline/idle/ceiling checks (`src/superharness/commands/inbox_watch.py:26-29`, `src/superharness/commands/inbox_watch.py:1091-1093`, `src/superharness/engine/lifecycle_rules.py:47-164`, `src/superharness/engine/lifecycle_rules.py:394-418`).
- Subtasks do not dispatch independently; parent close is gated on `done/cancelled` and results aggregate to `report_ready` (all done) or `failed` (any failed) (`src/superharness/engine/subtask.py:34-50`, `src/superharness/engine/subtask_gate.py:45-68`, `src/superharness/engine/subtask_aggregator.py:99-104`).

## 3. [[wiki/03-worker-restart-crash-recovery|Worker Restart and Crash Recovery]]

**In one sentence:** crashed or timed-out workers are detected via heartbeats and stale inbox rows, their partial state survives in append-only handoffs plus ledger plus git-stash checkpoints plus auto-flush YAML, and the next dispatch respawns with that full context while durable counters cap retry loops.

- Handoffs carry two phases, `plan` and `report`, with task status carried alongside — boundary validation is the crash-safety contract (`src/superharness/engine/handoffs_dao.py:14`, `src/superharness/engine/handoffs_dao.py:29`).
- Both handoff and ledger tables are append-only; nothing is updated or deleted in place (`src/superharness/engine/handoffs_dao.py:88`, `src/superharness/engine/ledger_dao.py:57`).
- Checkpoints are git-stash entries tagged `shux-checkpoint:<task-id>`, not files (`src/superharness/guard/checkpoint.py:9`).
- Expiring tasks are auto-flushed to `.superharness/handoffs/<id>-auto-flush-<date>.yaml` on every watcher tick (`src/superharness/engine/session_flush.py:50`, `src/superharness/commands/inbox_watch.py:3105`).
- Session end is handled by stop/exit hooks that park active inbox rows as `stopped` and clear the PID (`src/superharness/engine/inbox_dao.py:417`).
- Crash recovery is a pipeline: heartbeat zombie-marking → `inbox recover` → watcher auto-recover with reroute → `inbox gc` reconcile, all audited in the ledger (`src/superharness/engine/heartbeat_dao.py:141`, `src/superharness/commands/inbox_recover.py:68`, `src/superharness/commands/inbox_gc.py:26`).
- `recovery_count` lives in its own inbox column so failure rewrites cannot wipe it; retries are capped (`_RECOVERY_MAX=2`, absolute `max_retries=12`, identical-error threshold `4`) (`src/superharness/commands/inbox_watch.py:1594`, `tests/unit/test_recovery_counter_durable.py:27`).
- A respawned agent receives handoff history plus recent ledger plus the hashed dispatch prompt components (system, task instructions, rules, vault block) (`src/superharness/engine/handoffs_dao.py:119`, `src/superharness/engine/context_dao.py:16`, `src/superharness/engine/ledger_dao.py:79`).

## 4. [[wiki/04-conflict-resolution-gates|Conflict Resolution and Lifecycle Gates]]

**In one sentence:** Superharness prevents agent conflicts with per-agent git worktrees plus hook-layer write/push guards, and prevents premature progress with dispatch-time gates (status, preflight, policy, plan quality) and close-time gates (status, subtask resolution, verification, ownership).

- scope-guard does **not** compare agents' file sets against each other; it is a PreToolUse hook on `Write|Edit` that deny-blocks secrets/keys and warn-asks on system paths (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:1-8`, `src/superharness/adapters/claude-code/hooks/hooks.json:15-25`).
- Overlap prevention between concurrent agents comes from **worktree isolation** (one git worktree per dispatch slot), not from scope-guard (`src/superharness/engine/worktree_ops.py:38-50`, `src/superharness/engine/parallel_dispatch.py:200-215`).
- Branch guard blocks pushes to `main`/`master` and bare `--force`, resolving refspecs by tokenizing (not regex over the whole command) (`src/superharness/adapters/claude-code/hooks/branch_guard.py:63-102`, `src/superharness/adapters/claude-code/hooks/branch_guard.py:138-159`).
- Dispatch is gated in order: workflow status gate, then preflight (`src/superharness/commands/delegate.py:912-946`, `src/superharness/commands/delegate.py:952-977`).
- Preflight hard-blocks on unmet dependencies and unmet `requires:`/mandate capabilities; spec/TDD/acceptance-criteria gaps only warn (`src/superharness/engine/preflight.py:197-208`, `src/superharness/engine/preflight.py:355-459`, `src/superharness/engine/preflight.py:648-658`).
- `close` requires status `report_ready`/`review_passed`, zero blocking subtasks, `verified=true`, and matching owner — each bypassable only by an explicit flag that is ledger-logged (`src/superharness/commands/close.py:57-58`, `src/superharness/commands/close.py:123-168`, `src/superharness/commands/close.py:180-198`).
- The subtask gate is off by default; profile flag wins, task flag can only tighten (`src/superharness/engine/subtask_gate.py:3-10`, `src/superharness/engine/subtask_gate.py:51-58`).
- Enforcement parity is partial and pinned by contract test: hook trees must stay byte-identical and CI/pre-commit gates must not drift, while engine gates are re-checked at each entry point (CLI `close` + `task`, watcher, MCP approval) rather than in one choke point (`tests/contract/test_enforcement_parity.py:233-261`, `src/superharness/commands/close.py:139-157`, `src/superharness/commands/task.py:739-749`).

## 5. [[wiki/05-workflow-abstraction|Workflow Abstraction]]

**In one sentence:** The workflow layer is a verb surface (`enqueue`/`dispatch`/`watch`/`talk`/`delegate`/`discuss`) over a SQLite-backed task state machine with per-workflow dispatch gates, orchestrator routing, three fanout executors, quorum-gated discussions, classifier-driven auto-dispatch, and YAML module hooks.

- Verbs map 1:1 to commands: `enqueue` writes an inbox row (`src/superharness/commands/inbox_enqueue.py:206`), `dispatch` claims and launches one item (`src/superharness/commands/inbox_dispatch.py:777`), `watch` loops dispatch across agents (`src/superharness/commands/inbox_watch.py:524`), `talk`/`delegate`/`discuss` are conversation, launch, and consensus entry points (`src/superharness/commands/talk.py:222`, `src/superharness/commands/delegate.py:793`, `src/superharness/commands/discuss.py:844`).
- There is no `shux queue` command; "queue" is only the `auto-dispatch` log verb for a task selected for enqueue (`src/superharness/commands/auto_dispatch.py:346`).
- Dispatch is workflow-gated, not status-global: `infer_workflow` defaults to `implementation` (`src/superharness/engine/next_action.py:217`), `allowed_statuses_for_workflow` returns a different dispatchable set per workflow (`src/superharness/engine/next_action.py:233`), and `plan_only_allowed_statuses` additionally admits `todo`/`plan_proposed` for implementation planning (`src/superharness/engine/next_action.py:271`).
- Three fanouts differ by trigger and aggregation: `parallel_dispatch` runs N isolated worktrees with no judge (`src/superharness/engine/parallel_dispatch.py:173`), `swarm` adds a reviewer vote with cheapest-slot fallback (`src/superharness/engine/swarm.py:106`), `ReviewFanout` runs read-only per-task reviewers and AND-merges verdicts (`src/superharness/engine/review_fanout.py:43`).
- Discussions are round-based with a quorum consensus gate (`agree`/`consensus`/`abstain` pass; `disagree`/`partial` block) (`src/superharness/engine/discussion.py:252`), advanced or closed by `cmd_advance` (`src/superharness/engine/discussion.py:559`), re-enqueued by `discussion_dispatch.dispatch` (`src/superharness/commands/discussion_dispatch.py:384`).
- Auto-dispatch scores adapters by keyword overlap and falls back to owner/`claude-code` (`src/superharness/engine/smart_dispatch.py:90`), splits roles into worktree/payload profiles (`src/superharness/engine/dispatch_profile.py:56`), and ships dry-run/print-only as its headless modes (`src/superharness/commands/auto_dispatch.py:386`, `src/superharness/commands/delegate.py:701`).
- Modules are YAML hook packs: templates live in `module_templates/` (`src/superharness/modules/registry.py:14`), `load_modules` reads `.superharness/modules/*.yaml` and skips disabled entries (`src/superharness/modules/loader.py:63`), `run_hooks(event, context, project_dir)` fires matching hooks (`src/superharness/modules/runner.py:57`).

## 6. [[wiki/06-multi-harness-adapters|Multi-Harness Support]]

**In one sentence:** superharness dispatches work to five coding-agent runtimes (Claude Code, Codex CLI, Gemini CLI, opencode, Pi) through one `Harness` protocol (a shared interface, i.e. a contract every adapter must implement), YAML manifests (config files describing each adapter) plus a Python adapter registry (lookup/validation code), and per-harness launcher scripts — with golden parity tests proving adapter argv is byte-identical to the legacy path.

- The `Harness` protocol (`src/superharness/harnesses/base.py:33-51`) requires only `build_invocation(task, project_dir, non_interactive) -> Invocation`; model discovery via `discover_models(auth_mode)` defaults to no-op `[]`.
- `Invocation` (`src/superharness/harnesses/base.py:16-30`) is a frozen dataclass (immutable, i.e. cannot be changed after creation) with `argv: tuple`, `env: dict`, `cwd: str`; tuple storage blocks both reassignment and in-place mutation.
- Two registries cooperate: `harnesses/__init__.py` maps runtime name → live `Harness` object (`register`/`get_harness`), while `engine/adapter_registry.py:190-283` maps adapter name → YAML manifest → launcher-script path, validation, and model tiers.
- Every manifest declares `name, version, type (native|external), launcher_script, capabilities, model_tiers, requires, validation` (`src/superharness/engine/adapter_registry.py:103-128`); new-schema tiers add `preferred / accept / auth_compat / capability_tags` (`src/superharness/adapter_manifests/codex-cli.yaml:23-43`).
- Claude is the special case: `ClaudeHarness.build_invocation` (`src/superharness/harnesses/claude.py:28-61`) builds argv by hand and never prefixes the model, while codex/gemini/opencode/pi all delegate to `build_generic_invocation` (`src/superharness/harnesses/base.py:93-132`), which applies provider/model prefixing.
- Discovery differs per harness: claude/codex/gemini probe via the manifest accept chain (`src/superharness/harnesses/base.py:64-90`); opencode runs `opencode models` natively (`src/superharness/harnesses/opencode.py:57-62`); Pi parses its offline `pi --offline ... --list-models` table (`src/superharness/harnesses/pi.py:15-23`).
- `shux adapter-payload` (`src/superharness/commands/adapter_payload.py:680-709`) emits one stable JSON snapshot (schema `1.4`) with tasks, edges, ledger, failures, decisions, inbox, agent pulse, rules, artifacts, heartbeats for external consumers such as Morpheme.
- Parity tests (`tests/unit/test_harness_registry.py:39-71`, `tests/unit/test_harness_adapters.py:37-123`) assert adapter argv tuples equal golden values captured from the live legacy `delegate.py::_launch_agent` path, including prompt-as-single-element injection safety.

## 7. [[wiki/07-watchdog-telemetry-benchmark|Watchdog, Telemetry, Skills, and Benchmarks]]

**In one sentence:** Stuck work is killed by a dual event-driven watchdog (`idle-timeout` + `absolute-ceiling`), liveness is decided from DB (Structured Query Language database) heartbeats, all activity lands in typed telemetry events with opt-in Langfuse (external observability backend) export, and completed work feeds a skill library plus a cost leaderboard.

- **Watchdog A (idle timeout)** fails a task when minutes-since-last-`events`-row >= `idle_timeout_minutes` (`src/superharness/engine/lifecycle_rules.py:505`); **Watchdog B (absolute ceiling)** fails it when total age since `in_progress_at` >= `absolute_ceiling_minutes` even with fresh events (`src/superharness/engine/lifecycle_rules.py:485`).
- **Fresh events spare the task**: with event history present, idle/ceiling semantics fully replace the legacy `deadline_minutes` check, so an active task past its own deadline survives (`src/superharness/engine/lifecycle_rules.py:525`, `tests/unit/test_dual_watchdog.py:66`); with both keys unset behavior is byte-identical to legacy (`src/superharness/engine/lifecycle_rules.py:438`, `tests/unit/test_dual_watchdog.py:170`).
- **Liveness is one pure function**: `is_fresh(ts, ttl)` returns True only if the ISO-8601 (standard text date format) timestamp parses and is within TTL, default `WATCHER_TTL_SECONDS = 90`, never raising (`src/superharness/engine/liveness.py:18`, `src/superharness/engine/liveness.py:23`); the watcher stamps `agent_id="watcher"` each cycle via `touch_watcher` (`src/superharness/engine/liveness.py:40`).
- **Typed events table + fire-and-forget emitter**: `events(ts, kind, task_id, payload_json)` created in migration v31 (`src/superharness/engine/db.py:1306`); `emit()` validates synchronously then queues to a daemon background thread whose DB failures are warn-only (`src/superharness/engine/events.py:158`, `src/superharness/engine/events.py:199`); unconfigured `emit()` is a silent no-op until `configure(project_dir)` (`src/superharness/engine/events.py:187`).
- **Transcript progress feeds the watchdog** via persisted byte-offset cursors (`dispatch_cursors`, migration v32, `src/superharness/engine/db.py:1322`): `tail_step` reads only new complete lines since the stored offset, emits one `transcript_progress` event per tool-use line, resets to 0 on rotation/truncation (`src/superharness/engine/transcript_tail.py:162`).
- **Langfuse is opt-in and failure-isolated**: enabled only by `SUPERHARNESS_LANGFUSE_ENABLED` truthy plus credentials, `DO_NOT_TRACK` truthy is an absolute opt-out (`src/superharness/engine/langfuse_telemetry.py:51`, `src/superharness/engine/langfuse_telemetry.py:68`); dispatches export one pseudonymized event (`task_id_hash`, no content) named `superharness.dispatch.completed` (`src/superharness/engine/langfuse_telemetry.py:143`).
- **Skill flow is extract → persist → inject**: `record_skill` on task completion dedupes by `task_id` into `.superharness/skills.yaml` (`src/superharness/engine/skill_extractor.py:291`, `src/superharness/commands/task.py:769`); `get_skill_hints` keyword-searches top-3 into dispatch context (`src/superharness/engine/skill_extractor.py:360`, `src/superharness/engine/context_hint.py:166`); `skill_usage` table tracks per-skill uses/success-rate best-effort (`src/superharness/engine/skill_metrics.py:16`, `src/superharness/engine/skill_metrics.py:58`).
- **Benchmark is a JSONL (newline-delimited JSON log) leaderboard**: `record_dispatch` appends `BenchmarkRecord(task_id, agent, outcome, duration, cost, model, slot, fanout)` to `benchmark.jsonl` and also triggers the Langfuse export (`src/superharness/engine/benchmark.py:52`); `aggregate` ranks per-task stats by total cost descending (`src/superharness/engine/benchmark.py:139`); `shux benchmark --top 20 --agents/--models` renders it plus a 7-day per-model cost/budget view (`src/superharness/commands/benchmark.py:27`, `src/superharness/commands/benchmark.py:61`).

## 8. [[wiki/targeted|Targeted Analysis for Fleet]]

Fleet question set answered from wiki/01-07 with file:line citations; full detail lives in the page.

- Q1 design principles: local-first, one SQLite `state.db` authority, typed DAO boundaries, explicit status graph, agent-neutral adapters, fail-closed split-brain handling.
- Q2 restart handling: heartbeat/zombie detection → handoff+ledger+stash-checkpoint+auto-flush survival → respawn bundle → durable retry ceilings.
- Q3 conflict resolution: worktree isolation (not file-set diffing) + hook guards + dispatch/close gates + enforcement parity tests.
- Q4 workflow abstraction: verb surface over the status graph with per-workflow gates, three fanout executors, quorum discussions, auto-dispatch, YAML modules.
- Q5 multi-harness: one `Harness` protocol + dual registries + YAML manifests + launcher shims + golden parity tests.
- Q6 fleet borrows: dual watchdog, typed events, skill loop, benchmark leaderboard, atomic inbox claim, recovery ceilings, watcher singleton lease, content-addressed dispatch context — see [[wiki/targeted|the page]] for file:line per item.

## The system in five moves

1. Operator delegates work that `inbox_enqueue` validates and queues as inbox rows.
2. `inbox_dispatch` atomically claims the next item and the harness adapter launches the agent in an isolated worktree.
3. Watchdog, heartbeats, and typed events supervise liveness and kill stuck work via idle and ceiling rules.
4. Handoffs, ledger, checkpoints, and auto-flush preserve partial state so a respawn continues with full context.
5. Lifecycle gates and close rules verify, approve, and archive finished work while retry ceilings prevent runaway loops.
6. Benchmark, skill extraction, and telemetry record cost and lessons for the next dispatch.
