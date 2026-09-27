> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: wavekat/wavekat-turn

## Claims vs. evidence

- Claim: one crate unifies turn detection behind common Rust traits, following the `wavekat-vad` pattern, so backends stay swappable (README.md:16-18). Evidence: moderate — two trait families plus a backend-agnostic `TurnController` are precisely described, but no multi-backend swap example is cited.
- Claim: three backends cover audio and text — Pipecat Smart Turn v3 (~8 MB int8 ONNX, ~12 ms CPU, BSD 2-Clause), WaveKat fine-tunes (same contract), LiveKit text (~400 MB ONNX, ~25 ms CPU) (README.md:29-31). Evidence: moderate — sizes, latencies, licenses are concrete, but lack hardware, batching, and tail-latency context.
- Claim: WaveKat fine-tunes are drop-in, language-specialized weights sharing the upstream Pipecat ONNX contract, with more languages landing in the same HF repo (README.md:33-37). Evidence: weak — only Mandarin (`zh`) ships today, with no per-language accuracy deltas cited.
- Claim: the crate answers "are they done speaking?" above VAD's "is someone speaking?", orchestrated with VAD/ASR/LLM/TTS by `wavekat-voice` (README.md:101-107). Evidence: moderate — role and Finished/Unfinished/Wait tri-state with soft vs. hard reset are clearly specified, but no pause-heavy or interruption results are cited.
- Claim: correctness is enforced by input discipline plus cross-validation against the Python reference on three fixture clips at ±0.02 tolerance via `make accuracy` (README.md:163-169). Evidence: partial — the parity harness is concrete, but three clips prove port fidelity, not turn-taking quality, and benchmark markers are empty (README.md:166-167).

## Genuinely new vs. repackaged

- Genuinely new: the Rust-side packaging — one crate, two trait families split by modality (raw audio frames vs. ASR transcript text), plus `TurnController` semantics (soft `reset_if_finished()` on VAD speech start vs. hard `reset()` after the assistant responds). Pause-vs-finished handling is the real design contribution.
- Repackaged: the models themselves — Pipecat Smart Turn v3 weights and the LiveKit Turn Detector are wrapped, not invented; WaveKat fine-tunes reuse the upstream ONNX contract (same shapes, same tensor names).
- Borrowed pattern: the "same pattern as `wavekat-vad`" framing is explicit, so the novelty is consistency across the WaveKat voice stack, not a new detection algorithm.
- Net: integration and ergonomics innovation, not modeling innovation. Value stands or falls on trait stability and controller correctness.
- Honest signals: the repo warns "early development: API may change" (README.md:20-21) and credits upstream Pipecat/LiveKit rather than inflating originality — a point for trust.
- Verification posture is a plus: a worked `examples/controller.rs` walkthrough and a scripts README for regenerating the Python reference lower the cost of independent checking.
- Open question the digest cannot answer: whether the shared ONNX contract survives future upstream architecture changes, which would break the drop-in fine-tune story.
- Release hygiene note: the root enables tag-plus-release automation (`release-plz.toml`) while ignoring `Cargo.lock`, so downstream pins must live in the consuming workspace, not upstream.

## Weaknesses and blind spots

- Thin validation: three clips at ±0.02 match the Python reference, with empty benchmark markers — no precision/recall, no interruption or overlap metrics, no noise/accent breakdown.
- Early-development churn risk is stated openly (README.md:20-21); the "no backend-specific code" pitch still warrants isolating backend paths until traits stabilize.
- Single shipped fine-tune (Mandarin only) with "more landing over time" as promise: multilingual coverage is aspirational today.
- Heavyweight text path: ~400 MB ONNX under the LiveKit Model License vs. ~8 MB BSD audio weights — very different cost and licensing profiles behind one "unified" label.
- Sharp documented edges: 8 kHz telephony silently corrupts Smart Turn v3 output unless upsampled (README.md:153-155); text-path accuracy inherits all ASR errors and needs streaming ASR (README.md:156-157).
- Runtime-download coupling for WaveKat variants (HuggingFace on first call, cached under `$HF_HOME/hub/`) raises cold-start and hermetic-build concerns, only partly mitigated by `WAVEKAT_TURN_MODEL_DIR`.
- Dependency surface per backend (`ort`, `ndarray`, plus `hf-hub` for WaveKat variants) grows build weight well beyond the ~8 MB figure; flags default off, so every adopter pays explicitly.
- Missing from the digest: `Wait`-state calibration, VAD-boundary sensitivity, concurrency/thread-safety story, and error handling around ONNX/`ort` failures.

## Applicability

- Direct fit: Rust real-time voice pipelines that already separate VAD ("is someone speaking?") from turn detection ("are they done?") and want a swappable audio-first end-of-turn signal without mandatory ASR in the loop.
- Conditional fit: transcript-aware pipelines with streaming ASR that can absorb a 400 MB model and the LiveKit license — otherwise the text backend is hard to justify.
- Poor fit: 8 kHz telephony without a resampling stage, offline/air-gapped builds unwilling to vendor weights, or teams needing stable APIs and multilingual coverage today.
- Suggested trial harness: run `examples/controller.rs` on your own pause-heavy and interruption clips, log Finished/Unfinished/Wait at each VAD boundary, and compare against human labels before wiring LLM dispatch.

- **Relevance to my work**
  - AI/ML engineering: cheap (~8 MB, ~12 ms-class) BSD-licensed audio EOU with a Python-parity check (`make accuracy`); standardize the 16 kHz upsample discipline and vendor weights for hermetic builds before adopting.
  - Agentic systems: the Finished/Unfinished/Wait tri-state maps onto barge-in, hold-vs-respond, and LLM-dispatch gating; prototype `TurnController` soft/hard reset semantics against interruption-heavy speech first.
  - Elisity data platform: turn-boundary events are natural segmentation points for conversation logging, transcript chunking, and evaluation slices — but only if boundary quality is measured (precision/recall on pauses and interruptions), not assumed from ±0.02 port parity.

## What this changes

- Little for modeling: no new turn-detection science is claimed or evidenced.
- Something for Rust voice stacks: a credible small-footprint convention (traits + controller + feature flags + offline weights) reducing glue code between VAD, turn detection, and the `wavekat-voice` orchestrator.
- Process change if adopted: treat audio as default, gate the text path on license/size review, and add boundary-quality metrics plus 8 kHz resampling tests to CI rather than relying on the three-clip parity check.
- Non-change worth stating: VAD selection and ASR quality still dominate perceived turn-taking; this crate refines the decision layer without fixing upstream signal problems.

## Verdict

- Audio backend: promising enough to prototype — small, BSD-licensed, offline-capable, with a sensible orchestration abstraction.
- Text backend: defer pending license review and evidence it beats the audio path on your ASR setup given its ~400 MB weight.
- Ecosystem bet: premature to standardize on until the API stabilizes and more than Mandarin ships with measured gains.
- Revisit triggers: a second shipped fine-tune with per-language gains, turn-boundary precision/recall on noisy pause-heavy speech, or a stabilized API with changelog discipline.
- Skip conditions: if the LiveKit Model License is a non-starter, or 8 kHz telephony without resampling is a hard constraint.
- Bottom line: prototype the audio path behind a version pin, measure turn-boundary quality on your own clips, and revisit in one quarter — **trial**.
