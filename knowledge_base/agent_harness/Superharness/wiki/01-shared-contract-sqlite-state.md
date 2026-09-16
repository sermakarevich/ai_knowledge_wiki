> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Shared Contract and SQLite State
**In one sentence:** One per-project SQLite `state.db` (39 migrations, Pydantic-validated contract model) is the sole runtime authority, with all task/inbox/handoff writes funneled through typed DAO boundaries and canonical `state_reader` / `state_writer` paths while YAML survives only as export/backfill material.

## Key points
- Local-first, one authoritative state: tasks, inbox rows, handoffs, decisions, failures, heartbeats, dispatch context all live in one SQLite DB, never a network service (`docs/ARCHITECTURE.md:12-20`).
- Schema is 39 ordered migrations (`src/superharness/engine/db.py:20`, `src/superharness/engine/db.py:1886-1926`); `init_db` tracks `schema_migrations` + `PRAGMA user_version` and heals additive-column drift via `_ADDITIVE_COLUMN_MANIFEST` (`src/superharness/engine/db.py:271-289`, `src/superharness/engine/db.py:346-389`).
- DB path resolves to `$XDG_STATE_HOME/superharness/<project-hash>/state.db`, overridable by `SUPERHARNESS_STATE_DIR`, with fail-closed `StateDatabaseConflictError` on split-brain roots (`src/superharness/utils/paths.py:135-165`, `docs/ARCHITECTURE.md:118-131`).
- Journal mode is WAL on local disk, PERSIST rollback journal on network filesystems, with stale `-wal`/`-shm` sidecar removal and `foreign_keys=ON` + busy timeout on every connection (`src/superharness/engine/db.py:89-107`, `src/superharness/engine/db.py:161-233`).
- Handoff writes are gated at the DAO edge: `phase` in `{plan, report}` (+ legacy `done`), `status` in task lifecycle enum + `{approved, plan_confirmed}`, else `BoundaryError` (`src/superharness/engine/handoffs_dao.py:14-50`).
- Event writes validate structurally (frozen dataclass with non-empty `kind` + `task_id`), raising `TypeError`/`ValueError` synchronously before queueing; background-writer failures stay warn-only (`src/superharness/engine/events.py:70-80`, `docs/ARCHITECTURE.md:81-91`).
- Dispatch prompt ingredients are content-addressed: `context_component` keyed by sha256, `dispatch_context` per dispatch, `dispatch_context_component` ordered join; `COMPONENT_TYPES` is a closed 5-value set (`src/superharness/engine/context_dao.py:16-32`, `src/superharness/engine/db.py:1839-1883`).
- Reads go through `state_reader` (SQLite direct in production, YAML auto-ingest only under pytest); writes go through `state_writer` (transition validation, contract lock, timestamps); `BoundaryError` (caller bug, re-raised) is distinguished from `StateError` (infrastructure, swallowed by best-effort paths) (`src/superharness/engine/state_reader.py:129-173`, `src/superharness/engine/state_writer.py:367-462`, `src/superharness/engine/state_errors.py:4-39`).

---
## Design principles
Six principles from `docs/ARCHITECTURE.md:10-20`:

| Principle                        | Mechanism                                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------------------ |
| Local-first                      | Runtime state is SQLite, works offline after install                                       |
| One authoritative state          | Tasks, inbox, handoffs, decisions, failures, heartbeats in one DB                          |
| Explicit state transitions       | `engine/next_action.py` owns legal lifecycle edges and next-action gates                   |
| Agent-neutral adapters           | Claude Code, Codex CLI, Gemini CLI, OpenCode share manifests + common task model           |
| Least surprise for operators     | Background services opt-in; dashboard loopback-only with per-project auth                  |
| Compatibility without split brain| Legacy YAML import/export allowed; production reads use SQLite; conflicting roots fail closed |

Runtime topology (`docs/ARCHITECTURE.md:21-40`):

```text
Operator ──► CLI (cli.py) ──► commands/ ──► engine/ ──► SQLite state.db
                                     │            ▲
                                     ▼            │
                              Agent adapters ─► Agents (Claude / Codex / Gemini / OpenCode)
Operator service ──► Watcher/dispatcher ──► engine/
Loopback dashboard ──► engine/ ◄── Operator
```

The CLI is a thin Click entry point (`src/superharness/cli.py`); per-command validation lives in `src/superharness/commands/`; reusable state machine, DAO layer, and lifecycle rules live in `src/superharness/engine/` (`docs/ARCHITECTURE.md:37-55`).

## SQLite as single authority
`CURRENT_SCHEMA_VERSION = 39` with `_MIGRATIONS` list run in order under per-migration SAVEPOINTs (`src/superharness/engine/db.py:20`, `src/superharness/engine/db.py:1886-1926`). Core tables created in v1 (`src/superharness/engine/db.py:617-813`): `tasks`, `task_dependencies`, `inbox` (with partial unique index blocking duplicate active `(task_id, target_agent)`), `handoffs`, `failures`, `decisions`, `ledger`, `review_store`, `watcher_instance`. Later migrations add: subtasks/discussions (`src/superharness/engine/db.py:815-876`), contract lock columns (`src/superharness/engine/db.py:970-975`), observations/summarizer/operator tables (`src/superharness/engine/db.py:978-1050`), heartbeats/artifacts (`src/superharness/engine/db.py:1060-1112`), `project_meta` key/value id+goal store (`src/superharness/engine/db.py:1115-1124`), agent liveness tables (`src/superharness/engine/db.py:1173-1219`), usage/cooldowns/issue/events/cursors tables (`src/superharness/engine/db.py:1254-1333`), FK hardening rebuilds (`src/superharness/engine/db.py:1336-1539`), `tasks.status` CHECK constraint generated from `next_action.ALL_STATUSES` (`src/superharness/engine/db.py:1576-1721`), discussion dedup index (`src/superharness/engine/db.py:1724-1768`), model discovery cache (`src/superharness/engine/db.py:1771-1836`), content-addressed dispatch context (`src/superharness/engine/db.py:1839-1883`). Dead schema is removed, not left: v6 FTS table dropped in v23, `yaml_sync_queue` dropped in v24 (`src/superharness/engine/db.py:1153-1170`).

Connection setup (`src/superharness/engine/db.py:161-233`): requires SQLite >= 3.35.0, resolves path via `resolve_active_state_db_path`, `makedirs` the parent, picks journal mode via `_resolve_journal_mode` (env `SUPERHARNESS_JOURNAL_MODE` override validated against `_VALID_JOURNAL_MODES`, else WAL local / PERSIST on NFS/CIFS/sshfs-class mounts detected via `/proc/mounts` in `_is_network_fs`), deletes stale `-wal`/`-shm` sidecars when leaving WAL, then sets `PRAGMA journal_mode`, `foreign_keys=ON`, `busy_timeout` 5000 ms (15000 ms off-WAL). `managed_connection` opens, runs `init_db`, yields, commits, rolls back on error, always closes (`src/superharness/engine/db.py:251-268`).

DB location (`src/superharness/utils/paths.py:109-173`, `docs/ARCHITECTURE.md:116-131`):

```text
$XDG_STATE_HOME/superharness/<12-char-project-hash>/state.db
```

`SUPERHARNESS_STATE_DIR` overrides the root; `SUPERHARNESS_STATE_PROJECT` lets a worktree reuse its parent's state. If the override would create a second DB while a legacy `.superharness/state.sqlite3` or ambient-XDG DB already exists, resolution raises `StateDatabaseConflictError` instead of splitting state. `sqlite_only.is_sqlite_only()` defaults to True (migration permanent since 2026-05-24); YAML is export-only (`src/superharness/engine/sqlite_only.py:1-33`).

Per-DAO stores (skim): `tasks_dao` holds the `TaskRow` lifecycle record with optimistic-concurrency `version` and `VALID_STATUSES` derived from `next_action.ALL_STATUSES` (`src/superharness/engine/tasks_dao.py:12-19`); `inbox_dao` holds `InboxRow` dispatch records with `enqueue` dedup against active statuses and `update_status` timestamp handling (`src/superharness/engine/inbox_dao.py:10-60`); `ledger_dao.record` appends operational trace rows and degrades dangling `task_id` to NULL instead of losing the record (`src/superharness/engine/ledger_dao.py:25-54`).

Verbatim schema excerpt — v1 tasks/inbox/handoffs (`src/superharness/engine/db.py:621-718`):

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id                   TEXT    PRIMARY KEY,
    title                TEXT    NOT NULL,
    owner                TEXT,
    status               TEXT    NOT NULL,
    effort               TEXT,
    project_path         TEXT,
    development_method   TEXT,
    acceptance_criteria  TEXT,
    ...
    version              INTEGER NOT NULL DEFAULT 1,
    created_at           TEXT    NOT NULL,
    ...
);
CREATE TABLE IF NOT EXISTS inbox (
    id              TEXT    PRIMARY KEY,
    task_id         TEXT    NOT NULL,
    target_agent    TEXT    NOT NULL,
    status          TEXT    NOT NULL,
    ...
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_inbox_unique_task_agent
ON inbox(task_id, target_agent)
WHERE status NOT IN ('failed', 'done', 'cancelled');
```

## Typed write boundaries
Rule: malformed payload fails loudly at the DAO edge, never silently persisted or silently dropped (`docs/ARCHITECTURE.md:57-62`).

Handoff boundary — `handoffs_dao.append` (`src/superharness/engine/handoffs_dao.py:29-50`, `src/superharness/engine/handoffs_dao.py:76-89`): `_validate_boundary` runs before any write; `VALID_PHASES = {plan, report}`, `LEGACY_PHASES = {done}` (legacy `<task>-done-<date>.yaml` filenames), status must be in `tasks_dao.VALID_STATUSES | HANDOFF_ONLY_STATUSES` where `HANDOFF_ONLY_STATUSES = {approved, plan_confirmed}` (discussion approval gate + dashboard legacy alias). Append-only, never update/delete; content is privacy-stripped before insert.

Event boundary — `events.emit` / `validate_event` (`src/superharness/engine/events.py:35-80`, `docs/ARCHITECTURE.md:81-91`): core kinds `TaskTransition`, `DispatchStarted`, `DispatchFinished` are frozen dataclasses; acceptance is structural (any frozen dataclass with non-empty `str kind` and `task_id`, e.g. `TranscriptProgress`), raising `TypeError` on wrong shape and `ValueError` on empty `task_id`, synchronously before queueing. `emit` is a no-op until `configure(project_dir)` is called, so most CLI/test processes never spawn an emitter thread; background-writer failure is warn-only so a DB outage degrades telemetry without breaking the caller.

Content-addressed dispatch context — `context_dao` (`src/superharness/engine/context_dao.py:16-80`, `src/superharness/engine/db.py:1839-1883`): `COMPONENT_TYPES = {system, task_instructions, discussion_prompt, vault_block, project_rules}`; `record_component` sha256-hashes content and `INSERT OR IGNORE`s into `context_component`; `record_dispatch` validates every type up front (no partial dispatch rows) then stores the ordered `position -> sha256` mapping in `dispatch_context_component`. Call site is best-effort (`shux delegate` warns and dispatches anyway on failure); read back via `shux diff <task-id> --context` or `last_dispatches()` / `components_for_dispatch()` (`docs/ARCHITECTURE.md:93-112`).

Verbatim boundary excerpt (`src/superharness/engine/handoffs_dao.py:29-50`):

```python
def _validate_boundary(phase: str, status: str) -> None:
    from superharness.engine.tasks_dao import VALID_STATUSES

    valid_phases = VALID_PHASES | LEGACY_PHASES
    if phase not in valid_phases:
        raise BoundaryError(
            f"Invalid handoff phase '{phase}'. Valid phases: "
            f"{', '.join(sorted(valid_phases))}"
        )
    valid_statuses = VALID_STATUSES | HANDOFF_ONLY_STATUSES
    if status not in valid_statuses:
        raise BoundaryError(
            f"Invalid handoff status '{status}'. Valid statuses: "
            f"{', '.join(sorted(valid_statuses))}"
        )
```

## Contract model
Pydantic v2 models in `src/superharness/engine/schemas.py:1-283` validate the five protocol YAML types (Contract, Handoff, Heartbeat, Profile, Inbox). `Contract` carries optional `id/goal` + `tasks/decisions/failures` lists (`src/superharness/engine/schemas.py:138-150`); `ContractTask` requires `id` + `status: TaskStatus` with optional owner, workflow, acceptance criteria, TDD plan (aliased `tdd`), blocked_by, effort, timeouts, `issue_url` snapshot pointer (`src/superharness/engine/schemas.py:92-135`); `Handoff` requires `id/task/from/to/status` (`src/superharness/engine/schemas.py:157-171`); `InboxItem` requires `id/to/task/project/status` with priority/retry defaults (`src/superharness/engine/schemas.py:255-275`).

`TaskStatus` enum (`src/superharness/engine/schemas.py:22-45`): `todo, plan_proposed, plan_approved, in_progress, report_ready, pending_user_approval, review_requested, review_passed, review_failed, pr_open, done, failed, blocked, stopped, waiting_input, paused, archived`. `InboxStatus` (`src/superharness/engine/schemas.py:48-55`): `pending, launched, running, done, failed, stale, paused`, with lifecycle `pending -> launched -> running -> done` plus `failed | stale | paused` exits (`docs/ARCHITECTURE.md:147-159`). The DB-level floor mirrors this: `tasks_dao.VALID_STATUSES = frozenset(next_action.ALL_STATUSES)` guards `update()` against typo statuses even for `force=True` callers, and v35 bakes the same vocabulary into a `CHECK (status IN (...))` constraint (`src/superharness/engine/tasks_dao.py:12-19`, `src/superharness/engine/tasks_dao.py:268-271`, `src/superharness/engine/db.py:1585-1609`).

Whole-document path `contract_io.write_contract` validates via `Contract.model_validate` (strict by default; `SUPERHARNESS_SCHEMA_ENFORCEMENT=warn` logs at CRITICAL but still writes) then, in sqlite_only mode, skips the YAML file write and upserts every task + nested subtask to SQLite via `_sqlite_sync_tasks`; `read_contract` reconstructs the doc from SQLite via `state_reader.get_contract_doc` so out-of-band `shux task status` mutations are never clobbered by stale YAML (`src/superharness/engine/contract_io.py:43-67`, `src/superharness/engine/contract_io.py:187-238`, `src/superharness/engine/contract_io.py:267-290`). Note: `engine/contract.py` is only the legacy YAML query CLI (`task_exists`, `task_status`, `latest_handoff_task` over `*.yaml` files), not the contract model itself (`src/superharness/engine/contract.py:30-171`).

Verbatim contract-lock excerpt (`src/superharness/engine/state_writer.py:155-170`):

```python
# Contract lock: freeze acceptance_criteria + tdd at plan_approved time
if status == "plan_approved" and not task_row.contract_locked_at:
    import json as _json

    snapshot = {
        "acceptance_criteria": task_row.acceptance_criteria,
        "tdd": task_row.tdd,
    }
    changes["locked_contract"] = _json.dumps(snapshot)
    changes["contract_locked_at"] = now

# Contract lock release: review_failed sends the task back to rework —
# clear the lock so the plan can be revised before the next approval.
if status == "plan_proposed" and task_row.status == "review_failed":
    changes["locked_contract"] = None
    changes["contract_locked_at"] = None
```

## Read/write paths
Canonical split (`docs/ARCHITECTURE.md:42-55`): `state_reader.py` + `state_writer.py` are the only sanctioned paths over the SQLite store; DAOs are leaves underneath.

Reader (`src/superharness/engine/state_reader.py:85-173`, `src/superharness/engine/state_reader.py:245-305`): `get_tasks / get_task / get_inbox_items / get_contract_doc / get_handoffs / get_failures / get_decisions / get_ledger_entries` each open via `get_connection`, run `init_db`, call the matching DAO, translate rows (`_inbox_row_to_yaml_shape` maps `task_id/target_agent/project_path` back to YAML `task/to/project`; `_enrich_task` reattaches `blocked_by`, stamped `workflow/require_tdd`, and `extras_json`). In production (`_production_path`: not under pytest and `is_sqlite_only`) SQLite errors propagate — no silent YAML fallback; the YAML auto-ingest helpers (`_ensure_ingested`, `_legacy_ingest_then_*`) run only inside pytest fixtures. `get_contract_doc` rebuilds `{id, goal, tasks, decisions, failures}` with id/goal from `project_meta` (`src/superharness/engine/state_reader.py:245-279`).

Writer (`src/superharness/engine/state_writer.py:82-238`, `src/superharness/engine/state_writer.py:241-320`): `set_task_status` validates the edge via `next_action.validate_status_transition` (unless `force=True` for reconciler moves), stamps lifecycle timestamps, snapshots `locked_contract` at `plan_approved`, emits `event_stream.write_event` + typed `events.TaskTransition`, auto-captures an observation on `report_ready`, ensures an active inbox row for active states, auto-records reviews on terminal statuses. `set_inbox_status` delegates timestamps to `inbox_dao.update_status` and filters extra fields through a YAML-to-SQLite column map + valid-column set. `write_handoff_to_db` maps content dict to handoff columns, stubs a minimal task row as FK guard, calls `handoffs_dao.append`, and records self-reported token/cost usage when present (`src/superharness/engine/state_writer.py:367-462`).

Error taxonomy (`src/superharness/engine/state_errors.py:4-39`): `StateError` base with `ConnectionError, SchemaError, ConcurrencyError, NotFoundError, ParityError, SingletonConflict, ContractLockError`, and `BoundaryError(StateError)` for payload-shape failures at typed boundaries. The distinction is load-bearing: `write_handoff_to_db` re-raises `BoundaryError` (caller bug) but returns False on any other exception so a storage outage never breaks the YAML export path; the DAO wraps every `sqlite3.Error` as plain `StateError` (`src/superharness/engine/state_writer.py:458-462`, `docs/ARCHITECTURE.md:75-79`).

```text
Caller ──► state_writer ──► DAO boundary ──► SQLite state.db
               │                  │
               │                  ├── valid ──► write + commit
               │                  │
               │                  └── invalid ──► BoundaryError (re-raise, caller bug)
               │
               └── sqlite3.Error ──► StateError (swallow + warn, infra failure)
Reader ◄── state_reader ◄── DAO ◄── SQLite state.db (prod: errors propagate)
```

**Covers:** `docs/ARCHITECTURE.md`, `protocol/spec.md`, `src/superharness/engine/db.py`, `src/superharness/engine/sqlite_only.py`, `src/superharness/engine/contract.py`, `src/superharness/engine/contract_io.py`, `src/superharness/engine/schemas.py`, `src/superharness/engine/tasks_dao.py`, `src/superharness/engine/inbox_dao.py`, `src/superharness/engine/ledger_dao.py`, `src/superharness/engine/handoffs_dao.py`, `src/superharness/engine/context_dao.py`, `src/superharness/engine/events.py`, `src/superharness/engine/state_reader.py`, `src/superharness/engine/state_writer.py`, `src/superharness/engine/state_errors.py`, `src/superharness/utils/paths.py`
