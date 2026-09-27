# Towards a Science of AI Agent Reliability

**Paper:** [Towards a Science of AI Agent Reliability (Rabanser, Kapoor, Kirgis, Liu, Utpala, Narayanan, 2026)](https://arxiv.org/abs/2602.16666)

## Human Readable TL;DR

Imagine hiring a contractor who can successfully do 90% of jobs you give them -- but you can never predict which 10% they'll fail at, and sometimes they accidentally flood your bathroom while fixing a leaky faucet. Today's AI assistants are graded mostly by "how often do they succeed?" but not by whether they behave the same way twice, how they handle surprises, whether they know when they're about to make a mistake, or how bad the mistakes can get. This paper creates a report card with twelve specific measures across four categories -- borrowed from industries like aviation and nuclear power that have built reliable systems for decades. When they tested 15 AI models, they found that while models have gotten much smarter over two years, they haven't gotten much more reliable.

## TL;DR

This paper proposes a formal reliability framework for AI agents, decomposing reliability into four dimensions -- consistency, robustness, predictability, and safety -- with 12 concrete metrics adapted from safety-critical engineering. Evaluating 15 frontier models (OpenAI, Google, Anthropic) across GAIA and τ-bench, the authors find that 24 months of rapid capability gains have yielded only modest reliability improvements, with consistency and predictability discrimination lagging most significantly, while calibration and safety show some progress.

---

## Problem & Motivation

AI agents are being deployed for consequential real-world tasks (code modification, database management, web browsing), but current evaluations rely on mean task success rates as the primary metric. This single-metric approach hides critical behavioral properties: whether an agent behaves consistently across runs, degrades gracefully under perturbations, recognizes its own failure likelihood, or bounds error severity. High-profile failures -- Replit's AI deleting a production database, OpenAI Operator making unauthorized purchases, an NYC chatbot giving illegal business advice -- demonstrate the gap between benchmark performance and real-world reliability. The paper asks: "How should we define and evaluate agent reliability?"

---

## Main Original Ideas

1. **Four-Dimensional Reliability Taxonomy:** Adapted from aviation, nuclear, automotive, and industrial process control standards, the authors decompose agent reliability into: Consistency (repeatable behavior across runs), Robustness (stable performance under perturbations), Predictability (calibrated confidence aligned with actual success), and Safety (bounded error severity when failures occur).

2. **Twelve Capability-Independent Metrics:** The framework proposes 12 concrete metrics designed to be independent of raw accuracy:
   - *Consistency:* C_out (outcome), C_d_traj (distributional trajectory), C_s_traj (sequential trajectory), C_res (resource)
   - *Robustness:* R_fault (infrastructure failures), R_env (environment changes), R_prompt (instruction rephrasings)
   - *Predictability:* P_cal (calibration), P_AUROC (discrimination), P_brier (joint score)
   - *Safety:* S_comp (constraint compliance), S_harm (violation severity)
   Overall score R averages the first three dimensions; Safety is reported separately as a hard constraint.

3. **Capability-Reliability Disentanglement:** Metrics are normalized to decouple reliability from raw capability -- e.g., C_out normalizes variance by the maximum possible variance at a given success rate; robustness uses accuracy ratios between perturbed and nominal conditions.

4. **Reliability as an Independent Evaluation Axis:** The paper advocates shifting from "How often does the agent succeed?" to "How predictably, consistently, robustly, and safely does it behave?" -- establishing reliability as a distinct progress axis requiring targeted optimization, not just a byproduct of scaling capability.

---

## Key Findings

| Dimension | GAIA trend | τ-bench trend | Notable pattern |
|---|---|---|---|
| **Consistency** | Low, flat | Low, modest gain | C_out low across all models |
| **Robustness** | Ceiling (fault/env); prompt varies | Similar | Prompt robustness key differentiator |
| **Predictability** | Calibration ↑, discrimination flat/↓ | Both improving | Divergent benchmark trends |
| **Safety** | N/A | Improving in frontier | Fin. accuracy most common violation |

- **Reliability lags capability:** Overall reliability slope on GAIA is 0.03/yr vs. accuracy slope of 0.18 -- a 6× gap
- **Consistency crisis:** Outcome consistency (C_out) remains low across all models; agents capable of a task often fail to solve it consistently across 5 independent runs
- **"What but not when" pattern:** Agents reliably choose similar action *types* (high C_d_traj) but vary in execution *order* (low C_s_traj), indicating unstable planning
- **Counterintuitive robustness:** Models handle genuine infrastructure failures gracefully but remain brittle to superficial instruction rephrasings
- **Calibration vs. discrimination split:** Calibration has improved (especially Claude models), but discrimination -- predicting *which specific tasks* will fail -- has stagnated or worsened on GAIA
- **Safety improving but not solved:** Recent frontier models show lower violation rates; financial accuracy errors (incorrect charges/refunds) are the most prevalent failure mode on τ-bench
- **Reliability is an industry-wide plateau:** All three frontier providers cluster similarly, ruling out vendor-specific explanations

---

## Suggestions & Future Directions

1. **Dynamic, generative benchmarks:** Move beyond single-run accuracy to multi-run protocols with systematic perturbations, parameterized environments (rename fields, inject faults), and temporal re-evaluation
2. **Architecture-level reliability optimization:** Explicitly design agent systems to target consistency and discrimination -- the dimensions showing the least natural improvement
3. **Deployment governance frameworks:** Establish minimum reliability thresholds before promoting agents from sandboxed pilots to production, analogous to aviation certification requirements
4. **Autonomy-scaled requirements:** Apply stricter reliability standards for fully autonomous deployments vs. augmentation settings where humans serve as a reliability backstop
5. **Multi-agent reliability:** Model how errors propagate and compound across agents in multi-agent pipelines
6. **Online monitoring:** Develop online signals that predict reliability failures before they manifest, enabling proactive intervention
7. **Formal operational envelopes:** Develop formal failure semantics, task distributions, and exposure models for agents -- the groundwork that safety-critical standards (IEC 61508, DO-178C) eventually required

---

## Authors & Institutions

Stephan Rabanser, Sayash Kapoor, Peter Kirgis, Kangheng Liu, Saiteja Utpala, Arvind Narayanan -- Princeton University (Princeton Language and Intelligence, Princeton AI Lab). Published at ICML 2026.
