---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Bernstein

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What does "no model in the coordination loop" mean in Bernstein code?

> [!tip]- Answer
> It means scheduling, assignment, retry, and completion decisions are made by plain single-threaded Python in `tick()` with no prompt or model call on that path. Model calls happen only in agents and planning, and planning calls are recorded to `llm_calls.jsonl` for replay. See [[wiki/01-deterministic-scheduler|Deterministic Scheduler]].

### Q2. What are Bernstein's two bounded retry budgets, and where do exhausted tasks go?

> [!tip]- Answer
> Regular retries are capped at a hard maximum of 2, escalating effort first then model haiku → sonnet → opus unless the operator pins the model. Janitor verification failures reopen under the same id with a separate default budget of 2 cycles, then fail permanently. Exhausted tasks land in the DLQ at `.sdd/runtime/dlq.jsonl` for operator listing and resubmission. See [[wiki/02-task-lifecycle-retries|Task Lifecycle and Retries]].

### Q3. Why does a workspace hash mismatch force a cold retry instead of a warm resume?

> [!tip]- Answer
> A warm retry reattaches to the old session, so it is only safe when a verified checkpoint exists and the live worktree hash matches the recorded hash. A mismatch means the resumed session would inherit silently diverged files, so the pure `decide_retry` function downgrades to cold and resends the full prompt. See [[wiki/02-task-lifecycle-retries|Task Lifecycle and Retries]].

### Q4. How do Bernstein's per-task worktrees, branch names, and FIFO merge queue isolate parallel work?

> [!tip]- Answer
> Each session gets its own checkout under `.sdd/worktrees/<session_id>` on branch `agent/<session_id>`, so agents never write the same files during work. Merges serialize one at a time through a thread-safe FIFO queue after lint, type-check, and test gates, with `git merge-tree` pre-flight and `git merge --abort` on conflict. See [[wiki/03-worktrees-merge-gates|Worktrees and Merge Gates]].

### Q5. What breaks if worktrees are disabled with `use_worktrees=False`?

> [!tip]- Answer
> No worktree manager is created and the agent falls back to the shared main workdir with isolation reported as `none`. Parallel agents can then overwrite each other's files and branch-per-session guarantees plus pre-merge gates lose their isolation premise. See [[wiki/03-worktrees-merge-gates|Worktrees and Merge Gates]].

### Q6. How does the adapter registry add a new coding-agent CLI without touching orchestration?

> [!tip]- Answer
> The `_ADAPTERS` dict maps a short name like `claude` to an adapter class implementing `spawn()` and `name()`, and `get_adapter()` instantiates it and raises `ValueError` for unknown names. New harnesses add one dict entry plus one subclass with a strategy row and contract YAML, or ship via `bernstein.adapters` entry points or data-only capability profiles. See [[wiki/04-adapter-registry|Adapter Registry]].

### Q7. How do Bernstein's two workflow formats differ, and how do guarded edges work?

> [!tip]- Answer
> A YAML manifest uses a `nodes` list with `command` or `agent` plus `depends_on` and `when`, while the DSL uses `phases` plus a `nodes` mapping with `phase`, `role`, and `retry`. A DSL edge is plain `depends_on` or guarded `source` plus `condition` such as `status == 'failed'`, checked by a safe AST evaluator without `eval()`, with all-skipped nodes recorded as stranded. See [[wiki/05-workflow-abstraction|Workflow Abstraction]].

### Q8. How do the lineage spine, replay journal, and evidence bundles each surface a one-byte tamper?

> [!tip]- Answer
> The always-on spine chains `entry_hash = H(prev_hash, artifact_path, content_hash, ...)` with HMAC tags, while the journal chains `event_hash = H(prev_hash, event_type, payload_hash, index)` excluding wall-clock fields. Signed Ed25519 receipts and content-addressed bundles under a 1 MiB per-blob cap rehash bytes at verify time, so any change reports a named mismatch at an exact line, step, or blob. See [[wiki/06-lineage-receipts-audit|Lineage and Audit]].

### Q9. What are Bernstein's quality-gate defaults, and what blocks versus allows a bypass?

> [!tip]- Answer
> Lint (`ruff check .`) is on by default while type-check (`pyright`) and tests are opt-in, with PII, DLP, mutation, intent, and run-config gates available. The runner passes only when no result is marked blocked, and any skip raises unless `allow_bypass` is set. See [[wiki/07-policy-quality-gates|Policy and Quality Gates]].

### Q10. Why must strict replay abort on a cache miss instead of calling the live model?

> [!tip]- Answer
> Recording every planning prompt plus model, provider, temperature, and tokens into per-key FIFO queues is what makes the same seed reproduce yesterday's task graph byte-identically. Falling through to live on a miss would silently substitute a new decomposition while the journal digest still claims reproducibility, so strict mode raises `ReplayMissError` unless `BERNSTEIN_REPLAY_ALLOW_LIVE_MISS` opts in. See [[wiki/01-deterministic-scheduler|Deterministic Scheduler]].

### Q11. How would you port Bernstein's CAS claims, DLQ, and adapter registry to another orchestrator like Fleet?

> [!tip]- Answer
> Add a version number per bead and reject claims with stale versions plus reset claimed and in-progress beads to open on restart, mirroring Bernstein's 409-conflict and crash-recovery path. Store exhausted beads in a JSONL dead-letter list with replay-as-new, and hide every coder CLI behind one `spawn` interface plus a name-to-class table. See [[wiki/targeted|Targeted Comparison for Fleet]].

### Q12. What is the weakest evidence link in Bernstein's determinism and zero-token claims?

> [!tip]- Answer
> The scheduling, seed, DAG, and strict-replay mechanisms are source-verified, but claims like zero coordination tokens, byte-identical subagent delegation, and plan-stage expansion rest on docs without a token counter or examined delegation path in the files read. Treat those as unproven until measured, which is the [[critical_thinking]] habit of separating verified mechanism from asserted consequence. See [[wiki/01-deterministic-scheduler|Deterministic Scheduler]].
