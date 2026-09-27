> [[index|Wiki]] | [[summary|Summary]]
# PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices — Digest

## 1. [[wiki/01-introduction-and-context|Introduction and Context]]
**In one sentence:** PracRepair is proposed as a fully automated LLM-based APR framework inspired by human-like debugging that uses on-demand static-dynamic context, question-driven diagnosis, and validation/trace-level patch refinement to outperform prior static- and retrieval-driven approaches.
## Key points
- Existing LLM-based APR approaches "still largely rely on static or retrieved context, error messages, and coarse-grained validation outcomes," underutilizing failure-execution dynamics and patch-validation dynamics.
- Leveraging dynamic information is challenging because "failure-execution traces are large and noisy, raw static-dynamic context is not self-explanatory, and patch-validation dynamics are often reduced to coarse feedback."
- PracRepair constructs "an on-demand static-dynamic context from buggy programs and failure executions," performs "question-driven failure diagnosis to formulate explicit repair hypotheses," and "iteratively refines candidate patches using validation diagnostics and trace-level behavioral changes."
- Under GPT-3.5, PracRepair "correctly fixes 139/136 bugs on Defects4J V1.2/V2.0," and under GPT-4o it "further improves to 162/171."
- PracRepair "generalizes effectively to RWB (Real-World Bugs), achieving the best performance across multiple foundation models."
- Real-world defects' "causes and effects ... often extend beyond a single function and require reasoning over non-local contextual information, such as call relationships, data dependencies, and execution logic."
- Developers "spend roughly 35% to 50% of their time, and 50% to 75% of project budgets, on testing, verification, and debugging, costing over 100 billion dollars each year."
- Early APR "mainly relied on manually designed fix patterns or bug-fixing datasets" and was "constrained by limited pattern coverage, strong data dependence, and weak generalization ability," while recent methods (ChatRepair, ThinkRepair, RepairAgent, ReInFix) improved Defects4J results but still underutilize dynamic information.

## 2. [[wiki/02-limitations-of-prior-apr|Limitations of Prior APR]]
**In one sentence:** Existing LLM-based repair is still largely driven by static or retrieved context, error messages, and coarse-grained validation outcomes, missing the failure-execution and patch-validation dynamics that PracRepair targets with three mapped stages.
## Key points
- Prior repair processes are "still largely driven by static or retrieved context, error messages, and coarse-grained validation outcomes."
- They do not systematically exploit two dynamic information types: failure-execution dynamics (executed paths, runtime states, branch outcomes showing how the failure is triggered) and patch-validation dynamics (how a candidate patch changes behavior during validation).
- Without these signals, LLMs "may miss root causes or generate incomplete and overfitted fixes, especially for bugs whose root causes depend on runtime states and value evolution."
- C1: failure-execution dynamics are large and noisy — "Directly exposing complete traces to the LLM may overwhelm the repair context rather than help identify failure-relevant behavior."
- C2: raw static-dynamic context is not self-explanatory — the LLM must determine "which runtime states matter and how they relate to the faulty logic; otherwise, it may make incorrect behavioral inferences."
- C3: patch-validation dynamics are often underused — "frequently reduced to coarse validation outcomes, such as pass/fail results or error messages," leaving iterations without fine-grained evidence of what changed and why the patch still fails.
- PracRepair maps one stage to each challenge: (1) static-dynamic context construction for C1, (2) question-driven failure diagnosis for C2, (3) feedback-guided patch refinement for C3.
- Reported results: under GPT-3.5 PracRepair fixes 139 bugs on Defects4J V1.2 and 136 on V2.0; under GPT-4o 162 and 171 respectively, including "75 unique correct fixes achieved … with GPT-3.5 and 93 unique correct fixes under GPT-4o when compared with ReInFix."

## 3. [[wiki/03-motivating-example-static-repair|Bug Information & A. Repairing with Static]]
**In one sentence:** The chunk presents the Compress-21 `writeBits` bug information (failing test, failure message, and buggy code) and shows the static-only repair attempt that reasons from program context and targeted questions without execution traces.
## Key points
- The failing test is `testSevenEmptyFiles`, which calls `testCompress252(7, 0)`, and the reported failure is `java.io.IOException: Unknown property 128`.
- The buggy method is `writeBits(final DataOutput header, final BitSet bits, final int length)`, initialized with `int cache = 0` and `int shift = 7`.
- The in-loop logic does `cache |= ((bits.get(i) ? 1 : 0) << shift)`, then `--shift`, and flushes with `if (shift == 0) { header.write(cache); shift = 7; cache = 0; }`.
- The after-loop logic flushes leftovers with `if (length > 0 && shift > 0) { header.write(cache); }`.
- The static-context repair task is framed as `## Task: generate a corrected patch...` with `## Input: Bug_Info, Program_Context`.
- The static program context supplies `testCompress252`, imports (`DataOutput`, `DataOutputStream`, `File`, `org.apache.commons.compress.archivers`), `writeFileEmptyFiles`, the `writeBits(out, emptyFiles, emptyStreamCounter)` call, and `out.flush()`.
- Diagnosis in this pane answers `What are cache and shift when if (shift == 0) is entered?` with `When branch is entered, cache = 254 and shift = 0 after i = 6`.
- The static repair proposes masking and a final-flush change: `Writing cache directly may produce invalid data, so use cache & 0xFF to keep only the lower 8 bits`, and `Change 'shift > 0' to 'shift < 8' to ensure any remaining cached bits are flushed after writing`, yielding `if (length > 0 && shift < 8 ) { header.write(cache); }`.

## 4. [[wiki/04-dynamic-traces-and-diagnosis|Dynamic Traces and Diagnosis]]
**In one sentence:** Static context and pass/fail validation alone leave repairs stuck on symptoms, so PracRepair motivates static-dynamic context construction (Stage I), question-driven diagnosis (Stage II), and feedback-guided refinement (Stage III).
## Key points
- Static-only repair changes `header.write(cache)` to `header.write(cache & 0xFF)` but still fails with the same error `Unknown property 128`.
- The Dynamic Execution Trace panel shows how `cache` and `shift` evolve across loop iterations and exposes the runtime state where the failure is triggered.
- Full execution traces can contain many irrelevant calls, branches, and state changes that would overwhelm the LLM, motivating static-dynamic context construction in Stage I.
- Raw static-plus-dynamic context is not self-explanatory (C2): even with dynamic evidence, the model still must determine which runtime states matter, as illustrated in the B. Repairing with Static + Dynamic Context panel.
- Question-driven diagnosis uses targeted questions such as cache/shift values when `if (shift == 0)` is entered and how the in-loop flush condition should change, focusing the model on the premature flush and motivating Stage II.
- Validation feedback is often reduced to coarse pass/fail or error messages (C3); the initial patch `if (shift == 0)` to `if (shift < 0)` removes `Unknown property 128` but introduces `Badly terminated header`.
- PracRepair instead extracts structured validation feedback — validation diagnostic, code diff, and trace diff — revealing the post-loop write is inconsistent with the updated in-loop flush, localizing the issue to the final flush condition and yielding the passing patch `if (length > 0 && shift < 7)`.

## 5. [[wiki/05-framework-overview-three-stages|Framework Overview: Repair Hypothesis and Validation Feedback]]
**In one sentence:** PracRepair runs a budgeted diagnosis loop that asks one diagnostic question at a time and a budgeted refinement loop that updates the repair hypothesis from failed patches, both grounded in a statically-plus-dynamically built context accessed on demand.
## Key points
- The diagnosis loop updates QA history one diagnostic question at a time and stops when no further question is needed or the diagnosis budget is exhausted.
- The refinement loop updates the repair hypothesis using feedback from failed candidate patches and stops when a plausible patch is found or the refinement budget is exhausted.
- Diagnosis and refinement budgets are set to 10 and 3 respectively, and both serve as upper bounds rather than mandatory numbers of rounds.
- Static context is built by parsing the project with Joern and constructing a Code Property Graph unifying AST, CFG, and data-dependence relations to expose classes, methods, statements, control branches, call edges, and variable definition–use chains.
- Dynamic context is collected by non-intrusive bytecode instrumentation with JavaAgent and ASM, executing triggering tests and recording per-statement sequence, in-scope variable values, and conditional branch outcomes scoped to the buggy function.
- Object-type variable fields are recursively serialized up to a depth of 3 to balance contextual richness and token efficiency, and evidence is organized into an Execution Trace Table per <triggering test, buggy function> pair.
- Static and dynamic context are not given to the LLM all at once but exposed through a uniform on-demand retrieval interface, avoiding overload from full project context and long traces while following the current diagnostic need.

## 6. [[wiki/06-static-dynamic-context-construction|Question-driven Failure Diagnosis and Repair Hypothesis]]
**In one sentence:** PracRepair transforms collected static and dynamic evidence into diagnostic understanding by iteratively asking one what/why/how question at a time, answering it via the unified context interface, and summarizing the QA history into a structured four-field repair hypothesis that feeds iterative patch refinement.
## Key points
- Stage II does not generate a patch directly from Stage III-A context; it first builds diagnostic understanding through question-driven failure diagnosis.
- Each round raises one diagnostic question, retrieves evidence to answer it, and appends a QA pair recording question, retrieved evidence, diagnostic answer, and repair implication.
- What-type questions establish factual understanding of the failing execution (executed statements, branch outcomes, variable evolution, deviations), mainly using dynamic evidence.
- Why-type questions connect abnormal runtime behavior to program logic (incorrect control flow, abnormal state transitions, invalid data dependencies), using both static and dynamic evidence.
- How-type questions determine how to change the faulty logic to restore intended semantics, mainly using the diagnosed root cause and static code context.
- Question answering interleaves reasoning and retrieval in a ReAct-inspired loop until enough evidence is collected, and validation feedback from Stage III is incorporated to re-diagnose patch behavior.
- The repair hypothesis has four fields — faulty behavior, supporting evidence, suspected root cause, modification suggestion — and serves as the output of Stage II and input to Stage III.
- Stage III turns the hypothesis into an iterative loop that analyzes behavioral differences before and after patching and feeds unsuccessful-validation feedback back into Stage II.

## 7. [[wiki/07-question-driven-diagnosis-and-refinement|Question-Driven Diagnosis and Refinement]]
**In one sentence:** PracRepair refines the repair hypothesis in a feedback-guided loop of at most 3 rounds — generating a hypothesis-guided patch, validating it by compilation and test execution, and feeding categorized failure outcomes plus diagnostics, code diff, and trace diff back into question-driven re-diagnosis until a plausible patch is found or the budget is exhausted.
## Key points
- The refinement loop continues until the maximum of 3 refinement rounds is reached, or terminates earlier once a plausible patch is found.
- Patch generation uses a structured zero-shot prompt with three parts — bug context (buggy function, triggering tests, failure information), repair hypothesis (suspected root cause and modification suggestions), and a generation instruction to produce a corrected implementation — with no in-context examples.
- Patch validation applies the candidate patch, compiles and executes tests, and collects patched-program execution traces with the same trace-collection procedure as Section III-A so patched behavior can be compared with the original failing execution.
- A patch is regarded as plausible only if the patched program compiles successfully and passes all tests within the maximum execution time of 10 minutes.
- Failed validation is categorized into four outcomes: (1) compilation failures, (2) runtime failures (compiles but triggers runtime exceptions or timeouts), (3) remaining failures (originally failing tests still not fixed), and (4) regression failures (original failure resolved but previously passing tests now fail).
- Each failure yields three complementary feedback forms: validation diagnostics (compiler errors, runtime exceptions, timeout messages, updated failing tests), code diff (patch vs. original buggy function), and trace diff (aligned by executed statement and execution order; changed branch outcomes, added or removed statement executions, divergent runtime values).
- The extracted feedback is fed back into Question-driven Failure Diagnosis as optional diagnostic input (Figure 2), where the LLM re-diagnoses from original bug context plus accumulated QA history plus new feedback, and the resulting QA pairs refine the repair hypothesis for the next generation–validation round.

## 8. [[wiki/08-evaluation-design-and-rq1|Evaluation Design and RQ1: Fault-Localization Settings and Repair Effectiveness]]
**In one sentence:** PracRepair is evaluated on Defects4J under both perfect fault localization (exact buggy statement locations provided) and a relaxed setting where they are not, using GPT-3.5-turbo and GPT-4o with reused baseline results and plausible/correct patch counts.
## Key points
- Main experiments use gpt-3.5-turbo and gpt-4o at sampling temperature 1.0 for direct comparability with prior APR studies, with gpt-4, Llama-3, and DeepSeek-v3 deferred to RQ4 generalizability.
- Each bug gets at most 3 independent repair sessions from the original bug context, with the diagnosis loop capped at 10 rounds (averaging no more than 5, terminating when no further diagnostic questions arise) and the refinement loop capped at 3 rounds.
- All experiments ran on Ubuntu 20.04 with a 16-core Intel Xeon processor, 192GB RAM, and eight NVIDIA A800 GPUs.
- Nine baselines are compared (TBar; SelfAPR, KNOD, Tare; Codex, AlphaRepair, ChatRepair, ThinkRepair, RepairAgent, ReinFix), reusing results reported in their original papers because the benchmark split, fault-localization setting, and metrics match.
- Effectiveness is measured as number of plausible patches (pass all developer-written tests, not necessarily correct) and number of correct patches (matches developer fix or is manually judged semantically equivalent).
- Under perfect fault localization, PracRepairGPT-3.5 produces 275 correct / 332 plausible fixes and PracRepairGPT-4o produces 333 correct / 413 plausible fixes summed over Defects4J (Table III).
- Under the relaxed no-perfect-FL setting on Defects4J V1.2, PracRepairNo-PFL achieves 105 correct / 133 plausible fixes, versus ThinkRepairNo-PFL at 80 correct and Codex at 63 (Table IV).

## 9. [[wiki/09-main-repair-results|TABLE V: Repair results (correct fixes)]]
**In one sentence:** PracRepair tops all baselines on correct-fix counts on Defects4J V1.2 and V2.0, holds unique-fix and cross-project breadth, and stays ahead of baselines even without perfect fault localization.
## Key points
- On Defects4J V1.2, PracRepair GPT-4o reaches 135 correct fixes and PracRepair GPT-3.5 reaches 120, beating ReInFix GPT-4o (124) and ReInFix GPT-3.5 (104) by 16 and 21 fixes respectively.
- On Defects4J V2.0, PracRepair GPT-4o reaches 153 correct fixes and PracRepair GPT-3.5 reaches 121, beating ReInFix GPT-4o (130) and ReInFix GPT-3.5 (109) by 26 and 13 bugs respectively.
- Under GPT-3.5 on Defects4J V1.2, PracRepair also surpasses ChatRepair, ThinkRepair, and RepairAgent.
- PracRepair fixes bugs across all Defects4J projects — Chart, Closure, Lang, Math, Mockito, and Time — showing effectiveness across different domains.
- Unique-fix analysis (Figure 3): under GPT-3.5 PracRepair has 75 unique correct fixes vs 29 (ThinkRepair), 26 (RepairAgent), 12 (ChatRepair); under GPT-4o it has 93 vs 51 (ReInFix).
- Without exact buggy-statement locations, PracRepairNo-PFL fixes 105 bugs correctly with 133 plausible patches, below the perfect-localization GPT-3.5 result (139 correct, 167 plausible) but ahead of ThinkRepairNo-PFL by 25 and Codex by 42 correct fixes.
- Semantically correct results show PracRepair not only satisfies the test oracle on many bugs but also achieves strong repair accuracy, complementing prior methods rather than duplicating them.

## 10. [[wiki/10-generalization-rwb-results|Generalization on RWB, Repair Scenarios, Ablation and Repair Costs]]
**In one sentence:** PracRepair stays robust across SL/SH/SF/MF scenarios with its strongest edge on multi-function bugs, gains cumulatively from all three stages plus dynamic traces, question-driven diagnosis and three refinement rounds, generalizes on RWB across foundation models, and does so at lower per-bug cost than baselines.
## Key points
- In the single-function (SF) setting PracRepair is best overall: on Defects4J V1.2 GPT-3.5 repairs 120 and GPT-4o repairs 135 bugs, and on Defects4J V2.0 the numbers rise to 121 and 153, consistently exceeding all baselines.
- In single-hunk (SH) and single-line (SL) settings PracRepair matches or surpasses recent LLM-based baselines, and in multi-function (MF) it beats ReInFix, the only other MF-capable baseline: PracRepair GPT-4o repairs 27 MF bugs on V1.2 and 18 on V2.0 versus 22 and 15 for ReInFix GPT-4o.
- Ablation on Defects4J V1.2 with GPT-3.5 (Table VI, correct/plausible): w/o SDC+QFD+FPR 84/98, w/o SDC+QFD 105/113, w/o SDC 115/126, full PracRepair 139/167, showing refinement, then diagnosis, then static-dynamic context each add gains.
- Removing dynamic execution traces (w/o DI) drops correct patches from 139 to 120 and plausible patches from 167 to 137, indicating traces expose executed paths, branch outcomes and variable-state changes not recoverable from static context alone.
- Reasoning strategy: one-shot CoT without function calls yields 107 correct patches, on-demand retrieval with ReAct raises this to 121, and full question-driven diagnosis reaches 139, showing benefit beyond tool use alone via targeted questions and systematic hypothesis formulation.
- Refinement rounds (Figure 4): 89 correct patches with no refinement, 107 after one round, 119 after two, 139 after three, then unchanged with more interactions, so three rounds is adopted as default balancing effectiveness and interaction cost.
- On the unseen RWB benchmark (Table VII) PracRepair generalizes across GPT-4/GPT-3.5, DeepSeek-v3/DeepSeek-Coder and Llama-3, and on cost it stays efficient: GPT-3.5 $0.04 per repaired bug versus ReInFix $0.06, RepairAgent $0.14 and ChatRepair $0.42, and GPT-4o $1.13 versus ReInFix GPT-4o $1.45.

## 11. [[wiki/11-ablation-and-rq3|Answer to RQ3: PracRepair]]
**In one sentence:** All three PracRepair stages — Static-dynamic Context Construction, Question-driven Failure Diagnosis, and Feedback-guided Patch Refinement — integrate effectively to improve correct repair effectiveness, and the approach generalizes across RWB benchmarks and foundation models.
## Key points
- Answer to RQ3 states all three stages (Static-dynamic Context Construction, Question-driven Failure Diagnosis, Feedback-guided Patch Refinement) can be effectively integrated to improve correct repair effectiveness.
- RQ4 generalizability study evaluates PracRepair on the RWB benchmark under the perfect fault localization setting, following ThinkRepair [27].
- PracRepair is instantiated with GPT-4, GPT-3.5, DeepSeek-v3, DeepSeek-Coder, and Llama-3, and compared against published ThinkRepair [27] and ReInFix [28] results on the same benchmark.
- On RWB V1.0 (44 bugs), PracRepair repairs 23 bugs with GPT-4 and DeepSeek-v3, outperforming ReInFix (21 with GPT-4) and ThinkRepair (19 with GPT-3.5); it also repairs 22 with Llama-3 and 21 with GPT-3.5.
- On RWB V2.0 (29 bugs), PracRepair repairs 13 bugs with DeepSeek-Coder, compared with 12 by ReInFix and 10 by ThinkRepair.
- Results are described as best or tied-best across both RWB datasets and all evaluated model settings, including competitive effectiveness with open-source models, indicating generalization rather than dependence on a specific dataset or model family.
- Internal threats are manual validation of plausible patches (exact match to developer fix, else manual semantic-equivalence check per prior APR work) and potential data leakage, mitigated by RWB evaluation on post-training-cutoff commits with strong results across models.
- External threat is evaluation on Defects4J and RWB, two real-world Java benchmarks that may not represent other languages or much larger codebases; broader evaluation remains future work.

## 12. [[wiki/12-related-work|Related Work — Pipelines and Similar Code Fragments]]
**In one sentence:** The chunk positions PracRepair against prior repair pipelines that retrieve similar code fragments as repair ingredients, task-specific learning-based methods, and prompt-based / iterative / agent-based LLM repair, then concludes with PracRepair's static-dynamic, question-driven, feedback-guided design and future multi-language extension.
## Key points
- Prior pipelines retrieve similar code fragments as repair ingredients [51], [52].
- Beyond functional bugs, prior studies also address syntax errors, performance bugs, vulnerabilities, type errors, and build failures [53], [54].
- Early learning-based methods use machine learning to rank or prioritize candidate patches [55].
- More recent learning-based approaches adopt neural machine translation to directly transform buggy code into fixed code [56], [57], or predict tree-level / syntax-aware code transformations [58], [59].
- Some methods train repair-specific models on curated bug-fix datasets [19], [60], unlike LLM-based APR which uses general-purpose foundation models without explicit repair-specific training.
- Early LLM-based APR relies on prompt engineering for one-shot repair generating a candidate patch in a single interaction [24], [45], [61]; later methods add iterative repair with validation feedback across rounds [12], [25], [27]; agent-based methods let the LLM invoke external tools [26], [28].
- PracRepair differs by structuring repair around static-dynamic information integration, question-driven failure diagnosis, and feedback-guided patch refinement.
- Extensive experiments with state-of-the-art baselines, scenario-based analysis, and ablation studies show PracRepair consistently outperforms existing methods, with future work extending to more languages.

## 13. [[wiki/13-conclusion-and-references|Conclusion and References]]
**In one sentence:** This chunk is the paper's bibliography tail (references [24]–[61] plus the ICSE '24 venue line), listing the LLM-based, learning-based, and classic APR works cited by PracRepair.
## Key points
- Xia and Zhang [24] revisit APR via zero-shot learning (ESEC/FSE 2022, pages 959–971) under the title "Less training, more repairing please".
- Xia and Zhang [25] report conversation-based repair fixing "162 out of 337 bugs for $0.42 each using chatgpt" (ISSTA 2024, pages 819–831).
- Bouzenia, Devanbu, and Pradel [26] present "Repairagent: An autonomous, llm-based agent for program repair" (ICSE '25, pages 2188–2200).
- Yin et al. [27] present "Thinkrepair: Self-directed automated program repair" (ISSTA 2024, pages 1274–1286).
- Zhang et al. [28] propose improving LLM-based repair "via repair ingredients search" (2025 preprint).
- Huang et al. [29] survey "Evolving paradigms in automated program repair: Taxonomy, challenges, and opportunities" (ACM Comput. Surv., 57(2), October 2024).
- Kolak et al. [30] study "Patch generation with language models: Feasibility and scaling behavior" (Deep Learning for Code Workshop, 2022).
- The tail [44]–[61] spans classic and neural repair baselines cited by the paper, from GenProg [46] and SemFix [49] through SequenceR-style NMT repair [57], DLFix [59], and execution-based backpropagation [60] to the ICSE '23 LLM impact study [61].

## The argument in five moves
1. Human debugging is non-local, evidence-driven, and iterative, but existing LLM-based APR still relies on static/retrieved context, error messages, and coarse pass/fail signals, missing failure-execution and patch-validation dynamics.
2. The Compress-21 `writeBits` example shows why: static-only reasoning patches symptoms (`cache & 0xFF`) yet still fails with `Unknown property 128`, while execution traces expose the premature-flush runtime behavior that a correct fix must address.
3. PracRepair therefore builds an on-demand static-dynamic context (Joern CPG plus JavaAgent/ASM traces with a uniform retrieval interface) and converts it into understanding via budgeted what/why/how question-driven diagnosis that yields an explicit four-field repair hypothesis.
4. That hypothesis drives a budgeted feedback-guided refinement loop (zero-shot generation, compilation plus 10-minute test validation, four failure categories with diagnostics/code-diff/trace-diff fed back into re-diagnosis) that resolves follow-on failures such as `Badly terminated header` into the passing `shift < 7` fix.
5. Across Defects4J, scenarios, ablations, RWB generalization, and cost, every stage adds correct fixes (up to 139/136 on GPT-3.5 and 162/171 on GPT-4o, plus unique-fix, MF, and cross-model breadth at lower per-bug cost), positioning static-dynamic integration with question-driven diagnosis and feedback-guided refinement as the advance over one-shot, iterative, and agent-based predecessors.
