> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** speech-core is on-device C++17 speech infrastructure for Linux, Windows, and Android covering VAD, batch and streaming STT, diarization, TTS, and the voice-agent pipeline that connects them (README.md:15).
## Key points
- speech-core runs locally on CPU with no cloud, no Python at inference, and no audio leaving the machine (README.md:17).
- The core is a small model-agnostic orchestration layer owning turn detection, interruption handling, audio utilities, conversation state, and tool calls, while the application chooses the models (README.md:34).
- Live-agent behavior is built in: VAD-driven turns, eager STT, partial transcripts, barge-in, streaming TTS, and tool calling (README.md:37).
- Streaming ASR uses cache-aware RNN-T decoders with end-of-utterance detection, beam search, and contextual phrase biasing (README.md:38).
- Backend choice is a construction and link decision: ONNX Runtime, LiteRT, both, neither, or custom implementations of the abstract interfaces, and the orchestration target never depends on a concrete model (README.md:39, README.md:193).
- The portable surface is a native C++ API plus C APIs suitable for Kotlin/JNI, Swift/FFI, embedded Linux, and other hosts (README.md:40).
- Targets covered are Linux, Windows, macOS, Android-oriented arm64 builds, plus sanitizers and model-backed nightly lanes (README.md:41).
- Releases ship Linux `.deb`/`.tar.gz` packages for amd64 and arm64 that bundle runtime libraries but not models (README.md:149).
---
## Purpose and scope
On-device speech infrastructure in **C++17** for **Linux, Windows, and Android**: voice activity detection, batch and real-time streaming speech-to-text, speaker diarization, text-to-speech, and the voice-agent pipeline that connects them (README.md:15).
Runs locally on CPU. No cloud, no Python at inference, and no audio leaves the machine (README.md:17).
Full offline voice-agent demo fits in 1.2 GB on Android via the speech-android control-demo (README.md:30).
## Design principles
speech-core separates a small, model-agnostic orchestration layer from optional inference backends. The core owns turn detection, interruption handling, audio utilities, conversation state, and tool calls; your application chooses the models (README.md:34).
- **Local-first:** pure C++17 core, float audio buffers, no network or platform audio dependency (README.md:36).
- **Built for live agents:** VAD-driven turns, eager STT, partial transcripts, barge-in, streaming TTS, and tool calling (README.md:37).
- **Real streaming ASR:** cache-aware RNN-T decoders, end-of-utterance detection, beam search, and contextual phrase biasing (README.md:38).
- **Backend choice:** enable ONNX Runtime, LiteRT, both, neither, or implement the abstract interfaces yourself (README.md:39).
- **Portable surface:** native C++ API plus C APIs suitable for Kotlin/JNI, Swift/FFI, embedded Linux, and other hosts (README.md:40).
- **Tested across targets:** Linux, Windows, macOS, Android-oriented arm64 builds, sanitizers, and model-backed nightly lanes (README.md:41).
## v0.0.11 highlights
- **OpenAI-compatible local TTS:** `speech-server` exposes `POST /v1/audio/speech` with OpenAI model aliases, native and generic voices, language and speed controls, WAV/PCM output, and optional bearer authentication (README.md:45).
- **Windows release package:** a self-contained x64 ZIP ships the server, ONNX CLI tools, `speech.dll`, ONNX Runtime, and a native PowerShell model downloader; CI builds and smoke-tests the extracted archive (README.md:46).
- **DeepFilterNet3 parity:** native libdf-compatible STFT scaling, ERB/complex normalization, deep filtering, overlap-add, and 480-sample delay compensation restore reference DSP behavior (README.md:47).
- **Streaming Pocket TTS:** the ONNX backend emits fixed 80 ms frames with a bounded decoder cache and an opt-in model-backed round-trip harness (README.md:48).
- **Correct Silero v5 context:** every ONNX inference now receives the graph's required 64-sample left context (README.md:49).
## Supported models
See `docs/models.md` for maturity, bundle layouts, preprocessing, memory notes, and complete examples (README.md:82).
| Model | Task | ONNX | LiteRT |
|---|---|:---:|:---:|
| Silero VAD v5 | Voice activity detection | ✓ | ✓ |
| Smart Turn v3.2 | End-of-turn detection | ✓ | — |
| Parakeet TDT v3 (0.6B) | Speech-to-text | ✓ | ✓ |
| Whisper v3 / turbo | Multilingual speech-to-text | ✓ | — |
| Canary 180M Flash | Speech-to-text + translation (en/de/es/fr) | ✓ | — |
| Nemotron Speech Streaming (0.6B) | Streaming speech-to-text | ✓ | ✓ |
| Nemotron-3.5 multilingual (0.6B) | Prompt-conditioned streaming STT | ✓ | ✓ |
| MOSS Transcribe-Diarize 0.9B | Multilingual transcription + speaker activity | ✓ | — |
| Parakeet-EOU (120M) | Streaming STT + end-of-utterance | ✓ | — |
| Omnilingual ASR CTC (300M) | Multilingual speech-to-text | — | ✓ |
| Pyannote Segmentation 3.0 | Diarization segmentation | — | ✓ |
| WeSpeaker ResNet34-LM | Speaker embedding | — | ✓ |
| ReDimNet2-B6 | Speaker embedding | ✓ | — |
| VoxCPM 0.5B | 16 kHz TTS + voice cloning | ✓ | — |
| VoxCPM2 (2B) | 48 kHz TTS + voice cloning | ✓ | ✓ |
| CosyVoice3 0.5B | 24 kHz conditioned TTS | staged | — |
| Chatterbox | 24 kHz text-to-speech | — | ✓ |
| Supertonic 3 | Text-to-speech | — | ✓ |
| Indic-Mio | Hindi/Indic voice cloning + emotion | — | ✓ |
| Kokoro 82M | Text-to-speech | ✓ | ✓ |
| Pocket TTS 100M | Streaming TTS (fixed Alba voice) | ✓ | — |
| DeepFilterNet3 | Speech enhancement | ✓ | — |
| LocalVQE v1.4 AEC | Acoustic echo cancellation | ✓ | — |
| Sidon | Denoise + dereverb (16 → 48 kHz) | ✓ | — |
| PersonaPlex 7B | Full-duplex speech-to-speech (CUDA) | structural | — |
| FunctionGemma 270M | On-device structured tool calls | — | LiteRT-LM |
(Table content per README.md:53-80; links omitted, cell values verbatim.)
## Platforms and backends
| Backend | Target | Platforms | Runtime setup |
|---|---|---|---|
| Core only | `speech_core` | Linux, Windows, macOS, Android | none |
| ONNX Runtime | `speech_core_models` | Linux, Windows, macOS, Android | extracted ONNX Runtime release via `ORT_DIR` |
| LiteRT | `speech_core_models_litert` | Linux x86_64, Windows x86_64, macOS arm64, Android | `scripts/fetch_litert.sh` / `LITERT_DIR` |
| LiteRT-LM | `speech_core_models_litert_lm` | macOS, Android build path | `scripts/fetch_litert_lm.sh` / `LITERT_LM_DIR` |
(Table per README.md:86-91.)
ONNX can use CPU, Android NNAPI, Qualcomm QNN on Linux, or an application-supplied execution-provider hook. LiteRT currently uses CPU through its C API (README.md:93).
## Quick start
Build the core and LiteRT backend (README.md:97-107):
```bash
git clone https://github.com/soniqo/speech-core.git
cd speech-core
scripts/fetch_litert.sh build/litert
cmake -B build -DCMAKE_BUILD_TYPE=Release \
    -DSPEECH_CORE_WITH_LITERT=ON \
    -DLITERT_DIR="$PWD/build/litert"
cmake --build build --parallel
```
Transcribe an audio buffer; Parakeet v3 detects the language automatically (README.md:109-121):
```cpp
#include <speech_core/models/litert_parakeet_stt.h>

speech_core::LiteRTParakeetStt stt(
    "parakeet-encoder.tflite",
    "parakeet-decoder-joint.tflite",
    "vocab.json");

auto result = stt.transcribe(audio, sample_count, 16000);
std::cout << result.text << "\n";
```
Connect any implementations of the abstract VAD, STT, LLM, and TTS interfaces to the live pipeline (README.md:123-137):
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
Link only what your application uses (README.md:139-145):
```cmake
target_link_libraries(my_app PRIVATE speech_core)
target_link_libraries(my_app PRIVATE speech_core speech_core_models)
target_link_libraries(my_app PRIVATE speech_core speech_core_models_litert)
```
## Linux CLI packages
Releases ship `.deb` and `.tar.gz` packages for amd64 and arm64. The package bundles runtime libraries but not models (README.md:149).
```bash
VERSION=0.0.11
ARCH="$(dpkg --print-architecture)"   # amd64 or arm64
curl -fLO "https://github.com/soniqo/speech-core/releases/download/v${VERSION}/speech_${VERSION}_${ARCH}.deb"
sudo apt install "./speech_${VERSION}_${ARCH}.deb"

speech download-models
speech transcribe recording.wav
speech turn recording.wav
speech speak "Hello world" hello.wav
speech phonemize "Bonjour le monde" fr
speech serve
```
(README.md:151-163.) The amd64 package also includes the LiteRT VoxCPM2 voice-cloning command. Its x86 bundle is about 13 GB and is downloaded explicitly (README.md:165):
```bash
speech download-models voxcpm2
speech clone reference.wav "This is my cloned voice." cloned.wav
```
Exact syntax, model directories, standalone binaries, and the amd64/arm64 command matrix are in the Linux CLI reference `docs/cli.md` (README.md:172).
## Architecture
```text
application audio / events
            │
            ▼
┌──────────────────────────────────────┐
│ speech_core                          │
│ VoicePipeline · turn detection       │
│ interruption · tools · audio utils   │
│ abstract VAD / STT / LLM / TTS APIs  │
└──────────────┬───────────────┬───────┘
               │               │
      ┌────────▼────────┐ ┌────▼────────────┐
      │ ONNX Runtime    │ │ LiteRT / LiteRT-LM │
      │ reference models│ │ reference models   │
      └─────────────────┘ └─────────────────────┘
```
(README.md:176-191.) The orchestration target never depends on a concrete model. A backend swap is a construction and link choice, not a pipeline rewrite (README.md:193).
## Truncation note
The chunk ends mid-section: the `Documentation` table header at README.md:197-199 is cut off after its first rows and no topic rows are present, so documentation links beyond `docs/cli.md`, `docs/http-server.md`, and `docs/models.md` are not covered here. The trailing `Macro components` list names only `top-level-files/` (README.md:200-202) and is covered by the companion page `02-top-level-files.md`.
**Covers:** README.md (repo root overview, model/backend tables, quick-start snippets, CLI package commands, architecture diagram) as captured in chunks/01-overview.md:1-202.
