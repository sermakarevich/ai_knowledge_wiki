> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Environments and Experimental Setup
**In one sentence:** RRSI is evolved in three domains — coding, agentic workspace, and engineering design — with frozen Claude Opus 4.8 policy and fixed evolve/held-out splits, and improves every held-out split while baselines overfit the evolve set.
## Key points
- Coding uses Terminal-Bench 2.1 (89 containerized terminal tasks, real shell, task-owned unit tests); agentic workspace uses Harvey LAB (25 practice areas; 120-task evolve set plus 40-task pristine in-distribution held-out); engineering design uses EngDesign (61 tasks, each graded by its own frozen simulator, not a judge model).
- Out-of-distribution generalization is tested on SWE-bench Verified (coding bug fixing), JobBench / GDPval / APEX-Agents (agentic workspace), and Frontier-Eng (engineering design).
- Baselines are the unevolved base harness H0 plus Meta-Harness, AHE, TTHE, and HarnessX, all starting from the same H0 with the same frozen policy, evolve set, and candidate budget.
- Policy, proposer, cross-round failure-feedback analyst, and leakage critic are all Claude Opus 4.8, frozen throughout; base harnesses are Terminus-2 (coding), a ReAct loop over an MCP tool gateway, a dynamic toolbelt, and ReSum-style context management (Harvey LAB and EngDesign).
- Evolve-set gains are +6.0 points (Terminal-Bench 2.1), +4.9 (EngDesign), +1.1 (Harvey LAB); held-out gains include +1.8 on never-scored SWE-bench Verified, +2.3 on Harvey LAB ID held-out, +3.5 to +4.7 (7.2%–13.1%) on the three OOD agentic benchmarks, and +4.3 Medal points (+24.3%) on Frontier-Eng, with no held-out split regressing.
- On agentic workspace tasks RRSI posts the smallest evolve-set gain of any evolved harness but the only OOD average clearing H0 by more than a point (43.6 vs 39.7), while Meta-Harness adds only 0.9 OOD, HarnessX lands on base, and AHE/TTHE finish below base (TTHE by 1.7).
- Ablation shows removing either regularizer group raises the evolve score and lowers transfer: without acceptance constraints evolve rises 90.5 to 91.5 while OOD average falls 43.6 to 41.0 and token cost rises by half.
- Transfer survives deterministic simulation/testbench grading on EngDesign and Frontier-Eng, ruling out judge-styling or shared-format artifacts, and replicates under a different frozen policy (Gemini 3.5 Flash: +14.1 evolve, +2.2 OOD on SWE-bench Verified).
---
## Three evolve environments
"We evolve harnesses in three types of tasks, i.e., coding tasks, agentic workspace tasks and engineering design tasks."

- Coding: "Terminal-Bench 2.1 (Merrill et al., 2026) is a suite of 89 containerized terminal tasks in which the agent drives a real shell and is verified by the task's own unit tests."
- Agentic workspace: "Harvey LAB (Harvey AI, 2026) is a legal-work benchmark spanning 25 practice areas. It is split into a fixed evolve set of 120 tasks and a pristine in-distribution held-out set of 40 tasks."
- Engineering design: "EngDesign (Guo et al., 2025) contributes 61 design tasks, each graded by its own frozen simulator rather than by a judge model."

**Covers:** Section 4 setup, evolve environments (Terminal-Bench 2.1 / Harvey LAB / EngDesign).
## Out-of-distribution benchmarks
"To test its generalization capability, we additionally evaluate on out-of-distribution (OOD) held-out benchmarks: SWE-bench Verified (Jimenez et al., 2024) for repository-level bug fixing on the coding task, JobBench (Li et al., 2026), GDPval (Patwardhan et al., 2026) and APEX-Agents (Vidgen et al., 2026) on the agentic workspace task, and Frontier-Eng (Chi et al., 2026) on the engineering design task."

**Covers:** Section 4 setup, OOD held-out benchmarks per domain.
## Baselines
"We compare against the unevolved base harness H0 that every run starts from, and against four recent harness evolution methods, Meta-Harness (Lee et al., 2026b), AHE (Lin et al., 2026a), TTHE (Nie et al., 2026) and HarnessX (Chen et al., 2026). All the baselines start from the same H0 and share the frozen policy, the evolve set and the candidate budget. The detailed descriptions of baselines are given in Appendix B."

**Covers:** Section 4 setup, baselines and shared-budget protocol.
## Implementation details
"The policy is frozen throughout Claude Opus 4.8 (Anthropic, 2026a) across all three domains. The proposer, the analyst that writes the cross-round failure feedback and the leakage critic are all Claude Opus 4.8."

"The base harness we used are Terminus-2 (for coding) (Merrill et al., 2026), a ReAct loop (Yao et al., 2022) over an MCP tool gateway, a dynamic toolbelt (Vidgen et al., 2026), and ReSum-style context management (for Harvey LAB and EngDesign). Further hyperparameters are given in Appendix D.1."

**Covers:** Section 4 setup, frozen policy / proposer / analyst / critic and base harnesses.
## Main results (Section 4.2)
"RRSI improves every split outside the evolve set, in all three domains. Figure 3 reports every number against the unevolved base harness H0 measured in the same window, so no gain can be attributed to drift in the evaluation infrastructure."

- "The evolve-set gains are 6.0 points on Terminal-Bench 2.1, 4.9 on EngDesign and 1.1 on Harvey LAB."
- "SWE-bench Verified gains 1.8 points although repository-level bug fixing was never scored."
- "The in-distribution held-out split of Harvey LAB gains 2.3, and the three out-of-distribution agentic benchmarks gain between 3.5 and 4.7 points, 7.2% to 13.1%."
- "Frontier-Eng gains 4.3 Medal points, a 24.3% relative improvement."
- "No held-out split regresses anywhere, which is the failure a memorizing harness produces."

(Figure 3 graphic itself is garbled/unreadable in this chunk; the agentic-workspace numbers are preserved in Table 1 below.)

**Covers:** Section 4.2, main results and Figure 3 headline gains.
## Baseline comparison (Table 1)
"RRSI consistently outperforms baselines on all held-out datasets. Table 1 runs the four prior methods from the same H0 on the same evolve split under the same candidate budget. Every one of them works well on evolve set. The performance on in-distribution held-out split is quite similar."

"The separation appears out of distribution, and there the ranking inverts. Meta-Harness, the strongest baseline on the evolve split, adds 0.9 points to the out-of-distribution average; HarnessX lands on the base one; AHE and TTHE finish below the harness they started from, TTHE by 1.7 points. RRSI posts the smallest evolve-set gain of any evolved harness and the only out-of-distribution average that clears H0 by more than a point, 43.6 against 39.7, which is the trade the regularizers are designed to make."

| Method | Harvey LAB (Evolve) | Harvey LAB (ID Held-out) | JobBench | GDPval | APEX-Agents |
|---|---|---|---|---|---|
| H0 (no evolution) | 89.4 | 86.9 | 36.0 | 48.8 | 34.2 |
| Meta-Harness (Lee et al., 2026b) | 93.0 | 89.2 | 37.1 | 49.1 | 35.7 |
| AHE (Lin et al., 2026a) | 90.7 | 88.7 | 37.2 | 47.2 | 33.1 |
| TTHE (Nie et al., 2026) | 91.1 | 88.5 | 35.2 | 47.0 | 31.7 |
| HarnessX (Chen et al., 2026) | 91.8 | 89.1 | 36.3 | 48.5 | 34.3 |
| RRSI (ours) | 90.5 | 89.2 | 40.7 | 52.3 | 37.9 |

**Covers:** Section 4.2, Table 1 (agentic workspace baseline comparison).
## Not a judge-grading artifact
"The transfer is not an artifact of judge-mediated grading or of a shared task format. Harvey LAB, JobBench and GDPval are all scored by a judging model, so a harness could in principle raise its score by writing the way a judge rewards rather than by producing better work."

"The engineering design instance closes that route: each EngDesign and Frontier-Eng task is graded by its own simulation or testbench, the grading is deterministic, and a design either meets the stated constraints or does not. The gains survive there unchanged, and deterministic grading also removes judge variance from the measurement."

**Covers:** Section 4.2, judge-vs-simulator grading discussion.
## Analysis setup and ablation (Section 4.3)
"The main results establish that the evolved harnesses transfer; this section asks what produced that property, whether it depends on the backbone the search was run with, and what it costs. Unless stated otherwise, every run below uses the agentic workspace instance and shares the base harness, policy, evolve split, round count and candidate budget of the main experiment, so that arms differ only in the factor under study."

"We ablate the two groups of regularizers, (i) the proposal-side constraints and (ii) the acceptance-side constraints. As shown in Table 2, removing either group raises the evolve-set score and lowers transfer. Without the acceptance constraints the evolve-set score rises from 90.5 to 91.5 while the out-of-distribution average falls from 43.6 to 41.0 and token cost rises by half, showing that an unconstrained selection rule spends most of its accepted edits on noise and on context rather" [chunk truncates here].

| Variant | Harvey LAB (Evolve) | Harvey LAB (ID Held-out) | OOD Avg. | Tokens/trial (m) |
|---|---|---|---|---|
| H0 (no evolution) | 89.4 | 86.9 | 39.7 | 1.56 |
| Unregularized evolution | 92.8 | 88.9 | 40.3 | 3.80 |
| w/o proposal regularizers | 90.7 | 88.8 | 41.9 | 2.69 |
| w/o acceptance regularizers | 91.5 | 88.7 | 41.0 | 3.59 |
| RRSI | 90.5 | 89.2 | 43.6 | 2.42 |

"OOD Avg. is the mean over JobBench, GDPval and APEX-Agents."

**Covers:** Section 4.3 opening and ablation (Table 2); final sentence of the acceptance-constraint claim is truncated in the chunk.
## Policy robustness (Table 3)
"Harness evolution is run independently with each frozen policy on Terminal-Bench, and the harness is evaluated unchanged on SWE-bench Verified."

| Policy | Benchmark | H0 | RRSI | Δ |
|---|---|---|---|---|
| Claude Opus 4.8 | Terminal-Bench 2.1 (Evolve) | 74.2 | 80.2 | +6.0 |
| Claude Opus 4.8 | SWE-bench Verified (OOD) | 82.0 | 83.8 | +1.8 |
| Gemini 3.5 Flash | Terminal-Bench 2.1 (Evolve) | 64.6 | 78.7 | +14.1 |
| Gemini 3.5 Flash | SWE-bench Verified (OOD) | 76.8 | 79.0 | +2.2 |

**Covers:** Section 4.3, Table 3 (policy robustness in the coding domain).
**Covers:** Chunk 04-environments-we-evolve-harnesses-in-three — Sec. 4 setup (three environments, OOD benchmarks, baselines, implementation) through Sec. 4.2 main results (Fig. 3, Table 1, judge-artifact discussion) into Sec. 4.3 analysis opening, Table 2 ablation, and Table 3 policy robustness.
