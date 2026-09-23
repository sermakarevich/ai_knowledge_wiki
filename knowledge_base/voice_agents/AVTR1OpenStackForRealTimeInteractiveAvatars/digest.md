> [[index|Wiki]] | [[summary|Summary]]

# AVTR-1: Open Stack for Real-Time Interactive Avatars — Digest

## 1. [[wiki/01-avtr-1-overview-and-introduction|AVTR-1 overview and introduction]]
**In one sentence:** AVTR-1 is an open stack for real-time interactive avatar conversations that splits the problem into a 153M-parameter dyadic motion generator (renderer side) and a worklet-based serving backend (streamer side) consuming an external voice agent's speech, because fast inference alone cannot deliver synchronized audio-video, scheduled playback, and interruption handling.
## Key points
- Fast motion generation alone does not make a live conversation: the system must synchronize external voice-agent speech with output, schedule frames, and handle interruptions (response vs. interruption latency).
- Motion generator predicts head/facial motion from both participants' audio; renderer converts motion to video plus session state; streamer drives the renderer loop; the external voice agent owns the dialogue itself.
- 153M-parameter conditional flow-matching Transformer over five-frame chunks (self audio = speaking, other audio = listening); trained on 926 hours of dyadic conversation with history-replacement curriculum; chunk HuBERT via self-distillation.
- Reported dyadic-leading visual quality, lip sync, and listening with real-time GPU inference; R-DGG metric for speech dependence; weights, renderer, and streamer released under component-specific licenses.

## 2. [[wiki/02-motion-representation-and-model-architecture|Motion representation and model architecture]]
**In one sentence:** AVTR-1 generates a 42-dimensional per-frame motion vector (axis-angle head rotation plus 39 brow/eye/mouth expression coordinates from LivePortrait's disentangled space) with a 153M-parameter pre-norm Transformer decoder doing conditional flow matching over five-frame chunks, conditioned via separate near/far motion, dual-audio, and reference paths with an entropy-style audio gate under voice-activity supervision.
## Key points
- 42-dim target: axis-angle rotation plus 39 selected expression coordinates (brow/eyes/mouth), z-scored; scale, translation, keypoints, and 24 remaining coordinates held from the source image at render time.
- Config: 18 layers, 512 wide, 8 heads, RoPE base 10^4, 5-frame chunks, 75-frame motion history, 75/5/5 audio steps per stream at 1024 dims; HuBERT Large (~300M) audio encoder at 50 Hz averaged to 25 fps.
- Per-head QK RMSNorm with learned (1+w) scales, per-head sigmoid output gates (bias 2), AdaLN timestep modulation with zero-init, self-attention restricted to the chunk so cost is history-independent.
- Near/far history + self/other audio cross-attention plus reference MLP fused under a binary availability mask; VAD-supervised audio gate against cross-speaker leakage; four regional output heads enabling per-region classifier-free guidance.

## 3. [[wiki/03-data-pipeline-and-training-procedure|Data pipeline and training procedure]]
**In one sentence:** AVTR-1 trains on 926 retained hours of unscripted dyadic conversation distilled from 34,219 candidate videos through annotation, scene/face filtering, audiovisual speaker separation, and motion-outlier rejection, optimizing a regional flow-matching loss plus smoothness, cosine, and VAD-gate terms under a teacher-forcing rollout curriculum and multi-condition guidance dropout with the Adan optimizer.
## Key points
- 34,219 candidates → 1,472 annotated videos (1,370.13 h) → PySceneDetect + face/YOLO two-person filtering → landmark confidence gating (0.3, ≥5 s) → ClearerVoice audiovisual separation → HuBERT feature caching → LivePortrait motion extraction → finite-difference outlier rejection (0.15 threshold) → 926 retained hours.
- Losses: regional flow-matching MSE + regional cosine direction + third-order smoothness (λexp = 0.1, λrot = λ3D = 100) + BCE audio-gate (λVAD = 0.01); progressive + per-region immiscible noise.
- Rollout curriculum replaces ground-truth history with one-step estimates from the final chunk backward across epochs, with learned timestep embeddings marking estimates; guidance dropout keeps self/other/reference together 45%, drops all 15%, history separately at 75%.
- Adan, 5k-step warm-up to 3×10⁻⁴, 200k-step cosine decay to 10⁻⁵, EMA 0.995 for release; 200k steps on one GH200 in ~35 h (float32 + TF32).

## 4. [[wiki/04-chunk-based-audio-encoder-and-distillation|Chunk-based audio encoder and distillation]]
**In one sentence:** Because bidirectional HuBERT features drift 30–60% (relative L1) when computed on short windows instead of full audio, AVTR-1 self-distills the frozen-architecture encoder to reproduce its own full-context features from fixed 525 ms chunks (120 ms past / 200 ms present / 205 ms future), cutting the error from ~50% to 12%.
## Key points
- Window-only features drift 30–60% from full-context; fidelity needs ~2 s past and ~400 ms future — both unaffordable at inference latency.
- 525 ms chunk (3/5/5 frames) with 5 ms extra future for the convolutional frontend to emit exactly 26 vectors downsampled to 13.
- Student initialized from teacher, MSE match to frozen full-context features over 13 frames; no architecture change, no resumed pretraining.
- Trained on Multilingual LibriSpeech English + motion-model data (AdamW, Noam 20k warm-up, bfloat16, ~200 epochs) with silence-substitution and Gaussian-noise augmentations.

## 5. [[wiki/05-streamer-architecture-and-stream-clock|Streamer architecture and stream clock]]
**In one sentence:** The streamer closes the gap between chunk-based generation and a live video call with three worklets (transport, conversation engine, rendering worklet) communicating only through a type-routed event bus, synchronized to a shared stream clock that absorbs inference overruns by shifting the media timeline instead of skipping or accelerating frames.
## Key points
- Transport (direct WebRTC peer, 25 fps timestamped delivery, clock started on first frame, overruns absorbed as exact-duration pauses), conversation engine (OpenAI Realtime + Cartesia Line adapters, turn/barge-in decisions delegated to the voice agent), rendering worklet (schedulers + renderer loop).
- Speech streams are start-marker/fragment/end-marker segments with real-time in-segment arrival; mic stream segmented by data availability without VAD.
- Clock exposes sleep-until-deadline and overrun measurement; accumulated overruns shift the timeline so precomputed deadlines stay valid.

## 6. [[wiki/06-renderer-and-rendering-worklet|Renderer and rendering worklet]]
**In one sentence:** The renderer turns each five-frame motion request into video with cached LivePortrait appearance (TensorRT engines, Euler flow sampling with noise truncation, per-region classifier-free guidance, ~0.64 MB session state) while the rendering worklet drives it continuously with lead time Tlead = 100 ms, fusing each frame with its 40 ms of avatar speech at the source.
## Key points
- Session init caches source motion/appearance/crop/pasteback; per-request audio bridging keeps a fixed 13-frame encoder window against a 75-frame motion history.
- Progressive noise (α = 2) + truncation (τ = 1.2), Euler ODE with 4 evaluations, past-only-baseline per-region CFG; LivePortrait stitch + warp + decode + pasteback with MODNet matting.
- TensorRT engines (encoder batch-2, split motion encoder/decoder with 4× decoder runs, parallel warp/stitch, serial decode/matte), single CUDA stream, fp16 with fp32 norms.
- Throughput: L40S 2.81× (TTFF 42 ms), A100 2.20× (54 ms), 4060 Ti 1.24× (99 ms), 3070 1.11× (94 ms); L4/3060 Ti/4060 just under 1×.
- Worklet fuses each frame with 40 ms of present-window speech at the source, stamps 40 ms-spaced media times, holds at most one unplayed chunk.

## 7. [[wiki/07-speech-schedulers-and-latency-model|Speech schedulers and latency model]]
**In one sentence:** Each speech scheduler converts irregular gappy speech segments into gapless 200 ms present / 205 ms future window pairs via four admission rules (left-pad, fragment-split, right-pad-at-end, one-boundary-per-window), from which the streamer contributes a response latency of 305–705 ms and an interruption latency of 305–505 ms — both confirmed against OpenAI Realtime and Cartesia Line measurements.
## Key points
- R1 left-pad, R2 fragment-split, R3 right-pad-at-end (all-silence when idle), R4 one-boundary-per-window; blocking (never silence-substitution) on late fragments; interruption discards unadmitted content and reports admitted/discarded amounts for dialogue-state retraction.
- RLC = Tlead + Tpresent + Twait + Tpad ∈ [305, 705) ms; ILC shares the floor with Tpad at its 5 ms floor, below 505 ms; derivation needs real-time arrival, discrete speech markers, and non-blocking iterations.
- Measured: OpenAI RLC 390.4 [315, 491] / ILC 362.7 [310, 409] ms; Cartesia RLC 454.2 [426, 497] / ILC 393.3 [345, 473] ms — all terms in-bounds, additive within 1 ms; agents differ only in deployment-dependent Tpad.
- End-to-end reference (Cartesia): 1757 ms total = 114 inbound + 5 + 1090 voice agent + 5 + 454 streamer + 89 outbound; voice agent dominates, 1500 ms target unreachable without cutting it.

## 8. [[wiki/08-evaluation-protocol-and-r-dgg-metric|Evaluation protocol and R-DGG metric]]
**In one sentence:** On 184 Seamless Interaction speaker–listener pairs (SI-184, 11.90 hours) the paper scores visual quality, lip sync, and conventional listening metrics, then introduces the Reference-Based Directed Granger Gain (R-DGG) — the log-ratio of prediction error with versus without projected speaker speech, shift-corrected and bootstrapped — to test whether listener motion actually depends on the speaker's speech.
## Key points
- SI-184: 184 pairs, 11.90 h at 30 fps; R-DGG scored set 1,457 segments / 177 videos / 3.46 h at 25 fps with strict silence/history/tracking filters; 3 dyadic + 4 talking-head systems; K = 100 shifts.
- Conventional: FID/FVD/CSIM/LSE-D/LSE-C plus rPCC/PFD/SID/Var from EMOCA and LivePortrait features.
- R-DGG: 126-dim motion targets, PCA-reduced speaker motion (32) and HuBERT-L9 speech (64), 25 offsets over 1–100 frames; reference projections fit once on ground truth with identity-disjoint cross-fitting; twin regressions, log error-ratio in nats, circular-shift correction, 20k participant bootstraps.
- Positive control (ground truth above zero) plus two negative controls (talking-head generators, GT×other mismatches include zero) gate interpretability; scores compare only within one corpus.

## 9. [[wiki/09-quantitative-results|Quantitative results]]
**In one sentence:** AVTR-1 leads the compared dyadic systems on visual quality (FID 14.3, FVD 76.8, CSIM 0.94) and most conventional listening metrics while staying competitive on lip sync, and its R-DGG interval sits above zero like the other dyadic systems and ground truth — unlike every talking-head generator — though the dyadic intervals overlap so no ranking among them is supported.
## Key points
- Table 5a: dyadic-best visual quality across the board; lip sync competitive (DyStream leads LSE-D 6.57, AVTR-1 leads dyadic LSE-C 3.28).
- Table 5b: dyadic-best rPCC (0.083/0.140), PFD (25.98/6.417), expression SID/Var.
- Table 6: talking-head generators take both highlighted ranks on every rPCC/PFD component — motion similarity cannot establish speech dependence.
- Table 7: AVTR-1 R-DGG 0.57 [0.19, 0.98] ×10⁻⁴ nats (p = 0.002); validation passes; no reliable dyadic ranking.

## 10. [[wiki/10-references-and-further-reading|References and further reading]]
**In one sentence:** The paper's 39 references span talking-head generators (Ditto, FLOAT, SoulX), dyadic systems (ARIG, AvatarForcing, DyStream), the LivePortrait/flow-matching/HuBERT methodological core, and the latency/benchmark context (Full-Duplex-Bench, Moshi, voice-agent budgets).
## Key points
- Baselines [1–6]; LivePortrait core [7]; generative/stability/guidance methods [8–14, 19–21]; speech/data tooling [15–18, 23–26]; eval/deployment context [27–39]; Adan optimizer [22].

## 11. [[wiki/11-appendix-additional-evaluation|Appendix additional evaluation]]
**In one sentence:** The appendix adds qualitative listening comparisons (Figures 7–8), full SI-184 corpus processing statistics (184 videos → 1,457 scored segments, 3.46 hours), and ablations showing the motion-metric pattern holds across LivePortrait features (Table 8) and full-frame scoring (Tables 9–10).
## Key points
- SI config V00/ipc_conversation/improvised/test; two grounded_gesture videos excluded; 1,284,704 frames → 311,776 scored frames (mean segment 8.6 s).
- LivePortrait-feature and full-frame ablations both preserve the Table 6 pattern — motion similarity is not rescued as a dependence test, which is the gap R-DGG fills.

## The argument in five moves
1. Live avatar conversation needs more than fast inference — continuous synchronized delivery, scheduled playback, and interruption handling — so the stack splits into a dyadic motion generator, a renderer, and a streamer around an external voice agent.
2. Generation stays compact (motion/appearance split, 42-dim targets, history-independent chunk cost) while training closes the train/inference gap three ways: history-replacement curriculum, self-distilled chunk encoder, and guidance dropout.
3. Serving is made analyzable: worklets plus a stream clock plus four-rule schedulers turn irregular speech into gapless windows with derived, bounded latency contributions.
4. Measurement confirms the derivation (both commercial integrations in-bounds and additive; end-to-end budget dominated by the voice agent) and throughput confirms real-time rendering on most tested GPUs.
5. Evaluation pairs conventional metrics (dyadic-leading quality) with R-DGG dependence testing (validated controls; speech dependence for dyadic outputs, none for talking-head or mismatched pairs) — quality and genuine responsiveness, separately evidenced.
