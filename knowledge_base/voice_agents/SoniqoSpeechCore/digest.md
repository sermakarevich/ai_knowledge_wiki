> [[index|Wiki]] | [[summary|Summary]]
# soniqo/speech-core — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** speech-core is on-device C++17 speech infrastructure for Linux, Windows, and Android covering VAD, batch and streaming STT, diarization, TTS, and the voice-agent pipeline that connects them (README.md:15).
- speech-core runs locally on CPU with no cloud, no Python at inference, and no audio leaving the machine (README.md:17).
- The core is a small model-agnostic orchestration layer owning turn detection, interruption handling, audio utilities, conversation state, and tool calls, while the application chooses the models (README.md:34).
- Live-agent behavior is built in: VAD-driven turns, eager STT, partial transcripts, barge-in, streaming TTS, and tool calling (README.md:37).
- Streaming ASR uses cache-aware RNN-T decoders with end-of-utterance detection, beam search, and contextual phrase biasing (README.md:38).
- Backend choice is a construction and link decision: ONNX Runtime, LiteRT, both, neither, or custom implementations of the abstract interfaces, and the orchestration target never depends on a concrete model (README.md:39, README.md:193).
- The portable surface is a native C++ API plus C APIs suitable for Kotlin/JNI, Swift/FFI, embedded Linux, and other hosts (README.md:40).
- Targets covered are Linux, Windows, macOS, Android-oriented arm64 builds, plus sanitizers and model-backed nightly lanes (README.md:41).
- Releases ship Linux `.deb`/`.tar.gz` packages for amd64 and arm64 that bundle runtime libraries but not models (README.md:149).

## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** The repo root defines the build, contributor contract, multilingual front door, and license notices for the C++17 voice-agent engine and its optional ONNX/LiteRT backends.
- The root is a C++17 voice-agent pipeline engine whose core (state machine, turn detection, interruption, speech queue, context, streaming VAD, audio utils) has zero ML dependencies (`AGENTS.md:5-7`).
- Three static-library targets split the build: always-built `speech_core`, ONNX-gated `speech_core_models`, LiteRT-gated `speech_core_models_litert` (`AGENTS.md:65-67`; `CMakeLists.txt:9-12`).
- `CMakeLists.txt:1-18` pins `cmake_minimum_required(VERSION 3.16)`, `project(speech_core VERSION 0.1.0 LANGUAGES CXX)`, C++17, and options including `SPEECH_CORE_WITH_ONNX`, `SPEECH_CORE_WITH_LITERT`, `SPEECH_CORE_WITH_LITERT_LM`, `SPEECH_CORE_WITH_HF_DOWNLOAD`, `SPEECH_CORE_BUILD_EXAMPLES`, `SPEECH_CORE_BUILD_HTTP_SERVER`, `SPEECH_CORE_WITH_OLLAMA`, and `SPEECH_CORE_PACKAGE`.
- Incompatible option combos fail fast: `SPEECH_CORE_WITH_HF_DOWNLOAD` requires `SPEECH_CORE_WITH_LITERT`, and `SPEECH_CORE_BUILD_HTTP_SERVER` requires `SPEECH_CORE_WITH_ONNX` (`CMakeLists.txt:20-29`).
- Shell scripts are forced to LF line endings via `*.sh text eol=lf` so installed/CI scripts survive Windows checkouts (`.gitattributes:4`).
- `.gitignore:1-31` excludes build trees, venvs, caches, compiled artifacts (`*.o`, `*.a`, `*.so`, `*.dylib`, `*.xcframework`), while `.gitignore:22-31` keeps fetched model bundles and runtime prebuilds (`/scripts/models*/`, `/litert/`, `/ort-linux/`, `/ort-win-gpu/`) out of git.
- `THIRD-PARTY-NOTICES.md:10-27` states binary `.deb`/`.tar.gz`/Windows `.zip` releases bundle ONNX Runtime (MIT) and `libLiteRt.so` (Apache-2.0), while `THIRD-PARTY-NOTICES.md:87-93` states no ML models ship in any package and models are fetched separately at runtime.
- Truncated in this chunk (contents beyond what is quoted below are not claimed): `CMakeLists.txt` past its first ~239 of 1378 lines, the `README translations` tails of `AGENTS.md`/`CLAUDE.md`/`CODEX.md`, and the tails of `README_ar/de/es/fr/hi/ja/ko/pt/ru/th/tr/vi.md`.

## The system in five moves
1. Start from a local-first promise: on-device C++17 speech infrastructure covering VAD, batch/streaming STT, diarization, TTS, and the voice-agent pipeline, running on CPU with no cloud, no Python at inference, and no audio leaving the machine.
2. Separate a small model-agnostic orchestration core — turn detection, interruption, audio utils, conversation state, tool calls — from the models the application chooses.
3. Make live-agent behavior native to that core: VAD-driven turns, eager STT, partial transcripts, barge-in, streaming TTS, and tool calling, with streaming ASR built on cache-aware RNN-T decoders plus end-of-utterance, beam search, and phrase biasing.
4. Turn backend selection into a construction and link decision — ONNX Runtime, LiteRT, both, neither, or custom abstract-interface implementations — exposed through portable native C++ plus C APIs for Kotlin/JNI, Swift/FFI, and embedded hosts, with CMake targets and fail-fast option guards enforcing the split.
5. Ship it as tested, packaged infrastructure: Linux, Windows, macOS, and Android-oriented arm64 builds with sanitizer and model-backed lanes, Linux `.deb`/`.tar.gz` (plus Windows ZIP) releases bundling runtimes but never models, with version-control hygiene, multilingual READMEs, and third-party notices defining the contributor and license contract.
