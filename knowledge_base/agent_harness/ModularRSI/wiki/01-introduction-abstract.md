> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Modular RSI: Modular and Generalizable Recursive Harness Self-Improvement — Abstract and Introduction
**In one sentence:** ModularRSI is a benchmark-disjoint, contrastive, and modular framework that converts coarse task-level outcomes into localized harness improvements by contrasting same-task success/failure trajectories, aggregating evidence across tasks, and evolving five functional harness modules independently before integrating them.
## Key points
- Existing harness Recursive Self-Improvement (RSI) typically evolves directly on evaluation benchmarks or subsets drawn from them, so reusable harness improvements cannot be distinguished from benchmark-specific adaptation.
- Trajectory-level ambiguity entangles systematic harness deficiencies with instance-specific reasoning and solution details, so updates from individual or one-sided trajectories produce task-specific modifications that transfer poorly.
- Mechanism-level credit assignment is hard in monolithic harnesses: whole-harness optimization entangles unrelated mechanisms and produces changes that are difficult to attribute and validate.
- ModularRSI addresses this by contrasting successful and failed trajectories for the same task and aggregating evidence across tasks to identify recurring behavioral deficiencies.
- The evolvable harness is decomposed into five functional modules — Agent Loop, Tool Use, Observation Management, Context Management, and Task Completion Detection — each evolved independently within a restricted modification scope, then combined in an integration stage that resolves conflicts.
- A benchmark-disjoint evolution protocol curates 2,000 executable evolution tasks from external data sources fully disjoint from downstream benchmarks, with the evolved harness frozen before evaluation and modifications retained only after validation for correctness, executability, and task-specific overfitting.
- Experiments on TerminalBench 2.0 and SWE-Bench Verified report consistent improvements on unseen in-domain and cross-domain tasks, with transfer across different foundation models; code and datasets at https://github.com/IQuestLab/ModularRSI.
---
## Abstract
**Covers:** Abstract (p. 1)

Recent work extends Recursive Self-Improvement (RSI) to agent harnesses for long-horizon coding and terminal tasks, enabling agents to improve their execution mechanisms from experience. The abstract states three blockers to generalizable harness RSI:

1. Evolution on evaluation benchmarks or subsets drawn from them — difficult to distinguish reusable improvements from benchmark-specific adaptation.
2. Updates from individual trajectories entangle systematic harness deficiencies with instance-specific reasoning and solution details — task-specific modifications that transfer poorly.
3. Localizing recurring deficiencies to responsible components in a monolithic harness is difficult — whole-harness optimization entangles unrelated mechanisms.

Proposed solution, verbatim: "We propose ModularRSI, a benchmark-disjoint, contrastive, and modular framework for generalizable harness evolution."

Mechanism, verbatim claims: "ModularRSI contrasts successful and failed trajectories for the same task and aggregates evidence across tasks to identify recurring behavioral deficiencies."

Paper metadata in chunk: title "MODULAR RSI: MODULAR AND GENERALIZABLE RECURSIVE HARNESS SELF-IMPROVEMENT"; authors Siwei Wu, Jincheng Ren, Yizhi Li, Haau-Sing Li, Chengran Yang, Yuxuan Zhang, Weicheng Gu, Jian Yang, Riza Batista-Navarro, Chuanyi Zhang, Xianglong Liu, Ming Zhou, Bryan Dai, Chenghua Lin; affiliations Beihang University, University of Manchester, IQuest Research, M-A-P, Langboat, Hohai University; arXiv:2609.14857v1 [cs.CL] 14 Sep 2026.

## 1 Introduction
**Covers:** Section 1, Introduction (pp. 1–2)

Context: "CLI agents have achieved remarkable performance on complex software engineering and terminal-based tasks" and "their effectiveness increasingly depends on agent harnesses that govern execution, tool interaction, context management, and environment feedback."

Three coupled challenges restated as data-, trajectory-, and mechanism-level:

| Level | Challenge (per chunk) |
|---|---|
| Data | Obtaining high-quality evolution experience is costly: building executable long-horizon terminal tasks with reliable environments and correctness feedback at scale and diversity is difficult; environment completeness, task validity, and evaluator reliability at scale remain challenging, so existing methods "typically rely on data from downstream benchmarks for evolution," making generalizability indeterminate. |
| Trajectory | "Individual or one-sided execution trajectories entangle systematic harness deficiencies with task-specific reasoning and solution details," so direct optimization "may therefore introduce task-specific behaviors that transfer poorly to unseen tasks." |
| Mechanism | Even given a recurring deficiency, "it remains unclear which harness component should be modified"; many approaches "still optimize or rewrite large portions of the harness," and "[t]his large modification space can entangle unrelated mechanisms, making targeted and reliable evolution difficult." |

ModularRSI design, verbatim: "a contrastive and modular credit-assignment framework for harness self-evolution" that "translates coarse task-level outcomes into localized harness evolution signals by contrasting successful and failed trajectories and aggregating evidence across tasks."

Localization: five functional modules — "Agent Loop, Tool Use, Observation Management, Context Management, and Task Completion Detection" — each "evolved independently within a restricted modification scope," with improvements "subsequently integrated into a unified harness," reducing "both task-specific adaptation and interference across unrelated harness mechanisms."

Evaluation protocol: "benchmark-disjoint evolution protocol with 2,000 independently curated executable tasks that are fully disjoint from downstream evaluation benchmarks"; harness frozen before evaluation; modifications "retained only after validation for correctness, executability, and task-specific overfitting."

## Main contributions
**Covers:** Section 1, contributions list (p. 2)

1. "We propose ModularRSI, a contrastive and modular framework that addresses the credit-assignment problem in harness self-evolution. By combining same-task trajectory contrast, cross-task evidence aggregation, and module-restricted evolution, ModularRSI converts coarse task-level outcomes into localized harness modification signals while reducing task-specific and cross-mechanism interference."
2. "We establish a benchmark-disjoint evolution protocol for evaluating generalizable Harness RSI. We independently curate 2,000 executable evolution tasks from external data sources and apply instance-level similarity filtering and fine-grained domain analysis to minimize overlap with downstream benchmarks, providing a standardized evolution resource for studying transferable harness improvements."
3. "We extensively evaluate ModularRSI on TerminalBench 2.0 and SWE-Bench Verified. The evolved harness consistently improves performance on unseen in-domain and out-of-domain tasks and transfers across different foundation models. Our controlled studies further show that independently evolving and merging harness modules substantially outperforms joint or non-modular evolution, while different modules contribute complementary improvements to execution reliability and interaction efficiency."

## 2 Related Work (header and comparison table present in chunk)
**Covers:** Section 2 / 2.1 header and Table 1 header rows

Chunk opens Section 2 ("RELATED WORK"), subsection 2.1 ("AGENT HARNESSES AND SELF-IMPROVEMENT"), noting alongside coding-model advances "executable environments and verified trajectories provide scalable signals for agent im-" (sentence cut off at chunk boundary).

Table 1 ("Modular / Whole-Harness Evolution / Not Use Benchmark Data" columns) compares representative methods; the ModularRSI (Ours) row is marked ✓ / ✓ / ✓, the only row with ✓ in all three columns. Other rows as printed (✓ = present): AutoHarness ✗/✗/✗; Meta-Harness ✗/✓/✗; AHE ✗/✗/✗; Self-Harness ✗/✗/✗; RHO ✗/✗/✗; HarnessFix ✓/✗/✗; Living-Harness ✓/✗/✗; HarnessForge ✓/✓/✗; HarnessBank ✓/✓/✗; RSEA ✓/✗/✗; TACO ✗/✗/✗.

**Covers:** Paper Abstract through Section 1 (Introduction + contributions) and Section 2/2.1 header with Table 1 comparison rows, arXiv:2609.14857v1
