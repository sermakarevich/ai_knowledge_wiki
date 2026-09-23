---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Voice-Light: A Full-Duplex Cascaded Voice Agent with Causal Turn-Taking and Speculative Generation

### Q1. What is Voice-Light's central design rule, and what does full duplex mean in this system?
> [!tip]- Answer
> The central rule is that uncertain work may begin early but may become audible or durable only after explicit causal checks, with conversation history containing only speech acknowledged by the listener's browser. Full duplex means microphone ingestion continues during assistant playback, playback reacts reversibly to detected user speech, and generation, synthesis, and acknowledged audio are managed concurrently, while the cascaded ASR → LLM → TTS boundaries expose typed tools, playback state, and cancellation. See [[wiki/01-full-duplex-cascaded-voice-agent|Voice-Light: A Full-Duplex Cascaded Voice Agent]].

### Q2. What three research questions does the paper ask, and what does it explicitly not claim?
> [!tip]- Answer
> It asks whether a small causal adapter reusing a persistent streaming ASR encoder can improve turn commitment over deployable timing baselines, whether a reversible controller can exploit uncertain evidence without canceling on every VAD onset, and how much response latency private speculation can hide in the cascade. The contributions are framed as systems and evaluation contributions only: no new state-of-the-art adapter, no general tool competence from synthetic evaluation, and no population-level interaction quality estimates from the microphone sessions. See [[wiki/01-full-duplex-cascaded-voice-agent|Voice-Light: A Full-Duplex Cascaded Voice Agent]].

### Q3. What is the acknowledged-audio durability rule, and how are speculation and latency scoped?
> [!tip]- Answer
> Generated assistant text becomes durable conversation context only to the extent that browser acknowledgments show it was audible, with the browser streaming 16 kHz microphone PCM over one WebSocket and acknowledging rendered audio ranges. Speculation means privately preparing downstream text and PCM before a final turn commitment, and the latency results are system measurements not directly comparable with model-internal latency reported for end-to-end architectures. See [[wiki/02-acknowledged-audio-latency-results|Acknowledged Audio and Latency Results]].

### Q4. What does the synthetic spoken-tool corpus contain, and what does its holdout actually measure?
> [!tip]- Answer
> A pinned Qwen3.6-27B-FP8 teacher generated provider-neutral records yielding 3,999 conversations, 11,810 user messages, 15,308 assistant messages, and 3,498 structured calls across search, calculate, and get time, with deterministic calculator/time results and teacher-written (not live-web) search results. The branch targets a narrow spoken protocol — short audible bridges, causally ordered call/result records, sequential calls, suppression of protocol markup — so its shared-generator holdout measures acquisition of that protocol, not general tool use or factual retrieval. See [[wiki/02-acknowledged-audio-latency-results|Acknowledged Audio and Latency Results]].

### Q5. How are synthetic turn-taking timelines rendered, and what are the V4/V5 manifest counts?
> [!tip]- Answer
> Each user unit is rendered and trimmed independently with Qwen VoiceDesign references conditioning CosyVoice 3 zero-shot voices, measured for active speech, assembled into a timeline, and rasterized as 20-second views into 250 frames at 80 ms. A planned pause becomes HOLD supervision only if the rendered unit contains at least 500 ms of silence followed by resumed speech, and the retained V4 and V5 manifests hold 1,092 timelines / 21.84h and 1,097 timelines / 21.80h of source timeline; the public repository stores lossless speech units plus reconstruction metadata rather than every composed waveform. See [[wiki/03-synthetic-data-turn-taking-corpora|Synthetic Data and Turn-Taking Corpora]].

### Q6. What is in the locked human corpus, and what are the two trained adapters?
> [!tip]- Answer
> The locked manifest records 107 accepted conversations totaling 36.30 hours (MagicHub 8 / 2.77h, TurnBench 37 / 7.31h, additional authorized material 62 / 26.22h) across conversation-disjoint splits, stored as lossless FLAC plus Parquet 20-second windows after excluding one silent TurnBench recording. The tool experiment fine-tuned Qwen3-1.7B with a BF16 rank-16 LoRA (17.43M parameters, 904 steps, 47 min on an RTX 4090), while the turn model attaches ~183k trainable parameters to the frozen Nemotron Streaming 0.6B encoder via layers 6/12/18/24 taps, causal depthwise-separable convolutions, and a single-layer 64-dim unidirectional GRU. See [[wiki/03-synthetic-data-turn-taking-corpora|Synthetic Data and Turn-Taking Corpora]].

### Q7. How was the deployed step-750 adapter selected, and what transfer gap did tuning expose?
> [!tip]- Answer
> Tuning warm-started prior weights with a fresh optimizer, 15% synthetic replay, and 1,884 human boundaries (1,038 HOLD, 846 EOT), selecting the 750-step checkpoint on human validation because synthetic validation could not select it; assistant-token validation loss bottomed after pass 4 then rose even as free-generation protocol metrics improved. Completion AUROC was 0.9260 on 893 held-out synthetic examples but only 0.5646 on 789 clean human labels (0.5972 after fine-tuning), with step 750 reaching 65.04% EOT recall, 3.73% false cutoffs, and 2.0 s p95 commitment latency on validation — validation results, not locked-test results. See [[wiki/04-model-adaptation-validation-loss|Model Adaptation and Validation-Loss Tuning]].

### Q8. What was the locked V1 test outcome, and why are detectors compared at native gates?
> [!tip]- Answer
> On 1,673 causal silence candidates from 11 conversations (only 37 HOLD), historical step 3,500 at threshold 0.90 / 560 ms minimum delay / 800 ms timeout kept a 2.70% false-cutoff rate but reached only 12.53% EOT recall with 770 ms mean latency, crossing its learned threshold on just 205 of 1,636 EOT cases so most turns fell back to timeout — versus 95.60% recall for Silero and 91.50% for LiveKit at the same cutoff rate. Detectors emit boundary evidence on different cadences (Voice-Light 80 ms, Smart Turn 240 ms, LiveKit 320 ms, Silero 32 ms chunks), so comparisons evaluate complete causal policies at native gates rather than isolating model quality under identical acoustic evidence. See [[wiki/05-turn-completion-evaluation|Turn-Completion Evaluation — The Detectors Do Not Score]].

### Q9. What did the three-session microphone case study measure, and what limits its interpretation?
> [!tip]- Answer
> Across 36 measured response turns by one operator against a scale-to-zero Modal service (cold start excluded), median final-VAD-to-first-server-audio latency was 758 ms (mean 932 ms, range 528–1,652 ms) with 21/36 turns below 800 ms; component medians in the 13-turn traced subset overlap and must not be added. Nine traced turns promoting speculative work showed 667 ms median versus 1,513 ms for four without promotion, but this is an observational split confounded with transcript stability and turn difficulty, not a causal 846 ms speedup; the 250–600 ms target was not met consistently and the 800 ms line is a development reference, not a population target. See [[wiki/06-streaming-controller-deployment|5 Snapshots Failed for the Multi-Process — End-to-End Latency Case Study]].

### Q10. (Evaluation) Should a team ship the learned completion policy as a replacement for the hybrid timing controller, and what evidence would change your recommendation?
> [!tip]- Answer
> No — keep the hybrid controller with the adapter as an optional signal, because the historical learned policy failed the locked real-conversation gate (12.53% EOT recall at matched 2.70% false cutoffs) and the deployed step-750 adapter was never evaluated on that locked test, while the latency case study is three unscripted sessions from one operator, not a user study. I would switch only on a stronger evaluation: conversation-disjoint human labels with participant-level intervals, controlled overlap scenarios, final-topology action latencies, and a learned policy that improves the latency-versus-false-cancel frontier — the paper's own stated replacement criterion. See [[wiki/07-discussion-limitations|Discussion and Limitations: The Negative Result]].
