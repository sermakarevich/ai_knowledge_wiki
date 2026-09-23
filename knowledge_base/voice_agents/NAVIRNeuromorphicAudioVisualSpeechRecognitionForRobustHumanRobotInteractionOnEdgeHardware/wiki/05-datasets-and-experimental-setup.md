[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Datasets and Experimental Setup
**In one sentence:** NAVIR is an internal 183-command / 366-recording audio-visual robot-command corpus augmented with industrial machinery noise from UrbanSound8K, evaluated alongside GRID under unseen- and overlapped-speaker protocols with flip/jitter augmentation and modality-specific QAT schedules.
## Key points
- NAVIR is a custom, internal (not publicly released) audio-visual dataset of robot-manipulation commands used to fine-tune and evaluate the deployed system.
- NAVIR contains 183 distinct commands from ~39 words in 5 categories, each with synonymous phrasings, produced in full by 2 speakers for 366 recordings total.
- UrbanSound8K (8,732 excerpts, ≤4 s, 10 classes, 10 folds) is used solely as a noise source; only the mechanical/machinery subset (air conditioner, drilling, engine idling, jackhammer) is mixed into GRID and NAVIR.
- Noise mixing uses SNRs sampled from {−15, −10, −5, 0} dB during training and a fixed −10 dB SNR for the noisy-audio test condition; the first predefined fold is held out for evaluation.
- GRID is reported under both the LipNet unseen-speaker protocol and an overlapped-speaker protocol, while NAVIR uses an 80/20 sentence-level split holding out random commands across both speakers (only 2 speakers, so it tests unseen sentences, not unseen speakers).
- Both runs apply horizontal-flip augmentation (p = 0.5) and temporal jitter (p = 0.05); after float training, hybrid quantization plus QAT fine-tuning runs 15 epochs (GRID unseen-speaker), 100 epochs (GRID overlapped), 200 epochs (NAVIR).
- Under the GRID unseen-speaker split, clean-trained audio models collapse to ~77–80% WER in noise, noisy-audio training brings this to 21.0% float / 22.5% quantized, and noisy-audio + video fusion reduces it further to 16.6% float / 14.0% quantized.
---
## B. NAVIR industrial-command corpus (internal)
**Covers:** Section IV-B

The NAVIR corpus is a custom audio-visual dataset of robot-manipulation commands developed for this project. It is an internal corpus, used to fine-tune and evaluate the deployed system but not publicly released. The corpus consists of 183 distinct commands drawn from a structured vocabulary of approximately 39 words, organised in five categories:

1) Move [object] into [location] (e.g., "Move the blue cube into the box").
2) Pick up [object] (e.g., "Grab the mouse").
3) Place [object] in [location] (e.g., "Put the green cube in the box").
4) Go to [object/location/position] (e.g., "Go above the blue cube", "Return to home").
5) Rotate [object] clockwise (e.g., "Spin the battery clockwise").

Objects are: blue cube, yellow cube, green cube, white ball, mouse, battery. Locations are: box, bin. Positional targets are: home, up, ready. Each command admits multiple synonymous phrasings (e.g., move / transfer / relocate / shift / bring), introducing lexical variation while preserving semantic equivalence. Two speakers each produced the full set of 183 commands, yielding 366 recordings. Compared to GRID, NAVIR is domain-specific and command-oriented, making it more representative of the target deployment.

## C. UrbanSound8K noise augmentation
**Covers:** Section IV-C

UrbanSound8K [36] is a publicly available corpus of 8,732 labelled urban-sound excerpts of up to 4 s, drawn from ten classes (air conditioner, car horn, children playing, dog bark, drilling, engine idling, gun shot, jackhammer, siren and street music) and pre-folded for ten-fold cross-validation. We use it solely as a noise-augmentation source. Following CochleaNet [37], we extract the mechanical and machinery subset (air conditioner, drilling, engine idling, jackhammer), which is representative of the ambient noise found in industrial settings, and mix these clips into the clean audio tracks of GRID and the NAVIR corpus at SNRs sampled from {−15, −10, −5, 0} dB during training. For evaluation, the noisy-audio test condition uses a fixed SNR of −10 dB. The first predefined fold is held out for evaluation.

## V. Experimental setup (as present in chunk)
**Covers:** Section V (partial; Table 2 referenced but not present in chunk)

Table 2 summarises the configuration of both training runs. On GRID we report both the standard unseen-speaker protocol of LipNet [28] and an overlapped-speaker protocol (speakers shared between train and test, sentences disjoint), which is the other widely reported GRID setting. NAVIR uses an 80/20 sentence-level split that holds out a random subset of commands across both speakers, so the evaluation set probes generalisation to unseen sentences rather than unseen speakers (the corpus contains only two speakers). Both runs apply horizontal-flip augmentation (p = 0.5) and temporal jitter (p = 0.05). After float training, models are quantized using the hybrid scheme of Section III-H and fine-tuned with QAT (15 epochs on GRID unseen-speaker, 100 epochs on GRID overlapped, 200 epochs on NAVIR; the longer NAVIR schedule reflects the smaller corpus and the longer overlapped schedule reflects the harder cross-sentence generalisation within a fixed speaker set).

## VI. Recognition results — GRID WER (as present in chunk)
**Covers:** Section VI-A (partial; Tables 3–6 values only)

Verbatim framing from chunk: "Under clean audio, all audio-capable models on the unseen-speaker split perform comparably (3.2–7.7% WER across configurations). The interesting contrast appears under noise. Training on clean audio collapses to roughly 77–80% WER when noise is introduced, while training on noisy audio brings this down to 21.0% (float) and 22.5% (quantized). Crucially, fusing noisy audio with video reduces WER further to 16.6% (float) and 14.0% (quantized)."

Table 3 — Non-quantized WER (%) on GRID (unseen-speaker split):

| Training modalities | Clean audio | Noisy audio |
|---|---|---|
| Clean audio | 3.7 | 79.9 |
| Noisy audio | 4.4 | 21.0 |
| Video | 34.0 | 34.0 |
| Noisy audio + video | 7.7 | 16.6 |
| Clean audio + video | 3.6 | 78.6 |

Table 4 — Quantized WER (%) on GRID (unseen-speaker split) after QAT:

| Training modalities | Clean audio | Noisy audio |
|---|---|---|
| Clean audio | 4.2 | 77.3 |
| Noisy audio | 5.2 | 22.5 |
| Video | 35.3 | 35.3 |
| Noisy audio + video | 5.3 | 14.0 |
| Clean audio + video | 3.2 | 77.8 |

Table 5 — Non-quantized WER (%) on GRID (overlapped-speaker split), 100 epochs:

| Training modalities | Clean audio | Noisy audio |
|---|---|---|
| Clean audio | 1.3 | 79.8 |
| Noisy audio | 1.9 | 10.4 |
| Video | 9.1 | 9.1 |
| Noisy audio + video | 0.7 | 2.8 |
| Clean audio + video | 0.7 | 77.4 |

Table 6 — Quantized WER (%) on GRID (overlapped-speaker split) after QAT:

| Training modalities | Clean audio | Noisy audio |
|---|---|---|
| Clean audio | 2.0 | 78.7 |
| Noisy audio | 2.3 | 11.8 |
| Video | 6.7 | 6.7 |
| Noisy audio + video | 0.8 | 3.3 |
| Clean audio + video | 0.8 | 77.1 |
