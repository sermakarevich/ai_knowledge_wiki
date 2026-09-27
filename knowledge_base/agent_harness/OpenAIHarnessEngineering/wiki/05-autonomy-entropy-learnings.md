> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Autonomy, Entropy, and What Comes Next

**In one sentence:** The repository crossed into end-to-end single-prompt feature delivery with humans working one abstraction layer up, while a codified garbage-collection loop fights the entropy Codex otherwise accumulates by copying existing patterns including the bad ones.

## Key points

- "Agent-generated" means everything: product code and tests, CI configuration and release tooling, internal developer tools, documentation and design history, evaluation harnesses, review comments and responses, repository-management scripts, and production dashboard definition files.
- Humans stay in the loop one layer up: prioritizing work, translating user feedback into acceptance criteria, validating outcomes, and treating every agent struggle as a missing-tool, guardrail, or documentation signal that Codex itself then encodes as a fix.
- The autonomy threshold crossed recently: from a single prompt Codex can validate codebase state, reproduce a reported bug, record a failure video, implement the fix, validate it by driving the app, record a resolution video, open the PR, answer agent and human feedback, remediate build failures, escalate only on judgment calls, and merge.
- That autonomy is explicitly repo-specific: it depends on this repository's structure and tooling and should not be assumed to generalize without similar investment, at least not yet.
- Entropy is structural: Codex replicates patterns already in the repository even when uneven or suboptimal, so drift compounds unless actively collected.
- The first cleanup attempt failed to scale: humans spent every Friday (about 20% of the week) cleaning "AI slop" manually, which collapsed under growing throughput.
- The replacement is golden principles plus scheduled collection: opinionated mechanical rules (prefer shared utility packages over hand-rolled helpers; never probe data YOLO-style, instead validate at boundaries or use typed SDKs) enforced by recurring background Codex tasks that scan for deviations, update quality grades, and open targeted refactoring PRs, most reviewable in under a minute and automerged.
- Open questions remain: how architectural coherence evolves over years in a fully agent-generated system, where human judgment adds the most leverage and how to encode it so it compounds, and how the system changes as models keep improving; the durable conclusion is that discipline now lives in scaffolding (tooling, abstractions, feedback loops) rather than in code.

---

## What agent-generated covers

The post enumerates the full surface agents produce: product code and tests, CI and release tooling, internal developer tools, documentation and design history, evaluation harnesses, review comments and responses, scripts managing the repository itself, and production dashboard definitions. Nothing in the repo has a human author; the human contribution is steering, specifying, and validating.

## The autonomy loop

Once testing, validation, review, feedback handling, and recovery were encoded into the system, Codex became able to drive a feature end to end from one prompt through eleven steps: validate current state, reproduce the bug, record a failure video, implement the fix, validate by driving the application, record the resolution video, open the pull request, respond to agent and human feedback, detect and remediate build failures, escalate to a human only when judgment is required, and merge. The video artifacts are notable: the agent demonstrates failure and resolution visually, using the legibility infrastructure from page 2.

## Entropy and garbage collection

### Why drift is inevitable

An agent trained to continue repository patterns will reproduce the bad ones alongside the good. Every merged imperfection becomes a template for future output, so quality decays by default. Manual Friday cleanups consuming a fifth of engineering time could not keep pace with generation throughput.

### Golden principles and background collection

The team encoded opinionated mechanical rules directly into the repository. Two are named: prefer shared utility packages over hand-rolled helpers to keep invariants centralized, and never probe data YOLO-style but validate boundaries or rely on typed SDKs so the agent cannot build on guessed shapes. On a regular cadence, background Codex tasks scan for deviations, update quality grades, and open targeted refactoring PRs; most take under a minute to review and automerge. The framing is garbage collection for technical debt, explicitly compared to a high-interest loan best paid down continuously in small increments rather than in painful bursts. Human taste is captured once, then enforced continuously on every line; bad patterns get caught daily instead of spreading for weeks.

## What is still unknown

Three open questions close the post: long-term architectural coherence over years of fully agent-generated evolution, the highest-leverage placement of human judgment and how to encode it so it compounds, and how the whole system shifts as models grow more capable. What the team treats as settled is the relocation of discipline from code to scaffolding: tooling, abstractions, and feedback loops are now the primary engineering surface, and the hardest problems are designing environments, feedback loops, and control systems for building complex reliable software at scale with agents.

**Covers:** article sections "What 'agent-generated' actually means", "Increasing levels of autonomy", "Entropy and garbage collection", and "What we're still learning".
