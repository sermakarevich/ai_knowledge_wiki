> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# ORC Anti-Patterns (ORC-01 to ORC-18)

**In one sentence:** Eighteen numbered failure patterns — from shallow-slice disguise and evidence upgrades to stale worktree bases and runbook bloat — give every review a shared rejection vocabulary backed by real incidents.

## Key points

- ORC IDs are shared verbatim across all three adapters (claude, codex, kimi); the house rule is that every entry is backed by a real incident and a gate that never caught a real bug does not belong (playbook `README.md:15,68-91`).
- ORC-01–03 cover fake completion: shallow-slice disguise, evidence-label upgrade, and blind trust in self-reported gates (`SKILL.md:700-702`).
- ORC-04–08 cover orchestration discipline failures: slot-filling dispatch, review treated as authorization, constraint amnesia, the orchestrator writing worker code, and merging before review (`SKILL.md:703-709`).
- ORC-09–14 cover execution failures: silent stops, idempotency blindness, phantom commits (the #1 Claude Code subagent failure mode), parallel name collisions, same-module parallelism, and the stale worktree base trap (`SKILL.md:710-716`).
- ORC-15–18 cover review and process decay: skipped reviews, role drift, runbook bloat, and motion mistaken for progress (`SKILL.md:717-721`).
- The runbook prune rule (ORC-17) requires every gate to periodically show evidence of catching a real bug or be demoted or deleted (`SKILL.md:20,719`).
- Fleet fit: the ORC table is directly reusable as supervisor rejection reasons and worker guidance keyed by ID.

---

## The table

(`SKILL.md:700-721`; playbook `README.md:68-91`)

| ID | Pattern | Gloss |
|---|---|---|
| ORC-01 | Shallow-slice disguise | Read-only shells or placeholders dressed as features; rejected unless they remove a named blocker (`SKILL.md:126-141`) |
| ORC-02 | Evidence upgrade | Local claimed as proxy, proxy as direct; TCP reachability cited as payment proof (`SKILL.md:252-253,520`) |
| ORC-03 | Blind self-report trust | Accepting "gates pass" without re-running them on the acceptance side |
| ORC-04 | Slot-filling dispatch | Dispatching because a slot is free, not because a bounded contract is ready (`SKILL.md:498`) |
| ORC-05 | Review as authorization | Treating one passing review as license to merge + push + deploy + cleanup |
| ORC-06 | Constraint amnesia | Forgetting allowed/forbidden paths, hardware/payment/human gates mid-batch |
| ORC-07 | Orchestrator writes worker code | Implementing the task yourself because dispatch failed (`SKILL.md:221`) |
| ORC-08 | Merge before review | Merging a branch that has not passed the review gate (except the defined pre-merge-review pipeline for high-risk paths) |
| ORC-09 | Silent stop | Agent halts without reporting a blocker; content-filter refusals must be recorded, retried, then marked `blocked` (`SKILL.md:569-575`) |
| ORC-10 | Idempotency blindness | Accepting work that cannot be safely re-run or re-applied |
| ORC-11 | Phantom commit | "Done" with nothing committed — the #1 Claude Code subagent failure mode (`SKILL.md:712`); fixed by the MUST-COMMIT rule, 40% → 100% commit rate |
| ORC-12 | Parallel name collision | Two agents inventing the same symbol (e.g. `PaymentStatus`); fix with scoped naming (`OdPaymentStatus`) (`SKILL.md:714`) |
| ORC-13 | Same-module parallelism | Parallel agents in one module; measured 43% conflicts → 0% when serialized (`SKILL.md:715`) |
| ORC-14 | Stale worktree base | Branching from local main instead of `origin/main` after serial merges (`SKILL.md:72-79`) |
| ORC-15 | Review skip | Skipping cross-model review; two consecutive skips stop the run (`SKILL.md:321-325`) |
| ORC-16 | Role drift | Reviewer, merger, and worker roles blurring into one actor |
| ORC-17 | Runbook bloat | Gates accreting without evidence; prune rule: show a caught bug or be demoted/deleted (`SKILL.md:20,719`) |
| ORC-18 | Motion vs progress | Activity counts (batches, agents, lines) mistaken for capability (adapter `README.md:89`) |

## How to use the vocabulary

The playbook's adoption ladder tells any harness to cite ORC IDs in review (playbook `README.md:96-102`). New patterns are added by appending a numbered row with a real incident behind it; IDs stay shared across adapters, so numbering is coordinated.

**Covers:** claude-orchestrator `SKILL.md:20,126-141,221,252-253,498,569-575,700-721`; orchestration-playbook `README.md:15,68-91,96-102`; adapter `README.md:85-89`.
