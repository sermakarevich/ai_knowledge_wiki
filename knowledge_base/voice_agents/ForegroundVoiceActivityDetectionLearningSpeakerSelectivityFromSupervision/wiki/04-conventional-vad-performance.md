> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Conventional VAD Performance — Interference-Aware Training, Not Architectural Inductive Bias

**In one sentence:** Mamba-FVAD stays broadly competitive with specialist conventional VADs on public and deployment-relevant sets while leading on the foreground-labeled in-house benchmark, and ablations show this selectivity comes from supervised exposure to competing-speech mixing rather than generic noise augmentation.

## Key points

- Foreground selectivity must not cost ordinary detection: with no competing speaker, an FVAD model should reduce to a conventional VAD rather than suppress single-talker speech.
- Verification covers three public sets (KAIST, VoxConverse [29], TEN-VAD test) plus two deployment-relevant conditions: a human-annotated in-house benchmark and long-form LibriVAD-concat.
- The in-house set is 9.8 h of conversational Japanese from real voice-agent interactions in noisy venues (restaurants, meeting rooms, open-plan offices) where background speech and babble are prevalent; frame-level human labels mark only the intended speaker as speech, with background/overlapping talkers and non-speech as negative.
- For LibriVAD-concat the authors follow [24], concatenating LibriSpeech recordings under clean and additive-noise conditions (SNR −5 to 20 dB), reporting ROC-AUC where available and F1@0.5 threshold as a secondary measure (Table I).
- On the public sets Mamba-FVAD trails the strongest specialist on each (MarbleNet on KAIST, Pyannote on VoxConverse, Silero-v6 on TEN-VAD) only slightly with no categorical failure, while leading on the in-house benchmark whose labeling mirrors the FVAD objective.
- On LibriVAD-concat it is strong from 5 dB SNR upward, reflecting the conventional noise/music/RIR augmentation in the IA recipe; the one weak spot visible in the chunk is −5 dB speech-shaped noise (SSN: ROC-AUC 0.70, vs ≥0.93 elsewhere).
- Ablation setup: all ablation models train on the same IA recipe as Mamba-FVAD but on a fixed budget limited to 5 epochs; the competing-speaker mixing ablation compares reference (On, each interferer rendered as far-field background), Off (no competing-speaker mixing), and Nearfield (overlap kept, far-field simulation skipped).
- Off is by far the most damaging — BG-FAR rises across the board, widening as the interferer grows louder and largest on real-recorded VOiCES — confirming that supervised exposure to unlabeled competing speech, not generic noise augmentation, is the causal ingredient for background-speech rejection (the Off model tends to fire on any speech, hence its marginally higher foreground recall).

---

## B. Conventional VAD Performance

The chunk states the requirement verbatim:

> "Foreground selectivity must not cost ordinary detection: with no competing speaker, an FVAD model should reduce to a conventional VAD rather than suppress single-talker speech."

Evaluation conditions (verbatim details):

- "We verify this on three public sets: KAIST, VoxConverse [29], Ten-VAD test; and two deployment-relevant conditions: a human-annotated in-house benchmark and long-form LibriVAD-concat."
- "The in-house set is 9.8 h of conversational Japanese from real voice-agent interactions in noisy venues (restaurants, meeting rooms, open-plan offices) where background speech and babble are prevalent."
- "Following FVAD, frame-level human labels mark only the intended speaker as speech, whereas background/overlapping talkers and non-speech are negative."
- "Because such calls interleave clean single-talker and competing-speech stretches, it jointly tests conventional detection and foreground selectivity under one label set."
- "For LibriVAD-concat we follow [24], concatenating LibriSpeech recordings under clean and additive-noise (SNR −5 to 20 dB) conditions."
- "As not all baselines expose per-frame posteriors, we report ROC-AUC where available and F1@0.5 threshold as a secondary measure (Table I)."

Results (verbatim claims):

- "On the public sets, Mamba-FVAD is broadly competitive, trailing the strongest specialist on each (MarbleNet on KAIST, Pyannote on VoxConverse, Silero-v6 on TEN-VAD) only slightly and with no categorical failure, while leading on the in-house benchmark, whose labeling mirrors the FVAD objective."
- "On LibriVAD-concat it is strong from 5 dB SNR upward, reflecting the conventional noise/music/RIR augmentation the IA recipe includes for robustness."
- "The one weak spot is −5 dB speech-shaped noise (SSN: ROC-AUC 0.70, vs ≥0.93 for …" — the sentence is cut off mid-comparison in the chunk; the remainder of Table I is not present.
- "Because the IA recipe pairs competing-speech mixing with standard noise augmentation, selectivity and general noise-robustness coexist — the speaker-selective objective adds the former without sacrificing the latter."

## C. Ablations — competing-speaker mixing (partial; chunk truncated)

- "For ablation experiments, all models were trained on the same IA recipe as Mamba-FVAD but on a fixed budget limited to 5 epochs."
- "Table II isolates the selectivity-bearing augmentation via three variants that differ only in how overlapping speech is generated: the reference (On) renders each interferer as far-field background; Off completely removes competing-speaker mixing; Nearfield keeps the overlap but skips far-field simulation."
- "Off is by far the most damaging. BG-FAR rises across the board, widening as the interferer grows louder and largest on the real-recorded VOiCES."
- "Never exposed to competing speech, the model tends to fire on any speech (hence its marginally higher foreground recall)."
- "This confirms that supervised exposure to unlabeled competing speech, not generic noise augmentation, is the causal ingredient for background-speech rejection."
- Table II ("Competing-speaker augmentation ablation: BG-FAR and foreground recall (fgRec) on Mix-Interference and VOiCES", columns S17 / S15 / S13 / S11 / S9 (loud) / S9 / music / babble / telephone / babble) is cut off mid-header in the chunk — no numeric cells are present, so no Table II numbers are reported here. The architecture-ablation portion (if any) is likewise absent from the chunk.

**Covers:** Section IV-B (Conventional VAD Performance) and opening of Section IV-C (competing-speaker mixing ablation); Table I referenced but not contained; Table II header only, numeric cells missing due to chunk truncation.
