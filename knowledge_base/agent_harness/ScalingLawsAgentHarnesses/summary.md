# Scaling Laws for Agent Harnesses Via Effective Feedback Compute

**Paper:** [Scaling Laws for Agent Harnesses Via Effective Feedback Compute (Zhang et al., 2026)](https://arxiv.org/abs/2605.29682)

## Human Readable TL;DR

Imagine two students taking the same exam with the same amount of study time. One spends it re-reading the same pages repeatedly; the other tackles new practice problems, understands mistakes, and updates their notes. They both "studied equally long," but only one improves. This paper shows AI agents work the same way: what matters isn't how much computation they spend -- it's whether that computation produces useful, new, retained learning from the environment. The authors invent a score called EFC to measure this "useful feedback," and prove it predicts agent success far better than simply counting tokens or tool calls.

## TL;DR

This paper introduces Effective Feedback Compute (EFC), a trace-level scalar that credits agent feedback only when it is informative, valid, non-redundant, and retained for future decisions. Normalized by task demand (EFC/D_task), it consistently outperforms raw-compute baselines (tokens, tool calls, cost) and a strong multivariate SAS baseline across synthetic, executable code, real benchmark, held-out, and prospective validation settings. Oracle-EFC/D_task achieves R² = 0.99 on controlled tasks; NRS-EFC/D_task achieves R² = 0.92 on real mixed traces and R² = 0.85 on a prospective holdout where raw compute scores negative R².

---

## Problem & Motivation

Agent harnesses -- the scaffolding that orchestrates tool calls, feedback reception, memory, verification, and error repair -- increasingly determine LLM system performance. Yet current test-time scaling analyses measure resource usage through raw metrics like tokens, tool calls, or wall time. These metrics do not distinguish useful feedback from redundant or unstable interaction: two trajectories with identical raw compute can yield drastically different outcomes. The paper asks: **what scalar should serve as the scaling coordinate for closed-loop agent harness performance?**

---

## Main Original Ideas

1. **Effective Feedback Compute (EFC)** -- A multiplicative, event-level measure: `EFC_t = κ · I_t · V_t · R_t · M_t` (κ = 10), where each factor is bounded [0, 1]:
   - *Informativeness* (I): reveals task-relevant info (new constraint, subgoal progress)
   - *Validity* (V): grounded in reliable evidence (deterministic checker, unit test result)
   - *Non-redundant relevance* (R): addresses active subgoal and adds new information
   - *Memory update* (M): changes plan/state/memory to affect future actions
   Run-level EFC sums over all feedback events. The multiplicative form creates a bottleneck: a weak score on any single factor collapses the event's contribution.

2. **Task-Demand Normalization (D_task)** -- `D_task = L · H_tool · S_state · (1 + N_obs) · (1 − V_oracle)` captures reasoning depth, tool selection ambiguity, state-tracking demand, observation noise, and verifier coverage. Normalizing by D_task collapses failure curves across heterogeneous task families and is especially critical for mixed holdouts.

3. **Harness Efficiency (η = EFC / C_raw)** -- Measures how effectively a harness converts raw budget into useful feedback. Factor ablations show η explains 97% of success variation (R² = 0.97) while raw cost explains ~1% (R² = 0.01), localizing performance gains to the raw-to-EFC conversion mechanism.

4. **Estimated-EFC and NRS-EFC** -- Since oracle hidden state is unavailable in real settings:
   - *Estimated-EFC*: trained from trace-observable signals (checker activity, tool-result references, plan updates, memory retention, error avoidance, subgoal progress) on synthetic data then transferred.
   - *NRS-EFC* (Non-Redundant Stable EFC): applies status-aware discounting and stronger penalties for repeated failures on noisy real traces, emphasizing retained over transient feedback.

---

## Key Findings

| Predictor | Controlled R² | Held-out R² | Real Traces R² | Prospective R² |
|---|---|---|---|---|
| Raw tokens | 0.33 | 0.44 | -0.08 | -0.11 |
| Tool calls | 0.42 | 0.68 | -0.02 | -0.04 |
| SAS (multivariate) | 0.88 | 0.86 | 0.43 | 0.26 |
| Oracle-EFC | 0.94 | 0.88 | -- | -- |
| Estimated-EFC | 0.94 | 0.86 | -- | -- |
| Oracle-EFC/D_task | **0.99** | **0.95** | -- | -- |
| NRS-EFC | -- | -- | 0.89 | 0.77 |
| **NRS-EFC/D_task** | -- | -- | **0.92** | **0.85** |

- **Matched-budget intervention**: With raw cost and tool-call budgets held exactly equal, switching from low- to high-quality feedback raises success from **0.27 to 0.90** (p < 10⁻³⁰⁰), ruling out raw compute as the causal driver.
- **Module ablations**: Harness efficiency (η) explains 97% of success variation; raw cost explains ~1%. Stronger verifiers, better routers, and higher memory fidelity all increase η and success.
- **Slice-specific η**: On HumanEval, H5/H6 achieve η ≈ 1.9; on Terminal tasks all harnesses plateau at η ≈ 0.1; on SWE tasks, earlier harnesses (H0, H3) outperform deep closed-loop ones -- η is a harness--task interaction, not a fixed harness property.
- **Task-demand calibration transfer**: Fitted D_task exponents beat hand-designed D_task on heterogeneous holdout (R² = 0.83 vs. 0.53, MAE 0.10 vs. 0.19).

---

## Suggestions & Future Directions

1. **Extend EFC estimation to open-ended environments** -- Current calibration relies on structured task families; broader web/multi-modal environments need new trace-observable estimation strategies.
2. **Improve task-demand calibration** -- Fitted D_task exponents require a calibration split that may not always be available; more principled methods could reduce this dependency.
3. **Use EFC as an adaptive budget allocation objective** -- Real-time EFC monitoring could guide decisions about when to continue spending compute vs. stop, replacing rigid budget limits.
4. **Use EFC for automated harness design** -- EFC/D_task provides a signal for harness optimization loops, replacing binary task pass/fail as the training objective.
5. **Investigate slice-specific η to guide harness selection** -- The harness--task interaction pattern suggests principled matching of harness type to task environment based on predicted η.

---

## Authors & Institutions

Xuanliang Zhang, Dingzirui Wang, Keyan Xu, Qingfu Zhu, Wanxiang Che -- Harbin Institute of Technology
