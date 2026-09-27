> [[index|Wiki]] | [[summary|Summary]]
# DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging — Digest

## 1. [[wiki/01-framework-overview|DebugRepair Framework Overview]]
**In one sentence:** DebugRepair enhances feedback-based LLM program repair by replacing reliance on outcome-level failure symptoms with intermediate runtime evidence collected through self-directed simulated debugging.
- Feedback-based LLM APR techniques (e.g., ChatRepair, ContrastRepair, TSAPR) iteratively refine patches from test execution feedback but rely primarily on outcome-level symptoms such as stack traces.
- Outcome-level symptoms show how failures are observed but hide the intermediate runtime states needed for root-cause analysis, causing LLMs to infer bug causes without evidence and produce incorrect patches.
- DebugRepair's key idea is to enhance patch refinement with intermediate runtime evidence collected through simulated debugging rather than relying solely on outcome-level failure symptoms.
- Component 1, test semantic purification, extracts the minimal failure-triggering test context to remove noise from tests and follow-up debugging logs.
- Component 2, simulated instrumentation, lets the LLM insert targeted debugging statements into buggy functions to collect runtime traces, with a rule-based fallback when LLM-instrumented code fails to compile or introduces semantic inconsistencies.
- Component 3, debugging-driven conversational repair, organizes patch generation into a hierarchical, iterative process that progressively refines candidates using both prior repair attempts and newly observed runtime states.
- With GPT-3.5, DebugRepair correctly fixes 224 bugs on Defects4J (26.2% average improvement over SOTA LLM-based approaches); with DeepSeek-V3 it fixes 295 Defects4J bugs, 59 more than the second-best baseline.
- Across five additional backbone LLMs of different families and sizes, DebugRepair improves repair performance by 51.3% on average over vanilla settings, and ablation studies confirm all three components contribute effectively.

## 2. [[wiki/02-background-and-limitations|Background and Limitations: Why LLM-based APR Needs Debugging Augmentation]]
**In one sentence:** LLM-based APR must be augmented with a debugging-oriented cognitive process because outcome-level failure symptoms alone leave LLMs to misdiagnose complex bugs, which DebugRepair addresses via test purification, simulated instrumentation, and conversational repair to achieve large gains (e.g., 224 correct Defects4J fixes on GPT-3.5, +26.2% over SOTA).
- It is imperative to augment LLM-based APR tools with a debugging-oriented cognitive process to alleviate their reasoning burden on complex bugs.
- Existing feedback-based APR approaches rely mainly on outcome-level failure symptoms, which are insufficient for precise patch refinement.
- Test Semantic Purification reduces useless debugging logs by statically slicing the failing test to the minimal semantic subset directly related to the failure.
- Simulated Instrumentation guides the LLM into a debugging phase with autonomous breakpoints and print statements, plus a deterministic rule-based fallback for robust trace collection.
- Debugging-Driven Conversational Repair uses hierarchically iterative loops: an outer loop for instrumentation and an inner loop refining patches from prior fixes plus new runtime-state feedback, until a plausible patch or budget exhaustion.
- With GPT-3.5, DebugRepair correctly fixes 224 Defects4J bugs (+26.2% average over SOTA LLM baselines); with DeepSeek-V3 it fixes 295 (59 more than the second-best approach).
- Across five other LLMs from diverse families and sizes, DebugRepair fixes 51.3% more bugs than vanilla settings on average, and ablation shows both purification and simulated debugging are critical.

## 3. [[wiki/03-motivation-example|Motivation: Chart-24 Example Shows Why Repair Needs Runtime State]]
**In one sentence:** The Defects4J Chart-24 bug shows that feeding an LLM only buggy code plus the outcome-level crash symptom yields a plausible-but-wrong patch that clamps `g`, while observing runtime intermediates (value = -0.5, v = 0.0, g = -127) exposes that `g` was computed from the raw input instead of the clamped `v`.
- The motivating example is the Defects4J Chart-24 bug in function `getPaint`, which should return a `Color` based on variable `v` clamped between `lowerBound` and `upperBound` derived from input `Value`.
- The root cause is that the parameter `g` for constructing the `Color` object erroneously uses the raw input value instead of the restricted variable `v`, crashing with `java.lang.IllegalArgumentException`.
- Existing LLM-based APR tools are fed the buggy code plus outcome-level failure symptoms, which only confirm an invalid color parameter while concealing intermediate states.
- From symptoms alone the LLM concludes `g` is simply outside the valid range and generates a plausible but incorrect patch that explicitly clamps `g` before the `Color` constructor (Line 5).
- That incorrect patch merely masks the symptom instead of fixing the mistaken variable reference of `Value` in Line 4.
- A human-style debugging trace (inserted print statements) shows `value` is -0.5, `v` is evaluated as 0.0, and `g` is calculated as -127.
- The conflict — `v` correctly clamped to the legal lower bound 0.0 while `g` is an illegal -127 — reveals `g` was computed from the raw negative value (-0.5) rather than the restricted `v`, enabling the correct patch.
- The chunk's thesis is that runtime intermediate states are the critical bridge between symptom and root cause, so the LLM should proactively insert print statements and analyze debugging output rather than passively consuming outcome-level symptoms.

## 4. [[wiki/04-framework-workflow|Framework Workflow (Fig. 2) and TimeSeries Illustration]]
**In one sentence:** This chunk is a heavily garbled OCR rendering of Fig. 2 ("Overview of DebugRepair") whose only reliably readable content is a TimeSeries `createCopy` test plus an instrumented clone/copy loop with `// DEBUG` prints and pipeline labels (purified test context, instrumented function, runtime trace, patch validation).
- The failing/purified test builds `TimeSeries s1 = new TimeSeries("S1")` with entries `(Year 2009, 100.0)`, `(Year 2010, 101.0)`, `(Year 2011, 102.0)` and asserts `getMinY() == 100.0` and `getMaxY() == 102.0`.
- The test then exercises `s1.createCopy(0, 1)` (asserting min 100.0 / max 101.0) and `s1.createCopy(1, 2)` (asserting min 101.0 / max 102.0), plus a `testCreateCopy3` case that builds the same 3-point series and asserts `createCopy(0, 1)` has max 101.0.
- The instrumented function is shown as `TimeSeries copy = (TimeSeries) super.clone();` followed by `copy.data = new java.util.ArrayList();` and a `for (int index = start; index <= end; index++)` copy loop.
- Three inserted debug statements are legible: a post-clone print of `copy.minY`/`copy.maxY`, a per-item print of `index`, `item.getValue()`, and `copy.maxY`, and a pre-return print of `copy.data.size()` and `copy.maxY`.
- The only readable runtime-trace values are `copy.minY=100.0, copy.maxY=102.0` after clone, `index=0, value=100.0` / `index=1, value=101.0` with `copy.maxY=102.0` per item, and `copy.size=2, copy.maxY=102.0` before return.
- The surrounding pipeline labels name the stages `Insert Print Statement`, `Failure-Triggering Statement`, `Purified Test Context`, `Instrumented Function`, `Run and Collect Output`, `Runtime Trace`, `Candidate Patch Augment` / `Patch`, and a `Validator` with `Pass`/`Fail` branches leading to `Plausible Patch` and `Verified Plausible Patches`.
- Because the text is fragmented OCR (overlapping columns, broken sentences, no complete prose claims), no further mechanism, number, or result can be faithfully extracted from this chunk alone.

## 5. [[wiki/05-test-semantic-purification|Test Semantic Purification]]
**In one sentence:** Test semantic purification backward-slices the failing test to a minimal reproducing method plus its helper-method and field dependencies, using iterative rescans to capture alias-induced side effects missed in a single pass.
- Backward traversal starts from the failure-triggering statement 𝑠_𝑓𝑎𝑖𝑙 and keeps a preceding statement 𝑠_𝑖 when its defined variables/objects or (for non-asserts) used objects intersect the required set 𝑉_𝑟𝑒𝑞 (Algorithm 1, Lines 13–14).
- Statements not dependent on 𝑠_𝑓𝑎𝑖𝑙 can still use objects in 𝑉_𝑟𝑒𝑞 and cause side effects that affect 𝑠_𝑓𝑎𝑖𝑙, so traversal repeats iteratively updating Slice and 𝑉_𝑟𝑒𝑞 until no new objects appear (changed flag fixed to False, Lines 18–19).
- The alias example (Fig. 3): listB is an alias of listA (L2), and `listB.add(...)` at L3 mutates their shared object, implicitly affecting listA checked by the failing assertion at L4.
- First traversal misses the L3 side effect because alias listB is not in 𝑉_𝑟𝑒𝑞 until L2 is processed; discovering listB at L2 sets changed True and triggers a second traversal that captures L3, yielding final Slice {L1, L2, L3, L4} from {L1, L2, L4}.
- The minimal test 𝑇_𝑚𝑖𝑛 is reconstructed by preserving the original method signature of 𝑇 and assembling retained Slice statements in original relative order (Line 24).
- Direct helper-method dependencies D_𝑚 are method callees of 𝑇_𝑚𝑖𝑛 defined in enclosing class C (Lines 25–26); indirect dependencies are found by iteratively intersecting callees with methods defined in C until the intersection is empty (Lines 27–31).
- Class-level field dependencies D_𝑣 are variables/objects of 𝑇_𝑚𝑖𝑛 plus D_𝑚 intersected with fields declared in C (Lines 32–33); required field and method definitions form complete external dependencies D (Line 34).
- The purified context strips irrelevant noise so later simulated instrumentation and repair focus on the failure-triggering scenario while reducing irrelevant log length.

## 6. [[wiki/06-simulated-instrumentation|Simulated Instrumentation: Adding Debugging Print Statements]]
**In one sentence:** DebugRepair instruments the buggy Java function with debugging print statements via an LLM prompt (Fig. 4) guarded by a two-stage consistency check, falling back to deterministic rule-based AST instrumentation (Algorithm 2) before capturing a runtime trace for repair.
- The instrumentation prompt asks the LLM to "add appropriate debugging print statements to the given Java function" given the buggy function, failing test context, and error information (Fig. 4).
- LLM-generated instrumentation may add unintended edits beyond prints (auxiliary comments, syntactic errors), so a two-stage consistency check enforces `Norm(F_inst) ≡ Norm(F_buggy)` line-wise after stripping prints/comments plus a compilation check on `F_inst`.
- If LLM instrumentation fails the checks over a maximum of `M_inst` attempts, a deterministic rule-based fallback (Algorithm 2) parses `F_buggy` to an AST and reinserts prints mechanically.
- The rule-based fallback inserts `// START_DEBUG` as the first statement, `// DEBUG [VAR] names = vals` after each variable init/assignment, and `// DEBUG [COND] cond =` before each if-condition via a temp variable `t` that replaces the condition to avoid repeated-execution side effects.
- Loops are handled by replacing the loop condition with `true` and inserting `s1` (assign `c` to `t`), `s2` (log `// DEBUG [LOOP] cond =` + `t`), and `s3` (conditional break on non-`t`) at loop entry; returns use the same temp-variable pattern (`// DEBUG [RETURN]`) or a fixed `// DEBUG [RETURN] void` for empty returns, with `// END_DEBUG` before every exit.
- Executing the verified `F_inst` in context `<T_min, D>` yields `τ_runtime = <log1, ..., logk>`, where each log records a critical variable `v ∈ V_crit` and its value before `s_fail`, revealing data-flow issues invisible from outcome-level symptoms.

## 7. [[wiki/07-conversational-repair|Debugging-Driven Conversational Repair]]
**In one sentence:** DebugRepair repairs with a hierarchical conversational loop that feeds the LLM a prompt combining the buggy and instrumented function, purified test context, runtime trace, and prior failure feedback, retries within a session up to K_round, starts fresh debugging sessions up to a global N_session × K_round budget, and then augments the first plausible patch into diverse validated variants.
- The repair prompt combines F_buggy, its instrumented version F_inst, the purified test context ⟨T_min, D⟩, the serialized dynamic trace τ_runtime, plus the initial failed patch P0 and its error message E0.
- The stated goal of this comprehensive context is evidence-based reasoning: deducing logic errors by contrasting observed runtime values against expected behaviors rather than relying solely on outcome-level failure symptoms.
- In each round k (1 ≤ k < K_round), the LLM generates candidate Pk from the augmented context plus feedback history; on failure the framework captures compilation or runtime symptoms as ⟨Pk, Ek⟩ and appends them for the next round's Pk+1.
- Iteration continues until a plausible patch is found or the K_round limit is reached, with each failed attempt's specific failure symptoms preserved in the conversation history.
- If K_round attempts fail, the session is terminated, its history discarded, and a new debugging session captures a fresh dynamic trace; the whole process ends on a plausible patch or exhaustion of the global N_session × K_round budget.
- Patch augmentation addresses test overfitting: following prior work [19, 38], the first plausible patch is used as a reference and the LLM generates logically similar but differently implemented variants, all validated against the test suite, outputting a set of plausible patches.
- Evaluation is organized around five research questions (RQ1–RQ5) covering SOTA comparison, repair scenarios (single-function/hunk/line), backbone-LLM generality, component contributions, and post-training-cutoff generalization.
- Benchmarks are Defects4J-V1.2 (391 bugs), Defects4J-V2.0 (+438 bugs), QuixBugs (40 Java + 40 Python), and HumanEval-Java (163 single-hunk cases chosen to reduce GPT-3.5 data-leakage risk), with SL ⊆ SH ⊆ SF categorization.

## 8. [[wiki/08-evaluation-setup|Evaluation Setup]]
**In one sentence:** DebugRepair is evaluated against 15 SOTA baselines on Defects4J and QuixBugs using plausible/correct-fix counts, with GPT-3.5 as the primary backbone under perfect fault localization and a patch budget of 32, and it correctly fixes 224 Defects4J bugs plus all 40 QuixBugs Java and Python bugs.
- 15 SOTA baselines are compared: 8 learning-based (CURE, Recoder, SelfAPR, RewardRepair, KNOD, AlphaRepair, FitRepair, RAP-Gen), 1 template-based (TBar), and 6 LLM-based (ChatRepair, ContrastRepair, TSAPR, RepairAgent, ReinFix, ThinkRepair), plus a BaseChatGPT basic-prompt baseline.
- Results reported for baselines follow the common APR practice of reusing numbers from their original papers, with "-" in Table 2 marking unreported results.
- Two metrics are used: # Plausible (bugs passing all test cases after fixing, without further verification) and # Correct (plausible patches confirmed by manual review).
- The primary backbone is gpt-3.5-turbo via OpenAI API, supplemented by DeepSeek-V3, Qwen2.5-7B, Qwen2.5-Coder-7B, and Qwen2.5-32B via SiliconFlow, all sampled at temperature 1.0.
- Fault localization uses the perfect setting to avoid FL-tool bias, consistent with recent studies, and AST parsing/manipulation for Java and Python uses tree-sitter on an Ubuntu 20.04 server with two Intel Xeon Gold 6138 CPUs and 251 GB RAM.
- The repair budget is bounded by 32 candidate patches per bug (6 sessions × 4 rounds + 8 patch-augmentation queries), with LLM instrumentation attempts capped at 10.
- On Defects4J, DebugRepair fixes 224 bugs total (111 on V1.2, 113 on V2.0; 224/283 correct/plausible), 11 more than second-ranked ReinFix (213) with a smaller patch size, and tops 7 of 17 projects.
- On QuixBugs, DebugRepair correctly fixes all 40 Java and all 40 Python bugs, and with DeepSeek-V3 as backbone it fixes 59 more Defects4J bugs than the most competitive reproduced LLM baseline (ReinFix).

## 9. [[wiki/09-main-results|Main Results]]
**In one sentence:** DebugRepair matches SOTA across languages and datasets, leads all baselines in unique fixes on Defects4J-V1.2/V2.0, fixes 111/113/40 bugs (V1.2/V2.0/QuixBugs), and its Lang-6 case study shows dynamic runtime-state debugging succeeding with a single iteratively debugged candidate where outcome-level search (e.g. TSAPR's MCTS) fails.
- RQ1 totals: DebugRepair fixes 111 bugs on Defects4J-V1.2, 113 on Defects4J-V2.0, and all 40 on QuixBugs, matching the best SOTA baselines across languages and datasets.
- Against RepairAgent, ThinkRepair, and BaseChatGPT (ReinFix excluded as its detailed GPT-3.5 results are not publicly available), all four jointly fix 33 bugs on V1.2 and 20 on V2.0, while DebugRepair uniquely fixes 27 and 22 respectively and ranks first in unique fixes.
- Against feedback-based baselines ChatRepair, ContrastRepair, and TSAPR, all four jointly fix 56 bugs on V1.2 and 24 on V2.0, while DebugRepair contributes the largest unique-fix counts of 17 and 39 respectively.
- The overlap is attributed largely to a shared backbone model, yet DebugRepair's patch refinement via dynamic debugging gives it a distinct, complementary advantage readily integrable into most existing APR tools.
- Lang-6 case study (Apache Commons Lang character utility): `pos` used as index of `Character.codePointAt(input, pos)` increments past the valid range, causing `StringIndexOutOfBoundsException`; DebugRepair instruments the function, observes `pos` evolving step by step to the invalid boundary, and inserts a boundary check plus updates `pos` from the retrieved code point.
- TSAPR's Monte Carlo Tree Search over multiple patch candidates fails on Lang-6 because its execution feedback is limited to outcome-level symptoms (e.g. producing only `pos` to `pos + 1` changes), while DebugRepair needs only a few rounds iteratively debugging a single candidate.
- RQ2 setup: robustness is evaluated across Single-Function (SF), Single-Hunk (SH), and Single-Line (SL) bug complexity, comparing only LLM-based baselines on Defects4J and QuixBugs with GPT-3.5 and DeepSeek-V3 backbones, with DebugRepair reported superior/SOTA on complex SF and SH settings.

## 10. [[wiki/10-results-analysis|Results Analysis]]
**In one sentence:** With a GPT-3.5 backbone DebugRepair leads the single-function scenario with 111 correct fixes on Defects4J-V1.2 and 113 on Defects4J-V2.0 while remaining competitive in the single-hunk scenario, and its iterative patch-refinement design is orthogonal to TSAPR's MCTS exploration and to ReinFix.
- On Defects4J-V1.2 single-function (SF), DebugRepair fixes 111 bugs, outperforming TSAPR (108) and ReinFix (104).
- On Defects4J-V2.0 SF, DebugRepair fixes 113 bugs, surpassing ReinFix (109) and TSAPR (93).
- On single-hunk (SH) scenarios DebugRepair fixes 82 bugs on V1.2 and 83 on V2.0, closely rivaling the top baselines of 86 (TSAPR on V1.2) and 85 (ReinFix on V2.0).
- On QuixBugs DebugRepair reaches 40/40 (SF, Java), 37/37 (SH, Java), and 40/40 (SF, Python) correct/plausible fixes in Table 4.
- Fig. 8 illustrates self-directed debugging on the Lang-6 bug: TSAPR's patch changes the index to `pos + 1` (incorrect), while DebugRepair's instrumented runtime trace pinpoints the out-of-range location and yields a bounds-guarded correct patch.
- DebugRepair can be utilized by ReinFix for patch refinement because their working mechanisms are orthogonal.
- TSAPR shares the execution-feedback paradigm with ChatRepair, ContrastRepair, and DebugRepair, but TSAPR uses feedback to guide MCTS patch exploration whereas the latter three directly iteratively refine a given candidate patch, making them orthogonal as well.

## 11. [[wiki/11-comparison-and-generality|Comparison, Orthogonality to TSAPR, and Generality Across LLMs]]
**In one sentence:** DebugRepair's refinement-oriented self-directed debugging outperforms ChatRepair, ContrastRepair, ReinFix and TSAPR on complex repairs, stays competitive or leading on single-line bugs, and lifts every tested LLM by 51.3% on average while remaining orthogonal to ReinFix/TSAPR for future integration.
- On Defects4J-V1.2 complex bugs (GPT-3.5 backbone), DebugRepair correctly fixes 111 SF and 82 SH bugs versus ChatRepair (75 SF, 69 SH) and ContrastRepair (76 SF, 79 SH).
- On QuixBugs, DebugRepair fixes 100% of SF and SH bugs, and achieves a 100% fix rate across both Java and Python versions (predominantly SL bugs).
- With DeepSeek-V3, DebugRepair fixes 139 SF (V1.2) and 156 SF (V2.0) versus ReinFix (118 and 118) and TSAPR (108 and 116); on SH it fixes 98 and 113 versus second-ranked ReinFix (83 and 89).
- On Single-Line bugs with GPT-3.5, DebugRepair gets 55 (V1.2) and 50 (V2.0) fixes — neck-and-neck on V1.2 behind ChatRepair and TSAPR (57 each), surpassing all baselines on V2.0; with DeepSeek-V3 it gets 57 (V1.2, behind ContrastRepair's 60) and 61 (V2.0, versus ReinFix's 47).
- Across five LLMs, DebugRepair improves correct fixes by 51.3% on average: Qwen2.5-7B +21 (86→107), Qwen2.5-32B +71 (124→195), Qwen2.5-Coder-7B +30 (111→141), GPT-3.5 142→224, DeepSeek-V3 155→295 (+140).
- Gains scale with size (Qwen2.5-32B +71 vs 7B +21), favor code models over general models at the same scale (Coder-7B +30 vs 7B +21; enhanced Coder-7B's 141 approaches vanilla GPT-3.5), and favor stronger reasoning models (DeepSeek-V3 +140 vs GPT-3.5's stated +74); hierarchy is commercial > code > general.
- DebugRepair targets patch refinement through dynamic execution states, making it highly orthogonal to ReinFix and TSAPR and integrable for further improvement; on SL bugs its print-statement traces can lengthen context and slightly hinder pattern-matching on outcome-level symptoms.

## 12. [[wiki/12-ablation-test-purification|Ablation: Effectiveness of Test Purification]]
**In one sentence:** Removing test semantic purification drops correct fixes from 224 to 164 (a 26.8% decrease) because unpurified failing tests contain irrelevant scenarios that produce redundant runtime output, and purification cuts the average runtime-output token count by 18.6%.
- Removing test semantic purification reduces the number of correct fixes from 224 to 164, a 26.8% decrease.
- Real-world failing tests often contain irrelevant test scenarios that obscure the failure-triggering logic.
- Those irrelevant scenarios bring about redundant runtime outputs collected from the inserted print statements.
- Applying test purification reduces the average token count of collected runtime output by 18.6% versus the unpurified setting.
- The token reduction was measured quantitatively on the runtime output collected from print statements during the repair process.
- Purification minimizes redundant runtime outputs, ensuring the concentration of LLMs during bug fixing.
- The paper's joint RQ4 answer states that removing any single module drops correct fixes by 19.9%–26.8%, proving all components are jointly essential.

## 13. [[wiki/13-ablation-repair-rounds|Ablation on Repair Rounds and Budget Hyperparameters]]
**In one sentence:** This chunk reports hyperparameter sensitivity (debugging sessions, repair rounds, augmentation budget), a cost comparison where DebugRepair is cheapest per bug, threats-to-validity mitigations, related-work positioning, and the paper's conclusion.
- Fig. 9(a) plots repair performance over Number of Debugging Sessions (Nsession, x-axis 1–10) for Repair Rounds Kround = 1 through 5 (y-axis 80–140 fixes).
- Fig. 9(b) plots Number of Correct Fixes (y-axis 160–240) over Augmentation Numbers (x-axis 0–20).
- DebugRepair uses 32 patches/bug, 38,000 tokens/bug, and $0.036 money/bug — the lowest cost on all three per-bug metrics in Table 8.
- Comparators in Table 8: ChatRepair 500 patches / 210,000 tokens / $0.42 (2024) or $0.14 (today's price); RepairAgent 117 / 270,000 / $0.14; TSAPR 32 / 40,000 / $0.06; ReinFix 45 / no token figure ("-") / $0.06.
- The chunk claims DebugRepair "achieves this superior cost-efficiency while simultaneously delivering a higher number of correct fixes, demonstrating the ability of the proposed framework to yield SOTA performance at a significantly lower budget."
- Construct-validity threat (subjective manual patch-correctness judgment) is mitigated by independent double-blind review by two researchers plus a third arbitrator on disagreement until consensus.
- Internal-validity threat (data leakage from LLM pretraining) is mitigated by evaluation on HumanEval-Java, released after GPT-3.5's training cutoff, with consistent gains attributed to design rather than memorization.
- External-validity threat (generalizability) is addressed via three benchmarks (Defects4J, QuixBugs, HumanEval-Java) across Java and Python; SWE-bench is intentionally excluded because its default setting denies APR tools explicit test cases, rendering DebugRepair inapplicable.

## 14. [[wiki/14-conclusion-and-references-a|Conclusion and References (Part A: [1]–[32])]]
**In one sentence:** This chunk contains no conclusion prose — only the first half of the bibliography (references [1]–[32]), spanning model/infrastructure sources, classic APR methods, and recent LLM-based APR work.
- The chunk lists references [1]–[32] verbatim, with no conclusion, discussion, or open-science text present in the chunk body.
- References [1]–[3] are online sources: OpenAI Models docs (accessed 2026-01-20), SiliconFlow (accessed 2026-01-20), and tree-sitter (accessed 2026-03-13).
- References [4]–[11] cover recent LLM/agent-based APR work, including RepairAgent (2024), APRMCTS (2025), TSAPR (2025), and ContrastRepair (2025).
- References [12]–[25] cover classic and learning-based APR foundations: GenProg (2011), Defects4J (2014), Angelix (2016), Sequencer (2019), TBar (2019), and CURE/DLFix/DEAR/KNOD (2020–2023).
- References [26]–[32] cover benchmarks (QuixBugs 2017, SWE-bench 2023) and template/condition-based repair (Avatar 2019, Staged repair 2015, Astor 2016, RAP-Gen 2023).
- The chunk also carries journal page furniture ("J. ACM, Vol. 37, No. 4, Article 111", "111:26 Wu et al.", "111:27" running head) rather than paper content.
- Note: the planned page scope mentions a conclusion and open-science note, but neither appears in this chunk, so they are not summarised here.

## 15. [[wiki/15-references-b|References (Part B: [33]–[51])]]
**In one sentence:** This chunk contains only the second half of the bibliography (references [33]–[51]) plus journal page furniture, with no body prose, results, or discussion.
- The chunk lists references [33]–[51] verbatim, with no paper body, conclusion, or evaluation content present.
- References [33]–[36] cover interactive/debugging-driven and survey work on LLM repair: InspectCoder (2026), context-aware patch generation (2018), plastic surgery hypothesis in the LLM era (2023), and APR in the era of pre-trained models (2023).
- References [37]–[38] are zero-shot and conversational ChatGPT-based APR by Xia and Zhang (2022, 2024), including fixing 162 out of 337 bugs for $0.42 each.
- References [39]–[43] cover Xue et al. and Yang et al. work on code translation (ClassEval-T 2025, TransLibEval 2025), metamorphic robustness of LLM-powered APR (2024), commit message generation (2024), and LLM code translation (FSE 2024).
- References [44]–[47] cover an LLM security/privacy survey (2024), SelfAPR self-supervised repair with test diagnostics (2022), execution-based backpropagation repair (2022), and ThinkRepair self-directed APR (2024).
- References [48]–[51] cover repair-ingredients search (2025), a learning-based APR survey (2023), and a syntax-guided edit decoder (2021).
- The chunk also carries journal page furniture ("Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009" and "J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018") rather than paper content.

## The argument in five moves
1. Outcome-level failure symptoms (e.g., stack traces) hide intermediate runtime states, so feedback-based LLM repair misdiagnoses bugs and masks symptoms instead of fixing root causes (Chart-24).
2. Test semantic purification backward-slices the failing test to the minimal failure-triggering context plus helper/field dependencies, cutting noise and redundant runtime output.
3. Simulated instrumentation has the LLM insert targeted print statements guarded by consistency checks (with a rule-based AST fallback), and executing it yields runtime traces exposing data-flow root causes.
4. Debugging-driven conversational repair iteratively refines patches in inner repair rounds using trace plus failure history, starts fresh debugging sessions on exhaustion, and augments the first plausible patch into validated variants.
5. Across Defects4J, QuixBugs, and HumanEval-Java, DebugRepair beats SOTA baselines (224 GPT-3.5 / 295 DeepSeek-V3 Defects4J fixes), generalizes across LLMs (+51.3%), ablates cleanly, and stays cheapest per bug.
