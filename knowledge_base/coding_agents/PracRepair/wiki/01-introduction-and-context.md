> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction and Context
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
---
## Paper header and abstract
**Covers:** IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 14, NO. 8, AUGUST 2021, p. 1 through Abstract and Index Terms.

| Field | Value (verbatim / exact) |
|---|---|
| Title | "P RAC R EPAIR: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices" |
| Authors | "Yu Cheng, Zhongxin Liu, Zhenchang Xing, Chao Ni, Qing Huang, Xiaoxue Ren" |
| Affiliations | "Y. Cheng, Z. Liu, C. Ni, and X. Ren are with Zhejiang University, China. E-mail: {yucheng1127, liu zx, chaoni, xxren}@zju.edu.cn." / "Z. Xing is with CSIRO's Data61, Australia." / "Q. Huang is with Jiangxi Normal University, China." / "X. Ren is the corresponding author." |
| Identifier | "arXiv:2606.17612v1 [cs.SE] 16 Jun 2026" |
| Index Terms | "Automated program repair, large language model." |

Abstract argument (from the chunk): "As software systems grow in scale and complexity, debugging and repair remain costly and time-consuming. Large language models (LLMs) have advanced automated program repair (APR), but existing LLM-based APR approaches still largely rely on static or retrieved context, error messages, and coarse-grained validation outcomes."

## Introduction: defects and the human debugging workflow
**Covers:** Section I. INTRODUCTION, from defect non-locality through developer debugging practices.

- Defects "have become increasingly common in real-world development," and "in real-world software systems, the causes and effects of a defect often extend beyond a single function and require reasoning over non-local contextual information, such as call relationships, data dependencies, and execution logic [3]."
- "Developers typically debug in IDE-like environments [4], [5], where they leverage richer information and follow a structured workflow to understand failures, formulate repair hypotheses, and iteratively refine fixes [6]–[11]."
- Developers gather evidence "by inspecting the buggy method and failing tests, navigating to relevant implementations, and tracing execution through interactive operations such as step into and step over."
- "Through this process, they recover implicit execution knowledge, including call relationships, and observe fine-grained runtime behaviors such as executed paths, variable states, branch outcomes, and intermediate values [6], [9]–[12]."
- "Based on such evidence, developers then diagnose failures in a question-driven manner [7], [8], [13], asking targeted questions such as what happened here? or why is x null at this point?, and progressively narrowing down the root cause while identifying what additional evidence is needed to better understand the buggy behavior [12]."
- "After completing the failure diagnosis, developers often return to the debugging environment to re-execute the patched program and compare its behavior with the original failing execution. If the patch does not fully resolve the bug, they further analyze the remaining failure and refine the repair accordingly. As a result, failure understanding and patch construction co-evolve through continuous feedback and refinement [10]–[12]."

## Cost motivation and APR background
**Covers:** Section I. INTRODUCTION, from debugging cost through recent LLM-based APR (chunk ends mid-sentence).

- Cost: "Software developers spend roughly 35% to 50% of their time, and 50% to 75% of project budgets, on testing, verification, and debugging, costing over 100 billion dollars each year [14]–[16]."
- APR goal: APR "aims to automatically generate patches for buggy programs [17]–[28]."
- Early APR: "mainly relied on manually designed fix patterns or bug-fixing datasets [18]–[23], but their effectiveness was often constrained by limited pattern coverage, strong data dependence, and weak generalization ability [18], [29]."
- LLMs and recent APR: "large language models (LLMs) have demonstrated stronger code understanding and generation capabilities for APR [24], [30], [31]. Building on this progress, recent LLM-based APR approaches, such as ChatRepair [25], ThinkRepair [27], RepairAgent [26], and ReInFix [28], further incorporate richer repair context and iterative interaction, achieving stronger repair performance on benchmarks such as Defects4J [3]."
- Stated limitation (chunk cuts off here): "However, a key limitation is that prior approaches underutilize dynamic information for failure understanding and repair, while overestimating LLMs' ability to precisely infer complex program behavior from static context alone."
