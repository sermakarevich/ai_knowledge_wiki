> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Unified turn detection for WaveKat voice pipelines, wrapping multiple open-source models behind common Rust traits (README.md:16-18).
## Key points
- Wraps multiple open-source turn-detection models behind common Rust traits, following the same pattern as `wavekat-vad` (README.md:16-18).
- Ships three backends: Pipecat Smart Turn v3 audio (~8 MB int8 ONNX, ~12 ms CPU, BSD 2-Clause), WaveKat Smart Turn fine-tunes (same contract, language-specialized), and LiveKit Turn Detector text backend (~400 MB ONNX, ~25 ms CPU) (README.md:29-31).
- WaveKat fine-tunes share the upstream Pipecat ONNX contract (same input shape, same tensor names) with only Mandarin (`zh`) shipped today, more languages landing in the same HF repo over time (README.md:33-37).
- Exposes two trait families by input modality — `AudioTurnDetector` on raw audio frames and `TextTurnDetector` on ASR transcript text — with `TurnController` adding soft-reset orchestration on top of any audio detector (README.md:95-99).
- Positions itself in the pipeline as answering "are they done speaking?" (vs. VAD's "is someone speaking?"), orchestrated with VAD/ASR/LLM/TTS by `wavekat-voice` (README.md:101-107).
- Requires 16 kHz PCM for audio backends — 8 kHz telephony audio must be upsampled because Smart Turn v3 silently produces incorrect results at 8 kHz — while text backends depend on streaming ASR transcript quality (README.md:153-156).
- Validates accuracy cross-checked against the original Python (Pipecat) pipeline on three fixture clips at ±0.02 probability tolerance, regenerable via `make accuracy` (README.md:163-169).
---
## Backends
Three backends behind feature flags (README.md:25-31):

| Backend | Feature flag | Input | Model size | Inference | License |
|---------|-------------|-------|------------|-----------|---------|
| [Pipecat Smart Turn v3](https://github.com/pipecat-ai/smart-turn) | `pipecat` | Audio (16 kHz PCM) | ~8 MB (int8 ONNX) | ~12 ms CPU | BSD 2-Clause |
| WaveKat Smart Turn fine-tunes ([HF](https://huggingface.co/wavekat/smart-turn-ONNX)) | `wavekat-smart-turn` | Audio (16 kHz PCM) | ~8 MB (int8 ONNX) | ~12 ms CPU | BSD 2-Clause |
| [LiveKit Turn Detector](https://github.com/livekit/turn-detector) | `livekit` | Text (ASR transcript) | ~400 MB (ONNX) | ~25 ms CPU | LiveKit Model License |

The WaveKat fine-tunes share the upstream Pipecat ONNX contract (same input shape, same tensor names) — they're language-specialized weights for the same architecture (README.md:33-37).
## Quick Start
Add with a backend feature (README.md:43-45):

```sh
cargo add wavekat-turn --features pipecat
```

Wrap any detector with `TurnController` for automatic state tracking (README.md:47-72):

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

Or use the text-based detector directly (README.md:74-84):

```rust
use wavekat_turn::{TextTurnDetector, TurnState};
use wavekat_turn::text::LiveKitEou;

let mut detector = LiveKitEou::new()?;

let prediction = detector.predict_text("I was wondering if", &context)?;
assert_eq!(prediction.state, TurnState::Unfinished);
```

Full walkthrough with real audio in `examples/controller.rs` (README.md:86-87; examples/controller.rs:1).
## Architecture
Two trait families cover the two input modalities (README.md:93-99):

- **`AudioTurnDetector`** -- operates on raw audio frames (no ASR needed)
- **`TextTurnDetector`** -- operates on ASR transcript text with optional conversation context

`TurnController` wraps any `AudioTurnDetector` and adds orchestration helpers like soft-reset (preserves buffer when the user pauses mid-sentence) (README.md:98-99).

Pipeline role (README.md:101-107):

```
wavekat-vad   -->  "is someone speaking?"
wavekat-turn  -->  "are they done speaking?"
     |                   |
     v                   v
wavekat-voice -->  orchestrates VAD + turn + ASR + LLM + TTS
```
## Feature Flags
| Flag | Default | Description |
|------|---------|-------------|
| `pipecat` | off | Pipecat Smart Turn v3 audio backend (requires `ort`, `ndarray`) |
| `wavekat-smart-turn` | off | WaveKat language-specialized fine-tunes; implies `pipecat`, adds `hf-hub` runtime download |
| `livekit` | off | LiveKit text-based backend (requires `ort`, `ndarray`) |

(Rows verbatim README.md:115-117.)
### Selecting a Smart Turn variant
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
(README.md:123-141.) First call downloads the ONNX from `wavekat/smart-turn-ONNX` and caches it under `$HF_HOME/hub/` (default `~/.cache/huggingface/hub/`); for offline builds set `WAVEKAT_TURN_MODEL_DIR` to a directory containing `<lang>/smart-turn-cpu.onnx` to skip the download (README.md:143-147).
## Important Notes
- **8 kHz telephony audio must be upsampled to 16 kHz** before passing to audio-based detectors. Smart Turn v3 silently produces incorrect results at 8 kHz (README.md:153-155).
- Text-based detectors depend on ASR transcript quality. Pair with a streaming ASR provider for best results (README.md:156-157).
- Early development: API may change between minor versions (README.md:20-21).
## Accuracy
Cross-validated against the original Python (Pipecat) pipeline on three fixture clips. Tolerance: ±0.02 probability (README.md:163-164). Benchmark table markers are empty in this snapshot (README.md:166-167). Regenerate with `make accuracy`; see `scripts/README.md` for how to regenerate the Python reference (README.md:169; scripts/README.md:1).
**Covers:** README.md, examples/controller.rs, scripts/README.md
