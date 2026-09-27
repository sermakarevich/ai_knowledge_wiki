> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# State, Persistence, and Restart Safety
**In one sentence:** Ruah keeps all orchestration state in a single versioned JSON file that is written atomically under a file lock with revision checks, migrated to the current shape on every load, and reconciled against git on restart.
## Key points
- State is a single JSON document at `<root>/.ruah/state.json` with schema `RuahState` holding `version`, `revision`, `baseBranch`, `tasks`, `artifacts`, `locks`, `lockModes`, `lockSnapshots`, and `history` (`state.ts:67-78`, `state.ts:120-122`).
- `loadState` returns defaults when the file is missing and otherwise parses plus migrates the file contents, so a fresh checkout and a restart use the same code path (`state.ts:225-232`, `state.ts:132-133`).
- Writes are serialized by an exclusive lock file at `<root>/.ruah/state.lock` created with `O_EXCL` (`wx`), polling every 50 ms with a 5 s timeout and treating locks older than 30 s as stale (`state.ts:93-96`, `state.ts:179-223`).
- Stale writes are rejected by a generation counter: `saveState` re-reads disk under the lock and throws if the in-memory `revision` differs from disk, then persists `revision + 1` (`state.ts:240-247`, `state.ts:251-259`).
- Persistence is crash-safe via write-to-temp plus atomic rename: the new state is written to `state.json.<rand>.tmp` and then `renameSync` replaces the old file (`state.ts:256-258`).
- Old state files are upgraded in place to `version: 2` on every load and save: missing `claims` are derived from `files`, missing `workspace` handles are derived from `worktree`/`branch`, and missing `files`, `integration`, and `artifacts` entries are backfilled (`state-migrations.ts:99-113`, `state-migrations.ts:36-97`, `state.ts:136-164`).
- Restart reconciliation only removes terminal or externally merged tasks: `merged` and `cancelled` tasks are cleaned unconditionally, `done` tasks are removed only if both branches still exist and the task branch is merged, and all other statuses are left untouched (`reconcile.ts:17-47`, `reconcile.ts:49-70`).
---
## Where state lives
State lives in `<root>/.ruah/state.json` (`state.ts:120-122`). The directory layout is created by `ensureStateDir`, which creates `.ruah/`, `.ruah/worktrees/`, and `.ruah/workflows/` (`state.ts:112-118`). The companion lock file path is `<root>/.ruah/state.lock` (`state.ts:124-126`).
The in-memory shape is `RuahState` (`state.ts:67-78`): a numeric `version` and `revision`, a `baseBranch` string, `tasks` and `artifacts` maps, `locks` plus `lockModes` plus `lockSnapshots` for file ownership, and a `history` list. Each `Task` (`state.ts:30-59`) records branch, worktree, files, lock mode, executor, prompt, parent/children, dependencies, timestamps, workflow reference, claims, artifact, integration status, and workspace handle.
History is bounded: `addHistoryEntry` appends timestamped entries and truncates to the last 200 (`state.ts:93-93`, `state.ts:265-278`).
## Process-safe atomic writes
Concurrent CLI processes are serialized by `acquireStateWriteLock` (`state.ts:179-223`). It creates the lock file with `openSync(lockFile, "wx")` so creation fails with `EEXIST` if another process holds it (`state.ts:186-186`). The holder writes its PID and acquisition time into the lock file (`state.ts:187-194`). Waiters poll every `STATE_LOCK_POLL_MS` (50 ms) until `STATE_LOCK_TIMEOUT_MS` (5 s) (`state.ts:94-96`, `state.ts:220-220`), then throw `"State is locked by another ruah process..."` (`state.ts:215-219`).
The write itself in `saveState` (`state.ts:234-263`) holds that lock for the whole read-modify-write cycle, writes the full JSON document with 2-space indentation plus trailing newline to a uniquely named temp file (`state.ts:256-257`), and atomically replaces the old file with `renameSync` (`state.ts:258-258`). The lock is always released in a `finally` block (`state.ts:260-262`).
## Stale-write rejection
Each persisted document carries a monotonically increasing `revision`, starting at 0 for new state (`state.ts:98-110`, `state.ts:169-169`). `saveState` re-reads the current on-disk revision while holding the lock (`state.ts:240-242`) and compares it to the caller's in-memory revision (`state.ts:243-247`). On mismatch it throws `"State changed on disk while this command was running..."` and writes nothing (`state.ts:243-247`). On match it writes `revision: current.revision + 1` and `version: 2`, and updates the in-memory object to the new revision (`state.ts:251-259`).
## State migration toward the engine model
Every load passes through `parseState`, which calls `migrateStateShape` and then backfills task fields (`state.ts:132-177`). `migrateStateShape` forces `version` to at least 2, defaults `artifacts` and `baseBranch`, and runs `migrateTaskLike` for every task (`state-migrations.ts:99-113`). `saveState` also calls `migrateStateShape` before writing and stamps `version: 2` (`state.ts:249-254`).
`migrateTaskLike` (`state-migrations.ts:36-97`) performs four upgrades: derive `claims` from `files` via `claimSetFromFiles` when absent (`state-migrations.ts:41-46`); synthesize a `workspace` handle of kind `worktree` from legacy `worktree`/`branch` fields (`state-migrations.ts:48-57`) or from the derived path `.ruah/worktrees/<sanitized-task-name>` when neither exists (`state-migrations.ts:59-75`, `state-migrations.ts:32-34`); copy the workspace root and branch name back onto `worktree` and `branch` (`state-migrations.ts:77-83`); and default `files` from claims and `integration` to `{ status: "unknown", conflictsWith: [] }` (`state-migrations.ts:85-94`).
`parseState` adds a second layer of backward compatibility (`state.ts:136-164`): default `depends` from `workflow.depends` (`state.ts:137-139`), default `lockMode` to `"write"` (`state.ts:140-142`), derive `claims` from `files` and `files` from `claims` when one side is missing (`state.ts:143-148`), sync `worktree`/`branch` from the workspace handle (`state.ts:149-155`), default `integration` to unknown (`state.ts:156-161`), and link `artifact` from the top-level artifacts map (`state.ts:162-164`).
## Reconcile on restart
`reconcileStateWithGit` (`reconcile.ts:10-77`) aligns in-memory state with git reality after restarts or external merges. Tasks with status `merged` are logged as `task.cleaned.merged`, their worktrees removed, and their state entries (including locks) deleted via `removeTask` (`reconcile.ts:18-29`, `state.ts:414-424`). Tasks with status `cancelled` follow the same path with event `task.cleaned.cancelled` (`reconcile.ts:31-39`).
Only `done` tasks are eligible for automatic merge detection; `created`, `in-progress`, and `failed` tasks are skipped explicitly to avoid the disappearing-tasks false positive where a fresh branch is trivially an ancestor of its base (`reconcile.ts:41-47`). For `done` tasks, reconciliation requires both `task.branch` and `task.baseBranch` to exist and `isBranchMerged` to return true before logging `task.reconciled.merged` and cleaning up (`reconcile.ts:49-70`). If any task was removed, the new state is persisted with `saveState`, which bumps the revision (`reconcile.ts:72-74`). The function returns the lists of merged and cleaned-cancelled task names (`reconcile.ts:5-8`, `reconcile.ts:76-76`).
## Config surface
Runtime defaults come from `loadConfig` (`config.ts:46-83`), which reads `.ruahrc` JSON at the repo root if present (`config.ts:50-59`), otherwise falls back to the `"ruah"` section of `package.json` (`config.ts:62-75`), otherwise returns an empty config (`config.ts:31-31`, `config.ts:82-82`). `.ruahrc` takes precedence and an invalid `.ruahrc` throws `Invalid .ruahrc: ...` while a broken `package.json` ruah section is silently ignored (`config.ts:55-58`, `config.ts:71-73`). The `PITH_RUAH_MAX_PARALLEL` environment variable overrides `maxParallel` when set to a positive integer (`config.ts:77-80`, `config.ts:33-39`).
`validateConfig` (`config.ts:85-114`) accepts only known keys: `baseBranch`, `executor`, `timeout`, `files`, `skipGates`, `parallel`, `maxParallel`, `strictLocks`, `workspaceBackend` (only `"worktree"`), `captureArtifacts`, `enableCompatibilityChecks`, and `enablePlannerV2` (`config.ts:4-29`, `config.ts:89-113`). Positive-number constraints apply to `timeout` and `maxParallel`, with `maxParallel` floored to an integer (`config.ts:93-101`).
## Excerpts
`state.ts:234-263`:
```
export function saveState(root: string, state: RuahState): void {
	const file = statePath(root);
	mkdirSync(dirname(file), { recursive: true });
	const releaseLock = acquireStateWriteLock(root);

	try {
		const current = existsSync(file)
			? parseState(readFileSync(file, "utf-8"), root)
			: defaultState();
		if (state.revision !== current.revision) {
			throw new Error(
				"State changed on disk while this command was running. Re-run the command.",
			);
		}

		migrateStateShape(state, root);

		const nextState: RuahState = {
			...state,
			version: 2,
			revision: current.revision + 1,
		};
		const tmp = `${file}.${randomBytes(4).toString("hex")}.tmp`;
		writeFileSync(tmp, `${JSON.stringify(nextState, null, 2)}\n`, "utf-8");
		renameSync(tmp, file);
		state.revision = nextState.revision;
	} finally {
		releaseLock();
	}
}
```
`reconcile.ts:41-59`:
```
		// Only auto-reconcile "done" tasks. Tasks in created/in-progress/failed
		// haven't completed their lifecycle — auto-removing them causes the
		// "disappearing tasks" bug (freshly created branches are trivially
		// ancestors of their base, so isBranchMerged returns a false positive).
		if (task.status !== "done") {
			continue;
		}

		if (
			!task.branch ||
			!branchExists(task.branch, root) ||
			!branchExists(task.baseBranch, root)
		) {
			continue;
		}

		if (!isBranchMerged(task.branch, task.baseBranch, root)) {
			continue;
		}
```
**Covers:** packages/core/src/core/{state,state-migrations,reconcile,config}.ts @ 58c4ee5b
