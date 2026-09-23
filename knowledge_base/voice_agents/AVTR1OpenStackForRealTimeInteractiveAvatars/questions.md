---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: AVTR-1: Open Stack for Real-Time Interactive Avatars

### Q1. Why isn't fast motion generation enough for a live avatar conversation, and what are the two latencies that matter?

> [!tip]- Answer
> A live system must also synchronize output with external voice-agent speech (which arrives in irregular fragments, not fixed windows), schedule frames for playback, and handle interruptions — plus generate continuously during silence for reactive listening. The two user-facing latencies are response latency (reply audible) and interruption latency (speech after barge-in). See [[wiki/01-avtr-1-overview-and-introduction|Overview]].

### Q2. What does the motion model predict, and what are its headline configuration numbers?

> [!tip]- Answer
> A 42-dim per-frame vector: axis-angle head rotation plus 39 brow/eye/mouth expression coordinates from LivePortrait's disentangled space, predicted in five-frame chunks by a 153M-parameter pre-norm Transformer decoder (18 layers, 512 wide, 8 heads, RoPE base 10^4) doing conditional flow matching from self (speaking) and other (listening) audio, with 75-frame motion history and 75/5/5 audio steps per stream. See [[wiki/02-motion-representation-and-model-architecture|Motion representation]].

### Q3. How was the 926-hour training corpus built, and what closes the train/inference gap?

> [!tip]- Answer
> 34,219 candidate videos → 1,472 annotated → scene/face filtering (PySceneDetect, YOLO fallback, landmark confidence 0.3) → ClearerVoice audiovisual speaker separation → HuBERT feature caching → LivePortrait motion extraction → finite-difference outlier rejection. Three gap-closers: replacing ground-truth history with model estimates under a rollout curriculum, self-distilling the HuBERT encoder for 525 ms chunks (50%→12% drift), and multi-condition guidance dropout. See [[wiki/03-data-pipeline-and-training-procedure|Data pipeline]] and [[wiki/04-chunk-based-audio-encoder-and-distillation|Audio encoder]].

### Q4. How does the streamer turn irregular speech into a live call, and what delays does it add?

> [!tip]- Answer
> Three worklets (transport/WebRTC, conversation-engine/voice-agent adapter, rendering worklet) over a type-routed event bus share a stream clock that absorbs overruns by shifting the timeline; per-stream schedulers admit segments into gapless 200/205 ms window pairs under four rules (left-pad, fragment-split, right-pad-at-end, one-boundary-per-window). Derived contributions: RLC 305–705 ms, ILC 305–505 ms — confirmed by OpenAI Realtime (390.4/362.7 ms) and Cartesia (454.2/393.3 ms) measurements. See [[wiki/05-streamer-architecture-and-stream-clock|Streamer]] and [[wiki/07-speech-schedulers-and-latency-model|Schedulers]].

### Q5. What rendering performance does the paper report, and on which GPUs is it real-time?

> [!tip]- Answer
> Per five-frame chunk: L40S 71 ms (2.81×, TTFF 42 ms), A100 91 ms (2.20×, 54 ms), RTX 4060 Ti 162 ms (1.24×, 99 ms), RTX 3070 180 ms (1.11×, 94 ms) — real-time; L4 (0.99×), RTX 3060 Ti (0.97×), RTX 4060 (0.86×) fall just short. TensorRT engines, Euler sampling with 4 evaluations, truncation τ = 1.2, per-region CFG, ~0.64 MB session state, lead time Tlead = 100 ms. See [[wiki/06-renderer-and-rendering-worklet|Renderer]].

### Q6. What is R-DGG, how is it validated, and what does it show?

> [!tip]- Answer
> Reference-Based Directed Granger Gain measures the extra predictive information speaker speech adds about listener motion beyond listener history and speaker motion: twin ridge regressions with once-fit reference projections, log error-ratio in nats, K = 100 circular-shift correction, 20k participant bootstraps. Validated by a ground-truth positive control (0.72 [0.32, 1.12] ×10⁻⁴ nats) and two negative controls (talking-head generators, GT×other mismatches — all include zero). All three dyadic systems score above zero (AVTR-1 0.57 [0.19, 0.98], p = 0.002) with overlapping intervals, so no dyadic ranking is supported. See [[wiki/08-evaluation-protocol-and-r-dgg-metric|Protocol]] and [[wiki/09-quantitative-results|Results]].

### Q7. A team wants to put a face on their voice agent using AVTR-1 — what do you recommend?

> [!tip]- Answer
> Recommend it as a complete runnable path (weights + renderer + streamer, real-time on L40S/A100/4060 Ti/3070-class hardware) that consumes the agent's speech and returns synchronized video, budgeting ~300–700 ms of streamer serving delay inside a ~1.8 s end-to-end loop dominated by the voice agent — while flagging the private training data (no retraining/audit), sub-real-time behavior on weaker GPUs, fixed Tlead tuning per deployment, and R-DGG evidence that is corpus-specific. See [[wiki/06-renderer-and-rendering-worklet|Renderer]], [[wiki/07-speech-schedulers-and-latency-model|Schedulers]], and [[wiki/11-appendix-additional-evaluation|Appendix]].
