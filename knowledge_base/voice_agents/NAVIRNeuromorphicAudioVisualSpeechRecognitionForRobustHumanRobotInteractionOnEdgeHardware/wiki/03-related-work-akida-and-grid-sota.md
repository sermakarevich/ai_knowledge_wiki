> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related Work: AKD1000 Applications and GRID Lip-Reading State of the Art
**In one sentence:** Prior AKD1000 work shows strong energy advantages on lightweight sparse inference but is limited by single-node capacity, idle floor, and unsupported primitives, while GRID lip-reading SOTA (1.83–4.8% WER overlapped) relies on 3D convolutions, recurrence, or attention that AKD1000 does not support, leaving noisy-audio AVSR fusion on GRID an open gap.
## Key points
- Benoot et al. [15] integrate the AKD1000 (and forthcoming AKD1500) into a heterogeneous on-board satellite data-processing unit.
- Lutes et al. [16] exploit on-chip edge learning for individualised braking-intent EEG classification in the biomedical domain.
- Bråtman and Dow [17] characterise edge-learning hyperparameters for intracranial-pathology CT classification.
- Across these works, the AKD1000 consistently delivers strong energy advantages on lightweight, sparse inference, limited by single-node model capacity, the high idle floor, and constraints on architectural primitives.
- GRID [18] is the standard sentence-level lip-reading benchmark; LRW [19], LRS2 [20], LRS3 [21], TCD-TIMIT [22], AVSpeech [23], and ASPIRE [24] extend coverage to in-the-wild sentences and noisy conditions.
- On the SNN side, DVS-Lip-Audio [25] provides event-based audio-visual lip data, while SHD/SSC [26] and Speech Commands [27] provide audio-only benchmarks.
- GRID overlapped-speaker SOTA runs from LipNet 4.80% (2016) down to Wu et al. 1.83% (2024), with unseen-speaker results far worse (LipNet 11.40%, HLR-Net 9.70%, Wu et al. 10.21%).
- No published results exist for full AVSR fusion on GRID under noisy audio conditions, presenting both a literature gap and a comparison point for any neuromorphic approach.
---
## AKD1000 edge applications
**Covers:** Benoot et al. [15], Lutes et al. [16], Bråtman and Dow [17]; AKD1000 strengths and limits

- Benoot et al. [15] integrate the "AKD1000 (and the forthcoming AKD1500) into a heteroge-neous on-board satellite data-processing unit."
- In the biomedical domain, "Lutes et al. [16] exploit on-chip edge learning for individualised braking-intent EEG classification, and Bråt-man and Dow [17] characterise edge-learning hyperparame-ters for intracranial-pathology CT classification."
- "Across these works, the AKD1000 consistently delivers strong energy advantages on lightweight, sparse inference, while its primary limits are single-node model capacity, the high idle floor and constraints on architectural primitives."

## AVSR datasets and audio-only SNN benchmarks
**Covers:** GRID corpus and related corpora; DVS-Lip-Audio, SHD/SSC, Speech Commands

- "The GRID corpus [18] is the standard sentence-level bench-mark for lip reading. LRW [19], LRS2 [20], LRS3 [21], TCD-TIMIT [22], AVSpeech [23] and ASPIRE [24] extend coverage to in-the-wild sentences and noisy conditions."
- "On the SNN side, DVS-Lip-Audio [25] provides event-based audio-visual lip data, while SHD/SSC [26] and the broader Speech Commands corpus [27] provide audio-only bench-marks."
- "Detailed descriptions of the corpora used in this work are deferred to Section IV."

## Lip reading on the GRID corpus
**Covers:** LipNet through Wu et al.; Table 1; trends and AVSR-fusion gap

| Model | Year | Setting | WER (%) |
|---|---|---|---|
| LipNet [28] | 2016 | Overlapped | 4.80 |
| WLAS [29] | 2017 | Overlapped | 3.00 |
| LCANet [30] | 2018 | Overlapped | 2.90 |
| LipSound [31] | 2019 | Overlapped | 2.50 |
| DualLip [32] | 2020 | Overlapped | 2.71 |
| HLR-Net [33] | 2021 | Overlapped | 3.30 |
| LCSNet [34] | 2023 | Overlapped | 2.30 |
| Wu et al. [35] | 2024 | Overlapped | 1.83 |
| LipNet [28] | 2016 | Unseen | 11.40 |
| HLR-Net [33] | 2021 | Unseen | 9.70 |
| Wu et al. [35] | 2024 | Unseen | 10.21 |

Table caption (verbatim): "TABLE 1. State-of-the-art lip-reading WER on the GRID corpus. All baselines use full 3D convolutions, recurrent layers or attention, none of which are supported on AKD1000."

- "LipNet [28] established the modern baseline by com-bining three-dimensional spatio-temporal CNNs with bidi-rectional GRUs and connectionist temporal classification (CTC) loss, mapping mouth-region frames directly to char-acter sequences and achieving 4.8% WER on the overlapped split (11.4% WER unseen-speaker)."
- "The Watch, Listen, At-tend, and Spell (WLAS) architecture [29] added attention-based sequence-to-sequence decoding and curriculum learn-ing, reaching 3.0% WER."
- "LCANet [30] addressed CTC's conditional-independence assumption via cascaded attention-CTC decoding, reaching 2.9% WER."
- "LipSound [31] recon-structed the mel-spectrogram from lip video and ran ASR on the result, reaching 2.5% WER."
- "DualLip [32] introduced a generation/recognition dual learning scheme." (chunk gives no WER in prose; table lists 2.71% overlapped)
- "HLR-Net [33] combined inception modules with attention-CTC, reaching 3.3% WER overlapped and 9.7% WER unseen-speaker."
- "LC-SNet [34] added channel-attention and selective-feature fu-sion, reaching 2.3% WER."
- "Most recently, the landmark-guided cross-speaker model of Wu et al. [35], built on a hybrid CTC/attention conformer back-end with mutual-information regularisation, reached 1.83% WER overlapped and 10.21% WER on the unseen-speaker split."
- "Several trends are noteworthy. First, attention-augmented decoders consistently improve over CTC alone by better modelling output dependencies. Second, the visual front-end remains a primary bottleneck, and methods that improve it through channel attention, landmark localisation or interme-diate acoustic reconstruction yield large gains. Third, the gap between overlapped and unseen-speaker performance remains substantial. Finally, no published results exist for full" — "AVSR fusion on GRID under noisy audio conditions, present-ing both a gap in the literature and a relevant comparison point for any neuromorphic approach."
