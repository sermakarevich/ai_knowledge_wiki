> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Ablations: supervision drives selectivity, backbone is secondary

**In one sentence:** Competing-speaker mixing and foreground-only supervision create foreground selectivity while the temporal backbone (Mamba vs LSTM vs Transformer) matters little, and the resulting model behaves like selective attention with known boundary failures when the target is not dominant.

## Key points

- A louder, sustained speech-like masker inverts the training dominance cue (interferers always quieter than the target) and the model suppresses the now-quietest true foreground — the stated boundary case of the selectivity prior.
- On VOiCES, where competitors are physically distant and reverberant, the far-field reference wins at every distractor because its training interferers match real background acoustics, at only a one-to-two point recall cost.
- Table III (identical IA recipe, iso-parameter temporal decoders): Mamba edges out the LSTM by at most ~2 points of ROC-AUC, each leading on some sets, while the Transformer trails on every benchmark despite its larger context.
- Foreground selectivity is driven primarily by the supervision strategy while backbone choice is secondary and therefore a deployment choice: Mamba adopted for O(1) streaming recurrence, LSTM a near-equivalent lighter alternative.
- The model locks onto an established dominant speaker, falls back to conventional VAD before any primary speaker enters, and returns to silence when the target stops even though background speech continues — a switch not explainable by acoustic change alone.
- Selection is not loudness tracking: a quiet target near utterance end (~31 s) is still detected, background talkers are suppressed with clean boundaries, and with no speaker-embedding module the model follows speaker changes without re-enrollment at 1–2 ms per-frame CPU latency.
- Limits: the dominant-foreground commitment under-fires when the target is not dominant (recall falls at extreme negative SNR; VOiCES far-field recall drops under acoustic shift), and the work assumes a single foreground speaker per segment.

---

## Boundary case of the selectivity prior

**Covers:** non-speech noise / dominance-cue inversion paragraph

> "non-speech noise). This represents the boundary case of the selectivity prior, whose training interferers are always quieter than the target, so a louder, sustained speech-like masker inverts the dominance cue and the model suppresses the now-quietest true foreground."

Nearfield vs far-field rendering paragraph (garbled table row in chunk):

| Condition | Row values as printed (unlabelled columns) |
|---|---|
| On (ref) | 0.059, 0.088, 0.140, 0.226, 0.357, 0.946, 0.141, 0.270, 0.183, 0.848 |
| Off | 0.076, 0.112, 0.184, 0.300, 0.462, 0.957, 0.231, 0.342, 0.235, 0.877 |
| Nearfield | 0.065, 0.091, 0.134, 0.219, 0.359, 0.962, 0.193, 0.313, 0.230, 0.858 |

> "Nearfield shows that how the overlap is rendered governs real-world transfer. On synthetic Mix-Interference near- and far-field are nearly indistinguishable, but on VOiCES, where competitors are physically distant and reverberant, the far-field reference wins at every distractor, its training interferers matching real background acoustics. For only a one to two point recall cost, far-field competing-speaker mixing both rejects background speech and generalizes."

## Architecture ablation (Table III)

**Covers:** Architecture subsection + Table III

> "Architecture. Table III compares the three iso-parameter temporal decoder backbones under the identical IA recipe on the conventional VAD benchmarks. Mamba only very slightly edges out the LSTM, differing by at most ∼2 points of ROC-AUC, with each leading on some sets (Mamba on KAIST 0.962 and TEN-VAD 0.910, the LSTM on VoxConverse 0.930), at comparable parameter count."

> "TABLE III: Architecture ablation: ROC-AUC across benchmarks. LibriVAD-concat is frame-weighted over all noises and SNRs."

| Decoder | KAIST | VoxConverse | Ten VAD | In-house | LibriVAD concat | Params |
|---|---|---|---|---|---|---|
| Transf. | 0.893 | 0.746 | 0.858 | 0.927 | 0.876 | 615,369 |
| LSTM | 0.953 | 0.930 | 0.891 | 0.977 | 0.922 | 662,657 |
| Mamba | 0.962 | 0.922 | 0.910 | 0.978 | 0.923 | 615,297 |

> "The Transformer trails on every benchmark despite its larger context. However, we acknowledge that the Transformer trained less stably on this data regime despite hyperparameter tuning and also required chunking on long clips; hence we treat its scores as a floor."

> "Together with the matched Mamba/LSTM selectivity in Section IV-A and the competing-speaker ablation in Section IV-C, the results suggest that foreground selectivity is driven primarily by the proposed supervision strategy, while the choice of backbone appears to play a secondary role under the evaluated settings. The backbone is therefore a deployment choice: we adopt Mamba for its O(1) streaming recurrence, with the LSTM a near-equivalent, lighter alternative."

## Performance analysis: learned contextual selection (Fig. 3)

**Covers:** Section D, Performance Analysis / Fig. 3 a–c

> "Fig. 3: Mamba-FVAD inference on a multi-talker recording: the model locks onto the dominant speaker (c) while gracefully degrading to standard VAD in the absence of a primary speaker (a, b)."

- Before the primary speaker enters (first ∼3 s of Fig. 3c), no dominant speaker yet exists, so the model falls back to conventional VAD and marks preceding speech-plus-noise as active.
- Once the primary speaker appears it locks onto that target; when the speaker stops (∼4 s later) it returns to silence even though background speech continues.
- Because the background spectrum is nearly identical before and after the target's turn, "this switch cannot be explained by acoustic change alone; it reflects learned contextual selection."
- "Selection is not driven by loudness. Near the end of an utterance (∼31 s), the target is quiet yet still detected, indicating the model holds a stable latent representation of the foreground rather than tracking instantaneous amplitude."
- "Background talkers are consistently suppressed with clean segment boundaries, and because FVAD carries no explicit speaker-embedding module, it follows speaker changes without re-enrollment, keeping the model lightweight."
- "When no primary speaker is present (Figs. 3(a),(b)), it gracefully reverts to conventional VAD, marking all speech active."
- "Overall, Mamba-FVAD behaves like human auditory attention — focusing on a target, suppressing competitors, and falling back to general-purpose VAD when no target is established — at 1–2 ms per-frame latency on an AWS t2.micro instance, confirming real-time CPU-only deployment."

## Conclusion and limitations (Section V)

**Covers:** Section V, Conclusion and Limitations

> "We formalized Foreground VAD (FVAD), an enrollment-free, frame-synchronous task that tracks a single dominant speaker and reduces to conventional VAD when only one is present, and introduced BG-FAR and Foreground F1 to measure it."

> "Our central finding is that foreground selectivity primarily comes from supervision: a fully automatic recipe pairing foreground-only labels with competing-speaker mixing turns an ordinary streaming VAD selective, and iso-parameter Mamba, LSTM, and Transformer backbones confirm that temporal-modeling capacity is at most a secondary factor."

> "The resulting model, Mamba-FVAD, surpasses commercial VADs and enrollment-based speaker-aware systems on selectivity while staying competitive on conventional VAD and maintaining 1–2 ms per-frame CPU latency. The Mix-Interference benchmark will be released to support further study."

> "The selectivity that drives these gains also bounds the method. Because the model commits to a dominant foreground, it under-fires when the target is not the dominant source: recall falls at extreme negative SNR on all-speech-positive benchmarks, and on out-of-distribution far-field speech (VOiCES) selectivity transfers but foreground recall drops under the acoustic shift. We also assume a single foreground speaker per segment, leaving turn-taking and co-equal speakers to future work."

**Covers:** chunk 05-non-speech-noise-this-represents-the-boundary (boundary-case paragraph through Section V conclusion); footnotes 1–4 list generic-VAD links (py-webrtcvad, auditok, jtkim-kaist/VAD, TEN-VAD testset).
