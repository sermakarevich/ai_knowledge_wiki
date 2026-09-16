> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Targeted Analysis: Superharness for Fleet
Fleet question set answered from wiki/01-07 (compressed survey of the superharness repo),
with file:line citations reusable for deeper spot-checks in the clone.

## Q1. Design principles (shared contract, queue-based delegation, lifecycle rules)?
Superharness is local-first with one per-project SQLite (Structured Query Language Lite, file-based database) `state.db` as the sole runtime authority; all writes go through typed DAO (Data Access Object, validated write layer) boundaries and a strict status graph.
Six principles from `docs/ARCHITECTURE.md:10-20`: local-first, one authoritative state, explicit state transitions, agent-neutral adapters, least surprise for operators, compatibility without split brain (two writers diverging).
- One DB holds tasks, inbox rows, handoffs, decisions, failures, heartbeats, dispatch context — never a network service (`docs/ARCHITECTURE.md:12-20`).
- Schema is 39 ordered migrations under per-migration SAVEPOINTs; `init_db` tracks `schema_migrations` + `PRAGMA user_version` and heals additive-column drift (`src/superharness/engine/db.py:20`, `src/superharness/engine/db.py:1886-1926`, `src/superharness/engine/db.py:271-289`).
- DB path is `$XDG_STATE_HOME/superharness/<12-char-project-hash>/state.db`, overridable by `SUPERHARNESS_STATE_DIR`; conflicting roots raise fail-closed `StateDatabaseConflictError` (`src/superharness/utils/paths.py:135-165`, `docs/ARCHITECTURE.md:118-131`).
- WAL (Write-Ahead Log) journal on local disk, PERSIST rollback journal on network filesystems, stale sidecar cleanup, `foreign_keys=ON` + busy timeout per connection (`src/superharness/engine/db.py:89-107`, `src/superharness/engine/db.py:161-233`).
- Typed write boundaries fail loudly at the DAO edge: handoff phase in `{plan, report}` (+ legacy `{done}`), status in task enum + `{approved, plan_confirmed}`, else `BoundaryError` (`src/superharness/engine/handoffs_dao.py:14-50`); events validate frozen-dataclass shape before queueing (`src/superharness/engine/events.py:70-80`).
- Canonical paths: `state_reader` for reads, `state_writer` for writes (transition validation, contract lock, timestamps); `BoundaryError` (caller bug, re-raised) vs `StateError` (infrastructure fault, swallowed best-effort) (`src/superharness/engine/state_reader.py:129-173`, `src/superharness/engine/state_writer.py:367-462`, `src/superharness/engine/state_errors.py:4-39`).
- Contract lock: `plan_approved` snapshots acceptance criteria + TDD (Test-Driven Development, write-the-test-first practice); `review_failed → plan_proposed` clears it (`src/superharness/engine/state_writer.py:155-170`).
- Inbox rows are a priority queue `pending → launched → running/paused → done/failed/stale`; enqueue dedups active `(task_id, target_agent)`, dispatch claims atomically (`src/superharness/engine/inbox_dao.py:34-60`, `src/superharness/engine/inbox_dao.py:161-176`).
- Timeout automation is a data-driven `LIFECYCLE_RULES` table (paused 30 m → fail, review_requested 120 m → revert, in_progress 180 m → archive, …) with profile overrides (`src/superharness/engine/lifecycle_rules.py:47-164`, `src/superharness/engine/lifecycle_rules.py:205-211`).
- CLI (Command-Line Interface) is thin Click entry (`src/superharness/cli.py`); per-command validation in `commands/`; state machine + DAOs + lifecycle in `engine/` (`docs/ARCHITECTURE.md:37-55`).

## Q2. Worker restart handling (crash recovery, handoff/ledger state, respawn with context, checkpoints)?
Crashed workers are found via heartbeats and stale inbox rows; partial work survives in append-only handoffs + ledger + git-stash checkpoints + auto-flush YAML (human-readable config format), and the next dispatch respawns with that full bundle while durable counters cap retry loops.
- Handoff phases are closed `{plan, report}` (+ legacy `done`); `append()` is `INSERT ... RETURNING`, never update/delete, with `<private>` stripping (`src/superharness/engine/handoffs_dao.py:14-50`, `src/superharness/engine/handoffs_dao.py:76-89`).
- Ledger is append-only `(task_id, agent, action, details)`; dangling `task_id` degrades to NULL; `decision_log()` never raises (`src/superharness/engine/ledger_dao.py:25-54`, `src/superharness/engine/ledger_dao.py:120`).
- Checkpoints are git-stash entries `shux-checkpoint:<task-id>` (`snapshot`/`rollback`/`prune_old`), not files (`src/superharness/guard/checkpoint.py:9-60`).
- Expiring tasks auto-flush to `.superharness/handoffs/<id>-auto-flush-<date>.yaml` every watcher tick (`src/superharness/engine/session_flush.py:50`, `src/superharness/commands/inbox_watch.py:3105`); stop/exit hooks park active rows as `stopped` + clear PID (`src/superharness/engine/inbox_dao.py:417-438`).
- Recovery pipeline: zombie-marking after 120 s silence (`src/superharness/engine/heartbeat_dao.py:141`) → `inbox recover` (`--timeout-minutes 20`, `stale|retry`, `src/superharness/commands/inbox_recover.py:68`) → watcher auto-recover with fallback-agent reroute → `inbox gc` reconcile (`src/superharness/commands/inbox_gc.py:26-84`); operator loop reaps zombies, emits `process_recovery` per restart (`src/superharness/engine/operator.py:370-421`).
- Retry ceilings: `recovery_count` in its own column (`_RECOVERY_MAX=2`, absolute `max_retries=12`, identical-error threshold 4); exhausted failures escalate to `waiting_input` (`src/superharness/commands/inbox_watch.py:1594-2063`, `tests/e2e/test_runaway_recovery_e2e.py:65-95`).
- Heartbeat durability: SQLite primary, YAML crash-dump on SQLite failure, reads prefer whichever is newer; watcher singleton lease with steal-if-stale (`src/superharness/engine/heartbeat_contract.py:70-217`, `src/superharness/engine/watcher_singleton.py:21-100`).
- Transcript progress feeds the watchdog via persisted byte-offset cursors, one `transcript_progress` event per tool-use line (`src/superharness/engine/transcript_tail.py:97-162`).
- Respawn bundle in authority order: `get_history()` + `get_latest(task, phase)` (`src/superharness/engine/handoffs_dao.py:119-172`), generated compaction doc (`src/superharness/engine/handoff_generator.py:65-113`), ledger tail (`src/superharness/engine/ledger_dao.py:79`), sha256 content-addressed dispatch components (`src/superharness/engine/context_dao.py:16-80`).

## Q3. Conflict resolution (file-overlap prevention, task lifecycle gates todo→done)?
Overlap between concurrent agents is prevented structurally by per-dispatch git worktrees (isolated directory copies), not by comparing file sets; hook guards block secrets and protected-branch pushes, while dispatch-time and close-time gates block premature progress.
- scope-guard is a PreToolUse hook on `Write|Edit` that deny-blocks secrets (`*.env`, `*credentials*`, `*.pem`, `*.key`, `*/.ssh/*`, tfvars) and warn-asks on system paths — never compares agents' file sets (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:27-79`, `src/superharness/adapters/claude-code/hooks/hooks.json:15-25`).
- Real isolation: one branch + worktree per parallel slot, `.superharness/` symlinked in, worktrees removed in `finally` and on close after realpath containment check (`src/superharness/engine/worktree_ops.py:23-79`, `src/superharness/engine/parallel_dispatch.py:200-215`, `src/superharness/commands/close.py:289-330`).
- Branch guard blocks pushes to `main`/`master` and bare `--force` by tokenizing refspecs (not whole-string regex), resolving `src:dst` and bare-push HEAD (`src/superharness/adapters/claude-code/hooks/branch_guard.py:63-159`).
- Dispatch gates in order: workflow status gate (implementation needs `plan_approved`/`in_progress`; `todo`/`plan_proposed` blocked without `--plan-only`) then preflight; blocks log `gate_block`, exit permanent (`src/superharness/commands/delegate.py:912-977`).
- Preflight hard-blocks on unmet `blocked_by` deps and missing `requires:`/mandate capabilities; spec/TDD/acceptance gaps only warn (`src/superharness/engine/preflight.py:197-208`, `src/superharness/engine/preflight.py:355-459`, `src/superharness/engine/preflight.py:648-658`).
- Loop policy blocks on `loop_detected` or cost overrun, invoked on the watcher path (`src/superharness/engine/policy_gate.py:9-34`, `src/superharness/commands/inbox_watch.py:3210-3232`).
- MCP (Model Context Protocol, tool-permission layer) approval is risk-based: low-risk auto-approves, medium/high raise `ApprovalPending`; discussion approval writes `approval_gate.*` (`src/superharness/mcp/approval.py:101-105`, `src/superharness/engine/discuss.py:238-291`).
- Close gates (`src/superharness/commands/close.py:57-68`, `src/superharness/commands/close.py:115-198`): owner match, status in `{report_ready, review_passed}`, zero blocking subtasks (gate off by default; profile flag wins, `src/superharness/engine/subtask_gate.py:51-58`), `verified=true` — each bypassable only by an explicit ledger-logged flag.
- Parity pinned by contract test (hook trees byte-identical, CI/pre-commit gates no drift); engine gates re-checked at each entry point, not one choke point (`tests/contract/test_enforcement_parity.py:233-261`).

## Q4. Workflow abstraction? How implemented (contracts, TDD blocks, queue/enqueue/dispatch/watch, fanout/swarm modes)?
The workflow layer is a verb surface (`enqueue`/`dispatch`/`watch`/`talk`/`delegate`/`discuss`) over the SQLite task state machine, with per-workflow dispatch gates, an orchestrator router, three fanout executors, quorum-gated discussions, classifier-driven auto-dispatch, and YAML module hooks.
- Verbs map 1:1: `enqueue` writes one inbox row (`src/superharness/commands/inbox_enqueue.py:206`), `dispatch` claims + launches one item (`src/superharness/commands/inbox_dispatch.py:777-866`), `watch` loops dispatch per agent with heartbeat + reconcilers (`src/superharness/commands/inbox_watch.py:5381-5470`).
- Status graph: `ALL_STATUSES` + `TERMINAL_STATUSES={done, failed, stopped}`; legal edges in `_MAPPING` enforced by `validate_status_transition` (`src/superharness/engine/next_action.py:19-150`, `src/superharness/engine/next_action.py:371-392`).
- Dispatch is workflow-gated: `infer_workflow` defaults to `implementation`; `allowed_statuses_for_workflow` differs per workflow; `plan_only_allowed_statuses` admits `todo`/`plan_proposed` for planning (`src/superharness/engine/next_action.py:217-287`).
- TDD/plan-quality blocks auto-approval via `validate_plan`: missing `tdd.{red,green,refactor}`, placeholder markers, missing risks, zero-overlap acceptance criteria (`src/superharness/engine/plan_validator.py:30-111`).
- Orchestrator: `route` returns owner+tier+effort+decompose in one model call; model chain tries Claude/Codex/Gemini/opencode/Pi quality-weighted with per-pair success recording
  (`src/superharness/engine/orchestrator.py:173-479`); policy via `shux workflow` into `.superharness/profile.yaml` (`src/superharness/commands/workflow_cmd.py:27-43`).
- Three fanouts: `parallel_dispatch` = N isolated worktrees, no judge, caller merges (`src/superharness/engine/parallel_dispatch.py:173-247`); `swarm` adds reviewer `WINNER:`/`REASONING:` vote with cheapest-slot fallback (`src/superharness/engine/swarm.py:46-270`); `ReviewFanout` = read-only per-task reviewers, AND-merge (`src/superharness/engine/review_fanout.py:43-110`).
- Discussions round-based with quorum consensus (`agree`/`consensus`/`abstain` pass; `disagree`/`partial` block; n-1 of n for n>2); `cmd_advance` advances/closes; dispatcher re-enqueues only pending agents with budget left (`src/superharness/engine/discussion.py:252-361`, `src/superharness/engine/discussion.py:559`, `src/superharness/commands/discussion_dispatch.py:384-546`).
- Subtasks are planning artifacts, not independently dispatched; parent close gated on `done/cancelled`, results aggregate to `report_ready`/`failed` (`src/superharness/engine/subtask_gate.py:45-68`, `src/superharness/engine/subtask_aggregator.py:48-107`).
- `talk` sends session-addressed messages as `partial`-verdict rounds (never auto-consensus) up to `MAX_ROUNDS = 99` (`src/superharness/commands/talk.py:50-235`).
- Auto-dispatch scans `todo` only, skips unresolved `blocked_by`, keyword-overlap agent scoring with owner/`claude-code` fallback, plan-only default for implementation,
  `DispatchProfile.for_role` shaping, `--dry-run`/`--print-only` headless modes (`src/superharness/commands/auto_dispatch.py:45-346`, `src/superharness/engine/smart_dispatch.py:74-131`, `src/superharness/engine/dispatch_profile.py:56`).
- Modules are YAML hook packs: templates in `module_templates/`, `load_modules` reads `.superharness/modules/*.yaml`, `run_hooks(event, context)` fires matches (`src/superharness/modules/registry.py:14-29`, `src/superharness/modules/loader.py:63`, `src/superharness/modules/runner.py:57`).

## Q5. Multi-harness support (claude/codex/gemini/opencode)? How implemented (Harness protocol + adapter registry — cite files)?
Five runtimes (Claude Code, Codex CLI, Gemini CLI, opencode, Pi) hang off one `Harness` protocol (shared interface every adapter implements) plus a Python adapter registry and YAML manifests with per-harness launcher scripts; parity tests prove adapter argv byte-identical to the legacy launch path.
- Protocol (`src/superharness/harnesses/base.py:33-51`): only required method is `build_invocation(task, project_dir, non_interactive) -> Invocation`; `discover_models(auth_mode)` defaults to `[]`.
- `Invocation` is a frozen dataclass (immutable after creation): `argv: tuple; env: dict; cwd: str` (`src/superharness/harnesses/base.py:16-30`).
- Two registries: `harnesses/__init__.py` maps runtime name → live object (`register`/`get_harness`, `KNOWN_HARNESSES`); `engine/adapter_registry.py:190-283` maps adapter name → YAML manifest → launcher path, validation, and model tiers
  (`load_manifest`, `validate_adapter` via `shutil.which`/env, `resolve_launcher`, `resolve_model`).
- Manifests (`src/superharness/adapter_manifests/*.yaml`, parsed at `src/superharness/engine/adapter_registry.py:103-187`): `name/version/type(native|external)/launcher_script/capabilities/model_tiers/requires/validation`; new-schema tiers add `preferred/accept/auth_compat/capability_tags` (`src/superharness/adapter_manifests/codex-cli.yaml:23-43`).
- Claude is bespoke (`src/superharness/harnesses/claude.py:28-61`, never model-prefixes); codex/gemini/opencode/pi share `build_generic_invocation` with provider prefixing (`src/superharness/harnesses/base.py:93-132`).
- Discovery differs: claude/codex/gemini probe the manifest accept chain (`src/superharness/harnesses/base.py:64-90`); opencode parses `opencode models` natively (`src/superharness/harnesses/opencode.py:19-62`); Pi parses offline `pi --list-models` table (`src/superharness/harnesses/pi.py:15-86`).
- Launchers are bash shims `scripts/delegate-to-<harness>.sh`: claude maps `--non-interactive` to `-p --dangerously-skip-permissions` (`scripts/delegate-to-claude.sh:33-52`); gemini uses `< /dev/null` + retry (`scripts/delegate-to-gemini.sh:121-141`); Pi execs `pi_runtime --mode json` (`src/superharness/engine/pi_runtime.py:39-71`).
- `shux adapters` surfaces list/info/test plus `--probe` discovery across adapters with cache-first reads (`src/superharness/commands/adapters.py:23-258`).
- Stable external snapshot: `shux adapter-payload` emits schema-`1.4` JSON (tasks, edges, ledger, inbox, heartbeats, rules, artifacts) (`src/superharness/commands/adapter_payload.py:680-709`).
- Parity tests assert golden argv tuples incl. single-element prompt-injection safety (`tests/unit/test_harness_registry.py:39-91`, `tests/unit/test_harness_adapters.py:37-123`, `tests/unit/test_harness_adapters.py:241-253`).

## Q6. What concrete features/ideas can fleet borrow?
1. **Dual watchdog (idle-timeout + absolute-ceiling) over the events table.**
   What: fail a task on minutes-since-last-event OR total age; fresh events spare past-deadline tasks.
   Where: `src/superharness/engine/lifecycle_rules.py:394-505`; tests `tests/unit/test_dual_watchdog.py:66-170`.
   Why fleet wants it: beads rows alone cannot tell "wedged, no output" from "slow but progressing" — this gives the orchestrator a principled kill/retry signal for coder workers.

2. **Typed telemetry events with fire-and-forget background emitter.**
   What: `events(ts, kind, task_id, payload)` table plus daemon-thread writer.
   Where: table `src/superharness/engine/db.py:1306`; emitter `src/superharness/engine/events.py:158-215` (validate-then-queue, warn-only on DB failure, no-op until `configure()`).
   Why fleet wants it: per-task activity history without blocking dispatch or dying on SQLite contention in the beads DB.

3. **Skill extraction → persist → inject loop with usage metrics.**
   What: extract on completion, dedupe by `task_id`, inject top-3 keyword hints into the next dispatch, track uses/success-rate.
   Where: `src/superharness/engine/skill_extractor.py:212-360` (trigger `src/superharness/commands/task.py:769`); hints `src/superharness/engine/context_hint.py:166`; metrics `src/superharness/engine/skill_metrics.py:16-58`.
   Why fleet wants it: coder workers repeat the same repo-specific fixes — a beads-backed skill file compounds that knowledge across runs.

4. **Benchmark JSONL (newline-delimited JSON log) leaderboard + per-model cost view.**
   What: append `(task, agent, outcome, duration, cost, model, slot, fanout)` per dispatch; rank most-expensive-first; 7-day per-model cost/budget table.
   Where: `src/superharness/engine/benchmark.py:52-194`; CLI `src/superharness/commands/benchmark.py:27-61`.
   Why fleet wants it: the orchestrator spawns mixed-model coder workers and needs empirical cost/quality data for routing, not vibes.

5. **Atomic inbox claim + partial unique dedup index.**
   What: one `UPDATE ... WHERE id=(SELECT ... WHERE status='pending' ... ORDER BY priority DESC, created_at ASC) RETURNING *`
   plus a partial unique index blocking duplicate active `(task_id, target_agent)`.
   Where: `src/superharness/engine/inbox_dao.py:161-176`; schema `src/superharness/engine/db.py:621-718`.
   Why fleet wants it: concurrent orchestrator loops claiming from the beads queue is exactly the double-spawn race this kills.

6. **Durable recovery counter + retry ceilings + identical-error escalation.**
   What: `recovery_count` in its own column, fallback-agent reroute, escalate to `waiting_input` at count ≥ 2, `max_retries` ≥ 12, or 4 identical errors.
   Where: `src/superharness/commands/inbox_watch.py:1594-2063`; proof `tests/e2e/test_runaway_recovery_e2e.py:65-95`.
   Why fleet wants it: a crash-looping coder worker otherwise burns budget forever — this is the proven runaway fuse with an e2e-tested ceiling.

7. **Watcher singleton lease + supervisor that watches the watcher.**
   What: lease row with steal-if-stale + `SingletonConflict`, plus a monitor loop that adopts/polls/respawns the watcher; launchd self-heal every 300 s.
   Where: `src/superharness/engine/watcher_singleton.py:21-100`; `src/superharness/commands/daemon_monitor.py:42-109`; `src/superharness/engine/launchd_health.py:315-376`.
   Why fleet wants it: the fleet orchestrator is itself the single point of failure — this keeps exactly one alive across crashes and reboots.

8. **Content-addressed dispatch context (sha256 prompt components).**
   What: prompt parts (`system`, `task_instructions`, `discussion_prompt`, `vault_block`, `project_rules`) deduped by hash with per-dispatch ordering stored.
   Where: `src/superharness/engine/context_dao.py:16-80`; schema `src/superharness/engine/db.py:1839-1883`.
   Why fleet wants it: identical prompts re-dispatched to coder workers waste tokens and hide prompt drift — hashing makes dispatch reproducible and auditable.

## Bottom line
Fleet and superharness share the same core: a SQLite task/queue store as sole authority, an atomic-claim inbox feeding spawned coder workers, and a reconciling watcher loop with heartbeats and lifecycle timeouts.
Fleet already has the beads DB (SQLite task store) + queue + orchestrator skeleton, so the mechanical borrows (atomic claim, singleton lease, recovery ceilings) are small.
Closest overlap beyond storage is the watcher itself: fleet's orchestrator loop needs the same zombie-reaping, stuck-input, and orphan-GC reconcilers superharness runs every tick.
Next after the watchdog, the cheapest wins are the atomic claim and the recovery ceilings — both small, test-backed, and directly stopping double-spawns and runaway spend.
The single highest-value borrow is the dual watchdog over typed telemetry events — it turns "worker is silent" from a guess into a measured kill/retry decision, and it unlocks the benchmark, skill, and cost-routing layers above it.

**Covers:** wiki/01-07 + `engine/db.py`, `engine/next_action.py`, `engine/lifecycle_rules.py`, `engine/inbox_dao.py`, `engine/handoffs_dao.py`, `engine/ledger_dao.py`, `engine/events.py`, `engine/context_dao.py`, `engine/state_reader.py`, `engine/state_writer.py`
**Covers (cont.):** `engine/preflight.py`, `engine/plan_validator.py`, `engine/subtask_gate.py`, `engine/worktree_ops.py`, `engine/parallel_dispatch.py`, `engine/swarm.py`, `engine/review_fanout.py`, `engine/discussion.py`, `engine/orchestrator.py`, `engine/smart_dispatch.py`, `engine/skill_extractor.py`, `engine/skill_metrics.py`, `engine/benchmark.py`, `engine/liveness.py`, `engine/transcript_tail.py`, `harnesses/base.py`, `engine/adapter_registry.py`, `commands/inbox_enqueue.py`, `commands/inbox_dispatch.py`, `commands/inbox_watch.py`, `commands/inbox_gc.py`, `commands/daemon_monitor.py`, `commands/close.py`, `commands/delegate.py`
