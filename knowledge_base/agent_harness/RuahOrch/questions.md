---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: ruah-orch

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What are the three claim buckets, and in what precedence order are they matched?

> [!tip]- Answer
> Owned (exclusive write), shared (append-only write), and read-only. `findClaimMatch` checks owned first, then shared-append, then read-only. See [[wiki/01-claims-and-artifacts|Claims, Artifacts, and Contract Enforcement]].

### Q2. What does a TaskArtifact contain, and when does it count as absent?

> [!tip]- Answer
> Identity (taskName, workspaceId), history pointers (baseRef, headRef, commitSha), content (changedFiles, full patch), embedded claims, and a validation triple (executorSuccess, contractSuccess, optional gatesSuccess). It counts as absent when both changedFiles and patch are empty. See [[wiki/01-claims-and-artifacts|Claims, Artifacts, and Contract Enforcement]].

### Q3. How does shared-append (append-only) validation decide pass vs fail?

> [!tip]- Answer
> Missing base version passes; deleted/moved files fail; identical content passes; otherwise the new content must start with the original bytes and must not reduce the line count, else a shared-append violation is recorded. See [[wiki/01-claims-and-artifacts|Claims, Artifacts, and Contract Enforcement]].

### Q4. Why does saveState re-read the disk under the lock, and what happens on a revision mismatch?

> [!tip]- Answer
> To detect stale writes from concurrent processes: it compares the in-memory revision with the on-disk revision, throws without writing on mismatch, and persists revision + 1 on match. See [[wiki/02-state-and-restart-safety|State, Persistence, and Restart Safety]].

### Q5. What makes state persistence crash-safe, and what serializes concurrent writers?

> [!tip]- Answer
> Crash safety comes from write-to-temp plus atomic rename; serialization comes from an exclusive O_EXCL lock file with 50 ms polling, a 5 s timeout, and stale treatment after 30 s. See [[wiki/02-state-and-restart-safety|State, Persistence, and Restart Safety]].

### Q6. Which task statuses does restart reconciliation touch, and why are the others skipped?

> [!tip]- Answer
> It cleans merged and cancelled tasks unconditionally and auto-removes done tasks only when both branches exist and the branch is merged; created, in-progress, and failed tasks are skipped to avoid the disappearing-tasks false positive from fresh branches trivially being ancestors of their base. See [[wiki/02-state-and-restart-safety|State, Persistence, and Restart Safety]].

### Q7. trace what happens when a Markdown workflow file arrives: parse, validate, stage, and run.

> [!tip]- Answer
> The file is parsed into tasks with files/executor/depends/prompt fields; the DAG is validated (unknown deps, DFS cycle detection); ready-set expansion groups tasks into stages; each stage gets a planner strategy and runs in order with contract validation, compatibility checks, gates, and ordered merges. See [[wiki/03-planner-and-workflows|Planner, DAG Workflows, and Claim-Aware Scheduling]].

### Q8. What numeric thresholds force a serial stage, and how is a serial stage ordered?

> [!tip]- Answer
> Overlap ratio above 0.3 or risk score above 2.0 forces serial execution, ordered most-connected-first (by connection count). See [[wiki/03-planner-and-workflows|Planner, DAG Workflows, and Claim-Aware Scheduling]].

### Q9. How does the planner compute pairwise risk between two tasks in a stage?

> [!tip]- Answer
> It sums per-pattern file-size weights (glob/directory 1.0, tiny files 0.3-0.7, larger 1.5, missing 0.5) plus a history penalty for prior merge conflicts or contract failures plus 3.0 for any compatibility conflict. See [[wiki/03-planner-and-workflows|Planner, DAG Workflows, and Claim-Aware Scheduling]].

### Q10. How is the executor for a task chosen, and how would you add a new harness?

> [!tip]- Answer
> From the task's executor string field defaulting to script at spawn time; an unknown name fails fast. Adding a harness means adding one adapter entry keyed by name with its spawn form. See [[wiki/04-executors-and-workspaces|Executors, Workspace Providers, and Task Lifecycle]].

### Q11. Which RUAH_* variables are always set, which are conditional, and what reads RUAH_PARENT_TASK back?

> [!tip]- Answer
> Always: RUAH_TASK, RUAH_WORKTREE, RUAH_EXECUTOR. Conditional: RUAH_PARENT_TASK (when parented), RUAH_ROOT (when repoRoot known), RUAH_FILES (when file scope non-empty). taskCreate reads RUAH_PARENT_TASK as the --parent fallback so subagents inherit scope. See [[wiki/04-executors-and-workspaces|Executors, Workspace Providers, and Task Lifecycle]].

### Q12. How do subtask merge targets and governance gates differ from root-task ones?

> [!tip]- Answer
> Subtask branches merge from inside the parent worktree and their gates are deferred to the parent merge; root-task branches merge after checking out the base in the repo root with governance gates enforced. Merging also blocks while unmerged children exist. See [[wiki/04-executors-and-workspaces|Executors, Workspace Providers, and Task Lifecycle]].

### Q13. What is the weakest link in ruah's evidence that its design works at scale?

> [!tip]- Answer
> The single JSON state file with a 5 s lock timeout is an unmeasured contention point — no benchmarks show behavior under dozens of concurrent writers — and glob semantics are hand-rolled rather than battle-tested, so exotic patterns and CRLF reformat edge cases can surprise. See [[critical_thinking|Critical Analysis]].
