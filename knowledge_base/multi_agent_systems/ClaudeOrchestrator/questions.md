---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Claude-Orchestrator Skill + Orchestration-Playbook Core

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What are the ten fields of the dispatch contract, and what happens if a dispatch has no contract?

> [!tip]- Answer
> Outcome, anti-shallow-slice class, minimum-change rationale, boundaries, gates, evidence, challenge duty, restart policy, rubric, handoff. No contract, no dispatch. See [[wiki/01-task-contracts-dispatch|Task Contracts and Dispatch]].

### Q2. What does the anti-shallow-slice classification require an agent to declare?

> [!tip]- Answer
> One of `vertical-completion | runtime-proof | blocked-removal | owner-gated`, plus why the task is not repeating an already-completed first slice. See [[wiki/01-task-contracts-dispatch|Task Contracts and Dispatch]].

### Q3. Why is the batch loop synchronous, and who owns merge, push, and cleanup?

> [!tip]- Answer
> Synchronous dispatch is what makes review→merge gates enforceable; there is no fire-and-forget. The orchestrator alone owns merge (`--no-ff`), push to `origin/main`, worktree removal, and post-merge testing. See [[wiki/02-worktree-agents-batch-loop|Worktree Agents and the Batch Loop]].

### Q4. When may three agents run in parallel, and why are same-module tasks serialized?

> [!tip]- Answer
> Three only with all four preconditions: no shared contract/migration/API, no hardware/payment, clean main, disjoint modules and write sets. Same-module parallelism measured 43% conflicts vs 0% serial, and conflict resolution costs more than the wall-clock gain. See [[wiki/02-worktree-agents-batch-loop|Worktree Agents and the Batch Loop]].

### Q5. Name the four evidence levels and state the no-upgrade rule.

> [!tip]- Answer
> `direct` (real target env), `proxy` (substitute), `local` (dev/test only), `blocked` (needs human/credentials/hardware/decision). Upgrading a label is lying — never `local→proxy` or `proxy→direct`. See [[wiki/03-evidence-discipline-acceptance-rules|Evidence Discipline]].

### Q6. What are the four acceptance iron rules?

> [!tip]- Answer
> (1) "Committed" is not evidence — prove `git log <branch> --not main` is non-empty. (2) Re-run self-reported gates. (3) Review ≠ authorization to merge/push/deploy/cleanup. (4) Remove worktrees only after verified merge — plus the adapter's live-proof gate requiring `direct` proof at runtime/payment boundaries. See [[wiki/03-evidence-discipline-acceptance-rules|Evidence Discipline]].

### Q7. What are ORC-11, ORC-13, and ORC-14, and what fixes each?

> [!tip]- Answer
> ORC-11 phantom commit (claims done, nothing committed) — MUST-COMMIT rule + orchestrator commits on the agent's behalf. ORC-13 same-module parallelism — serialize same-module work. ORC-14 stale worktree base — create worktrees from `origin/main` after pushing. See [[wiki/04-orc-antipatterns|ORC Anti-Patterns]].

### Q8. What is the runbook prune rule (ORC-17)?

> [!tip]- Answer
> Every gate must periodically show evidence of catching a real bug or be demoted to an appendix or deleted; cross-harness syncs import and trim discipline. See [[wiki/04-orc-antipatterns|ORC Anti-Patterns]].

### Q9. Why must the reviewer come from a different model family, and what did the case study show?

> [!tip]- Answer
> Same-family reviewers share blind spots. Reported yield: 15×P1 + 37×P2 findings self-review and mechanical checks missed. The case study showed vantage beats brand: plan-text-only review (GPT) missed a runtime landmine that repo-access review (DeepSeek) caught. See [[wiki/05-cross-model-review-fleet-lessons|Cross-Model Review]].

### Q10. What three conditions form the review enforcement gate, and what happens after two consecutive skips?

> [!tip]- Answer
> Current-batch review launched, previous findings processed (P1 fixed, P2 recorded), written trace with findings count (no record = not run). Two consecutive skips stop the run; P2s unfixed 3+ batches escalate to P1. See [[wiki/05-cross-model-review-fleet-lessons|Cross-Model Review]].

### Q11. What is the weakest link in this source's evidence, and how should a borrower treat its numbers?

> [!tip]- Answer
> Scale numbers (53 batches, 43%→0% conflicts, 15×P1+37×P2) ship without datasets, windows, or false-positive rates, and thresholds (2-skip stop, P2→P1, ≤5-line hotfix) are heuristics without derivation. Treat them as field reports to trial, not constants to adopt. See [[critical_thinking|Critical Analysis]].
