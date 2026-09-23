> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# GRID Recognition Results: Visual Modality Anchors Recognition When Audio Degrades
**In one sentence:** On GRID and NAVIR, fusing video with audio sharply lowers WER under noise — with quantization largely preserved and occasional small QAT gains — while clean-audio-only models collapse under noise and the AKD1000-constrained video-only model trails unconstrained SOTA on GRID unseen speakers but approaches baselines on overlapped speakers and saturates near 0% WER on NAVIR.
## Key points
- In the fused noisy condition the quantized model is marginally better than its float counterpart, but the effect is small and not consistent across all configurations.
- The GRID video-only model reaches 34.0% (float) and 35.3% (quantized) WER on the unseen-speaker split, versus a 9.7–11.4% SOTA range whose baselines use 3D convolutions, attention-augmented decoders, and large-scale pre-training that are not AKD1000-compatible.
- On the GRID overlapped-speaker split, video-only reaches 9.1% (float) and 6.7% (quantized) WER, approaching the 1.83–4.8% unconstrained ANN baseline range, with QAT improving video-only by 2.4 absolute points over float.
- Under GRID overlapped-speaker noise, noisy-audio + video fusion reaches 2.8% (float) and 3.3% (quantized) WER versus 10.4%/11.8% for noisy audio alone and 9.1%/6.7% for video alone; under clean audio fusion reaches 0.7%/0.8%, below both single-modality baselines.
- Training on clean audio alone collapses under noise: 77.1–79.8% WER across the four clean-audio-trained configurations on GRID overlapped split (and 97.5% float / 98.7% quantized on NAVIR), whereas training on noisy audio reduces noisy-test WER substantially.
- On NAVIR, video-only retains 0.5% to 0.7% WER with 100% command accuracy preserved through quantization, and noisy-audio + video fusion degrades only from 0.3% to 0.6% WER clean and 0.9% to 1.5% noisy; the 200-epoch QAT schedule is described as well matched to the small corpus size.
- The Pareto analysis in Section VII-C uses both the overlapped- and unseen-speaker video-only stats for cross-method comparison.
---
## GRID unseen-speaker results
**Covers:** GRID WER tables, float vs quantized, unseen vs overlapped splits

In the fused noisy condition the quantized model is marginally better than its float counterpart, "although the effect is small and not consistent across all configurations."

The video-only model reaches 34.0% (float) and 35.3% (quantized) WER on the unseen-speaker split. The chunk states this is higher than the SOTA range of 9.7–11.4% (Section II-D), where "those baselines all employ 3D convolutions, attention-augmented decoders and large-scale pre-training, none of which are AKD1000-compatible." It adds: "The factorised AkidaNet pipeline trades representational depth for hardware deployability, and even so fusion still extracts useful information from the visual stream when audio is corrupted."

Training on noisy audio "reduces noisy-test WER by nearly an order of magnitude (10.4% float and 11.8% quantized)."

## GRID overlapped-speaker results
**Covers:** GRID WER tables, float vs quantized, unseen vs overlapped splits

On the overlapped-speaker split (Tables 5 and 6), where "train and test sets share speakers but not sentences, every trend observed in the unseen-speaker regime is preserved and the absolute numbers tighten substantially."

| Condition (overlapped-speaker split) | Float WER | Quantized WER |
|---|---|---|
| Video-only | 9.1% | 6.7% |
| Noisy audio alone (noisy test) | 10.4% | 11.8% |
| Noisy audio + video (noisy test) | 2.8% | 3.3% |
| Fusion (clean audio test) | 0.7% | 0.8% |
| Clean-audio-trained, tested under noise | 77.1–79.8% WER across the four clean-audio-trained configurations | (same range) |

The video-only result approaches "the 1.83–4.8% range of unconstrained ANN baselines despite the AKD1000-imposed architectural budget." QAT "improves the video-only model over its float counterpart by 2.4 absolute points in this setting, an effect of similar direction to the one observed in the unseen-speaker fused condition, though again we do not claim a consistent QAT advantage across configurations." The chunk's key claim: "confirming that the visual modality anchors recognition when the acoustic signal degrades." "Under clean audio, fusion reduces WER to 0.7% (float) and 0.8% (quantized), below both single-modality baselines."

## B. NAVIR word error rate and command accuracy
**Covers:** GRID WER tables, float vs quantized, unseen vs overlapped splits (Tables 7–8 reported range)

"Tables 7 and 8 report WER and sentence-level command accuracy on the NAVIR corpus."

"NAVIR results are strong across vision-based modalities both before and after quantization. The video-only model retains near-perfect performance through quantization (0.5% to 0.7% WER, 100% command accuracy preserved), and the noisy-audio + video fusion model degrades only marginally (0.3% to 0.6% WER clean and 0.9% to 1.5% noisy)."

"Audio-only models are far less robust. The clean-audio model collapses entirely under noise both before (97.5%) and after (98.7%) quantization, confirming that without visual input the system has no path to reliable performance in real-world acoustic environments."

"The 200-epoch QAT schedule is well matched to the small corpus size, with multimodal models retaining most of their float accuracy."

Table 7 (non-quantized NAVIR results, WER % / command accuracy %) as present in the chunk:

| Training modalities | Clean audio | Noisy audio |
|---|---|---|
| Clean audio | 5.4 / 93.0 | 97.5 / 2.8 |
| Noisy audio | 11.0 / 81.7 | 42.6 / 52.1 |
| Video | 0.5 / 100.0 | 0.5 / 100.0 |
| Noisy audio + video | 0.3 / 100.0 | 0.9 / 100.0 |
| Clean audio + video | 4.3 / 93.0 | 95.6 / 2.8 |

Partial complexity/energy tables visible in the chunk (Tables 9–10 headers and GRID rows):

| Model | WER (%) | Params | FLOPs | ANN energy |
|---|---|---|---|---|
| LipNet [28] | 11.4 | 4.57 M | 10.69 G | 19.78 mJ |
| Wu et al. [35] | 10.21 | 10.89 M | 84.62 G | 156.54 mJ |
| Ours (video-only) | 35.30 | 1.49 M | 2.24 G | 4.15 mJ |

## C. Cross-dataset discussion
**Covers:** GRID WER tables, float vs quantized, unseen vs overlapped splits

"Across both benchmarks, multimodal fusion provides a robust gain over single-modality baselines, especially under noise. QAT preserves accuracy and in some configurations slightly improves it. The video-only ceiling on the GRID unseen-speaker split (35.3% WER) reflects the architectural constraints of the AKD1000 rather than a fundamental limit of lip reading itself. On NAVIR, where the visual task is much easier (small command vocabulary, controlled recording conditions, two speakers), the same architecture saturates near 0% WER."
