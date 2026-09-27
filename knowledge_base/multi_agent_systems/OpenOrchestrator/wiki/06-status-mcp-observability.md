> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Status Store, MCP Peers, Environment, Observability

**In one sentence:** A shared SQLite database is the system's memory — agent hooks write status, every reader polls it, MCP peer messages ride in the same tables — while `owt` itself never calls an LLM.

## Key points

- **owt calls no LLM and no external API.** The LLM is the client: the coding agent (Claude/Droid/Pi/OpenCode) runs in the worktree pane and reports back via hooks, `owt hook`, status writes, and the optional MCP peer server.
- State lives in SQLite `status.db` (`~/.open-orchestrator/status.db`, overridable via `$OWT_DB_PATH`): schema v3.3 in `core/status_schema.py:70-176` with tables `worktree_status` (16 cols), `shared_notes`, `metadata`, `peer_messages`, `usage_events`; legacy `ai_status.json` is migrated once.
- Concurrency is SQLite WAL + `busy_timeout=5000` + `synchronous=NORMAL` (`core/_db.py:52-83`); every write is `INSERT OR REPLACE` + commit; readers always read fresh (`reload()` is a documented no-op, `core/status.py:93-94`); change detection is a `MAX(updated_at):COUNT(*)` token (`core/status.py:96-107`).
- Lifecycle values `AIActivityStatus` (`models/status.py:16-26`): terminal = waiting/completed/error (`core/status_policy.py:29-41`); attention = blocked/error (:44-46). Writes come from hooks and `record_command` (idle/waiting/blocked → working on agent input, `core/status.py:243-260`).
- MCP peer messaging is an opt-in extra (`pip install open-orchestrator[mcp]`): one stdio server per agent (`python -m open_orchestrator.core.mcp_peer`) exposing `list_peers / send_message / check_messages` (+ `set_summary`, `get_peer_files`); loopback-only bind; peer messages are a named prompt-injection source in the threat model.
- `owt new` builds a reproducible nest: dependency install per detected package manager, `.env` copy with path-key rewriting (atomic, `0o600`), CLAUDE.md injection with idempotent markers, and hook installation gated on `supports_hooks` (Claude/Droid only).
- Observability: ContextVar correlation IDs + per-worktree context with a JSON log formatter (`--log-format json`), and a `{"status":"ok|error","data":…}` machine envelope for CLI output.

---

## Persistence and lifecycle

Schema bootstrap is `ensure_schema` (`core/status_schema.py:361-371`); DB path resolution prefers `$OWT_DB_PATH`, then `~/.open-orchestrator/status.db`, with a repo-local/temp fallback when home is unwritable (:390-459); files are `chmod 0o600` (:482-483, `core/_db.py:24-49`). Writers: `StatusTracker.set_status/update_task/mark_completed/mark_idle/mark_stalled/set_notes/initialize_status/remove_status` (`core/status.py:126-314`); the hook entry `owt hook --event …` funnels into `update_task` (`commands/agent.py:200-236`); usage and notes at `core/status.py:316-343`. Readers: `get_status/get_all_statuses/get_summary/get_generation/has_changed_since` (:96-120, :345-373); `get_backend_session` rebuilds the recorded session (:167-192); health at :501-517.

```python
# core/status_schema.py:232-264 — the write path (structure)
INSERT OR REPLACE INTO worktree_status
  (worktree_name, worktree_path, branch, tmux_session, ai_tool,
   activity_status, current_task, last_task_update, notes,
   modified_files, backend_kind, backend_session_id, backend_meta,
   session_type, created_at, updated_at)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
```

Policy (`core/status_policy.py`): terminal `waiting, completed, error` (:29-41); attention `blocked, error` (:44-46); working (:49-51); backend `summary_bucket` maps waiting→idle (:54-66) while frontend `ui_bucket` maps waiting+blocked→waiting (:69-75). The orchestrator runtime consumes this in `evaluate_completion` (`core/runtime.py:96-197`: terminal→completed/failed, non-working→running, plus tmux/pane and commit inspection).

## MCP peers, environment, logging

MCP server lifecycle (`core/mcp_peer.py:1-16, :65-88`): spawned per-agent over stdio with `OWT_WORKTREE_NAME`/`OWT_DB_PATH` in env; activates only when `import mcp` succeeds, else graceful skip (:15, :130-144). Tools: `list_peers` (all rows except self, :90-106); `send_message(to_peer|"*")` with broadcast fan-out (:108-129); `check_messages(mark_read=True)` inbox + auto-ack (:131-147); `set_summary`, `get_peer_files` (:149-170). Tracker-side inbox: `store_message/get_unread_messages/mark_messages_read/purge_old_messages` (`core/status.py:447-493`). Isolation: loopback-only bind, no override flag (:37-54, :80, :181).

```python
# core/mcp_peer.py:131-147 — inbox read (structure)
SELECT id, from_peer, message, created_at FROM peer_messages
  WHERE to_peer = ? AND read = 0 ORDER BY created_at
```

Environment on `owt new`: `_setup_pane_environment` → `EnvironmentSetup.setup_worktree` (`core/pane_actions.py:174-190`); headless path also installs hooks + `initialize_status` + initial `update_task(WORKING)` (`core/agent_launcher.py:400-438`; hook+status init `core/pane_actions.py:206-249`). Dependency commands per manager (`uv sync`, `pip install -r…`, `npm install`, …) at `core/environment.py:74-95`; binaries resolved via safe-PATH `resolve_binary` (anti worktree-planted binary, :159-175 + `core/_path.py:174-199`); installs run `subprocess.run(timeout=300)` streamed to a tempfile (:137-212); timeout classes (`AI_CLI` 600 s → mark stalled) in `core/_subprocess.py:30-96`. `.env` copy + path-key rewrite + atomic `0o600` at `core/environment.py:214-324` (patterns :56-63); extra configs at :326-382. CLAUDE.md: copy `.claude/CLAUDE.md` + `CLAUDE.md` (`core/environment_claude_md.py:23-76`) with idempotent `<!-- OWT-<ID>-START/END -->` markers (:79-119); project context injected at `core/pane_actions.py:194-200`. Hooks install only when `supports_hooks` (Claude/Droid true; Pi/custom false — `core/hooks.py:26-47`, `core/tool_registry.py:86-101, :133-141, :172-180`): Claude `UserPromptSubmit→working`, `Stop→waiting`, `Notification(permission_prompt)→blocked` with `OWT_DB_PATH=` prefix plus the `owt-peers` MCP stanza (:56-148); Droid mirror in `.factory/settings.json` (:151-217).

Logging: ContextVars `correlation_id/current_worktree/current_component` + `StructuredLogFilter` (`utils/logging.py:15-31`); `JsonFormatter` one-JSON-per-line with `extra=` promoted (:63-102); `log_event(event, …)` helper (:105-119); `configure_logging(verbose, json_format)` (:122-153); CLI `--log-format text|json --verbose` (`cli.py:21, :62-65`); machine envelope `{"status":"ok|error","data":…}` (`utils/output.py:40-62`). Security posture (loopback-only peers, shell-argv invariants, hook threat model) is written up in `docs/security.md`.

**Covers:** `core/status.py`, `core/status_schema.py`, `core/status_policy.py`, `core/mcp_peer.py`, `core/runtime.py`, `core/environment.py`, `core/environment_claude_md.py`, `core/hooks.py`, `core/_db.py`, `core/_path.py`, `core/_subprocess.py`, `utils/io.py`, `utils/output.py`, `utils/logging.py`, `models/status.py`, `docs/security.md`
