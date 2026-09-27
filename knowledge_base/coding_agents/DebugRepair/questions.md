---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging

### Q1. What is DebugRepair's key idea and what are its three components?
> [!tip]- Answer
> DebugRepair replaces reliance on outcome-level failure symptoms with intermediate runtime evidence collected through self-directed simulated debugging. Its three components are test semantic purification, simulated instrumentation, and debugging-driven conversational repair. With GPT-3.5 it fixes 224 Defects4J bugs and with DeepSeek-V3 it fixes 295. See [[wiki/01-framework-overview|DebugRepair Framework Overview]].

### Q2. Why must feedback-based LLM APR be augmented with a debugging-oriented cognitive process?
> [!tip]- Answer
> Existing feedback-based approaches such as ChatRepair, ContrastRepair, and TSAPR rely mainly on outcome-level symptoms like stack traces, which show how failures are observed but hide intermediate runtime states. Without that evidence LLMs must infer bug causes and often produce incorrect patches. DebugRepair therefore adds purification, simulated instrumentation, and conversational repair to supply runtime-state evidence. See [[wiki/02-background-and-limitations|Background and Limitations]].

### Q3. How does the Chart-24 motivating example show that outcome-level symptoms lead to a plausible-but-wrong patch?
> [!tip]- Answer
> In Chart-24, `getPaint` builds a `Color` from parameter `g` computed from the raw input `Value` instead of the clamped variable `v`, crashing with `IllegalArgumentException`. From the symptom alone the LLM merely clamps `g` before the constructor, masking the symptom instead of fixing the wrong variable reference. A print-statement trace showing `value = -0.5`, `v = 0.0`, and `g = -127` exposes that `g` was computed from the raw negative input rather than the restricted `v`. See [[wiki/03-motivation-example|Motivation: Chart-24 Example]].

### Q4. What does the Fig. 2 workflow illustration show with the TimeSeries createCopy example?
> [!tip]- Answer
> The failing test builds a 3-point `TimeSeries` and exercises `createCopy(0, 1)` and `createCopy(1, 2)` with min/max assertions, while the instrumented function clones the series and copies items in a loop. Three legible `// DEBUG` prints record post-clone `minY/maxY`, per-item index and value, and pre-return size and `maxY`. Pipeline labels connect purified test context, instrumented function, runtime trace, candidate patch, and validator branches to plausible patches. See [[wiki/04-framework-workflow|Framework Workflow]].

### Q5. How does test semantic purification build the minimal reproducing context, and why are iterative rescans needed?
> [!tip]- Answer
> Backward traversal from the failure-triggering statement keeps preceding statements whose defined or used objects intersect the required set, then reconstructs the minimal test preserving the original signature and order. Iterative rescans are needed because alias-induced side effects are missed in one pass, as in the listA/listB example where discovering the alias at L2 triggers a second pass capturing the L3 mutation. Helper-method and field dependencies are then added to form the complete purified context. See [[wiki/05-test-semantic-purification|Test Semantic Purification]].

### Q6. How does simulated instrumentation collect runtime traces, and what guards its correctness?
> [!tip]- Answer
> The LLM is prompted to add debugging print statements to the buggy function given the failing test context and error information, and executing the verified instrumented function yields the runtime trace of critical variables before the failure. A two-stage consistency check enforces line-wise equivalence after stripping prints plus a compilation check over up to `M_inst` attempts. On failure a deterministic AST-based fallback inserts `START_DEBUG`, per-assignment, condition, loop, and return prints mechanically. See [[wiki/06-simulated-instrumentation|Simulated Instrumentation]].

### Q7. How does debugging-driven conversational repair organize patch generation and combat overfitting?
> [!tip]- Answer
> The repair prompt combines the buggy and instrumented functions, purified test context, serialized runtime trace, and prior failure feedback so the LLM contrasts observed values against expected behavior. An inner loop refines candidates up to `K_round` rounds appending each failure, and on exhaustion a fresh debugging session starts until the global `N_session × K_round` budget is spent. Overfitting is addressed by augmenting the first plausible patch into logically similar but differently implemented validated variants. See [[wiki/07-conversational-repair|Debugging-Driven Conversational Repair]].

### Q8. What baselines, metrics, and budgets define the DebugRepair evaluation setup?
> [!tip]- Answer
> DebugRepair is compared against 15 SOTA baselines spanning learning-based, template-based TBar, and LLM-based methods plus BaseChatGPT, reusing reported numbers where available. Metrics are plausible fixes passing all tests and correct fixes confirmed by manual review, using GPT-3.5 as primary backbone under perfect fault localization. The budget is 32 patches per bug with instrumentation capped at 10 attempts, yielding 224 Defects4J fixes plus all 40 QuixBugs Java and 40 Python bugs. See [[wiki/08-evaluation-setup|Evaluation Setup]].

### Q9. What are DebugRepair's headline RQ1 totals and unique-fix leads on Defects4J?
> [!tip]- Answer
> DebugRepair fixes 111 bugs on Defects4J-V1.2, 113 on V2.0, and all 40 on QuixBugs, matching the best SOTA across languages and datasets. Against RepairAgent, ThinkRepair, and BaseChatGPT it uniquely fixes 27 bugs on V1.2 and 22 on V2.0, ranking first in unique fixes. Against ChatRepair, ContrastRepair, and TSAPR it contributes the largest unique-fix counts of 17 and 39 on the two versions. See [[wiki/09-main-results|Main Results]].

### Q10. How does DebugRepair perform across single-function, single-hunk, and QuixBugs scenarios?
> [!tip]- Answer
> On single-function Defects4J with GPT-3.5 it fixes 111 bugs on V1.2 and 113 on V2.0, leading TSAPR and ReinFix, while on single-hunk it fixes 82 and 83, closely rivaling the top baselines of 86 and 85. On QuixBugs it reaches 40/40 Java single-function, 37/37 Java single-hunk, and 40/40 Python single-function. Its iterative refinement is orthogonal to TSAPR's MCTS exploration and to ReinFix, since it refines one candidate with runtime states rather than searching many candidates. See [[wiki/10-results-analysis|Results Analysis]].

### Q11. How general is DebugRepair across backbones, and where is it weaker on single-line bugs?
> [!tip]- Answer
> Across five LLMs DebugRepair improves correct fixes by 51.3% on average, with gains scaling by size and favoring code models over general models and stronger reasoning models such as DeepSeek-V3. With DeepSeek-V3 it leads ReinFix and TSAPR substantially on single-function and single-hunk settings on both Defects4J versions. On single-line bugs it stays competitive but occasionally trails, since print-statement traces can lengthen context and hinder pure pattern-matching on outcome symptoms. See [[wiki/11-comparison-and-generality|Comparison and Generality Across LLMs]].

### Q12. What does the test-purification ablation show about fix counts and token cost?
> [!tip]- Answer
> Removing test semantic purification drops correct fixes from 224 to 164, a 26.8% decrease, because unpurified tests contain irrelevant scenarios producing redundant runtime output. Purification cuts the average runtime-output token count by 18.6% versus the unpurified setting. The joint RQ4 answer states removing any single module drops fixes by 19.9%–26.8%, proving all components are jointly essential. See [[wiki/12-ablation-test-purification|Ablation: Test Purification]].

### Q13. What do the budget, cost, and validity analyses report for DebugRepair?
> [!tip]- Answer
> Sensitivity plots cover debugging sessions, repair rounds, and augmentation numbers, and DebugRepair uses 32 patches, 38,000 tokens, and $0.036 per bug — the lowest per-bug cost among ChatRepair, RepairAgent, TSAPR, and ReinFix. Construct validity is addressed by double-blind review with a third arbitrator, and internal validity by HumanEval-Java evaluation past GPT-3.5's cutoff. External validity uses three benchmarks across Java and Python, excluding SWE-bench because its default setting denies explicit test cases. See [[wiki/13-ablation-repair-rounds|Ablation on Repair Rounds and Budget]].

### Q14. What does the first half of the bibliography (references [1]–[32]) cover?
> [!tip]- Answer
> This chunk contains no conclusion prose, only references [1]–[32] plus journal page furniture. It spans model and infrastructure sources, recent LLM and agent-based APR work, and classic and learning-based APR foundations from GenProg through Defects4J to CURE and KNOD. It closes with benchmarks such as QuixBugs and SWE-bench and template-based repair references. See [[wiki/14-conclusion-and-references-a|Conclusion and References Part A]].

### Q15. What does the second half of the bibliography (references [33]–[51]) cover?
> [!tip]- Answer
> This chunk contains only references [33]–[51] with journal page furniture and no body prose or results. It covers debugging-driven and survey work, zero-shot and conversational ChatGPT repair, code translation and robustness studies, and security and self-supervised repair foundations. It ends with repair-ingredients search, APR surveys, and syntax-guided decoding references. See [[wiki/15-references-b|References Part B]].

### Q16. Should a team adopt DebugRepair-style self-directed debugging for its LLM repair pipeline, and under what conditions?
> [!tip]- Answer
> Adopt it when bugs are complex multi-statement failures where outcome symptoms hide data flow, since purification plus runtime traces gave the largest unique-fix gains and the lowest per-bug cost in the study. Prefer lighter outcome-only prompting for pure single-line pattern bugs or tight context budgets, where extra traces added length without consistent wins. Pilot it as an orthogonal refinement stage alongside existing search or retrieval components before committing it as the default path. See [[wiki/11-comparison-and-generality|Comparison and Generality Across LLMs]].
