# Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents

**Paper:** [Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents (Anh Ta, Junjie Zhu, Shahin Shayandeh, 2026)](https://arxiv.org/abs/2604.27233)

## Human Readable TL;DR

Imagine an AI assistant that can order things online on your behalf -- but before actually clicking "buy", a careful supervisor reviews the order to make sure it got everything right. That's the core idea here: a second AI "reviewer" checks every action an AI agent is about to take before anything is actually done. This catches mistakes before they cause problems, rather than scrambling to undo things afterward. The researchers measured both how often the reviewer helped versus how often it accidentally made things worse -- and found a smart reviewer can be 3x more helpful than harmful.

## TL;DR

This paper introduces a duo-agent architecture where a specialized **reviewer agent** evaluates provisional tool calls from a primary **tool-calling agent** before execution, shifting error correction from post-hoc recovery to proactive inference-time mitigation. The system is evaluated on BFCL (single-turn) and τ²-Bench (multi-turn), achieving +5.5% on irrelevance detection and +7.1% on multi-turn tasks. Novel Helpfulness-Harmfulness metrics quantify the net benefit of feedback, showing reasoning models (o3-mini) achieve a 3.1:1 benefit-to-risk ratio vs. 2.7:1 for GPT-4o. Automated prompt optimization via GEPA adds another +1.5--2.8% with no base agent retraining.

---

## Problem & Motivation

Tool-calling agents face three systematic failure modes: selecting the wrong tool, constructing calls with incorrect parameters, and failing to recognize when no tool applies. Existing fixes are either (1) training-based (GRPO) -- expensive, slow to deploy -- or (2) inference-time self-reflection (Self-Refine, Reflexion) -- but these require the agent to maintain and revert prior states, a "state recovery problem" that becomes prohibitively expensive in multi-turn scenarios as trajectories grow exponentially. The core gap: LLM trajectory assessments are inherently post-hoc and cannot course-correct an agent in real time.

---

## Main Original Ideas

1. **Inference-Time Reviewer Agent** -- A separate, specialized agent evaluates provisional tool calls *before* they are executed. This decouples execution from review, preventing destructive errors without needing state rollback.

2. **Three Collaboration Mechanisms** -- (a) *Progressive Feedback (rN)*: iterative review-refine loops up to N iterations; (b) *Best-of-N Selection (sN)*: N candidates generated, reviewer picks best; (c) *Best-of-N Grading (gN)*: reviewer scores each candidate 0--1 and highest wins.

3. **Helpfulness-Harmfulness Metrics** -- Novel pair of metrics: *Helpfulness* = % of base-agent errors the reviewer corrects; *Harmfulness* = % of correct base-agent responses the reviewer degrades. Their ratio (benefit-to-risk) quantifies net reviewer value -- the first systematic framework for this trade-off.

4. **GEPA-Based Automated Prompt Optimization (APO)** -- Reviewer prompts are iteratively evolved using a genetic-pareto strategy: collect failure cases → LLM reflects → propose improved prompts → repeat until convergence. Applied without touching the base agent.

---

## Key Findings

| Configuration | BFCL Relevance | BFCL Irrelevance | τ²-Bench Avg |
|---|---|---|---|
| Baseline (GPT-4o only) | 90.9% | 84.9% | 48.7% |
| + o3-mini reviewer, v1 prompt | ~91% | ~89.6% | -- |
| + o3-mini reviewer, v2 prompt (manual) | **92.5%** | **90.4%** | **55.8%** |
| + GPT-5 mini reviewer, GEPA v3 prompt | **94.0%** | **93.2%** | -- |

- Reasoning models (o3-mini, GPT-5 mini) are significantly better reviewers than standard GPT-4o: **3.1:1 vs. 2.7:1** benefit-to-risk ratio.
- Progressive Feedback (rN) outperforms Best-of-N for iterative tasks like irrelevance detection; Best-of-N is simpler but less effective.
- GEPA-optimized prompts (v3, 1,599 tokens) beat manual v2 (358 tokens) by +1.5% relevance, +2.8% irrelevance; largest gains on `parallel_multiple` (+2.1%).
- Reviewer "over-skepticism" is the dominant failure mode: reviewer incorrectly flags valid calls expecting user-facing dialogue or execution results -- fixed by explicit prompt guidelines.
- BFCL-optimized prompts do **not** transfer to τ²-Bench; domain-specific adaptation is required.
- **Latency**: single-turn overhead 6.2x (1.27s → 7.87s); multi-turn overhead 2.4x (158.7s → 384.3s) -- amortized across ~40 turns per episode.

---

## Suggestions & Future Directions

1. **Distill the reviewer** into a lightweight reward model or classifier to reduce the 6.2x latency cost for single-turn, high-volume deployments.
2. **Extend APO to τ²-Bench** -- automated prompt optimization was only validated on BFCL; applying it to multi-turn contexts is the natural next step.
3. **Selective feedback** -- apply the reviewer only to high-uncertainty or high-stakes tool calls rather than uniformly, to better manage latency.
4. **On-device deployment** -- distilled reviewer models could enable inference-time feedback in latency-sensitive or privacy-sensitive edge deployments.
5. **Generalize metrics** -- apply Helpfulness-Harmfulness framework to other multi-agent feedback paradigms beyond tool calling.

---

## Authors & Institutions

Anh Ta (Apple), Junjie Zhu (Apple), Shahin Shayandeh (Apple)
