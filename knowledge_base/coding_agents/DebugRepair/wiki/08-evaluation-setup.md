> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation Setup
**In one sentence:** DebugRepair is evaluated against 15 SOTA baselines on Defects4J and QuixBugs using plausible/correct-fix counts, with GPT-3.5 as the primary backbone under perfect fault localization and a patch budget of 32, and it correctly fixes 224 Defects4J bugs plus all 40 QuixBugs Java and Python bugs.
## Key points
- 15 SOTA baselines are compared: 8 learning-based (CURE, Recoder, SelfAPR, RewardRepair, KNOD, AlphaRepair, FitRepair, RAP-Gen), 1 template-based (TBar), and 6 LLM-based (ChatRepair, ContrastRepair, TSAPR, RepairAgent, ReinFix, ThinkRepair), plus a BaseChatGPT basic-prompt baseline.
- Results reported for baselines follow the common APR practice of reusing numbers from their original papers, with "-" in Table 2 marking unreported results.
- Two metrics are used: # Plausible (bugs passing all test cases after fixing, without further verification) and # Correct (plausible patches confirmed by manual review).
- The primary backbone is gpt-3.5-turbo via OpenAI API, supplemented by DeepSeek-V3, Qwen2.5-7B, Qwen2.5-Coder-7B, and Qwen2.5-32B via SiliconFlow, all sampled at temperature 1.0.
- Fault localization uses the perfect setting to avoid FL-tool bias, consistent with recent studies, and AST parsing/manipulation for Java and Python uses tree-sitter on an Ubuntu 20.04 server with two Intel Xeon Gold 6138 CPUs and 251 GB RAM.
- The repair budget is bounded by 32 candidate patches per bug (6 sessions × 4 rounds + 8 patch-augmentation queries), with LLM instrumentation attempts capped at 10.
- On Defects4J, DebugRepair fixes 224 bugs total (111 on V1.2, 113 on V2.0; 224/283 correct/plausible), 11 more than second-ranked ReinFix (213) with a smaller patch size, and tops 7 of 17 projects.
- On QuixBugs, DebugRepair correctly fixes all 40 Java and all 40 Python bugs, and with DeepSeek-V3 as backbone it fixes 59 more Defects4J bugs than the most competitive reproduced LLM baseline (ReinFix).
---
## 4.3 Baselines
To make a comprehensive evaluation on Defects4J and QuixBugs, DebugRepair is compared against 15 SOTA baselines across categories: eight learning-based approaches (CURE [16], Recoder [50], SelfAPR [45], RewardRepair [46], KNOD [15], AlphaRepair [37], FitRepair [35], RAP-Gen [32]), one template-based traditional method (TBar [28]), and six LLM-based approaches in three subgroups — feedback-based (ChatRepair [38], ContrastRepair [19], TSAPR [11]), retrieval-based (RepairAgent [4], ReinFix [48]), and hybrid (ThinkRepair [47]).
A further LLM baseline named BaseChatGPT directly uses a basic prompt without additional feedback, following prior work [19, 38, 47], as a foundational comparison. Following common APR practice [19, 35, 37, 38, 47, 50], results provided by the baselines' original papers are reported.
## 4.4 Evaluation Metrics
Following previous work [11, 15, 16, 19, 47, 48], two widely used metrics are considered:
- Number of Plausible Fixes (# Plausible): "Counts the number of bugs which can pass all the test cases after fixing, without further verification."
- Number of Correct Fixes (# Correct): "Measures the number of programs that are successfully fixed based on a manual review of the generated plausible patches."
## 4.5 Implementation
Experiments primarily adopt gpt-3.5-turbo (GPT-3.5) [1] via the OpenAI API, plus four other LLMs (DeepSeek-V3, Qwen2.5-7B, Qwen2.5-Coder-7B, Qwen2.5-32B) via SiliconFlow [2], covering a range of architectures and sizes. Sampling temperature is 1.0 for diverse patches, following prior work [19, 38, 47, 48]. Fault localization adopts the perfect setting, aligning with recent studies [11, 19, 38, 47, 48], to avoid FL-tool bias. Repair budget: 6 debugging sessions (N_session), max 4 repair rounds (K_round) per session, plus 8 patch-augmentation queries, so the maximum per bug is 32 (6 × 4 + 8); LLM instrumentation attempts capped at 10 (M_inst). Server: Ubuntu 20.04, two Intel Xeon Gold 6138 CPUs, 251 GB RAM; tree-sitter [3] for AST parsing/manipulation of Java and Python.
## 5 / 5.1 RQ1: Comparison with SOTA Approaches
Section 5 evaluates effectiveness, robustness, and generalizability on Defects4J, QuixBugs, and HumanEval-Java; RQ1 compares overall repair effectiveness against the 15 baselines via plausible/correct patch counts in Table 2 (# Correct/# Plausible):

| Category | APR Approach | Patch Size | Defects4J V1.2 | Defects4J V2.0 | Defects4J Total | QuixBugs Java | QuixBugs Python |
|---|---|---|---|---|---|---|---|
| Template-based | TBar [28] | - | 68/95 | 8/25 | 76/120 | - | - |
| Learning-based (NMT) | CURE [16] | 5000 | 57/- | 19/- | 76/- | 26 | - |
| Learning-based (NMT) | Recoder [50] | 100 | 71/- | 19/46 | 90/- | 31 | - |
| Learning-based (NMT) | SelfAPR [45] | 150 | 65/74 | 45/47 | 110/121 | - | - |
| Learning-based (NMT) | KNOD [15] | 1000 | 71/85 | 50/85 | 121/170 | 25 | - |
| Learning-based (NMT) | RewardRepair [46] | 200 | 45/- | 45/- | 90/- | 20 | - |
| Learning-based (PLM) | AlphaRepair [37] | 5000 | 74/109 | 36/- | 110/- | 28 | 27 |
| Learning-based (PLM) | FitRepair [35] | 4000 | 89/- | 44/- | 133/- | - | - |
| Learning-based (PLM) | RAP-Gen [32] | - | 72/- | 53/- | 125/- | - | - |
| LLM-based (Basic) | BaseChatGPT | 32 | 75/104 | 67/100 | 142/204 | 33 | 32 |
| LLM-based (Retrieval) | RepairAgent [4] | 117 | 92/96 | 72/90 | 164/186 | - | - |
| LLM-based (Retrieval) | ReinFix [48] | 45 | 104/- | 109/- | 213/- | - | - |
| LLM-based (Hybrid) | ThinkRepair [47] | 125 | 98/- | 107/- | 205/- | 39 | 40 |
| LLM-based (Feedback) | ChatRepair [38] | 500 | 114/- | 48/- | 162/- | 39 | 40 |
| LLM-based (Feedback) | ContrastRepair [19] | 160 | 103/- | 40/- | 143/201 | 40 | 40 |
| LLM-based (Feedback) | TSAPR [10] | 32 | 108/146 | 93/134 | 201/280 | 40 | - |
| LLM-based | DebugRepair | 32 | 111/146 | 113/137 | 224/283 | 40 | 40 |

Note: "'-' indicates no results reported in the original work" and highest plausible/correct counts are bolded in the source.
### Results on Defects4J
DebugRepair correctly fixes 224 bugs total (111 on V1.2, 113 on V2.0); vs second-ranked ReinFix it fixes 11 additional bugs with a smaller patch size. Among feedback-based APR with fewer or equal patch sizes: 62 more than ChatRepair (+38.3%) and 81 more than ContrastRepair (+56.6%), and 23 more than TSAPR (+11.44% over 201). Vs conventional learning-based approaches: 85.1%–194.7% more correct fixes with only 1/3 to 1/156 of the patch sizes. Per-project (Table 3), DebugRepair is best on 7 of 17 projects, 4 ahead of second-ranked TSAPR and ThinkRepair — e.g., 37 in Math, 29 in JacksonDatabind, 27 in Lang, 18 in Compress. Six LLM baselines (ChatRepair, ContrastRepair, ThinkRepair, RepairAgent, TSAPR, ReinFix) were manually reproduced on Defects4J with DeepSeek-V3, where DebugRepair fixes 59 more bugs than the most competitive counterpart (ReinFix).
### Results on QuixBugs and per-project Table 3
DebugRepair correctly fixes all 40 Java and all 40 Python QuixBugs bugs. Correct fixes per Defects4J project (# Bugs in header; ReinFix excluded here because "its GPT-3.5 performance under the single-function (SF) repair scenario across specific projects is neither reported nor open-sourced"):

| Approach | Chart (26) | Closure (174) | Lang (63) | Math (106) | Mockito (38) | Time (26) | Cli (39) | Codec (18) | Collect (4) | Compress (47) | Csv (16) | Gson (18) | Core (26) | Databind (112) | Xml (6) | Jsoup (93) | JxPath (22) | Total (835) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RepairAgent | 11 | 27 | 17 | 29 | 6 | 2 | 8 | 9 | 1 | 10 | 6 | 3 | 5 | 11 | 1 | 18 | 0 | 164 |
| ThinkRepair | 11 | 34 | 19 | 27 | 6 | 4 | 9 | 10 | 0 | 16 | 8 | 5 | 7 | 17 | 2 | 28 | 2 | 205 |
| ChatRepair | 15 | 37 | 21 | 32 | 6 | 3 | 5 | 8 | 0 | 2 | 3 | 3 | 3 | 9 | 1 | 14 | 0 | 162 |
| ContrastRepair | 12 | 32 | 19 | 30 | 8 | 2 | 4 | 5 | 0 | 2 | 3 | 1 | 3 | 7 | 1 | 14 | 0 | 143 |
| TSAPR | 12 | 28 | 24 | 32 | 8 | 4 | 12 | 5 | 0 | 15 | 7 | 4 | 4 | 18 | 1 | 26 | 1 | 201 |
| DebugRepair | 12 | 25 | 27 | 37 | 7 | 4 | 10 | 8 | 0 | 18 | 7 | 6 | 4 | 29 | 2 | 27 | 1 | 224 |

Abbreviations: Core = JacksonCore, Xml = JacksonXml, Databind = JacksonDatabind, Collect = Collections; highest per-project counts bolded in the source.

**Covers:** Sections 4.3–5.1 (Baselines; Evaluation Metrics; Implementation; Experimental Results intro and RQ1 with Tables 2–3)
