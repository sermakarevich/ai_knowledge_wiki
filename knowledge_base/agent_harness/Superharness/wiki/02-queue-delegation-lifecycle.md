> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Queue-Based Delegation and Lifecycle Rules

**In one sentence:** Delegation is a SQLite (Structured Query Language Lite, file-based database)-backed queue (`inbox` rows) fed by `inbox_enqueue`, claimed atomically by `inbox_dispatch`, supervised by `inbox_watch`, while task progress follows a strict status graph (`next_action.py`) plus a timeout reconciler (`lifecycle_rules.py`).

## Key points

- Inbox rows are a priority queue with states `pending → launched → running/paused → done/failed/stale` (`src/superharness/engine/schemas.py:48-55`, `src/superharness/engine/inbox_dao.py:34`); `stopped` is written only via the session-stop hook path (`src/superharness/engine/inbox_dao.py:417-438`), not the `InboxStatus` enum (Application Programming Interface, the allowed value list).
- Enqueue inserts one `pending` row per (`task_id`, `target_agent`) and rejects duplicates while an active row exists (`src/superharness/engine/inbox_dao.py:37-60`); `inbox_enqueue` additionally blocks non-dispatchable task statuses by workflow (`src/superharness/commands/inbox_enqueue.py:158-184`).
- Dispatch claims with a single atomic `UPDATE ... WHERE id = (SELECT ... WHERE status='pending' ...)` so concurrent watchers cannot double-claim (`src/superharness/engine/inbox_dao.py:144-176`, wrapped at `src/superharness/commands/inbox_dispatch.py:740-774`).
- Watch runs single-cycle (launchd (macOS background scheduler)/systemd (Linux background scheduler)) or foreground poll loop (`src/superharness/commands/inbox_watch.py:5381-5460`), writes a watcher heartbeat each tick (`src/superharness/commands/inbox_watch.py:610-639`), and reconciles zombies, stuck inputs, orphaned discussion inboxes, and consensus closes (`src/superharness/commands/inbox_watch.py:3673-3684`, `src/superharness/commands/inbox_watch.py:5210-5235`, `src/superharness/commands/inbox_watch.py:5250-5288`).
- Task lifecycle is a closed graph: `VALID_STATUSES` derives from `ALL_STATUSES` (`src/superharness/engine/tasks_dao.py:19`, `src/superharness/engine/next_action.py:19-38`), legal edges live in `_MAPPING` and are enforced by `validate_status_transition` (`src/superharness/engine/next_action.py:53-150`, `src/superharness/engine/next_action.py:371-392`).
- Auto-mode (non-interactive operation governed by `profile.yaml autonomy`, e.g. `ai_driven`) auto-closes reviews, auto-retries failures, and auto-archives/fails timed-out states via one rule table plus deadline/idle/ceiling checks (`src/superharness/commands/inbox_watch.py:26-29`, `src/superharness/commands/inbox_watch.py:1091-1093`, `src/superharness/engine/lifecycle_rules.py:47-164`, `src/superharness/engine/lifecycle_rules.py:394-418`).
- Subtasks do not dispatch independently; parent close is gated on `done/cancelled` and results aggregate to `report_ready` (all done) or `failed` (any failed) (`src/superharness/engine/subtask.py:34-50`, `src/superharness/engine/subtask_gate.py:45-68`, `src/superharness/engine/subtask_aggregator.py:99-104`).

---

## Inbox queue model

Inbox rows (`InboxRow`: `id, task_id, target_agent, status, priority, retry_count, max_retries, pid, timestamps...`) are defined at `src/superharness/engine/inbox_dao.py:11-32`. Native enum states are `pending, launched, running, done, failed, stale, paused` (`src/superharness/engine/schemas.py:48-55`). Active set for dedup/claim is `("pending", "launched", "running", "paused")` (`src/superharness/engine/inbox_dao.py:34`).

Terminal handling is explicit: `mark_done` sets `done + done_at` (`src/superharness/engine/inbox_dao.py:276-286`), `mark_failed` sets `failed + failed_reason + failed_at` (`src/superharness/engine/inbox_dao.py:298-309`), `mark_stale` sets `stale` unconditionally for cleanup (`src/superharness/engine/inbox_dao.py:263-273`), `purge_stale` deletes `stale` rows (`src/superharness/engine/inbox_dao.py:355-358`). `sync_task_status` moves every active row for a `task_id` to a given status and clears `pid`, used by session-stop/exit hooks to mark rows `stopped` (`src/superharness/engine/inbox_dao.py:417-438`). Heartbeat column `last_heartbeat` plus `get_stale` (rows in `launched/running` older than cutoff) drive staleness detection (`src/superharness/engine/inbox_dao.py:215-242`).

## Enqueue path

`enqueue_cmd` validates project dir, target agent (`KNOWN_HARNESSES`, `src/superharness/commands/inbox_enqueue.py:23`), priority, and task-id token, then generates `item_id` when absent (`src/superharness/commands/inbox_enqueue.py:206-239`). `_sqlite_enqueue` writes via `inbox_dao.enqueue` plus a ledger (append-only audit log) `enqueued` record in one transaction (`src/superharness/commands/inbox_enqueue.py:30-67`).

Two dispatch gates run before insert:

- `plan_proposed` is always blocked until plan approval (`src/superharness/commands/inbox_enqueue.py:151-156`).
- Other statuses must belong to `allowed_statuses_for_workflow(workflow, for_review=True)` or `plan_only_allowed_statuses(workflow)`; `failed/stopped` pass through for retry, `todo` without `--plan-only` gets a planning hint (`src/superharness/commands/inbox_enqueue.py:158-184`, allowed sets at `src/superharness/engine/next_action.py:233-287`).

SQLite (database) dedup rejects a second active row for the same (`task_id`, `target_agent`); discussion round-ids (`/round-`) downgrade to a warning instead of crashing (`src/superharness/engine/inbox_dao.py:56-79`).

## Dispatch path

Entry is `dispatch()` → `_do_dispatch()` with a mkdir-based non-blocking lock (`src/superharness/commands/inbox_dispatch.py:777-834`, `src/superharness/commands/inbox_dispatch.py:837-866`, lock at `src/superharness/commands/inbox_dispatch.py:105-120`). Claim order is priority `DESC`, `created_at ASC` inside the atomic `UPDATE ... RETURNING *` (`src/superharness/engine/inbox_dao.py:161-176`):

```sql
UPDATE inbox
SET status='launched', pid=?, launched_at=?, last_heartbeat=?
WHERE id = (
    SELECT id FROM inbox
    WHERE status='pending' AND target_agent=?
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
)
RETURNING *
```

— `src/superharness/engine/inbox_dao.py:162-172`.

`_claim_next_item` requires `--to <agent>` in `sqlite_only` mode and maps the claimed row to YAML (human-readable config format)-shape keys (`id/to/task/project`) (`src/superharness/commands/inbox_dispatch.py:950-984`). `_transition_to_launched` is a no-op transition in SQLite mode because `claim_next` already set `launched` (`src/superharness/commands/inbox_dispatch.py:987-999`).

Safety guards before spawn live in `_resolve_execution_context` (`src/superharness/commands/inbox_dispatch.py:2093-2192`): effort-based launcher timeout (`TIMEOUT_LOW/MEDIUM/HIGH_EFFORT`, `src/superharness/commands/inbox_dispatch.py:24-27`), mandatory isolated git worktree (separate directory for safe code changes) for Pi (agent runtime) non-interactive dispatch with preflight error fail-closed (`src/superharness/commands/inbox_dispatch.py:2125-2146`), dirty-worktree pause for other agents (`src/superharness/commands/inbox_dispatch.py:2126-2131`, `src/superharness/commands/inbox_dispatch.py:2190-2192`), and dependency check via `blocked_by` requiring deps in `done/archived` (`src/superharness/engine/inbox.py:50-79`, cached variant `src/superharness/commands/inbox_watch.py:43-65`). Retry/fallback paths use `set_retry` (back to `pending`), `reassign` (new agent), and `mark_recovered` (`max_retries+1`) (`src/superharness/engine/inbox_dao.py:245-260`, `src/superharness/engine/inbox_dao.py:312-352`).

## Watch path

`watch()` (`src/superharness/commands/inbox_watch.py:5381-5402`) takes a watcher lock with stale-lock auto-break keyed on heartbeat age (`src/superharness/commands/inbox_watch.py:459-484`, `src/superharness/commands/inbox_watch.py:5418-5429`) plus a SQLite singleton lease (`src/superharness/commands/inbox_watch.py:5431-5432`). One-shot (`--once`, the launchd path) runs `_run_scripts` once; foreground loops on `interval` (`src/superharness/commands/inbox_watch.py:5458-5470`).

Each cycle writes two heartbeats — legacy `watcher.heartbeat` timestamp and `heartbeat_contract` YAML (`src/superharness/commands/inbox_watch.py:610-639`) — then runs reconcilers:

- `_reconcile_zombies`: `launched` rows with no live process → `done` if contract says `done`, `failed` if pid dead, kill-and-fail on plan-only >15 min or any launch >2 h (`src/superharness/commands/inbox_watch.py:3673-3792`).
- Heartbeat staleness: `get_stale` selects `launched/running` rows whose `COALESCE(last_heartbeat, launched_at, created_at)` predates the cutoff (`src/superharness/engine/inbox_dao.py:220-242`); `inbox_recover --timeout-minutes 20 --action stale|retry` converts them (`src/superharness/commands/inbox_recover.py:17-19`, `src/superharness/commands/inbox_recover.py:68-77`).
- `_reconcile_paused_dead_pids`, `_reconcile_permanent_blocks`, `_reconcile_discussion_contract` cover paused/dead and discussion drift (`src/superharness/commands/inbox_watch.py:401`, `src/superharness/commands/inbox_watch.py:2118`, `src/superharness/commands/inbox_watch.py:3866-3880`).
- Orphan/consensus garbage collection (GC, automatic cleanup): `_gc_orphaned_discussion_inbox` marks inbox rows `done` for closed discussions (`src/superharness/commands/inbox_watch.py:5210-5235`); `_auto_advance_orphaned_rounds` moves inbox-done rounds with no verdicts to pending-review `consensus` after 5 min (`src/superharness/commands/inbox_watch.py:3964-3966`, `src/superharness/commands/inbox_watch.py:4071-4226`); `_auto_close_consensus_discussions` closes consensus after 60 min grace (`src/superharness/commands/inbox_watch.py:3964`, `src/superharness/commands/inbox_watch.py:4244-4312`).

## Lifecycle state machine

Canonical task statuses (`todo, plan_proposed, plan_approved, in_progress, pending_user_approval, report_ready, review_requested/passed/failed, pr_open, done, failed, blocked, stopped, waiting_input, paused, archived`, plus `pending` for decomposed-subtask rows) are listed in `ALL_STATUSES` (`src/superharness/engine/next_action.py:19-38`); `TERMINAL_STATUSES = {done, failed, stopped}` (`src/superharness/engine/next_action.py:40`). Task-field enum mirrors this in `TaskStatus` (`src/superharness/engine/schemas.py:22-45`).

Legal edges and recommendations live in `_MAPPING`, e.g. `todo → plan_proposed/waiting_input`, `in_progress → report_ready/pending_user_approval/stopped/failed/waiting_input`, `report_ready → review_passed/review_failed/review_requested` (`src/superharness/engine/next_action.py:53-150`):

```python
"todo": (
    "plan_proposed",
    ["plan_proposed", "waiting_input"],
    "author a plan handoff before dispatch",
),
```

— `src/superharness/engine/next_action.py:65-69`.

`validate_status_transition` raises on illegal edges; unknown current statuses fail open (`src/superharness/engine/next_action.py:371-392`). Dispatchability per workflow (implementation, quick, note, discussion, review, approval) is decided by `allowed_statuses_for_workflow` / `plan_only_allowed_statuses` (`src/superharness/engine/next_action.py:233-287`); `task.py` enforces both the transition check and the dispatch-ready check on status changes (`src/superharness/commands/task.py:548-555`, `src/superharness/commands/task.py:630-632`). Dashboard columns derive from `STATUS_TO_COL` / `STATUS_GROUPS` (`src/superharness/engine/next_action.py:300-356`).

## Auto-mode rules

Auto-mode means watcher-driven operation with `non_interactive=True` and profile `autonomy` (default `ai_driven`) controlling defaults for `auto_close`/`auto_retry` (`src/superharness/commands/inbox_watch.py:26-29`, `src/superharness/commands/inbox_watch.py:5395`, `src/superharness/commands/inbox_watch.py:1091-1093`, `src/superharness/commands/inbox_watch.py:1445`). Watch auto-closes `report_ready`/`review_requested` on reviewer LGTM (Looks Good To Me, approval signal) verdicts and auto-retries failures only when enabled (`src/superharness/commands/inbox_watch.py:1090-1154`, `src/superharness/commands/inbox_watch.py:1445`).

Timeout automation is data-driven in `LIFECYCLE_RULES` (`src/superharness/engine/lifecycle_rules.py:47-164`):

```python
LifecycleRule(
    state="paused",
    timeout_minutes=30,
    on_timeout="fail",
    source="inbox",
    timestamp_field="paused_at",
    skip_if_field="reason",
    profile_key="paused_timeout_minutes",
),
```

— `src/superharness/engine/lifecycle_rules.py:48-56`.

Covered timeouts: inbox `paused` 30 m → `fail`; contract `review_requested` 120 m → revert to `report_ready`; `in_progress` 180 m → `archive`; `waiting_input` 480 m → `fail`; `report_ready` 1440 m → `archive`; `todo` 120 m → `archive`; `stopped` 7 d → `archive`; `plan_approved` 240 m / `plan_proposed` 480 m / `pending_user_approval` 480 m → `fail` (`src/superharness/engine/lifecycle_rules.py:47-164`). Each rule honors a `profile.yaml` override and a `skip_if_field` exemption (`reason`, `escalated_to`) (`src/superharness/engine/lifecycle_rules.py:205-211`, `src/superharness/engine/lifecycle_rules.py:269-306`). `_apply_action` stamps `failed_reason/failed_at` or `archived_reason/archived_at` (`src/superharness/engine/lifecycle_rules.py:230-252`); contract writes use `force=True` to bypass the user transition graph (`src/superharness/engine/lifecycle_rules.py:354-365`).

Deadlines add a second layer in `_check_deadlines`: legacy `deadline_minutes`/`default_deadline_minutes` measured from `in_progress_at` (fallback `created_at`), plus opt-in dual watchdog (`idle_timeout_minutes` on event-table silence, `absolute_ceiling_minutes` on total age) (`src/superharness/engine/lifecycle_rules.py:394-468`, eligible states at `src/superharness/engine/lifecycle_rules.py:169-186`). `reconcile_lifecycle` runs inbox scan + contract scan + deadline check (`src/superharness/engine/lifecycle_rules.py:571-583`). Watch-local GC duplicates part of this for `waiting_input` (>30 m → `archived`) and no-handoff stale tasks (4 h, `src/superharness/commands/inbox_watch.py:5250-5288`, `src/superharness/commands/inbox_watch.py:642-651`).

## Subtasks

Subtasks are planning artifacts inside `contract.yaml`, not independently dispatched (`src/superharness/engine/subtask.py:1-11`). Resolved = `done/cancelled`; open/blocking = `pending/in_progress/failed` (`src/superharness/engine/subtask.py:34-50`). Effective status inherits parent `done/review_passed` unless an explicit non-`pending` status exists (`src/superharness/engine/subtask.py:53-76`).

The close gate (`evaluate_subtask_gate`) is off by default, enabled per-task or per-profile with profile winning; blocking subtasks produce a `shux close --cancel-remaining/--force` error message (`src/superharness/engine/subtask_gate.py:45-91`). `SubtaskAggregator.record_results` writes per-subtask tokens/cost/model, then sets parent `report_ready` (all done) or `failed` (any failed) (`src/superharness/engine/subtask_aggregator.py:48-107`). Bulk-cancel of leftovers is `shux close --cancel-remaining --cancel-reason` (`src/superharness/commands/close.py:97-174`); dangling discussion inbox rows for closed discussions are swept by `_gc_orphaned_discussion_inbox` (`src/superharness/commands/inbox_watch.py:5210-5235`).

**Covers:** `engine/inbox.py`, `engine/inbox_dao.py`, `engine/next_action.py`, `engine/lifecycle_rules.py`, `commands/inbox_enqueue.py`, `commands/inbox_dispatch.py`, `commands/inbox_watch.py`, `commands/inbox_recover.py`, `commands/delegate.py`, `commands/task.py`, `engine/subtask.py`, `engine/subtask_gate.py`, `engine/subtask_aggregator.py`, `engine/tasks_dao.py`.
