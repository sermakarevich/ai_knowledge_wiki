> [[index|Wiki]] | [[summary|Summary]]

# OpenOrchestrator (`owt`) — Digest

The whole source at medium depth: every component's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-control-plane-cockpit|Control-Plane Cockpit (Textual TUI)]]

**In one sentence:** A deliberately thin Textual decision surface that polls worktree status every 2 seconds, sorts rows into three priority lanes, and dispatches single-key verb actions to `owt` subprocesses — all business logic lives outside the view.

- The lane model is a 3-value enum `SectionKind` (`NEEDS_YOU / READY_TO_SHIP / IN FLIGHT`) in `models/control_plane.py:18-28`; classification lives in `core/control_plane_sections.py`, not the view.
- NEEDS YOU = leftover merge/rebase state (MERGE_HEAD check) sorted first plus BLOCKED/ERROR tracker rows; READY TO SHIP = merge-queue candidates as `(name, commits_ahead, overlaps)` tuples; IN FLIGHT = WORKING rows sorted by recency.
- Empty lanes are hidden with CSS (`.empty{display:none}`), so the most important lane is always on top.
- Every row carries verb actions (`s`hip, `a`ttach, `d`iff, `f`ix, `m`erge, `x`delete); the footer renders only the focused row's keys, rebuilt on every render.
- The view is stateless about work: a 2-second poll (`REFRESH_SECONDS = 2.0`) rebuilds sections off-thread; there are no reactive watchers.
- `fix` opens `$EDITOR` and exits the cockpit (hands control to the human); `attach`/`diff` suspend the TUI and exec into the session/pager; `ship`/`merge` run as `owt` subprocesses.

## 2. [[wiki/02-multiplexer-backends|Pluggable Multiplexer Backends (tmux / herdr)]]

**In one sentence:** A single `MultiplexerBackend` protocol fronts tmux (default) and herdr (opt-in) so no CLI command ever touches session machinery directly, and each worktree row remembers which backend owns it.

- The abstraction is `MultiplexerBackend`, a runtime-checkable `Protocol` in `core/multiplexer.py:18`, with `create_session / session_for / send_text / send_keys / read_recent / attach / kill / is_alive / report_agent_state`.
- Backend identity is data: `BackendKind` (`TMUX`/`HERDR`) and `BackendSession(kind, id, worktree_name, meta)` in `models/backend.py:16-35`; status rows carry `backend_kind/backend_session_id/backend_meta` so reattach needs no flags.
- tmux sessions are named `owt-{sanitized}` (`core/tmux_manager.py:202-205`); prompt delivery uses `send-keys`, with a `load-buffer/paste-buffer` path for large prompts and `capture-pane` polling for agent readiness.
- herdr talks newline-delimited JSON-RPC over a Unix socket (`core/herdr_client.py:82-163`); one owt worktree maps to one herdr workspace with the agent in the root pane.
- Backend selection (`core/backend_factory.py:78-117`): explicit `--herdr/--tmux` flag beats config `[backend] mode` (`tmux|herdr|auto`, default `tmux`); `auto` uses herdr only if a live daemon is detected.
- `owt attach` resolves the recorded backend for the session (`commands/worktree/attach.py:41-61`); the cockpit suspends the TUI and execs into it. herdr attach execs `herdr agent attach <pane>`; tmux attach uses `attach-session`/`switch-client`.
- Interactive relaunch on an existing tmux session reuses it instead of double-spawning (`core/agent_launcher.py:354-367`).

## 3. [[wiki/03-harness-plugin-layer|Harness Plugin Layer (multi-provider AI tools)]]

**In one sentence:** A registry plus a small tool protocol abstracts every coding agent behind one launch pipeline, so built-ins (Claude, Pi, Droid, OpenCode, ClawCore) and config-registered custom tools are launched identically from `owt new --ai-tool <name>`.

- The contract is `AIToolProtocol` (`core/tool_protocol.py:14-99`): `name/binary/supports_hooks/supports_headless/supports_plan_mode/task_via_args/install_hint` plus `get_command/is_installed/get_known_paths/install_hooks`.
- Built-ins are bespoke classes in `core/tool_registry.py`: `claude` (:96-141), `droid` (:144-180), `pi` (:183-232), `opencode` (:235-271), one-shot `clawcore` (:325-352, `task_via_args=True`), plus plain `CustomTool` entries for codex/gemini/aider/amp/kilo-code (:277-283, registered :362-369).
- Custom tools need no code changes: `[tools.<name>]` tables in config (`binary`, `command_template`, `prompt_flag`, capability flags) are registered before validation in `load_config` (`config.py:322-326`), so validators accept the new names.
- One-shot argv tools substitute shell-quoted `{{task}}`/`{{worktree}}` into `command_template` (`core/tool_registry.py:67-74`); paste-based REPL tools receive the prompt through the multiplexer instead.
- Auto-detection priority is `claude > pi > droid > opencode` (`core/agent_detector.py:14`); one installed tool is auto-picked, several produce an interactive numbered picker (`commands/worktree/_shared.py:24-41`).
- `--workflow` is plan-first framing, not a separate engine: the task classifier (`core/prompt_builder.py:34-43`) picks a protocol preamble that is prepended to the prompt (`commands/worktree/new.py:162-170`).
- Headless mode shells out with stdin piping and requires `supports_headless` (only Claude and Pi); it is incompatible with `--herdr/--workflow/--in-place`.

## 4. [[wiki/04-merge-queue-conflict-guard|Merge, Conflict Guard, Queue, Worktree Lifecycle]]

**In one sentence:** Shipping is a two-phase merge (update the feature branch first, then the base) guarded by file-overlap warnings from the status database, ordered by a smallest-first queue, with PR-based shipping and full teardown as the exits.

- Conflict Guard is file-overlap detection, not semantic merge prediction: `get_modified_files` runs `git diff --name-only {base}...{branch}` (`core/merge.py:183-189`); `check_file_overlaps` (:191-213) intersects that set with peers' `modified_files` from the status DB (not live diffs of peer worktrees).
- The pre-merge warning is advisory only: `commands/merge_cmds.py:322-328` prints the top-5 overlaps before confirmation but never blocks.
- Two-phase merge (`MergeManager.merge`, `core/merge.py:328-438`): phase 1 merges/rebases the base into the feature branch inside the worktree (:440-491); phase 2 checks out the base in the main checkout, merges the feature, and restores branch + autostash (:522-574). Any phase-1 conflict aborts before phase 2 is attempted.
- Options: `--rebase` (rebase path :471-491), `--strategy ours|theirs` → `merge -X <strategy>` (:503-507), `--leave-conflicts` skips the abort and leaves the merge/rebase in progress (:487-490, :514-518). `ship --pr` rejects all three (`commands/merge_cmds.py:417-420`).
- Queue ordering (`plan_merge_order`, `core/merge.py:283-326`): only COMPLETED/WAITING rows; each candidate scores `(commits_ahead, overlap_count)`; sort is smallest-first unless an explicit DAG `dependency_order` is supplied. Branch age and size play no role.
- `queue --ship` (`commands/merge_cmds.py:575-606`) merges in order with worktree deletion and stops at the first conflict.
- PR shipping (`create_pr`, `core/merge.py:231-281`): push + `gh pr create --fill`; the worktree, session, and status stay intact — only the status flips to WAITING (`commands/merge_cmds.py:103-111`).
- Worktree creation wires branch naming, dependency install, `.env` copy, and hooks; deletion is a best-effort full teardown; `owt doctor` finds orphans across worktrees, branches, sessions, and status rows without auto-deleting session-less directories.

## 5. [[wiki/05-cli-config-models|CLI Surface, Config, Models]]

**In one sentence:** A Click command group where bare `owt` opens the cockpit and every cockpit verb has a scripting-grade CLI twin, configured by layered TOML files and typed by Pydantic models.

- Entry points (`pyproject.toml:51-53`): `owt = open_orchestrator.cli:main`, `owt-popup = open_orchestrator.popup.picker:main`; `cli.py:19` declares the Click group with `--json/--theme/--verbose/--log-format/--profile`, and no subcommand launches `ControlPlaneApp().run()` (:88-97).
- The verb inventory covers the full lifecycle: `new/branch/list/switch/attach/delete`, `send/wait/note/hook`, `merge/ship/queue`, `run/sync/cleanup/version/usage`, `doctor`, `db`, `config` — each cockpit key maps to one of these.
- Quick Actions (`[[actions]]` with `on_create`) turn shell commands into named, auto-runnable project steps (`config.py:147-158`, `core/quick_actions.py:29-115`); Agent Broadcast (`send --all/--working`) fans out to live sessions filtered by WORKING status (`commands/agent.py:53-84`).
- Headless mode (`--headless` → `LaunchMode.HEADLESS`) bypasses multiplexers via `subprocess.Popen` + stdin and requires `supports_headless` (Claude and Pi only); `owt wait` polls the status DB until a terminal state (`waiting/completed/error`).
- Config resolution order: `--config > ./.worktreerc > ./.worktreerc.toml > ~/.config/open-orchestrator/config.toml > ~/.worktreerc` (`config.py:299-313`); sections cover worktree, tmux, environment, sync, backend, per-tool, custom `[tools.*]`, `[[actions]]`, templates, and theme.
- Environment contract (`docs/configuration.md:67-74`): `OWT_AUTOMATED`, `OWT_WORKTREE_NAME`, `OWT_DB_PATH`, `OWT_BACKGROUND`.
- Models are small Pydantic types: `WorktreeInfo/SessionInfo` (`models/worktree_info.py`), `AIActivityStatus/WorktreeAIStatus` (`models/status.py`), `BackendKind/BackendSession/BackendConfig` (`models/backend.py`), `SectionKind/RowAction/ControlPlaneRow` (`models/control_plane.py`), maintenance and project-config types.

## 6. [[wiki/06-status-mcp-observability|Status Store, MCP Peers, Environment, Observability]]

**In one sentence:** A shared SQLite database is the system's memory — agent hooks write status, every reader polls it, MCP peer messages ride in the same tables — while `owt` itself never calls an LLM.

- **owt calls no LLM and no external API.** The LLM is the client: the coding agent (Claude/Droid/Pi/OpenCode) runs in the worktree pane and reports back via hooks, `owt hook`, status writes, and the optional MCP peer server.
- State lives in SQLite `status.db` (`~/.open-orchestrator/status.db`, overridable via `$OWT_DB_PATH`): schema v3.3 in `core/status_schema.py:70-176` with tables `worktree_status` (16 cols), `shared_notes`, `metadata`, `peer_messages`, `usage_events`; legacy `ai_status.json` is migrated once.
- Concurrency is SQLite WAL + `busy_timeout=5000` + `synchronous=NORMAL` (`core/_db.py:52-83`); every write is `INSERT OR REPLACE` + commit; readers always read fresh (`reload()` is a documented no-op, `core/status.py:93-94`); change detection is a `MAX(updated_at):COUNT(*)` token (`core/status.py:96-107`).
- Lifecycle values `AIActivityStatus` (`models/status.py:16-26`): terminal = waiting/completed/error (`core/status_policy.py:29-41`); attention = blocked/error (:44-46). Writes come from hooks and `record_command` (idle/waiting/blocked → working on agent input, `core/status.py:243-260`).
- MCP peer messaging is an opt-in extra (`pip install open-orchestrator[mcp]`): one stdio server per agent (`python -m open_orchestrator.core.mcp_peer`) exposing `list_peers / send_message / check_messages` (+ `set_summary`, `get_peer_files`); loopback-only bind; peer messages are a named prompt-injection source in the threat model.
- `owt new` builds a reproducible nest: dependency install per detected package manager, `.env` copy with path-key rewriting (atomic, `0o600`), CLAUDE.md injection with idempotent markers, and hook installation gated on `supports_hooks` (Claude/Droid only).
- Observability: ContextVar correlation IDs + per-worktree context with a JSON log formatter (`--log-format json`), and a `{"status":"ok|error","data":…}` machine envelope for CLI output.

## 7. [[wiki/targeted|Targeted: OpenOrchestrator Deep Dive for Fleet Comparison]]

**In one sentence:** OpenOrchestrator (`owt`) is a supervise-don't-replace cockpit over isolated git worktrees whose borrowable core is the decision-surface UX (lanes + verb rows + context footer), real-time file-overlap Conflict Guard, and a recorded-backend + ordered-queue shipping discipline — all grounded in file:line citations below.

- Design principle is explicit: "doesn't try to be the agent — it supervises them" (`README.md:5`); the cockpit owns prioritization, the harnesses own execution.
- Worker restart/attach is backend-record-driven: each status row stores its owner backend, so `owt attach` and the `a` key reattach without flags; crashed sessions surface as BLOCKED/ERROR lanes and `fix` hands control to the human's `$EDITOR`.
- Conflict Guard = `git diff --name-only {base}...{branch}` intersected with peers' last-reported `modified_files` from SQLite — cheap, real-time, advisory-only; the merge itself is two-phase with abort discipline.
- There is no workflow DAG abstraction: `--workflow` is plan-first prompt framing (classifier + prepended protocol), and ordering is a smallest-first queue sort, not a dependency scheduler.
- Multi-harness support is a `Protocol` + registry + config-table plugin layer: 5 bespoke tool classes, auto-detect priority `claude > pi > droid > opencode`, and no-code custom tools via `[tools.<name>]` with `{{task}}`/`{{worktree}}` argv substitution.
- 7 concrete borrowable ideas for fleet are listed below, each with the exact file:line to steal from and a fleet-mapping note.

## The system in five moves

1. Isolate: each task gets a git worktree, a backend session (tmux/herdr), and a status row.
2. Report: agent hooks and file lists keep one shared SQLite store fresh.
3. Prioritize: the cockpit sorts everything into NEEDS YOU / READY TO SHIP / IN FLIGHT.
4. Decide: the human presses one verb key per row (attach, diff, fix, ship, merge).
5. Ship safely: overlap warning, two-phase merge in queue order, teardown or PR — then sweep orphans.
