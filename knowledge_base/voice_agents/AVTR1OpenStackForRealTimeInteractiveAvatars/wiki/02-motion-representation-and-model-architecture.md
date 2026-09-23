> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Motion representation and model architecture
**In one sentence:** AVTR-1 generates a 42-dimensional per-frame motion vector (axis-angle head rotation plus 39 brow/eye/mouth expression coordinates from LivePortrait's disentangled space) with a 153M-parameter pre-norm Transformer decoder doing conditional flow matching over five-frame chunks, conditioned via separate near/far motion, dual-audio, and reference paths with an entropy-style audio gate under voice-activity supervision.
## Key points
- Per-frame target is a 42-dimensional vector: axis-angle rotation vector r plus 39 expression coordinates selected from LivePortrait's 63 (brow, eyes, mouth), z-score normalized with dataset-global statistics; scale, translation, canonical keypoints, and 24 remaining coordinates are excluded and taken from the source image at render time.
- Representation comes from LivePortrait's motion–appearance disentangled space (canonical keypoints xc, pose R, expression δ, scale s, translation t with xd = s(xc R + δ) + t); deformations are moved into the head frame (δ̃ = δRT) before selection; training targets use the motion extractor alone.
- Static reference condition: training concatenates per-track medians of rotation, all 63 canonical keypoint coordinates, and all 63 expression coordinates (129 dimensions); inference builds it from the source image; it enters via an MLP, not attention.
- Model config (Table 1): 153M parameters, 18 decoder layers, width 512, 8 heads / 64 dim, feed-forward 512, 2 audio-condition encoder layers per stream, dropout 0, RoPE base 10^4, 5-frame generated chunk, 75-frame past motion context, 75/5/5 past/present/future audio steps per stream at 1024 dim.
- Transformer block: three residual sub-blocks (self-attention restricted to the five-frame chunk, conditioning block, feed-forward); flow-matching timestep modulates each via AdaLN with zero-initialized projections; past-motion/audio routed through the conditioning block so per-chunk cost is independent of generated length.
- Stability details: per-head RMSNorm on queries and keys with learned (1+w) scale vectors (unit gain init, decay toward one), per-head learned sigmoid output gates (zero weights, bias 2, following Qiu et al. against attention sinks), independent position construction per query/key sequence under one RoPE config.
- Conditioning: 75-frame history split into near (last 5) and far (earlier 70) cross-attention paths plus self/other audio cross-attention plus reference MLP, fused as a masked residual with a binary availability vector b = (bpast, bself, bother, bref); near/far share bpast so guidance treats past motion as one condition.
- Audio gate: channel-wise weights predicted jointly from both streams (Gated Multimodal Unit style) but applied separately; channel-averaged logits supervised with pseudo-VAD targets (1 = self active, 0 = other active) to suppress cross-speaker leakage from imperfect separation.
- Regional output heads: four linear projections (rotation, brow, eyes, mouth) per 512-dim token enable per-region classifier-free guidance; RMS normalization across frames/channels, then four linear maps to motion coordinates, concatenated to the 42-dim velocity prediction.
---
## Motion parameters (Section 2.1)
LivePortrait's decomposition and the reduced 42-dim target are given above; the appearance extractor's volumetric feature is render-time only and never a training target.

## Audio encoder
24-layer pre-trained HuBERT Large (~300M parameters), 1024-dim features at 50 Hz, adjacent pairs averaged to the 25 fps motion rate; both audio channels encoded separately.

## Conditioning equation
The layer-wise conditioning residual combines the four cross-attention outputs and reference MLP output under the availability mask (Equation 3 in the paper).
**Covers:** the LivePortrait motion representation and the flow-matching Transformer architecture.
