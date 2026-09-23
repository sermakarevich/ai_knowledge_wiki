> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experiment Setting and Generalization Results
**In one sentence:** ModularRSI is evaluated on TerminalBench 2.0 and SWE-Bench-Verified with four metrics and shown to improve accuracy and reliability both in-domain and out-of-domain, across models, and over non-modular and prior RSI baselines.
## Key points
- Evaluation uses TerminalBench 2.0 (89 long-horizon terminal tasks) and SWE-Bench-Verified (500 human-validated software engineering tasks), both run under the Harbor framework with original released versions.
- Four metrics are reported: Accuracy (mean per-trajectory success), Pass@3 (solved in at least 1 of 3 rollouts), StepNum (mean agent-environment steps per rollout), and Pass3 (solved in all 3 rollouts).
- Evolution runs 3 epochs for single-module and joint-module evolution, sampling 120 TB-related plus 120 SWE-related instances from the 2,000-instance evolution dataset, using DeepSeek-V4-Flash-Preview and DeepSeek-V4-Flash-0731 with a 2M TPM limit and batch size 10.
- In-domain evolution improves accuracy from 47.57 to 52.43 on TerminalBench 2.0 and from 73.40 to 76.45 on SWE-Bench-Verified, with largely monotonic gains across RSI generations (see Appendix F).
- Out-of-domain transfer also holds: TB-evolved harness reaches 75.80 on SWE-Bench-Verified and SWE-evolved harness reaches 49.40 on TerminalBench 2.0, and TerminalBench Pass3 rises from 30.34 to 35.96, indicating better reliability.
- A harness evolved with DeepSeek-V4-Flash Preview on TB tasks transfers to other backbones on TerminalBench 2.0 (GLM-5.2: 59.55 to 61.80; MiniMax-2.5: 41.57 to 44.94; DeepSeek-V4-Flash: 47.57 to 52.43).
- Independent per-module evolution plus integration beats joint and non-modular evolution (ModularRSI 52.43 Acc vs. 44.19 joint vs. 46.44 non-modular vs. 47.57 baseline), and all five single-module variants beat baseline with Agent Loop best on accuracy and Observation Management cutting steps to 22.50.
- Against prior methods on TerminalBench 2.0 with DeepSeek-V4-Flash-0731 (Terminus-2 baseline 61.79, 16-epoch AHE/Meta-Harness, web search disabled), AHE (62.54) and Meta-Harness (62.92) stay near baseline while ModularRSI reaches 67.42 Acc, 78.65 Pass@3, 56.18 Pass3.
---
## 5.1 Benchmarks
**Covers:** Section 5.1, Experiment Setting — Benchmarks

To validate effectiveness, the chunk evaluates against the baseline on "two recent and challenging terminal-related benchmarks: TerminalBench 2.0 (Merrill et al., 2026b) and SWE-Bench-Verified (Jimenez et al., 2024b)."

- TerminalBench 2.0: 89 diverse long-horizon terminal tasks.
- SWE-Bench-Verified: 500 human-validated software engineering tasks from real-world repositories.
- Together they cover general terminal interaction and repository-level software engineering.
- "For reproducibility, we use the original released benchmark versions and conduct all evaluations under the Harbor framework."

## 5.2 Metrics
**Covers:** Section 5.2, Metrics (four metrics)

- Accuracy (Acc): "average success rate over all rollout trajectories. A trajectory is considered successful if the agent successfully completes the corresponding task according to the task-specific evaluator."
- Pass@3: "whether the agent can successfully solve a task within three independent rollout attempts. A task is counted as solved if at least one of the three trajectories succeeds."
- StepNum: "average number of agent-environment interaction steps required per rollout... fewer steps generally indicating a more efficient problem-solving process."
- Pass3: consistency/reliability — "counted as successfully solved only if all 3 trajectories succeed, and the final score is averaged across all evaluation tasks."

## 5.3 Implementation Details
**Covers:** Section 5.3, Implementation Details

- All evolution processes (single-module and joint-module) run for 3 epochs.
- 120 instances sampled from each of the TB-related and SWE-related subsets of the 2,000-instance evolution dataset.
- Primary evolution models: DeepSeek-V4-Flash-Preview and DeepSeek-V4-Flash-0731.
- Deployed models provisioned with TPM limit of 2 million tokens, batch size 10.

## 6.1 Generalization Beyond Evolution Experience
**Covers:** Section 6.1, cross-benchmark transfer (Table 2)

Setup: two independent evolution sets (TB-related, SWE-related), 120 instances each; evolved harnesses evaluated on both TerminalBench 2.0 and SWE-Bench-Verified in-domain and out-of-domain. "The evolution sets are completely isolated from the evaluation benchmarks, preventing direct exposure to evaluation tasks during evolution."

Table 2 — Cross-benchmark transfer of frozen evolved harnesses (DeepSeek-V4-Flash-Preview backbone):

| Evolution Set | SWE-Bench-Verified setting | Acc | Pass@3 | Pass3 | TerminalBench 2.0 setting | Acc | Pass@3 | Pass3 |
|---|---|---|---|---|---|---|---|---|
| No Evolution | – | 73.40 | 83.20 | 62.80 | – | 47.57 | 58.43 | 30.34 |
| TB-Related | Out-of-Domain | 75.80 | 84.67 | 66.20 | In-Domain | 52.43 | 65.17 | 35.96 |
| SWE-Related | In-Domain | 76.45 | 85.30 | 66.80 | Out-of-Domain | 49.40 | 60.67 | 30.34 |

Key claims (verbatim in spirit): "with DeepSeek-V4-Flash-Preview as the backbone model, ModularRSI consistently improves performance across both evaluation benchmarks under different evolution settings"; "gains transfer beyond the evolution domain"; this "suggest[s] that ModularRSI discovers reusable improvements to the underlying agent execution mechanism, rather than merely specializing to the tasks encountered during evolution." Pass3 on TerminalBench 2.0 rising "from 30.34 to 35.96... not only increases average task-solving capability but also enhances execution reliability, reducing stochastic failures across repeated trials." Performance shows "a largely monotonic improvement throughout the evolution process (see Appendix F)."

## 6.2 Cross-Model Generalization
**Covers:** Section 6.2, frozen harness transferred across inference models (Table 3)

Setup: harness evolved with DeepSeek-V4-Flash Preview on the TB-related set, frozen, then applied to different foundation models on TerminalBench 2.0.

Table 3 — Generalization across inference models on TerminalBench 2.0:

| Inference Model | Method | Acc | Pass@3 | Pass3 |
|---|---|---|---|---|
| GLM-5.2 | Baseline | 59.55 | 70.79 | 46.07 |
| GLM-5.2 | ModularRSI | 61.80 | 74.16 | 49.44 |
| MiniMax-2.5 | Baseline | 41.57 | 56.18 | 24.72 |
| MiniMax-2.5 | ModularRSI (Ours) | 44.94 | 57.30 | 30.34 |
| DeepSeek-V4-Flash | Baseline | 47.57 | 58.43 | 30.34 |
| DeepSeek-V4-Flash | ModularRSI (Ours) | 52.43 | 65.17 | 35.96 |

Claim: "the evolved harness consistently improves Acc, Pass@3, and Pass3 across all evaluated foundation models," demonstrating "transferable improvements to the agent execution process rather than exploiting model-specific behaviors."

## 6.3 Effect of Modular Evolution
**Covers:** Section 6.3, modular vs. joint vs. non-modular and single-module ablations (Tables 4–5)

Table 4 — Harness evolution strategies on TerminalBench 2.0:

| Method | Acc | Pass@3 | Pass3 | StepNum |
|---|---|---|---|---|
| Baseline | 47.57 | 58.43 | 30.34 | 34.70 |
| Non-modular Evolution | 46.44 | 64.04 | 24.72 | 29.03 |
| Joint All-Module Evolution | 44.19 | 61.80 | 24.72 | 44.34 |
| ModularRSI (Ours) | 52.43 | 65.17 | 35.96 | 35.57 |

Claim: "independently evolving modules and then integrating them achieves the best overall performance... In contrast, both joint and non-modular evolution reduce accuracy below the baseline. This suggests that restricting the modification scope helps reduce interference when optimizing the harness."

Table 5 — Single-module evolution and cross-module integration on TerminalBench 2.0:

| Method | Acc | Pass@3 | Pass3 | StepNum |
|---|---|---|---|---|
| Baseline | 47.57 | 58.43 | 30.34 | 34.70 |
| Context Management | 49.44 | 61.80 | 31.40 | 35.10 |
| Tool Use | 50.19 | 62.92 | 30.34 | 41.28 |
| Agent Loop | 50.56 | 64.04 | 34.83 | 40.40 |
| Observation Management | 49.81 | 65.17 | 33.70 | 22.50 |
| Task Completion Detection | 49.44 | 65.17 | 31.40 | 31.06 |
| ModularRSI (Ours, integrated) | 52.43 | 65.17 | 35.96 | 35.57 |

Claims: each of the five modules is evolved independently for three epochs from the same baseline; "all single-module variants improve accuracy over the baseline, with different modules providing distinct benefits. Agent Loop yields the largest single-module accuracy gain, whereas Observation Management substantially reduces the average number of execution steps." Integration "further increases Acc to 52.43 and Pass3 to 35.96, suggesting that the modules capture complementary improvements that can be effectively combined."

## 6.4 Comparing with Existing RSI Methods
**Covers:** Section 6.4, comparison with AHE and Meta-Harness (Table 6, partial)

Protocol: AHE and Meta-Harness adapted to the Harbor framework, evolved from the same Terminus-2 harness on the same 120 evolution instances. "ModularRSI evolves each module independently for three epochs, followed by a merging stage. To match the aggregate number of evolution rounds... we evolve AHE and Meta-Harness for 16 epochs." Final-generation harness evaluated on TerminalBench 2.0; all use DeepSeek-V4-Flash-0731 for evolution and evaluation with 2M TPM limit; "web search [disabled] for all methods to prevent the evolved harnesses from retrieving task solutions from external sources."

Table 6 — Comparison with existing harness evolution methods on TerminalBench 2.0:

| Method | Acc | Pass@3 | Pass3 |
|---|---|---|---|
| Baseline | 61.79 | 73.03 | 50.56 |
| Meta-Harness | 62.92 | 74.16 | 50.56 |
| AHE | 62.54 | 73.03 | 51.69 |
| ModularRSI (Ours) | 67.42 | 78.65 | 56.18 |

Claim: "although existing RSI methods can achieve strong performance when evolving directly on benchmark data, their improvements are much more limited under our benchmark-disjoint protocol. Both AHE and Meta-Harness remain close to the Terminus-2 baseline, with accuracy changes of approximately one percentage point, whereas ModularRSI improves accuracy by" — [chunk truncates here; continuation not present in source].
**Covers:** Sections 5–6.4 (Experiment Setting through comparison with existing RSI methods); chunk header URLs (github.com, huggingface.co, kaggle.com, docs.kernel.org) are extraction noise, not content.
