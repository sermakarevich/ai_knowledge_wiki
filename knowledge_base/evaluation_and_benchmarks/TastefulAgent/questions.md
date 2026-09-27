---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks

### Q1. How does the paper define agent "taste," and why is it hard to measure directly?
> [!tip]- Answer
> Taste is the ability to make good long-horizon decisions whose influence extends beyond the current step, such as which hypothesis to test, which implementation to build on, or which experiment to run next. Direct measurement is hard because a good and bad choice can look equally reasonable at decision time, and judging quality needs deep domain expertise that makes human annotation expensive and hard to scale. Existing benchmarks measure only end-to-end task success, so none measures decision quality along the way. See [[wiki/01-introduction-and-taste-definition|Introduction and Taste Definition]].

### Q2. What is the formal decision-fork model of taste, and what does each symbol mean?
> [!tip]- Answer
> Each fork defines one taste question x = (q, ht, c1, c2) with shared prefix ht = (o0, a0, …, ot), and the label is the supported candidate y = arg max_i U(Ei), where Ei is branch evidence (test results, research scores) mapped to a scalar by U. Taste Tb(π) is the fraction of questions where the model π(x) = y, with everything after fork time t hidden. A single trajectory outcome cannot score a judgment alone because execution quality and environment also shape outcomes, so the method isolates judgment by comparing branches sharing an equivalent prefix. See [[wiki/02-measuring-taste-via-hindsight|Measuring Taste via Hindsight: Decision Forks and Taste-Bench Construction]].

### Q3. What are the parallel and detour constructions, and how do the two filters plus scoring work?
> [!tip]- Answer
> Parallel construction aligns two attempts at the same task with opposite outcomes at their divergence fork (wrong judgments the agent never notices, run to completion), while detour construction mines one trajectory where the agent takes a wrong direction, hits an observed failure, then recovers (testing whether the model recognizes the failure earlier than the acting agent did). The trivial filter drops questions every judge answers correctly from candidates alone, and the undecidable filter releases a question only when every judge agrees with its label given the full task record, trajectory, and outcome. Each question is asked twice (seeded order plus exact reverse) and headline accuracy requires both correct, so random guessing scores 25% and always picking one position scores 0%. See [[wiki/02-measuring-taste-via-hindsight|Measuring Taste via Hindsight: Decision Forks and Taste-Bench Construction]].

### Q4. What are the headline accuracy results on Taste-Bench, and what is Finding 1?
> [!tip]- Answer
> Best model GPT-5.6 Sol reaches only 59.7% Average accuracy with GPT-5.5 close behind at 59.5%, and all remaining models sit dispersed below them despite every question being a binary choice. Subsets diverge per model (e.g. Claude Opus 5 scores 64.3% research but 46.7% engineering), and detour forks are harder than parallel forks in both domains, with that gap exceeding the domain gap. Finding 1 states that current frontier models show limited taste and cannot reliably identify the better direction at decision time. See [[wiki/03-model-accuracy-results|Accuracy of Current Models on Taste-Bench]].

### Q5. How do time horizon and reasoning budget affect accuracy (Findings 2 and 3)?
> [!tip]- Answer
> Mean accuracy over 14 models falls from 62.3% at the in-prefix horizon to 42.9% inferable, 31.5% next-step, and 21.0% at the more-work horizon — near the 25% random-guessing level on the both-orders-correct metric. Moving from lowest to highest reasoning effort changes accuracy by −0.2 points (GPT-5.6 Sol) and +2.2 points (GPT-5.6 Luna), with settings overlapping at every horizon, and models emit the most reasoning tokens at the more-work level where accuracy is lowest. Finding 2 says errors concentrate on long-horizon forks and Finding 3 says a larger reasoning budget does not improve taste, suggesting the deciding evidence appears only in the later work. See [[wiki/03-model-accuracy-results|Accuracy of Current Models on Taste-Bench]].

### Q6. Is Taste-Bench Average just a restatement of end-to-end ability?
> [!tip]- Answer
> No: Pearson correlation between Taste-Bench Average and SWE-bench Verified is r = +0.63 (R² = 0.39 of variance explained), and only r = +0.37 on the engineering subset mined from SWE-bench Pro tasks, using 11 models after excluding 3 with over 9% unparsable presentations. The four highest models on SWE-bench Verified sit within 4.0 points there but 10.7 points apart on Taste-Bench Average, so Taste-Bench separates models that SWE-bench compresses at the top. The chunk states the Average is useful only when it is not a restatement of end-to-end ability and argues it passes this test. See [[wiki/04-taste-bench-vs-end-to-end-benchmarks|Taste-Bench Average vs End-to-End Benchmarks]].

### Q7. How is taste distilled into Qwen3.6-27B, and what transfer does the student show (Finding 4)?
> [!tip]- Answer
> The recipe distills reasoning rather than binary labels: a privileged teacher seeing the question plus the supported-candidate description generates reasoning, and the student seeing only task, prefix, and two shuffled candidates is aligned via SDPO-style token-level forward-KL distillation on teacher-sampled continuations, trained with LoRA adapters on task-disjoint folds. On the held-out fold the student reaches 47.9% vs 30.0% for the base model (mean over orders 62.4% vs 42.7%, +17.9 pp), and with a fixed Qwen3.6-27B executor on 41 held-out SWE-bench Pro tasks, success rises from 14.6% (no advice) to 33.7% with student advice (39.0% with correct advice as upper bound). Finding 4 states that taste can be distilled and better judgment produces gains in task success. See [[wiki/04-taste-bench-vs-end-to-end-benchmarks|Taste-Bench Average vs End-to-End Benchmarks]].

### Q8. How does the paper position Taste-Bench against the four related literatures?
> [!tip]- Answer
> Long-horizon benchmarks (AgentBench, SWE-bench/Pro, MLAgentBench, RE-Bench) test whether an agent completes a task, whereas Taste-Bench tests whether it chooses the better direction inside the task. Pre-outcome idea judgment judges standalone ideas or solutions, while Taste-Bench judges forks inside executed trajectories carrying the agent's situation and recorded outcome labels — motivated by evidence that pre-execution judgments often flip after execution. Process/step-level evaluation and whole-trajectory judges score steps or attribute failures, while Taste-Bench labels the better direction with the later-recorded outcome and tests blind choice; its distillation recipe follows SDPO but replaces environment feedback with a supported-candidate demonstration. See [[wiki/05-related-work|Related Work: Long-Horizon Agents, Pre-Outcome Judgment, Process Evaluation, and Distillation]].

### Q9. What are the Taste-Bench source trajectory pools and the released per-cell sizes?
> [!tip]- Answer
> The engineering pool has 2,677 graded rollouts on 517 SWE-bench Pro tasks from 11 repositories, produced by GPT-5.4/5.5 agents in 31 runs from April to July 2026. The research pool has 1,132 MALT/METR runs on 47 RE-Bench plus HCAST-research tasks from Claude 3.5/3.7 Sonnet, Sonnet 4, Opus 4, and DeepSeek V3 agents. Released cells are parallel engineering 124 (median 35 prefix steps), parallel research 48, detour engineering 266, and detour research 64; the released engineering parallel cell has 111 same-model contrasts and 13 GPT-5.5-vs-5.4 contrasts. See [[wiki/06-references-and-appendix-opening|References and Appendix Opening: Benchmark Construction Details]].

### Q10. What acceptance and rejection filters does the Goal appendix impose on mined samples?
> [!tip]- Answer
> A sample is rejected when the better option is already identifiable from pre-decision differences, when choices mention scores, pass/fail, grades, hindsight, or use praise/blame wording that creates a strawman, and when a choice carries a self-reported or predicted target metric that makes it mechanically preferable. The proposed action must be new at the cut with completed experiment outputs as evidence (not timeouts, OOMs, or missing outputs), the reason must cite post-decision evidence causally connecting the decision to the native outcome, and failures from protocol, crash, missing dependency, hard-coding, or instruction noncompliance are rejected. Every evidence quote must be a literal excerpt from the cited step, checked mechanically, and the detour generator treats rejection as correct whenever no clean detour is demonstrable. See [[wiki/07-appendix-goal-spec|Appendix Goal Spec]].

### Q11. What JSON schema must miners return, who judges the filters, and what is the filtering yield?
> [!tip]- Answer
> Miners return exactly one object with `is_good_sample`, `reason`, `query`, `breakpoint_step`, `good_choice`, `bad_choice`, and `evidence` holding `bad_action`, `wall`, `recovery_action`, and `success` steps with literal quotes, ordered breakpoint_step ≤ bad_action.step ≤ wall.step < recovery_action.step ≤ success steps. The wall must be an observed failure (non-zero exit, error, traceback, failing assertion), hindsight-only recoveries are rejected with preference for rejection when unsure, and both options must be live, parallel-phrased candidates a competent engineer could plausibly pick. Both filters use the same four-judge panel (Kimi K2.5, GPT-4.1, Llama 4 Maverick, Mistral Large 3, excluding the generator); of 4,657 mined forks, 1,809 pass the rubric, 729 survive the trivial filter, and 502 (10.8%) are released. See [[wiki/08-appendix-required-json-format|Required JSON Format]].

### Q12. Which fork was removed as undecidable, and what do the four released example questions show?
> [!tip]- Answer
> A ResNet18 CIFAR-10 sparse-attack fork was removed because the prefix record favored the multi-strategy ensemble (0.80 success, 3.00 avg pixels vs 0.43 for one-pixel) while the label rested only on a later full-scale ensemble timeout with no stated time budget, so judges did not confirm the label. Appendix B releases one question per cell: parallel engineering picks the five-field delegated-auth selection (direct block assignment fails hidden deep-equality tests), parallel research fine-tunes only the tied embedding (loss_validation 7.3821 vs 10.1482 for rescaling), detour engineering puts the placeholder on the production path (28 passed vs 3 failed/25 passed), and detour research finds add(inverse(X4), cosine(X3)) at 5.13e-10 error. The evaluation prompt tells the model exactly one candidate is better and demands one line `ANSWER: X`. See [[wiki/09-filtering-undecidable-examples|Filtering Undecidable Examples]].

### Q13. How are evaluation prefixes rendered, answers parsed, and scores computed?
> [!tip]- Answer
> Prefixes render one line per pre-fork trajectory step (`[i] AGENT:` text, `[i] $` command plus exit code and indented output, `[i] EDIT:` paths), truncating outputs over 700 characters to head plus tail with the omitted count marked, and capping prompts at 65,536 tokens by keeping the first 25 setup lines plus the longest fitting tail. Responses are parsed from the final `ANSWER: X` line (a lone letter accepted), unparseable responses score incorrect, and each question is presented twice with cell accuracy requiring both presentations correct and Average as the 1:1 mean of research and engineering accuracies. Figure 3 intervals are 95% percentile intervals from 4,000 within-domain bootstrap resamples, and detour engineering (35.9% model-mean) is the hardest cell while parallel engineering (58.1%) is the easiest. See [[wiki/10-evaluation-prefix-rendering|Evaluation Prefix Rendering]].

### Q14. What do the horizon-level accuracies, judge-agreement, human-review, and distillation-hyperparameter details establish?
> [!tip]- Answer
> Per-level accuracy runs 62.3% in-prefix (n=158) down to 21.0% more-work (n=69), with GPT-5.6 Sol best in-prefix at 79.7% and a null budget×horizon interaction (p = 0.80 Sol, p = 0.82 Luna over 10,000 joint bootstraps); only Luna on research improves with budget (43.8% → 54.5%). Judge agreement on released parallel-engineering items is weak (pairwise 51.7%), yet human reviewers support mined labels on 170/172 retained judgments (98.8%) with κ = 0.973. Distillation trains a frozen Qwen3.6-27B teacher/student pair with forward KL over top-100 tokens (≤512 reasoning positions) plus answer-token KL on teacher-sampled continuations, then cross-entropy calibration, using LoRA rank 16/α 32 (79.7M params, ~2 h per fold on one A100 80GB). See [[wiki/11-time-horizon-annotation-levels|Time-Horizon Annotation Levels]].

### Q15. How are the distillation folds split, and how is the end-to-end advice experiment run?
> [!tip]- Answer
> The 390 engineering questions split task-disjointly into Fold 1 / Fold 2 with 195 questions and identical 62-parallel/133-detour counts each (different task counts 86 vs 72 and per-repo mixes, e.g. ansible 29 vs 43). Transfer scoring counts a question correct only when both presentations are correct: the student gets 187 vs 117 for the base (+104 gained, −34 lost), and log-odds advice selects the supported candidate on 287/390 vs 207/390. The end-to-end test covers 41 held-out SWE-bench Pro tasks (98 forks, 11 repos) with a SWE-agent 1.1.0 + Qwen3.6-27B executor, advice from the fold not containing the task, and per-fork notes naming the trap and the route to take; student advice picks the supported fork on 77/98 with exact McNemar p ≤ 0.004 for the correct-advice gain. See [[wiki/12-distillation-fold-splits|Fold Splits, Transfer Results, and End-to-End Experiment Details]].

### Q16. What substantive content does chunk 13/13 ("33") contain?
> [!tip]- Answer
> It contains no substantive content at all — only the heading `# 33` and the text `33`, with no claims, numbers, mechanisms, tables, or quotes to summarise. There are no source sections to mirror, so the wiki page exists purely as a placeholder keeping the 13/13 wiki set complete. Nothing from this chunk can appear in retrieval practice beyond noting its emptiness. See [[wiki/13-trailing-fragment|Trailing Fragment (Chunk 33)]].

### Q17. Should a team building long-horizon coding agents invest in Taste-Bench-style judgment training, and why?
> [!tip]- Answer
> Yes, invest because taste is the binding constraint the paper documents: frontier models peak at 59.7% on binary direction choices, far-horizon errors resist extra reasoning budget, and Taste-Bench separates top models that end-to-end scores compress. Distilling outcome-informed teacher reasoning into a small advisor transfers to unseen tasks and lifts a fixed executor from 14.6% to 33.7% success, so per-fork advice is a practical lever. Treat it as complementary to end-to-end training rather than a replacement, since correlation with SWE-bench Verified is only partial (r = +0.63). See [[wiki/04-taste-bench-vs-end-to-end-benchmarks|Taste-Bench Average vs End-to-End Benchmarks]].
