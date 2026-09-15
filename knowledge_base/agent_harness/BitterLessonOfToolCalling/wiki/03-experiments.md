> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments

**In one sentence:** Evaluating 14 models on BFCL v4 and three ablations (chaining, parallelism, context rot) shows programmatic tool calling matches or beats JSON tool calling for most modern models — with its largest gains in long sequential chains (Claude Sonnet 5 +15.4 pp) and large parallel fan-outs (GPT-5 +25.0 pp), a token-cost crossover at ~26 concurrent calls, and stability under 128-schema context flooding while a filesystem-based baseline degrades by 32.0 pp.

## Key points

- 14 models (5 Anthropic Claude, 9 OpenAI GPT) are evaluated on a 309-entry BFCL v4 subset at temperature 0, where accuracy = fraction of entries where every required function call is both present and correctly parameterized.
- 11 of 14 models match or exceed their own JSON baseline under programmatic tool calling (PTC); all five Claude models do so with deltas of 0.0 to 6.5 pp across generations, while GPT-4o, GPT-4.1, and GPT-5.4-mini fall below baseline by 19.7% to 26.9% because they emit literal `\n` escape sequences in multiline scripts that fail with syntax errors.
- The GPT-5.6 family shows the largest PTC gains: GPT-5.6-Sol (72.2 → 82.8) and GPT-5.6-Terra (73.5 → 84.1) each improve +10.6 pp over their own JSON baseline; all three GPT-5.6 variants are positive (+4.2% to +10.6%).
- Per-category means (Table 6, Appendix) hide variance: PTC underperforms JSON by an absolute 14.1% on average in the `parallel` and `parallel_multiple` categories, but gains +10.0% in `live_multiple`.
- Chaining ablation (n = 52, chain lengths 2–20): Claude Sonnet 5 shows the largest PTC gain (80.8 → 96.2), Claude Opus 4.8 follows (80.8 → 94.2), six models stay within 5 pp parity, and GPT-4.1 collapses from 98.1 to 40.4 (sole outlier).
- Parallelism ablation (n = 32, fan-outs 7–48): PTC matches or exceeds baseline for 13 of 14 models; GPT-5 improves 71.9 → 96.9 (largest gain), and GPT-4.1 (90.6 vs 96.9 baseline) is the single model below baseline.
- Token costs cross over at N ≈ 26: at N = 30, JSON uses 3,559 tokens vs 3,380 for PTC; at N = 48, 5,097 vs 3,535 (below the threshold PTC's system-prompt overhead makes it costlier).
- Context rot ablation (n = 31 per condition, flood = 128 schemas with corpus decoys): mean change filtered → flood is −2.3% (JSON) and +5.5% (PTC), while the filesystem-discovery reference condition degrades −32.0% with every model declining.

---

## BFCL v4 Main Evaluation

Setup: 14 models tested on a 309-entry BFCL v4 subset, temperature 0, reported accuracy = fraction of entries where every required function call is present and correctly parameterized. JSON = JSON tool calling; PTC = programmatic tool calling; ± columns show 95% Wilson CI halfwidths. Per-category mean accuracies across all 14 models are reported in Table 6 (Appendix), which the aggregate results here do not reproduce.

| Model | JSON Acc ± | PTC Acc ± |
|---|---|---|
| **Anthropic** | | |
| Claude Haiku 4.5 | 81.9 ± 4.3 | **85.8** ± 3.9 |
| Claude Sonnet 4.5 | 86.4 ± 3.8 | **87.7** ± 3.7 |
| Claude Sonnet 4.6 | 80.9 ± 4.4 | **87.4** ± 3.7 |
| Claude Opus 4.8 | **84.8** ± 4.0 | **84.8** ± 4.0 |
| Claude Sonnet 5 | 84.5 ± 4.0 | **86.1** ± 3.9 |
| **OpenAI** | | |
| GPT-4o | **81.9** ± 4.3 | 55.0 ± 5.5 |
| GPT-4.1 | **81.9** ± 4.3 | 62.1 ± 5.4 |
| GPT-5-nano | 66.7 ± 5.2 | **68.3** ± 5.2 |
| GPT-5 | 71.5 ± 5.0 | **76.1** ± 4.7 |
| GPT-5.4-mini | **79.3** ± 4.5 | 55.0 ± 5.5 |
| GPT-5.4 | 79.3 ± 4.5 | **81.9** ± 4.3 |
| GPT-5.6-Luna | 76.1 ± 4.7 | **80.3** ± 4.4 |
| GPT-5.6-Sol | 72.2 ± 5.0 | **82.8** ± 4.2 |
| GPT-5.6-Terra | 73.5 ± 4.9 | **84.1** ± 4.1 |

Headline results:

- The GPT-5.6 family achieves the largest programmatic tool calling gains: **GPT-5.6-Sol and GPT-5.6-Terra each achieve an absolute improvement of 10.6%** over their own JSON tool calling baseline.
- Across all 14 models, **11 match or exceed baseline accuracy** under programmatic tool calling.
- The aggregate result conceals meaningful category-level variance (Table 6, Appendix): PTC **underperforms JSON by an absolute 14.1% on average in the `parallel` and `parallel_multiple` categories**, while **gaining an absolute 10.0% in `live_multiple`**. The parallel-category gap is partially explained by the `\n` encoding failures of the three weaker OpenAI models, which are most harmful on multi-call scripts; excluding those three models narrows the gap.
- All five Anthropic models (Claude Haiku 4.5 through Sonnet 5) match or exceed baseline under PTC, with deltas from 0.0 to 6.5 percentage points absolute — a pattern that holds across model generations.
- Among OpenAI models, the three newest GPT-5.6 variants are all positive (**absolute improvements of 4.2% to 10.6%**), while three older models (**GPT-4o, GPT-4.1, and GPT-5.4-mini**) fall below baseline by an absolute **19.7% to 26.9%**.
- The consistent failure mode for those three models: they produce code with literal `\n` escape sequences in multiline scripts rather than real newlines, causing the subprocess to fail with a syntax error on any entry requiring more than a single-line script. **GPT-5-nano** (released alongside GPT-5) does not exhibit this failure, suggesting the fix entered training data between GPT-5.4-mini and GPT-5.

## Chaining Ablation

In the chaining ablation (**n = 52 entries, chain lengths 2–20**), programmatic tool calling handles sequential multi-hop calls differently from JSON tool calling. In JSON tool calling, the model issues f₁, receives its return value, then issues f₂ in a second inference turn. In programmatic tool calling, the model writes both calls in a single script and computes the intermediate value from parametric knowledge before passing it to f₂.

| Model | JSON Acc ± | PTC Acc ± |
|---|---|---|
| **Anthropic** | | |
| Claude Haiku 4.5 | **88.5 ± 8.8** | 73.1 ± 11.7 |
| Claude Sonnet 4.5 | **90.4 ± 8.2** | 88.5 ± 8.8 |
| Claude Sonnet 4.6 | 90.4 ± 8.2 | **92.3 ± 7.6** |
| Claude Opus 4.8 | 80.8 ± 10.6 | **94.2 ± 6.8** |
| Claude Sonnet 5 | 80.8 ± 10.6 | **96.2 ± 6.0** |
| **OpenAI** | | |
| GPT-4o | **92.3 ± 7.6** | 86.5 ± 9.3 |
| GPT-4.1 [†] | **98.1 ± 4.9** | 40.4 ± 12.9 |
| GPT-5-nano | 69.2 ± 12.2 | **80.8 ± 10.6** |
| GPT-5 | **92.3 ± 7.6** | **92.3 ± 7.6** |
| GPT-5.4-mini | 76.9 ± 11.2 | **80.8 ± 10.6** |
| GPT-5.4 | **94.2 ± 6.8** | 90.4 ± 8.2 |
| GPT-5.6-Luna | 82.7 ± 10.2 | **92.3 ± 7.6** |
| GPT-5.6-Sol | **96.2 ± 6.0** | 90.4 ± 8.2 |
| GPT-5.6-Terra | **98.1 ± 4.9** | 96.2 ± 6.0 |

[†] GPT-4.1 PTC collapse caused by `\n` encoding failure; see text.

- Claude Sonnet 5 achieves the largest programmatic tool calling gain (**80.8% → 96.2%**), followed by Claude Opus 4.8 (**80.8% → 94.2%**), while six models maintain near-parity (within 5% absolute).
- GPT-4.1 is the sole outlier: its baseline accuracy of **98.1% collapses to 40.4%** under programmatic tool calling, driven by the `\n` encoding failure described above — most harmful in chaining tasks because every intermediate computation requires a multiline script.

## Parallelism Ablation

Programmatic tool calling matches or exceeds baseline accuracy for **13 of 14 models** on the parallelism ablation (**n = 32 entries, fan-out counts of 7 to 48** (7, 9, 11, 13, 15, 20, 30, 48)). Table 4 separates enumeration accuracy (did the model issue all N required calls?) from aggregation accuracy (did the model produce the correct aggregate answer?); enumeration and overall accuracy are identical for all models here — aggregation accuracy is discussed separately in the text.

| Model | JSON Acc ± | PTC Acc ± |
|---|---|---|
| **Anthropic** | | |
| Claude Haiku 4.5 | **100.0 ± 5.5** | **100.0 ± 5.5** |
| Claude Sonnet 4.5 | **100.0 ± 5.5** | **100.0 ± 5.5** |
| Claude Sonnet 4.6 | **100.0 ± 5.5** | **100.0 ± 5.5** |
| Claude Opus 4.8 | **100.0 ± 5.5** | **100.0 ± 5.5** |
| Claude Sonnet 5 | **100.0 ± 5.5** | **100.0 ± 5.5** |
| **OpenAI** | | |
| GPT-4o | **100.0 ± 5.5** | **100.0 ± 5.5** |
| GPT-4.1 | **96.9 ± 7.5** | 90.6 ± 10.5 |
| GPT-5-nano | 78.1 ± 14.0 | **87.5 ± 11.5** |
| GPT-5 | 71.9 ± 14.5 | **96.9 ± 7.5** |
| GPT-5.4-mini | **100.0 ± 5.5** | **100.0 ± 5.5** |
| GPT-5.4 | **100.0 ± 5.5** | **100.0 ± 5.5** |
| GPT-5.6-Luna | **100.0 ± 5.5** | **100.0 ± 5.5** |
| GPT-5.6-Sol | 96.9 ± 7.5 | **100.0 ± 5.5** |
| GPT-5.6-Terra | **100.0 ± 5.5** | **100.0 ± 5.5** |

- The largest programmatic tool calling gain is **GPT-5, which improves from 71.9% to 96.9%**: its baseline accuracy degrades as fan-out count increases above 13, while programmatic tool calling maintains near-perfect enumeration across all fan-out levels.
- The single model that falls below baseline under programmatic tool calling is **GPT-4.1 (90.6% vs. 96.9% baseline)**, again attributable to the `\n` encoding failure on parallel scripts that require `asyncio.gather`.
- PTC enumeration accuracy is high while aggregation accuracy is lower and noisier across models: inspection of outputs shows models frequently produce the correct aggregation answer from parametric world knowledge (stating, for example, the top-3 countries by population directly) without executing the enumeration calls. This is a correct answer by the scorer's standard, but it does not test whether the model actually executed the tools — so both metrics are reported separately, with enumeration accuracy as the primary measure of paradigm fidelity.
- **Token costs cross over at N ≈ 26**: below this threshold programmatic tool calling is more expensive due to its fixed system-prompt overhead; above it, JSON tool calling exceeds programmatic tool calling as the response must enumerate all N tool-call objects. At N = 30, JSON tool calling uses **3,559 tokens versus 3,380** for programmatic tool calling; at N = 48, the gap widens to **5,097 versus 3,535**.

## Context Rot Ablation

The context rot ablation (**n = 31 entries per condition**) compares each paradigm under two context loads: `filtered` (only the entry's relevant function schemas) and `flood` (128 total schemas, comprising the relevant functions plus corpus decoys from unrelated domains). JSON = JSON tool calling; PTC = programmatic tool calling; Arg = filesystem-discovery (reference condition). 95% Wilson confidence intervals range from ± 7.8% to ± 16.6% (n = 31; widest near 50% accuracy).

| Model | Filtered JSON | Filtered PTC | Filtered Arg | Flood JSON | Flood PTC | Flood Arg |
|---|---|---|---|---|---|---|
| **Anthropic** | | | | | | |
| Haiku 4.5 | **93.5** | 83.9 | 48.4 | **87.1** | 77.4 | 25.8 |
| Sonnet 4.5 | **90.3** | 83.9 | 58.1 | **93.5** | 80.6 | 29.0 |
| Sonnet 4.6 | **93.5** | 83.9 | 83.9 | **87.1** | 87.1 | 32.3 |
| Opus 4.8 | 87.1 | 83.9 | **90.3** | **83.9** | 80.6 | 41.9 |
| Sonnet 5 | 87.1 | **87.1** | 80.6 | **90.3** | 87.1 | 45.2 |
| **OpenAI** | | | | | | |
| GPT-4o | **96.8** | 51.6 | 61.3 | **90.3** | 74.2 | 16.1 |
| GPT-4.1 | **83.9** | 51.6 | 41.9 | **80.6** | 64.5 | 19.4 |
| GPT-5-nano | **74.2** | 54.8 | 25.8 | 64.5 | **71.0** | 16.1 |
| GPT-5 | **77.4** | 67.7 | 48.4 | 74.2 | **77.4** | 32.3 |
| GPT-5.4-mini | **80.6** | 45.2 | 54.8 | **87.1** | 80.6 | 12.9 |
| GPT-5.4 | 80.6 | **83.9** | 64.5 | 77.4 | **77.4** | 9.7 |
| GPT-5.6-Luna | **83.9** | 77.4 | 35.5 | **80.6** | 74.2 | 6.5 |
| GPT-5.6-Sol | 77.4 | **80.6** | 32.3 | 71.0 | **80.6** | 12.9 |
| GPT-5.6-Terra | 64.5 | **80.6** | 35.5 | 71.0 | **80.6** | 12.9 |
| **Mean Δ** | **−2.3** | **+5.5** | **−32.0** | | | |

(Anthropic model names omit "Claude" for space, as in the source table.)

- **JSON tool calling and programmatic tool calling are both stable under flooding**: the mean accuracy change from filtered to flood is an absolute **−2.3% for JSON** and **+5.5% for programmatic tool calling** (individual model changes range from −6.5% to +35.5% absolute).
- The PTC improvement under flood is driven by models that struggled with the strict type constraints of the filtered condition but found the flood condition's richer context helped them identify the correct function — most visible in **GPT-4.1 (+12.9%)**, **GPT-4o (+22.6%)**, and **GPT-5.4-mini (+35.5%)** absolute.
- For reference, a filesystem-based internal condition (Arg) degraded by an absolute **32.0%** on average under flooding, where **every model declined** — consistent with context navigation being a structural weakness of file-based tool delivery (Sen et al., 2026a).

**Covers:** Section 4 (Experiments): 4.1 BFCL v4 Main Evaluation, 4.2 Chaining Ablation, 4.3 Parallelism Ablation, 4.4 Context Rot Ablation
