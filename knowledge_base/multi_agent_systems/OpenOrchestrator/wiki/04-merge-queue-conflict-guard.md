> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Merge, Conflict Guard, Queue, Worktree Lifecycle

**In one sentence:** Shipping is a two-phase merge (update the feature branch first, then the base) guarded by file-overlap warnings from the status database, ordered by a smallest-first queue, with PR-based shipping and full teardown as the exits.

## Key points

- Conflict Guard is file-overlap detection, not semantic merge prediction: `get_modified_files` runs `git diff --name-only {base}...{branch}` (`core/merge.py:183-189`); `check_file_overlaps` (:191-213) intersects that set with peers' `modified_files` from the status DB (not live diffs of peer worktrees).
- The pre-merge warning is advisory only: `commands/merge_cmds.py:322-328` prints the top-5 overlaps before confirmation but never blocks.
- Two-phase merge (`MergeManager.merge`, `core/merge.py:328-438`): phase 1 merges/rebases the base into the feature branch inside the worktree (:440-491); phase 2 checks out the base in the main checkout, merges the feature, and restores branch + autostash (:522-574). Any phase-1 conflict aborts before phase 2 is attempted.
- Options: `--rebase` (rebase path :471-491), `--strategy ours|theirs` → `merge -X <strategy>` (:503-507), `--leave-conflicts` skips the abort and leaves the merge/rebase in progress (:487-490, :514-518). `ship --pr` rejects all three (`commands/merge_cmds.py:417-420`).
- Queue ordering (`plan_merge_order`, `core/merge.py:283-326`): only COMPLETED/WAITING rows; each candidate scores `(commits_ahead, overlap_count)`; sort is smallest-first unless an explicit DAG `dependency_order` is supplied. Branch age and size play no role.
- `queue --ship` (`commands/merge_cmds.py:575-606`) merges in order with worktree deletion and stops at the first conflict.
- PR shipping (`create_pr`, `core/merge.py:231-281`): push + `gh pr create --fill`; the worktree, session, and status stay intact — only the status flips to WAITING (`commands/merge_cmds.py:103-111`).
- Worktree creation wires branch naming, dependency install, `.env` copy, and hooks; deletion is a best-effort full teardown; `owt doctor` finds orphans across worktrees, branches, sessions, and status rows without auto-deleting session-less directories.

---

## Conflict Guard

`get_modified_files(branch, base)` (`core/merge.py:183-189`) shells to `git diff --name-only {base}...{branch}` (triple-dot; no `merge-tree` anywhere in the codebase). `check_file_overlaps(worktree_name, base_branch)` (`core/merge.py:191-213`) intersects that set against every other worktree's `s.modified_files` pulled from `StatusTracker.get_all_statuses()` — i.e. the last-reported file lists in SQLite, not live `git diff` output from peer worktrees — and returns `{file: [other_worktree, ...]}`. The live-conflict reader `_get_conflict_files` (:81-87) is separate: `git diff --name-only --diff-filter=U`.

The user-facing warning (`commands/merge_cmds.py:322-328`) prints `⚠ File overlap warning` with the top 5 files before the confirmation prompt and does not block the merge.

## Two-phase merge

`MergeManager.merge()` (`core/merge.py:328-438`):

- Phase 1 — `_phase1_merge_into_feature` (:440-469): fetch `origin <base>`, prefer `origin/<base>` else the local base, then merge (or rebase on `--rebase`) inside the worktree. Rebase failure (:483-491) and merge failure (:493-520) collect `_get_conflict_files()`, run `merge --abort` / `rebase --abort` unless `leave_conflicts`, and raise `MergeConflictError`. Phase 2 is never attempted after a phase-1 failure. Zero commits ahead short-circuits to `ALREADY_MERGED` (:397-404).
- Phase 2 — `_phase2_merge_into_base` (:522-556): autostash the main checkout (`stash push -u -m owt-merge-autostash`), `clean -fdX`, checkout the base, `merge <feature> --no-edit`, then restore branch + stash (:558-574).

```python
# core/merge.py:493-518 (paraphrase of structure) — merge with strategy + abort discipline
merge_args = [merge_ref, "--no-edit"]
if strategy: merge_args += ["-X", strategy]
wt_repo.git.merge(*merge_args)  # except: conflicts = _get_conflict_files()
# if not leave_conflicts: merge --abort; raise MergeConflictError(...)
```

CLI flags for both `merge` (:220-222) and `ship` (:381-389) are defined in `commands/merge_cmds.py`; conflict hints print at :38-47.

## Queue, PR shipping, lifecycle

Queue planner `plan_merge_order` (`core/merge.py:283-326`): considers only COMPLETED/WAITING rows; per candidate computes `(name, commits_ahead, overlap_count)` via `count_commits_ahead` (`rev-list --count base..branch`, :215-229) plus `check_file_overlaps`. With an explicit DAG `dependency_order` it sorts topologically, otherwise `candidates.sort(key=(commits, overlaps))` — fewest commits, then fewest overlaps (:319-325). `queue --ship` (:575-606) confirms, then loops `merge(delete_worktree=True)` + `teardown_worktree`, stopping at the first `MergeConflictError` ("Skipping remaining…").

PR shipping: `create_pr` (`core/merge.py:231-281`) requires an `origin` remote and `commits_ahead > 0`, runs `git push -u origin <branch>`, resolves `gh` via safe-PATH lookup, and runs `gh pr create --head <src> --base <dst> --fill`, returning the last stdout line (the PR URL); `gh` errors surface verbatim. `_ship_pr` (`commands/merge_cmds.py:62-100`) optionally auto-commits (`git add -A`), pushes + opens the PR, and deliberately leaves worktree/session/status intact, best-effort flipping status to WAITING (:103-111). Entry points at :458-462 (worktree) and :136-138 (branch mode).

Worktree lifecycle: `WorktreeManager.create` (`core/worktree.py:209-276`, `worktree add [-b branch path base_sha]`, detached/empty-repo guards); paths are `{project}-{sanitized-branch}` (:75-89, `/→-`, strip `[^\w-]` at :61-73). Branch names come from `generate_branch_name` (`core/branch_namer.py:128-165`, keyword→prefix, default `feat`) via `commands/worktree/_shared.py:44-68`, with a ref-conflict prompt at :81-97. Environment setup (`core/environment.py:97-135`: `.env` copy + dep install at :214-284 and :137-212) is wired in `core/pane_actions.py:188-189`. Deletion: `WorktreeManager.delete` (:346-380, `git worktree remove [--force]`, refuses main); full `teardown_worktree` (`core/pane_actions.py:331-371`: kill backend session + delete worktree/branch + clean status, best-effort list); `commands/worktree/delete.py:42-63` splits branch vs worktree paths; successful merge auto-deletes at `core/merge.py:430-436`. Orphan detection (`owt doctor`, `commands/doctor.py:82-113`) cross-checks status rows against `git worktree list` and `git branch --list` (orphan iff dead session and branch gone, :110-113), flags `status-no-worktree` / `session-no-worktree`, and `--fix` kills sessions/clears rows (:160-202) but never auto-deletes session-less worktree dirs (:148-155).

**Covers:** `core/merge.py`, `commands/merge_cmds.py`, `core/sync.py`, `core/cleanup.py`, `core/worktree.py`, `core/pane_actions.py` (teardown), `commands/worktree/new.py`, `commands/worktree/delete.py`, `commands/worktree/attach.py`, `commands/doctor.py`, `core/branch_namer.py`
