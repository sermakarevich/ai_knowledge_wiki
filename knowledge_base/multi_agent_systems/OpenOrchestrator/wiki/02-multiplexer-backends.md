> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Pluggable Multiplexer Backends (tmux / herdr)

**In one sentence:** A single `MultiplexerBackend` protocol fronts tmux (default) and herdr (opt-in) so no CLI command ever touches session machinery directly, and each worktree row remembers which backend owns it.

## Key points

- The abstraction is `MultiplexerBackend`, a runtime-checkable `Protocol` in `core/multiplexer.py:18`, with `create_session / session_for / send_text / send_keys / read_recent / attach / kill / is_alive / report_agent_state`.
- Backend identity is data: `BackendKind` (`TMUX`/`HERDR`) and `BackendSession(kind, id, worktree_name, meta)` in `models/backend.py:16-35`; status rows carry `backend_kind/backend_session_id/backend_meta` so reattach needs no flags.
- tmux sessions are named `owt-{sanitized}` (`core/tmux_manager.py:202-205`); prompt delivery uses `send-keys`, with a `load-buffer/paste-buffer` path for large prompts and `capture-pane` polling for agent readiness.
- herdr talks newline-delimited JSON-RPC over a Unix socket (`core/herdr_client.py:82-163`); one owt worktree maps to one herdr workspace with the agent in the root pane.
- Backend selection (`core/backend_factory.py:78-117`): explicit `--herdr/--tmux` flag beats config `[backend] mode` (`tmux|herdr|auto`, default `tmux`); `auto` uses herdr only if a live daemon is detected.
- `owt attach` resolves the recorded backend for the session (`commands/worktree/attach.py:41-61`); the cockpit suspends the TUI and execs into it. herdr attach execs `herdr agent attach <pane>`; tmux attach uses `attach-session`/`switch-client`.
- Interactive relaunch on an existing tmux session reuses it instead of double-spawning (`core/agent_launcher.py:354-367`).

---

## The protocol and the session record

`core/multiplexer.py:18` defines `MultiplexerBackend(Protocol, runtime_checkable)` with `kind: BackendKind` (:25) and methods `create_session` (:27-36), `session_for` (:52), `send_text` (:56), `send_keys` (:60), `read_recent` (:64), `attach` (:68), `kill` (:72), `is_alive` (:76), `report_agent_state` (:80).

`models/backend.py:16-35` defines `BackendKind(TMUX/HERDR)`, `BackendSession(kind, id, worktree_name, meta)` — where `id` is the tmux session name or the herdr pane id — and `models/backend.py:38-54` defines `BackendConfig(mode, herdr_session, herdr_socket)`. Because the owning backend is recorded per worktree row, later commands reconstruct it via `select_backend_for_session` (`core/backend_factory.py:120-142`) instead of requiring the user to repeat flags.

## tmux backend

`core/tmux_backend.py` is a thin wrapper over `TmuxManager` (`core/tmux_manager.py`). Session names come from `generate_session_name()` → `owt-{sanitized}` (`core/tmux_manager.py:202-205`, prefix `SESSION_PREFIX="owt"` at :175, with `/` and `.` mapped to `-`); lookup via `session_exists` (:207) and `get_session_for_worktree` (:581).

Creation flows `create_session` (`core/tmux_manager.py:549-579`) → `server.new_session(attach=False)` (:225) → `_start_ai_tool_in_pane` (:278) → `install_status_bar` (:261). `_start_ai_tool_in_pane` resolves the tool via the registry, honors `plan_mode/automated/task_via_args` (:297-321, `OWT_AUTOMATED=1` prefix at :314, one-shot `task` at :320, `cat file | claude -p` shortcut at :327-329), waits for shell readiness (`_wait_for_shell_ready`, :361), then sends literal keystrokes (`send-keys -l` + `Enter`, :456-471).

I/O primitives: `send_text` → `send_keys_to_pane` (:99-101, :612); large prompts go through `paste_to_pane` via `load-buffer/paste-buffer` + `Enter` (:626-675); readiness via `wait_for_ai_ready` polling `capture-pane` (:396-443), exposed as `wait_and_paste` (:78-86). Attach branches on `is_inside_tmux` (:592): `switch_client` (:515) inside, `attach` (:508, `tmux attach-session`) outside. Kill → `kill_session` (:538); `read_recent` via `capture-pane -p -J -S -N` (:113-127).

Restart safety: on `TmuxSessionExistsError`, `core/agent_launcher.py:354-367` reuses the existing `BackendSession` for interactive launches only and refuses otherwise, preventing double-spawns.

## herdr backend

herdr (herdr.dev) is an external mouse-native terminal daemon with a sidebar; the integration is documented in `docs/multiplexer-backends.md` and `docs/herdr-integration.md`. Transport is `HerdrClient` (`core/herdr_client.py:50`): async newline-delimited JSON-RPC over a Unix socket (`connect` at :82 via `open_unix_connection`, `call` at :117 with an `id` correlator at :149-153, `ping` at :133, `read_loop` at :163). Default socket: `$XDG_CONFIG_HOME/herdr/herdr.sock` or `sessions/<name>/herdr.sock` (:38-47).

Mapping (`core/herdr_backend.py:1-5`): workspace → tab → pane; one owt worktree is one herdr workspace, agent in the root pane. `create_session` (:222-267) issues RPC `workspace.create {cwd, label}` (:237-240), parses ids via `_extract_workspace_pane` (:101-175), with fallback `_discover_root_pane` (:269, prefers `pane.list` at :307). The sync façade bridges async via `asyncio.run`/`run_until_complete` in `_call` (:200-218). tmux-only features (`plan_mode`, `automated`, `task`) are explicitly ignored (`del` at :236).

Prompt submission is the design crux: `_send_line` (`core/herdr_backend.py:469-510`) splits the body and terminator into two `pane.send_text` calls (keys overridable via `OWT_HERDR_SUBMIT`, :32-63); `submit_prompt` (:372-415) nudges `\r` until `agent_status != idle`, with `wait_for_ready` (:343) polling `agent/idle`. `read_recent` (:512, `pane.read`), `send_keys` (:466, `pane.send_keys`), `is_alive` (:447, `pane.exists`), `kill` (:435, `pane.close` + `workspace.close`), `report_agent_state` (:529, `pane.report_agent`, non-fatal — tmux no-ops it at `core/tmux_backend.py:135`).

## Selection and attach

`detect_herdr` (`core/backend_factory.py:30-61`) checks `shutil.which("herdr")` plus a 1 s `HerdrClient.ping()`, never raising. `select_backend(config, override)` (:78-117): explicit override wins; then config `mode`; `herdr` mode raises `BackendUnavailableError` (:104-108) when no daemon; `auto` (:110-112) picks herdr-if-live else tmux. Results are cached per `(mode, session, socket)` (:98-100). Flags `--herdr/--tmux` and `[backend] mode/herdr_session/herdr_socket` in `.worktreerc.toml` are documented in `docs/multiplexer-backends.md:18-24`; `--headless` skips backend resolution entirely.

Attach (`commands/worktree/attach.py:11`): `resolve_session_target` (:41) → `tracker.get_backend_session` (:45) → unforced path reuses the recorded backend (`select_backend_for_session`, :51) and calls `backend.attach` (:61); forced flags re-resolve via `backend.session_for(name)` (:73) and error clearly instead of coercing ids (:75-78). The cockpit's `action_attach` (`core/control_plane_actions.py:94-98`) prefers `runtime.backend_attach`, else shells to `owt attach` after suspending the TUI. Both backends exec on attach: tmux via `attach-session` (`core/tmux_manager.py:508-513`), herdr via `os.execvp(["herdr","agent","attach",pane_id])` (`core/herdr_backend.py:521-527`, argv helper `attach_argv` at :542).

```python
# core/multiplexer.py:27-68 — the protocol core
def create_session(self, worktree_name: str, cwd: str, *, agent_command: str | None = None, ...) -> BackendSession: ...
def session_for(self, worktree_name: str) -> BackendSession | None: ...
def send_text(self, session: BackendSession, text: str) -> None: ...
def attach(self, session: BackendSession) -> None: ...
```

**Covers:** `core/multiplexer.py`, `core/tmux_backend.py`, `core/tmux_manager.py`, `core/herdr_backend.py`, `core/herdr_client.py`, `core/backend_factory.py`, `models/backend.py`, `commands/worktree/attach.py`, `docs/multiplexer-backends.md`, `docs/herdr-integration.md`
