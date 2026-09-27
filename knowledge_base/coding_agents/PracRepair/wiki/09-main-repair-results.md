> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# TABLE V: Repair results (correct fixes)
**In one sentence:** PracRepair tops all baselines on correct-fix counts on Defects4J V1.2 and V2.0, holds unique-fix and cross-project breadth, and stays ahead of baselines even without perfect fault localization.
## Key points
- On Defects4J V1.2, PracRepair GPT-4o reaches 135 correct fixes and PracRepair GPT-3.5 reaches 120, beating ReInFix GPT-4o (124) and ReInFix GPT-3.5 (104) by 16 and 21 fixes respectively.
- On Defects4J V2.0, PracRepair GPT-4o reaches 153 correct fixes and PracRepair GPT-3.5 reaches 121, beating ReInFix GPT-4o (130) and ReInFix GPT-3.5 (109) by 26 and 13 bugs respectively.
- Under GPT-3.5 on Defects4J V1.2, PracRepair also surpasses ChatRepair, ThinkRepair, and RepairAgent.
- PracRepair fixes bugs across all Defects4J projects — Chart, Closure, Lang, Math, Mockito, and Time — showing effectiveness across different domains.
- Unique-fix analysis (Figure 3): under GPT-3.5 PracRepair has 75 unique correct fixes vs 29 (ThinkRepair), 26 (RepairAgent), 12 (ChatRepair); under GPT-4o it has 93 vs 51 (ReInFix).
- Without exact buggy-statement locations, PracRepairNo-PFL fixes 105 bugs correctly with 133 plausible patches, below the perfect-localization GPT-3.5 result (139 correct, 167 plausible) but ahead of ThinkRepairNo-PFL by 25 and Codex by 42 correct fixes.
- Semantically correct results show PracRepair not only satisfies the test oracle on many bugs but also achieves strong repair accuracy, complementing prior methods rather than duplicating them.
---
## TABLE V results
**Covers:** correct-fix counts across Defects4J baselines.

TABLE V reports correct fixes under different repair scenarios (columns MF, SF, SH, SL for each of Defects4J V1.2 and V2.0):

| Method | Defects4J V1.2 (MF / SF / SH / SL) | Defects4J V2.0 (MF / SF / SH / SL) |
|---|---|---|
| ChatRepair | – / 76 / – / – | – / – / – / 48 |
| ThinkRepair | – / 98 / 78 / 52 | – / 107 / 81 / 47 |
| RepairAgent | 7 / 83 / 71 / 51 | 6 / 68 / 65 / 48 |
| ReInFix GPT-3.5 | 14 / 104 / 78 / 53 | 14 / 109 / 85 / 47 |
| ReInFix GPT-4o | 22 / 124 / 93 / 57 | 15 / 130 / 103 / 56 |
| PracRepair GPT-3.5 | 19 / 120 / 90 / 55 | 15 / 121 / 92 / 51 |
| PracRepair GPT-4o | 27 / 135 / 97 / 57 | 18 / 153 / 108 / 57 |

Note: "–" indicates that no result was reported in the original work.

The chunk states that because the fixes are semantically correct, "these results indicate that PracRepair not only satisfies the test oracle on a large number of bugs, but also achieves strong repair accuracy," and that PracRepair "successfully fixes bugs across all Defects4J projects, including Chart, Closure, Lang, Math, Mockito, and Time, demonstrating its effectiveness across projects from different domains."

Head-to-head vs the strongest baseline ReInFix: "PracRepair consistently outperforms the strongest baseline, ReInFix, on both Defects4J V1.2 and V2.0. On Defects4J V1.2, PracRepair GPT-4o improves over ReInFix GPT-4o by 16 correct fixes, while PracRepair GPT-3.5 exceeds ReInFix GPT-3.5 by 21 fixes," with "similar gains" on V2.0 of 26 and 13 bugs respectively. "In addition, under GPT-3.5, PracRepair also surpasses other recent LLM-based APR approaches, including ChatRepair, ThinkRepair, and RepairAgent, on Defects4J V1.2."

## Unique fix analysis
**Covers:** correct-fix counts across Defects4J baselines.

The chunk "further analyze[s] the unique repair capability of PracRepair on Defects4J V1.2 and V2.0" by "compar[ing] the sets of correctly repaired bugs produced by PracRepair and recent LLM-based APR baselines under the same base model setting." Per Figure 3: "under GPT-3.5, PracRepair GPT-3.5 achieves 75 unique correct fixes, compared with 29 for ThinkRepair, 26 for RepairAgent, and 12 for ChatRepair. Under GPT-4o, PracRepair GPT-4o achieves 93 unique correct fixes, while ReInFix achieves 51." The authors "exclude ReInFix from the GPT-3.5-based comparison because its public results are only available under GPT-4o." Conclusion: "these results show that PracRepair maintains stronger unique repair capability than existing LLM-based APR baselines, suggesting that its repair process complements prior methods."

## Effectiveness without perfect fault localization
**Covers:** correct-fix counts across Defects4J baselines.

The above comparisons "assume perfect fault localization, where exact buggy statement locations are provided." To test robustness, the authors "further evaluate it under GPT-3.5 without providing exact fault locations, referred to as PracRepairNo-PFL," comparing "with available baselines under the same setting, including ThinkRepairNo-PFL and Codex." Result: "As shown in Table IV, PracRepairNo-PFL fixes 105 bugs correctly and generates 133 plausible patches. Although this is lower than PracRepair GPT-3.5 under perfect fault localization (139 correct and 167 plausible patches), it outperforms ThinkRepairNo-PFL and Codex by 25 and 42 correct fixes, respectively." Conclusion: "These results show that fault locations are helpful, but PracRepair remains effective when they are unavailable."

> "Answer to RQ1: PracRepair achieves the best overall repair effectiveness under perfect fault localization with both GPT-3.5 and GPT-4o. Without exact buggy statement locations, its performance decreases but still surpasses the only comparable baseline, showing that its effectiveness does not solely rely on perfect fault localization."

## RQ2 transition
**Covers:** correct-fix counts across Defects4J baselines.

"While RQ1 evaluates the overall repair effectiveness of PracRepair, analyzing its performance under specific repair" scenarios follows.
