---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: soniqo/speech-core

### Q1. What is soniqo/speech-core and what is its local-first promise?
> [!tip]- Answer
> It is on-device C++17 speech infrastructure for Linux, Windows, and Android covering VAD, batch and streaming STT, diarization, TTS, and the voice-agent pipeline connecting them. It runs locally on CPU with no cloud, no Python at inference, and no audio leaving the machine, with a full offline Android voice-agent demo fitting in 1.2 GB. See [[wiki/01-overview|Overview]].

### Q2. How does speech-core deliver live-agent behavior and real streaming ASR?
> [!tip]- Answer
> The core provides VAD-driven turns, eager STT, partial transcripts, barge-in, streaming TTS, and tool calling as native pipeline behavior. Streaming ASR uses cache-aware RNN-T decoders with end-of-utterance detection, beam search, and contextual phrase biasing. See [[wiki/01-overview|Overview]].

### Q3. Which models and backends does speech-core support, and on which platforms?
> [!tip]- Answer
> Supported models span Silero VAD v5, Smart Turn, Parakeet TDT v3, Whisper, Canary, Nemotron streaming variants, diarization and embedding models, and TTS voices including VoxCPM, Kokoro, Pocket TTS, plus DeepFilterNet3 and echo-cancellation models. Backends are core-only, ONNX Runtime, LiteRT, and LiteRT-LM across Linux, Windows, macOS, and Android, with ONNX using CPU/NNAPI/QNN hooks and LiteRT on CPU. See [[wiki/01-overview|Overview]].

### Q4. How do you build speech-core and wire the VoicePipeline, and how are Linux CLI packages used?
> [!tip]- Answer
> Build the core plus LiteRT backend via `scripts/fetch_litert.sh` followed by `cmake -B build` with `SPEECH_CORE_WITH_LITERT=ON` and `LITERT_DIR`, then transcribe with `LiteRTParakeetStt::transcribe` or connect VAD/STT/LLM/TTS implementations to `VoicePipeline::start` and `push_audio`. Releases ship amd64/arm64 `.deb` and `.tar.gz` packages bundling runtime libraries but not models, driven by commands like `speech download-models`, `speech transcribe`, `speech speak`, and `speech serve`. See [[wiki/01-overview|Overview]].

### Q5. How does the CMake build split the core from optional backends, and which guards fail fast?
> [!tip]- Answer
> Three static-library targets split the build: always-built `speech_core`, ONNX-gated `speech_core_models`, and LiteRT-gated `speech_core_models_litert`, with options for tests, LiteRT-LM, HF downloads, examples, HTTP server, Ollama, and packaging. Incompatible combos fail fast with `FATAL_ERROR`: `SPEECH_CORE_WITH_HF_DOWNLOAD` requires `SPEECH_CORE_WITH_LITERT`, and `SPEECH_CORE_BUILD_HTTP_SERVER` requires `SPEECH_CORE_WITH_ONNX`. See [[wiki/02-top-level-files|Top-level files]].

### Q6. What do the agent contract, version-control hygiene, and third-party notices define?
> [!tip]- Answer
> The identical `AGENTS.md`/`CLAUDE.md`/`CODEX.md` files define a pure-C++17 zero-ML-dependency orchestration core with abstract VAD/STT/TTS/LLM/enhancer/diarizer interfaces, optional ONNX and LiteRT reference implementations, nine named `test_*` executables, and branch/PR/release conventions. Shell scripts are pinned to LF endings and fetched model/runtime dirs stay out of git, while binary releases bundle ONNX Runtime (MIT) and `libLiteRt.so` (Apache-2.0) but never ship ML models. See [[wiki/02-top-level-files|Top-level files]].

### Q7. Would you recommend speech-core for a fully offline on-device voice agent, and why?
> [!tip]- Answer
> Yes, conditionally: the local-first C++17 core, model-agnostic orchestration with swappable ONNX/LiteRT backends, built-in barge-in and streaming pipeline, and packaged Linux/Windows/Android targets fit offline deployment well. Caveats are confirming the needed STT/TTS models exist for the target backend and language, and validating CPU latency on the actual device. Pilot the 1.2 GB Android-style offline demo plus the core `ctest` suite before committing. See [[wiki/01-overview|Overview]].
