> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Statistical Analysis: TOST Equivalence and Audio vs Text Modality
**In one sentence:** Two one-sided tests (TOST) on per-sample audio−text differences show audio and text-only input are statistically equivalent within ±0.02 for the six Gemini configurations but not equivalent even at ±0.05 for the nine open-weight configurations, where text-only wins outright and audio never wins in any of the 15 dual-modality configurations.
## Key points
- Equivalence is tested with the two one-sided tests (TOST) procedure [34] on per-sample (epoch-averaged) audio−text differences with margins Δ ∈ {0.02, 0.03, 0.05}, split by model family.
- Gemini (six configurations, n=2568): TF audio−text = −0.007 and RQ Pass diff = −0.001, both equivalent at ±0.02 (p = 0.013 and p = 0.0002 respectively).
- Open-weight (nine configurations, n=3852): TF audio−text = −0.079 (text wins by ∼8 points) and RQ Pass diff = −0.062; TOST fails to establish equivalence even at ±0.05 on either metric.
- One-sided paired t-tests on open-weight models show text significantly outperforms audio on TF (t(3851) = −14.95, p < 10−26) and RQ Pass (t(3851) = −10.70, p < 10−26).
- Across all 15 dual-modality configurations text-only is either statistically equivalent to audio (six Gemini models, within ±0.02 on every metric) or strictly better (nine open-weight configurations); audio never wins.
- The text-only condition substitutes transcripts in place of the audio waveforms, holding everything else (conversation history, baseline, judge) fixed; OpenAI models and Kimi-Audio-7B are excluded for not accepting text-only input.
- Figure 5 reports pairwise Pearson correlations across the four AMC axes (APR) and the two IHBench primary metrics (TF Win Rate, RQ Pass Rate) over n=27 paired models, with the IHB-RQ row/column the lightest, reflecting its low correlation with the AMC axes.
---
## Equivalence method
**Covers:** TOST procedure, margins, and experimental control

A standard difference test shows only whether modality has any effect, not whether the two conditions are comparable, so the chunk uses:

> "the two one-sided tests (TOST) procedure [34] on per-sample (epoch-averaged) audio−text differences, with equivalence margins ∆ ∈ {0.02, 0.03, 0.05}. We split by model family, which behave very differently."

Control:

> "in place of the audio waveforms (OpenAI models and Kimi-Audio-7B are excluded due to not accepting text-only input). Everything else (conversation history, baseline, judge) is held fixed."

## Gemini vs open-weight TOST results
**Covers:** per-family equivalence outcomes and t-tests

| Family | n | TF audio−text diff | RQ Pass audio−text diff | TOST outcome |
|---|---|---|---|---|
| Gemini (six configurations) | 2568 | −0.007 | −0.001 | Equivalent at ±0.02 (p = 0.013 and 0.0002, respectively); "audio and text-only are statistically indistinguishable" |
| Open-weight (nine configurations) | 3852 | −0.079 (text wins by ∼8 points) | −0.062 | "TOST fails to establish equivalence even at ±0.05 on either metric" |

Confirmatory one-sided paired t-tests (open-weight only):

- TF: "t(3851) = −14.95, p < 10−26"
- RQ Pass: "t(3851) = −10.70, p < 10−26"
- Interpretation given: "a one-sided paired t-test shows text significantly outperforms audio on both TF ... and RQ Pass".

Summary verdict stated in chunk:

> "Audio input never outperforms text. Across all 15 dual-modality configurations, text-only input is either statistically equivalent to audio (the six Gemini models, within ±0.02 on every metric) or strictly better (the nine open-weight configurations, text ahead by ∼8 points on TF and ∼6 on RQ Pass); audio never wins."

## Audio vs text-only task fulfillment (Figure 6)
**Covers:** Figure 6, 15 dual-modality configurations

- Compares the two conditions on TF across "the 15 dual-modality configurations (6 Gemini + 9 open-weight, 3 epochs each), grouped by family."
- "Error bars are 95% percentile bootstrap CIs."
- "Audio never beats text-only."
- "The recovery-quality counterpart is in Appendix E (Figure 8)" / "recovery-quality counterpart is in Appendix E."

## Correlation context (Figure 5)
**Covers:** Figure 5, pairwise Pearson correlations, n=27 paired models

> "Figure 5: Pairwise Pearson correlations across the four AMC axes (APR) and the two IHB ENCH primary metrics (TF Win Rate, RQ Pass Rate), over the n=27 paired models. The IHB-RQ row and column are the lightest in the matrix, reflecting its low correlation with the AMC axes."

Transcribed matrix values as legible in the chunk (row order as printed):

- IHB-RQ: 0.34, 0.48, 0.61, 0.67, 0.67
- IHB-TF: 0.64, 0.79, 0.65, 0.79, 1, 0.67
- AMC-VOICE: 0.88, 0.89, 0.77, 1, 0.79, 0.67
- AMC-SELF: 0.66, 0.65, 1, 0.77, 0.65, 0.61
- AMC-INSTR: 0.93, 1, 0.65, 0.89, 0.79, 0.48
- AMC-INFER: 1, 0.93, 0.66, 0.88, 0.64, 0.34

**Covers:** chunk 09-1-sided-tests-tost-procedure-34 (TOST procedure, Figure 5 correlations, Figure 6 audio vs text-only comparison)
