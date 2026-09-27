> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# DebugRepair Framework Overview
**In one sentence:** DebugRepair enhances feedback-based LLM program repair by replacing reliance on outcome-level failure symptoms with intermediate runtime evidence collected through self-directed simulated debugging.
## Key points
- Feedback-based LLM APR techniques (e.g., ChatRepair, ContrastRepair, TSAPR) iteratively refine patches from test execution feedback but rely primarily on outcome-level symptoms such as stack traces.
- Outcome-level symptoms show how failures are observed but hide the intermediate runtime states needed for root-cause analysis, causing LLMs to infer bug causes without evidence and produce incorrect patches.
- DebugRepair's key idea is to enhance patch refinement with intermediate runtime evidence collected through simulated debugging rather than relying solely on outcome-level failure symptoms.
- Component 1, test semantic purification, extracts the minimal failure-triggering test context to remove noise from tests and follow-up debugging logs.
- Component 2, simulated instrumentation, lets the LLM insert targeted debugging statements into buggy functions to collect runtime traces, with a rule-based fallback when LLM-instrumented code fails to compile or introduces semantic inconsistencies.
- Component 3, debugging-driven conversational repair, organizes patch generation into a hierarchical, iterative process that progressively refines candidates using both prior repair attempts and newly observed runtime states.
- With GPT-3.5, DebugRepair correctly fixes 224 bugs on Defects4J (26.2% average improvement over SOTA LLM-based approaches); with DeepSeek-V3 it fixes 295 Defects4J bugs, 59 more than the second-best baseline.
- Across five additional backbone LLMs of different families and sizes, DebugRepair improves repair performance by 51.3% on average over vanilla settings, and ablation studies confirm all three components contribute effectively.
---
## Problem: outcome-level symptoms are insufficient
Feedback-based approaches "have shown promising results by iteratively refining candidate patches according to test execution feedback," but "most of these approaches rely primarily on outcome-level failure symptoms, e.g., stack traces."

Verbatim claim from the chunk:

> "which indicate how failures are observed but fail to expose the intermediate runtime states that are often critical for root-cause analysis. As a result, LLMs must infer bug causes without access to such intermediate runtime evidence, often leading to incorrect patches."

The paper contrasts this with developer practice: developers observe program behavior by inserting instrumentation, e.g., print statements, to expose intermediate runtime states and progressively localize bug causes. This chunk focuses on the second LLM-based APR paradigm, i.e., feedback-based approaches, and targets this limitation.

## DebugRepair: three components
The chunk defines DebugRepair as "a self-directed debugging framework for LLM-based APR" whose "key idea ... is to enhance patch refinement with intermediate runtime evidence collected through simulated debugging, rather than relying solely on outcome-level failure symptoms."

| # | Component | Mechanism stated in chunk |
|---|---|---|
| 1 | Test semantic purification | Extracts the minimal failure-triggering test context, removing noise in both tests and follow-up debugging logs |
| 2 | Simulated instrumentation | LLM inserts targeted debugging statements into buggy functions to collect runtime traces; rule-based fallback invoked when LLM-instrumented code fails to compile or semantically introduces inconsistencies |
| 3 | Debugging-driven conversational repair | Organizes patch generation into a hierarchical, iterative process in which the LLM progressively refines candidate patches using both prior repair attempts and newly observed runtime states |

## Claimed evaluation results
Evaluation scope stated in the chunk: "three widely used benchmarks across two Programming Languages (PLs), e.g., Java and Python" against "15 representative approaches."

| Backbone | Defects4J correct fixes | Comparison stated in chunk |
|---|---|---|
| GPT-3.5 | 224 | 26.2% average improvement over SOTA LLM-based approaches |
| DeepSeek-V3 | 295 | Exceeds the second-best baseline by 59 correct fixes |
| Five additional backbone LLMs of different families and sizes | not enumerated per-model in this chunk | 51.3% average improvement over their vanilla settings, described as model-agnostic effectiveness |

The chunk also states that "further ablation studies confirm that all components of DebugRepair contribute effectively to the overall repair performance."

## Background context in this chunk
The chunk places DebugRepair in this taxonomy:

- Traditional APR: template-based, heuristic-based, constraint-based.
- Learning-based APR: NMT-based (repair as translation from buggy code to patches using historical fixes) and PLM-based (larger corpora and pre-training, more powerful bug-fixing performance).
- LLM-based APR: (1) retrieval-based (e.g., RepairAgent and ReinFix, using static analysis and search for repair ingredients and historical fixes); (2) feedback-based (e.g., ChatRepair, ContrastRepair, and TSAPR, iterative self-correction with test feedback); (3) hybrid (e.g., ThinkRepair, combining both strategies).

Paper identifiers in this chunk: arXiv:2604.19305v1 [cs.SE] 21 Apr 2026; authors led by Linhao Wu and Yifei Pei (equal contribution), corresponding author Zhen Yang; CCS concept Software testing and debugging; keywords Automated Program Repair, Large Language Models.

**Covers:** paper abstract and DebugRepair framework introduction (problem, three components, claimed results).
