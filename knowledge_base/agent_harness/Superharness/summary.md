# Technical Analysis: superharness

**Repository:** https://github.com/artificemachine/superharness
**Version analyzed:** 1.84.1 (commit 9c2166dccac6717b8b4056a8eae87c44052d77d5, 2026-08-28)
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves

Running several AI coding agents (Claude Code, Codex CLI, Gemini CLI, opencode, Pi) against one project causes collisions: two agents edit the same files, push to the same branch, or duplicate each other's work with no shared memory. Superharness solves this with a coordination layer, not another agent. One per-project SQLite database (`state.db`) is the sole runtime authority for tasks, queue rows, handoffs, and audit trail; all writes pass through typed Data Access Object (DAO, a small class that owns all reads/writes for one table) boundaries that reject malformed payloads loudly at the edge.

On top of that contract sit three mechanisms: a queue delegation pipeline (`shux delegate` writes an inbox row, a watcher loop dispatches it through a per-harness adapter that spawns the external agent CLI), lifecycle rules (a status state machine plus timeout reconcilers that auto-fail, archive, or revert stuck work), and crash recovery (heartbeats, zombie reaping, git-stash checkpoints, append-only handoffs so a respawned worker inherits full context). The primary user is a human operator running AI coding agents from the `shux` command line, with an optional loopback-only dashboard and background daemons for unattended operation.

## 2. High-Level Architecture

```text
Operator ──► shux CLI (cli.py) ──► commands/ ──► engine/ ──► SQLite state.db
                                      │              ▲
                                      ▼              │
                               harness adapters ─► Agents (Claude / Codex / Gemini / opencode / Pi)
Operator service ──► Watcher/dispatcher (inbox_watch.py) ──► engine/
Loopback dashboard ──► engine/ ◄── Operator
```

(Topology from `docs/ARCHITECTURE.md:21-40`; CLI is a thin Click entry point at `src/superharness/cli.py`, per-command validation in `src/superharness/commands/`, reusable state machine and DAOs in `src/superharness/engine/` per `docs/ARCHITECTURE.md:37-55`.)

Data flow for `shux delegate --id TASK --to claude-code`:

1. `delegate` validates project dir, workflow status gate (`src/superharness/commands/delegate.py:912-946`), then preflight (`src/superharness/commands/delegate.py:952-977`).
2. Enqueue writes one `pending` inbox row via `inbox_dao.enqueue` plus a ledger record (`src/superharness/commands/inbox_enqueue.py:30-67`), deduped on active `(task_id, target_agent)` (`src/superharness/engine/inbox_dao.py:56-79`).
3. Watcher claims atomically (`UPDATE ... WHERE status='pending' ... RETURNING *`, `src/superharness/engine/inbox_dao.py:161-176`) and launches the agent through the harness adapter's `build_invocation` (`src/superharness/harnesses/base.py:37-39`).
4. During the run the agent/CLI writes heartbeats (`src/superharness/engine/heartbeat_dao.py:35`) and typed events (`src/superharness/engine/events.py:199`); the watcher tails transcripts via byte-offset cursors (`src/superharness/engine/transcript_tail.py:97-128`).
5. The agent writes a `plan`/`report` handoff through the DAO boundary (`src/superharness/engine/handoffs_dao.py:29-50`) and the ledger records the trace (`src/superharness/engine/ledger_dao.py:25-54`).
6. `shux status`/`close` reads via `state_reader` and verifies gates before `done` (`src/superharness/commands/close.py:89-99`).

Persistent state lives in one per-project SQLite file at `$XDG_STATE_HOME/superharness/<12-char-project-hash>/state.db` (XDG, a standard for where apps store data files, aware; overridable by `SUPERHARNESS_STATE_DIR`), with fail-closed conflict errors on split-brain roots (`src/superharness/utils/paths.py:135-165`, `docs/ARCHITECTURE.md:118-131`).

## 3. The Shared Contract (core abstraction)

Representation: SQLite tables `tasks`, `inbox`, `handoffs`, `ledger`, `decisions`, `failures`, `discussions`, `heartbeats` (`agent_heartbeats`), `events` — created in v1 migration (`src/superharness/engine/db.py:617-813`) and extended across 39 ordered migrations (`src/superharness/engine/db.py:20`, `src/superharness/engine/db.py:1886-1926`). Pydantic v2 models in `src/superharness/engine/schemas.py:1-283` validate the five protocol types; `TaskStatus` enum (`src/superharness/engine/schemas.py:22-45`) lists 17 states (`todo` … `archived`), `InboxStatus` (`src/superharness/engine/schemas.py:48-55`) lists 7 (`pending` … `paused`).

Typed write boundaries: handoff writes gate `phase ∈ {plan, report}` (+ legacy `done`) and status ∈ task enum + `{approved, plan_confirmed}`, else `BoundaryError` (`src/superharness/engine/handoffs_dao.py:14-50`); event writes validate structurally (frozen dataclass with non-empty `kind` + `task_id`), raising `TypeError`/`ValueError` synchronously (`src/superharness/engine/events.py:70-80`); dispatch prompt ingredients are content-addressed (`context_component` keyed by sha256, closed 5-value `COMPONENT_TYPES`, `src/superharness/engine/context_dao.py:16-32`). Reads go through `state_reader` (`src/superharness/engine/state_reader.py:129-173`), writes through `state_writer` with transition validation and contract lock (`src/superharness/engine/state_writer.py:155-170`, `src/superharness/engine/state_writer.py:367-462`); `BoundaryError` (caller bug, re-raised) is distinguished from `StateError` (infrastructure, swallowed on best-effort paths) (`src/superharness/engine/state_errors.py:4-39`). Knobs: `SUPERHARNESS_STATE_DIR` / `SUPERHARNESS_STATE_PROJECT` for DB location, `SUPERHARNESS_JOURNAL_MODE` for WAL vs PERSIST (`src/superharness/engine/db.py:161-233`), `SUPERHARNESS_SCHEMA_ENFORCEMENT=warn` to soften contract validation (`src/superharness/engine/contract_io.py:43-67`).

## 4. LLM / External Service Integration

The repo does NOT route main agent work through its own LLM calls — agents are external CLIs spawned by adapters (`build_invocation` returns argv/env/cwd, `src/superharness/harnesses/base.py:93-132`). Design: pure coordination layer; the LLM is the worker, not the server. But it does call LLMs itself for auxiliary tasks:

- **Summarizer** (`src/superharness/engine/summarizer_providers.py:1-435`): providers are Anthropic (`ANTHROPIC_API_KEY`, default `claude-haiku-4-5-20251001`), Gemini (`GEMINI_API_KEY`/`GOOGLE_API_KEY`, default `gemini-2.0-flash`), OpenAI (`OPENAI_API_KEY`, default `gpt-4o-mini`), OpenRouter (`OPENROUTER_API_KEY`, default `anthropic/claude-haiku-4.5`), plus experimental CLI-subprocess summarizers (opencode, Claude Code — binary must be on PATH). HTTP uses stdlib `urllib`, no provider SDKs pinned. All optional — construction raises `SummarizerError` when credentials are missing, and the auto-capture caller swallows faults.
- **Model router / fallback** (`src/superharness/engine/model_router.py:42-887`): `resolve_model` (line 807), `cheap_model` returns the mini-tier model for summarizer-class calls (line 77); valid tiers are exactly `{mini, standard, max}`; `model_fallback.py` exists as a companion.
- **Distiller / skill extraction** (`src/superharness/engine/distiller.py:27-137` extracts ≤3 lessons via an injected `llm_fn`; `src/superharness/engine/skill_extractor.py:212-360` records skills on task completion; `src/superharness/commands/insights.py` surfaces them).
- **Observability extra**: `langfuse` is the only optional dependency (`langfuse>=4.7,<5`), enabled only by `SUPERHARNESS_LANGFUSE_ENABLED` plus credentials, `DO_NOT_TRACK` is an absolute opt-out (`src/superharness/engine/langfuse_telemetry.py:51-143`); per-dispatch export is pseudonymized (`task_id_hash`, no content).

## 5. The Delegation Pipeline (main pipeline)

1. **Onboard** (`src/superharness/commands/onboard.py`): scaffolds `.superharness/` project state. Input: project dir → output: initialized state dir + profile.
2. **Task create** (`src/superharness/commands/task.py:548-555`): validates status transitions via `next_action.validate_status_transition` (`src/superharness/engine/next_action.py:371-392`) and dispatch-readiness per workflow (`src/superharness/engine/next_action.py:233-287`). Input: title/owner/workflow → output: task row (`status=todo`).
3. **Enqueue** (`src/superharness/commands/inbox_enqueue.py:206-239`): validates agent/priority, applies workflow status gates (`src/superharness/commands/inbox_enqueue.py:158-184`), inserts `pending` row + ledger record (`src/superharness/commands/inbox_enqueue.py:30-67`). Input: task-id + agent → output: inbox row id.
4. **Dispatch** (`src/superharness/commands/inbox_dispatch.py:777-866`): mkdir lock (`src/superharness/commands/inbox_dispatch.py:105-120`), atomic `claim_next` (`src/superharness/engine/inbox_dao.py:144-176`), execution-context guards — effort timeouts, isolated git worktree for Pi, dirty-worktree pause, `blocked_by` dependency check (`src/superharness/commands/inbox_dispatch.py:2093-2192`) — then harness `build_invocation` + spawn.
5. **Watch** (`src/superharness/commands/inbox_watch.py:5381-5470`): single-cycle or poll loop, watcher heartbeat each tick (`src/superharness/commands/inbox_watch.py:610-639`), zombie/stale/orphan reconcilers (`src/superharness/commands/inbox_watch.py:3673-3792`, `src/superharness/commands/inbox_watch.py:5210-5235`), lifecycle timeout rules (`src/superharness/engine/lifecycle_rules.py:47-164`), dual watchdog on event silence/ceiling (`src/superharness/engine/lifecycle_rules.py:394-468`).
6. **Handoff** (`src/superharness/commands/handoff_write.py:150-322` → `state_writer.write_handoff_to_db`, `src/superharness/engine/state_writer.py:367-462`): plan payload (status `plan_proposed`) or report payload (status `report_ready`), boundary-validated, YAML export best-effort.
7. **Verify/close/archive** (`src/superharness/commands/close.py:89-336`): ownership + status (`report_ready`/`review_passed`) + subtask gate + `verified=true` gates, then `status=done`, ledger CLOSE line, worktree cleanup.

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `src/superharness/commands/inbox_watch.py` | 5594 | Watcher loop, heartbeats, zombie/stale/consensus reconcilers, auto-recover |
| `src/superharness/commands/inbox_dispatch.py` | 2404 | Claim-next, execution-context guards, harness launch, reconcile |
| `src/superharness/engine/db.py` | 1926 | 39 migrations, connection setup (WAL/PERSIST, FK, busy timeout), schema |
| `src/superharness/commands/delegate.py` | 1780 | Status gate, preflight, prompt build, harness launch |
| `src/superharness/cli.py` | 1493 | Click entry point (`shux`/`superharness`), subcommand registration |
| `src/superharness/engine/model_router.py` | 1100 | Tier resolution, ChatGPT-auth overrides, fleet failover |
| `src/superharness/engine/state_writer.py` | 827 | Status transitions, contract lock, handoff/event writes |
| `src/superharness/engine/lifecycle_rules.py` | 583 | Timeout rule table, deadlines, dual watchdog checks |
| `src/superharness/engine/inbox_dao.py` | 463 | Inbox rows, atomic claim, retry/reassign/recover, stale scan |
| `src/superharness/state_reader.py` / `engine/state_reader.py` | 442 | Canonical read path, YAML-shape translation, contract rebuild |
| `src/superharness/engine/summarizer_providers.py` | 435 | Anthropic/Gemini/OpenAI/OpenRouter/CLI summarizers |
| `src/superharness/commands/inbox_enqueue.py` | 429 | Enqueue validation, workflow gates, ledger transaction |
| `src/superharness/engine/next_action.py` | 392 | Status graph `_MAPPING`, transition validation, workflow dispatch sets |
| `src/superharness/engine/adapter_registry.py` | 356 | Manifest load/validate, launcher + model-tier resolution |
| `src/superharness/engine/schemas.py` | 283 | Pydantic `TaskStatus`/`InboxStatus`/Contract/Handoff/Inbox models |
| `src/superharness/engine/events.py` | 218 | Typed event dataclasses, background emitter, sync validation |
| `src/superharness/engine/benchmark.py` | 216 | JSONL leaderboard records, aggregate, Langfuse hook |
| `src/superharness/engine/handoffs_dao.py` | 202 | Phase/status boundary gate, append-only history |
| `src/superharness/harnesses/base.py` | 132 | `Harness` protocol, `Invocation`, generic argv builder |
| `src/superharness/engine/liveness.py` | 59 | `is_fresh` TTL check, watcher heartbeat stamp |

(Line counts via `wc -l` on the clone.)

## 7. Dependencies

Required (from `pyproject.toml` `dependencies`, verbatim):

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| click | `>=8.3.3` | CLI framework for `shux` commands |
| pyyaml | `>=6.0` | YAML protocol files (legacy/export) |
| ruamel.yaml | `>=0.18` | Round-trip YAML preservation |
| pydantic | `>=2.0,<3` | Contract/handoff/inbox schema validation |
| fastmcp | `>=0.4` | MCP (Model Context Protocol, a standard for exposing tools to agents) server |
| requests | `>=2.31` | HTTP transport |
| cryptography | `>=50.0.0` | CVE (public security-bug ID) floor on FastMCP/MCP transitives |
| idna | `>=3.15` | CVE floor on transitives |
| joserfc | `>=1.6.8` | CVE floor on transitives |
| mcp | `>=1.28.1,<3` | MCP protocol library |
| pydantic-settings | `>=2.14.2` | Settings management |
| pygments | `>=2.20.0` | CVE floor / syntax highlighting |
| pyjwt | `>=2.13.0` | CVE floor (JWT auth tokens) |
| starlette | `>=1.3.1` | CVE floor (ASGI web layer under MCP) |
| python-multipart | `>=0.0.31` | CVE floor (multipart form parsing) |

Observability extra: `langfuse>=4.7,<5` (only optional dependency). CVE floors are pinned by contract test `tests/contract/test_dependency_security_floors.py` (exists in clone), which must stay aligned with the comment in `pyproject.toml`.

## 8. CLI / Usage Surface

Entry points (`[project.scripts]`): `superharness = "superharness.cli:main"`, `shux = "superharness.cli:main"`. Commands (under `src/superharness/commands/`): `onboard`, `delegate`, `task`, `inbox_enqueue`/`inbox_dispatch`/`inbox_watch`/`inbox_recover`/`inbox_gc`, `discuss`/`discussion_dispatch`/`talk`, `handoff_write`/`handoff_generate`, `status`, `close`, `verify`, `worktree`, `daemon`/`daemon_monitor`, `benchmark`, `adapters`/`adapter_payload`, `auto_dispatch`, `distill`, `insights`, `doctor`, `tui`, `dashboard`, `pack`, `migrate_state`, plus ~30 more (full list in section 5 source: commands dir holds 60+ modules).

| Env var | Effect |
|---------|--------|
| `SUPERHARNESS_STATE_DIR` | Overrides DB root |
| `SUPERHARNESS_STATE_PROJECT` | Lets a worktree reuse parent state |
| `SUPERHARNESS_JOURNAL_MODE` | Overrides WAL/PERSIST journal mode |
| `SUPERHARNESS_SCHEMA_ENFORCEMENT=warn` | Softens contract validation |
| `SUPERHARNESS_LANGFUSE_ENABLED` + keys | Enables Langfuse export; `DO_NOT_TRACK` opts out |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `OPENROUTER_API_KEY` / `GEMINI_API_KEY` | Summarizer provider credentials |

| Path | Role |
|------|------|
| `$XDG_STATE_HOME/superharness/<hash>/state.db` | Authoritative per-project SQLite DB |
| `.superharness/handoffs/` | YAML handoff export (best-effort) |
| `.superharness/daemon-state.json` | Daemon tracking state |
| `.superharness/modules/*.yaml` | Enabled module hook packs |
| `.superharness/skills.yaml` | Extracted skill library |

## 9. Extensibility Points

- **New harness**: implement the `Harness` protocol (`build_invocation` + optional `discover_models`, `src/superharness/harnesses/base.py:33-51`), register the live object in `harnesses/__init__.py`, and ship a YAML manifest (`name/version/type/launcher_script/capabilities/model_tiers/requires/validation`, parsed at `src/superharness/engine/adapter_registry.py:103-187`) plus a `scripts/delegate-to-<name>.sh` launcher. Parity tests (`tests/unit/test_harness_adapters.py:37-123`) pin argv equality.
- **New module**: drop a YAML hook pack into `src/superharness/module_templates/` (format: `schema_version/name/description/enabled/detect/hooks.<event>.action/settings`, e.g. `ship.yaml:1-10`); `load_modules` reads `.superharness/modules/*.yaml` (`src/superharness/modules/loader.py:63`) and `run_hooks(event, context, project_dir)` fires matches (`src/superharness/modules/runner.py:57`).
- **New CLI command**: add a module under `src/superharness/commands/` and register it in `src/superharness/cli.py` (the `_register_*` functions, `src/superharness/cli.py:1-1493`); commands call `state_writer`/`state_reader`, never raw SQL.
- **New telemetry event kind**: define a frozen dataclass with non-empty `kind` + `task_id` (like `TaskTransition`, `src/superharness/engine/events.py:35-50`) — acceptance is structural, so no registry change is needed; emit via `emit()` after `configure()` (`src/superharness/engine/events.py:187-199`).

## 10. Limitations and Gotchas

- **VERSION file stale vs pyproject**: `VERSION` in the clone reads `1.77.0` while `pyproject.toml` says `1.84.1` — do not trust the VERSION file.
- **`inbox_watch.py` is a 5594-line god module**: watcher loop, a dozen reconcilers, auto-approval, auto-recover, and GC all live in one file (`src/superharness/commands/inbox_watch.py:1-5594`), making changes risky.
- **YAML legacy split-brain risk**: production reads SQLite only, but YAML auto-ingest still runs under pytest and legacy `.superharness/state.sqlite3` roots can conflict — resolution fails closed with `StateDatabaseConflictError` (`src/superharness/utils/paths.py:135-165`) rather than merging, so misconfigured worktrees error instead of syncing.
- **Watcher silent-death history**: a documented 19+-hour silent outage with no alert motivated the three-layer supervision (daemon monitor respawn, launchd/systemd daemon, macOS self-heal) — see `docs/bugs/BUGREPORT-watcher-silent-death-no-recovery.md:12` and `src/superharness/commands/daemon_monitor.py:42-109`.
- **Dashboard/CLI DB-path divergence bug class**: any consumer resolving the DB path differently from `resolve_active_state_db_path` silently reads a different database; the fail-closed conflict error is the only guard.
- **Test count vs e2e coverage**: README claims about test suite size were not verified in source (per README; not verified in source) — unit/parity/contract tests are strong (golden argv, enforcement parity, dual-watchdog regressions), but full multi-agent e2e runs are inherently environment-dependent.

## 11. How It Compares to Alternatives

- **Beads** (issue-tracker DB): Beads gives agents a shared SQLite-backed issue graph with dependencies, but has no harness adapters, no process spawning, and no lifecycle/watchdog layer — it tracks work, while superharness launches and supervises the workers doing it. Tradeoff: Beads is simpler and agent-agnostic; superharness is heavier but closes the loop.
- **Claude Squad / tmux orchestration**: tmux-based multi-agent runners multiplex terminal sessions for parallel agents but share no typed contract — coordination is visual (panes) rather than programmatic (status graphs, gates, ledger). Tradeoff: tmux is transparent and debuggable; superharness adds enforcement at the cost of a state layer to maintain. In-repo `docs/ARCH-exo-vs-superharness.md` covers a similar external-orchestrator comparison.
- **OpenClaw / Clawdbot-style gateway agents**: gateway architectures route everything through one always-on agent process with tools, whereas superharness is agent-neutral — five harness adapters behind one protocol, with per-harness launcher scripts and manifests. Tradeoff: gateways centralize skill/tool logic; superharness centralizes only the contract and lets each CLI keep its own strengths. In-repo `docs/AUDIT-pi-hermes-adaptation.md` and `hermes-integration-tdd-plan.md` discuss adjacent Hermes/Pi integration tradeoffs.
- **LangGraph Supervisor / AutoGen Magentic-One**: framework-level orchestrators compose LLM agents as in-process graphs with code-defined edges, while superharness orchestrates at the OS/process layer (SQLite + subprocess + git worktrees) with no LLM in the loop of the coordinator itself. Tradeoff: frameworks give fine-grained control-flow; superharness gives crash-safe, language-agnostic supervision of black-box CLIs.

Positioning in one sentence: superharness is the process-and-contract supervisor for black-box coding-agent CLIs, not another agent framework — SQLite is the shared memory, adapters are the hands, and gates/watchdogs are the immune system.

## Appendix: Selected Code Snippets

**Harness protocol** (`src/superharness/harnesses/base.py:33-51`):

```python
@runtime_checkable
class Harness(Protocol):
    name: str

    def build_invocation(
        self, task: dict, project_dir: str, non_interactive: bool
    ) -> Invocation: ...

    def discover_models(
        self, auth_mode: str = "unknown"
    ) -> list["DiscoveredModel"]:
        """Return models available on this host for the given auth mode.
        ...
        """
        return []
```

**Atomic inbox dispatch claim** (`src/superharness/engine/inbox_dao.py:161-176`):

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

**Dual-watchdog checks** (`src/superharness/engine/lifecycle_rules.py:485-505`):

```python
if absolute_ceiling > 0 and age >= absolute_ceiling:
    reason = (
        f"absolute ceiling exceeded ({int(age)}m elapsed >= "
        f"{absolute_ceiling}m ceiling) — task was in status '{status}'"
    )
    ...
if idle_timeout > 0 and last_event_age >= idle_timeout:
    reason = (
        f"idle timeout exceeded (no events for {int(last_event_age)}m >= "
        f"{idle_timeout}m idle limit) — task was in status '{status}'"
    )
```

**Watcher liveness check** (`src/superharness/engine/liveness.py:23-37`):

```python
def is_fresh(ts_str: str | None, ttl_seconds: int = WATCHER_TTL_SECONDS) -> bool:
    if not ts_str or not isinstance(ts_str, str):
        return False
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except ValueError:
        return False
    ...
    return age < ttl_seconds
```
