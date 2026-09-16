# Self-Harness: Harnesses That Improve Themselves

**Paper:** [Self-Harness: Harnesses That Improve Themselves (Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, Shuyue Hu, 2026)](https://arxiv.org/abs/2606.09498)

## Human Readable TL;DR

Imagine you hired a new employee, but instead of you teaching them better work habits, they watch recordings of their own mistakes and figure out better rules for themselves -- without anyone else's help. That's essentially what this paper builds for AI agents: a system where the agent's operating instructions automatically fix themselves by studying where the agent keeps failing, proposing small rule changes, and checking that the changes actually help before keeping them.

## TL;DR

Self-Harness introduces a three-stage iterative loop (Weakness Mining → Harness Proposal → Proposal Validation) that enables a fixed LLM to autonomously improve its own execution harness -- the non-parametric scaffolding of prompts and tool configurations that governs its behavior. Applied to Terminal-Bench-2.0 across three models, pass rates improved by 14--21 percentage points without any human engineering or stronger external model.

---

## Problem & Motivation

LLM-based agents are increasingly deployed with a fixed "harness" -- a scaffold of system prompts, tool definitions, and execution rules that shapes behavior without changing model weights. These harnesses require significant human engineering and become stale as models diversify. Existing improvement methods either require human labor, access to stronger teacher models, or modify weights directly. The paper addresses the gap: can a fixed model improve its own harness autonomously, using only its own execution traces as evidence?

---

## Main Original Ideas

1. **Self-improving harness loop** -- The core contribution is a closed-loop system where the same model serves both as the agent-under-test and as the proposer of harness improvements. No stronger model or human is required at any stage.

2. **Weakness Mining via failure clustering** -- Rather than treating each failed task independently, the system clusters failed execution traces by verifier-grounded failure signatures to identify recurring, actionable failure patterns. This creates structured evidence bundles that pinpoint systemic weaknesses rather than one-off errors.

3. **Minimal, targeted harness proposals** -- The proposer generates K diverse candidate edits, each materially distinct and minimally scoped to address a specific failure mechanism. Proposals include an audit record describing the targeted pattern and expected effect, preventing diffuse or contradictory modifications.

4. **Regression-gated acceptance** -- A candidate edit is accepted only when it improves both the held-in split (which provided the failure evidence) and the held-out split (regression test), with `Δin ≥ 0 AND Δho ≥ 0 AND max(Δin, Δho) > 0`. This prevents overfitting to observed failures and ensures generalization.

5. **Model-specific harness adaptation** -- The same framework produces qualitatively different harness changes for different model families, reflecting their distinct failure modes (e.g., Qwen3.5 needed dependency pre-checking; GLM-5 needed persistent environment state across shell commands).

---

## Key Findings

| Model | Initial Pass (%) | Final Pass (%) | Absolute Gain | Relative Gain |
|---|---|---|---|---|
| MiniMax M2.5 | 40.5 | **61.9** | +21.4 pp | +53% |
| Qwen3.5-35B-A3B | 23.8 | **38.1** | +14.3 pp | +60% |
| GLM-5 | 42.9 | **57.1** | +14.2 pp | +33% |

- All improvements held on both held-in and held-out splits -- no regression cases observed.
- Accepted edits show targeted behavioral changes matching diagnosed failure mechanisms, not generic instruction bloat.
- The approach is compute-light: the same fixed model performs all roles (agent, failure analyst, proposer, validator).
- Model-specific divergence in accepted edits confirms the method surfaces genuine per-model weaknesses rather than generic patterns.

---

## Suggestions & Future Directions

1. **Open-ended improvement beyond benchmarks** -- Current work studies bounded edits under fixed benchmarks; extending to open-ended task distributions is a key next step.
2. **Stronger acceptance gates** -- Higher-stakes deployments may require more conservative validation criteria or human-in-the-loop review before accepting edits.
3. **Evaluator quality dependency** -- The method's effectiveness is bounded by the quality of the verifier and trace recorder; improving these components is a prerequisite for broader deployment.
4. **Generalization verification** -- Results may partially reflect benchmark-specific patterns; cross-benchmark transfer experiments are needed to confirm generalizability.
5. **Scaling to more capable models** -- All tested models are mid-tier; behavior on frontier models (where initial harnesses may already be near-optimal) remains an open question.

---

## Authors & Institutions

Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, Shuyue Hu
