> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Comparison, Orthogonality to TSAPR, and Generality Across LLMs
**In one sentence:** DebugRepair's refinement-oriented self-directed debugging outperforms ChatRepair, ContrastRepair, ReinFix and TSAPR on complex repairs, stays competitive or leading on single-line bugs, and lifts every tested LLM by 51.3% on average while remaining orthogonal to ReinFix/TSAPR for future integration.
## Key points
- On Defects4J-V1.2 complex bugs (GPT-3.5 backbone), DebugRepair correctly fixes 111 SF and 82 SH bugs versus ChatRepair (75 SF, 69 SH) and ContrastRepair (76 SF, 79 SH).
- On QuixBugs, DebugRepair fixes 100% of SF and SH bugs, and achieves a 100% fix rate across both Java and Python versions (predominantly SL bugs).
- With DeepSeek-V3, DebugRepair fixes 139 SF (V1.2) and 156 SF (V2.0) versus ReinFix (118 and 118) and TSAPR (108 and 116); on SH it fixes 98 and 113 versus second-ranked ReinFix (83 and 89).
- On Single-Line bugs with GPT-3.5, DebugRepair gets 55 (V1.2) and 50 (V2.0) fixes — neck-and-neck on V1.2 behind ChatRepair and TSAPR (57 each), surpassing all baselines on V2.0; with DeepSeek-V3 it gets 57 (V1.2, behind ContrastRepair's 60) and 61 (V2.0, versus ReinFix's 47).
- Across five LLMs, DebugRepair improves correct fixes by 51.3% on average: Qwen2.5-7B +21 (86→107), Qwen2.5-32B +71 (124→195), Qwen2.5-Coder-7B +30 (111→141), GPT-3.5 142→224, DeepSeek-V3 155→295 (+140).
- Gains scale with size (Qwen2.5-32B +71 vs 7B +21), favor code models over general models at the same scale (Coder-7B +30 vs 7B +21; enhanced Coder-7B's 141 approaches vanilla GPT-3.5), and favor stronger reasoning models (DeepSeek-V3 +140 vs GPT-3.5's stated +74); hierarchy is commercial > code > general.
- DebugRepair targets patch refinement through dynamic execution states, making it highly orthogonal to ReinFix and TSAPR and integrable for further improvement; on SL bugs its print-statement traces can lengthen context and slightly hinder pattern-matching on outcome-level symptoms.
---
## Refinement philosophy and complex-repair lead
**Covers:** end of RQ2 discussion — to TSAPR and can be integrated through DeepSeek-V3 complex results

Under a refinement-oriented philosophy, DebugRepair is positioned against ChatRepair and ContrastRepair and "to TSAPR and can be integrated into it for further improvement during the patch refinement."

Complex-repair claims in the chunk:

- Defects4J-V1.2: DebugRepair correctly fixes 111 SF and 82 SH bugs, versus ChatRepair (75 SF, 69 SH) and ContrastRepair (76 SF, 79 SH).
- QuixBugs: 100% of SF and SH bugs fixed.
- DeepSeek-V3 backbone: 139 SF (V1.2) and 156 SF (V2.0), versus ReinFix (118 and 118) and TSAPR (108 and 116); SH: 98 and 113 for DebugRepair versus 83 and 89 for second-ranked ReinFix.
- Orthogonality claim: "because DebugRepair specifically targets the patch refinement through dynamic execution states, its mechanism is highly orthogonal to existing APR tools, such as ReinFix and TSAPR. This orthogonality indicates a strong potential for integrating these approaches in the future to further boost repair performance."

## Single-Line (SL) repair scenarios
**Covers:** SL results on Defects4J-V1.2/V2.0 and QuixBugs, plus trace-length caveat

- GPT-3.5 backbone: 55 SL fixes (V1.2) and 50 SL fixes (V2.0). On V1.2 it is "neck-and-neck," falling "only marginally behind ChatRepair and TSAPR (57 fixes)"; on V2.0 it "surpasses all evaluated baselines."
- DeepSeek-V3 backbone: 57 SL fixes on V1.2 ("closely follows" ContrastRepair's 60) and 61 SL fixes on V2.0 ("significantly outperform the second-ranked ReinFix (47)").
- QuixBugs (predominantly SL bugs): 100% fix rate across both Java and Python versions.
- Caveat given in the chunk: "SL bugs typically require straightforward pattern matching based on outcome-level failure symptoms. In these cases, inserting print statements and collecting execution traces can make the input context longer and slightly more difficult for the LLM to process."
- Overall assessment stated: "while the self-directed debugging strategy excels in complex, multi-statement scenarios, it remains a highly effective framework for simpler, line-level fixes."

> x Answer to RQ2: DebugRepair achieves SOTA performance on complex repairs while maintaining competitive performance on simpler bugs, demonstrating its effectiveness across different repair scenarios.

## RQ3: Generalizability across different LLMs
**Covers:** RQ3 setup, Table 5, hierarchy/scaling/synergy analysis, Answer to RQ3

Setup: five distinct LLMs (general, code, commercial); Table 5 reports Defects4J # Correct/# Plausible and the improvement over vanilla backbones, averaging 51.3%.

Table 5. Comparison results between vanilla LLMs and DebugRepair on Defects4J (# Correct/# Plausible):

| Category | Model | V1.2 SF | V1.2 SH | V1.2 SL | V2.0 SF | V2.0 SH | V2.0 SL | Total |
|---|---|---|---|---|---|---|---|
| General | Qwen2.5-7B | 40/64 | 30/46 | 20/29 | 46/73 | 36/57 | 23/35 | 86/137 |
| General | Qwen2.5-7B (DebugRepair) | 50/65 | 39/49 | 27/32 | 57/75 | 42/58 | 22/32 | 107/140 |
| General | Qwen2.5-32B | 62/90 | 47/64 | 33/43 | 62/88 | 42/63 | 23/34 | 124/178 |
| General | Qwen2.5-32B (DebugRepair) | 92/126 | 66/89 | 39/50 | 103/121 | 78/91 | 38/48 | 195/247 |
| Code | Qwen2.5-Coder-7B | 58/88 | 46/67 | 33/45 | 53/82 | 40/62 | 27/36 | 111/170 |
| Code | Qwen2.5-Coder-7B (DebugRepair) | 62/96 | 54/80 | 33/47 | 79/91 | 61/69 | 34/38 | 141/187 |
| Commercial | DeepSeek-V3 | 82/112 | 59/76 | 36/46 | 73/91 | 56/70 | 31/40 | 155/203 |
| Commercial | DeepSeek-V3 (DebugRepair) | 139/179 | 98/122 | 57/65 | 156/180 | 113/129 | 61/65 | 295/359 |
| Commercial | GPT-3.5 | 75/104 | 56/74 | 36/45 | 67/100 | 49/73 | 31/44 | 142/204 |
| Commercial | GPT-3.5 (DebugRepair) | 111/146 | 82/102 | 55/61 | 113/137 | 83/100 | 50/55 | 224/283 |

Stated deltas: Qwen2.5-7B +21, Qwen2.5-32B +71, Qwen2.5-Coder-7B +30; GPT-3.5 from 142 to 224; DeepSeek-V3 from 155 to 295. The chunk text describes the commercial-model gains as "140 additional fixes for DeepSeek-V3 compared to a 74-fix increase for GPT-3.5" (table totals imply 224 − 142 = 82 for GPT-3.5; both figures are reproduced here as given in the chunk).

Further analysis claims:

- Hierarchy: "commercial models consistently achieve the highest overall repair performance, followed by code models, and finally general models."
- At the same parameter scale, code models outperform general counterparts; e.g. "the DebugRepair-enhanced Qwen2.5-Coder-7B resolves 141 bugs, significantly outperforming the general model Qwen2.5-7B and approaching the efficacy of the much larger vanilla GPT-3.5."
- Size scaling: "Models with larger parameter sizes inherently outperform smaller variants, as evidenced by" Qwen2.5-32B vs Qwen2.5-7B and their DebugRepair-enhanced versions.
- Scaling effect of gains: Qwen2.5-32B (+71) substantially larger than Qwen2.5-7B (+21).
- Stronger synergy with code models: Coder-7B (+30) higher than 7B general (+21).
- Interpretation: "models equipped with stronger foundational reasoning capabilities and domain-specific code training can process and leverage the runtime evidence provided by DebugRepair more effectively."

> x Answer to RQ3: DebugRepair consistently enhances the repair capability of various LLMs, regardless of their size, type, or architecture. On average, it improves the number of correct fixes by 51.3% across the evaluated models.

## RQ4 ablation setup (introduction only)
**Covers:** start of §5.4 RQ4 — five variants and Table 6 values present in this chunk

The chunk introduces the ablation (GPT-3.5 backbone, Defects4J) with five variants:

1. DebugRepair-w/o-Purification: raw failing test without slicing, directly to debugging.
2. DebugRepair-w/o-Debugging: disables simulated debugging; relies solely on outcome-level failure symptoms.
3. DebugRepair-w/o-Augmentation: returns first plausible patch without generating other variants.
4. DebugRepair-wo-LLM Instrumentation: removes LLM-based instrumentation; rule-based strategy only.
5. DebugRepair-wo-Rule Instrumentation: removes rule-based fallback; skips cases where LLM-generated instrumentation fails.

Table 6 values present in this chunk (full interpretation belongs to the ablation page):

| Variant | # Plausible | Plausible Drop | # Correct | Correct Drop |
|---|---|---|---|---|
| w/o-Purification | 215 | ↓ 24.0% | 164 | ↓ 26.8% |
| w/o-Debugging | 213 | ↓ 24.7% | 165 | ↓ 26.3% |
| w/o-Augmentation | 283 | – | 173 | ↓ 19.9% |
| w/o-LLM-based Instrumentation | 233 | ↓ 17.7% | 189 | ↓ 15.6% |
| w/o-Rule-based Instrumentation | 227 | ↓ 19.4% | 181 | ↓ 19.2% |
| DebugRepair | 283 | – | 224 | – |
