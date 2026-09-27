# Technical Analysis: openorchestrator (`owt`)

**Repository:** https://github.com/gitpcl/openorchestrator
**Version analyzed:** 0.5.0 @ `1b485ae` (2026-07-04)
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves

Running several AI coding agents at once is coordination chaos: each agent works in its own checkout, reports progress in its own way, and collisions surface only at merge time. OpenOrchestrator (`owt`) answers with a supervise-don't-replace cockpit: it never writes code and never calls an LLM itself. Instead it isolates each agent in its own git worktree + terminal session, tracks all of them in one SQLite status store, and presents a single keyboard-driven Textual board with three priority lanes — NEEDS YOU / READY TO SHIP / IN FLIGHT — where every row carries verb actions (`ship`, `attach`, `diff`, `fix`, `merge`).

The primary user is a human developer supervising parallel coding agents across providers (Claude Code, Pi, Droid, OpenCode, ClawCore, plus config-registered custom tools). Secondary users are scripts and CI, which use the same verbs headlessly (`owt new --headless`, `owt wait`, `owt queue --ship`). The headline differentiators are Conflict Guard (real-time file-overlap warnings between agents), a pluggable tmux/herdr multiplexer layer, two-phase merge with an ordered queue, and PR-based shipping.

---

## 2. High-Level Architecture

```
                ┌─────────────────────────────┐
                │  owt cockpit (Textual TUI)  │  bare `owt`
                │  lanes + verbs + footer    │  polls every 2 s
                └──────────────┬──────────────┘
                               │ subprocess per verb (ship/merge/attach/...)
                               ▼
┌──────────┐  ┌─────────────────────────────────────────┐  ┌──────────────────┐
│ CLI verbs│─►│ StatusTracker (SQLite status.db, WAL)   │◄─│ agent hooks      │
│ (Click)  │  │ worktree_status / peer_messages / notes │  │ owt hook events  │
└────┬─────┘  └─────────────────────────────────────────┘  └──────────────────┘
     │                    ▲                                       │
     ▼                    │ get_all_statuses                      ▼
┌─────────────┐  ┌────────┴────────┐                  ┌──────────────────────┐
│ AgentLaunch │  │ MergeManager    │                  │ MultiplexerBackend   │
│ registry +  │  │ 2-phase merge,  │                  │ tmux (default) or    │
│ prompt prep │  │ Guard, queue    │                  │ herdr (opt-in)       │
└──────┬──────┘  └─────────────────┘                  └──────────┬───────────┘
       │ new worktree + env + hooks                              │ session per
       ▼                                                         ▼ worktree
  git worktree + deps + .env + CLAUDE.md              tmux session / herdr workspace
                                                      running claude|pi|droid|opencode
```

Data flow from `owt new "task"` to shipped code:

1. `new_worktree` (`commands/worktree/new.py:43`) resolves base/branch (auto-named via `core/branch_namer.py:128-195`), AI tool (explicit, auto-detected, or picker), and template overlay.
2. `AgentLauncher.launch` (`core/agent_launcher.py:133-230`) creates the git worktree (`core/worktree.py:209-276`), sets up env (deps, `.env`, CLAUDE.md, hooks via `core/pane_actions.py:174-249`), opens the backend session, pastes the (protocol-prepended, for `--workflow`) prompt, and writes the initial WORKING status row.
3. While the agent works, its hooks (`UserPromptSubmit→working`, `Stop→waiting`, permission-prompt→blocked; `core/hooks.py:56-148`) and `modified_files` reports keep SQLite fresh.
4. The cockpit poll loop (`core/control_plane_view.py:316-322`, every 2 s) rebuilds the three lanes from tracker rows + merge-queue plan + MERGE_HEAD checks; the operator reacts with single keys.
5. `s`/`m` run `owt ship/merge`: Conflict Guard warns on file overlap (`core/merge.py:183-213`), phase 1 proves the feature branch absorbs base, phase 2 merges into base (`core/merge.py:328-574`), then teardown removes session + worktree + branch (`core/pane_actions.py:331-371`) — or `--pr` ships via GitHub instead.

Persistent state: one shared SQLite file (`~/.open-orchestrator/status.db`, `$OWT_DB_PATH` override; `core/status_schema.py:390-459`), WAL mode, per-write commits. No server process, no daemon — every command is a short-lived process over the same DB.

---

## 3. The Status Row (core abstraction)

The central domain object is the per-worktree status row, `WorktreeAIStatus` (`models/status.py:29-54`): 16 columns covering identity (`worktree_name/path/branch`), session (`tmux_session`, `ai_tool`), activity (`activity_status`, `current_task`, `last_task_update`, `notes`, `modified_files`), backend ownership (`backend_kind/backend_session_id/backend_meta`), `session_type` (worktree vs branch mode), and timestamps. Activity values are `AIActivityStatus` (`models/status.py:16-26`): idle/working/blocked/waiting/completed/error/stalled/unknown.

Key behaviors on the row: `update_task/mark_completed/mark_idle/mark_stalled` (`models/status.py:56-84`); `record_command` flips idle/waiting/blocked → working on agent input (`core/status.py:243-260`); `get_backend_session` rebuilds the live backend handle from the recorded columns (`core/status.py:167-192`). Classification policy is split three ways (`core/status_policy.py`): terminal = waiting/completed/error (:29-41), attention = blocked/error (:44-46), with backend `summary_bucket` (waiting→idle, :54-66) vs frontend `ui_bucket` (waiting+blocked→waiting, :69-75) kept deliberately distinct.

The schema (v3.3, `core/status_schema.py:70-176`) adds `peer_messages`, `shared_notes`, `metadata`, and `usage_events` tables beside `worktree_status`. Knobs: `$OWT_DB_PATH` relocation, `db purge/vacuum/health` thresholds (10K messages / 100 MB, `commands/db_cmd.py:48-51`).

---

## 4. LLM / External Service Integration

**The repo does not call any LLM or external API itself.** There is no LangChain/LangGraph/MCP-client-to-LLM code and no model key handling. The intended callers are the external coding agents running in worktree panes (Claude Code, Pi, Droid, OpenCode, ClawCore, custom CLIs). owt's side of the contract is:

- Launch: exact argv per tool from `get_command()` (`core/tool_registry.py`), prompt delivery through the multiplexer.
- Reporting: shell hooks installed into Claude (`.claude/settings.json` stanza) and Droid (`.factory/settings.json`) that curl back `owt hook --event …` with `OWT_DB_PATH`/`OWT_WORKTREE_NAME` in env (`core/hooks.py:56-217`); Pi/OpenCode/custom tools report via polling gaps (no hooks — `supports_hooks=False`).
- Peer messaging: an opt-in MCP server (`pip install open-orchestrator[mcp]`, `python -m open_orchestrator.core.mcp_peer` over stdio) exposing `list_peers/send_message/check_messages` (+ `set_summary`, `get_peer_files`) so *agents* can discover and message each other (`core/mcp_peer.py:90-170`). The LLM is the MCP client here, not owt.
- Shipping: `gh` CLI for PR creation (`core/merge.py:231-281`); `origin` remote required.

---

## 5. The Supervise-to-Ship Pipeline

The primary user-facing workflow is new → watch → ship, and every step names its function:

1. **Start** (`commands/worktree/new.py:43-195`): flags (`--ai-tool/--workflow/--plan-mode/--headless/--herdr/--tmux/--template/--prefix/-y/--in-place`), tool resolution with `supports_plan_mode` guard for workflows (:143-156), branch naming (`commands/worktree/_shared.py:44-97`), `LaunchRequest` (:184-195).
2. **Launch** (`core/agent_launcher.py:133-230` + `core/pane_actions.py:174-249`): worktree create → env setup (deps per `core/project_detector.py:80-131`, `.env` copy+rewrite `core/environment.py:214-324`, CLAUDE.md injection `core/environment_claude_md.py:23-119`, hooks if `supports_hooks`) → backend `create_session` → prompt paste (`wait_and_paste` tmux / `submit_prompt` herdr) → `initialize_status` + `update_task(WORKING)`.
3. **Watch**: cockpit 2 s poll (`core/control_plane_view.py:290-322`) or `owt wait` polling loop (`commands/agent.py:118-157`); `owt send` fans out mid-course corrections (`commands/agent.py:29-84`).
4. **Decide**: lanes classify (conflict/blocked → NEEDS YOU; queue candidates → READY TO SHIP with `(commits_ahead, overlaps)`; working → IN FLIGHT). Overlap warnings print top-5 pre-merge (`commands/merge_cmds.py:322-328`).
5. **Ship**: `MergeManager.merge` two-phase (`core/merge.py:328-574`) with `--rebase/--strategy/--leave-conflicts`; `queue --ship` loops it in order (`commands/merge_cmds.py:575-606`); `ship --pr` pushes + `gh pr create --fill` leaving everything intact (`core/merge.py:231-281`); local ship ends in `teardown_worktree` (`core/pane_actions.py:331-371`).
6. **Sweep**: `owt sync/cleanup/doctor` reconcile the DB with git/session reality (`commands/maintenance.py`, `commands/doctor.py:67-202`).

Input → output shape: task string → `LaunchRequest` → (worktree path + backend session + status row) → status transitions → merged base commits (or open PR URL) + deleted worktree.

---

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `core/control_plane_view.py` | 659 | Textual app: lanes mount, 2 s poll loop, footer builder, suspend-to-attach/diff |
| `core/tmux_manager.py` | 791 | tmux session lifecycle, prompt paste/readiness polling, attach/kill |
| `core/merge.py` | 574 | Conflict Guard, two-phase merge, queue planner, PR creation |
| `commands/merge_cmds.py` | 613 | `merge/ship/queue` CLI, overlap warnings, `--ship` loop, `_ship_pr` |
| `core/pane_actions.py` | 563 | env setup wiring, backend create/teardown, full `teardown_worktree` |
| `core/herdr_backend.py` | 547 | herdr workspace/pane mapping, two-call prompt submit, exec attach |
| `core/status.py` | 517 | `StatusTracker`: all reads/writes, inbox, health |
| `core/status_schema.py` | 505 | schema v3.3 DDL, migrations, path resolution, upserts |
| `core/agent_launcher.py` | 497 | launch pipeline across backends and headless |
| `core/environment.py` | 472 | dep install, `.env` copy+rewrite, config fan-out |
| `core/prompt_builder.py` | 416 | task classifier + plan-first protocol preambles |
| `core/project_detector.py` | 407 | package-manager / project-type detection |
| `core/tool_registry.py` | 402 | built-in tool classes, `CustomTool`, custom registration |
| `core/worktree.py` | 398 | git worktree create/delete, path sanitizing |
| `core/modals.py` | 390 | `n`-flow dialogs (input, select, confirm) |
| `core/cleanup.py` | 356 | stale-worktree reaping policy |
| `config.py` | 348 | TOML load, section models, custom-tool pre-registration |
| `core/sync.py` | 432 | worktree↔DB reconciliation |
| `core/control_plane_sections.py` | 226 | lane classifiers |
| `core/control_plane_actions.py` | 257 | verb dispatch table + handlers |

---

## 7. Dependencies

Required (`pyproject.toml:27-35`, `open-orchestrator==0.5.0`, `requires-python>=3.10`):

| Package | Version constraint | Purpose |
|---|---|---|
| `click` | `>=8.1.0` | CLI group, commands, flags |
| `pydantic` | `>=2.0.0` | config + status + control-plane models |
| `rich` | `>=13.0.0` | terminal tables/panels for CLI output |
| `textual` | `>=8.0.0` | control-plane TUI |
| `toml` | `>=0.10.0` | config file parsing |
| `gitpython` | `>=3.1.50` | worktree/branch/merge git operations (security-pinned per `pyproject.toml:189-197`) |
| `libtmux` | `>=0.25.0` | tmux session management |

Optional extras: `mcp>=1.0.0` (`open-orchestrator[mcp]`, `pyproject.toml:46-49`) for peer messaging only. Dev group (PEP 735): pytest, pytest-cov, pytest-asyncio, ruff, mypy (strict), pyyaml, build, twine. Seven runtime deps total — a deliberate minimalism the README advertises.

---

## 8. CLI / Usage Surface

Entry points (`pyproject.toml:51-53`): `owt` → `open_orchestrator.cli:main`; `owt-popup` → `open_orchestrator.popup.picker:main`. Global opts: `--json/--theme/--verbose/--log-format/--profile` (`cli.py:20-29`); bare `owt` opens the cockpit (`cli.py:88-97`).

Commands (implementations in wiki/05):

```
owt new "task" [--ai-tool NAME] [--workflow] [--plan-mode] [--headless]
               [--herdr|--tmux] [-b BASE] [--branch N] [-t TPL] [--prefix P] [-a] [-y]
owt branch "task" [...]            # in-place variant, forces interactive
owt list|ls [-a]  |  owt switch|s <id>  |  owt attach <id> [--herdr|--tmux]
owt delete|rm <id> [-f] [-y]
owt send [name] "msg" [--all|--working]
owt wait <name> [--timeout 600] [--poll 10] [--json]
owt note "msg" [--clear]
owt merge|m <name> [--base B] [--rebase] [--strategy ours|theirs] [--leave-conflicts] [--keep] [-y]
owt ship <name> [merge flags] [-m MSG] [--pr]
owt queue [--base B] [--ship] [-y]
owt run <action> [worktree]
owt sync [name]|--all [--json]  |  owt cleanup [--days 14] [--force] [--json]
owt doctor [--fix]  |  owt db purge|vacuum|health  |  owt config validate|show
owt version  |  owt usage [--days 30]
```

Environment variables (`docs/configuration.md:67-74`): `OWT_AUTOMATED` (hook context), `OWT_WORKTREE_NAME` (agent identity), `OWT_DB_PATH` (shared SQLite), `OWT_BACKGROUND` (theme detect).

Configuration files (`config.py:299-313`, precedence `--config > ./.worktreerc > ./.worktreerc.toml > ~/.config/open-orchestrator/config.toml > ~/.worktreerc`): `[worktree]`, `[tmux]`, `[environment]`, `[sync]`, `[backend]` (mode tmux|herdr|auto), `[claude]/[opencode]/[droid]`, `[tools.*]` custom harnesses, `[[actions]]` quick actions, `[templates.*]`, `theme`.

---

## 9. Extensibility Points

- **New AI harness, no code change**: add a `[tools.<name>]` table (`binary`, `command_template="{binary}"`, `prompt_flag`, `supports_hooks/headless/plan_mode`, `task_via_args`, `known_paths`; `docs/configuration.md:130-154`). `register_custom_tools()` (`core/tool_registry.py:372-392`, pre-validation at `config.py:322-326`) builds a `CustomTool`; `{{task}}`/`{{worktree}}` substitution is shell-quoted at `core/tool_registry.py:67-74`. For bespoke behavior (plan flags, hook stanzas), subclass the protocol in `core/tool_registry.py` following the `claude` class (`:96-141`) and satisfy `AIToolProtocol` (`core/tool_protocol.py:14-99`).
- **New multiplexer backend**: implement `MultiplexerBackend` (`core/multiplexer.py:18-80`), register in `select_backend`/`select_backend_for_session` (`core/backend_factory.py:78-142`), extend `BackendKind` (`models/backend.py:16-20`). herdr (`core/herdr_backend.py`) is the reference second implementation.
- **New cockpit verb**: add a `RowAction` (`models/control_plane.py:30-57`), expose it in the relevant lane builder (`core/control_plane_sections.py`), add the keybinding (`core/control_plane_view.py:227-240`), and register the handler in the dispatch table (`core/control_plane_actions.py:193-203`).
- **New project type / installer**: extend detection in `core/project_detector.py:80-131` and the command table in `core/environment.py:74-95`.
- **New status lifecycle state**: extend `AIActivityStatus` (`models/status.py:16-26`) and the policy buckets (`core/status_policy.py:29-75`); schema change goes through `migrate_columns` (`core/status_schema.py:144-176`).
- **New prompt protocol**: add a task-class entry to `_PROTOCOLS` (`core/prompt_builder.py:123-207`) and a keyword rule in `classify_task` (:34-43).

---

## 10. Limitations and Gotchas

- **Conflict Guard reads reported files, not live peer diffs.** Overlaps compare against `modified_files` as last written to SQLite (`core/merge.py:191-213`) — a silent agent (Pi/OpenCode have no hooks) under-reports, and the pre-merge warning is advisory-only (`commands/merge_cmds.py:322-328`). Fine as an early signal; not a guarantee.
- **Poll-everything refresh.** The cockpit rebuilds all sections every 2 s with no reactive updates or change-token short-circuit in the view (`core/control_plane_view.py:290-322`), despite the DB exposing a generation token (`core/status.py:96-107`). Scales to tens of worktrees, not hundreds.
- **tmux-only feature paths.** `plan_mode`, `automated` task threading, and `task_via_args` handling are tmux-gated; herdr ignores them (`core/herdr_backend.py:236`, `core/agent_launcher.py:177-184`). herdr also shells async over `asyncio.run` bridges (`core/herdr_backend.py:200-218`) — sync-over-async with its own failure modes.
- **Headless is Claude/Pi-only** (`supports_headless` gate at `commands/worktree/new.py:148`) and incompatible with `--herdr/--workflow/--in-place` (`:77-87`).
- **Phase-2 merge mutates the main checkout** (checkout base + `clean -fdX` + autostash dance, `core/merge.py:522-574`) — safe when the main checkout is idle, hazardous if the operator works there mid-ship.
- **Maintenance smells**: `plan.toml` at repo root is a stale batch-task file unrelated to the product; several modules carry sprint-numbered comments; `popup/picker.py` (curses) is dead weight beside the Textual UI; `core/tool_search.py`'s name misleads (in-agent schema loader, not harness search).
- **Security posture is documented but hook-shaped**: agents' hook callbacks and peer messages are named prompt-injection sources (`docs/security.md:16-51`); `gh` and installer CLIs run with user privileges; `.env` files are copied between checkouts by design (`core/environment.py:214-284`).

---

## 11. How It Compares to Alternatives

- **Claude Code Agent Teams** coordinate multiple agents *within one codebase*; owt supervises *isolated worktrees across providers* from one screen (`README.md:20`). Complementary: Teams for intra-branch collaboration, owt as the cross-branch cockpit. Tradeoff: owt pays worktree + session overhead per task and gets isolation in return.
- **Conductor / Claude Squad / Vibe Kanban** (cf. KB entry [[RalphLoopConductorOrchestratorLandscape/summary]]) are the same species — worktree-per-task boards over heterogeneous harnesses. owt's distinct bets are Conflict Guard, the recorded-backend multiplexer abstraction (tmux + herdr, not tmux-only), and the verb-row/footer UX; its gap vs. this class is any built-in review/CI gate before ship.
- **Agent Orchestrator / AO** (cf. KB entry [[AgentOrchestrator/summary]]) adds inspector gates (tests + review must sign off) where owt trusts the human's `d`iff + `s`hip keystrokes. owt is lighter (7 deps, no server) but says less about correctness.
- **Fleet** (this analysis's consumer): fleet's queue + retry-table + worktree-merge architecture already covers scheduling and recovery more generally than owt's smallest-first ship loop; what owt contributes is UX and safety-plumbing ideas — lanes/verbs/footer, overlap warnings from stored file lists, two-phase merge discipline, PR shipping, and the capability-flag harness matrix (see [[wiki/targeted]] for the 7-item borrow list with file:line sources).

Positioning: OpenOrchestrator is the minimalist's multi-provider cockpit — one SQLite file, seven dependencies, no daemon — trading automatic correctness gates for human decision speed.

---

## Appendix: Selected Code Snippets

**Dispatch table — the cockpit's whole action model (`core/control_plane_actions.py:193-203`)**

```python
(NEEDS_YOU, FIX): action_fix, (READY_TO_SHIP, SHIP): action_ship,
(READY_TO_SHIP, MERGE): action_merge, (∗, ATTACH): action_attach,
(∗, DELETE): action_delete
```

**Queue ordering — smallest-first (`core/merge.py:319-325`)**

```python
if dependency_order: sort by order_map …
else: candidates.sort(key=lambda x: (x[1], x[2]))  # fewest commits, then overlaps
```

**PR creation (`core/merge.py:254-266`, structure)**

```python
push -u origin source_branch …
run([gh_bin, "pr", "create", "--head", src, "--base", dst, "--fill"])
```

**Generic plugin command (`core/tool_registry.py:58-78`)**

```python
def get_command(self, *, executable_path=None, plan_mode=False, prompt=None, worktree=None) -> str:
    binary = shlex.quote(executable_path) if executable_path else self.binary
    if self.task_via_args:
        cmd = self.command_template.replace("{binary}", binary)
        cmd = cmd.replace("{{task}}", shlex.quote(prompt or ""))
        cmd = cmd.replace("{{worktree}}", shlex.quote(worktree or "."))
        return cmd
```
