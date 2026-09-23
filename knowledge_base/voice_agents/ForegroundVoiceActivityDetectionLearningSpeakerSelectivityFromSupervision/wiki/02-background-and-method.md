[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Background and Method: Introduction, Related Work, and Interference-Aware Recipe
**In one sentence:** The paper defines enrollment-free Foreground VAD (dominant-speaker-selective, reducing to conventional VAD with one speaker) and argues foreground selectivity comes primarily from an automatic interference-aware supervision recipe rather than from larger temporal-modeling capacity.
## Key points
- FVAD is formalized as frame-synchronous binary classification where a frame is positive if and only if it contains speech from the foreground speaker, defined by greatest sustained speech presence and temporal identity coherence rather than instantaneous energy, so a momentarily louder competitor must not capture the role.
- FVAD is enrollment-free yet identity-committed: unlike personal/target-speaker VAD which models P(yτ | x, et) over target-speaker speech / non-target-speaker speech / non-speech given an enrollment et, FVAD models the binary posterior P(yτ = 1 | x) for an endogenously inferred foreground F(x), assuming one foreground speaker per segment.
- The paper motivates FVAD with three crowded-setting failures (restaurants, public squares, meeting rooms): background speech reaches noise-robust ASR and causes erroneous LLM responses, withholds the VAD falling edge that triggers generation (perpetual listening), and falsely triggers barge-in.
- The decisive supervision recipe is fully automatic with no human annotation: clean utterances are pseudo-labeled by Silero-v6 plus energy-adaptive edge refinement (separate onset/offset factors absorbing asymmetric detector lag), then 1–3 held-out interfering-speaker segments covering 10–50% of the utterance are mixed at 0–15 dB target-to-interference ratio (p = 0.2) with DNS-Challenge RIRs and 1–4 kHz low-pass, leaving foreground labels unchanged so competing speech is supervised as negative.
- General-robustness augmentations are applied stochastically per utterance at load time: environmental noise (p = 0.45, easy [5, 20] dB / hard [−5, 5] dB), music (p = 0.15, [5, 20] dB), target reverberation (p = 0.2), ±6 dB gain perturbation with per-segment dynamics, hard non-speech negatives (1–2% each), and telephone band-pass (300–3400 Hz / 50–7000 Hz).
- The primary system Mamba-FVAD (~0.6M parameters) pairs a streaming-adapted LEAF front-end (temporal pooling removed, Gaussian pooling replaced by global average pooling, 512-sample frames at 31.25 Hz) with a Mamba state-space decoder giving O(1) per-frame compute and memory; iso-parameter LSTM (limited context) and offline Transformer (unbounded in-window, length-growing cost) controls plus a conventional-LibriVAD-recipe control isolate the recipe's contribution.
- The Mix-Interference benchmark pits one LibriSpeech test-other foreground track against one far-field-simulated competitor (random small/medium room, near/medium distance, 4–8 kHz low-pass, ±10 s offset) across seven frame-locked 16 kHz variants (clean; noise-only at ≈6 dB; five interference takes at 9, 11, 13, 15, 17 dB with ≈15 dB noise, peak-normalized to 0.95) with foreground-only labels; adapted VOiCES (none / musi / babb / tele, physically recorded far-field) serves as the out-of-distribution cross-check with background talkers left unlabeled.
---
## I. Introduction — task definition and central claim
**Covers:** Section I (Introduction, task formalization, contributions)

Foreground VAD is a frame-synchronous, enrollment-free task in which only the dominant speaker, defined by sustained presence rather than instantaneous loudness, is positive, and which reduces to conventional VAD when a single speaker is present.

> "We formalize Foreground VAD (FVAD): a frame-synchronous, enrollment-free task in which only the dominant speaker, defined by sustained presence rather than instantaneous loudness, is positive, and which reduces to conventional VAD when a single speaker is present."

Formal definition given in the chunk:

| Paradigm | Posterior | Target source |
|---|---|---|
| Personal / target-speaker VAD | P(yτ \| x, et) over tss / ntss / ns given enrollment et | Exogenous enrolled identity |
| Foreground VAD | P(yτ = 1 \| x) for foreground speaker F(x) | Endogenous, self-derived pseudo-enrollment inferred online and kept coherent |

Additional definitional constraints from the chunk: the foreground role is defined by sustained presence and temporal identity coherence, not instantaneous energy (defining it by frame-wise loudness would collapse the task into energy-based VAD); non-foreground speech is negative; one foreground speaker per segment is assumed, the identity the model commits to and tracks throughout.

Three claimed distinguishing axes versus existing paradigms: it strictly generalizes VAD (no separation front-end), it is enrollment-free yet identity-committed (unlike pVAD or energy-following detection), and it runs in a single streaming stage (unlike a VAD-plus-diarization cascade).

> "Our central finding is that foreground focus is governed largely by supervision, not architecture."

Supporting observations quoted in the chunk: across equal-size backbones, Mamba and LSTM perform on par while a longer-context attention model is no better, and the resulting lightweight streaming model Mamba-FVAD outperforms commercial VADs and enrollment-based speaker-aware systems in foreground selectivity while staying competitive on conventional VAD at 1–2 ms per-frame CPU latency.

Key contributions as listed in the chunk:
- Task and metric: formal enrollment-free dominant-speaker-selective VAD plus Background False-Alarm Rate (BG-FAR), the probability of firing while only competing speech is active and the foreground is silent, gated by foreground F1.
- New benchmark: Mix-Interference (target mixed with competing speech at controlled SNRs) plus adapted VOiCES (real far-field television and babble noise); Mix-Interference to be released.
- Data recipe: fully automatic pipeline yielding large-scale frame-level FVAD supervision without human annotation; architecture and data ablations show the recipe primarily unlocks foreground focus.
- Model: Mamba-FVAD, lightweight streaming, surpassing mainstream commercial VADs and specialized speaker-aware systems on the benchmark while remaining competitive on conventional VAD in clean and noisy conditions.

## II. Related work — why existing approaches do not solve FVAD
**Covers:** Section II (production VADs, energy gating, enhancement, identity-aware lines)

Production VADs (Silero [1], TEN-VAD [2], MarbleNet [18], related neural detectors [3], [7], [8]) give robust low-latency frame-level detection but are trained to detect all speech; competing speakers are treated as positive examples rather than interference. Modern systems achieve strong robustness, ultra-low latency, and efficient CPU-only inference at 30 Hz or higher, yet classify all human speech — background speakers included — as valid activity. Deployed VADs often use LSTMs or GRUs [7], [8] with only a few hundred milliseconds of effective context.

Energy-gated VAD (assuming the foreground is closest to the microphone) is rejected because instantaneous energy is an unreliable proxy for the foreground role: foreground speech may be soft at utterance boundaries while a background interjection can be momentarily loud; smoothing energy statistics over a longer window trades flicker for latency; hand-tuned thresholds transfer poorly across devices and environments.

Speech-enhancement front-ends [19], [20] raise SNR before VAD but optimize perceptual quality over speaker selectivity: they are trained to preserve all speech, denoise background speakers alongside the foreground, erase the level and reverberation cues that distinguish them, and add cascade latency in the single-speaker conditions that dominate real usage.

Identity-aware alternatives and their stated gaps:

| Line | Stated limitation for FVAD |
|---|---|
| Streaming end-to-end diarization [21], [22] | Attributes all speakers ("who spoke when"), typically needs look-ahead, leaves the foreground unchosen |
| Personal / target-speaker VAD [4]–[6] | Conditions on an enrollment embedding; strong selectivity only for a pre-registered identity, fails when the speaker is unknown or enrollment is mismatched |
| Post-VAD diarization [23] | Accurate offline but introduces multi-stage latency |
| FVAD (this paper) | Foreground inferred endogenously (no enrollment), committed to as one coherent identity, produced by one streaming detector (no cascade) |

## III.A. Interference-aware data recipe
**Covers:** Section III.A (training data, dynamic augmentation)

Training labels are constructed without human annotation: clean utterances are first pseudo-labelled by Silero-v6 [1], then passed through an energy-adaptive edge refinement that relocates each segment's onset and offset to the local acoustic boundary, placing the decision threshold a fixed fraction of the way from the local noise floor toward speech energy with separate onset/offset factors to absorb the asymmetric boundary lag of the base detector. The corpus combines an in-house Japanese call-centre dataset of real conversational speech (1,128 hours) with concatenated LibriSpeech read speech with inter-utterance silences, similar to the LibriVAD [24] recipe.

Augmentations are applied stochastically per utterance at load time rather than as pre-computed fixed mixtures, so every epoch presents new conditions:

| Augmentation | Parameters in chunk |
|---|---|
| Competing-speaker mixing (selectivity-bearing) | 1–3 interfering segments from held-out pool, covering 10–50% of utterance, target-to-interference ratio 0–15 dB over speech-active frames, p = 0.2; interferer convolved with DNS-Challenge [25] RIR (50/50 simulated/real) plus random 1–4 kHz low-pass; foreground labels unchanged (competing speech supervised as negative) |
| Environmental noise | p = 0.45, scattered or full-length, bimodal SNR easy [5, 20] dB / hard [−5, 5] dB |
| Music | p = 0.15, [5, 20] dB |
| Room reverberation on target | p = 0.2 |
| Gain perturbation | ±6 dB with per-segment level dynamics |
| Hard non-speech negatives | Noise-, silence-, music-, and far-field-speech-only clips, 1–2% each |
| Telephone band-pass | 300–3400 Hz / 50–7000 Hz, stated to sharpen rejection without eroding foreground recall |

## III.B. Model architecture and experimental setup
**Covers:** Section III.B (front-end, backbones, training)

The system pairs a learnable acoustic front-end with a temporal backbone and per-frame classification head, processing raw audio frame-wise. The front-end is a LEAF encoder [12] adapted for streaming: temporal pooling removed and Gaussian pooling replaced by global average pooling to preserve frame-level resolution, operating on pre-segmented 512-sample frames at a fixed 31.25 Hz.

| Backbone | Context / cost characterization in chunk |
|---|---|
| Mamba state-space decoder [13] (primary, Mamba-FVAD, ~0.6M parameters) | Linear-time recurrence, O(1) per-frame compute and memory, low-latency CPU-only streaming |
| LSTM [14] | Recurrent model with more limited effective context [15]; O(1) per-frame cost, streams |
| Transformer [16] | Unbounded in-window context but length-growing cost; does not stream; serves as offline upper bound |

All backbones train with AdamW (lr 10−4, weight decay 0.01, cosine schedule with linear warmup), batch size 16, dropout 0.3, bf16 mixed precision; the Transformer uses a reduced learning rate and longer warmup for stable convergence. Models trained with the Section III.A recipe are called interference-aware (IA); as a control each backbone is also trained under the conventional LibriVAD recipe [24] to isolate the recipe's contribution.

## III.C. Benchmark creation
**Covers:** Section III.C (Mix-Interference, adapted VOiCES)

Mix-Interference foreground utterances come from concatenated LibriSpeech [26] test-other recordings with frame-level VAD labels (31.25 Hz) from an energy-based labeler; these labels define the foreground throughout. For each foreground clip seven temporally aligned 16 kHz variants are synthesized: (1) clean target; (2) target + environmental noise; (3–7) target + the same noise + a competing speaker at five fixed target-to-interference SNRs of 9, 11, 13, 15, 17 dB. The competitor is a different test-other utterance passed through far-field simulation (random small/medium room, near/medium distance, 4–8 kHz low-pass) and offset by a random temporal delay (±10 s) so it behaves as an intermittent background talker. Level ratios are VAD-weighted RMS over speech-active frames: noise at ≈15 dB SNR for interference variants and harsher ≈6 dB for the noise-only variant; each mixture peak-normalized to 0.95. Every variant retains foreground-only labels (competitor never labeled as speech); because the five mixed variants share target, noise, and interferer and differ only in interferer level, takes are frame-locked for paired per-frame contrasts.

Adapted VOiCES devkit [17] is the out-of-distribution benchmark: clean LibriSpeech utterances replayed through a loudspeaker and re-recorded by far-field microphones in real rooms, so reverberation, distance, and the distractor (none / musi / babb / tele, where babb/tele are competing background speech) are physically baked in with nothing mixed at conversion time. The distant recording is the input; foreground-only labels come from keying the target speaker's word-level timestamps from the original source forced alignments to each segment while recorded background talkers stay unlabeled (negative). Every segment is recorded under all conditions and frame-aligned, so the matched none take serves as a per-frame clean reference for paired metrics like BG-FAR.
