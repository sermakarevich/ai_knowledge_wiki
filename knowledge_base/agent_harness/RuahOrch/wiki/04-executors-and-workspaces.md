> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Executors, Workspace Providers, and Task Lifecycle
**In one sentence:** Ruah runs each task by creating an isolated git worktree on a `ruah/<name>` branch, spawning the harness named in the task's `executor` field inside that worktree with `RUAH_*` context variables, and moving the task through create/start/done/merge with merge targets that differ for root tasks and subtasks.
## Key points
- The `executor` field is an optional string on the task definition defaulting to `"script"`, and an unknown name fails fast with an error naming the supported options (`executor.ts:26-34`, `executor.ts:330`, `executor.ts:353-359`).
- Seven adapter entries map executor names to spawn commands: `claude-code` runs `claude -p <short-prompt> --dangerously-skip-permissions` with optional `--model`/`--effort` flags, `aider` runs `aider --message <prompt> --yes-always --no-git`, `codex` runs `codex <prompt>`, `codex-mcp` posts to `CODEX_MCP_URL` over HTTP or falls back to the `codex` CLI, `open-code` runs `opencode -p <prompt>`, `script` splits the prompt as a command line, and `raw` runs the prompt through `sh -c` (or `cmd` on Windows) (`executor.ts:241-260`, `executor.ts:262-317`).
- The workspace layer has a single provider kind, `"worktree"`, whose `create` calls `createWorktree` to run `git worktree add -b ruah/<safe-name> <repo>/.ruah/worktrees/<safe-name> <base>` and returns a handle with root, baseRef, headRef, and branch metadata (`workspace.ts:21-39`, `workspace.ts:41-66`, `git.ts:140-159`).
- `ruah task create` resolves `--executor`, `--files`, `--prompt`, `--base`, `--parent`, and `--depends` flags (falling back to config file values), validates file locks and parent status, then creates the worktree and stores the workspace handle on the task record (`task.ts:202-237`, `task.ts:256-312`, `task.ts:315-344`).
- `ruah task start` requires status `created`, enforces the dependency gate unless `--force` is passed, flips the task to `in-progress`, and invokes `executeTask` in the task worktree unless `--no-exec` is given; `task done` requires `in-progress`, snapshots the diff stat and artifact, and flips the task to `done` (`task.ts:371-426`, `task.ts:428-483`, `task.ts:109-200`).
- `ruah task merge` requires status `done`, blocks when unmerged children exist, runs governance gates for root tasks but defers them for subtasks, merges subtask branches from inside the parent worktree and root-task branches after checking out the base in the repo root, then removes the worktree, deletes the branch, and drops the task record (`task.ts:485-514`, `task.ts:534-586`, `task.ts:588-613`, `git.ts:161-176`, `git.ts:189-231`).
- Every spawned executor receives `RUAH_TASK`, `RUAH_WORKTREE`, and `RUAH_EXECUTOR` unconditionally plus conditional `RUAH_PARENT_TASK`, `RUAH_ROOT`, and `RUAH_FILES`, and the same values are documented into the `.ruah-task.md` file written into the worktree before spawn so nested agents can call `ruah task create --parent $RUAH_TASK` (`executor.ts:362-402`, `executor.ts:412-431`).
---
## Executor field and supported harnesses
The task definition carries `executor?: string | null` alongside `prompt`, `parent`, `files`, `repoRoot`, and `contract` (`executor.ts:26-34`). `taskCreate` fills it from `--executor` or the `executor` key in config, defaulting to null when neither is set (`task.ts:216-219`). At spawn time `executeTask` resolves `taskDef.executor || "script"`, so tasks without an explicit executor are executed as a shell command line (`executor.ts:330`). When no adapter matches, it returns `{ success: false, error: "Unknown executor: ..." }` without spawning anything (`executor.ts:353-359`). `getAvailableExecutors` returns the adapter table keys (`executor.ts:319-321`).
### claude-code
Builds its argument list in `buildClaudeCodeArgs`, probing the installed CLI once via `claude --help` and caching the result, adding `--model <model>` and `--effort <level>` only when the CLI advertises them (`executor.ts:213-230`, `executor.ts:241-260`). Model and effort defaults are `sonnet` and `low`, overridable through `PITH_RUAH_CLAUDE_MODEL` and `PITH_RUAH_CLAUDE_EFFORT` (`executor.ts:185-202`). The actual prompt sent on the CLI is a short pointer telling the agent to read `.ruah-task.md` in the current directory, stay within file scope, and commit with `git add -A && git commit -m "ruah(<name>): completed task"` (`executor.ts:232-239`). Spawn form is `claude [--model M] [--effort E] -p <short-prompt> --dangerously-skip-permissions` (`executor.ts:266-269`).
### aider
Spawns `aider --message <prompt> --yes-always --no-git`, passing the full task prompt as the message and disabling aider's own git handling because ruah owns branching and committing (`executor.ts:270-273`).
### codex and codex-mcp
The `codex` adapter spawns `codex <prompt>` with the full prompt as a single argument (`executor.ts:274-277`). The `codex-mcp` adapter checks `CODEX_MCP_URL`: when set it spawns `node --input-type=module -e <generated-script>` where the generated script POSTs a JSON-RPC `tools/call` for tool `execute` with `{ prompt, workdir: process.cwd() }` to that URL, and when unset it falls back to the plain `codex` CLI form (`executor.ts:144-178`, `executor.ts:278-294`).
### open-code
Spawns `opencode -p <prompt>` with the full task prompt (`executor.ts:295-298`).
### script (default)
Parses the prompt with a quote- and backslash-aware `parseCommandLine` splitter, requires a non-empty result, and spawns `parts[0]` with `parts[1..]` as arguments without a shell (`executor.ts:98-142`, `executor.ts:307-316`). This is the fallback when the task has no executor configured (`executor.ts:330`).
### raw
Spawns `sh -c <prompt>` on POSIX and `cmd /d /s /c <prompt>` on Windows with `shell: false` (`executor.ts:299-306`).
## Workspace providers
The `WorkspaceProvider` interface exposes one kind, `"worktree"`, with `create`, `remove`, `currentHead`, `changedFiles`, `patch`, `diffStat`, and `merge` operations (`workspace.ts:21-39`). The default provider is created by `createWorktreeProvider` and can be swapped via `setWorkspaceProvider` / read via `getWorkspaceProvider` (`workspace.ts:41-42`, `workspace.ts:104-112`).
### Worktree isolation
`create` delegates to `createWorktree(taskName, baseRef, repoRoot)`, which sanitizes the task name (`[^a-zA-Z0-9._-]` becomes `_`), derives branch `ruah/<safe>` and path `<repo>/.ruah/worktrees/<safe>`, throws if the branch already exists, and runs `git worktree add -b <branch> <path> <base>` (`git.ts:136-159`, `workspace.ts:44-66`). `remove` runs `git worktree remove <path> --force` and `git branch -D <branch>`, both with errors ignored (`git.ts:161-176`, `workspace.ts:67-69`). The handle records `id` (task name), `root` (worktree path), `baseRef`, `headRef` (commit at creation), and `metadata.branchName` (`workspace.ts:55-65`). Readouts delegate to git helpers: `currentHead` reads `rev-parse HEAD` in the worktree, `changedFiles` unions `diff --name-only <base>` with `status --porcelain` entries, `patch` concatenates per-file unified-zero diffs, and `diffStat` runs `git diff <base>...<branch> --stat` (`workspace.ts:70-89`, `git.ts:233-248`, `git.ts:313-348`).
## Task lifecycle: create, start, done, merge
### create
`ruah task create <name>` parses `--files` (comma-split) defaulting to `config.files`, `--base` defaulting to `config.baseBranch`, `--executor` defaulting to `config.executor`, `--prompt`, `--parent` (defaulting to `$RUAH_PARENT_TASK` so subagents inherit the parent), and `--depends` (comma-split), plus `--read-only` / `--strict-locks` for lock mode (`task.ts:210-237`). It rejects unknown dependency names and duplicate task names (`task.ts:241-254`). For subtasks it requires the parent to exist and be `created` or `in-progress`, and branches from the parent's branch rather than the base branch (`task.ts:256-277`). File locks are acquired with subtask scope validated against the parent (`task.ts:279-305`). It then calls `provider.create(name, base, root)`, derives claims from the file list, stores the workspace handle plus legacy `branch`/`worktree` fields, links the child onto the parent record, and appends a `task.created` history entry (`task.ts:307-356`).
### start
`ruah task start <name>` only accepts tasks in `created` status, checks `isTaskClaimable` against `depends` unless `--force` is passed, flips the task to `in-progress` with a `startedAt` timestamp, and delegates to `executeTaskLifecycle`, which calls `executeTask(task, workspace.root, { debug, dryRun })` when a prompt is set and `--no-exec` is absent (`task.ts:371-426`, `task.ts:109-132`). On success the helper marks the task `done`, refreshes `workspace.headRef`, builds and stores the artifact, optionally runs compatibility checks, and appends `task.done`; on failure it marks the task `failed`, appends `task.failed`, and prints retry/takeover hints (`task.ts:139-195`). With `--dry-run` it prints the rendered command instead of spawning (`task.ts:134-137`). Tasks without a prompt are left ready for manual work with the worktree path printed (`task.ts:196-199`).
### done
`ruah task done <name>` only accepts `in-progress` tasks, prints the provider `diffStat` against the base branch, marks the task `done`, refreshes `headRef`, captures the artifact when `captureArtifacts` is not false, syncs legacy fields, and appends `task.done` (`task.ts:428-483`).
### merge
`ruah task merge <name>` only accepts `done` tasks and refuses to merge while `getUnmergedChildren` is non-empty (`task.ts:498-514`). `--dry-run` prints the diff stat that would merge into the parent branch for subtasks or the base branch otherwise (`task.ts:525-532`). Governance gates from `integrations.ts` run only for root tasks: `detectGovernance` looks for `.claude/governance.md` or `governance.md`, `runGates` executes each gate command with `execSync` in the worktree (or gate subdirectory), failing the merge on the first `MANDATORY` failure while letting `OPTIONAL`/`ADVISORY` failures continue (`task.ts:534-572`, `integrations.ts:39-49`, `integrations.ts:126-161`). Subtask merges log that gates are deferred to the parent merge (`task.ts:568-569`). The merge itself passes `parentWorkspace.root` for subtasks so `mergeBranchIntoTarget` runs `git merge <branch> --no-ff` inside the parent worktree (already on the target branch) instead of checking out the base in the repo root; on conflict it parses `status --porcelain` for `UU/AA/DD/AU/UA/DU/UD` entries, aborts, and returns the file list (`task.ts:574-586`, `git.ts:189-231`). On success the provider worktree is removed, the task record is deleted via `removeTask`, and a `task.merged` history entry records target and parent (`task.ts:588-598`). `cancel` cascades: it removes each child worktree, releases child locks, marks children `cancelled`, then removes the task worktree and releases its locks (`task.ts:839-880`).
## RUAH_* environment variables injected into subagents
The spawn environment starts as a copy of `process.env` and adds the following keys before `spawn(cmd, args, { cwd: worktreePath, env: taskEnv })` (`executor.ts:412-445`). The same values are written into the `.ruah-task.md` guide section so agents that only read files still learn them (`executor.ts:374-402`).
- `RUAH_TASK`: task name; always set; identifies the running task (`executor.ts:415`).
- `RUAH_WORKTREE`: absolute path of the task worktree, which is also the child process working directory (`executor.ts:416`, `executor.ts:440-445`).
- `RUAH_EXECUTOR`: resolved executor name after defaulting (e.g. `script` when unset) (`executor.ts:417`, `executor.ts:330`).
- `RUAH_PARENT_TASK`: parent task name; set only when `taskDef.parent` is present (`executor.ts:422-424`).
- `RUAH_ROOT`: repository root; set only when `taskDef.repoRoot` is present (`executor.ts:425-427`).
- `RUAH_FILES`: comma-joined file-lock scope; set only when `taskDef.files` is non-empty (`executor.ts:428-431`).
- `RUAH_DEBUG`: read (not written) by `isExecutionDebugEnabled` together with the `debug` option; values `1`/`true`/`yes` enable spawn logging and prefixed stdout/stderr capture (`executor.ts:53-57`, `executor.ts:433-460`).
- `RUAH_PARENT_TASK` (read direction): `taskCreate` falls back to `process.env.RUAH_PARENT_TASK` when `--parent` is omitted, so a subagent spawned inside a parent worktree automatically scopes `ruah task create` to that parent (`task.ts:222-225`).
## Subagent spawning mechanism
Spawning is `node:child_process.spawn` with `cwd` set to the worktree path, `stdio` inherited by default or piped when `silent` or debug capture is on, and `shell` true only on Windows unless the adapter overrides it (`executor.ts:438-445`). Before spawning, `executeTask` writes `.ruah-task.md` into the worktree containing the full prompt, parent line, locked-files line, rendered file-modification contract, and a subtask guide with copy-paste `ruah task create --parent <name> --files ... --executor <cli> --prompt ...` / `start` / `done` / `merge` commands plus the `RUAH_*` listing (`executor.ts:362-402`). The Claude prompt additionally orders the agent to commit before exiting, and both the spawn-error and process-close paths call `autoCommitChanges`, which stages with `git add -A` and commits as `ruah: auto-commit changes from task <name>` when anything is staged, reporting `autoCommitted` on the result (`executor.ts:232-239`, `executor.ts:481-531`, `git.ts:297-311`). Governance gate execution (`integrations.ts:126-161`) is separate from executor spawning and only runs at merge time as described above.
## Verbatim excerpts
`executor.ts:412-431` — task environment construction:
```ts
	return new Promise((resolve) => {
		const taskEnv: Record<string, string> = {
			...process.env,
			RUAH_TASK: taskDef.name,
			RUAH_WORKTREE: worktreePath,
			RUAH_EXECUTOR: executorName,
		} as Record<string, string>;

		// Subagent context: pass parent info + repo root so spawned CLIs
		// can call `ruah task create --parent $RUAH_TASK` from within execution
		if (taskDef.parent) {
			taskEnv.RUAH_PARENT_TASK = taskDef.parent;
		}
		if (taskDef.repoRoot) {
			taskEnv.RUAH_ROOT = taskDef.repoRoot;
		}
		// Pass file lock scope so agents know their boundaries
		if (taskDef.files && taskDef.files.length > 0) {
			taskEnv.RUAH_FILES = taskDef.files.join(",");
		}
```
`git.ts:140-159` — worktree creation:
```ts
export function createWorktree(
	taskName: string,
	baseBranch: string,
	repoRoot: string,
): WorktreeInfo {
	const safe = sanitizeName(taskName);
	const branchName = `ruah/${safe}`;
	const worktreePath = join(repoRoot, ".ruah", "worktrees", safe);

	if (branchExists(branchName, repoRoot)) {
		throw new Error(`Branch ${branchName} already exists`);
	}

	git(`worktree add -b ${branchName} "${worktreePath}" ${baseBranch}`, {
		cwd: repoRoot,
		silent: true,
	});

	return { worktreePath, branchName };
}
```
**Covers:** packages/core/src/core/{executor,workspace,git,integrations}.ts, commands/task.ts @ 58c4ee5b
