---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: superharness

Answer from memory before opening any answer.

### Q1. What values does the handoff write boundary accept, and what happens on a bad value versus a database (DB, storage layer) outage?
> [!tip]- Answer
> Phase must be `plan` or `report` (plus legacy `done`), and status must be in the task lifecycle enum (a fixed list of allowed task states) plus `approved`/`plan_confirmed`, else the write raises `BoundaryError` before touching storage. `BoundaryError` means caller bug and is re-raised, while any other storage failure becomes `StateError` (infrastructure fault) and is swallowed on best-effort paths so telemetry never breaks the caller. See [[wiki/01-shared-contract-sqlite-state|Shared Contract and SQLite State]].

### Q2. What are the inbox row states, and how does dispatch claim one row without double-claiming under concurrent watchers?
> [!tip]- Answer
> States are `pending → launched → running/paused → done/failed/stale`, with `stopped` written only via the session-stop hook path, not the `InboxStatus` enum (the allowed value list). Dispatch claims with a single atomic `UPDATE ... WHERE id = (SELECT ... WHERE status='pending' ORDER BY priority DESC, created_at ASC)` so only one watcher wins the row. Enqueue additionally dedups on active `(task_id, target_agent)` via a partial unique index (a rule blocking duplicates only for non-terminal rows). See [[wiki/02-queue-delegation-lifecycle|Queue-Based Delegation and Lifecycle Rules]].

### Q3. Why are handoff and ledger writes append-only, and what breaks if a retry overwrites them in place?
> [!tip]- Answer
> Both tables only `INSERT` new rows and never update or delete, so a crashed worker's partial `plan`/`report` handoffs plus the retry/escalation ledger trail survive for the next dispatch. Overwriting in place would destroy the history a respawned agent needs (handoff chain, recent ledger, hashed prompt components) and hide the identical-error pattern the retry ceilings detect. The durable `recovery_count` column exists for the same reason: failure rewrites must not wipe the retry count. See [[wiki/03-worker-restart-crash-recovery|Worker Restart and Crash Recovery]].

### Q4. What does scope-guard actually check, and what breaks if you remove worktree isolation and rely on scope-guard alone?
> [!tip]- Answer
> Scope-guard is a PreToolUse hook (a check that runs before the agent edits files) on `Write|Edit` that deny-blocks secrets/keys and warn-asks on system paths — it never compares one agent's file set against another's. Removing per-dispatch git worktrees (isolated directory copies, one branch each) removes the real overlap prevention, so concurrent agents would edit and commit over the same files with no structural separation. See [[wiki/04-conflict-resolution-gates|Conflict Resolution and Lifecycle Gates]].

### Q5. How do the three fanout executors differ in trigger and result merging?
> [!tip]- Answer
> `parallel_dispatch` runs N isolated worktrees with no judge — the caller merges results itself. `swarm` adds a reviewer vote parsed from `WINNER:`/`REASONING:` lines, falling back to the cheapest finished slot on an invalid pick. `ReviewFanout` runs read-only per-task reviewers and AND-merges verdicts (all must pass). See [[wiki/05-workflow-abstraction|Workflow Abstraction]].

### Q6. What is the `Harness` protocol (the shared interface every adapter implements), and what does `build_invocation` return?
> [!tip]- Answer
> The protocol requires only `build_invocation(task, project_dir, non_interactive) -> Invocation`, with model discovery via `discover_models(auth_mode)` defaulting to an empty list. `Invocation` is a frozen dataclass (immutable, unchangeable after creation) holding `argv` as a tuple, `env` dict, and `cwd` string, so adapter output is an exact ready-to-spawn subprocess (operating-system process) description. Claude builds argv by hand without a model prefix; the other four share the generic builder with provider prefixing. See [[wiki/06-multi-harness-adapters|Multi-Harness Support]].

### Q7. What are the two watchdog conditions, and what does each measure?
> [!tip]- Answer
> Watchdog A (idle timeout) fails a task when minutes since the last `events`-table row reach `idle_timeout_minutes` (wedged, no output). Watchdog B (absolute ceiling) fails it when total age since `in_progress_at` reaches `absolute_ceiling_minutes`, even with fresh events (runaway, slow but never finishing). Both are opt-in profile keys defaulting to 0 = disabled, and tasks with no event rows fall back to the legacy `deadline_minutes` path. See [[wiki/07-watchdog-telemetry-benchmark|Watchdog, Telemetry, Skills, and Benchmarks]].

### Q8. Why a dual watchdog instead of a single deadline, and what goes wrong with only one?
> [!tip]- Answer
> A single deadline from dispatch time cannot tell "slow but progressing" from "wedged with no output", so it either kills active work past its deadline or lets silent workers burn budget forever. Fresh events therefore spare a past-deadline task under the dual scheme, while the ceiling still catches a task that emits events but never converges. With both keys unset behavior stays byte-identical to the legacy deadline check. See [[wiki/07-watchdog-telemetry-benchmark|Watchdog, Telemetry, Skills, and Benchmarks]].

### Q9. How would you add a new harness adapter, and how would you apply the handoff pattern to fleet's coder workers?
> [!tip]- Answer
> Implement `build_invocation` (+ optional `discover_models`), register the live object in `harnesses/__init__.py`, ship a YAML manifest (config file: name, version, type, launcher script, capabilities, model tiers, requirements) plus a `scripts/delegate-to-<name>.sh` launcher, and pin argv equality with a golden parity test. For fleet, give each coder worker append-only `plan`/`report` handoffs plus an audit ledger so a crashed worker's respawn receives handoff history, ledger tail, and hashed prompt components instead of restarting blind. See [[wiki/targeted|Targeted Analysis: Superharness for Fleet]].

### Q10. Superharness closes the loop (spawns and supervises workers) while Beads only tracks work — is the extra state layer worth it, given the 5594-line watcher god module and the silent-death history?
> [!tip]- Answer
> The supervision buys principled kill/retry signals (dual watchdog, zombie reaping, retry ceilings with e2e-tested runaway fuse) that a pure tracker cannot give, at the cost of one risky god module (`inbox_watch.py`) that concentrates the watcher loop, reconcilers, auto-approval, and recovery in a single change-risky file. The documented 19+-hour silent outage shows the layer itself needs supervising (singleton lease plus daemon monitor plus launchd self-heal), so adopt it only with that three-layer supervision intact. See [[wiki/02-queue-delegation-lifecycle|Queue-Based Delegation and Lifecycle Rules]].
