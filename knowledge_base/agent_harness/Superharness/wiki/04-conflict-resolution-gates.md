> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Conflict Resolution and Lifecycle Gates

**In one sentence:** Superharness prevents agent conflicts with per-agent git worktrees plus hook-layer write/push guards, and prevents premature progress with dispatch-time gates (status, preflight, policy, plan quality) and close-time gates (status, subtask resolution, verification, ownership).

## Key points

- scope-guard does **not** compare agents' file sets against each other; it is a PreToolUse hook on `Write|Edit` that deny-blocks secrets/keys and warn-asks on system paths (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:1-8`, `src/superharness/adapters/claude-code/hooks/hooks.json:15-25`).
- Overlap prevention between concurrent agents comes from **worktree isolation** (one git worktree per dispatch slot), not from scope-guard (`src/superharness/engine/worktree_ops.py:38-50`, `src/superharness/engine/parallel_dispatch.py:200-215`).
- Branch guard blocks pushes to `main`/`master` and bare `--force`, resolving refspecs by tokenizing (not regex over the whole command) (`src/superharness/adapters/claude-code/hooks/branch_guard.py:63-102`, `src/superharness/adapters/claude-code/hooks/branch_guard.py:138-159`).
- Dispatch is gated in order: workflow status gate, then preflight (`src/superharness/commands/delegate.py:912-946`, `src/superharness/commands/delegate.py:952-977`).
- Preflight hard-blocks on unmet dependencies and unmet `requires:`/mandate capabilities; spec/TDD/acceptance-criteria gaps only warn (`src/superharness/engine/preflight.py:197-208`, `src/superharness/engine/preflight.py:355-459`, `src/superharness/engine/preflight.py:648-658`).
- `close` requires status `report_ready`/`review_passed`, zero blocking subtasks, `verified=true`, and matching owner — each bypassable only by an explicit flag that is ledger-logged (`src/superharness/commands/close.py:57-58`, `src/superharness/commands/close.py:123-168`, `src/superharness/commands/close.py:180-198`).
- The subtask gate is off by default; profile flag wins, task flag can only tighten (`src/superharness/engine/subtask_gate.py:3-10`, `src/superharness/engine/subtask_gate.py:51-58`).
- Enforcement parity is partial and pinned by contract test: hook trees must stay byte-identical and CI/pre-commit gates must not drift, while engine gates are re-checked at each entry point (CLI `close` + `task`, watcher, MCP approval) rather than in one choke point (`tests/contract/test_enforcement_parity.py:233-261`, `src/superharness/commands/close.py:139-157`, `src/superharness/commands/task.py:739-749`).

---

## File-overlap prevention (scope-guard mechanism: what it compares, where it hooks in)

Scope-guard is bound as `PreToolUse` on matcher `Write|Edit` (`src/superharness/adapters/claude-code/hooks/hooks.json:15-25`). It parses `tool_input.file_path` from stdin JSON (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:15`) and applies, in order:

1. Fail-closed parse: unparseable input returns `ask`, not silent allow (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:18-21`).
2. Sensitive-file deny list, always enforced regardless of contract: `*.env`, `*.env.*`, `*credentials*`, `*secrets.json|yaml|yml|toml`, `*.pem`, `*.key`, `*/.ssh/*`, `*/.kube/config`, `*terraform.tfvars`, `*.tfvars`, `*.tfvars.json` — with a carve-out allowing `*.env.example` (checked-in placeholder template) (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:27-42`). Pinned by `tests/unit/test_scope_guard.py:18-55` (e.g. `secrets.txt` allows, `secrets.json` denies).
3. Scratchpad allow: `/tmp/claude-*/*` is a sanctioned agent work area and returns `allow` — but only after the sensitive-file deny, so a key inside the scratchpad is still blocked (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:49-54`, `tests/unit/test_scope_guard.py:49-52`).
4. System-path warn: `/etc/*`, `/usr/*`, `/var/*`, `/tmp/*` return `ask` (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:57-70`, `tests/unit/test_scope_guard.py:44-46`).
5. Inactive-project passthrough: no `.superharness/state.sqlite3` means `allow` (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:73-76`); otherwise allow (`src/superharness/adapters/claude-code/hooks/scope-guard.sh:78-79`).

What it does not do: compare one agent's target files against another agent's. There is no file-set intersection check anywhere in the hook. Cross-agent write conflicts are handled structurally by worktree isolation (below) and by serializing dispatch through status/preflight gates.

Companion hook: `ledger-append.sh` is `PostToolUse` on `Write|Edit` and appends one line per modified file to `.superharness/ledger.md`, skipping self-writes and `.superharness/` protocol files (`src/superharness/adapters/claude-code/hooks/hooks.json:37-48`, `src/superharness/adapters/claude-code/hooks/ledger-append.sh:9-38`). It is audit trail, not a gate.

## Branch guard

Bound as `PreToolUse` on matcher `Bash` (`src/superharness/adapters/claude-code/hooks/hooks.json:26-35`); the shell wrapper execs the Python implementation (`src/superharness/adapters/claude-code/hooks/branch-guard.sh:13`). Protected set is `{"main", "master"}` (`src/superharness/adapters/claude-code/hooks/branch_guard.py:31`).

Mechanism (`src/superharness/adapters/claude-code/hooks/branch_guard.py:19-20`, `src/superharness/adapters/claude-code/hooks/branch_guard.py:121-130`): split the command on shell separators (`SEGMENT_SPLIT` over `&&`, `||`, `;`, `|`, newline, `src/superharness/adapters/claude-code/hooks/branch_guard.py:35`), `shlex.split` each segment, and only judge segments containing both `git` and `push`. This replaced whole-string regexes that both over-blocked (the word "main" later in the command denied a feature-branch push) and under-blocked (`HEAD:main` colon form, bare `git push` from a protected branch) (`src/superharness/adapters/claude-code/hooks/branch_guard.py:7-18`).

`push_targets()` skips flags and valued flags, treats the first positional as remote and the rest as refspecs, resolves `src:dst` to the destination side, strips leading `+` and `refs/heads/`, and for a bare push (no refspecs) resolves the destination via `git rev-parse --abbrev-ref HEAD` (`src/superharness/adapters/claude-code/hooks/branch_guard.py:63-102`). Verdicts: bare `--force` without `--force-with-lease` is `deny` (`src/superharness/adapters/claude-code/hooks/branch_guard.py:138-143`); unresolvable target is `ask` (`src/superharness/adapters/claude-code/hooks/branch_guard.py:145-151`); any target in `PROTECTED` is `deny` (`src/superharness/adapters/claude-code/hooks/branch_guard.py:152-159`); `git reset --hard` / `clean -f` / `checkout -- .` and `rm -rf /` patterns warn via `ask` (`src/superharness/adapters/claude-code/hooks/branch_guard.py:161-173`); empty/unparseable input allows unless raw stdin was non-empty (`src/superharness/adapters/claude-code/hooks/branch_guard.py:105-119`). A `gitlab`-prefixed push remote (LAN mirror) is skipped (`src/superharness/adapters/claude-code/hooks/branch_guard.py:132-136`).

## Dispatch-time gates (preflight, policy_gate, plan_validator — what each rejects)

Order in `delegate`: workflow status gate first, preflight second, both before prompt build (`src/superharness/commands/delegate.py:900-911`, `src/superharness/commands/delegate.py:948-960`).

Status gate: implementation workflow without `--plan-only` dispatches only from `plan_approved`/`in_progress` (plus `pr_open`, and `review_requested` when `for_review`); `todo`/`plan_proposed` are blocked with a "plan must be approved" message; `quick` allows `todo`; `approval` allows only `pending_user_approval` (`src/superharness/commands/delegate.py:912-930`, `tests/unit/test_lifecycle.py:43-78`, `tests/unit/test_lifecycle.py:105-116`). A block writes a `gate_block` decision-log entry and returns a permanent (non-retryable) exit (`src/superharness/commands/delegate.py:932-946`).

Preflight (`run_preflight`, `src/superharness/engine/preflight.py:666-713`): `pass`/`warn`/`block` report with `can_dispatch = not has_block` (`src/superharness/engine/preflight.py:695-713`); delegate prints non-pass summaries and aborts on `can_dispatch == False` with a `gate_block` log (`src/superharness/commands/delegate.py:961-977`). Block-level checks: `blocked_dependency` when any `blocked_by`/`depends_on` task is not `done`/`archived` (`src/superharness/engine/preflight.py:197-208`); missing required skill/CLI/env/MCP when merged `requires:` (profile baseline + signal-derived + per-task, override wins) has `fail_mode: block` (`src/superharness/engine/preflight.py:355-381`, `src/superharness/engine/preflight.py:387-449`); `mandate_requires_missing` when the task matches profile `mandate_requires_for` (ship/effort/test_types) but has no explicit per-task `requires:` block (`src/superharness/engine/preflight.py:636-658`). Warn-level: missing title/owner, missing TDD red/green, missing or oversized (>6) acceptance criteria, dirty worktree, prior failures (`src/superharness/engine/preflight.py:89-166`, `src/superharness/engine/preflight.py:462-514`). Preflight never blocks on its own internal errors (`src/superharness/commands/delegate.py:984-986`).

Policy gate (`check_agent_policy`, `src/superharness/engine/policy_gate.py:9-34`): blocks on `loop_detected` unconditionally and on `cost_usd > max_cost_usd`. Dispatch-path caller is the watcher loop-guard: on a `block` loop verdict it invokes the policy check and skips dispatch (`src/superharness/commands/inbox_watch.py:3210-3232`).

Plan validator (`validate_plan`, `src/superharness/engine/plan_validator.py:96-111`): blocks auto-approval (not dispatch itself) when any heuristic fails — missing `tdd.{red,green,refactor}` (`src/superharness/engine/plan_validator.py:39-49`), empty plan body or `TODO|FIXME|XXX|placeholder|???` markers (`src/superharness/engine/plan_validator.py:30-36`, `src/superharness/engine/plan_validator.py:52-61`), missing risks section (`src/superharness/engine/plan_validator.py:64-68`), or any acceptance criterion with zero significant-word overlap in plan/TDD text (`src/superharness/engine/plan_validator.py:71-93`). Caller `task.py` prints failures and returns without approving (`src/superharness/commands/task.py:701-719`).

Note on similarly named modules: `behavioral.py` (adaptive user/project profiles with confidence, hysteresis, trials) and `behavioral_validator.py` (HTTP assertion runner over `behavioral_assertions` against a live service) are not dispatch/lifecycle gates (`src/superharness/engine/behavioral.py:1-9`, `src/superharness/engine/behavioral_validator.py:1-20`).

## Lifecycle gates (which transitions require what: approval, consensus verdict, verify-on-close)

Terminal statuses are `done`, `failed`, `stopped` (`tests/unit/test_lifecycle.py:122-123`).

Approval: `pending_user_approval` status (or `approval_gate.required && !approved`) marks a pending approval, surfaced by `discuss status`/`contract_today`/`status --fix` health checks (`src/superharness/engine/discuss.py:78-129`, `src/superharness/commands/status.py:1204-1209`, `src/superharness/commands/contract_today.py:193-203`). Approving writes `approval_gate.{required,approved_by_user,approved_at,approved_by}` and moves the task back to `todo` (or leaves terminal statuses untouched) (`src/superharness/engine/discuss.py:238-291`). Implementation tasks sitting in `todo` cannot be delegated until the plan is approved (`src/superharness/commands/delegate.py:916-923`). MCP-layer approval is separate and risk-based: low-risk tools auto-approve, medium/high raise `ApprovalPending` until an operator approves (`src/superharness/mcp/approval.py:4-5`, `src/superharness/mcp/approval.py:101-105`).

Consensus verdict: discussion rounds accept `agree|disagree|partial|consensus|abstain`; auto-transition to `consensus` requires quorum over agent participants, and only blocking verdicts become follow-up tasks (`src/superharness/engine/discussion.py:249-313`, `src/superharness/engine/discussion.py:323-361`). Unclosed `consensus` discussions are flagged and auto-closeable via `status --fix` (`src/superharness/commands/status.py:772-777`, `src/superharness/commands/status.py:979-991`).

Verify-on-close (`close_task`, `src/superharness/commands/close.py:89-99`): four ordered gates. (1) Ownership: non-empty owner rejects other actors (`src/superharness/commands/close.py:115-121`). (2) Status: current status must be in `{"report_ready", "review_passed"}` unless `--force` (`src/superharness/commands/close.py:57-58`, `src/superharness/commands/close.py:123-133`). (3) Subtask resolution gate (below) unless `--force`; `--cancel-remaining` requires `--cancel-reason` and bulk-cancels open subtasks with ledger lines (`src/superharness/commands/close.py:137-157`, `src/superharness/commands/close.py:60-86`, `src/superharness/commands/close.py:173-177`). (4) Verification: `task_row.verified` must be true unless `--skip-verify`, else the error directs to `superharness verify --id … --method … --result pass` (`src/superharness/commands/close.py:161-168`). `--force` with open subtasks appends a `FORCE_CLOSE_WARNING` ledger line (`src/superharness/commands/close.py:180-198`); success persists `status=done` + `done_at`, ledger `CLOSE` line, handoff YAML, inbox sync, `on_close` module hooks, and dispatch-worktree cleanup (`src/superharness/commands/close.py:200-336`). The `task status --status done` path duplicates the subtask gate plus an acceptance-criteria warning (`src/superharness/commands/task.py:738-762`).

Subtask gate (`src/superharness/engine/subtask_gate.py:45-68`): `enabled = profile.require_subtask_resolution or task.require_subtask_resolution`, source recorded as `profile|task|none`; blocking = subtasks whose status is not resolved per `is_subtask_resolved` (open: `pending`, `in_progress`, `failed`; resolved: `done`, `cancelled`) (`src/superharness/engine/subtask_gate.py:3-10`, `src/superharness/engine/subtask_gate.py:60-68`). Error text prescribes resolve/cancel, `--cancel-remaining`, or `--force` (`src/superharness/engine/subtask_gate.py:77-91`):

```sh
shux close --id demo.task --cancel-remaining --reason "<why>"
```

```python
enabled = profile_flag or task_flag
source = "profile" if profile_flag else ("task" if task_flag else "none")
# src/superharness/engine/subtask_gate.py:54-55
```

```sh
superharness: BLOCKED — this would push to main. Never push directly to a protected branch. Use a feature branch and PR.
# src/superharness/adapters/claude-code/hooks/branch_guard.py:153-159
```

## Worktree isolation (per-agent worktrees, dispatch state isolation)

Each parallel slot gets its own branch + worktree: `git worktree add -b <branch> <path> HEAD`, tracked as a `WorktreeSlot(index, branch, worktree_path, status, result, error, cost, duration)` (`src/superharness/engine/worktree_ops.py:23-50`). Task ids are sanitized for branch/path safety (`sanitize_task_id`, `src/superharness/engine/worktree_ops.py:11-20`). `.superharness/` state is symlinked (not copied) into the worktree so the agent has context while the SQLite source of truth stays shared (`src/superharness/engine/worktree_ops.py:71-79`). Both `parallel_dispatch` and `swarm` follow create → symlink-state → `WorktreeSlot` per slot (`src/superharness/engine/parallel_dispatch.py:200-215`, `src/superharness/engine/swarm.py:139-152`).

Manual surface mirrors this: `shux worktree create <task-id>` does a detached `git worktree add` under `<tmp>/superharness-worktrees/<task-id>-<rand>` plus the `.superharness` symlink; `remove` unlinks the symlink then `worktree remove --force` + `prune`; `gc` reaps orphaned dispatch worktrees (`src/superharness/commands/worktree.py:83-127`, `src/superharness/commands/worktree.py:129-170`). On close, the recorded `tasks.worktree_path` is removed only after a realpath containment check (`_worktree_path_is_safe`, `src/superharness/commands/close.py:22-41`) with symlink unlink, `worktree remove --force`, fallback `rmtree`, and `prune` (`src/superharness/commands/close.py:289-330`).

## Enforcement parity (same rule enforced in CLI, MCP tools, hooks — cite parity test)

Parity here means: the same invariant is checked at every entry point that could violate it, and the check copies cannot silently drift. What the contract test actually pins is the drift half: the two hook trees (`adapters/claude-code/hooks/` and `src/superharness/adapters/claude-code/hooks/`) must be byte-identical in both directions with a shrink-only allowlist (`tests/contract/test_enforcement_parity.py:233-261`, rationale `tests/contract/test_enforcement_parity.py:34-62`); the pre-commit hook must unset `GIT_DIR`/`GIT_INDEX_FILE` (`tests/contract/test_enforcement_parity.py:106-119`), keep `-m "not network"` in both fast and full branches (`tests/contract/test_enforcement_parity.py:122-142`), and name existing subset paths (`tests/contract/test_enforcement_parity.py:264-272`); CI's unit job must run the full `tests/unit` suite with `-n auto --dist loadfile` coverage runs whose `--cov-fail-under` equals `pyproject.toml`'s floor (`tests/contract/test_enforcement_parity.py:159-230`).

Rule-level duplication observed (defense in depth, not single choke point): the subtask gate runs in both `close_task` (`src/superharness/commands/close.py:139-157`) and `task status --status done` (`src/superharness/commands/task.py:739-749`); the status lifecycle gate runs in `delegate` with `gate_block` logging (`src/superharness/commands/delegate.py:912-946`) while close enforces its own `_CLOSE_ALLOWED_STATUSES` (`src/superharness/commands/close.py:57-58`); loop policy is constructed in `policy_gate` (`src/superharness/engine/policy_gate.py:9-34`) and invoked on the watcher path (`src/superharness/commands/inbox_watch.py:3221-3232`); approval exists independently in the MCP risk gate (`src/superharness/mcp/approval.py:101-105`), the discussion approval gate (`src/superharness/engine/discuss.py:238-244`), and the delegate plan-approval block (`src/superharness/commands/delegate.py:916-923`). Hook-layer rules (scope/branch deny lists) have no second enforcement inside CLI/MCP code — their parity guarantee is the byte-identical hook test above.

**Covers:** scope-guard.sh, branch-guard.sh, branch_guard.py, hooks.json, ledger-append.sh, policy_gate.py, plan_validator.py, preflight.py, subtask_gate.py, worktree_ops.py, commands/worktree.py, behavioral.py, behavioral_validator.py, test_enforcement_parity.py, test_scope_guard.py, test_lifecycle.py (commit 9c2166dccac6717b8b4056a8eae87c44052d77d5).
