[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# NAVIR results and energy method (Table 8, Section VII.A–VII.B)
**In one sentence:** After quantization-aware training, NAVIR's accuracy collapses on audio-only training but the video-anchored noisy-audio+video model holds 1.5% WER / 98.6% command accuracy under noisy audio, and the operation-count energy model (Horowitz 45 nm constants, 27.55% firing rate) gives a 13.17× SNN-over-ANN gain at 314.92 µJ per sentence.
## Key points
- Table 8 reports quantized (post-QAT) NAVIR results as WER (%) / command accuracy (%): clean-audio training gives 6.6 / 91.5 on clean audio but 98.7 / 0.0 on noisy audio.
- Noisy-audio training alone is weak: 12.1 / 77.5 on clean audio and 43.1 / 47.9 on noisy audio.
- Video-only training holds 0.7 / 100.0 on both clean and noisy audio test conditions.
- Noisy audio + video training holds 0.6 / 98.6 on clean audio and 1.5 / 98.6 on noisy audio, showing the visual modality anchoring recognition.
- Clean audio + video training gives 4.3 / 93.0 on clean audio but collapses to 95.7 / 4.2 on noisy audio.
- Energy methodology: E_ANN = MACs × E_MAC with E_MAC ≈ 3.7 pJ, and E_SNN = MACs × r̄ × E_AC with E_AC ≈ 0.9 pJ, using Horowitz 45 nm primitive costs; Horowitz reports only primitive-cost numbers, not a model-level methodology.
- Measured average firing rate r̄ is 27.55% (72.45% sparsity) across spiking layers on GRID, yielding a theoretical 13.17× ANN/SNN gain, 314.92 µJ per-sentence SNN inference versus a 4.15 mJ ANN baseline for the video-only model.
---
## Table 8 — Quantized NAVIR results after QAT
**Covers:** TABLE 8 (quantized NAVIR results after QAT: WER % / command accuracy %)

| Training modalities | Clean audio | Noisy audio |
|---|---|---|
| Clean audio | 6.6 / 91.5 | 98.7 / 0.0 |
| Noisy audio | 12.1 / 77.5 | 43.1 / 47.9 |
| Video | 0.7 / 100.0 | 0.7 / 100.0 |
| Noisy audio + video | 0.6 / 98.6 | 1.5 / 98.6 |
| Clean audio + video | 4.3 / 93.0 | 95.7 / 4.2 |

## Energy and power analysis — theoretical energy methodology (VII.A)
**Covers:** Section VII.A

- Adopts "the operation-count framework that has become a standard in the SNN/ANN comparison literature [6], [5], [11], [38], parameterised by the per-operation energy constants reported by Horowitz [2] for 45 nm CMOS."
- "Horowitz [2] does not propose a model-level methodology, only the underlying primitive-cost numbers."
- ANN inference energy: E_ANN = MACs × E_MAC, with E_MAC ≈ 3.7 pJ (Eq. 1).
- SNN synaptic operations "reduce to additions, since spike values are binary and inactive neurons contribute nothing, at E_AC ≈ 0.9 pJ, scaled by the empirically measured average firing rate r̄": E_SNN = MACs × r̄ × E_AC (Eq. 2).
- Efficiency gain: E_ANN / E_SNN = E_MAC / (E_AC × r̄) = 3.7 / (0.9 × r̄) (Eq. 3).
- Caveat, verbatim: "These figures are theoretical estimates derived from operation counts. They do not capture memory-access cost, hardware parallelism or implementation-specific factors, but they serve as a standard, reproducible cross-architecture baseline."

## Theoretical results on GRID (VII.B)
**Covers:** Section VII.B (Table 9 / Table 10 comparison points)

| Model | ANN energy | SNN energy | ANN/SNN gain |
|---|---|---|---|
| LipNet [28] | 19.78 mJ | — | — |
| Wu et al. [35] | 156.54 mJ | — | — |
| Ours (video-only) | 4.15 mJ | 314.92 µJ | 13.17× |

- "The SNN energy advantage stems from the combination of spike sparsity and the AC-vs-MAC asymmetry."
- "Our model achieves a measured average firing rate of 27.55% (i.e., 72.45% sparsity) across spiking layers, evaluated empirically on GRID."
- Per-sentence inference cost reduced to 314.92 µJ; with the 4.15 mJ ANN baseline this is "approximately 62.8× below LipNet [28] and 497× below Wu et al. [35] when both are evaluated as ANNs (Table 10)."
- "LipNet and Wu et al. are not directly convertible to SNN equivalents and are quoted as ANN comparison points only."
- Compactness: "3.1× fewer FLOPs than LipNet [28] and 37.8× fewer than Wu et al. [35]", translating "directly into a 4.8× and 37.8× lower ANN energy footprint respectively."
- Note: this chunk's tail also shows Pareto (Figure 2) and hardware power (Table 12) material, which is covered in detail on the next wiki page (08-power-measurements-and-pareto.md), not duplicated here.

**Covers:** TABLE 8 + Section VII.A–VII.B (chunk 07-table-8-quantized-navir-results-after; Pareto/power spillover detailed in chunk 08)
