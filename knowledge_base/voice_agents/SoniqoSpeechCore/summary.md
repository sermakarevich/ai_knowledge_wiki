# Technical Analysis: soniqo/speech-core

**Repository:** https://github.com/soniqo/speech-core
**Version analyzed:** 0.0.11 (release line; CMake `project(speech_core VERSION 0.1.0)` per `CMakeLists.txt:9-12`)
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

The problem space is shipping a complete voice-interaction loop — voice activity detection, speech-to-text (batch and streaming), speaker diarization, speech enhancement, text-to-speech, and tool-calling dialogue — fully on-device on CPU, without cloud APIs, without Python at inference time, and without audio leaving the machine (README.md:15, README.md:17). The repo addresses it with a small model-agnostic C++17 orchestration core (`speech_core`) that owns turn detection, interruption handling, audio utilities, conversation state, and tool calls, while the application chooses and links concrete models via optional ONNX Runtime and LiteRT backends (README.md:34, README.md:39). The primary user is the application developer building an offline voice agent for Linux, Windows, macOS, or Android — including resource-constrained Android targets, where a full offline voice-agent demo fits in 1.2 GB (README.md:30). Releases distribute Linux `.deb`/`.tar.gz` packages (amd64/arm64) and a Windows x64 ZIP that bundle runtime libraries but never models; models are fetched separately at runtime (README.md:149, THIRD-PARTY-NOTICES.md:87-93).

## 2. High-Level Architecture

```text
application audio / events
            │
            ▼
┌──────────────────────────────────────┐
│ speech_core (pure C++17, zero ML)    │
│ VoicePipeline · TurnDetector         │
│ SpeechQueue · ConversationContext    │
│ StreamingVAD · audio utils (buffer,  │
│ resampler, pcm_codec) · C API        │
│ abstract VAD / STT / LLM / TTS /     │
│ enhancer / echo-canceller APIs       │
└──────────────┬───────────────┬───────┘
               │               │
      ┌────────▼────────┐ ┌────▼────────────────┐
      │ ONNX Runtime    │ │ LiteRT / LiteRT-LM  │
      │ speech_core_    │ │ speech_core_models_ │
      │ models          │ │ litert[_lm]         │
      │ reference models│ │ reference models    │
      └─────────────────┘ └─────────────────────┘
```

(Structure per README.md:176-191 and AGENTS.md:5-12.)

Data-flow narrative:

1. The host pushes float PCM frames into the orchestration core (`VoicePipeline::push_audio`); `StreamingVAD` plus `TurnDetector` decide when speech starts and when a turn ends (README.md:123-137, CMakeLists.txt:45-81).
2. Completed or partial utterances are routed to whichever `STTInterface` implementation the application constructed (e.g. `LiteRTParakeetStt::transcribe`); streaming decoders use cache-aware RNN-T decoding with end-of-utterance detection, beam search, and phrase biasing (README.md:38, README.md:109-121).
3. Recognized text updates the in-core `ConversationContext`, optionally triggers an `LLMInterface` call and structured tool calls, and interruptions (barge-in) preempt the output path (README.md:37, AGENTS.md:5-7).
4. Response text flows to a `TTSInterface` implementation (e.g. streaming Pocket TTS emitting fixed 80 ms frames with a bounded decoder cache, README.md:48); optional enhancement (DeepFilterNet3, LocalVQE AEC, Sidon) and diarization (`DiarizationPipeline`) run as orthogonal stages (README.md:47, AGENTS.md:44).
5. Audio and events leave through the native C++ API or the C API surface (`src/speech_core_c.cpp`) suitable for Kotlin/JNI, Swift/FFI, and embedded Linux hosts; the OpenAI-compatible `speech-server` sidecar exposes `POST /v1/audio/speech` (README.md:40, README.md:45).

Persistent state: none outside the process. Conversation state, the speech queue, VAD/turn-detector state, and streaming decoder caches (e.g. the bounded Pocket TTS decoder cache) live in process memory; fetched model bundles and runtime prebuilds live on disk but are explicitly excluded from git (`/scripts/models*/`, `/litert/`, `/ort-linux/`, `/ort-win-gpu/` per .gitignore:22-31) and no ML models ship in any package (THIRD-PARTY-NOTICES.md:87-93).

## 3. The Abstract Speech Interfaces

The central concept is the set of model-agnostic abstract interfaces in `include/speech_core/interfaces.h` (AGENTS.md:5-12): the orchestration target never depends on a concrete model, and a backend swap is a construction and link choice, not a pipeline rewrite (README.md:193). Representation is pure C++17 abstract classes with zero ML dependencies; the core library compiles with `-Wall -Wextra -Wpedantic` on non-MSVC and `POSITION_INDEPENDENT_CODE ON` (CMakeLists.txt:99-110).

Named kinds (all in `include/speech_core/interfaces.h` per AGENTS.md:5-12):

- `STTInterface` (AGENTS.md:7), `TTSInterface` (AGENTS.md:7), `VADInterface` (AGENTS.md:7), `TurnCompletionInterface` (AGENTS.md:8), `EnhancerInterface` (AGENTS.md:8), `EchoCancellerInterface` (AGENTS.md:8), `LLMInterface` (AGENTS.md:8), plus `SegmentationInterface` / `EmbeddingInterface` / `DiarizerInterface` (AGENTS.md:8).
- `DiarizationPipeline` in `include/speech_core/diarization/`, pure C++17 and built into the core library (AGENTS.md:44).
- Concrete reference implementations live outside the core: ONNX side (`src/models/silero/silero_vad.cpp`, `src/models/parakeet/parakeet_stt.cpp`, `src/models/kokoro/kokoro_tts.cpp`, `src/models/deepfilter/deepfilter.cpp`, `src/models/smartturn/onnx_smart_turn.cpp` per CMakeLists.txt:146-171) and LiteRT side (e.g. `LiteRTParakeetStt` in `speech_core/models/litert_parakeet_stt.h` per README.md:85).

Key usage (verbatim, README.md:109-121):

```cpp
#include <speech_core/models/litert_parakeet_stt.h>

speech_core::LiteRTParakeetStt stt(
    "parakeet-encoder.tflite",
    "parakeet-decoder-joint.tflite",
    "vocab.json");

auto result = stt.transcribe(audio, sample_count, 16000);
std::cout << result.text << "\n";
```

## 4. LLM / External Service Integration

The repo makes no required network or LLM calls: the default posture is fully offline CPU inference with no cloud and no audio leaving the machine (README.md:17). LLM participation is an optional, application-supplied capability behind `LLMInterface` (AGENTS.md:8):

- **Optional Ollama adapter:** `SPEECH_CORE_WITH_OLLAMA=ON` builds the `speech_core_llm_ollama` adapter, which vendors cpp-httplib + nlohmann/json to talk to a locally hosted Ollama endpoint (CMakeLists.txt:9-18, option table).
- **Optional on-device LM:** FunctionGemma 270M for structured tool calls runs via the `speech_core_models_litert_lm` target backed by `libLiteRt-LM` (README.md:53-80 model table; CMakeLists.txt:9-18).
- **Optional local HTTP surface:** `speech-server` exposes OpenAI-compatible `POST /v1/audio/speech` with model aliases, voices, language/speed controls, WAV/PCM output, and optional bearer authentication — served locally, not a cloud dependency (README.md:45).

Env vars / paths (no secrets; all are local build/runtime locators):

| Variable | Purpose |
|---|---|
| `ORT_DIR` | Extracted ONNX Runtime release used by the ONNX backend (README.md:86-91) |
| `LITERT_DIR` | LiteRT tree extracted by `scripts/fetch_litert.sh` (README.md:97-107) |
| `LITERT_LM_DIR` | LiteRT-LM tree from `scripts/fetch_litert_lm.sh`, needed for `SPEECH_CORE_WITH_LITERT_LM` (CMakeLists.txt:9-18) |
| (unnamed) model-dir env vars | Backend integration tests skip when these are unset; core tests need no model files (README_zh.md:196-203) |

## 5. The Voice-Agent Pipeline

The primary workflow connects any implementations of the abstract VAD, STT, LLM, and TTS interfaces to the live pipeline (README.md:123-137). Step by step (function-level line numbers are not quoted in the covered wiki chunks beyond the CMake source list at CMakeLists.txt:45-81, so locations are file-level):

1. **Configure** — build an `AgentConfig` and select `AgentConfig::Mode::Pipeline` (`include/speech_core/`, `src/pipeline/voice_pipeline.cpp`).
2. **Construct** — instantiate `VoicePipeline` with `(stt, tts, &llm, vad, config, event_callback)` where the callback receives transcription, response audio, tool-call, or error events (`src/pipeline/voice_pipeline.cpp`; README.md:123-137).
3. **Start** — call `VoicePipeline::start()` to arm the state machine (`src/pipeline/voice_pipeline.cpp`).
4. **Stream audio in** — call `VoicePipeline::push_audio(mic_samples, sample_count)` per frame; `src/vad/streaming_vad.cpp` scores speech presence while `src/pipeline/turn_detector.cpp` (with Smart Turn v3.2 / Parakeet-EOU style end-of-turn signals) decides turn boundaries (`src/vad/streaming_vad.cpp`, `src/pipeline/turn_detector.cpp`; README.md:37-38).
5. **Transcribe eagerly** — partial and final hypotheses flow from the STT implementation (cache-aware RNN-T decoders, beam search, contextual phrase biasing) through `src/pipeline/speech_queue.cpp` (`src/pipeline/speech_queue.cpp`; README.md:37-38).
6. **Reason and act** — finalized text updates `src/pipeline/conversation_context.cpp`, optionally invokes the LLM and structured tool calls (`src/pipeline/conversation_context.cpp`; README.md:37).
7. **Speak with barge-in** — response text is synthesized (streaming TTS path) and played; new VAD-gated input interrupts output via the core's interruption handling (`src/pipeline/voice_pipeline.cpp`, `src/tts_synthesis_options.cpp`; README.md:37, README.md:48).
8. **Export across languages** — embedders link only what they use through the C API in `src/speech_core_c.cpp` (`src/speech_core_c.cpp`; README.md:139-145).

Verbatim wiring (README.md:123-137):

```cpp
speech_core::AgentConfig config;
config.mode = speech_core::AgentConfig::Mode::Pipeline;

speech_core::VoicePipeline pipeline(
    stt, tts, &llm, vad, config,
    [](const speech_core::PipelineEvent& event) {
        // transcription, response audio, tool call, or error
    });

pipeline.start();
pipeline.push_audio(mic_samples, sample_count);
```

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `CMakeLists.txt` | 1378 (first ~239 covered) | Build definition: 3 static-library targets, feature options, CPack rules (CMakeLists.txt:1-18, CMakeLists.txt:20-29) |
| `include/speech_core/interfaces.h` | n/a in chunks | All abstract interfaces: STT/TTS/VAD/turn-completion/enhancer/echo-canceller/LLM/segmentation/embedding/diarizer (AGENTS.md:5-12) |
| `src/pipeline/voice_pipeline.cpp` | n/a in chunks | Live agent orchestration: turns, interruption, tool calls, event dispatch (CMakeLists.txt:45-81) |
| `src/pipeline/turn_detector.cpp` | n/a in chunks | End-of-turn detection feeding the pipeline state machine (CMakeLists.txt:45-81) |
| `src/pipeline/speech_queue.cpp` | n/a in chunks | Ordering/buffering of (partial) hypotheses and responses (CMakeLists.txt:45-81) |
| `src/pipeline/conversation_context.cpp` | n/a in chunks | In-memory dialogue state owned by the core (CMakeLists.txt:45-81) |
| `src/vad/streaming_vad.cpp` | n/a in chunks | Frame-wise streaming VAD scoring (CMakeLists.txt:45-81) |
| `src/audio/audio_buffer.cpp` | n/a in chunks | Float audio-buffer primitives; no platform audio dependency (CMakeLists.txt:45-81) |
| `src/audio/resampler.cpp` | n/a in chunks | Sample-rate conversion for heterogeneous model front ends (CMakeLists.txt:45-81) |
| `src/audio/pcm_codec.cpp` | n/a in chunks | PCM encode/decode incl. WAV/PCM CLI and server output paths (CMakeLists.txt:45-81) |
| `src/diarization/diarization_pipeline.cpp` | n/a in chunks | Pure-C++17 diarization pipeline built into `speech_core` (CMakeLists.txt:45-81) |
| `src/speech_core_c.cpp` | n/a in chunks | C API for Kotlin/JNI, Swift/FFI, embedded hosts (CMakeLists.txt:45-81) |
| `src/tts_synthesis_options.cpp` | n/a in chunks | TTS voice/language/speed option handling (CMakeLists.txt:45-81) |
| `src/models/silero/silero_vad.cpp` | n/a in chunks | Silero v5 VAD reference impl; requires 64-sample left context (CMakeLists.txt:146-171; README.md:49) |
| `src/models/parakeet/parakeet_stt.cpp` | n/a in chunks | Parakeet TDT v3 STT reference implementation (CMakeLists.txt:146-171) |
| `src/models/kokoro/kokoro_tts.cpp` | n/a in chunks | Kokoro TTS reference implementation (CMakeLists.txt:146-171) |
| `src/models/deepfilter/deepfilter.cpp` | n/a in chunks | DeepFilterNet3 enhancement with libdf-compatible DSP (CMakeLists.txt:146-171; README.md:47) |
| `src/models/smartturn/onnx_smart_turn.cpp` | n/a in chunks | Smart Turn end-of-turn reference implementation (CMakeLists.txt:146-171) |
| `src/models/pocket/pocket_tts_tokenizer.cpp` | n/a in chunks | Pocket TTS tokenizer; adapts sherpa-onnx SentencePiece algorithm, no sherpa runtime linked (THIRD-PARTY-NOTICES.md:51-85) |
| `scripts/fetch_litert.sh` | n/a in chunks | Fetches the LiteRT prebuild tree (`LITERT_DIR`) backing the LiteRT backend (README.md:97-107) |

Line counts for implementation files are not quoted in the covered wiki chunks; only the CMake source list (CMakeLists.txt:45-81, CMakeLists.txt:146-180) and the top-level option tables are.

## 7. Dependencies

Required first. The covered chunks quote no third-party version pins — only `cmake_minimum_required(VERSION 3.16)` and C++17 (CMakeLists.txt:1-18) — so constraints below are exactly as stated in the wiki (unpinned where unpinned).

| Package | Version constraint | Purpose |
|---|---|---|
| CMake | `>= 3.16` (`cmake_minimum_required(VERSION 3.16)`) | Build system (CMakeLists.txt:1-18) |
| C++ toolchain | C++17 | Language level for the entire tree (CMakeLists.txt:1-18; AGENTS.md:130-139) |
| ONNX Runtime | unpinned; extracted release located via `ORT_DIR` | Inference backend for `speech_core_models`; CPU/NNAPI/QNN/su
...[truncated 7370 chars]