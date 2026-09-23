> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Chunk-based audio encoder and distillation
**In one sentence:** Because bidirectional HuBERT features drift 30–60% (relative L1) when computed on short windows instead of full audio, AVTR-1 self-distills the frozen-architecture encoder to reproduce its own full-context features from fixed 525 ms chunks (120 ms past / 200 ms present / 205 ms future), cutting the error from ~50% to 12%.
## Key points
- Mismatch: training extracts HuBERT features once on full-length audio, but streaming inference receives audio incrementally; bidirectional attention makes short-chunk features differ sharply from full-context ones.
- Drift quantification: window-only features differ from same-window full-context features by 30–60% relative L1; fidelity plateaus at ~2 s of past audio and collapses below ~400 ms of future audio — but that lookahead exceeds the latency target and 2 s of past audio inflates per-chunk work.
- Chunk design: 525 ms input split into 120 ms past / 200 ms present / 205 ms future (3/5/5 video frames); the extra 5 ms of future audio lets HuBERT's convolutional frontend emit exactly 26 vectors at 50 Hz, downsampled to 13 to match the video frames.
- Self-distillation: no architecture change, no continued self-supervised pretraining (contrast wav2vec-S style adaptation); the student is initialized from the teacher's weights and fine-tuned to match frozen-teacher full-context features with an MSE loss over the N = 13 window frames (Equation 8).
- Result: relative L1 error falls from ~50% to 12% under this window.
- Training: English partition of Multilingual LibriSpeech plus the motion-model dataset; convolutional frontend frozen, projection + Transformer optimized with AdamW (LR 10⁻³, weight decay 10⁻⁴), Noam schedule with 20,000 warm-up steps, bfloat16, batch size 60, ~200 epochs.
- Robustness augmentations: 10% of windows replaced with silence or low-amplitude noise supervised by precomputed full-context silence features; a subset of speech windows gets added low-amplitude Gaussian noise.
---
## Why this matters downstream
The distilled encoder lets the motion model keep its 75-frame audio history conditioning at inference: per chunk the two channels are batched into one encoder call, 5 present + 5 future features are used while 3 past outputs are dropped as already cached, and 75 cached features are prepended (see the renderer page).
**Covers:** the streaming chunk-based HuBERT audio encoder via self-distillation.
