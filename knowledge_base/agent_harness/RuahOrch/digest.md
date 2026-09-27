> [[index|Wiki]] | [[summary|Summary]]

# Ruah-Orch — Digest

The whole source at medium depth: every component's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-claims-and-artifacts|Claims, Artifacts, and Contract Enforcement]]

**In one sentence:** Ruah isolates concurrent tasks with declared owned, shared-append, and read-only file globs, records what each task changed as a durable artifact, and validates those changes against the declared contract after execution.

- A `ClaimSet` declares three glob lists — `ownedPaths`, `sharedPaths`, and `readOnlyPaths` — with optional `ownedSymbols` and `sharedInterfaces`, normalized by backslash-to-slash conversion, trimming, trailing-slash removal, and deduplication (`claims.ts:3-9`, `claims.ts:45-59`, `claims.ts:69-80`).
- Path-to-claim matching checks buckets in fixed precedence — owned, then shared-append, then read-only — using `patternsOverlap` or `matchesPattern`, and returns the first matching bucket and pattern or null (`claims.ts:155-163`, `claims.ts:165-186`).
- Overlap detection compares every pattern pair across two claim sets with `patternsOverlap` and returns both overlapping patterns, while scope checking requires every child pattern to overlap at least one parent pattern unless the parent set is empty (`claims.ts:188-206`, `claims.ts:208-231`).
- A `TaskArtifact` stores `schemaVersion`, `taskName`, `workspaceId`, resolved `baseRef`, `headRef`, `commitSha`, `changedFiles`, full `patch`, `createdAt`, embedded `claims`, and a `validation` triple of `executorSuccess`, `contractSuccess`, and optional `gatesSuccess` (`artifact.ts:5-21`, `artifact.ts:38-63`).
- Contract validation lists changed files against the base ref, accepts files matching `ownedPaths`, rejects any change to a `readOnlyPaths` match as a `read-only` violation, and rejects any other changed file as `outside-contract` (`contract-validator.ts:104-131`, `contract-validator.ts:150-162`).
- Shared-path changes are accepted only if append-only: a missing base version passes, deletion or move fails, identical content passes, and modified content must start with the original bytes without reducing line count, otherwise a `shared-append` violation is recorded (`contract-validator.ts:47-84`, `contract-validator.ts:131-148`).
- `ClaimSource` with `owned`, `sharedAppend`, and `readOnly` keys and `FileContract` with `claims` or `owned`/`sharedAppend`/`readOnly` fields are both converted to the canonical `ClaimSet` before validation, and `artifactPresent` treats an artifact as non-empty only when `changedFiles` or `patch` is non-empty (`claims.ts:17-21`, `contract-validator.ts:86-102`, `artifact.ts:72-77`).

## 2. [[wiki/02-state-and-restart-safety|State, Persistence, and Restart Safety]]

**In one sentence:** Ruah keeps all orchestration state in a single versioned JSON file that is written atomically under a file lock with revision checks, migrated to the current shape on every load, and reconciled against git on restart.

- State is a single JSON document at `<root>/.ruah/state.json` with schema `RuahState` holding `version`, `revision`, `baseBranch`, `tasks`, `artifacts`, `locks`, `lockModes`, `lockSnapshots`, and `history` (`state.ts:67-78`, `state.ts:120-122`).
- `loadState` returns defaults when the file is missing and otherwise parses plus migrates the file contents, so a fresh checkout and a restart use the same code path (`state.ts:225-232`, `state.ts:132-133`).
- Writes are serialized by an exclusive lock file at `<root>/.ruah/state.lock` created with `O_EXCL` (`wx`), polling every 50 ms with a 5 s timeout and treating locks older than 30 s as stale (`state.ts:93-96`, `state.ts:179-223`).
- Stale writes are rejected by a generation counter: `saveState` re-reads disk under the lock and throws if the in-memory `revision` differs from disk, then persists `revision + 1` (`state.ts:240-247`, `state.ts:251-259`).
- Persistence is crash-safe via write-to-temp plus atomic rename: the new state is written to `state.json.<rand>.tmp` and then `renameSync` replaces the old file (`state.ts:256-258`).
- Old state files are upgraded in place to `version: 2` on every load and save: missing `claims` are derived from `files`, missing `workspace` handles are derived from `worktree`/`branch`, and missing `files`, `integration`, and `artifacts` entries are backfilled (`state-migrations.ts:99-113`, `state-migrations.ts:36-97`, `state.ts:136-164`).
- Restart reconciliation only removes terminal or externally merged tasks: `merged` and `cancelled` tasks are cleaned unconditionally, `done` tasks are removed only if both branches still exist and the task branch is merged, and all other statuses are left untouched (`reconcile.ts:17-47`, `reconcile.ts:49-70`).

## 3. [[wiki/03-planner-and-workflows|Planner, DAG Workflows, and Claim-Aware Scheduling]]

**In one sentence:** Ruah defines work as a Markdown task graph with dependency edges, validates it as a DAG, derives ready-set stages, and then refines each stage into parallel, parallel-with-contracts, or serial execution based on claim overlap, risk thresholds, and compatibility signals (workflow.ts:37-187, workflow.ts:194-267, planner.ts:372-484, commands/workflow.ts:136-148).

- Workflows are Markdown files with `# Workflow: <name>`, a `## Config` block (base, parallel, on_conflict), and one `### <task>` section per task carrying files, executor, depends, prompt, and on_conflict fields (workflow.ts:59-63, workflow.ts:86-101, workflow.ts:106-180, example-feature.md:1-31).
- Config defaults are base `main`, parallel `false`, and on-conflict `fail`, with only `fail`, `rebase`, and `retry` accepted as conflict strategies at config and task level (workflow.ts:42-46, workflow.ts:91-98, workflow.ts:160-164).
- DAG validation rejects unknown dependencies and detects cycles with depth-first search over the dependency edges, returning a valid flag plus an error list (workflow.ts:194-237).
- Stage computation groups tasks into ready sets by repeatedly selecting tasks whose dependencies are all completed, so independent tasks share a stage and dependents move to later stages (workflow.ts:239-267, example-feature.md:9-31).
- Overlap analysis compares task claim sets pairwise per stage, computing an overlap ratio over the union of claim patterns and a risk score from per-pattern file-size weights plus history and compatibility penalties (planner.ts:206-261, planner.ts:183-198, planner.ts:504-530).
- Stage strategy is selected by rule: single-task stages run parallel, hard compatibility conflicts force serial, zero effective overlap runs parallel, overlap above 0.3 ratio or 2.0 risk forces serial ordered by connection count, and manageable overlap runs parallel-with-contracts (planner.ts:100-103, planner.ts:372-484).
- Contracts assign owned, shared-append, and read-only access per task, either directly from explicit claim sets or by primary-task heuristic where the task referencing the most files owns a shared pattern and others get append-only access (planner.ts:268-365, planner.ts:628-670).
- Workflow execution runs stages in dependency order, applies the planner decision per stage, validates contracts and optional compatibility after execution, and merges each completed task branch before proceeding, with plan, run, explain, list, and create subcommands exposing this surface (commands/workflow.ts:54-78, commands/workflow.ts:183-199, commands/workflow.ts:294-302, commands/workflow.ts:417-505).

## 4. [[wiki/04-executors-and-workspaces|Executors, Workspace Providers, and Task Lifecycle]]

**In one sentence:** Ruah runs each task by creating an isolated git worktree on a `ruah/<name>` branch, spawning the harness named in the task's `executor` field inside that worktree with `RUAH_*` context variables, and moving the task through create/start/done/merge with merge targets that differ for root tasks and subtasks.

- The `executor` field is an optional string on the task definition defaulting to `"script"`, and an unknown name fails fast with an error naming the supported options (`executor.ts:26-34`, `executor.ts:330`, `executor.ts:353-359`).
- Seven adapter entries map executor names to spawn commands: `claude-code` runs `claude -p <short-prompt> --dangerously-skip-permissions` with optional `--model`/`--effort` flags, `aider` runs `aider --message <prompt> --yes-always --no-git`, `codex` runs `codex <prompt>`, `codex-mcp` posts to `CODEX_MCP_URL` over HTTP or falls back to the `codex` CLI, `open-code` runs `opencode -p <prompt>`, `script` splits the prompt as a command line, and `raw` runs the prompt through `sh -c` (or `cmd` on Windows) (`executor.ts:241-260`, `executor.ts:262-317`).
- The workspace layer has a single provider kind, `"worktree"`, whose `create` calls `createWorktree` to run `git worktree add -b ruah/<safe-name> <repo>/.ruah/worktrees/<safe-name> <base>` and returns a handle with root, baseRef, headRef, and branch metadata (`workspace.ts:21-39`, `workspace.ts:41-66`, `git.ts:140-159`).
- `ruah task create` resolves `--executor`, `--files`, `--prompt`, `--base`, `--parent`, and `--depends` flags (falling back to config file values), validates file locks and parent status, then creates the worktree and stores the workspace handle on the task record (`task.ts:202-237`, `task.ts:256-312`, `task.ts:315-344`).
- `ruah task start` requires status `created`, enforces the dependency gate unless `--force` is passed, flips the task to `in-progress`, and invokes `executeTask` in the task worktree unless `--no-exec` is given; `task done` requires `in-progress`, snapshots the diff stat and artifact, and flips the task to `done` (`task.ts:371-426`, `task.ts:428-483`, `task.ts:109-200`).
- `ruah task merge` requires status `done`, blocks when unmerged children exist, runs governance gates for root tasks but defers them for subtasks, merges subtask branches from inside the parent worktree and root-task branches after checking out the base in the repo root, then removes the worktree, deletes the branch, and drops the task record (`task.ts:485-514`, `task.ts:534-586`, `task.ts:588-613`, `git.ts:161-176`, `git.ts:189-231`).
- Every spawned executor receives `RUAH_TASK`, `RUAH_WORKTREE`, and `RUAH_EXECUTOR` unconditionally plus conditional `RUAH_PARENT_TASK`, `RUAH_ROOT`, and `RUAH_FILES`, and the same values are documented into the `.ruah-task.md` file written into the worktree before spawn so nested agents can call `ruah task create --parent $RUAH_TASK` (`executor.ts:362-402`, `executor.ts:412-431`).

## 5. [[wiki/targeted|Ruah File-Claim Orchestration: Answers to Fleet's Targeted Questions]]

**In one sentence:** Ruah coordinates parallel coding agents through declared file-claim locks, durable artifacts, DAG workflows with claim-aware scheduling, and harness-agnostic executors — all with zero runtime dependencies.

- Claims are three glob buckets (owned exclusive-write, shared append-only, read-only) with fixed match precedence owned > shared-append > read-only, enforced both before start (overlap/scope rejection) and after execution (contract validation).
- State is a single versioned JSON file with atomic temp-write plus rename, an `O_EXCL` lock file, revision-based stale-write rejection, in-place migration to version 2, and git reconciliation that only auto-cleans terminal or merged tasks.
- Workflows are Markdown task graphs validated as DAGs, staged by ready-set expansion, and scheduled per stage as parallel, parallel-with-contracts, or serial based on claim-overlap ratio (>0.3) and risk score (>2.0).
- Seven executors (claude-code, aider, codex, open-code, script, raw) are selected by the task's `executor` string field and spawned in an isolated git worktree with `RUAH_*` environment variables.
- Fleet can borrow at least seven concrete ideas: claim locks with pre-start rejection, artifact capture with patch plus validation triple, append-only shared contracts, atomic state writes with revision guards, claim-aware parallel/serial planning, `RUAH_*` env-var subagent context, and zero-dependency git-worktree isolation.

## The system in five moves

1. Each task declares which files it owns, shares append-only, or only reads — the claim is its contract.
2. The planner stages Markdown-defined tasks by dependencies, then picks parallel, parallel-with-contracts, or serial per stage from claim overlap and risk.
3. Every task runs isolated in its own git worktree, with the chosen harness spawned inside and `RUAH_*` variables telling the agent its boundaries.
4. After execution the diff is validated against the contract (read-only and out-of-scope edits rejected, shared files must be append-only) and stored as a durable artifact.
5. Branches merge in dependency order with governance gates, while the single JSON state file stays crash-safe through locks, atomic renames, and revision guards.
