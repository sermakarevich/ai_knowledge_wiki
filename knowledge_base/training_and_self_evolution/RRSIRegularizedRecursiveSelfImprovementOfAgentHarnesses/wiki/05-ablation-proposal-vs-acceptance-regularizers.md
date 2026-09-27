> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Ablation: Proposal vs Acceptance Regularizers, Transfer, Cost, and Conclusions
**In one sentence:** Removing proposal constraints costs little on the evolve split but 1.7 points out of distribution, removing both regularizers maximizes evolve score (92.8) while collapsing OOD transfer, and the full RRSI harness still transfers across policy families and to a weaker unseen backbone while remaining the lightest evolved harness.
## Key points
- Removing proposal constraints alone costs only 0.2 points on the evolve split but 1.7 points out of distribution, showing steering where search looks matters even when nothing is rejected.
- Removing both regularizers lifts the evolve-set score to 92.8 (highest of any arm) but leaves OOD average at 40.3, within a point of the unevolved harness, at 3.80M tokens per trial vs 2.42M for RRSI.
- Under Gemini 3.5 Flash, RRSI improves Terminal-Bench 2.1 from 64.6 to 78.7 (+14.1) and transfers +2.2 to SWE-bench Verified; under Claude Opus 4.8, Terminal-Bench 2.1 rises 74.2 to 80.2 and SWE-bench Verified 82.0 to 83.8.
- The Gemini 3.5 Flash–evolved coding harness run unchanged on unseen Gemini 3.1 Flash Lite rises 11.2 to 14.6 (+3.4, 30.4% relative) despite a base score less than a fifth of the search policy's.
- RRSI is the lightest evolved harness via two cost regularizers: an L1-style budget refusing unpaid growth at proposal time and a pruning rule removing growth that stopped paying since.
- AHE is the extreme cost case at 3.82M tokens per trial, 58% more than RRSI, for 4.4 points less OOD; RRSI runs 26.3 steps per trial vs 27.3–34.6 for prior methods, while unevolved H0 costs 1.56M tokens and 21.2 steps.
- RRSI regularizes search dynamics (full-history credit, task-specific-logic filtering, noise-adjusted acceptance) with an open edit space, and its conclusion holds that RSI requires controlling how feedback becomes persistent change, with limits around frozen backbones, finite evolve sets, and hyperparameters.
---
## Ablation: proposal vs acceptance regularizers
Removing the proposal constraints costs only 0.2 points on the evolve split but 1.7 out of distribution, "suggesting that steering where the search looks matters even when nothing is rejected."
The most significant degradation comes from removing both, which "lifts the evolve-set score to 92.8, the highest of any arm, and leaves the out-of-distribution average at 40.3, within a point of the unevolved harness, at 3.80 million tokens per trial against our 2.42."
**Covers:** ablation of proposal constraints vs both regularizers
## Cross-policy evolution: not tied to one backbone
RRSI is "not tied to one policy family": the coding evolution is run independently with Claude Opus 4.8 and Gemini 3.5 Flash, starting from the same coding harness, evolving only on Terminal-Bench 2.1, and evaluating on both the evolve benchmark and SWE-bench Verified.
Under Gemini 3.5 Flash, RRSI improves Terminal-Bench 2.1 from 64.6 to 78.7 and transfers a 2.2-point gain to SWE-bench Verified; under Claude Opus 4.8, Terminal-Bench 2.1 rises from 74.2 to 80.2 and SWE-bench Verified from 82.0 to 83.8, "although the stronger policy starts closer to the ceiling of both suites and leaves less room to gain."
"In both cases the harness improves the unseen benchmark without ever being scored on it, which suggests that the benefits of RRSI are not specific to a particular backbone."
**Covers:** cross-policy-family coding evolution results
## Cross-model transfer to an unseen weaker backbone
"A harness is a program, not a set of weights, so a mechanism that helps only the policy it was searched against is an artifact of that policy rather than a reusable one."
The final coding-run harness evolved with Gemini 3.5 Flash is evaluated unchanged with Gemini 3.1 Flash Lite, a smaller model that never took part in the search: Terminal-Bench 2.1 accuracy rises from 11.2 to 14.6, "a 30.4% relative gain against a base score less than a fifth of the search policy's."
"The mechanisms therefore do not depend on the capability level they were searched at, although the absolute gain is smaller because a weaker backbone leaves fewer tasks within reach of any harness."

| Evaluation policy | H0 | RRSI | Δ |
|---|---|---|---|
| Gemini 3.5 Flash (search policy) | 64.6 | 78.7 | +14.1 |
| Gemini 3.1 Flash Lite (unseen) | 11.2 | 14.6 | +3.4 |

Table 4 | Cross-model transfer on Terminal-Bench 2.1. The harness evolved with Gemini 3.5 Flash as the frozen policy is run unchanged with a weaker backbone that never took part in the search.
**Covers:** Table 4 cross-model transfer experiment
## Cost: lightest evolved harness
"RRSI produces the lightest harness of any evolved harness. Two regularizers act directly on cost: the L1-style budget refuses growth that is not paid for when it is proposed, and the pruning rule removes growth that has stopped being paid for since."
"No prior method carries either constraint, and Figure 4 (a) shows the consequence: all four sit in the region RRSI dominates, spending more policy tokens per trial for a lower out-of-distribution average."
"AHE is the extreme case, at 3.82 million tokens per trial, 58% more than ours, for 4.4 points less out of distribution."
Trajectory length carries over in Figure 4 (b): "RRSI runs 26.3 steps per trial against 27.3 to 34.6 for the prior methods."
"No evolved harness is as cheap as H0, at 1.56 million tokens and 21.2 steps, so evolution does buy part of its gain with test-time compute; the budget decides how much."
Figure 4 | Cost of the final harness of each arm, measured on the evolve split of the agentic workspace instance. OOD Avg. is the mean over JobBench, GDPval and APEX-Agents. The shaded region in (a) is everything RRSI dominates: more policy tokens per trial for a lower out-of-distribution average.
**Covers:** Figure 4 cost / token / step comparison
## Related work, conclusion, and limitations
Agent harnesses determine what an agent can accomplish (prompt structure, tool interfaces, context compaction, recovery logic); harnesses compose and generalize, can substitute for scale, but engineering is manual and tied to specific backbones so cost recurs each model release.
Harness evolution automates the loop (LLM proposer rewrites kept on benchmark gain; or single components like skills, memory, preference signals), inheriting self-improvement risks: search driven by evolve-suite score with no generalization term, gains that do not survive suite changes, and the need to separate reusable-mechanism edits from evolution-task fits. Concurrent work targets generalization as an explicit objective or via diversity-preserving archives.
"Our contribution is orthogonal to what these methods edit. We keep the same open edit space and instead regularize the search dynamics: credit assigned over the full evolution history, task-specific logic filtered before scoring, and acceptance against a noise-adjusted baseline, so what survives is a mechanism rather than a fit to the evolution suite."
Conclusion: "iterative harness evolution as a practical form of recursive self-improvement at the agent-system level" itself requires regularization, because a reused finite evolve set lets "apparent self-improvement" reflect "benchmark-specific fitting, evaluation noise, or unnecessary complexity rather than transferable progress"; RRSI "regularizing both proposal and selection while leaving the harness edit space open" improves held-out and cross-benchmark performance at lower inference cost than unregularized evolution.
Limitations: frozen backbones only (no weight updates); reliance on a finite evolve set plus several regularization hyperparameters (sensitivity to feedback quality and search budget); transfer shown across domains, benchmarks, and policies but broader validation needed for different architectures, tool ecosystems, and longer self-improvement runs.
**Covers:** Related Work through Limitations sections
