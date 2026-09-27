> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Planner, DAG Workflows, and Claim-Aware Scheduling
**In one sentence:** Ruah defines work as a Markdown task graph with dependency edges, validates it as a DAG, derives ready-set stages, and then refines each stage into parallel, parallel-with-contracts, or serial execution based on claim overlap, risk thresholds, and compatibility signals (workflow.ts:37-187, workflow.ts:194-267, planner.ts:372-484, commands/workflow.ts:136-148).
## Key points
- Workflows are Markdown files with `# Workflow: <name>`, a `## Config` block (base, parallel, on_conflict), and one `### <task>` section per task carrying files, executor, depends, prompt, and on_conflict fields (workflow.ts:59-63, workflow.ts:86-101, workflow.ts:106-180, example-feature.md:1-31).
- Config defaults are base `main`, parallel `false`, and on-conflict `fail`, with only `fail`, `rebase`, and `retry` accepted as conflict strategies at config and task level (workflow.ts:42-46, workflow.ts:91-98, workflow.ts:160-164).
- DAG validation rejects unknown dependencies and detects cycles with depth-first search over the dependency edges, returning a valid flag plus an error list (workflow.ts:194-237).
- Stage computation groups tasks into ready sets by repeatedly selecting tasks whose dependencies are all completed, so independent tasks share a stage and dependents move to later stages (workflow.ts:239-267, example-feature.md:9-31).
- Overlap analysis compares task claim sets pairwise per stage, computing an overlap ratio over the union of claim patterns and a risk score from per-pattern file-size weights plus history and compatibility penalties (planner.ts:206-261, planner.ts:183-198, planner.ts:504-530).
- Stage strategy is selected by rule: single-task stages run parallel, hard compatibility conflicts force serial, zero effective overlap runs parallel, overlap above 0.3 ratio or 2.0 risk forces serial ordered by connection count, and manageable overlap runs parallel-with-contracts (planner.ts:100-103, planner.ts:372-484).
- Contracts assign owned, shared-append, and read-only access per task, either directly from explicit claim sets or by primary-task heuristic where the task referencing the most files owns a shared pattern and others get append-only access (planner.ts:268-365, planner.ts:628-670).
- Workflow execution runs stages in dependency order, applies the planner decision per stage, validates contracts and optional compatibility after execution, and merges each completed task branch before proceeding, with plan, run, explain, list, and create subcommands exposing this surface (commands/workflow.ts:54-78, commands/workflow.ts:183-199, commands/workflow.ts:294-302, commands/workflow.ts:417-505).
---
## Markdown task-graph format
- A workflow file starts with `# Workflow: <name>` for the workflow name (workflow.ts:59-63).
- The `## Config` section accepts `- base:`, `- parallel: true|false`, and `- on_conflict:` keys, overriding the defaults of base `main`, parallel `false`, and on-conflict `fail` (workflow.ts:86-101, workflow.ts:42-46).
- The `## Tasks` section holds one `### <task-name>` block per task, each initialized with empty files, null executor, empty depends, empty prompt, and on-conflict `fail` (workflow.ts:75-83, workflow.ts:106-119).
- Per-task fields are `- files:` as a comma-separated list, `- executor:` as a string, `- depends:` as a bracketed comma-separated list, `- on_conflict:` with the same three accepted values, and `- prompt:` as either inline text or a multi-line block after `|` (workflow.ts:140-180).
- Multi-line prompts are collected until a new `- <key>:` property or `###` header, dedented by the first non-empty prompt line indent, and trimmed on task completion (workflow.ts:124-137, workflow.ts:166-178, workflow.ts:189-192).
- The example workflow sets `base: main` with `parallel: true`, declares independent `backend-api` and `frontend-ui` tasks with disjoint file globs, and declares `integration-tests` on `tests/**` depending on both prior tasks (example-feature.md:1-31).
## DAG validation
- Validation builds the task-name set and reports one error per dependency edge pointing at a nonexistent task (workflow.ts:194-207).
- Cycle detection runs depth-first search from every task, tracking a recursion stack alongside a visited set, and reports a circular-dependency error when a name reappears on the active stack (workflow.ts:209-234).
- The result is a `{ valid, errors }` record where validity means zero accumulated errors (workflow.ts:194-196, workflow.ts:236-237).
- Both `run` and `plan` subcommands parse the file, run this validation first, and exit on failure before computing any execution plan (commands/workflow.ts:104-110, commands/workflow.ts:593-601).
## Claim-aware parallel-vs-serial decision
- Task claims resolve from explicit `claims` fields or `claimsByTask` overrides, falling back to deriving a claim set from the task `files` list (planner.ts:120-130).
- Pairwise stage analysis loads persisted history, computes overlapping claim patterns per pair, skips pairs with no overlap and no compatibility conflict, and otherwise derives overlap ratio as overlapping count over union size capped at 1.0 (planner.ts:206-238).
- Risk per pair sums per-pattern file-size weights (glob 1.0, directory 1.0, under 100 bytes 0.3, under 1000 bytes 0.7, larger 1.5, missing file 0.5) plus a history penalty for prior merge conflicts or contract failures plus 3.0 for any compatibility conflict (planner.ts:183-198, planner.ts:239-246, planner.ts:504-530).
- `decideStageStrategy` returns `parallel` for single-task stages, `serial` in alphabetical order when hard compatibility conflicts exist, `parallel` when no effective overlap remains after honoring clean compatibility marks, `serial` ordered by most-connected-first when any pair exceeds 0.3 overlap ratio or 2.0 risk, and `parallel-with-contracts` otherwise (planner.ts:100-103, planner.ts:372-484).
- Verbatim excerpt, core/planner.ts:414-423:
```ts
	if (effectiveOverlaps.length === 0) {
		return {
			strategy: "parallel",
			tasks,
			reason:
				overlaps.length > 0
					? "compatibility data indicates safe parallelism"
					: "no file overlaps detected",
		};
	}
```
- `createSmartPlan` applies this per stage, defaults the parallel cap to 5, splits parallel or contract stages exceeding the cap into numbered sub-batches, and aggregates counts of parallel, serial, contract, and overlap totals (planner.ts:538-621, planner.ts:492-502).
- `splitStageByParallelLimit` slices oversized stages into consecutive chunks of at most `maxParallel` tasks and returns single-batch input unchanged (planner.ts:492-502).
## Parent/child branching
- Each executed task is recorded in persistent state with `parent: null`, an empty `children` list, a copy of its `depends` array, and a `workflow` record of workflow name, path, stage number, and depends (commands/workflow.ts:236-266).
- The record also stores base branch, workspace handle, branch name, worktree path, file list, lock mode, executor, prompt, and lifecycle timestamps from creation through start, completion, and merge (commands/workflow.ts:236-266).
- The examined sources initialize the parent/child fields but do not populate branching beyond these defaults in the workflow run path; dependency ordering is carried by the copied `depends` array and the stage index (commands/workflow.ts:253-265).
## Merge in dependency order
- `getExecutionPlan` emits stages by fixed-point ready-set expansion: each iteration collects tasks whose dependencies are all completed, appends them as one stage, and marks them complete until no tasks remain (workflow.ts:239-267).
- Verbatim excerpt, core/workflow.ts:239-267:
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
- `workflow run` iterates these stages in index order, uses the planner `serialOrder` sub-stages when the strategy is serial and a single combined stage otherwise, and halts the workflow on stage failure while preserving failed tasks for takeover (commands/workflow.ts:183-199, commands/workflow.ts:375-415).
- Within a sub-stage, tasks acquire file locks, get isolated workspaces branched from the base, execute with the planner contract injected, and pass contract validation before being marked done with captured artifacts (commands/workflow.ts:201-271, commands/workflow.ts:273-360).
- Optional per-stage compatibility checks compare each artifact against the base and pairwise between artifacts, marking integration state clean, stale, or conflict and exiting on pairwise conflict (commands/workflow.ts:417-472).
- Governance gates run per workspace after compatibility, and each task branch is then merged into the base in stage order with history entries, workspace removal, and state cleanup on success (commands/workflow.ts:474-509).
## Workflow CLI surface
- The dispatcher requires a subcommand and routes `run`, `explain`, `plan`, `list`, and `create`, exiting on missing or unknown subcommands (commands/workflow.ts:54-78).
- `run <file.md>` supports `--dry-run`, `--debug-exec`, `--json`, and `--strict-locks` flags, validates the DAG, computes the stage plan, builds a smart plan only when workflow config enables parallel, prints the plan, and optionally emits the stage list as JSON without executing (commands/workflow.ts:92-148).
- Parallel execution uses `Promise.all` over per-task promises when the strategy is not serial and more than one task is present, and awaits each promise sequentially otherwise (commands/workflow.ts:362-373).
- `plan <file.md>` prints workflow name, base, parallel flag, task count, formatted stages, per-task files, executor, dependencies, truncated prompt, and, for parallel workflows, overlap diagnostics plus per-stage strategy and contract bucket counts, with a `--json` alternative emitting workflow, config, tasks, and stages (commands/workflow.ts:585-683).
- `explain <name|file.md>` reads persisted task state for the matching workflow, sorts by stage then name, reports blocking created, in-progress, and failed tasks, and prints per-status next actions for takeover, start, or merge (commands/workflow.ts:530-583).
- `list` enumerates Markdown files under `.ruah/workflows` with name and path pairs and supports `--json`, while `create <name>` scaffolds a templated workflow with current branch as base, refuses to overwrite without `--force`, and points at `run` as the next step (commands/workflow.ts:685-732, workflow.ts:269-277, commands/workflow.ts:734-764).
- Contract text rendered into task artifacts uses `## Modification Contract` with owned, shared-append append-only, and read-only sections depending on which buckets are nonempty (planner.ts:628-670).
**Covers:** packages/core/src/core/{planner,workflow}.ts, commands/workflow.ts, .ruah/workflows/example-feature.md @ 58c4ee5b
