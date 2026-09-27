> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Control-Plane Cockpit (Textual TUI)

**In one sentence:** A deliberately thin Textual decision surface that polls worktree status every 2 seconds, sorts rows into three priority lanes, and dispatches single-key verb actions to `owt` subprocesses — all business logic lives outside the view.

## Key points

- The lane model is a 3-value enum `SectionKind` (`NEEDS_YOU / READY_TO_SHIP / IN_FLIGHT`) in `models/control_plane.py:18-28`; classification lives in `core/control_plane_sections.py`, not the view.
- NEEDS YOU = leftover merge/rebase state (MERGE_HEAD check) sorted first plus BLOCKED/ERROR tracker rows; READY TO SHIP = merge-queue candidates as `(name, commits_ahead, overlaps)` tuples; IN FLIGHT = WORKING rows sorted by recency.
- Empty lanes are hidden with CSS (`.empty{display:none}`), so the most important lane is always on top.
- Every row carries verb actions (`s`hip, `a`ttach, `d`iff, `f`ix, `m`erge, `x`delete); the footer renders only the focused row's keys, rebuilt on every render.
- The view is stateless about work: a 2-second poll (`REFRESH_SECONDS = 2.0`) rebuilds sections off-thread; there are no reactive watchers.
- `fix` opens `$EDITOR` and exits the cockpit (hands control to the human); `attach`/`diff` suspend the TUI and exec into the session/pager; `ship`/`merge` run as `owt` subprocesses.

---

## Lane model and classification

The three lanes are declared as `SectionKind` in `models/control_plane.py:18-28` with titles and mount order in `core/control_plane_view.py:72-83`. Classification is pure function work in `core/control_plane_sections.py`:

- `needs_you_section` (`core/control_plane_sections.py:32-83`): rows for worktrees with in-progress merge/rebase state (detected via `.git/MERGE_HEAD` / `rebase-merge` presence), sorted first, plus rows whose tracker status is BLOCKED or ERROR.
- `ready_to_ship_section` (`core/control_plane_sections.py:91-134`): rows built from `MergeManager.plan_merge_order()` output — each row carries `(name, commits_ahead, overlap_count)`.
- `in_flight_section` (`core/control_plane_sections.py:142-177`): rows with WORKING status, sorted by `updated_at` descending.
- `build_all_sections` (`core/control_plane_sections.py:185-208`) orchestrates the three builders.

Empty lanes are hidden, not shown as empty boxes: `SectionWidget.DEFAULT_CSS` (`core/control_plane_view.py:131-140`) sets `.empty{display:none}`, and `update_rows` (`core/control_plane_view.py:148-155`) toggles the class. The view mounts all three sections in `compose` (`core/control_plane_view.py:272-276`) and skips empty ones at render.

## Verb actions and dispatch

Row verbs are declared in `models/control_plane.py:30-57` (`RowAction`: `SHIP=s, ATTACH=a, FIX=f, MERGE=m, DIFF=d, DELETE=x`). Keybindings live in `core/control_plane_view.py:227-240`: `n` → new-work dialog, `s/d/a/f/m/x` → `action_dispatch(key)`, `q` → quit, arrows/`j/k` → focus.

Per-row exposure differs by lane (`core/control_plane_sections.py`): conflict rows get `(FIX, ATTACH, DELETE)` (:54); blocked/error rows get `(ATTACH, DELETE)` (:72); ready-to-ship rows get `(SHIP, DIFF, ATTACH, DELETE)` (:130); in-flight rows get `(ATTACH, DELETE)` (:166).

Dispatch goes through a table in `core/control_plane_actions.py:193-203` mapping `(section, action)` pairs to handlers (`action_ship:84-86`, `action_merge:89-91`, `action_attach:94-98`, `action_delete:101-105`, `action_fix:108-124`). The view gate `action_dispatch` (`core/control_plane_view.py:493-515`) rejects keys not in the focused row's `actions`; `d` (diff) and `x` (delete) are special-cased to `_review_diff` (:533) and `_confirm_delete` (:517) and never reach the dispatcher. `n` (new work) is not a row action at all: `action_new` (`core/control_plane_view.py:590-592`) chains `InputModal → SearchableSelectModal → ConfirmModal → _do_start_work` (:632-636).

## What fix / attach / diff actually do

A premise worth correcting: neither `fix` nor `merge` restarts a worker.

- `fix` (`core/control_plane_actions.py:108-124`) opens `$EDITOR` on the conflicted files or worktree and sets `handoff=True`, which exits the cockpit (`core/control_plane_view.py:579-582`) — the human resolves, then returns.
- `attach` (`core/control_plane_actions.py:94-98`) prefers `runtime.backend_attach`, else falls back to `_run_owt(["attach", ...])`. The view helper `_attach_via_suspend` (`core/control_plane_view.py:560-577`) suspends the TUI and runs `owt attach <wt>` on the real terminal.
- `diff` similarly suspends into `git diff` plus the pager (`core/control_plane_view.py:533-558`, argv built by `build_diff_args` in `core/control_plane_actions.py:178-180`).
- `merge`/`ship` are plain `_run_owt(["merge"|"ship", worktree])` subprocess calls — the same CLI verbs scripts use.

`core/pane_actions.py` (backend session create/teardown) and `core/quick_actions.py` (`on_create` hooks) are not cockpit verbs; the cockpit reaches them only indirectly through those subprocesses.

## Refresh loop and footer

- Poll loop: `REFRESH_SECONDS = 2.0` (`core/control_plane_view.py:70`); `set_interval` + `call_after_refresh(_tick)` (:290-291). `_tick` (:316-322) rebuilds sections on a worker thread (tracker `get_all_statuses` + `_safe_merge_queue` (:335-343) + `_detect_conflicts` (:345-354)), then repaints header and sections.
- No Textual reactive watchers: focus is manual via `_Focus(section, row)` (:120-125), `_set_focus_from_global` (:481-489), `_focused_global_index` (:452-459).
- Footer: `_build_footer` (`core/control_plane_view.py:412-432`) always shows navigation + `n`/`q` plus only the focused row's actions (`row.actions`, :427-430); `_update_footer` (:434-438) refreshes it on every render, so the footer is a per-row capability display.
- Header usage line is snapshotted once at `on_mount` (:285-289); toasts auto-hide after 3–5 s (:638-652). Theming comes from `core/theme.py` via `_apply_theme` (:293-306); `popup/picker.py` is a separate curses `tmux display-popup` tool, unused by the cockpit.

**Covers:** `core/control_plane_view.py`, `core/control_plane_sections.py`, `core/control_plane_actions.py`, `core/modals.py`, `core/pane_actions.py` (session side), `core/quick_actions.py` (hook side), `models/control_plane.py`
