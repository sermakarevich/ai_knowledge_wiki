> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Agent Orchestrator (AO)

## Claims vs. evidence

1. **Isolated worktrees + one PR per session let operators supervise fleets instead of babysitting (throughput 2–3 → 5+ PRs/day).** Evidence: weak. The mechanism (isolation prevents write collisions; ownership routing directs fixes) is sound and matches known failure modes, but the numbers are vendor testimonials with no baseline, no sample size, no task difficulty control, and no comparison against any alternative runner. Treat the direction as plausible, the magnitude as marketing.
2. **Derived status cannot drift while stored status always does.** Evidence: suggestive. This is a well-established pattern (event sourcing / read models), and the eight load-bearing rules are stated precisely enough to audit. But no failure-injection data or drift-incident comparison is offered — it is asserted architecture, not measured reliability.
3. **Built-in lifecycle automation recovers CI/review autonomously (right agent fixes its own CI).** Evidence: suggestive. The reaction table, signature dedup, and mode-aware delivery are concrete and implementable, and CI-failure auto-routing is corroborated by testimonial. Missing: recovery success rate, time-to-green vs manual, false-nudge rate, and behavior under flaky-test storms.
4. **27 harnesses work out of the box by reusing the user's CLIs/auth.** Evidence: strong for breadth, weak for depth. The registry list, readiness probes (`ao agent ls --refresh`), and preflight + daemon validation are verifiable mechanics; but only 4 harnesses get Chat drivers, so "support" means TUI-only for 23 of 27 — the headline count overstates parity.

## Genuinely new vs. repackaged

Little here is novel in isolation: git worktrees, one-branch-per-task, PR polling, SSE event logs, and append-only migrations are all standard practice. What is genuinely distinctive is the *combination as a product*: worktree isolation + PR-ownership invariant + fact-store/derived-status + daemon-owned (non-scriptable) lifecycle reactions + compiled-in multi-harness adapters with capability gating. The closest prior art is tmux-based parallel runners (e.g. Claude Squad's tmux + worktree model) and orchestrator-discipline approaches (skill-file contracts rather than runtimes). AO's "no workflow DSL on purpose" stance — retiring the YAML reactions schema in favor of topology + observed state machine — is a real position in the loops-vs-graphs debate, on the loops side.

## Weaknesses and blind spots

- **No step-level durability.** Durability is session/worktree/conversation-level; there is no checkpoint-resume of in-flight tool calls, no retry budget, no backoff schedule. A daemon crash mid-tool-call loses the step.
- **Tracker lane is GitHub-only in practice.** Broader tracker/SCM integrations from older docs are absent from the rewrite; teams on other forges get isolation but not the lifecycle loop.
- **Single-user, single-machine.** Loopback-first, SQLite-local, desktop-supervised daemon: there is no documented multi-operator or server-deploy story, unlike fleet's centralized beads DB + supervisor model.
- **Reviewer-agent quality is unmeasured.** The triage-before-delivery design is good hygiene, but precision/recall of machine review findings vs human review is never discussed.
- **Silent on cost.** 27 harnesses × parallel sessions × polling × reviewer runs: no token/compute cost model, no guidance on fleet sizing economics.
- **Acknowledged vs silent:** the docs openly acknowledge the retired YAML schema, the incomplete tracker lane, and the no-auto-merge stance; they are silent on cost, reviewer quality, step-level recovery, and multi-user operation.

## Applicability

Works when: a single operator (or small team) runs parallel coding agents against GitHub repos on one machine, with per-task branches and human-gated merges. Fails or degrades when: the forge is not GitHub (lifecycle loop missing), multiple operators share state (no multi-user story), tasks need step-level resume across crashes, or workflows need user-authored branching logic (no DSL by design). For Sergii's contexts:

- **Fleet orchestrator: trial the mechanisms, not the product.** Derived status, dirty-worktree protection, signature-deduped nudges, and claim-PR fallback map directly onto the beads DB + worker model.
- **Elisity data platform: watch.** The CDC-via-triggers + SSE-replay pattern is a small proven template for live pipeline dashboards, but the single-machine assumption does not transfer to shared data infra.
- **General agentic systems work: adopt the stance selectively.** "Topology + observed state machine instead of user YAML" is worth trialing wherever operators currently maintain brittle workflow files.

## What this changes

If the claims hold: parallel-agent supervision becomes a merge-approval job rather than a babysitting job; per-task isolation becomes the default rather than the careful setup; and "which harness" becomes a per-role default rather than a daily CLI decision. Second-order: reviewer agents as a standard second loop could shift human review toward triage of machine findings; compiled-in adapters could normalize "bring your own CLI + auth" as the onboarding model. If claims only partially hold (more likely): the durable-facts/derived-status pattern and the deduped owner-routing loop still survive as the portable core, even where the throughput numbers do not.

## Verdict

This is unusually explicit vendor architecture documentation — eight load-bearing rules, a concrete reaction table, named commands — which makes it auditable in a way most agent-runner marketing is not. But it remains vendor docs: no independent evaluation, no baselines, testimonial throughput numbers. Take the mechanisms seriously and the magnitudes skeptically. **trial** — prototype derived status + signature-deduplicated owner routing in fleet before adopting anything else, because those two are cheap, portable, and kill known bug classes.
