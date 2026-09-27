> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Generalization on RWB, Repair Scenarios, Ablation and Repair Costs
**In one sentence:** PracRepair stays robust across SL/SH/SF/MF scenarios with its strongest edge on multi-function bugs, gains cumulatively from all three stages plus dynamic traces, question-driven diagnosis and three refinement rounds, generalizes on RWB across foundation models, and does so at lower per-bug cost than baselines.
## Key points
- In the single-function (SF) setting PracRepair is best overall: on Defects4J V1.2 GPT-3.5 repairs 120 and GPT-4o repairs 135 bugs, and on Defects4J V2.0 the numbers rise to 121 and 153, consistently exceeding all baselines.
- In single-hunk (SH) and single-line (SL) settings PracRepair matches or surpasses recent LLM-based baselines, and in multi-function (MF) it beats ReInFix, the only other MF-capable baseline: PracRepair GPT-4o repairs 27 MF bugs on V1.2 and 18 on V2.0 versus 22 and 15 for ReInFix GPT-4o.
- Ablation on Defects4J V1.2 with GPT-3.5 (Table VI, correct/plausible): w/o SDC+QFD+FPR 84/98, w/o SDC+QFD 105/113, w/o SDC 115/126, full PracRepair 139/167, showing refinement, then diagnosis, then static-dynamic context each add gains.
- Removing dynamic execution traces (w/o DI) drops correct patches from 139 to 120 and plausible patches from 167 to 137, indicating traces expose executed paths, branch outcomes and variable-state changes not recoverable from static context alone.
- Reasoning strategy: one-shot CoT without function calls yields 107 correct patches, on-demand retrieval with ReAct raises this to 121, and full question-driven diagnosis reaches 139, showing benefit beyond tool use alone via targeted questions and systematic hypothesis formulation.
- Refinement rounds (Figure 4): 89 correct patches with no refinement, 107 after one round, 119 after two, 139 after three, then unchanged with more interactions, so three rounds is adopted as default balancing effectiveness and interaction cost.
- On the unseen RWB benchmark (Table VII) PracRepair generalizes across GPT-4/GPT-3.5, DeepSeek-v3/DeepSeek-Coder and Llama-3, and on cost it stays efficient: GPT-3.5 $0.04 per repaired bug versus ReInFix $0.06, RepairAgent $0.14 and ChatRepair $0.42, and GPT-4o $1.13 versus ReInFix GPT-4o $1.45.
---
## Repair scenarios analysis (RQ2 tail)
**Covers:** SL/SH/SF/MF breakdown on Defects4J V1.2 and V2.0.

Following prior work, the authors "further examine PracRepair under four commonly scenarios: single-line (SL), single-hunk (SH), single-function (SF), and multi-function (MF)."

- SF: "it delivers the best overall results among all compared approaches. On Defects4J V1.2, PracRepair GPT-3.5 and PracRepair GPT-4o repair 120 and 135 bugs, respectively, while on Defects4J V2.0 the corresponding numbers further increase to 121 and 153, consistently exceeding all baselines."
- SH/SL: "PracRepair continues to match or surpass recent LLM-based baselines, demonstrating its effectiveness across simpler and more complex repair scenarios."
- MF: "Compared with ReInFix, the only other baseline explicitly supporting MF repair, PracRepair achieves higher repair counts on both dataset versions. For example, PracRepair GPT-4o repairs 27 and 18 MF bugs on Defects4J V1.2 and V2.0, compared with 22 and 15 for ReInFix GPT-4o."
- Summary: "Overall, these results indicate that PracRepair performs robustly across diverse repair scenarios, with particularly strong advantages on challenging multi-function bugs."

> "Answer to RQ2: PracRepair consistently outperforms prior methods across different repair scenarios, including SL, SH, SF, and MF bugs. Its advantage is especially clear on the more challenging multi-function setting."

## RQ3 ablation setup and three-stage impacts
**Covers:** RQ3 ablation design and Table VI stage variants on Defects4J V1.2 with GPT-3.5.

"To assess the impact of individual components in PracRepair, we conduct an ablation study using the variants defined in Section IV-C. These variants are designed by systematically removing or replacing key parts of the framework." Scope: "Due to computational budget constraints, all ablation experiments are conducted on Defects4J V1.2 with GPT-3.5."

Table VI — repair results (correct patches / plausible patches) on Defects4J V1.2:

| Variant | Result | MF | SF | SH | SL |
|---|---|---|---|---|---|
| w/o SDC+QFD+FPR | 84/98 | 7 | 77 | 55 | 38 |
| w/o SDC+QFD | 105/113 | 12 | 93 | 74 | 46 |
| w/o SDC | 115/126 | 16 | 99 | 77 | 48 |
| w/o DI | 120/137 | 17 | 103 | 80 | 49 |
| PracRepair CoT | 107/123 | 9 | 98 | 68 | 52 |
| PracRepair ReAct | 121/149 | 15 | 106 | 79 | 53 |
| PracRepair GPT-3.5 | 139/167 | 19 | 120 | 90 | 55 |

Stage reading from the chunk: "The w/o SDC+QFD+FPR variant performs the worst, achieving 84 correct patches and 98 plausible patches. Adding only Feedback-guided Patch Refinement in w/o SDC+QFD increases the number of correct patches to 105, showing the benefit of iterative refinement. Further adding Question-driven Failure Diagnosis in w/o SDC raises the number of correct patches to 115, indicating that diagnosis improves repair beyond refinement alone." Then "Compared with w/o SDC, adding Static-dynamic Context Construction increases the number of correct patches from 115 to 139 and plausible patches from 126 to 167. Overall, the results show that all three stages contribute to repair effectiveness, and their combination yields the strongest performance."

## Impacts of dynamic execution traces
**Covers:** w/o DI comparison in Table VI.

"The w/o DI variant removes dynamic execution traces from Static-dynamic Context Construction, leaving only static program context and failure information. Compared with the full system, this change reduces the number of correct patches from 139 to 120 and the number of plausible patches from 167 to 137." Interpretation: "These results indicate that dynamic execution traces provide important failure-relevant evidence that cannot be fully recovered from static context alone. By exposing runtime behaviors, such as executed paths, branch outcomes, and variable state changes, they help the model perform more grounded diagnoses and repairs."

## Impacts of reasoning strategy
**Covers:** CoT vs ReAct vs question-driven diagnosis in Table VI.

"Compared with plain CoT and ReAct, the proposed question-driven diagnosis mechanism in Question-driven Failure Diagnosis improves repair effectiveness. The one-shot PracRepair CoT variant, which does not use the designed function calls, produces 107 correct patches. Allowing on-demand retrieval of failure-relevant evidence in PracRepair ReAct increases this number to 121, which suggests that tool-assisted diagnosis can be more effective than reasoning over a fixed input context alone. The full PracRepair further improves the result to 139. Since both PracRepair ReAct and the full PracRepair support function-call interaction, this additional gain indicates that the proposed question-driven diagnosis provides benefits beyond tool use alone. By organizing diagnosis around targeted questions, PracRepair appears to help the model systematically inspect failure-relevant evidence and formulate repair hypotheses."

## Impacts of refinement interaction number
**Covers:** Figure 4 refinement-rounds curve.

"According to Figure 4, repair performance improves as the number of refinement interactions increases. Without refinement, PracRepair produces 89 correct patches, which increases to 107 and 119 after one and two refinement rounds, respectively, indicating that iterative feedback helps correct early patch errors. Performance further improves to 139 correct patches after three rounds, but remains unchanged with additional interactions, showing diminishing returns beyond this point. Considering both repair effectiveness and interaction cost, we adopt three refinement rounds as the default setting."

## RWB generalizability (Table VII)
**Covers:** RWB correct-fix counts across foundation models; Answer to RQ4.

Table VII — repair results (correct fixes) of the generalizability study on RWB (as printed in chunk; columns under PracRepair / ReInFix / ThinkRepair with LLMs G4, DS-v3, L3, G3.5, DS-C):

| Project | PracRepair G4 | PracRepair DS-v3 | PracRepair L3 | PracRepair G3.5 | PracRepair DS-C | ReInFix G4 | ReInFix G3.5 | ReInFix DS-C | ThinkRepair G3.5 | ThinkRepair DS-C |
|---|---|---|---|---|---|---|---|---|---|---|
| Cli | 4 | 4 | 4 | 4 | – | 4 | 4 | – | 4 | – |
| Codec | 4 | 3 | 3 | 3 | – | 3 | 3 | – | 3 | – |
| Collections | 1 | 1 | 1 | 1 | – | 1 | 1 | – | 1 | – |
| Compress | 3 | 3 | 3 | 2 | – | 2 | 2 | – | 1 | – |
| Csv | 1 | 1 | 1 | 1 | – | 1 | 1 | – | 1 | – |
| Jsoup | 7 | 8 | 7 | 7 | – | 7 | 6 | – | 6 | – |
| Lang | 3 | 3 | 3 | 3 | – | 3 | 3 | – | 3 | – |

Note: "–" indicates that no result was reported in the original work. G4/G3.5 = GPT-4/GPT-3.5; DS-v3/DS-C = DeepSeek-v3/DeepSeek-Coder; L3 = Llama-3. The chunk header fragment reads "RWB V2.0 15 14 13 – 13 – – 12 – 10" with the same "– means not reported" note.

> "Answer to RQ4: PracRepair generalizes well across both unseen benchmarks and different foundation models. These results show that its repair framework is robust and not tied to a specific dataset or model."

## Repair costs discussion
**Covers:** Section VI.A average monetary cost per repaired bug.

"Using LLMs may raise concerns about repair costs. To address this, we follow prior work [25], [26], [28] and report the average monetary cost per repaired bug based on the" costs "against the costs reported in their original papers. In our setting, PracRepair GPT-3.5 costs $0.04 per repaired bug, while PracRepair GPT-4o costs $1.13. Compared with prior LLM-based APR methods, PracRepair remains cost-efficient: under GPT-3.5, its cost is lower than ReInFix GPT-3.5 ($0.06), RepairAgent ($0.14), and ChatRepair ($0.42), while under GPT-4o it also costs less than ReInFix GPT-4o ($1.45). These results show that PracRepair improves repair effectiveness while maintaining competitive repair cost."

**Covers:** RQ2 scenario tail through RQ3 ablation (Table VI, Figure 4), RWB generalizability (Table VII through Answer to RQ4), and repair-costs discussion; Defects4J V1.2/V2.0 scenario counts and dollar costs as above.
