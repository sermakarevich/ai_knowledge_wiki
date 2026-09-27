> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Claude-Orchestrator Skill + Orchestration-Playbook Core

## Claims vs. evidence

1. **Cross-model review catches what self-review and gates miss (15×P1 + 37×P2).** Suggestive. The yield is concrete (failure classes named: DTO mismatches, tenant filters, float-cents, fake toasts) and the case-study comparison (plan-text vs repo-access reviewer) is genuinely informative — but there is no false-positive rate, no control batch without cross-model review, and no window or dataset. Treat as a strong field report, not a measured effect.
2. **Same-module serialization cut conflicts 43% → 0%.** Suggestive. Direction is plausible and the cost math (10–15 min resolution vs wall-clock gain) is honest mechanism — but one team, one codebase shape, no variance reported. Likely transfers to similar web-app module structures; less sure for loosely coupled monorepos.
3. **Five P1 patterns cover ~40% of P1s; only-append auto-merge succeeds ~57%.** Weak. Useful as a checklist either way, but the percentages have no denominator, sample window, or adjudication rule. Borrow the checks, ignore the precision.
4. **The discipline ports across harnesses (three adapters, shared ORC IDs).** Suggestive. The kimi adapter's existence is attested only by link, and the claude/codex execution models genuinely differ (sync vs async) — but the shared core (evidence, contract, iron rules, ORC IDs) is prose, so portability is inherently plausible.

## Genuinely new vs. repackaged

The genuinely new unit is **prose discipline as the reusable artifact**: contracts + evidence labels + numbered anti-patterns + enforced outside review, with no runtime code. The pieces are individually old (worktrees, code review, checklists, "definition of done" from agile; evidence hierarchies from medicine/intelligence). What is novel is packaging them as a **failure-case library where every rule needs a real incident** — that prune rule is the idea most systems lack. The Minimalism Ladder, live-proof gate, and whole-invariant re-review are solid practitioner formulations rather than inventions.

## Weaknesses and blind spots

- Numbers without provenance (above); the README's own warning — counts measure activity, not capability — is the most honest line in the corpus.
- Severity (P1/P2/P3) is defined only by handling, never by stated criteria; triage consistency rests on unwritten judgment.
- Push-to-`origin/main` is assumed; forks, protected branches, offline work silently break the flow.
- Sync/async boundary is one sentence wide (forbidden fire-and-forget vs tolerated background review).
- Two pipelines (default merge→review vs pre-merge review for high-risk paths) hinge on correctly classifying task risk up front — the hardest step, with the least guidance.
- The P1 hotfix carve-out (orchestrator edits ≤5 lines directly) cuts against ORC-07 on labeling discipline alone.
- No cost analysis: synchronous batches + whole-invariant re-reviews + cross-model review of every batch are expensive; no token/time figures to weigh against the P1 yield.

## Applicability

Works where: a single main line, push access, disjoint-module parallelism, concrete gates (tests, builds, device readbacks), and access to a second model family for review. Fails or degrades where: protected-branch flows, offline work, UI/taste-heavy tasks without rubrics, single-model environments, or teams unwilling to pay the review-per-batch tax. Prerequisites: git worktree fluency, a written contract habit, and a reviewer (human or cross-model) that actually checks — prose discipline is enforceable only where someone verifies.

**Relevance to my work**
- **Fleet task specs:** add the anti-shallow-slice field + evidence labels + no-upgrade rule to worker RESULT.json acceptance — directly attacks placeholder "progress". Trial.
- **Supervisor rejections:** adopt ORC IDs as rejection vocabulary so workers get stable, citable guidance instead of ad-hoc prose. Trial.
- **Review policy:** gate next-batch dispatch on review-launched + findings-processed + written trace, with P2 escalation; use whole-invariant re-review to stop ping-pong rework loops. Trial.
- **Ignore:** the sync batch loop itself and the push-to-origin mechanics — fleet already owns the async runtime (bead DB, heartbeats, worktrees); do not copy what fleet already does better.

## What this changes

If the claims hold: multi-agent coding shifts from "more agents" to "better gates" — the scarce resource is verification, not generation; reviewer vantage (repo access, different family) matters more than reviewer brand; and runbooks stay alive only through prune rules. Second-order effect: teams that adopt evidence labeling will discover how much of their "done" was `local` masquerading as `direct` — uncomfortable but valuable. If claims only partially hold (likely on the exact percentages), what survives is the checklist core: contracts, labels, iron rules, ORC IDs, outside review.

## Verdict

A strong practitioner system with weak quantification: the mechanisms are sound, incident-grounded, and immediately borrowable, while the numbers are field lore rather than measurements. Its real contribution is making agent governance portable prose instead of runtime code. **trial** — adopt the evidence labels, contract fields, and ORC vocabulary into fleet acceptance and rejection paths, and measure whether they catch real failures before adopting the batch loop or the review-per-batch cost.
