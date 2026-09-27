# Autonomous Long-Running Coding Agents

**Source:** [Elvis (@omarsar0) on X (Jun 13, 2026)](https://x.com/omarsar0/status/2065880971031834786)
**Author:** Elvis Saravia (DAIR.AI), written in collaboration with Codex and Claude Code
**Published:** June 13, 2026

---

## Human Readable TL;DR

Think of a coding agent like a contractor. Right now, most people use them like a handyman you supervise every single minute. The shift being described here is: how do you hire a contractor who can work unsupervised for days, actually finish the job correctly, and not lie to you about it being done? The answer isn't just a smarter contractor -- it's better blueprints (goals), independent inspectors (evaluators), and check-in schedules (loops) built around them. You define what "done" means precisely enough that the contractor can't fake it.

## TL;DR

This article, based on a DAIR.AI Academy session, frames the transition in AI coding agents from turn-by-turn prompting to full autonomous operation. The core architecture has four components: a **goal** (a contract defining success, constraints, and budget), an **evaluator** (external judge -- deterministic checks for crisp tasks, LLM-as-judge for fuzzy ones), a **loop** (the outer control system that re-runs the agent until the goal is met), and **verifiers** (external evidence sources the agent can't manipulate). Session mining and visual artifacts round out the system as memory and observability layers.

---

## Problem & Motivation

Most serious engineering work spans long horizons -- ambiguous requirements, partial failures, changing context, and repeated verification. Current agent patterns rely on constant human steering (turn-by-turn prompting), which doesn't scale. The gap is not model capability but control system design: without structured goals, evaluators, and loops, even powerful models stop early, take shortcuts, overestimate completion, or declare success without verifiable evidence.

---

## Main Original Ideas

1. **Goal as Contract, Not Prompt** -- Replace open-ended prompts with a structured goal: desired end state, evidence required to prove success, constraints that must not be violated, and a turn/time budget. Weak goals let models redefine success in the transcript; strong goals give measurable targets the agent checks itself against. The human still decides what "done" means.

2. **Evaluator as First-Class Component** -- Long-running agents require a separate evaluator role (another agent, LLM-as-judge, test suite, benchmark harness, or a mix). Deterministic checks (tests, type checks, lint, benchmarks) serve as the floor; agent-based evaluation handles fuzzy success criteria like design fidelity, report coherence, or paper faithfulness. The two layers together reduce hallucinated success.

3. **Verifiers as the Trust Boundary** -- Autonomy only works if the system has a reliable external verifier -- something the agent cannot talk its way around. Verifiers include test suites, type checkers, benchmarks, browser runs, screenshot comparisons, and reproducible scripts. A vague verifier leads to the model satisfying the easiest interpretation; a narrow verifier leads to overfitting. Layered verification (cheap deterministic + higher-level review) is the correct pattern. Verifiers remain an open research area; fine-tuned verifiers are in high enterprise demand.

4. **The Loop as Outer Control System** -- A goal gives direction; a loop keeps work alive. The loop wakes up, inspects progress, runs checks, compares against the goal, and re-sends the agent with the next instruction if the goal is unmet. The Ralph loop is the simplest form (deterministic condition + agent); a more flexible form uses an evaluator agent to reason about progress. Long-running autonomy = repeated effort under supervision, not one continuous act of intelligence.

5. **Model Choice as Architecture** -- Planning and execution should be separated across different models. Stronger models define goals, identify missing constraints, and structure evaluation; cheaper/faster models execute once the plan is clear. Vision-capable models handle UI review. "The model" is not a single choice -- it is an architecture decision with swappable roles.

6. **Session Mining as Workflow Memory** -- Past agent session transcripts contain recurring failure patterns (same check forgotten, wrong path, broken retry). Mining those sessions to produce project instruction updates turns historical mistakes into operating rules -- incrementally improving the harness without retraining a model.

7. **Visual Artifacts as Control Surfaces** -- Terminal transcripts don't scale when multiple agents run in parallel. Dashboards with loss curves, benchmark scores, task states, screenshots, and cost estimates give humans a better supervision interface. The recommended pattern: Markdown/vault for durable evidence (agent-readable), HTML artifacts for visual rendering (human-readable).

---

## Key Findings

- Models still take shortcuts, stop early, overestimate completion, and produce confident but weak plans -- especially on recent papers, unfamiliar benchmarks, or out-of-distribution systems
- The OOD problem for verification is real: assigning verification tasks outside the model's training distribution causes significant performance degradation
- The strongest planning models are not always the best execution models -- splitting these roles improves overall system reliability
- Visual artifacts (screenshot references + vision-capable evaluators) are especially effective for UI/product work where prose cannot fully specify design intent
- Most failure modes occur at the verifier boundary: vague verifiers → model satisfies easiest interpretation; narrow verifiers → model overfits and misses broader intent

---

## Suggestions & Future Directions

1. **Invest heavily in verifiers** -- described as an open research area where companies will make large investments; fine-tuned verifiers are in high enterprise demand
2. **Promote session-mined lessons to project instructions** automatically -- small rules in agent instruction files prevent repeated failures across future sessions
3. **Build multi-model orchestrators** -- rather than waiting for a single vendor to provide the perfect coding agent interface, design systems that swap planning/execution/evaluation/vision models based on task type
4. **Separate storage from presentation** -- Markdown for agent-readable durable state; HTML artifacts for human-readable monitoring -- to enable parallel agent supervision at scale
5. The author's implicit research direction: bridging the gap between "using a coding agent" (conversation) and "engineering an autonomous coding system" (harness with goals, loops, evaluators, artifacts, and memory)

---

## Authors & Institutions

Elvis Saravia (@omarsar0) -- DAIR.AI (founder/researcher); article based on DAIR.AI Academy session, written in collaboration with Codex and Claude Code
