> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Contributions

**In one sentence:** Industrial voice control fails under acoustic noise, so NAVIR builds an end-to-end audio-visual speech recognizer that fuses lip-motion with audio using only sequential 2D convolutions executable on the BrainChip Akida neuromorphic processor.

## Key points

- Audio-only ASR degrades sharply in industrial settings due to noise from machinery, ventilation, and ambient activity, forcing workers back to keypads, touchscreens, or physical switches that slow workflows and compromise hands-free safety.
- AVSR exploits the same redundancy as the human perceptual system (McGurk illusion [1]), integrating the visual appearance of the speaker's mouth to deliver robustness gains at low signal-to-noise ratios.
- State-of-the-art AVSR relies on 3D convolutions, recurrent units, attention/conformer encoders, and large transformer language models that assume GPU-class hardware and exceed typical edge-device budgets.
- NAVIR targets the BrainChip AKD1000 neuromorphic SoC, which natively supports only sequential 2D convolutional inference, factorizing encoding into a per-frame visual encoder, a temporal video encoder, and a spectrogram audio encoder fused by a lightweight predictor head with constrained beam-search decoding.
- Models are trained with connectionist temporal classification on noise-augmented audio, then fine-tuned with quantization-aware training.
- On GRID, the quantized audio-visual model reaches 14.0% WER under noise on the unseen-speaker split and 3.3% WER on the overlapped-speaker split, versus 22.5% and 11.8% for audio-only baselines; on the industrial-command corpus it attains 98.6% command accuracy at 1.5% WER.
- Operation-count analysis indicates a 13-fold energy advantage of the spiking formulation over its ANN counterpart at 27.6% mean firing rate; on-board measurements show ~5x lower energy per inference than a Raspberry Pi CPU on the lip-reading model and >100x lower than a laptop GPU, at 14.5 inferences per second.

---

## Title, authors, and funding

**Covers:** Title block, authorship/affiliations, funding acknowledgment

| Field | Value |
|---|---|
| Title | NAVIR: Neuromorphic Audio-Visual Speech Recognition for Robust Human–Robot Interaction on Edge Hardware |
| Authors | Leonidas Delimpasis, Panagiota Moraiti, Antonis Porichis, Panos Chatzakos, Michail Karamousadakis |
| Affiliations | Plaixus Ltd., Athens; Tech Hive Labs, Halandri; AI Innovation Centre, University of Essex |
| Corresponding author | Leonidas Delimpasis (e-mail: leonidasd@disroot.org) |
| Funding | NAVIR project, EU Horizon Europe Research and Innovation Programme (dAIEDGE), Grant Agreement No. 101120726 |
| arXiv ID | arXiv:2609.24391v1 [cs.LG] 21 Sep 2026 |

## Abstract claims (verbatim numbers)

**Covers:** Abstract

- Problem: "Voice-controlled interaction in industrial settings is hampered by acoustic noise, which severely degrades audio-only speech recognition."
- Gap: "state-of-the-art pipelines rely on three-dimensional convolutions, recurrent units, and attention modules that exceed the budget of typical edge devices."
- System: "an end-to-end AVSR system targeting the BrainChip Akida neuromorphic processor, which natively supports only sequential two-dimensional convolutional inference."
- Pipeline: "a per-frame visual encoder, a temporal video encoder, and a spectrogram audio encoder, fused by a lightweight predictor head and decoded by constrained beam search."
- Training: "trained with connectionist temporal classification on noise-augmented audio and then fine-tuned with quantization-aware training."
- GRID results: "the quantized audio-visual model reaches 14.0% word error rate (WER) under noise on the unseen-speaker split and 3.3% WER on the overlapped-speaker split, against 22.5% and 11.8% for audio-only baselines".
- Industrial-command corpus: "98.6% command accuracy at 1.5% WER".
- Energy: "13-fold energy advantage of the spiking formulation over its artificial neural network counterpart at 27.6% mean firing rate"; "roughly 5-fold lower energy per inference than a Raspberry Pi central processing unit on the lip-reading model, and over 100-fold lower than a laptop graphics processing unit, while sustaining 14.5 inferences per second."
- Novelty claim: "To the best of our knowledge, this is the first complete multimodal AVSR pipeline running on neuromorphic hardware of this class."
- Index terms: "Akida, audio-visual speech recognition, BrainChip, edge computing, energy efficiency, human-robot interaction, lip reading, neuromorphic hardware, spiking neural networks."

## I. Introduction — motivation and tension

**Covers:** Section I, Introduction (partial, through the AKD1000 lead-in)

- Speech is "one of the most natural modalities for human-machine interaction," yet industrial deployment is limited because acoustic noise "sharply degrades the performance of audio-only automatic speech recognition (ASR)."
- Fallback to manual interfaces (keypads, touchscreens, physical switches) slows workflows and "can compromise safety in tasks that require both hands free."
- The human perceptual system mitigates this fragility "by integrating the visual appearance of the speaker's mouth, an effect captured most vividly by the McGurk illusion [1]"; AVSR systems "aim to exploit the same redundancy and have been shown to deliver substantial robustness gains at low signal-to-noise ratios."
- Counterpoint: "Modern high-accuracy AVSR pipelines, however, rely on three-dimensional convolutions, attention-based encoders, conformer back-ends or large transformer language models," which "implicitly assume GPU-class hardware and are difficult to deploy on the embedded, battery-powered or thermally constrained platforms found in mobile robotics" — "a tension between recognition performance and deployment feasibility that is central to embedded multimodal speech interfaces."
- Neuromorphic route: "Inspired by biological neural systems, they process sparse, event-driven binary spikes rather than dense floating-point activations, so that energy consumption scales with network activity rather than nominal compute capacity"; the chunk introduces "The BrainChip AKD1000" as "a commercially available neuromorphic system-on-chip that natively executes convolution-" (sentence cut off at chunk boundary).
