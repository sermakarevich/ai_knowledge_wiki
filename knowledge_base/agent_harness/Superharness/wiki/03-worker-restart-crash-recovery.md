> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Worker Restart and Crash Recovery

**In one sentence:** crashed or timed-out workers are detected via heartbeats and stale inbox rows, their partial state survives in append-only handoffs plus ledger plus git-stash checkpoints plus auto-flush YAML, and the next dispatch respawns with that full context while durable counters cap retry loops.

## Key points

- Handoffs carry two phases, `plan` and `report`, with task status carried alongside — boundary validation is the crash-safety contract (`src/superharness/engine/handoffs_dao.py:14`, `src/superharness/engine/handoffs_dao.py:29`).
- Both handoff and ledger tables are append-only; nothing is updated or deleted in place (`src/superharness/engine/handoffs_dao.py:88`, `src/superharness/engine/ledger_dao.py:57`).
- Checkpoints are git-stash entries tagged `shux-checkpoint:<task-id>`, not files (`src/superharness/guard/checkpoint.py:9`).
- Expiring tasks are auto-flushed to `.superharness/handoffs/<id>-auto-flush-<date>.yaml` on every watcher tick (`src/superharness/engine/session_flush.py:50`, `src/superharness/commands/inbox_watch.py:3105`).
- Session end is handled by stop/exit hooks that park active inbox rows as `stopped` and clear the PID (`src/superharness/engine/inbox_dao.py:417`).
- Crash recovery is a pipeline: heartbeat zombie-marking → `inbox recover` → watcher auto-recover with reroute → `inbox gc` reconcile, all audited in the ledger (`src/superharness/engine/heartbeat_dao.py:141`, `src/superharness/commands/inbox_recover.py:68`, `src/superharness/commands/inbox_gc.py:26`).
- `recovery_count` lives in its own inbox column so failure rewrites cannot wipe it; retries are capped (`_RECOVERY_MAX=2`, absolute `max_retries=12`, identical-error threshold `4`) (`src/superharness/commands/inbox_watch.py:1594`, `tests/unit/test_recovery_counter_durable.py:27`).
- A respawned agent receives handoff history plus recent ledger plus the hashed dispatch prompt components (system, task instructions, rules, vault block) (`src/superharness/engine/handoffs_dao.py:119`, `src/superharness/engine/context_dao.py:16`, `src/superharness/engine/ledger_dao.py:79`).

---

## Handoff model

Phases are a closed enum with one source of truth (`src/superharness/engine/handoffs_dao.py:14`):

```python
VALID_PHASES: frozenset[str] = frozenset({"plan", "report"})  # src/superharness/engine/handoffs_dao.py:14
```

`LEGACY_PHASES = {"done"}` still passes the gate for old `<task>-done-<date>` files read by `inbox_watch` (`src/superharness/engine/handoffs_dao.py:19`). `HANDOFF_ONLY_STATUSES = {"approved", "plan_confirmed"}` covers statuses written by `engine/discuss.py _do_approve` and the dashboard UI that are not task statuses (`src/superharness/engine/handoffs_dao.py:26`). `_validate_boundary()` rejects any out-of-set phase/status with `BoundaryError` before any write (`src/superharness/engine/handoffs_dao.py:29`).

`append()` is append-only — `INSERT ... RETURNING *`, never update/delete — and strips `<private>` tags from content and metadata (`src/superharness/engine/handoffs_dao.py:76`). Readers use `get_history()` (all rows for a task, `created_at ASC, id ASC`) and `get_latest(task, phase)` for the newest row of one phase (`src/superharness/engine/handoffs_dao.py:119`, `src/superharness/engine/handoffs_dao.py:172`).

CLI surface: `shux handoff write --phase plan|report` builds a plan payload (requires `--plan`, defaults status `plan_proposed`) or a report payload (requires `--outcome`, defaults status `report_ready`) (`src/superharness/commands/handoff_write.py:150`, `src/superharness/commands/handoff_write.py:204`, `src/superharness/commands/handoff_write.py:322`). SQLite is the source of truth via `write_handoff_to_db()`; YAML export to `.superharness/handoffs/` is best-effort and never blocks the write (`src/superharness/commands/handoff_write.py:274`). `write_handoff_to_db()` maps the dict to columns (phase defaults to `report`, status to `report_ready`), stubs a missing task row, and re-raises `BoundaryError` while swallowing only infrastructure failures (`src/superharness/engine/state_writer.py:367`). `handoff generate` produces a structured doc (`summary`, `scope`, `acceptance`, `risks`, `artifacts`, `compaction`, `rules`) from live task state into `<task>-auto.yaml` (`src/superharness/engine/handoff_generator.py:113`, `src/superharness/commands/handoff_generate.py:35`). `HANDOFF.md` at repo root (~2100 lines at this commit) is the human session log with `What happened` / `Next session — first moves` / `Operational notes` per entry — sampled, not parsed by code (`HANDOFF.md:1`).

## Ledger

`ledger_dao.record()` inserts `(task_id, agent, action, details, created_at)` and returns the row; unknown `task_id` degrades to `NULL` instead of failing, matching `ON DELETE SET NULL` semantics (`src/superharness/engine/ledger_dao.py:25`). `get_recent()` filters by task/agent, newest first, default limit 100 (`src/superharness/engine/ledger_dao.py:79`). `decision_log()` is the fire-and-forget wrapper used at decision points (gate blocks, retries, escalations, cancellations) and never raises (`src/superharness/engine/ledger_dao.py:120`). GC audits every reconcile with `agent="inbox_gc", action="gc_reconcile"` plus item id and from/to (`src/superharness/commands/inbox_gc.py:84`).

## Checkpoints

Git-stash based, three operations (`src/superharness/guard/checkpoint.py:1`):

```python
["git", "stash", "push", "-m", f"shux-checkpoint:{safe_id}"]  # src/superharness/guard/checkpoint.py:12
```

`snapshot()` stashes dirty changes under `shux-checkpoint:<safe-id>` and returns False when there is nothing to save (`src/superharness/guard/checkpoint.py:9`). `rollback()` pops the matching stash entry (`src/superharness/guard/checkpoint.py:22`). `prune_old()` drops `shux-checkpoint:` entries and `list_checkpoints()` lists them (`src/superharness/guard/checkpoint.py:41`, `src/superharness/guard/checkpoint.py:60`). There is no checkpoint file format or directory — location is the repo's stash stack. (Note: `guard/state.py` is unrelated to crash state; it is the approval allowlist with `once`/`session`/`permanent` scopes and low/medium/high risk classification — `src/superharness/guard/state.py:51`, `src/superharness/guard/state.py:83`.)

## Session flush

`check_expiring()` scans contract-status lifecycle rules and returns tasks whose timeout expires within `warning_minutes` (default 15) (`src/superharness/engine/session_flush.py:14`). `flush_task()` writes `.superharness/handoffs/<safe-id>-auto-flush-<YYYY-MM-DD>.yaml` with `phase: auto-flush`, current status, and a `task_snapshot` (status, acceptance criteria, context) (`src/superharness/engine/session_flush.py:50`). It fires on every watcher cycle inside `_run_scripts`, printing `session-flush: flushed N expiring task(s)` (`src/superharness/commands/inbox_watch.py:3105`). Separately, the session-stop/session-exit hooks call `sync_task_status()`, which moves every active inbox row for the task to the target status (typically `stopped`), clears `pid`, and never touches terminal done/failed rows (`src/superharness/engine/inbox_dao.py:417`).

## Crash recovery path

Liveness: agents upsert `agent_heartbeats` rows; the reconciler marks rows `zombie` when `updated_at` is older than `STALE_THRESHOLD_SECONDS = 120` (`src/superharness/engine/heartbeat_dao.py:14`, `src/superharness/engine/heartbeat_dao.py:35`, `src/superharness/engine/heartbeat_dao.py:141`). The operator's `monitor_and_recover()` loop reaps zombies via `proc.poll()`, terminates old subprocesses before restart to avoid orphan accumulation, reuses dashboard ports, and emits a `process_recovery` trace event per restart (`src/superharness/engine/operator.py:370`, `src/superharness/engine/operator.py:421`).

Stale inbox: `inbox recover` flips `launched` rows older than `--timeout-minutes` (default 20) to `stale` (default `--action stale`) or back to `pending` (`--action retry`), with a `--dry-run` preview mode (`src/superharness/commands/inbox_recover.py:17`, `src/superharness/commands/inbox_recover.py:68`). `inbox gc` (`run_gc`) reconciles `GC_ELIGIBLE = {"stopped", "failed", "stale", "paused"}` rows to `done` when the contract task is `done`/`archived` or past dispatch (`report_ready`, `review_*`) (`src/superharness/commands/inbox_gc.py:16`, `src/superharness/commands/inbox_gc.py:59`).

Watcher auto-recover for exhausted failures reads `recovery_count` from its own column, falls back to parsing legacy `recovery_N` markers only when the column is 0, reroutes to a fallback agent, and escalates to `waiting_input` once `recovery_count >= _RECOVERY_MAX` (2), when `max_retries >= _ABSOLUTE_MAX_RETRIES` (12), or when the last 4 failures share one error snippet (`src/superharness/commands/inbox_watch.py:1594`, `src/superharness/commands/inbox_watch.py:1865`, `src/superharness/commands/inbox_watch.py:2021`, `src/superharness/commands/inbox_watch.py:2063`).

Durable counter: migration v8 added `inbox.recovery_count` default 0, backfilling legacy `recovery_N:agentA_to_agentB` markers from `failed_reason` (`tests/unit/test_recovery_counter_durable.py:27`, `tests/unit/test_recovery_counter_durable.py:66`). The proven scenario is the production runaway (`max_retries=65` from 3 stale inbox items on one discussion task with a missing discussion directory): the e2e test asserts identical-error loops escalate to `waiting_input` with zero active rows and that repeated auto-recover cycles never push `max_retries` past 12 (`tests/e2e/test_runaway_recovery_e2e.py:1`, `tests/e2e/test_runaway_recovery_e2e.py:65`, `tests/e2e/test_runaway_recovery_e2e.py:95`).

## Respawn with context

A fresh worker for the same task receives, in order of authority:

- Handoff history: `get_history()` full chain plus `get_latest(task, "report")` for the newest report, which `observation_capture` also uses to ground the next observation (`src/superharness/engine/handoffs_dao.py:119`, `src/superharness/engine/observation_capture.py:43`).
- Generated compaction: `goal`, `constraints`, `progress` (TDD phase derived from status), `decisions`, `next_steps` per status, plus injected project rules (`src/superharness/engine/handoff_generator.py:65`, `src/superharness/engine/handoff_generator.py:102`).
- Ledger tail: `get_recent(task_id=...)` operational trace — retries, escalations, GC reconciles (`src/superharness/engine/ledger_dao.py:79`).
- Exact dispatch prompt: content-addressed components (`system`, `task_instructions`, `discussion_prompt`, `vault_block`, `project_rules`) deduplicated by sha256, with per-dispatch ordering in `dispatch_context_component` (migration v39) (`src/superharness/engine/context_dao.py:16`, `src/superharness/engine/context_dao.py:65`, `src/superharness/engine/db.py:1840`).
- Auto-flush snapshot if the previous session died near timeout: the `<task>-auto-flush-<date>.yaml` file with inline `task_snapshot` (`src/superharness/engine/session_flush.py:50`).

**Covers:** handoff phases/statuses/boundary, ledger append-only + decision log, git-stash checkpoints, session flush + stop hooks, heartbeat zombie detection, operator restart loop, inbox recover/GC, durable recovery counter + retry ceilings + e2e proof, respawn-with-context bundle.
