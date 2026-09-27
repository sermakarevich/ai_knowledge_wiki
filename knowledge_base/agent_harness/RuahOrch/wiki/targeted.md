> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Ruah File-Claim Orchestration: Answers to Fleet's Targeted Questions

**In one sentence:** Ruah coordinates parallel coding agents through declared file-claim locks, durable artifacts, DAG workflows with claim-aware scheduling, and harness-agnostic executors — all with zero runtime dependencies.

## Key points

- Claims are three glob buckets (owned exclusive-write, shared append-only, read-only) with fixed match precedence owned > shared-append > read-only, enforced both before start (overlap/scope rejection) and after execution (contract validation).
- State is a single versioned JSON file with atomic temp-write plus rename, an `O_EXCL` lock file, revision-based stale-write rejection, in-place migration to version 2, and git reconciliation that only auto-cleans terminal or merged tasks.
- Workflows are Markdown task graphs validated as DAGs, staged by ready-set expansion, and scheduled per stage as parallel, parallel-with-contracts, or serial based on claim-overlap ratio (>0.3) and risk score (>2.0).
- Seven executors (claude-code, aider, codex, codex-mcp, open-code, script, raw) are selected by the task's `executor` string field and spawned in an isolated git worktree with `RUAH_*` environment variables.
- Fleet can borrow at least seven concrete ideas: claim locks with pre-start rejection, artifact capture with patch plus validation triple, append-only shared contracts, atomic state writes with revision guards, claim-aware parallel/serial planning, `RUAH_*` env-var subagent context, and zero-dependency git-worktree isolation.

---

## 1. Design principles (claims over files, artifacts, compatibility checks)

Ruah's central idea: **parallel agents are safe only when each one declares which files it may touch, and the orchestrator enforces that declaration.** Everything else is scaffolding around that contract.

- **Claims over files, not branches.** A `ClaimSet` is three glob lists — `ownedPaths` (exclusive write), `sharedPaths` (append-only write), `readOnlyPaths` (read, never write) — plus optional symbol/interface refinements (`claims.ts:3-9`). Normalization (backslash-to-slash, trim, strip trailing slash, dedupe) keeps glob comparison predictable (`claims.ts:45-59`, `claims.ts:69-80`). See [[01-claims-and-artifacts|Claims, Artifacts, and Contract Enforcement]].
- **Precedence is fixed.** `findClaimMatch` checks owned first, then shared-append, then read-only (`claims.ts:165-186`). An agent that owns `src/api/**` wins over one that merely reads it.
- **Artifacts make work durable and auditable.** `TaskArtifact` stores identity (`taskName`, `workspaceId`), history pointers (`baseRef`, `headRef`, `commitSha`), content (`changedFiles`, full `patch`), the claim set in force, and a validation triple (`executorSuccess`, `contractSuccess`, optional `gatesSuccess`) (`artifact.ts:5-21`, `artifact.ts:38-63`). An artifact with empty `changedFiles` and empty `patch` counts as absent (`artifact.ts:72-77`).
- **Compatibility checks are data plus computation.** `CompatibilitySignal` carries `clean`, `staleBase`, `needsReplay`, `conflictingFiles` (`claims.ts:33-43`); the planner converts overlap, file-size weights, history penalties, and compatibility conflicts into a risk score that drives scheduling (`planner.ts:183-198`, `planner.ts:239-246`).
- **Zero runtime dependencies is a principle, not an accident.** `packages/core/package.json` lists only `devDependencies` (typescript, @types/node, biome) — no `dependencies` key at all. All git, filesystem, and process work uses Node.js built-ins (`node:child_process`, `node:fs`).

## 2. Worker restart handling (process-safe state writes, stale-write rejection, state migration)

All orchestration state lives in one JSON document at `<root>/.ruah/state.json` (`state.ts:67-78`, `state.ts:120-122`). Full detail in [[02-state-and-restart-safety|State, Persistence, and Restart Safety]].

- **Process-safe writes.** Concurrent CLI processes serialize on a lock file at `<root>/.ruah/state.lock` created with `O_EXCL` (`wx`), polling every 50 ms with a 5 s timeout; locks older than 30 s count as stale (`state.ts:93-96`, `state.ts:179-223`).
- **Crash-safe persistence.** `saveState` writes the full document to `state.json.<rand>.tmp` then atomically renames over the old file, holding the lock for the whole read-modify-write cycle and always releasing it in `finally` (`state.ts:234-263`).
- **Stale-write rejection.** Each document carries a monotonically increasing `revision`. `saveState` re-reads disk under the lock and throws `"State changed on disk while this command was running..."` when the in-memory revision differs, writing nothing; on match it persists `revision + 1` (`state.ts:240-247`, `state.ts:251-259`).
- **State migration.** Every load runs `migrateStateShape` (force `version` to 2, backfill `artifacts`/`baseBranch`, upgrade each task) plus `parseState` backfills (derive `claims` from `files` and vice versa, synthesize `workspace` handles from legacy `worktree`/`branch`, default `integration`) (`state-migrations.ts:36-113`, `state.ts:132-177`).
- **Restart reconciliation.** `reconcileStateWithGit` removes `merged`/`cancelled` tasks unconditionally, removes `done` tasks only when both branches exist and the task branch is merged into its base, and leaves `created`/`in-progress`/`failed` untouched — deliberately avoiding the "disappearing tasks" false positive where a fresh branch is trivially an ancestor of its base (`reconcile.ts:17-70`).

## 3. Conflict resolution (lock scopes rejected before start, contract enforcement read-only/shared-append, merge in dependency order)

Ruah resolves conflicts in three layers: **before start, after execution, at merge.**

- **Before start: overlap and scope checks.** `claimSetsOverlap` reports every pair of overlapping patterns across two claim sets (`claims.ts:188-206`); `claimSetWithinScope` reports child patterns outside the parent scope, with an empty parent set allowing everything (`claims.ts:208-231`). Task creation validates file locks and parent scope before any worktree or agent exists (`task.ts:279-305`).
- **After execution: contract enforcement.** `validateContractChanges` lists changed files against the base ref and validates each in owned, read-only, shared, outside-contract order (`contract-validator.ts:90-163`). Owned matches pass; read-only matches fail as `read-only` violations; shared matches run append-only validation (missing base passes, deletion/move fails, changed content must start with original bytes without reducing line count) and fail as `shared-append` violations; unmatched files fail as `outside-contract` (`contract-validator.ts:47-84`, `contract-validator.ts:114-156`).
- **At merge: dependency order plus gates.** `getExecutionPlan` emits ready-set stages by fixed-point expansion (`workflow.ts:239-267`); `workflow run` iterates stages in order, validates contracts and optional per-stage compatibility (marking integration clean/stale/conflict, exiting on pairwise conflict), runs governance gates per workspace, then merges each task branch in stage order (`commands/workflow.ts:183-199`, `commands/workflow.ts:417-509`). Task-level `merge` additionally blocks on unmerged children and defers governance gates for subtasks to the parent merge (`task.ts:498-586`).

## 4. Workflow abstraction and implementation (Markdown task graphs, DAG validation, claim-aware parallel/serial decision, parent/child branching)

Full mechanism in [[03-planner-and-workflows|Planner, DAG Workflows, and Claim-Aware Scheduling]].

- **Markdown task graphs.** Workflow files use `# Workflow: <name>`, a `## Config` block (`base`, `parallel`, `on_conflict`), and one `### <task>` section per task with `files`, `executor`, `depends`, `prompt`, `on_conflict` fields (`workflow.ts:59-180`). Defaults: base `main`, parallel `false`, on-conflict `fail` (only `fail`/`rebase`/`retry` accepted) (`workflow.ts:42-46`).
- **DAG validation.** Unknown dependencies produce one error per bad edge; cycle detection runs depth-first search with a recursion stack (`workflow.ts:194-237`). Both `run` and `plan` validate before planning anything (`commands/workflow.ts:104-110`).
- **Stage computation.** `getExecutionPlan` repeatedly selects tasks whose dependencies are all completed, so independent tasks share a stage and dependents move later (`workflow.ts:239-267`).
- **Claim-aware parallel/serial decision.** Per stage, the planner resolves each task's claim set, computes pairwise overlap ratio (overlapping patterns over union size) and risk (file-size weights plus history and +3.0 compatibility penalties), then `decideStageStrategy` returns: `parallel` for single-task stages; `serial` on hard compatibility conflicts; `parallel` on zero effective overlap; `serial` ordered by connection count when any pair exceeds 0.3 overlap ratio or 2.0 risk; `parallel-with-contracts` otherwise (`planner.ts:100-103`, `planner.ts:183-261`, `planner.ts:372-484`, `planner.ts:504-530`). Oversized stages split into sub-batches capped at `maxParallel` (default 5) (`planner.ts:492-502`, `planner.ts:538-621`).
- **Parent/child branching.** Executed tasks record `parent: null`, empty `children`, copied `depends`, and a `workflow` record (name, path, stage, depends) (`commands/workflow.ts:236-266`). Task-level subtasks branch from the parent's branch rather than the base, merge from inside the parent worktree, and cascade-cancel with the parent (`task.ts:256-277`, `task.ts:574-586`, `task.ts:839-880`).

## 5. Multi-harness support (claude-code, aider, codex, open-code, script, raw executors) and implementation via the executor field

Full catalog in [[04-executors-and-workspaces|Executors, Workspace Providers, and Task Lifecycle]].

- **The `executor` field is a plain string on the task definition** (`executor?: string | null`, defaulting to `"script"` at spawn: `taskDef.executor || "script"`), and an unknown name fails fast naming the supported options (`executor.ts:26-34`, `executor.ts:330`, `executor.ts:353-359`). `taskCreate` fills it from `--executor` or config (`task.ts:216-219`).
- **Seven adapter entries** (`executor.ts:262-317`, `executor.ts:319-321`):
  - `claude-code`: `claude [-model M] [--effort E] -p <short-prompt> --dangerously-skip-permissions`; CLI capability probed once via `claude --help` and cached; defaults `sonnet`/`low` via `PITH_RUAH_CLAUDE_MODEL`/`PITH_RUAH_CLAUDE_EFFORT` (`executor.ts:185-260`, `executor.ts:266-269`).
  - `aider`: `aider --message <prompt> --yes-always --no-git` — ruah owns git (`executor.ts:270-273`).
  - `codex`: `codex <prompt>` (`executor.ts:274-277`).
  - `codex-mcp`: POSTs JSON-RPC `tools/call` to `CODEX_MCP_URL`, falling back to the `codex` CLI when unset (`executor.ts:144-178`, `executor.ts:278-294`).
  - `open-code`: `opencode -p <prompt>` (`executor.ts:295-298`).
  - `script` (default): quote-aware `parseCommandLine` split, spawned without a shell (`executor.ts:98-142`, `executor.ts:307-316`).
  - `raw`: `sh -c <prompt>` (POSIX) or `cmd /d /s /c` (Windows) (`executor.ts:299-306`).
- **Adding a harness means adding one adapter entry** keyed by name plus its spawn form — no other code changes. `getAvailableExecutors` returns the table keys (`executor.ts:319-321`).

## 6. Concrete features and ideas fleet can borrow (5-8 with file:line citations)

1. **Three-bucket claim locks with pre-start rejection.** Declare `owned`/`sharedAppend`/`readOnly` glob sets per task; reject overlapping claims (`claimSetsOverlap`) and out-of-scope subtasks (`claimSetWithinScope`) before spawning anything. Grounding: `packages/core/src/core/claims.ts:3-9` (ClaimSet shape), `:165-186` (precedence), `:188-231` (overlap/scope).
2. **Artifact capture with patch plus validation triple.** After each task, persist `changedFiles`, full `patch`, `baseRef`/`headRef`/`commitSha`, embedded claims, and `{executorSuccess, contractSuccess, gatesSuccess}` so merges and audits never re-derive diffs. Grounding: `packages/core/src/core/artifact.ts:5-21` (shape), `:38-63` (build), `:72-77` (presence check).
3. **Append-only shared contracts.** Let parallel tasks share files when they only append: pass missing-base and identical content, fail deletes/moves, require new bytes to extend original bytes without reducing line count. Grounding: `packages/core/src/core/contract-validator.ts:47-84` (append check), `:131-148` (shared branch).
4. **Atomic state writes with revision guards.** Single JSON state file, `O_EXCL` lock file with 50 ms poll / 5 s timeout, write-to-temp plus `renameSync`, and `revision` compare-and-swap that throws on stale writes. Grounding: `packages/core/src/core/state.ts:179-223` (lock), `:234-263` (save with temp+rename+revision).
5. **Claim-aware parallel/serial planning with numeric thresholds.** Overlap ratio > 0.3 or risk > 2.0 forces serial ordered by connection count; manageable overlap runs parallel-with-contracts; single-task and zero-overlap stages run parallel. Grounding: `packages/core/src/core/planner.ts:183-261` (risk/overlap), `:372-484` (strategy decision), `:492-502` (parallel cap split).
6. **`RUAH_*` env-var subagent context.** Inject `RUAH_TASK`, `RUAH_WORKTREE`, `RUAH_EXECUTOR` always plus conditional `RUAH_PARENT_TASK`/`RUAH_ROOT`/`RUAH_FILES`, mirror them into `.ruah-task.md`, and let subagents inherit parent scope via `RUAH_PARENT_TASK`. Grounding: `packages/core/src/core/executor.ts:362-431` (env + task file), `packages/core/src/commands/task.ts:222-225` (parent fallback).
7. **Zero-dependency git-worktree isolation.** One `WorkspaceProvider` kind (`worktree`): `git worktree add -b ruah/<safe> <path> <base>`, spawn with `cwd` set to the worktree, merge with `git merge --no-ff`, remove with `worktree remove --force` plus `branch -D`. Grounding: `packages/core/src/core/workspace.ts:21-69` (provider), `packages/core/src/core/git.ts:136-176` (create/remove), `:189-231` (merge with conflict parse).
8. **Restart-safe reconciliation limited to terminal tasks.** On restart, clean `merged`/`cancelled` unconditionally, auto-detect merges only for `done` tasks with both branches present, and never touch `created`/`in-progress`/`failed` (avoids the fresh-branch ancestor false positive). Grounding: `packages/core/src/core/reconcile.ts:17-70`.

**Covers:** task-spec questions 1-6, grounded in `wiki/01-claims-and-artifacts.md`, `wiki/02-state-and-restart-safety.md`, `wiki/03-planner-and-workflows.md`, `wiki/04-executors-and-workspaces.md` @ 58c4ee5b
