# Technical Analysis: wavekat/wavekat-turn

**Repository:** https://github.com/wavekat/wavekat-turn
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Voice pipelines must decide when a user has finished a conversational turn, which is distinct from voice activity detection ("is someone speaking?"). Fixed silence timeouts either cut users off mid-thought or add dead latency before responding. `wavekat-turn` answers "are they done speaking?" (README.md:101-107) as a Rust library wrapping multiple open-source turn-detection models behind common traits, following the pattern of `wavekat-vad` (README.md:16-18). The primary user is a developer building a WaveKat voice pipeline (orchestrated by `wavekat-voice` with VAD/ASR/LLM/TTS) who needs an offline, CPU-efficient end-of-turn signal from either raw audio or ASR text.

## 2. High-Level Architecture

```
Mic / telephony 16 kHz PCM ─► wavekat-vad ─► speech start/end events ─► TurnController ─► LLM trigger
       │                              │                                         ▲
       │                              ▼                                         │
       └──────────────────────► AudioTurnDetector (pipecat / wavekat-smart-turn) │
                                      │                                         │
ASR transcript text ─────────► TextTurnDetector (livekit) ──────────────────────┘
```

Data-flow narrative:

1. Audio frames (16 kHz PCM) stream into an `AudioTurnDetector` backend, or ASR transcript text feeds a `TextTurnDetector` backend (README.md:93-99).
2. `TurnController` wraps any audio detector and accumulates buffer state across frames via `push_audio` (README.md:47-72).
3. VAD speech-start events drive `reset_if_finished()` (soft reset: keeps buffer if the prior turn was unfinished); VAD speech-end events drive `predict()` returning `Finished` / `Unfinished` / `Wait` (README.md:47-72).
4. A `Finished` prediction gates the handoff to the LLM; `Unfinished` keeps listening; `Wait` holds for an AI-initiated pause (README.md:47-55).
5. After the assistant finishes responding, `reset()` performs a hard reset of controller state (README.md:54).
6. Persistent state lives in two places: in-memory detector/controller buffers at runtime, and on disk the HuggingFace model cache under `$HF_HOME/hub/` (default `~/.cache/huggingface/hub/`) or a pre-seeded `$WAVEKAT_TURN_MODEL_DIR` for offline use (README.md:143-147). No database or server-side store is involved.

## 3. The Turn Abstraction

The central concept is the turn prediction: a discrete state over an incremental observation (audio frames or transcript text plus context). Representation is a `TurnPrediction` value carrying a `TurnState` enum.

Named kinds/types (all attested in README excerpts):

- `AudioTurnDetector` — trait over raw audio frames, no ASR required (README.md:93-99), implemented by `audio::PipecatSmartTurn`.
- `TextTurnDetector` — trait over ASR transcript text with optional conversation context, `predict_text(&str, &context)` (README.md:74-84), implemented by `text::LiveKitEou`.
- `TurnController` — orchestration wrapper over any `AudioTurnDetector` with soft-reset semantics (README.md:98-99).
- `TurnState::{Finished, Unfinished, Wait}` — the decision output consumed at VAD speech end (README.md:47-55).
- `SmartTurnVariant::Wavekat(SmartTurnLang::Zh)` vs. embedded upstream Pipecat weights — backend/weight selection within the same ONNX contract (README.md:123-141).
- `SmartTurnLang::Zh` — the only WaveKat fine-tune language shipped in this snapshot; further languages land in the same HF repo (README.md:33-37).

Key queries:

- "Given buffered audio, is the turn complete?" — `ctrl.predict()?` matched on `prediction.state`:
```rust
let prediction = ctrl.predict()?;
match prediction.state {
    TurnState::Finished   => { /* user is done, send to LLM */ }
    TurnState::Unfinished => { /* keep listening */ }
    TurnState::Wait       => { /* user asked AI to hold */ }
}
```
(README.md:47-72.)
- "Given partial transcript plus context, is the utterance complete?" — `detector.predict_text("I was wondering if", &context)?` asserting `TurnState::Unfinished` (README.md:74-84).

## 4. LLM / External Service Integration

The repo calls no LLM and no inference API at runtime; both backends are local ONNX models executed on CPU (~12 ms audio, ~25 ms text) (README.md:29-31). The only network interaction is a one-time model-weight download: under the `wavekat-smart-turn` feature, the first `with_variant(SmartTurnVariant::Wavekat(...))` call fetches the ONNX file from the `wavekat/smart-turn-ONNX` HuggingFace repo and caches it under `$HF_HOME/hub/` (README.md:143-147). Upstream model sources are Pipecat Smart Turn v3 (https://github.com/pipecat-ai/smart-turn, BSD 2-Clause) and LiveKit Turn Detector (https://github.com/livekit/turn-detector, LiveKit Model License) (README.md:29-31). Env vars: `HF_HOME` (cache root, optional), `WAVEKAT_TURN_MODEL_DIR` (offline override directory containing `<lang>/smart-turn-cpu.onnx`, optional). Required calls: none beyond local inference. Optional calls: HF Hub download on first WaveKat-variant construction.

## 5. The Turn-Detection Pipeline

Audio path (primary workflow, via `TurnController` + `AudioTurnDetector`):

1. Construct detector — `PipecatSmartTurn::new()?` (embedded upstream weights, offline) or `PipecatSmartTurn::with_variant(SmartTurnVariant::Wavekat(SmartTurnLang::Zh))?` (HF download then cache) (README.md:123-141).
2. Wrap in orchestration — `TurnController::new(detector)` for automatic state tracking (README.md:47-72).
3. Stream frames — `ctrl.push_audio(&audio_frame)` fed continuously (README.md:47-72).
4. On VAD speech start — `ctrl.reset_if_finished()` soft-resets only if the previous turn completed, preserving a mid-sentence pause buffer (README.md:47-72, README.md:98-99).
5. On VAD speech end — `ctrl.predict()?` and branch on `Finished` (send to LLM) / `Unfinished` (keep listening) / `Wait` (hold) (README.md:47-72).
6. After assistant turn — `ctrl.reset()` hard-resets before the next user turn (README.md:54).

Text path (secondary workflow, via `TextTurnDetector`):

1. Construct detector — `LiveKitEou::new()?` (README.md:74-84).
2. Per transcript update — `detector.predict_text("I was wondering if", &context)?` with conversation context (README.md:74-84).
3. Branch on the same `TurnState` contract (README.md:74-84).

Validation path: `make accuracy` cross-checks audio predictions against the original Python (Pipecat) pipeline on three fixture clips at ±0.02 probability tolerance; `scripts/README.md` documents regenerating the Python reference (README.md:163-169; scripts/README.md:1). A full audio walkthrough lives in `examples/controller.rs` (README.md:86-87; examples/controller.rs:1).

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `README.md` | line refs to ~169 | Canonical spec: backends, traits, quick start, feature flags, sampling constraints, accuracy protocol |
| `examples/controller.rs` | from :1 | End-to-end audio walkthrough with real audio (README.md:86-87; examples/controller.rs:1) |
| `scripts/README.md` | from :1 | How to regenerate the Python reference predictions (README.md:169; scripts/README.md:1) |
| `scripts/gen_reference.py` | referenced via `.gitignore:18` | Generates Python reference / mel tensors (`*.mel.npy`) for accuracy cross-check |
| `Makefile` (`make accuracy`) | referenced README.md:169 | Regenerates/validates ±0.02-tolerance accuracy check on three fixture clips |
| `Cargo.toml` (workspace/crate manifest) | not line-cited in snapshot | Declares features `pipecat`, `wavekat-smart-turn`, `livekit` and `ort`/`ndarray`/`hf-hub` deps (flags README.md:115-117) |
| `src/audio` (`PipecatSmartTurn`, `SmartTurnVariant`, `SmartTurnLang`) | refs README.md:123-141 | Audio backends sharing the Pipecat ONNX contract (README.md:33-37) |
| `src/text` (`LiveKitEou`) | refs README.md:74-84 | Text backend over ASR transcripts |
| `src/controller` (`TurnController`, `TurnState`) | refs README.md:47-72 | Buffer orchestration, soft/hard reset, prediction enum |
| `.gitignore` | 41 | Excludes target, lockfile, tooling, training data/viewer output (`.gitignore:1-41`) |
| `release-plz.toml` | 4 (3 non-blank) | Release automation: git tags + GitHub releases (`release-plz.toml:1-3`) |

Note: the wiki snapshot covers only the files above; internal `src/` layout beyond the named types is not line-cited in the snapshot.

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `ort` | version not recorded in wiki snapshot (required by `pipecat`, `livekit` features) | ONNX Runtime inference for audio and text backends (README.md:90-92) |
| `ndarray` | version not recorded in wiki snapshot (required by `pipecat`, `livekit` features) | Tensor handling for ONNX inputs (README.md:90-92) |
| `hf-hub` | version not recorded in wiki snapshot (required by `wavekat-smart-turn` feature) | Runtime download/cache of WaveKat fine-tune weights (README.md:90-92) |
| `release-plz` (config, not a code dep) | config only, no version pin (`release-plz.toml:1-3`) | Workspace release automation: git tags + GitHub releases |

Required vs. optional: all three Rust crates are optional behind feature flags (`pipecat` off, `wavekat-smart-turn` off implying `pipecat`, `livekit` off; README.md:115-117). Exact constraint strings are absent from the wiki snapshot.

## 8. CLI / Usage Surface

No binary or CLI is documented; the surface is a Rust library plus a `make` validation target. Entry points:

| Entry point | Form | Notes |
|-------------|------|-------|
| `cargo add wavekat-turn --features pipecat` | dependency declaration | Minimal install (README.md:43-45) |
| `examples/controller.rs` | example | Full walkthrough with real audio (README.md:86-87; examples/controller.rs:1) |
| `make accuracy` | validation command | Regenerates ±0.02-tolerance cross-check on three clips (README.md:163-169) |
| `scripts/gen_reference.py` | reference generator | Regenerates Python reference / mel tensors (`.gitignore:18`) |

Feature flags:

| Flag | Default | Effect |
|------|---------|--------|
| `pipecat` | off | Pipecat Smart Turn v3 audio backend; requires `ort`, `ndarray` (README.md:115-117) |
| `wavekat-smart-turn` | off | WaveKat fine-tunes; implies `pipecat`, adds `hf-hub` download (README.md:115-117) |
| `livekit` | off | LiveKit text backend; requires `ort`, `ndarray` (README.md:115-117) |

Env vars and config:

| Variable | Required | Purpose |
|----------|----------|---------|
| `WAVEKAT_TURN_MODEL_DIR` | no | Offline override: directory of `<lang>/smart-turn-cpu.onnx`, skips HF download (README.md:143-147) |
| `HF_HOME` | no | HF cache root (`hub/` subdir), default `~/.cache/huggingface/hub/` (README.md:143-147) |
| `release-plz.toml` (`git_tag_enable`, `git_release_enable`) | n/a (maintainer-side) | Tag + GitHub release on publish (`release-plz.toml:1-3`) |

## 9. Extensibility Points

- New audio backend: implement the `AudioTurnDetector` trait (same contract as `audio::PipecatSmartTurn`) and expose it behind a new feature flag following the `pipecat` pattern (README.md:93-99, README.md:115-117).
- New text backend: implement the `TextTurnDetector` trait (`predict_text` with context) alongside `text::LiveKitEou` (README.md:74-84).
- New language weights: ship additional variants through `SmartTurnVariant::Wavekat(SmartTurnLang::*)` reusing the shared Pipecat ONNX contract (same input shape/tensor names), distributed via the same HF repo; only `Zh` exists today (README.md:33-37).
- Orchestration policy: extend or wrap `TurnController` (soft-reset in `reset_if_finished`, hard `reset`) rather than forking backends (README.md:98-99).
- Validation fixtures: add clips/reference outputs to the `make accuracy` / `scripts/gen_reference.py` flow (README.md:163-169).

## 10. Limitations and Gotchas

- **16 kHz input is mandatory for audio backends.** 8 kHz telephony audio must be upsampled first; Smart Turn v3 silently returns incorrect results at 8 kHz rather than erroring (README.md:153-155).
- **Text-backend accuracy is bounded by ASR quality.** The LiveKit path needs a streaming ASR provider for best results; transcript errors propagate directly into turn decisions (README.md:156-157).
- **Only Mandarin (`zh`) WaveKat fine-tune ships today.** Other languages are promised in the same HF repo but absent, so non-Mandarin specialized use falls back to upstream Pipecat weights (README.md:33-37).
- **Text backend is heavyweight.** The LiveKit ONNX is ~400 MB vs. ~8 MB for either audio backend — a 50x size cost for the transcript path (README.md:29-31).
- **Early-stage API instability.** The API may change between minor versions, so pinned features/versions are advisable for production use (README.md:20-21).
- **Benchmark table is empty in this snapshot.** Accuracy markers at README.md:166-167 carry no numbers; trust requires running `make accuracy` locally (README.md:163-169).

## 11. How It Compares to Alternatives

- **pipecat-ai/smart-turn (upstream Python):** the reference audio implementation this crate ports to Rust/ONNX; use the original for Python/Pipecat pipelines, `wavekat-turn` for embedded Rust inference behind the same ONNX contract (README.md:29-37).
- **livekit/turn-detector (upstream):** the text-based EOU model wrapped as the `livekit` feature; use standalone for LiveKit agents, `wavekat-turn` to combine it with audio backends under one `TurnState` contract (README.md:29-31).
- **wavekat-vad (sibling crate):** answers "is someone speaking?" (frame-level speech detection) whereas `wavekat-turn` answers "are they done speaking?" (turn-level endpointing); pipelines use both, orchestrated by `wavekat-voice` (README.md:101-107).
- **wavekat-voice (orchestrator):** consumes VAD + turn + ASR + LLM + TTS rather than implementing detection itself; `wavekat-turn` is its pluggable turn-decision component (README.md:101-107).

Positioning: `wavekat-turn` is the Rust-native, multi-backend turn-decision layer for WaveKat voice stacks — upstream-compatible weights (Pipecat contract, LiveKit text model) behind unified audio/text traits with `TurnController` orchestration, at the cost of 16 kHz-only audio, ASR-dependent text accuracy, and an early-stage API.

## Appendix: Selected Code Snippets

1. Audio path with `TurnController` (README.md:47-72):

```rust
use wavekat_turn::{TurnController, TurnState};
use wavekat_turn::audio::PipecatSmartTurn;

let detector = PipecatSmartTurn::new()?;
let mut ctrl = TurnController::new(detector);

// Feed audio continuously
ctrl.push_audio(&audio_frame);

// VAD speech start — soft reset (keeps buffer if turn was unfinished)
ctrl.reset_if_finished();

// VAD speech end — predict
let prediction = ctrl.predict()?;
match prediction.state {
    TurnState::Finished   => { /* user is done, send to LLM */ }
    TurnState::Unfinished => { /* keep listening */ }
    TurnState::Wait       => { /* user asked AI to hold */ }
}

// After assistant finishes responding — hard reset
ctrl.reset();
```

2. Text path with `LiveKitEou` (README.md:74-84):

```rust
use wavekat_turn::{TextTurnDetector, TurnState};
use wavekat_turn::text::LiveKitEou;

let mut detector = LiveKitEou::new()?;

let prediction = detector.predict_text("I was wondering if", &context)?;
assert_eq!(prediction.state, TurnState::Unfinished);
```

3. Selecting a Smart Turn variant (README.md:123-141):

```rust
use wavekat_turn::audio::{PipecatSmartTurn, SmartTurnVariant};


# #[cfg(feature = "wavekat-smart-turn")]
use wavekat_turn::audio::SmartTurnLang;

// Embedded upstream weights — works offline, no setup.
let detector = PipecatSmartTurn::new()?;



# #[cfg(feature = "wavekat-smart-turn")]
// WaveKat Mandarin fine-tune — downloaded from HuggingFace on first call,
// then cached under $HF_HOME/hub/.
let detector = PipecatSmartTurn::with_variant(
    SmartTurnVariant::Wavekat(SmartTurnLang::Zh),
)?;
```
