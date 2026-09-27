---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: wavekat/wavekat-turn

### Q1. What pipeline question does wavekat-turn answer, and how does that differ from wavekat-vad's role?
> [!tip]- Answer
> wavekat-turn answers "are they done speaking?" while wavekat-vad answers "is someone speaking?", and the two are orchestrated with ASR/LLM/TTS by `wavekat-voice`. It wraps multiple open-source turn-detection models behind common Rust traits, following the same pattern as `wavekat-vad`. See [[wiki/01-overview|Overview]].

### Q2. Name the three backends wavekat-turn ships, with their input modality, model size, and inference latency.
> [!tip]- Answer
> Pipecat Smart Turn v3 takes audio (16 kHz PCM) at ~8 MB int8 ONNX and ~12 ms CPU; WaveKat Smart Turn fine-tunes use the same audio contract with language-specialized weights; and the LiveKit Turn Detector takes text (ASR transcript) at ~400 MB ONNX and ~25 ms CPU. Only Mandarin (`zh`) is shipped among the WaveKat fine-tunes today, with more languages landing in the same HF repo. See [[wiki/01-overview|Overview]].

### Q3. What are the two detector trait families, and what orchestration does TurnController add on top of an audio detector?
> [!tip]- Answer
> `AudioTurnDetector` operates on raw audio frames with no ASR needed, while `TextTurnDetector` operates on ASR transcript text with optional conversation context. `TurnController` wraps any audio detector and adds soft reset on VAD speech start (preserving the buffer when the user pauses mid-sentence) plus hard reset after the assistant responds, with predictions in `Finished`, `Unfinished`, or `Wait` states. See [[wiki/01-overview|Overview]].

### Q4. What are the three feature flags, and how do you select the Mandarin fine-tune or run fully offline?
> [!tip]- Answer
> The flags are `pipecat` (upstream audio backend), `wavekat-smart-turn` (language fine-tunes; implies `pipecat` and adds `hf-hub` runtime download), and `livekit` (text backend), all off by default. The Mandarin fine-tune is selected via `SmartTurnVariant::Wavekat(SmartTurnLang::Zh)`, which downloads from `wavekat/smart-turn-ONNX` into `$HF_HOME/hub/` on first call. For offline builds set `WAVEKAT_TURN_MODEL_DIR` to a directory containing `<lang>/smart-turn-cpu.onnx` to skip the download. See [[wiki/01-overview|Overview]].

### Q5. What input discipline do the audio backends require, and how is accuracy validated against the Python reference?
> [!tip]- Answer
> Audio backends require 16 kHz PCM: 8 kHz telephony audio must be upsampled because Smart Turn v3 silently produces incorrect results at 8 kHz, while text backends depend on streaming ASR transcript quality. Accuracy is cross-checked against the original Python (Pipecat) pipeline on three fixture clips at ±0.02 probability tolerance, regenerable via `make accuracy`. See [[wiki/01-overview|Overview]].

### Q6. What does the repository root exclude from version control, and what release automation does it enable?
> [!tip]- Answer
> The root excludes Rust build output (`/target`, `Cargo.lock`), editor/OS state, Python tooling outputs, generated `*.mel.npy` tensors (regenerable via `scripts/gen_reference.py`), and training working state including data, PDF refs, and viewer builds. Release automation in `release-plz.toml` sets `git_tag_enable = true` and `git_release_enable = true` under `[workspace]`, so releases create git tags and GitHub releases. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. You are building an offline English-language kiosk with no streaming ASR and tight CPU budget — which backend should you choose, and why?
> [!tip]- Answer
> Choose the embedded Pipecat Smart Turn v3 audio backend, since it works offline with no setup, needs no ASR transcripts, and costs only ~8 MB and ~12 ms CPU versus the ~400 MB LiveKit text model. Avoid the LiveKit backend (it needs streaming ASR quality you do not have) and the WaveKat fine-tunes (only Mandarin is shipped, so English gains nothing). See [[wiki/01-overview|Overview]].
