# Self-Harness: Harnesses That Improve Themselves

**Paper:** [Self-Harness: Harnesses That Improve Themselves (Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, Shuyue Hu, 2026)](https://arxiv.org/abs/2606.09498)

## Human Readable TL;DR

Think of an AI assistant that comes with an instruction manual someone wrote for it. Over time, as the assistant struggles with certain tasks, it reads its own instruction manual, figures out which parts are causing problems, rewrites those sections itself, and tests whether the new version works better — all without asking anyone for help. Self-Harness is exactly that: a system where the AI agent improves its own operating instructions through trial, observation, and revision.

## TL;DR

Self-Harness is a closed-loop framework that allows LLM-based agents to autonomously improve the "harnesses" (system prompts, tool configurations, and middleware) that govern their behavior. The method operates through three iterative stages: mining failure patterns from execution traces, proposing targeted harness modifications, and validating candidates with a regression-safe acceptance rule. Applied to three diverse models on Terminal-Bench-2.0, it yields absolute pass-rate gains of 7--21 percentage points with up to 138% relative improvement, producing model-specific yet broadly generalizing harness edits.

---

## Problem & Motivation

LLM-based agents are increasingly deployed through "harnesses" -- structured system prompts, tool definitions, and middleware layers that mediate agent-environment interaction. Today these harnesses are hand-crafted by human engineers, creating two problems: the engineering effort does not scale across diverse model families, and fixed harnesses cannot adapt as models and task distributions evolve.

Existing alternatives either rely on stronger external optimizer models (which introduces a capability ceiling and governance questions) or require large offline datasets. Self-Harness addresses this by showing that the same fixed model can propose and validate its own bounded harness improvements using only its own execution traces as evidence -- no stronger model, no human feedback required.

---

## Main Original Ideas

1. **Verifier-Grounded Failure Signatures** -- Rather than treating individual task failures independently, the framework clusters failed execution traces by a structured signature: (terminal failure cause, agent behavior status, exposed mechanism). This surfaces recurring behavioral patterns rather than task-specific noise.

2. **Evidence Bundle Construction** -- Clustered failure signatures are assembled into evidence bundles that the model receives alongside the editable harness surfaces. This grounds proposals in concrete behavioral evidence and prevents hallucinated or generic "instruction padding."

3. **Diversity-Constrained Proposal Generation** -- The model generates K candidate harness modifications that are mutually diverse (targeting different failure mechanisms) yet individually minimal (smallest change that addresses the targeted pattern). Each proposal carries an audit record: targeted failure pattern, modified surfaces, expected effect, and regression risks.

4. **Conservative Dual-Split Acceptance Rule** -- A candidate is accepted only if Δ\_in ≥ 0, Δ\_ho ≥ 0, and max(Δ\_in, Δ\_ho) > 0, where "in" and "ho" refer to held-in and held-out task splits. This prevents harnesses from overfitting to observed failures at the cost of unseen task performance.

5. **Model-Specific Harness Evolution** -- The framework produces fundamentally different accepted edits for each model family, reflecting distinct behavioral failure modes rather than generic improvements. MiniMax received artifact-creation discipline; Qwen3.5 received dependency prechecking and loop-breaking middleware; GLM-5 received environment-persistence and phase-transition logic.

---

## Key Findings

| Model | Initial Held-in | Final Held-in | Initial Held-out | Final Held-out | Max Rel. Gain |
|---|---|---|---|---|---|
| MiniMax M2.5 | 43.0% | 50.0% | 40.5% | 61.9% | +53% |
| Qwen3.5-35B-A3B | 15.1% | 36.0% | 23.8% | 38.1% | +138% |
| GLM-5 | 47.7% | 57.0% | 42.9% | 57.1% | +33% |

- All final harnesses improved both held-in and held-out pass rates simultaneously, confirming genuine generalization rather than benchmark-specific overfitting.
- Accepted edit counts were modest (3--4 per model), indicating the acceptance rule effectively filters candidates.
- Trace-level case studies confirm behavioral change: MiniMax shifted from prolonged exploration to concrete artifact-creation workflows; Qwen3.5 reduced repeated ineffective tool calls; GLM-5 improved environment-state management.
- Discarded proposal branches were common (early subagent and skill-extension branches for Qwen3.5 were abandoned as unpromising), showing the validation gate catches regressions.
- Self-Harness operates with a fixed single model -- no stronger oracle or external optimizer is needed.

---

## Suggestions & Future Directions

1. **Stronger acceptance criteria for higher-stakes edits** -- The current non-regression rule on pass rates is appropriate for bounded edits; the authors note that larger structural changes would require richer criteria (e.g., safety, latency, resource constraints).

2. **Open-ended self-improvement** -- The current study bounds harness edits; removing that bound and studying long-horizon self-modification with appropriate guardrails is an open problem.

3. **Multi-agent harness refinement** -- Exploring whether collaborative groups of agents can jointly improve shared harnesses more efficiently than single-agent loops.

4. **Multimodal task coverage** -- The initial harness excluded multimodal tasks; extending the framework to vision-action agents is a natural next step.

5. **Cross-benchmark generalization** -- Accepted edits may reflect Terminal-Bench-2.0-specific patterns; testing whether evolved harnesses transfer to other benchmarks would validate broader applicability.

6. **Verifier quality dependence** -- Improvement depends on the quality and granularity of task verifiers; developing richer verifier signals (partial credit, intermediate state) could enable finer-grained harness optimization.

---

## Authors & Institutions

Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, Shuyue Hu
