---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement

### Q1. What three blockers to generalizable harness Recursive Self-Improvement (RSI) does ModularRSI name, and what does each one mean?

> [!tip]- Answer
> The three blockers are data-level (evolving on evaluation benchmarks confuses reusable improvement with benchmark-specific adaptation), trajectory-level (single or one-sided trajectories entangle systematic harness flaws with task-specific reasoning details), and mechanism-level (monolithic harnesses make it hard to attribute a recurring deficiency to one responsible component). ModularRSI answers them with benchmark-disjoint evolution, contrastive trajectory analysis, and modular evolution. See [[wiki/01-introduction-abstract|Abstract and Introduction]].

### Q2. Which row of Table 1 scores ✓ in all three columns (Modular / Whole-Harness Evolution / Not Use Benchmark Data), and what does that signify?

> [!tip]- Answer
> Only the ModularRSI (Ours) row scores ✓ in all three columns, while baselines such as AutoHarness, AHE, TACO, and HarnessForge miss at least one. It signifies that ModularRSI is the only compared method that is both modular and evaluated under whole-harness evolution without using benchmark data. See [[wiki/01-introduction-abstract|Abstract and Introduction]].

### Q3. How does prior work reuse execution experience, and what gap does the paper claim remains?

> [!tip]- Answer
> Prior work adapts model weights, accumulates reusable skills or context artifacts, optimizes prompts and external mechanisms via trajectory feedback, diagnoses failures from traces, or directly evolves agent implementations and harness code, with TACO specializing in observation compression for terminal agents. The claimed gap is that existing harness-evolution methods often rely on evaluation-benchmark data and treat the harness monolithically, leaving generalizable fine-grained improvement underexplored. See [[wiki/02-related-work-comparison|Related Work and Comparison]].

### Q4. What are the three stages of ModularRSI's credit-assignment pipeline, and what is the shared starting harness?

> [!tip]- Answer
> The three stages are Contrastive Trajectory Sampling and Analysis, Module-wise Harness Evolution, and Validation Gates (program checks, generalization-oriented diff review, execution validation). The five functional modules are Agent Loop, Observation Management, Tool Use, Context Management, and Task Completion Detection, reorganized from the Terminus-2 harness from Harbor as the shared starting point. See [[wiki/02-related-work-comparison|Related Work and Comparison]].

### Q5. How does the Code-Modify Agent analyze the Contrastive, Negative, and Positive trajectory groups, and what role does Trajectory Memory play?

> [!tip]- Answer
> Contrastive pairs of same-task success and failure are compared to find function-level factors behind different outcomes; all-fail Negative groups first query Trajectory Memory for a prior success to pair contrastively, else get single-sided diagnosis of loops, bad tool use, or premature termination; all-success Positive groups are mined for efficiency such as redundant actions or needless tool calls. Trajectory Memory stores per-task trajectories and rewards across epochs so earlier experience supplies contrast when current rollouts alone are insufficient. See [[wiki/03-contrastive-trajectory-analysis|Contrastive Trajectory Analysis and Trajectory Memory]].

### Q6. How are modification targets selected, what do the validation gates check, and what happens after the five modules evolve independently?

> [!tip]- Answer
> Semantically similar diagnoses on the same function are consolidated into candidates with vote counts from distinct supporting tasks, prioritizing multi-task-supported edits, while per-function Evolution History prevents redundant or oscillating changes. Program Check runs static checks, Diff Review rejects task-specific overfit, and Execution Validation samples two batch tasks, with failures rolled back via recorded diffs. After independent evolution, a cross-module integration epoch resolves duplicated or conflicting behaviors before the function library is frozen. See [[wiki/03-contrastive-trajectory-analysis|Contrastive Trajectory Analysis and Trajectory Memory]].

### Q7. What benchmarks, metrics, and evolution setup does the experiment use?

> [!tip]- Answer
> Evaluation uses TerminalBench 2.0 (89 long-horizon terminal tasks) and SWE-Bench-Verified (500 human-validated software engineering tasks), both under the Harbor framework with original released versions. The four metrics are Accuracy (mean per-trajectory success), Pass@3 (at least 1 of 3 rollouts succeeds), Pass3 (all 3 rollouts succeed), and StepNum (mean interaction steps). Evolution runs 3 epochs sampling 120 TB-related plus 120 SWE-related instances from the 2,000-instance pool, using DeepSeek-V4-Flash-Preview and DeepSeek-V4-Flash-0731 with a 2M TPM limit and batch size 10. See [[wiki/04-evolution-dataset-protocol|Experiment Setting and Generalization Results]].

### Q8. What do the cross-benchmark and cross-model transfer numbers show?

> [!tip]- Answer
> In-domain accuracy rises from 47.57 to 52.43 on TerminalBench 2.0 and from 73.40 to 76.45 on SWE-Bench-Verified, while out-of-domain transfer holds (TB-evolved reaches 75.80 on SWE-Bench, SWE-evolved reaches 49.40 on TerminalBench) and TerminalBench Pass3 climbs from 30.34 to 35.96, showing better reliability. A harness evolved with DeepSeek-V4-Flash Preview on TB tasks also transfers to GLM-5.2 (59.55 to 61.80) and MiniMax-2.5 (41.57 to 44.94). See [[wiki/04-evolution-dataset-protocol|Experiment Setting and Generalization Results]].

### Q9. Why does independent-plus-integration modular evolution beat joint and non-modular evolution, and which single module helps most on accuracy versus efficiency?

> [!tip]- Answer
> ModularRSI reaches 52.43 accuracy versus 44.19 for joint all-module evolution, 46.44 for non-modular evolution, and 47.57 for baseline, suggesting restricted modification scope reduces interference across unrelated mechanisms. All five single-module variants beat baseline, with Agent Loop giving the largest accuracy gain (50.56) and Observation Management cutting mean steps to 22.50, and integration combines these complementary gains. See [[wiki/04-evolution-dataset-protocol|Experiment Setting and Generalization Results]].

### Q10. Why does the usable contrastive-pair ratio fall across epochs, and why do medium-difficulty tasks evolve better harnesses?

> [!tip]- Answer
> The contrastive-pair ratio falls (about 36.67% toward 34.17%, Δ = −7.50 pp) because the harness progressively absorbs the reusable improvements the pairs reveal, so fewer tasks still show coexisting success and failure. Moderately difficult tasks give the most informative contrasts since easy tasks lack failures and extremely hard tasks rarely yield successes, and the Medium-centered set beats Hard & Easy 76.45% to 74.25% on SWE-Bench Verified (+2.20 pp). See [[wiki/05-experimental-results|Contrastive Analysis, Data Quality, and Conclusion]].

### Q11. How does the Agent Loop coordinate the other four modules in one normal iteration, and how is completion decided?

> [!tip]- Answer
> Agent Loop is the outer execution coordinator whose central Loop control keeps execution state, schedules calls, handles retries, and decides continuation, with each other module exchanging call/return inputs and outputs with it while the LLM and terminal environment stay external resources. One iteration runs Context Management update, LLM prompt, Tool Use parse-and-execute, Observation Management feedback, and Task Completion Detection stop recommendation. The detector only recommends (e.g. requiring two consecutive completion declarations) while Agent Loop keeps the count, issues the confirmation prompt, and controls continuation or retry. See [[wiki/06-module-wise-evolution|Agent Loop Five-Module Harness Architecture]].

### Q12. What are the per-module function interfaces, and what do the C.1–C.4 prompts enforce?

> [!tip]- Answer
> Observation.capture returns observation text plus updated state; ToolSet splits into parse_llm_response (text to commands plus completion signal) and execute (tool call to result); ContextMgmt offers maybe_compress and force_summarize over chat history; VerificationLoop.should_terminate returns only a stop recommendation plus reason. Each analyzed task yields one JSON finding (task, lens, locked_module, is_culprit, divergence, would_change_outcome, fixable_now, suggested_change), and prompts C.1–C.4 enforce read-only counterfactual attribution, general cross-finding modification, reward-blind diff review rejecting task-specific overfit, and at most one coherent cross-module repair. See [[wiki/07-appendix-function-interfaces|Function Interfaces and Analysis Schema]].

### Q13. What mechanism did each of the three trajectory case studies (NULL filter, FFmpeg linkage, Zip Slip writes) produce, and how was it confirmed later?

> [!tip]- Answer
> The contrastive NULL-filter case produced a persistent task checklist with guard (generation 9), later keeping the isNotNull filter with 47 rows and 2 of 3 rollouts passing; the negative FFmpeg case produced a completion integrity guard (generation 6), later passing all 10 tests across 3 rollouts; the positive Zip Slip case produced a robust combined tool dispatcher (generation 9), cutting mean episodes from 36 to 25 with all 60 tests passing. Trajectory evidence split 40.67% paired, 8.33% replay-paired all-fail, 14.56% unpaired all-fail, and 36.00% all-succeed across five runs plus replay. See [[wiki/08-appendix-prompts-integration|Trajectory Case Studies, Difficulty Curation, and Evolution Curve]].

### Q14. Would you recommend ModularRSI's benchmark-disjoint modular evolution to a team building self-improving coding agents, given its stated limitations?

> [!tip]- Answer
> Yes, with caveats: the frozen-harness gains transfer across domains (+2.86 to +5.63 accuracy points), models, and prior RSI baselines (67.42 vs ~62.5–62.9), and the evolution curve plus Opus-4.8 trajectory judge shows steady quality growth, so the approach is worth adopting. The team should still replicate the missing dedicated contrastive-ablation and scale beyond the 120+120-instance subset before trusting the full 2,000-instance claim, since those are the authors' own stated limitations. See [[wiki/08-appendix-prompts-integration|Trajectory Case Studies, Difficulty Curation, and Evolution Curve]].
