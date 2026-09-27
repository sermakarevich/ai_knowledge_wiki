---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices

### Q1. What gap in existing LLM-based APR motivates PracRepair, and what cost figures justify automating debugging?
> [!tip]- Answer
> Existing LLM-based APR still largely relies on static or retrieved context, error messages, and coarse-grained validation outcomes, underutilizing failure-execution and patch-validation dynamics. Developers spend roughly 35–50% of their time and 50–75% of project budgets on testing, verification, and debugging, costing over $100 billion yearly. Real-world defect causes and effects often extend beyond a single function, requiring non-local reasoning over calls, data dependencies, and execution logic. See [[wiki/01-introduction-and-context|Introduction and Context]].

### Q2. What are the three challenges (C1–C3) in using dynamic information, and which PracRepair stage addresses each?
> [!tip]- Answer
> C1 is that failure-execution traces are large and noisy, so exposing complete traces overwhelms the repair context. C2 is that raw static-dynamic context is not self-explanatory, so the model may make incorrect behavioral inferences about which runtime states matter. C3 is that patch-validation dynamics are reduced to coarse pass/fail or error messages without fine-grained evidence of what changed. Stage 1 (static-dynamic context construction) maps to C1, Stage 2 (question-driven diagnosis) to C2, and Stage 3 (feedback-guided refinement) to C3. See [[wiki/02-limitations-of-prior-apr|Limitations of Prior APR]].

### Q3. In the Compress-21 `writeBits` example, what is the failing test, the error, and the static-only proposed fix?
> [!tip]- Answer
> The failing test is `testSevenEmptyFiles` calling `testCompress252(7, 0)`, with failure `java.io.IOException: Unknown property 128`. The buggy method initializes `cache = 0` and `shift = 7`, accumulates bits with `cache |= ((bits.get(i) ? 1 : 0) << shift)`, and flushes in-loop at `shift == 0` plus a post-loop `if (length > 0 && shift > 0)` flush. The static-only repair masks the write as `header.write(cache & 0xFF)` and changes the final condition to `shift < 8`, reasoning without execution traces. See [[wiki/03-motivating-example-static-repair|Bug Information & A. Repairing with Static]].

### Q4. Why does the static-only patch fail, and what sequence of patches leads to the passing fix?
> [!tip]- Answer
> The static-only change to `header.write(cache & 0xFF)` addresses only the symptom and still fails with `Unknown property 128`, since it lacks the runtime evolution of `cache` and `shift`. The dynamic trace exposes the premature-flush behavior, while question-driven diagnosis focuses the model on the in-loop flush condition. An initial patch changing `shift == 0` to `shift < 0` removes the original error but introduces `Badly terminated header`, and structured trace-diff feedback then localizes the inconsistency to the final flush, yielding the passing `if (length > 0 && shift < 7)`. See [[wiki/04-dynamic-traces-and-diagnosis|Dynamic Traces and Diagnosis]].

### Q5. How does PracRepair build static and dynamic context, and how is it exposed to the LLM?
> [!tip]- Answer
> Static context is built by parsing the project with Joern into a Code Property Graph unifying AST, CFG, and data-dependence relations, exposing classes, methods, branches, call edges, and definition–use chains. Dynamic context is collected by non-intrusive JavaAgent/ASM bytecode instrumentation of triggering tests, recording per-statement sequences, in-scope variable values, and branch outcomes scoped to the buggy function, with object fields serialized to depth 3 into an Execution Trace Table. Neither is dumped at once; both are exposed through a uniform on-demand retrieval interface (e.g. `get_execution_path`, `get_runtime_values`, `get_state_at_statement`) guided by diagnostic need. See [[wiki/05-framework-overview-three-stages|Framework Overview: Repair Hypothesis and Validation Feedback]].

### Q6. What are the what/why/how diagnostic questions, and what does the resulting repair hypothesis contain?
> [!tip]- Answer
> What-questions establish facts of the failing execution (statements, branch outcomes, variable evolution) mainly from dynamic evidence; why-questions link abnormal runtime behavior to program logic using both static and dynamic evidence; how-questions decide how to change faulty logic using the root cause plus static context. Each round raises exactly one question, answers it via ReAct-style interleaved retrieval, and appends a QA pair of question, evidence, answer, and repair implication. The QA history is summarized into a four-field hypothesis: faulty behavior, supporting evidence, suspected root cause, and modification suggestion, which feeds Stage III. See [[wiki/06-static-dynamic-context-construction|Question-driven Failure Diagnosis and Repair Hypothesis]].

### Q7. How does the feedback-guided refinement loop generate, validate, and re-diagnose patches?
> [!tip]- Answer
> Patch generation uses a structured zero-shot prompt of bug context, repair hypothesis, and generation instruction with no in-context examples. Validation applies the patch, compiles, runs tests with a 10-minute limit, and collects patched traces the same way as the original, calling a patch plausible only if everything compiles and passes. Failures split into compilation, runtime, remaining, and regression outcomes, each yielding validation diagnostics, a code diff, and an aligned trace diff of branch, statement, and value changes. That feedback re-enters question-driven diagnosis to refine the hypothesis for up to 3 rounds. See [[wiki/07-question-driven-diagnosis-and-refinement|Question-Driven Diagnosis and Refinement]].

### Q8. What is the evaluation design: models, budgets, baselines, and the plausible-vs-correct metric?
> [!tip]- Answer
> Main experiments use gpt-3.5-turbo and gpt-4o at temperature 1.0, with up to 3 independent repair sessions per bug, a diagnosis budget of 10 rounds (averaging ≤5), and a refinement budget of 3 rounds on Ubuntu 20.04 hardware. Nine baselines are compared (TBar; SelfAPR, KNOD, Tare; Codex, AlphaRepair, ChatRepair, ThinkRepair, RepairAgent, ReInFix) by reusing published results under matching splits and settings. A plausible patch passes all developer-written tests while a correct patch matches the developer fix or is manually judged semantically equivalent. See [[wiki/08-evaluation-design-and-rq1|Evaluation Design and RQ1: Fault-Localization Settings and Repair Effectiveness]].

### Q9. What are PracRepair's headline Defects4J correct-fix counts and unique-fix results?
> [!tip]- Answer
> On Defects4J V1.2 PracRepair reaches 120 correct (GPT-3.5) and 135 (GPT-4o), beating ReInFix by 21 and 16 fixes; on V2.0 it reaches 121 and 153, beating ReInFix by 13 and 26. It fixes bugs across all projects (Chart, Closure, Lang, Math, Mockito, Time) and holds strong unique fixes: 75 vs 29/26/12 (ThinkRepair/RepairAgent/ChatRepair) under GPT-3.5 and 93 vs 51 (ReInFix) under GPT-4o. Without exact fault locations it still fixes 105 correctly with 133 plausible patches, ahead of ThinkRepairNo-PFL by 25 and Codex by 42. See [[wiki/09-main-repair-results|TABLE V: Repair results (correct fixes)]].

### Q10. How does PracRepair perform across repair scenarios, ablations, refinement rounds, and cost?
> [!tip]- Answer
> PracRepair leads the single-function setting (V1.2: 120/135; V2.0: 121/153) and beats ReInFix, the only other MF-capable baseline, on multi-function bugs (V1.2: 27 vs 22; V2.0: 18 vs 15 under GPT-4o). Ablation on V1.2 GPT-3.5 rises cumulatively from 84/98 (no stages) to 105/113 (+refinement) to 115/126 (+diagnosis) to 139/167 (full), with dynamic traces, question-driven diagnosis over CoT/ReAct, and three refinement rounds (89→107→119→139, then flat) each contributing. It also stays cheaper per repaired bug: $0.04 vs $0.06/$0.14/$0.42 (ReInFix/RepairAgent/ChatRepair) on GPT-3.5 and $1.13 vs $1.45 (ReInFix) on GPT-4o. See [[wiki/10-generalization-rwb-results|Generalization on RWB, Repair Scenarios, Ablation and Repair Costs]].

### Q11. What are the RQ3/RQ4 answers and the stated threats to validity?
> [!tip]- Answer
> RQ3 concludes all three stages integrate effectively to improve correct repairs, and RQ4 finds best or tied-best generalization on post-cutoff RWB: V1.0 23 bugs (GPT-4, DeepSeek-v3) vs 21/19, plus 22 (Llama-3) and 21 (GPT-3.5); V2.0 13 (DeepSeek-Coder) vs 12/10. Internal threats are manual semantic-equivalence judging and possible pre-training data leakage, mitigated by exact-match-first checks and strong post-cutoff RWB results. The external threat is Java-only evaluation on Defects4J and RWB, which may not represent other languages or much larger codebases. See [[wiki/11-ablation-and-rq3|Answer to RQ3: PracRepair]].

### Q12. How does PracRepair differ from the three LLM-based APR paradigms in related work?
> [!tip]- Answer
> Prior LLM repair spans one-shot prompt-engineered repair in a single interaction, iterative repair refining across rounds with validation feedback, and agent-based methods invoking external tools. Earlier learning-based lines instead rank patches, translate buggy to fixed code with NMT, predict tree/syntax-aware edits, or train repair-specific models on curated datasets. PracRepair differs by structuring repair around static-dynamic information integration, question-driven failure diagnosis, and feedback-guided patch refinement, with future work extending to more languages. See [[wiki/12-related-work|Related Work — Pipelines and Similar Code Fragments]].

### Q13. Which cited works anchor the LLM-based, tooling, and classic repair baselines?
> [!tip]- Answer
> LLM anchors include zero-shot repair [24], conversation-based repair fixing 162/337 bugs at $0.42 each [25], RepairAgent [26], ThinkRepair [27], and repair-ingredients search [28], plus the taxonomy [29] and Codex/QuixBugs [31] studies. Tooling and method references cover Joern [32], CPG modeling [33], JavaAgent/ASM instrumentation [34–36], ReAct [37], and the artifact plus GPT-3.5/GPT-4o/Llama-3/DeepSeek model cards [38–45]. Classic and neural baselines span GenProg [46], PAR/Phoenix [47–48], SemFix [49], NMT repair [56–57], DLFix [59], and execution-based backpropagation [60]. See [[wiki/13-conclusion-and-references|Conclusion and References]].

### Q14. Should a team adopt PracRepair's full three-stage workflow for a new Java repair service?
> [!tip]- Answer
> Yes, adopt the full workflow because ablations show each stage adds correct fixes, RWB results show cross-model generalization, and per-bug cost stays below ReInFix, RepairAgent, and ChatRepair. Keep the 10-question diagnosis and 3-round refinement budgets since averages stay under 5 rounds and gains flatten after three. Plan follow-up validation beyond Java benchmarks before claiming broader language or large-codebase generality. See [[wiki/10-generalization-rwb-results|Generalization on RWB, Repair Scenarios, Ablation and Repair Costs]].
