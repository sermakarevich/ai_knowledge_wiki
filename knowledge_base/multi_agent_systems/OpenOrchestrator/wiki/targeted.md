> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Targeted: OpenOrchestrator Deep Dive for Fleet Comparison

**In one sentence:** OpenOrchestrator (`owt`) is a supervise-don't-replace cockpit over isolated git worktrees whose borrowable core is the decision-surface UX (lanes + verb rows + context footer), real-time file-overlap Conflict Guard, and a recorded-backend + ordered-queue shipping discipline — all grounded in file:line citations below.

## Key points

- Design principle is explicit: "doesn't try to be the agent — it supervises them" (`README.md:5`); the cockpit owns prioritization, the harnesses own execution.
- Worker restart/attach is backend-record-driven: each status row stores its owner backend, so `owt attach` and the `a` key reattach without flags; crashed sessions surface as BLOCKED/ERROR lanes and `fix` hands control to the human's `$EDITOR`.
- Conflict Guard = `git diff --name-only {base}...{branch}` intersected with peers' last-reported `modified_files` from SQLite — cheap, real-time, advisory-only; the merge itself is two-phase with abort discipline.
- There is no workflow DAG abstraction: `--workflow` is plan-first prompt framing (classifier + prepended protocol), and ordering is a smallest-first queue sort, not a dependency scheduler.
- Multi-harness support is a `Protocol` + registry + config-table plugin layer: 5 bespoke tool classes, auto-detect priority `claude > pi > droid > opencode`, and no-code custom tools via `[tools.<name>]` with `{{task}}`/`{{worktree}}` argv substitution.
- 7 concrete borrowable ideas for fleet are listed below, each with the exact file:line to steal from and a fleet-mapping note.

---

## 1. Design principles

Stated outright in `README.md:5`: "Open Orchestrator doesn't try to be the agent — it *supervises* them", closed by `README.md:7`: "You own the cockpit; the AI tools own the engine." Concretely this means: owt never calls an LLM (see wiki/06), never edits code itself, and every autonomous step ends at a human decision point.

The decision surface is the three-lane board (`models/control_plane.py:18-28`): NEEDS YOU (conflicts, blocked, errors — sorted first), READY TO SHIP (merge-queue candidates with overlap counts), IN FLIGHT (working, by recency). Classification is in `core/control_plane_sections.py:32-208`; empty lanes hide via CSS so attention is never split (`core/control_plane_view.py:131-155`). The footer shows only the focused row's keys (`core/control_plane_view.py:412-438`) — the operator never memorizes verbs, only reacts. Keyboard map: `n` new, `a` attach, `s` ship, `d` diff, `f` fix, `m` merge, `q` quit (`README.md:78-86`, bindings `core/control_plane_view.py:227-240`).

Fleet mapping: fleet's supervisor already owns orchestration; what owt adds is the *prioritized attention model* — lanes ordered by "needs human first", per-row verb affordances, and a footer that teaches keys contextually instead of a static help screen.

## 2. Worker restart handling

There is no process supervisor that restarts crashed agents. The model is session persistence + reattach + human triage:

- Every status row records its backend (`backend_kind/backend_session_id/backend_meta`, `models/status.py:29-54`), so `owt attach <id>` reconstructs the owning backend (`select_backend_for_session`, `core/backend_factory.py:120-142`) and execs into the live session — tmux via `attach-session`/`switch-client` (`core/tmux_manager.py:508-515`), herdr via `herdr agent attach` (`core/herdr_backend.py:521-527`).
- Interactive relaunch onto an existing tmux session reuses it rather than double-spawning (`core/agent_launcher.py:354-367`).
- Death detection is indirect: hooks stop reporting, `owt doctor` cross-checks status rows vs `git worktree list` / `git branch --list` / live sessions (`commands/doctor.py:82-155`), and stale/error rows land in NEEDS YOU with `(ATTACH, DELETE)` actions (`core/control_plane_sections.py:60-81`).
- `fix` (`core/control_plane_actions.py:108-124`) is the restart-adjacent verb: it opens `$EDITOR` and exits the cockpit (`handoff=True`) so the human repairs state, then returns. `merge` just runs the `owt merge` subprocess.

Fleet mapping: fleet's retry-table/queue model is stronger on automatic recovery; owt's contribution is making *session ownership durable data* (backend recorded per task row) so any later command reattaches without re-derivation — worth copying as a schema habit.

## 3. Conflict resolution

Conflict Guard (`core/merge.py:183-213`) is file-overlap detection between parallel branches: own modified set from `git diff --name-only {base}...{branch}` (:183-189) intersected with peers' `modified_files` as last reported to SQLite (:191-213). Limits to name plainly: it compares against *reported* file lists, not live peer diffs, and it is advisory — `commands/merge_cmds.py:322-328` prints the top-5 overlaps pre-merge without blocking.

The merge itself (`MergeManager.merge`, `core/merge.py:328-438`) is two-phase: phase 1 updates the feature branch from base inside the worktree (merge or `--rebase`, :440-491); phase 2 checks out base in the main checkout, merges, restores branch + autostash (:522-574). Any phase-1 conflict aborts (`merge --abort`/`rebase --abort`) and raises `MergeConflictError` before phase 2 is attempted; `--strategy ours|theirs` becomes `merge -X` (:503-507); `--leave-conflicts` skips the abort and leaves the state in progress (:487-490, :514-518). Queue order (`plan_merge_order`, :283-326) is smallest-first on `(commits_ahead, overlap_count)` unless an explicit DAG `dependency_order` is passed — branch age/size are not inputs.

Fleet mapping: fleet already merges worktrees; the borrowable pieces are (a) the *pre-merge overlap warning* computed from already-stored file lists (near-zero cost), and (b) the *two-phase discipline* (prove the feature branch merges cleanly before touching base).

## 4. Workflow abstraction

There is no workflow DAG, no task graph, no dependency scheduler in owt. "Workflow" means one thing: `--workflow` on `owt new` sets `plan_mode=True` (`commands/worktree/new.py:84-85`), classifies the task by keyword (`core/prompt_builder.py:34-43`, default FEATURE), and prepends the matching protocol preamble (`_PROTOCOLS`, :123-207, plus `COMMIT_SAFETY` :104, `TURN_EFFICIENCY` :113) to the agent prompt (:210-213, wired at `new.py:165-170`). The worktree is then tracked on the board like any other (`display_task="⟳ ..."`). "How implemented (queue --ship ordering)": `owt queue --ship` (`commands/merge_cmds.py:575-606`) is a *shipping loop* over the independently computed `plan_merge_order`, stopping at the first conflict — ordering, not orchestration.

Fleet mapping: fleet's queue + plan model is the more general abstraction; owt's lesson is that a *plan-first prompt preamble* (protocol per task class) is a lightweight substitute for a workflow engine when the harness (Claude plan mode) already understands planning.

## 5. Multi-harness support

Implemented as a three-part plugin layer (full detail in wiki/03):

- Contract: `AIToolProtocol` (`core/tool_protocol.py:14-99`) — capability flags (`supports_hooks/headless/plan_mode`, `task_via_args`) + `get_command/is_installed/get_known_paths/install_hooks`.
- Registry: `ToolRegistry` (`core/tool_registry.py:286-322`) with 5 bespoke classes — `claude` (:96-141), `droid` (:144-180), `pi` (:183-232), `opencode` (:235-271), one-shot `clawcore` (:325-352) — plus generic `CustomTool` entries for codex/gemini/aider/amp/kilo-code (:277-283, :362-369).
- Config: `[tools.<name>]` tables (`config.py:175`, schema `docs/configuration.md:130-154`) registered *before* Pydantic validation (`config.py:322-326`) so validators accept new names; `task_via_args` tools get shell-quoted `{{task}}`/`{{worktree}}` substitution (`core/tool_registry.py:67-74`).
- Selection: `owt new --ai-tool <name>` passes through; otherwise priority `claude > pi > droid > opencode` (`core/agent_detector.py:14`), single-installed auto-picks, multiple prompt (`commands/worktree/_shared.py:24-41`).

Fleet mapping: fleet's `--coder` flag is the same idea; owt's edge is the *capability-flag matrix* (`supports_hooks/headless/plan_mode`) that lets generic code branch on what each harness can do instead of hardcoding per-harness paths — plus config-only registration, which is how a team adds a new model CLI without a code change.

## 6. What fleet can borrow (7 ideas, with sources)

1. **Conflict Guard as a pre-merge warning from stored file lists.** Intersect the merging branch's `git diff --name-only base...branch` with sibling tasks' last-reported modified files; warn, don't block. Steal from `core/merge.py:183-213` + `commands/merge_cmds.py:322-328`. Fleet already stores per-task state — this is a cheap query before `fleet merge`.
2. **Verb-action rows + context-sensitive footer.** Every board row exposes only its valid verbs; the footer renders the focused row's keys. Steal the pattern from `models/control_plane.py:30-75` (row = id + section + actions + meta) and `core/control_plane_view.py:412-438`. For fleet: a `fleet board` view where each task row shows only applicable actions (attach/ship/retry/drop).
3. **Prioritized lanes with empty-lane hiding.** NEEDS YOU first, then READY TO SHIP, then IN FLIGHT; hide empties so the top of the screen is always the decision. Steal from `core/control_plane_sections.py:32-208` and the `.empty{display:none}` rule (`core/control_plane_view.py:131-155`).
4. **Two-phase merge discipline.** Phase 1 proves the feature branch absorbs base cleanly; phase 2 touches base only afterwards, with autostash + abort discipline. Steal from `core/merge.py:328-574`. Eliminates the "merge broke main checkout" class of incidents.
5. **Smallest-first merge queue with overlap counts.** Order candidates by `(commits_ahead, overlap_count)` and display both numbers per row; stop `--ship` loops at the first conflict. Steal from `core/merge.py:283-326` + `commands/merge_cmds.py:575-606`. Directly applicable to fleet's multi-task shipping.
6. **PR-based shipping as a first-class exit.** `ship --pr` pushes + `gh pr create --fill` while leaving worktree/session/status intact (`core/merge.py:231-281`, `commands/merge_cmds.py:62-111`). For fleet: a `--pr` ship mode for tasks that need review instead of direct merge.
7. **Capability-flag harness matrix + config-only tool registration.** Branch generic code on `supports_hooks/headless/plan_mode` instead of per-harness special cases; let teams add CLIs via config tables. Steal from `core/tool_protocol.py:14-99` and `core/tool_registry.py:372-392` + `config.py:322-326`. Reduces the cost of each new `--coder` backend to a config stanza.

Non-borrows (deliberately not recommended): the 2-second full-rebuild poll loop (fleet's event-driven updates scale better); herdr-specific submit quirks (`core/herdr_backend.py:469-510`); the reported-not-live overlap source (fine for warnings, insufficient for hard guarantees).

**Covers:** all wiki pages, synthesized for the fleet comparison; primary sources `README.md`, `core/merge.py`, `core/control_plane_sections.py`, `core/control_plane_view.py`, `core/control_plane_actions.py`, `core/backend_factory.py`, `core/tool_registry.py`, `core/tool_protocol.py`, `core/agent_detector.py`, `core/prompt_builder.py`, `commands/merge_cmds.py`, `commands/worktree/new.py`, `commands/worktree/_shared.py`, `commands/worktree/attach.py`, `commands/doctor.py`, `models/control_plane.py`, `models/status.py`, `config.py`
