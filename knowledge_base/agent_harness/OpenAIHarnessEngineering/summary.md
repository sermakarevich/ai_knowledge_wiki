# Harness Engineering: Leveraging Codex in an Agent-First World

**Article:** [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI, Feb 11 2026

## Human Readable TL;DR

Imagine a construction crew where robots do all the building and humans only draw the blueprints, set the safety rules, and inspect the result. An OpenAI team tried exactly that for software: for five months, no human wrote a single line of code, and AI helpers (called Codex) wrote everything, about a million lines in total. It worked and went roughly ten times faster than writing by hand. The secret was not clever instructions but good scaffolding: clear maps instead of giant manuals, automatic rule-checkers, and robot reviewers, so the humans could spend their time designing the worksite instead of laying bricks.

## TL;DR

An OpenAI engineering team built and shipped an internal-beta product over five months with zero manually-written code, producing roughly one million lines across application, tests, CI, docs, and tooling via Codex agents at an estimated one-tenth the hand-written time. The post introduces "harness engineering": designing environments, intent specification, and feedback loops so agents do reliable work, with human time and attention as the fixed scarce resource. Key mechanisms include AGENTS.md-as-map with a structured docs/ system of record, per-worktree application legibility (CDP browser control, ephemeral LogQL/PromQL observability), mechanically enforced layered architecture with remediation-carrying linters, agent-to-agent review with permissive merge gates, and scheduled garbage collection against entropy via golden principles. The repository crossed into single-prompt end-to-end feature delivery, with open questions on multi-year coherence and where human judgment compounds best.

---

## Problem & Motivation

When a team's primary job stops being writing code and becomes getting agents to write it, existing engineering practice breaks: environments are underspecified, agents cannot verify their own work, giant instruction files rot, architectural drift compounds at machine speed, and human QA becomes the bottleneck. The team imposed the zero-hand-written-code constraint to force discovery of whatever environment design, specification practices, and feedback loops actually raise engineering velocity by orders of magnitude.

---

## Main Original Ideas

1. **Harness engineering as a discipline.** The scarce resource is human time and attention; engineering effort moves to designing environments, specifying intent, and building feedback loops that let Codex agents execute reliably.
2. **AGENTS.md as map, docs/ as system of record.** A short (~100-line) map file with progressive disclosure into a structured, CI-validated knowledge tree (design docs, exec plans, product specs, quality grades) replaces the failed monolithic instruction manual.
3. **Application legibility for agents.** Per-worktree bootable instances, Chrome DevTools Protocol browser control (DOM snapshots, screenshots, navigation), and ephemeral per-worktree observability (LogQL/PromQL) let agents reproduce, fix, and verify against the running system, including multi-hour overnight runs.
4. **Mechanically enforced architecture and taste.** Rigid layered domains (Types → Config → Repo → Service → Runtime → UI) with a single Providers interface, custom Codex-generated linters and structural tests, remediation instructions embedded in lint errors, and taste invariants, with autonomy inside boundaries.
5. **Throughput-driven merge philosophy plus garbage collection.** Minimal blocking gates and short-lived PRs with agent-to-agent review (corrections cheap, waiting expensive), paired with golden principles and recurring background cleanup agents that collect entropy daily instead of in Friday cleanup marathons.

---

## Key Findings

- Zero-hand-written-code constraint sustained for five months on a real product with daily internal users and external alpha testers; roughly one million lines and about 1,500 merged PRs from a team growing 3 to 7 engineers.
- Sustained throughput of about 3.5 merged PRs per engineer per day, rising (not falling) as the team grew; estimated at roughly one-tenth the hand-written time.
- Early progress was slow because the environment was underspecified, not because the model was incapable; depth-first capability building (each failure becomes permanent tooling/guardrail/docs) compounded over time.
- The big-AGENTS.md manual failed in four specific ways: scarce context crowded out, saturation into non-guidance, instant rot, and resistance to mechanical verification.
- Boring, composable, API-stable dependencies beat opaque ones for agent legibility; the team reimplemented small subsets (e.g. an OTel-integrated map-with-concurrency helper with full test coverage) rather than fight opaque upstream behavior.
- Single-prompt end-to-end delivery was reached (validate, reproduce with video, fix, validate with video, PR, review responses, build remediation, merge with human escalation only on judgment), but explicitly depends on this repo's tooling and may not generalize yet.
- Manual entropy cleanup at 20% of engineering time (every Friday on "AI slop") did not scale; automated golden-principle collection with sub-minute-review refactor PRs did.

## Suggestions & Future Directions

1. Treat every agent failure as a missing capability (tool, guardrail, abstraction, documentation) and have Codex itself encode the fix, so the harness compounds.
2. Push all team knowledge (decisions, norms, taste) into repository-local versioned artifacts; anything in chat threads or heads is invisible to the agent.
3. Promote repeatedly-needed guidance from prose documentation into enforced code (linters, structural tests) with remediation-carrying error messages.
4. Open questions the post leaves unresolved: multi-year architectural coherence of fully agent-generated systems, highest-leverage placement and compounding of human judgment, and how the system evolves as models improve.

## Authors & Institutions

Ryan Lopopolo (Member of Technical Staff, OpenAI), with thanks to Victor Zhu, Zach Brock, and the product team. OpenAI, February 2026.
