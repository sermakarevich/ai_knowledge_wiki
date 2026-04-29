# How Much LLM Does a Self-Revising Agent Actually Need? Empirical Decomposition of World Modeling, Reflection, and Sparse LLM Revision

**Paper:** [How Much LLM Does a Self-Revising Agent Actually Need? (Jeong & Son, 2025)](https://arxiv.org/abs/2604.07236)

## Human Readable TL;DR

Imagine you hire an expensive consultant (the LLM) to run your entire business. This paper asks: what if you first set up clear rules, checklists, and self-correction procedures yourself -- how much do you actually still need that consultant? The authors built agents that play a battleship-like game and systematically stripped away the AI's involvement, replacing it with explicit rules and logic. They found that having a clear plan and strategy mattered most, that a basic self-check system worked on its own without AI, and that calling on the AI for occasional advice only helped a tiny bit -- and sometimes even hurt. The takeaway: build the structure first, and only call on the expensive AI brain for the parts you genuinely can't handle with straightforward logic.

## TL;DR

This paper introduces a declared reflective runtime protocol that decomposes LLM agent competence into four measurable layers: belief tracking, explicit world-model planning, symbolic reflection, and sparse LLM revision. Evaluated on noisy Collaborative Battleship, explicit world-model planning yielded the largest gain (+24.1pp win rate), symbolic self-revision functioned as a runtime mechanism but was not net-positive in aggregate, and sparse LLM intervention (invoked on ~4.3% of turns) produced small, non-monotonic effects -- suggesting the LLM's marginal contribution is bounded once structure is externalized.

---

## Problem & Motivation

Current LLM agent architectures (ReAct, Reflexion, etc.) bundle world modeling, planning, and reflection inside a single LLM loop. This entanglement makes it impossible to determine which parts of agent competence actually come from the LLM versus the explicit computational structures surrounding it. The paper asks: if you systematically externalize these capabilities into inspectable, declared runtime components, what measurable contribution remains for the LLM? The goal is not a new SOTA but a methodological framework that makes this question empirically tractable.

---

## Main Original Ideas

1. **Declared Reflective Runtime Protocol** -- A protocol that externalizes agent state, confidence signals, guarded actions, and hypothetical transitions into an inspectable runtime structure. Reflection becomes a declared legality structure (with variables like `modelConfidence`, `needRevision`, `shouldRevise`) rather than an opaque prompt pattern.

2. **Four-Layer Empirical Decomposition** -- Agent competence is decomposed into posterior belief tracking, explicit world-model planning, symbolic in-episode reflection, and sparse LLM revision. Each layer is isolated and measured independently via a family of four progressively complex agents.

3. **Symbolic Metacognition Without LLM** -- The Metacognitive Reflective Agent (MRA) implements a full predict-compare-revise loop using three symbolic revision presets (`coarse roi collapse`, `late diffuse reprobe`, `cluster closeout bias`) entirely within the declared runtime, with zero LLM calls.

4. **LLM as Conditional Residual Resource** -- Rather than embedding the LLM in every decision, it is gated behind confidence thresholds and invoked only when the declared substrate cannot resolve a situation -- making its invocation rate a measurable dependent variable.

---

## Key Findings

| Agent | Avg F1 | Win Rate | Avg Questions | LLM Rate |
|---|---|---|---|---|
| greedy+MCMC (baseline) | 0.522 | 50.0% | 0.0 | 0% |
| **WMA (World-Model Agent)** | **0.539** | **74.1%** | **11.9** | **0%** |
| MRA revision-off | 0.552 | 57.4% | 8.0 | 0% |
| MRA revision-on | 0.551 | 55.6% | 8.0 | 0% |
| MRA-LLM (th=0.0) | 0.552 | 57.4% | 8.0 | 0% |
| MRA-LLM (th=1.0) | 0.557 | 53.7% | 8.9 | 4.3% |

- **Explicit planning dominates:** WMA's +24.1pp win rate gain over the baseline is the single largest improvement, driven by strategically timed questions evaluated via `sim.next()`.
- **F1 vs. win rate divergence:** LLM revision improved local targeting (highest F1 at 0.557) but hurt win rate (lowest at 53.7%), suggesting LLM turns displace strategically valuable question turns.
- **Symbolic reflection is functional but uncalibrated:** On specific boards (e.g., B17-seed0), symbolic revision was decisive (F1 0.609 vs. 0.333 without it), but aggregate performance was slightly negative (-1.8pp win rate), indicating preset calibration is the bottleneck.
- **LLM contribution is sparse and non-monotonic:** At 4.3% invocation rate, the 9B LLM produced marginal, non-monotonic effects -- more LLM access did not consistently improve outcomes.

---

## Suggestions & Future Directions

1. **Calibrate symbolic revision presets** -- The current three presets are hand-designed; data-driven calibration could convert symbolic reflection from net-neutral to net-positive.
2. **Expand evaluation domains** -- The protocol was tested only on noisy Collaborative Battleship; validating it across diverse environments would test generality.
3. **Characterize LLM benefits at scale** -- Preliminary threshold sweeps suggest non-monotonic patterns that may shift with larger evaluation suites and different LLM sizes.
4. **Design principle proposed:** "Declare what you can, reflect symbolically where possible, and reserve the LLM for the residual that the declared substrate cannot resolve" -- the paper provides instrumentation to empirically determine where LLM intervention is justified.
5. **Investigate F1/win-rate tension** -- Understanding how LLM revision interacts with question budget allocation could inform better integration strategies.

---

## Authors & Institutions

Seongwoo Jeong (Independent Researcher), Seonil Son (RLWRLD.AI, Seoul, South Korea)
