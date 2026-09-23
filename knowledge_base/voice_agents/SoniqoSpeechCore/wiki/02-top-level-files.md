[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repo root defines the build, contributor contract, multilingual front door, and license notices for the C++17 voice-agent engine and its optional ONNX/LiteRT backends.
## Key points
- The root is a C++17 voice-agent pipeline engine whose core (state machine, turn detection, interruption, speech queue, context, streaming VAD, audio utils) has zero ML dependencies (`AGENTS.md:5-7`).
- Three static-library targets split the build: always-built `speech_core`, ONNX-gated `speech_core_models`, LiteRT-gated `speech_core_models_litert` (`AGENTS.md:65-67`; `CMakeLists.txt:9-12`).
- `CMakeLists.txt:1-18` pins `cmake_minimum_required(VERSION 3.16)`, `project(speech_core VERSION 0.1.0 LANGUAGES CXX)`, C++17, and options including `SPEECH_CORE_WITH_ONNX`, `SPEECH_CORE_WITH_LITERT`, `SPEECH_CORE_WITH_LITERT_LM`, `SPEECH_CORE_WITH_HF_DOWNLOAD`, `SPEECH_CORE_BUILD_EXAMPLES`, `SPEECH_CORE_BUILD_HTTP_SERVER`, `SPEECH_CORE_WITH_OLLAMA`, and `SPEECH_CORE_PACKAGE`.
- Incompatible option combos fail fast: `SPEECH_CORE_WITH_HF_DOWNLOAD` requires `SPEECH_CORE_WITH_LITERT`, and `SPEECH_CORE_BUILD_HTTP_SERVER` requires `SPEECH_CORE_WITH_ONNX` (`CMakeLists.txt:20-29`).
- Shell scripts are forced to LF line endings via `*.sh text eol=lf` so installed/CI scripts survive Windows checkouts (`.gitattributes:4`).
- `.gitignore:1-31` excludes build trees, venvs, caches, compiled artifacts (`*.o`, `*.a`, `*.so`, `*.dylib`, `*.xcframework`), while `.gitignore:22-31` keeps fetched model bundles and runtime prebuilds (`/scripts/models*/`, `/litert/`, `/ort-linux/`, `/ort-win-gpu/`) out of git.
- `THIRD-PARTY-NOTICES.md:10-27` states binary `.deb`/`.tar.gz`/Windows `.zip` releases bundle ONNX Runtime (MIT) and `libLiteRt.so` (Apache-2.0), while `THIRD-PARTY-NOTICES.md:87-93` states no ML models ship in any package and models are fetched separately at runtime.
- Truncated in this chunk (contents beyond what is quoted below are not claimed): `CMakeLists.txt` past its first ~239 of 1378 lines, the `README translations` tails of `AGENTS.md`/`CLAUDE.md`/`CODEX.md`, and the tails of `README_ar/de/es/fr/hi/ja/ko/pt/ru/th/tr/vi.md`.
---
## Version-control hygiene (.gitattributes, .gitignore)
Verbatim excerpt (`.gitattributes:1-5`):
```
# Shell scripts must stay LF — they execute on Linux/macOS (CI, containers,
# the .deb's installed speech_download_models*) even when the repo is checked
# out on Windows with core.autocrlf=true.
*.sh text eol=lf
```
Verbatim excerpt (`.gitignore:1-12`):
```
build/
build-*/
cmake-build-*/
dist/
.venv/
venv/
.cache/
__pycache__/
*.pyc
compile_commands.json
*.o
*.a
```
Model/runtime exclusion block (`.gitignore:22-31`): `/scripts/models/`, `/scripts/models-litert/`, `/scripts/models-voxcpm2/`, `/scripts/personaplex-*/`, `/scripts/sherpa-models/`, `/scripts/librispeech/`, `/litert/`, `/ort-linux/`, `/ort-win-gpu/`, plus `/.claude/` and `/bench-external.json`.
## Agent contract (AGENTS.md, CLAUDE.md, CODEX.md)
The three files are identical 158-line agent instructions. Five-part project definition (`AGENTS.md:5-12`):
1. Orchestration core, pure C++17, zero ML deps.
2. Abstract interfaces (`STTInterface`, `TTSInterface`, `VADInterface`, `TurnCompletionInterface`, `EnhancerInterface`, `EchoCancellerInterface`, `LLMInterface`, plus `SegmentationInterface`/`EmbeddingInterface`/`DiarizerInterface`) in `include/speech_core/interfaces.h`.
3. Optional ONNX reference implementations gated by `SPEECH_CORE_WITH_ONNX=ON`.
4. Optional LiteRT reference implementations gated by `SPEECH_CORE_WITH_LITERT=ON`, backed by `libLiteRt` extracted by `scripts/fetch_litert.sh`.
5. `DiarizationPipeline` in `include/speech_core/diarization/`, pure C++17, built into the core library.
Layout (`AGENTS.md:15-19`): `include/speech_core/` public headers, `src/` implementations, `tests/` (`test_*.cpp` via `file(GLOB)`), `docs/` (`pipeline.md`, `interfaces.md`, `models.md`, `c-api.md`, `tools.md`), `scripts/` utilities. Test command (`AGENTS.md:111-113`):
```bash
cmake -B build && cmake --build build && cd build && ctest --output-on-failure
```
9 test executables are named (`AGENTS.md:117`): `test_audio_buffer`, `test_c_api`, `test_conversation_context`, `test_pcm_codec`, `test_pipeline_e2e`, `test_resampler`, `test_speech_queue`, `test_streaming_vad`, `test_tools`; `test_pipeline_e2e` is noted intermittently flaky with SIGTRAP under load (`AGENTS.md:119`). Workflow rules (`AGENTS.md:121-126`): never push directly to main, branch names `feat/|fix/|chore/|docs/`, PR needs summary/what-changed/test-plan, releases tagged `git tag v0.0.X`. Guideline excerpts (`AGENTS.md:130-139`): C++17 only, no platform-specific code in `speech_core` (Android NNAPI/QNN gating lives in `models/`), don't commit unless asked, run `ctest --output-on-failure` after changes, build both default and `SPEECH_CORE_WITH_ONNX=ON` after CMake changes. English `README.md` is canonical with 13 mirrors (`AGENTS.md:141-143`); mirror tails were truncated in this chunk.
## Build system (CMakeLists.txt)
Exact option names (`CMakeLists.txt:9-18`):
| Option | Default | Purpose |
|---|---|---|
| `SPEECH_CORE_BUILD_TESTS` | ON | Build tests |
| `SPEECH_CORE_WITH_ONNX` | OFF | `speech_core_models` ONNX reference implementations |
| `SPEECH_CORE_WITH_LITERT` | OFF | `speech_core_models_litert` LiteRT reference implementations |
| `SPEECH_CORE_WITH_LITERT_LM` | OFF | Standalone `speech_core_models_litert_lm` LLM target; needs `LITERT_LM_DIR` |
| `SPEECH_CORE_WITH_HF_DOWNLOAD` | OFF | libcurl Hugging Face downloads; requires `SPEECH_CORE_WITH_LITERT=ON` + `CURL` |
| `SPEECH_CORE_BUILD_EXAMPLES` | OFF | `examples/`; requires `SPEECH_CORE_WITH_ONNX=ON` |
| `SPEECH_CORE_BUILD_HTTP_SERVER` | OFF | OpenAI-compatible sidecar; requires `SPEECH_CORE_WITH_ONNX=ON` |
| `SPEECH_CORE_WITH_OLLAMA` | OFF | `speech_core_llm_ollama` adapter; vendors cpp-httplib + nlohmann/json |
| `SPEECH_CORE_PACKAGE` | OFF | Install rules + CPack (Linux `.deb`/`.tar.gz`, Windows `.zip`) |
Guards (`CMakeLists.txt:20-29`): `FATAL_ERROR` when `SPEECH_CORE_WITH_HF_DOWNLOAD` without `SPEECH_CORE_WITH_LITERT`, and when `SPEECH_CORE_BUILD_HTTP_SERVER` without `SPEECH_CORE_WITH_ONNX`. Core library sources listed verbatim include `src/pipeline/voice_pipeline.cpp`, `src/pipeline/turn_detector.cpp`, `src/pipeline/speech_queue.cpp`, `src/pipeline/conversation_context.cpp`, `src/vad/streaming_vad.cpp`, `src/audio/audio_buffer.cpp`, `src/audio/resampler.cpp`, `src/audio/pcm_codec.cpp`, `src/diarization/diarization_pipeline.cpp`, `src/speech_core_c.cpp`, `src/tts_synthesis_options.cpp` (`CMakeLists.txt:45-81`). kissfft C sources are compiled as C++ (`CMakeLists.txt:35-43`); `speech_core` sets `POSITION_INDEPENDENT_CODE ON` (`CMakeLists.txt:110`) and `-Wall -Wextra -Wpedantic` on non-MSVC (`CMakeLists.txt:99-103`). ONNX sources shown include `src/models/silero/silero_vad.cpp`, `src/models/parakeet/parakeet_stt.cpp`, `src/models/kokoro/kokoro_tts.cpp`, `src/models/deepfilter/deepfilter.cpp`, `src/models/smartturn/onnx_smart_turn.cpp` (`CMakeLists.txt:146-171`); the VoxCPM2 tokenizer is compiled into `speech_core_models` only when the LiteRT target is off to avoid duplicate symbols (`CMakeLists.txt:172-180`). Content past this point (remaining ~1139 of 1378 lines) was truncated in this chunk and is not summarized.
## READMEs (multilingual front door)
`README.zh-CN.md:1-4` is a 4-line stub: Simplified-Chinese README moved, read `README_zh.md`, kept for link compatibility. The 13 mirrors (`README_ar/de/es/fr/hi/ja/ko/pt/ru/th/tr/vi/zh.md`, 224–264 lines each) share one shape: local C++17 CPU-only pitch, docs links (`soniqo.audio`, `docs/cli.md`, `docs/http-server.md`), demo, why-bullets, v0.0.11 highlights, ONNX/LiteRT model-support table, backend/target/platform table (`speech_core`, `speech_core_models`, `speech_core_models_litert`, `speech_core_models_litert_lm`), quickstart (`scripts/fetch_litert.sh`, `cmake -B build`, `LiteRTParakeetStt::transcribe`, `VoicePipeline::start`/`push_audio`), Linux CLI `.deb` install block, and architecture diagram. Fully visible example — `README_zh.md:180-194` build variants:
```bash
# 仅编排：无 ML 运行时
cmake -B build -DCMAKE_BUILD_TYPE=Release
# ONNX 模型
cmake -B build-onnx -DCMAKE_BUILD_TYPE=Release \
    -DSPEECH_CORE_WITH_ONNX=ON -DORT_DIR=/path/to/onnxruntime
# LiteRT 模型
scripts/fetch_litert.sh build/litert
cmake -B build-litert -DCMAKE_BUILD_TYPE=Release \
    -DSPEECH_CORE_WITH_LITERT=ON -DLITERT_DIR="$PWD/build/litert"
```
`README_zh.md:196-203` notes core tests need no model files, backend integration tests skip without model-dir env vars, and CI covers Linux/Windows/macOS. License line (`README_zh.md:215`): Apache 2.0, see `LICENSE`. All mirrors except `README_zh.md` and the `zh-CN` stub had their tails truncated in this chunk; their closing sections are not claimed.
## Third-party notices (THIRD-PARTY-NOTICES.md)
ONNX Runtime block (`THIRD-PARTY-NOTICES.md:10-16`): `lib/speech/libonnxruntime.so*` (Linux), `bin/onnxruntime.dll` + `bin/onnxruntime_providers_shared.dll` (Windows), MIT, plus MSVC runtime DLLs under Visual Studio terms in the Windows ZIP. LiteRT block (`THIRD-PARTY-NOTICES.md:22-32`): `lib/speech/libLiteRt.so` from `ai-edge-litert` PyPI via `scripts/fetch_litert.sh`, Apache-2.0, statically incorporating TensorFlow/TFLite, XNNPACK (BSD-3), Eigen (MPL-2.0), FlatBuffers, ruy, farmhash (MIT), FP16/pthreadpool/cpuinfo, Abseil. Vendored tree (`THIRD-PARTY-NOTICES.md:51-85`): `third_party/litert/` headers (Apache-2.0); sherpa-onnx SentencePiece algorithm adapted into `src/models/pocket/pocket_tts_tokenizer.cpp` (Apache-2.0, no sherpa runtime linked); Ooura FFT in `third_party/fftooura/` used by `speech_core::audio::fft_real`/`ifft_real`; KISS FFT in `third_party/kissfft/` (BSD-3) used by the 960-point DeepFilterNet3 STFT/iSTFT and Indic-Mio host ISTFT.
**Covers:** `.gitattributes`, `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `CMakeLists.txt`, `README.zh-CN.md`, `README_ar/de/es/fr/hi/ja/ko/pt/ru/th/tr/vi/zh.md`, `THIRD-PARTY-NOTICES.md`
