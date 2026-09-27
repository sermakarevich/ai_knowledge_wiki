# Technical Analysis: ruah-orch

**Repository:** https://github.com/ruah-dev/ruah-orch
**Version analyzed:** 1.1.2 (installer) / 1.1.1 (@ruah-dev/orch-core), commit 58c4ee5b9cd7318ada9110c620aa6607d070bd7c (2026-04-14)
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves

Running several AI coding agents in one repository at the same time creates one dominant failure: two agents edit the same files, and the merge becomes manual repair work. Existing harnesses (Claude Code, Aider, Codex, OpenCode) each assume they own the working tree.

Ruah-orch addresses this by making file ownership explicit and enforced. Every task declares a claim — which file globs it owns exclusively, which it may only append to, which it may only read. The orchestrator rejects conflicting claims before any agent starts, isolates each task in its own git worktree on a `ruah/<name>` branch, spawns the agent with that claim as its contract, validates the resulting diff against the contract after execution, and merges task branches in dependency order. The primary user is a developer (or a fleet supervisor) running parallel AI coding agents against a single repo. There are no runtime dependencies: the core package ships zero `dependencies`, using only Node.js built-ins for git, filesystem, and process management.

---

## 2. High-Level Architecture

```
                     +-------------------+
                     |  CLI  (cli.ts)    |
                     | task.* workflow.* |
                     | init setup doctor |
                     +--------+----------+
                              |
              +---------------+----------------+
              |               |                |
     +--------v------+ +------v-------+ +------v------+
     | Planner       | | Executor     | | Workspace   |
     | (planner.ts)  | | (executor.ts)| | (workspace, |
     | overlap/risk, | | 7 adapters,  | |  git.ts)    |
     | stage strategy| | spawn+env    | | worktrees   |
     +-------+-------+ +------+-------+ +------+------+
             |                |                 |
             +-------+--------+--------+--------+
                     |                 |
              +------v------+   +------v-------+
              | Claims +    |   | State        |
              | Contracts   |   | (state.ts,   |
              | (claims,    |   |  migrations, |
              |  contract-  |   |  reconcile)  |
              |  validator, |   | state.json + |
              |  artifact)  |   | state.lock   |
              +-------------+   +--------------+
```

Data flow from task creation to merged code:

1. `ruah task create <name> --files ... --executor ...` validates locks and parent scope, creates a git worktree on branch `ruah/<name>`, and persists the task plus its claim set in `.ruah/state.json` (atomic write under `state.lock`).
2. `ruah task start <name>` (or `workflow run` per stage) resolves the claim set, writes `.ruah-task.md` with the prompt plus the modification contract, and spawns the harness named by `executor` with `cwd` set to the worktree and `RUAH_*` context variables.
3. On completion the agent's changes are auto-committed; the orchestrator captures a `TaskArtifact` (`changedFiles`, full `patch`, base/head SHAs, validation triple).
4. `validateContractChanges` rejects read-only edits, non-append shared edits, and out-of-contract files.
5. `ruah task merge <name>` (or the workflow stage merge) runs governance gates for root tasks, merges the branch with `git merge --no-ff` in dependency/stage order, removes the worktree, and deletes the task record.

Persistent state lives in `<repo>/.ruah/state.json` (single versioned JSON document with a `revision` counter), guarded by `<repo>/.ruah/state.lock`. Worktrees live under `<repo>/.ruah/worktrees/`. Workflow definitions live under `<repo>/.ruah/workflows/`.

---

## 3. The File Claim

The representation is `ClaimSet` (`packages/core/src/core/claims.ts:3-9`): three glob lists — `ownedPaths` (exclusive write), `sharedPaths` (append-only write), `readOnlyPaths` (read-only) — plus optional `ownedSymbols` and `sharedInterfaces`. Construction normalizes every pattern (backslash-to-slash, trim, strip trailing slash, dedupe) via `normalizePathPattern` and `unique` (`claims.ts:45-80`).

Named kinds:

- `ClaimMatchResult` (`claims.ts:13-16`) — `{ bucket: "owned" | "shared-append" | "read-only" | null, pattern: string | null }`, returned by `findClaimMatch`, which checks owned, then shared, then read-only (`claims.ts:165-186`).
- `CompatibilitySignal` (`claims.ts:33-43`) — `{ clean, staleBase?, needsReplay?, conflictingFiles?, comparedAgainst?, checkedAt? }`: the data record that compatibility computation produces.
- `ClaimSource` (`claims.ts:17-21`) — `{ owned?, sharedAppend?, readOnly? }` input shape, converted to canonical `ClaimSet` before validation (`contract-validator.ts:86-102`).
- `TaskArtifact` (`packages/core/src/core/artifact.ts:5-21`) — `{ schemaVersion, taskName, workspaceId, baseRef, headRef, commitSha, changedFiles, patch, createdAt, claims, validation: { executorSuccess, contractSuccess, gatesSuccess? } }`.

Key traversal — precedence matching (`claims.ts:165-186`):

```ts
export function findClaimMatch(
	claims: ClaimSet,
	path: string,
	repoRoot?: string,
): ClaimMatchResult {
	for (const pattern of claims.ownedPaths) {
		if (claimMatchesPattern(pattern, path, repoRoot)) {
			return { bucket: "owned", pattern };
		}
	}
	for (const pattern of claims.sharedPaths) {
		if (claimMatchesPattern(pattern, path, repoRoot)) {
			return { bucket: "shared-append", pattern };
		}
	}
	for (const pattern of claims.readOnlyPaths) {
		if (claimMatchesPattern(pattern, path, repoRoot)) {
			return { bucket: "read-only", pattern };
		}
	}
	return { bucket: null, pattern: null };
}
```

Knobs: `strictLocks` flag on run paths, `lockMode` (`read` maps a file list to read-only, `write` to owned — `claims.ts:82-99`), and config keys `captureArtifacts` / `enableCompatibilityChecks` (`config.ts:4-29`).

---

## 4. LLM / External Service Integration

The repo does NOT call any LLM or external API itself. It is a pure orchestrator: the LLMs are the spawned harness CLIs (Claude Code, Aider, Codex, OpenCode), invoked as child processes. This is a deliberate design statement — zero runtime dependencies, no API keys in the orchestrator, no framework (no LangChain/LangGraph/FastMCP, only `node:child_process`).

The one network exception is the `codex-mcp` adapter, which POSTs a JSON-RPC `tools/call` to a `CODEX_MCP_URL` when that env var is set, falling back to the plain `codex` CLI otherwise (`executor.ts:144-178`, `executor.ts:278-294`). Configuration of harness behavior flows through env vars (`PITH_RUAH_CLAUDE_MODEL`, `PITH_RUAH_CLAUDE_EFFORT`, `CODEX_MCP_URL`, `RUAH_DEBUG`) rather than API clients.

---

## 5. The Task-and-Workflow Pipeline

**Task lifecycle** (`packages/core/src/commands/task.ts`):

1. `taskCreate` (`task.ts:202-356`) parses `--files/--base/--executor/--prompt/--parent/--depends` (falling back to config and to `$RUAH_PARENT_TASK` for parent), rejects unknown/duplicate names, requires subtask parents to be `created`/`in-progress` and to branch from the parent branch, acquires file locks with parent-scope validation, creates the worktree via the provider, derives claims, and persists the record.
2. `taskStart` (`task.ts:371-426`) requires `created`, enforces the dependency gate (`isTaskClaimable`) unless `--force`, flips to `in-progress`, and calls `executeTask` in the worktree unless `--no-exec`.
3. `executeTaskLifecycle` (`task.ts:109-200`) marks `done` with artifact capture and optional compatibility on success, or `failed` with retry/takeover hints on failure.
4. `taskDone` (`task.ts:428-483`) requires `in-progress`, prints diff stat, captures the artifact, marks `done`.
5. `taskMerge` (`task.ts:485-613`) requires `done`, blocks on unmerged children, runs governance gates for root tasks only (subtask gates defer to the parent merge), merges via `mergeBranchIntoTarget` (subtask merges run inside the parent worktree; root merges check out the base in the repo root), then removes the worktree, deletes the branch, and drops the record.

**Workflow pipeline** (`packages/core/src/commands/workflow.ts`, `packages/core/src/core/workflow.ts`, `packages/core/src/core/planner.ts`):

1. Parse the Markdown task graph; validate the DAG (unknown deps, DFS cycle detection — `workflow.ts:194-237`).
2. `getExecutionPlan` expands ready sets by fixed-point iteration (`workflow.ts:239-267`).
3. Per stage, `decideStageStrategy` returns `parallel`, `serial` (ordered by connection count), or `parallel-with-contracts` from overlap ratio and risk (`planner.ts:372-484`).
4. Execute each stage (parallel via `Promise.all`, serial sequentially), injecting the planner contract, validating contracts, running optional compatibility checks, then governance gates, then merging branches in stage order (`commands/workflow.ts:201-509`).

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `packages/core/src/commands/task.ts` | 880 | Task lifecycle: create/start/done/merge/cancel, lock acquisition, subtask scoping |
| `packages/core/src/commands/workflow.ts` | 764 | Workflow run/plan/explain/list/create; stage execution, compatibility, merge |
| `packages/core/src/core/planner.ts` | 670 | Overlap/risk analysis, stage strategy decision, contract text rendering |
| `packages/core/src/core/state.ts` | 579 | State shape, atomic locked writes, revision guards, lock registry |
| `packages/core/src/core/executor.ts` | 533 | Seven harness adapters, spawn, RUAH_* env, .ruah-task.md, auto-commit |
| `packages/core/src/core/git.ts` | 470 | Worktree/branch ops, merge with conflict parse, diff/patch/stat helpers |
| `packages/core/src/core/workflow.ts` | 277 | Markdown workflow parse, DAG validation, ready-set stage expansion |
| `packages/core/src/core/claims.ts` | 231 | ClaimSet shape, normalization, precedence matching, overlap/scope |
| `packages/core/src/core/contract-validator.ts` | 172 | Post-execution contract validation incl. append-only shared check |
| `packages/core/src/core/integrations.ts` | 162 | Governance gate detection and execution at merge time |
| `packages/core/src/core/workspace.ts` | 112 | WorkspaceProvider interface (single `worktree` kind), handle lifecycle |
| `packages/core/src/core/state-migrations.ts` | 113 | Version-2 migration: claims from files, workspace handles, backfills |
| `packages/core/src/core/config.ts` | 114 | `.ruahrc` / package.json config load, validation, PITH_RUAH_MAX_PARALLEL |
| `packages/core/src/core/artifact.ts` | 77 | TaskArtifact shape, build from provider diffs, presence check |
| `packages/core/src/core/reconcile.ts` | 77 | Restart reconciliation against git (terminal/merged tasks only) |
| `packages/core/src/cli.ts` | — | CLI entry dispatch (task/workflow/init/setup/doctor/status/config/clean/demo) |

Line counts from `wc -l` at 58c4ee5b. Ranges like `planner.ts:372-484` cite the strategy decision function.

---

## 7. Dependencies

`packages/core/package.json` (v1.1.1) declares **no `dependencies` key at all** — zero runtime dependencies. All git/filesystem/process work uses Node.js built-ins.

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| typescript | `^6.0.2` (dev) | Build only (`tsc`, `tsc --noEmit` typecheck) |
| @types/node | `^25.5.2` (dev) | Types for node built-ins |
| @biomejs/biome | `^2.4.10` (dev) | Lint/format |
| @ruah-dev/cli + @ruah-dev/orch-core | `file:../ruah-cli`, `file:./packages/core` (installer only) | Local file links, not registry deps |
| node | `>=18.0.0` (engines) | Minimum runtime |

No security-sensitive pins are documented; there is nothing to pin. The `codex-mcp` adapter uses the global `fetch` (Node 18+) rather than an HTTP client library.

---

## 8. CLI / Usage Surface

Entry points — `packages/core/src/cli.ts` dispatches `task`, `workflow`, `init`, `setup`, `status`, `config`, `clean`, `demo`, `doctor`; built output is `dist/cli.js` (`packages/core/package.json` scripts: `build: tsc && chmod +x dist/cli.js`, `start: node dist/cli.js`).

Commands:

```
ruah task create <name> --files a,b --base main --executor claude-code --prompt "..." [--parent P] [--depends d1,d2] [--read-only] [--strict-locks]
ruah task start <name> [--force] [--no-exec] [--dry-run] [--debug-exec]
ruah task done <name>
ruah task merge <name> [--dry-run]
ruah task cancel <name>
ruah workflow run <file.md> [--dry-run] [--debug-exec] [--json] [--strict-locks]
ruah workflow plan <file.md> [--json]
ruah workflow explain <name|file.md>
ruah workflow list [--json]
ruah workflow create <name> [--force]
ruah init | ruah setup | ruah doctor | ruah status | ruah config | ruah clean | ruah demo
```

Environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `RUAH_TASK` | (set at spawn) | Running task name |
| `RUAH_WORKTREE` | (set at spawn) | Task worktree path (also child cwd) |
| `RUAH_EXECUTOR` | (set at spawn) | Resolved executor name |
| `RUAH_PARENT_TASK` | unset | Parent task; also read by `task create` as `--parent` fallback |
| `RUAH_ROOT` | unset | Repo root, when known |
| `RUAH_FILES` | unset | Comma-joined file-lock scope |
| `RUAH_DEBUG` | unset | `1/true/yes` enables spawn logging |
| `PITH_RUAH_CLAUDE_MODEL` | `sonnet` | Model flag for claude-code adapter |
| `PITH_RUAH_CLAUDE_EFFORT` | `low` | Effort flag for claude-code adapter |
| `PITH_RUAH_MAX_PARALLEL` | config/5 | Overrides `maxParallel` |
| `CODEX_MCP_URL` | unset | Selects HTTP mode of codex-mcp adapter |

Configuration files:

| Path | Purpose |
|------|---------|
| `.ruahrc` (repo root, JSON) | Primary config; takes precedence; invalid JSON throws |
| `package.json` `"ruah"` section | Fallback config; broken section silently ignored |
| `.ruah/state.json` | Persisted orchestration state (version, revision, tasks, artifacts, locks) |
| `.ruah/workflows/*.md` | Workflow definitions |
| `.ruah-task.md` (per worktree) | Spawned-agent guide: prompt, locks, contract, subtask commands, RUAH_* listing |

---

## 9. Extensibility Points

- **New harness:** add one entry to the adapter table in `packages/core/src/core/executor.ts:262-317` keyed by executor name with its command-line build and spawn form; `getAvailableExecutors` (`executor.ts:319-321`) picks it up automatically. No other file changes.
- **New workspace backend:** implement the `WorkspaceProvider` interface (`packages/core/src/core/workspace.ts:21-39`: `create/remove/currentHead/changedFiles/patch/diffStat/merge`) and register via `setWorkspaceProvider` (`workspace.ts:104-112`). Only `"worktree"` exists today; `config.ts` validation accepts only `"worktree"`.
- **New workflow conflict strategy:** extend the `fail/rebase/retry` acceptance in `packages/core/src/core/workflow.ts:91-98,160-164` plus the merge/execution branches in `packages/core/src/commands/workflow.ts` that act on it.
- **New governance gate kind:** extend `detectGovernance`/`runGates` in `packages/core/src/core/integrations.ts:39-161` (currently file-presence detection of `governance.md` plus `execSync` gate commands with MANDATORY/OPTIONAL/ADVISORY severity).
- **New claim bucket or match semantic:** extend `ClaimSet` (`claims.ts:3-9`), `findClaimMatch` precedence (`claims.ts:165-186`), and the `validateContractChanges` branch order (`contract-validator.ts:104-163`) together — all three must agree.
- **New state field:** add to `RuahState`/`Task` (`state.ts:30-78`) plus a backfill in `migrateTaskLike` (`state-migrations.ts:36-97`) and `parseState` (`state.ts:136-164`) so old state files upgrade cleanly.

---

## 10. Limitations and Gotchas

- **Glob semantics are hand-rolled, not minimatch.** Overlap and matching use custom `patternsOverlap`/`matchesPattern` helpers; edge cases in advanced glob syntax (brace expansion, negation) may not behave like shell globs. Verify before relying on exotic patterns.
- **Single-file state is a contention point.** The `O_EXCL` lock plus 5 s timeout serializes all writers; a fleet running dozens of concurrent tasks against one repo will queue on `state.json`. The stale-lock path (30 s) risks two writers proceeding if a holder stalls past the timeout.
- **Fresh-branch ancestor false positive is load-bearing.** Reconciliation deliberately skips non-`done` tasks because fresh branches are trivially ancestors of their base (`reconcile.ts:41-47`). Any change to merge detection must preserve this guard or tasks disappear on restart.
- **Append-only shared check is byte-prefix plus line-count.** A task that reformats (line-ending normalization, trailing-newline change) without changing semantics can fail the shared-append gate (`contract-validator.ts:38-81`). CRLF repos need care.
- **Executor failure surface is stringly typed.** Unknown executors fail with a message, but misspelled executor names are only caught at spawn time, not at `task create` time.
- ** Governance is file-presence plus execSync.** Gate commands run synchronously in the worktree at merge time; a slow or hanging gate blocks the merge with no timeout documented in the examined sources.
- **Small maintenance smells.** `integration.ts` (93 lines) and `integrations.ts` (162 lines) coexist as near-duplicate names; `state.ts` carries two overlapping backfill layers (`migrateStateShape` plus `parseState` defaults) that must be kept in agreement.

---

## 11. How It Compares to Alternatives

- **Claude Squad / tmux-based multi-agent runners** multiplex agent sessions in terminals but leave file coordination to the user; ruah instead makes file ownership a first-class, enforced contract with pre-start rejection and post-execution validation. Tradeoff: ruah requires upfront claim declarations where tmux runners require nothing.
- **Gastown / worktree-per-agent harnesses** isolate agents in worktrees or containers but typically merge by hand or by convention; ruah adds claim-aware scheduling (overlap ratio/risk thresholds), artifact capture with patches, and dependency-ordered merges with governance gates. Tradeoff: more machinery per task in exchange for auditable, replayable merges.
- **LangGraph / workflow DAG frameworks** offer richer control flow (cycles, conditional edges, streaming state) with runtime dependencies and LLM-coupled execution; ruah offers a deliberately smaller model (Markdown DAGs, three stage strategies, zero runtime deps, LLM-free orchestrator). Tradeoff: less expressive workflows, far smaller install and no API coupling.
- **Fleet (this repo's own orchestrator)** uses a centralized beads database and Python worker supervision for agentic work distribution; ruah uses a single JSON state file with revision guards and git worktrees for code-task isolation. Tradeoff: fleet centralizes scheduling across heterogeneous work, ruah specializes in safe parallel code edits in one repo.

Positioning: ruah-orch is the minimal-dependency, file-contract-first way to run several coding-agent harnesses against one repository in parallel without merge chaos.

---

## Appendix: Selected Code Snippets

**Atomic state save with revision guard (`state.ts:234-263`)**

```ts
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

**Task environment construction (`executor.ts:412-431`)**

```ts
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

**Worktree creation (`git.ts:140-159`)**

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

**Ready-set stage expansion (`workflow.ts:239-267`)**

```ts
export function getExecutionPlan(tasks: WorkflowTask[]): WorkflowTask[][] {
	const taskMap = Object.fromEntries(tasks.map((t) => [t.name, t]));
	const remaining = new Set(tasks.map((t) => t.name));
	const completed = new Set<string>();
	const stages: WorkflowTask[][] = [];

	while (remaining.size > 0) {
		// Find tasks whose dependencies are all satisfied
		const ready: WorkflowTask[] = [];
		for (const name of remaining) {
			const task = taskMap[name];
			const depsReady = task.depends.every((d) => completed.has(d));
			if (depsReady) ready.push(task);
		}

		if (ready.length === 0) {
			// Stuck — remaining tasks have unmet deps (cycle should have been caught by validateDAG)
			break;
		}

		stages.push(ready);
		for (const task of ready) {
			remaining.delete(task.name);
			completed.add(task.name);
		}
	}

	return stages;
}
```
