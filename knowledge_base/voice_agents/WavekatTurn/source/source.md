PDF: https://github.com/wavekat/wavekat-turn
# wavekat/wavekat-turn
Source: https://github.com/wavekat/wavekat-turn
Kind: repo
Fetched: 2026-09-22T14:56:01.520477+00:00
Tool: git-clone

# wavekat/wavekat-turn

Commit: 5c1bb3a63ff3f4193145e55a2c7bbb3e01a1a755

## README

<p align="center">
  <a href="https://github.com/wavekat/wavekat-turn">
    <img src="https://github.com/wavekat/wavekat-brand/raw/main/assets/banners/wavekat-turn-narrow.svg" alt="WaveKat Turn">
  </a>
</p>

[![Crates.io](https://img.shields.io/crates/v/wavekat-turn.svg)](https://crates.io/crates/wavekat-turn)
[![docs.rs](https://docs.rs/wavekat-turn/badge.svg)](https://docs.rs/wavekat-turn)

Unified turn detection for [WaveKat](https://wavekat.com) voice pipelines, wrapping multiple open-source
models behind common Rust traits. Same pattern as
[wavekat-vad](https://github.com/wavekat/wavekat-vad).

> [!WARNING]
> Early development. API may change between minor versions.



## Backends

| Backend | Feature flag | Input | Model size | Inference | License |
|---------|-------------|-------|------------|-----------|---------|
| [Pipecat Smart Turn v3](https://github.com/pipecat-ai/smart-turn) | `pipecat` | Audio (16 kHz PCM) | ~8 MB (int8 ONNX) | ~12 ms CPU | BSD 2-Clause |
| WaveKat Smart Turn fine-tunes ([HF](https://huggingface.co/wavekat/smart-turn-ONNX)) | `wavekat-smart-turn` | Audio (16 kHz PCM) | ~8 MB (int8 ONNX) | ~12 ms CPU | BSD 2-Clause |
| [LiveKit Turn Detector](https://github.com/livekit/turn-detector) | `livekit` | Text (ASR transcript) | ~400 MB (ONNX) | ~25 ms CPU | LiveKit Model License |

The WaveKat fine-tunes share the upstream Pipecat ONNX contract (same input
shape, same tensor names) — they're language-specialized weights for the
same architecture. Use them when you want better behavior on a specific
language; today Mandarin (`zh`) is the only one shipped, but more will land
in the same HF repo over time.



## Quick Start

```sh
cargo add wavekat-turn --features pipecat
```

Use `TurnController` to wrap any detector with automatic state tracking:

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

Or the text-based detector directly:

```rust
use wavekat_turn::{TextTurnDetector, TurnState};
use wavekat_turn::text::LiveKitEou;

let mut detector = LiveKitEou::new()?;

let prediction = detector.predict_text("I was wondering if", &context)?;
assert_eq!(prediction.state, TurnState::Unfinished);
```

See [`examples/controller.rs`](crates/wavekat-turn/examples/controller.rs) for a
full walkthrough with real audio.



## Architecture

Two trait families cover the two input modalities:

- **`AudioTurnDetector`** -- operates on raw audio frames (no ASR needed)
- **`TextTurnDetector`** -- operates on ASR transcript text with optional conversation context

`TurnController` wraps any `AudioTurnDetector` and adds orchestration helpers
like soft-reset (preserves buffer when the user pauses mid-sentence).

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

The first call for a WaveKat variant downloads the ONNX from
[`wavekat/smart-turn-ONNX`](https://huggingface.co/wavekat/smart-turn-ONNX)
and caches it under `$HF_HOME/hub/` (default `~/.cache/huggingface/hub/`).
For offline builds, set `WAVEKAT_TURN_MODEL_DIR` to a directory containing
`<lang>/smart-turn-cpu.onnx` to skip the download.



## Important Notes

- **8 kHz telephony audio must be upsampled to 16 kHz** before passing to
  audio-based detectors. Smart Turn v3 silently produces incorrect results
  at 8 kHz.
- Text-based detectors depend on ASR transcript quality. Pair with a
  streaming ASR provider for best results.



## Accuracy

Cross-validated against the original Python (Pipecat) pipeline on three fixture clips.
Tolerance: ±0.02 probability.

<!-- benchmark-table-start -->
<!-- benchmark-table-end -->

Run locally with `make accuracy`. See [`scripts/README.md`](scripts/README.md) for how to regenerate the Python reference.



## About WaveKat

`wavekat-turn` is part of WaveKat, an open-source ecosystem of Rust crates for building real-time voice pipelines. It handles turn detection — deciding when a speaker has finished — alongside sibling crates for voice activity detection, speech-to-text, and text-to-speech.

See [wavekat.com](https://wavekat.com) for the full project.

## Cargo.toml

```
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.package]
version = "0.0.10"
edition = "2021"
license = "Apache-2.0"

```

## Top-level layout

- .github/ (dir, 3 files, ~198 lines)
- .gitignore (~41 lines)
- Cargo.toml (~8 lines)
- crates/ (dir, 16 files, ~2271 lines)
- docs/ (dir, 4 files, ~1020 lines)
- LICENSE (~190 lines)
- Makefile (~66 lines)
- README.md (~171 lines)
- release-plz.toml (~3 lines)
- scripts/ (dir, 2 files, ~233 lines)
- tests/ (dir, 7 files, ~47 lines)
- training/ (dir, 43 files, ~7830 lines)

