> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# CLI Surface, Config, Models

**In one sentence:** A Click command group where bare `owt` opens the cockpit and every cockpit verb has a scripting-grade CLI twin, configured by layered TOML files and typed by Pydantic models.

## Key points

- Entry points (`pyproject.toml:51-53`): `owt = open_orchestrator.cli:main`, `owt-popup = open_orchestrator.popup.picker:main`; `cli.py:19` declares the Click group with `--json/--theme/--verbose/--log-format/--profile`, and no subcommand launches `ControlPlaneApp().run()` (:88-97).
- The verb inventory covers the full lifecycle: `new/branch/list/switch/attach/delete`, `send/wait/note/hook`, `merge/ship/queue`, `run/sync/cleanup/version/usage`, `doctor`, `db`, `config` — each cockpit key maps to one of these.
- Quick Actions (`[[actions]]` with `on_create`) turn shell commands into named, auto-runnable project steps (`config.py:147-158`, `core/quick_actions.py:29-115`); Agent Broadcast (`send --all/--working`) fans out to live sessions filtered by WORKING status (`commands/agent.py:53-84`).
- Headless mode (`--headless` → `LaunchMode.HEADLESS`) bypasses multiplexers via `subprocess.Popen` + stdin and requires `supports_headless` (Claude and Pi only); `owt wait` polls the status DB until a terminal state (`waiting/completed/error`).
- Config resolution order: `--config > ./.worktreerc > ./.worktreerc.toml > ~/.config/open-orchestrator/config.toml > ~/.worktreerc` (`config.py:299-313`); sections cover worktree, tmux, environment, sync, backend, per-tool, custom `[tools.*]`, `[[actions]]`, templates, and theme.
- Environment contract (`docs/configuration.md:67-74`): `OWT_AUTOMATED`, `OWT_WORKTREE_NAME`, `OWT_DB_PATH`, `OWT_BACKGROUND`.
- Models are small Pydantic types: `WorktreeInfo/SessionInfo` (`models/worktree_info.py`), `AIActivityStatus/WorktreeAIStatus` (`models/status.py`), `BackendKind/BackendSession/BackendConfig` (`models/backend.py`), `SectionKind/RowAction/ControlPlaneRow` (`models/control_plane.py`), maintenance and project-config types.

---

## Command inventory (with implementing function)

- `owt new "task"` — `new_worktree()` (`commands/worktree/new.py:15,43`): `-b/--base`, `--branch`, `--ai-tool`, `--plan-mode`, `--workflow`, `-t/--template`, `-a/--attach`, `--prefix`, `-y/--yes`, `--headless`, `--in-place` (branch mode), `--herdr/--tmux`.
- `owt branch "task"` — `branch_cmd()` (`commands/worktree/branch.py:10,19`); subset of `new` flags; forces `headless=False` (:50).
- `owt list|ls`, `owt switch|s`, `owt attach [--herdr|--tmux]`, `owt delete|rm` — `commands/worktree/ls.py:26-28`, `switch.py:11-13`, `attach.py:11-15`, `delete.py:11-15`.
- `owt send [name] "msg" [--all, --working]` — `send_to_worktree()` (`commands/agent.py:23,29`; registered :241-246). Broadcast filters `AIActivityStatus.WORKING` (:71-84) and dispatches via `select_backend_for_session() + send_text()` (:53-69).
- `owt wait <name> [--timeout 600, --poll 10, --json]` — `wait_for_worktree()` (`commands/agent.py:102,107`): `tracker.reload() + get_status()` loop with `time.sleep(poll)` (:118-154); terminal check is `status_policy.is_terminal()` (:128 → `core/status_policy.py:29-41`: WAITING/COMPLETED/ERROR); ERROR exits 1 (:143-144), timeout raises ClickException (:156-157).
- `owt note "msg" [--clear]` — `shared_note()` (`commands/agent.py:160,163`), injected into CLAUDE.md (:174-193).
- `owt hook --event {working,waiting,blocked} --worktree` (hidden, internal) — `hook_event()` (`commands/agent.py:200-236`).
- `owt merge|m`, `owt ship [--pr]`, `owt queue [--ship]` — `merge_worktree()` (:215-231), `ship_worktree()` (:376-399), `merge_queue()` (:535-539) in `commands/merge_cmds.py`.
- `owt run <action> [worktree]` — `run_action_cmd()` (`commands/run_cmd.py:15-18`); exit code propagates (:52-53).
- `owt sync`, `owt cleanup [--days 14]`, `owt version`, `owt usage` — `commands/maintenance.py:18-136`.
- `owt doctor [--fix]` — `doctor()` (`commands/doctor.py:67-69`).
- `owt db purge|vacuum|health` — `commands/db_cmd.py:15-51` (thresholds: 10K messages / 100 MB).
- `owt config validate|show` — `commands/config_cmd.py:12-55`.

## Config and models

`ActionConfig{name, command, on_create}` (`config.py:147-158`, uniqueness validator :183-190); `find_action` (`core/quick_actions.py:29`); `run_action` (:56-63, shlex-only at :37-42, stdio-inheriting for `owt run` at :77-80); `run_startup_actions` (:103-115, best-effort, never raises). `owt run` itself is `commands/run_cmd.py:34-48`.

Worktree/client sections: `[worktree]` (`config.py:90-97`: `base_directory=../`, naming pattern, `auto_cleanup_days=14`); `[tmux]` (:100-120: layout, `auto_start_ai`, `ai_tool=claude`, `session_prefix=owt`, mouse mode, prefix key); `[environment]` (:123-134); `[sync]` (:137-144); `[backend]` → `BackendConfig`; `[claude]/[opencode]` config paths and `[droid]` automation level (:38-58); `[tools.*]` custom dict (:175, pre-validation registration :322-326); `[[actions]]` (:181); `theme=auto` (:177-180); templates dict (:174, builtins feature/bugfix/hotfix at :199-232).

Data models: `WorktreeInfo` + `SessionType` + `SessionInfo` + `WorktreeCreateResult` (`models/worktree_info.py:10-68`); `AIActivityStatus{idle,working,blocked,waiting,completed,error,stalled,unknown}` + `WorktreeAIStatus` (16 fields incl. `modified_files`, `backend_kind/session_id/meta`, `session_type`) + transitions `update_task/mark_completed/mark_idle/mark_stalled` (`models/status.py:16-98`); backend trio (`models/backend.py:16-54`); control-plane trio (`models/control_plane.py:18-75`); maintenance enums and reports (`models/maintenance.py:17-90`); `PackageManager/ProjectType/ProjectConfig` (`models/project_config.py:9-62`).

**Covers:** `cli.py`, `config.py`, `commands/run_cmd.py`, `commands/agent.py`, `commands/doctor.py`, `commands/maintenance.py`, `commands/db_cmd.py`, `commands/config_cmd.py`, `commands/_shared.py`, `models/worktree_info.py`, `models/status.py`, `models/backend.py`, `models/control_plane.py`, `models/maintenance.py`, `models/project_config.py`, `core/quick_actions.py`, `docs/commands.md`, `docs/configuration.md`
