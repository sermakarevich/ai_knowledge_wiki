> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Benchmark and Selectivity Metric: BG-FAR vs Foreground F1
**In one sentence:** Genuine foreground selectivity requires high Foreground F1 together with low Background False-Alarm Rate (BG-FAR), and only the interference-aware (IA) models achieve this bottom-right region while LibriVAD-recipe and generic VAD baselines fire on background speech.
## Key points
- Foreground F1 uses foreground-speech frames as positives and penalizes both missed foreground speech (recall) and activation on any foreground-silent frame including silence, noise, or competing speech (precision).
- BG-FAR is defined as `P(yτ = 1 | foreground-silent ∧ background-active)` at operating threshold 0.5, bounded by 0 (complete rejection) and 1 (complete acceptance).
- Background-active frames are obtained without extra annotation from paired frame-aligned takes (noise-only take in Mix-Interference, none take in VOiCES), marking foreground-silent frames whose energy exceeds the reference by margin δ = 6 dB.
- On Mix-Interference swept over SNR 9–17 dB, IA models (Mamba-FVAD and iso-parameter LSTM) hold Foreground F1 0.88–0.92 with BG-FAR from 0.05 at 17 dB to at most 0.40 at 9 dB, while every other system exceeds 0.8 BG-FAR at the loudest interferer.
- LibriVAD-recipe models share the same architectures as the IA models yet collapse into the high-BG-FAR region, isolating the data recipe as the cause of selectivity.
- Enrolled pVAD is the only baseline keeping BG-FAR low at a flat ∼0.23 interferer-independent band, but at far lower Foreground F1; removing enrollment (Standard VAD) returns BG-FAR to the LibriVAD region.
- On out-of-distribution distant-speech VOiCES, Mamba-FVAD stays near its music floor (telephone 0.07 vs music 0.06, babble 0.12), while Silero shows a large speech-specific gap (music 0.12 vs telephone 0.18, babble 0.27).
- Varying the backbone (Mamba→LSTM) under the IA recipe largely preserves selective behavior, whereas varying the recipe (IA→LibriVAD) collapses it to that of a conventional VAD.
---
## Foreground F1
**Covers:** metric definition preceding Fig. 2
- Foreground-speech frames are positives; the score is the harmonic mean of precision and recall.
- Recall penalizes missed foreground speech; precision penalizes activation on any foreground-silent frame (silence, noise, or competing speech).
- Reported together with its recall component, it acts as a gate: "a model cannot appear 'selective' merely by being conservative as suppressing the target collapses recall and hence F1."
## BG-FAR definition and background-active mask
**Covers:** metric definition and Appendix A/B pointer
- Formula: `BG-FAR = P(yτ = 1 | foreground-silent ∧ background-active)`.
- Ordinary FAR over all silent frames "is dominated by easy true silence and dilutes this signal"; conditioning on background-active frames targets "exactly the hard case."
- Frame-exact mask comes from paired, frame-aligned takes with the same foreground and environment but no competing speaker; a foreground-silent frame is background-active when its energy exceeds the reference by more than δ (6 dB in this paper).
- Operating threshold 0.5; bounded by 0 and 1, "denoting complete rejection and complete acceptance respectively."
- "Neither suffices alone, for example, a silent model trivially attains BG-FAR = 0 but fails Foreground F1, whereas a generic VAD attains high recall but high BG-FAR."
- "The full algorithms are described in Appendix A and B."
## Results: Fig. 2 Mix-Interference (SNR 9–17 dB)
**Covers:** Sec. IV.A, Fig. 2 top
- Plot is BG-FAR vs Foreground F1; "The ideal FVAD model falls in the bottom-right" / "An ideal FVAD model sits bottom-right with high foreground tracking, low BG-FAR."
- Baselines: production-grade Silero-v6, pretrained enrolled pVAD, Standard VAD (pVAD's architecture, no enrollment), and energy-based Auditok.
- Marker size encodes interferer loudness (big = 9 dB, small = 17 dB); systems drift "up the BG-FAR axis as the interferer becomes louder, exceeding 0.8 at the loudest."
- IA region: Foreground F1 0.88–0.92; BG-FAR from 0.05 at 17 dB to at most 0.40 at 9 dB.
- "Critically, the LibriVAD-recipe models share the same architectures yet collapse into this high-BG-FAR region, isolating the data recipe as the cause."
- Enrolled pVAD: BG-FAR low at "a flat ∼0.23 band, interferer-independent (as expected from an external speaker prior) but at far lower Foreground F1."
## Results: Fig. 2 VOiCES by distractor
**Covers:** Sec. IV.A, Fig. 2 bottom
- Distractors form a built-in control: "music is non-speech, so its BG-FAR measures only generic non-speech suppression, whereas babble and telephone are competing speech."
- "The gap between babble/telephone and music thus isolates false alarms specific to background speech; a true speaker-rejecter stays near its music floor, a generic 'any-speech' detector does not."
- Mamba-FVAD: "telephone (0.07) sits at the music floor (0.06) and babble (0.12) only just above, a small speech-specific excess."
- Silero: "music 0.12 vs. telephone 0.18, babble 0.27."
- "On this out-of-distribution distant-speech set Mamba-FVAD pays a small recall penalty (lower Foreground F1) yet rejects background speech as well as or better than the enrolled pVAD—without enrollment."
- Backbone vs recipe: "varying the backbone (Mamba→LSTM) under the IA recipe largely preserves the selective behavior, whereas varying the recipe (IA→LibriVAD) collapses it to that of a conventional VAD."
## Table I excerpt present in chunk
**Covers:** Table I header and rows as captured in chunk
| Model | KAIST | Voxconverse test | In-house | LibriVAD concat clean | SNR=-5 | SNR=0 | SNR=5 | SNR=10 | SNR=15 | SNR=20 |
|---|---|---|---|---|---|---|---|---|---|---|
| webRTC1 | – / 0.688 | – / 0.433 | – / 0.891 | – / 0.587 | – / 0.930 | – / 0.288 | – / 0.332 | – / 0.332 | – / 0.465 | – / 0.564 | – / 0.675 |
| Auditok2 | – / 0.586 | – / 0.941 | – / 0.886 | – / 0.614 | – / 0.938 | – / 0.802 | – / 0.802 | – / 0.803 | – / 0.807 | – / 0.834 | – / 0.899 |
| SpeechBrain [27] | 0.966 / 0.831 | 0.858 / 0.960 | 0.677 / 0.840 | 0.842 / 0.560 | 0.874 / 0.916 | 0.808 / 0.870 | 0.823 / 0.886 | 0.821 / 0.893 | 0.816 / 0.896 | 0.811 / 0.898 | 0.808 / 0.899 |
| Pyannote VAD [23] | – / 0.945 | – / 0.975 | – / 0.917 | – / 0.655 | – / 0.950 | – / 0.890 | – / 0.909 | – / 0.917 | – / 0.923 | – / 0.928 | – / 0.934 |
| FSMN-VAD [28] | – / 0.932 | – / 0.972 | – / 0.871 | – / 0.705 | – / 0.918 | – / 0.847 | – / 0.895 | – / 0.901 | – / 0.902 | – / 0.903 | – / 0.904 |
| Ten VAD [2] | 0.989 / 0.927 | 0.930 / 0.949 | 0.942 / 0.928 | 0.969 / 0.851 | 0.980 / 0.955 | 0.835 / 0.807 | 0.882 / 0.880 | 0.912 / 0.904 | 0.932 / 0.918 | 0.948 / 0.927 | 0.960 / 0.934 |
| MarbleNet [18] | 0.994 / 0.947 | 0.962 / 0.966 | 0.920 / 0.912 | 0.973 / 0.616 | 0.979 / 0.955 | 0.890 / 0.895 | 0.919 / 0.912 | 0.935 / 0.919 | 0.945 / 0.925 | 0.953 / 0.929 | 0.958 / 0.933 |
| Silero-v5 [1] | 0.992 / 0.926 | 0.947 / 0.946 | 0.925 / 0.903 | 0.966 / 0.728 | 0.979 / 0.952 | 0.846 / 0.809 | 0.909 / 0.905 | 0.943 / 0.922 | 0.963 / 0.932 | 0.971 / 0.941 | 0.975 / 0.949 |
| Silero-v6 [1] | 0.992 / 0.947 | 0.952 / 0.952 | 0.957 / 0.939 | 0.966 / 0.862 | 0.981 / 0.960 | 0.846 / 0.831 | 0.918 / 0.914 | 0.946 / 0.930 | 0.963 / 0.937 | 0.972 / 0.944 | 0.976 / 0.953 |
| Mamba-FVAD (IA) | 0.986 / 0.910 | 0.933 / 0.929 | 0.910 / 0.890 | 0.982 / 0.884 | 0.979 / 0.960 | 0.830 / 0.712 | 0.916 / 0.884 | 0.958 / 0.933 | 0.970 / 0.947 | 0.974 / 0.953 | 0.976 / 0.956 |
- Scored by ROC-AUC / F1@0.5; table title in chunk: "TABLE I: Conventional VAD Performance Benchmark, scored by ROC-AUC / F1@0.5".
**Covers:** BG-FAR/Foreground F1 definitions through Sec. IV.A plus Table I rows captured in chunk 03
