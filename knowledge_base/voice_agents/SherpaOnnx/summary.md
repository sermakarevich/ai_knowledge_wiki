# Technical Analysis: k2-fsa/sherpa-onnx

**Repository:** https://github.com/k2-fsa/sherpa-onnx
**Version analyzed:** 1.13.8
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

The problem space is deployment fragmentation for speech processing: models trained in heterogeneous frameworks must run offline on many CPUs, NPUs, operating systems, and language runtimes without cloud dependence. Platform-specific toolchains, ABI differences (x64/x86/arm64/arm32/riscv64), OS differences (Linux, macOS, Windows, openKylin, Android, WearOS, iOS, HarmonyOS, NodeJS, WebAssembly), and accelerator differences (Rockchip RKNN, Qualcomm QNN, Ascend NPU, Axera NPU, Intel NPU via OpenVINO) make a single portable runtime difficult (README.md:119-139, README.md:90-98).

The repo addresses this by shipping one C/C++ core executed through ONNX Runtime, plus a root CMake configuration and one shell script per target that cross-compiles the same tree for each ABI/OS/accelerator combination (CMakeLists.txt:4524, build-android-arm64-v8a.sh:546, build-ios.sh:2628, build-ohos-arm64-v8a.sh:3190, build-wasm-simd-asr.sh:3877). The primary user is an application or device developer embedding offline speech capability (ASR streaming and non-streaming, TTS, diarization, identification, verification, language identification, audio tagging, VAD, keyword spotting, punctuation, enhancement, source separation) into mobile, desktop, embedded, or web software via C++, C, Python, Go, C#, Java, Kotlin, JavaScript, Swift, Rust, Dart, or Object Pascal APIs (README.md:105-117, README.md:141-146).

## 2. High-Level Architecture

```
README feature matrix ─► CMakeLists.txt feature flags ─► per-target build-*.sh
        │                           │                              ▼
        │                           │                    ONNX Runtime (pinned per OS)
        │                           ▼                              │
        │              sherpa-onnx C/C++ core (+ C API / JNI) ──────┤
        │                           │                              │
        │                           ▼                              ▼
 language bindings ──► CLI binaries / websocket / WASM ─► CPU │ GPU │ RKNN │ QNN │ Ascend │ Axera │ OpenVINO │ SpacemiT
        │                           │                              │
        ▼                           ▼                              ▼
 Flutter / Tauri demo apps     install/ + jniLibs / xcframework / .wasm + .js
```

Data flow in five steps. (1) The caller selects a function set and target: CMake options `SHERPA_ONNX_ENABLE_*` fix which subsystems (TTS, diarization, C API, websocket, JNI, GPU, WASM variants, RKNN/AXERA/AXCL/QNN/SPACEMIT) and `BUILD_SHARED_LIBS` are compiled in (CMakeLists.txt:4546, CMakeLists.txt:4558). (2) A per-target script configures the toolchain (Android NDK ABI, iOS simulator/device slices, OHOS toolchain, `aarch64-linux-gnu.toolchain.cmake`, Emscripten) and points at a pinned ONNX Runtime (Android/iOS/macOS default `1.28.2`; OHOS `1.16.3`; Linux ARM64 GPU `1.11.0`) (build-android-arm64-v8a.sh:641, build-ios.sh:2631, build-ohos-arm64-v8a.sh:3190, build-aarch64-linux-gnu.sh:463, CMakeLists.txt:4581). (3) `cmake` plus `make -j` builds the core and the selected adapters: shared `libsherpa-onnx-jni.so` plus `libonnxruntime.so` on Android, static archives merged with `libtool -static` on macOS, `SherpaOnnxC.framework` / `sherpa-onnx.xcframework` on iOS, or `sherpa-onnx-wasm-*.js/.wasm` under Emscripten (build-android-arm64-v8a.sh:563, build-macos.sh:3104, build-ios.sh:2631, build-wasm-simd-asr.sh:3935). (4) At runtime the application loads local ONNX model files and dispatches through the core to CPU/GPU/NPU providers; the OpenVINO path uses `--provider=openvino` / `--vad-provider=openvino` with an optional `provider:config-file` (e.g. `device_type=NPU`), falling back to CPU when OpenVINO is unavailable (OPENVINO.md:4950, OPENVINO.md:4972, OPENVINO.md:4988). (5) Release tooling versions and packs the outputs: `new-release.sh` bumps version strings across CMake, `version.cc`, gradle, `build*.sh`, `pom.xml`, Swift/SPM, Flutter/Dart, HarmonyOS, and CI; `release.sh` rebuilds Android and iOS targets and tars `sherpa-onnx-v<V>-android.tar.bz2` and `sherpa-onnx-v<V>-ios.tar.bz2` (new-release.sh:4812, release.sh:5204).

Persistent state lives outside the compiled tree: model weight files (`*.onnx`, `*.pt`, `*.rknn` are git-ignored build inputs), audio inputs (`*.wav`, `*.mp3`), and build/install directories (`build`, `build-*`, `sherpa-onnx-*`) plus native artifacts (`*.so`, `*.dylib`, `*.dll`, `*.a`, `*.o`) (`.gitignore:212`, `.gitignore:254`). The repository itself stores no runtime database; configuration persists in CMake cache entries and provider config files passed at invocation.

## 3. The Local Speech Function

The central concept is a locally executed speech function: a fixed capability (recognition, synthesis, separation, identification, diarization, verification, language identification, tagging, VAD, keyword spotting, punctuation, enhancement) instantiated from local ONNX weights and invoked through a language binding with no network call (README.md:105-117).

Representation in the analyzed pages is a documentation-level matrix, not a class definition: the overview page reproduces the README support table verbatim (README.md:13-29) and the introduction list of locally runnable functions naming `silero-vad` for VAD, `gtcrn` and `DPDFNet` for enhancement, and `spleeter` and `UVR` for separation (README.md:107, README.md:114-117). Named kinds, with citations:

- Speech-to-text, streaming and non-streaming (README.md:116)
- Text-to-speech (README.md:117)
- Speaker diarization / identification / verification (README.md:118-120)
- Spoken language identification; audio tagging (README.md:121-122)
- VAD, e.g. `silero-vad` (README.md:123)
- Speech enhancement, e.g. `gtcrn`, `DPDFNet` (README.md:124)
- Keyword spotting (README.md:125)
- Source separation, e.g. `spleeter`, `UVR` (README.md:126)
- Punctuation restoration, listed in the function matrix (README.md:28)

Key query pattern from the build surface (how a function set is selected at compile time):

```
set(SHERPA_ONNX_VERSION "1.13.8")
option(SHERPA_ONNX_ENABLE_C_API "Whether to build C API" ON)
option(SHERPA_ONNX_ENABLE_WEBSOCKET "Whether to build webscoket server/client" ON)
```

The snippet is verbatim from the top-level CMake excerpt (CMakeLists.txt:4558 area per 02-top-level-files.md). Function inclusion beyond this follows the same mechanism: `SHERPA_ONNX_ENABLE_TTS`, `SHERPA_ONNX_ENABLE_SPEAKER_DIARIZATION`, and the nine `SHERPA_ONNX_ENABLE_WASM*` task flags (`WASM_ASR/KWS/VAD/VAD_ASR/TTS/NODEJS/WEB/SPEAKER_DIARIZATION/SPEECH_ENHANCEMENT`) gate which function code is compiled (CMakeLists.txt:4558, CMakeLists.txt:4569).

## 4. LLM / External Service Integration

The repo calls no LLM and no metered external API at runtime. All functions listed in the analyzed pages run locally from ONNX files (README.md:105-117). No provider keys, endpoints, or network-related environment variables appear in the two component pages. The `Links for Huggingface Spaces` and WebAssembly spaces entries (README.md:148-194) are browser-tryable demos and pre-built Android APK references, not runtime service dependencies; the APK table body itself is truncated in the chunk and carries no rows (README.md:197-203). The only provider concept is the ONNX Runtime execution provider selected by local flags (`--provider=openvino`, `--vad-provider=openvino`, `provider:config-file` with `device_type=NPU`), which dispatches to a locally installed accelerator backend and falls back to CPU (OPENVINO.md:4950, OPENVINO.md:4988).

## 5. The Target Build Pipeline: Configure-Compile-Package

This is the only end-to-end workflow described in the available pages: turning the same source tree into per-target binaries. Each step cites the script and chunk line that defines it.

1. Select feature flags in `CMakeLists.txt:4546` — set `SHERPA_ONNX_ENABLE_PYTHON`, `SHERPA_ONNX_ENABLE_TESTS`, `BUILD_SHARED_LIBS`, `SHERPA_ONNX_ENABLE_PORTAUDIO`, `SHERPA_ONNX_ENABLE_JNI`, `SHERPA_ONNX_ENABLE_C_API`, `SHERPA_ONNX_ENABLE_WEBSOCKET`, `SHERPA_ONNX_ENABLE_GPU`/`DIRECTML`, the nine `SHERPA_ONNX_ENABLE_WASM*` flags, `SHERPA_ONNX_ENABLE_BINARY`, `SHERPA_ONNX_ENABLE_TTS`/`SPEAKER_DIARIZATION`, and `SHERPA_ONNX_ENABLE_RKNN/AXERA/AXCL/ASCEND_NPU/QNN/SPACEMIT` (CMakeLists.txt:4546, CMakeLists.txt:4558, CMakeLists.txt:4568, CMakeLists.txt:4575).
2. Invoke the target script in `build-*.sh:417` — each script creates its own `build-<target>` directory, runs `cmake` with the target toolchain, then `make -j` plus `make install/strip`, disabling `BUILD_PIPER_PHONMIZE_*` / `BUILD_ESPEAK_NG_*` executables and tests (build-aarch64-linux-gnu.sh:417, build-wasm-simd-asr.sh:3877).
3. Cross-compile embedded Linux in `build-aarch64-linux-gnu.sh:463` — use `aarch64-linux-gnu-gcc` / `arm-linux-gnueabihf-gcc`, cross-build `alsa-lib v1.2.12`, pass `-DSHERPA_ONNX_ENABLE_PORTAUDIO=ON -DSHERPA_ONNX_ENABLE_C_API=ON -DSHERPA_ONNX_ENABLE_WEBSOCKET=ON` via `toolchains/aarch64-linux-gnu.toolchain.cmake`; default is static (`BUILD_SHARED_LIBS=OFF`) (build-aarch64-linux-gnu.sh:497, build-aarch64-linux-gnu.sh:517, build-aarch64-linux-gnu.sh:527).
4. Cross-compile Android in `build-android-arm64-v8a.sh:641` — set `ANDROID_ABI` (`arm64-v8a`, `armeabi-v7a`, `x86_64`, `x86`), default `BUILD_SHARED_LIBS=ON` and ONNX Runtime `1.28.2` via `SHERPA_ONNX_ONNXRUNTIME_VERSION`, pass `-DSHERPA_ONNX_ENABLE_JNI=ON -DSHERPA_ONNX_ENABLE_PORTAUDIO=OFF`; outputs are `libsherpa-onnx-jni.so` plus copied `libonnxruntime.so` (build-android-arm64-v8a.sh:563, build-android-arm64-v8a.sh:720).
5. Build Apple targets in `build-ios.sh:2631` — triple-build `SIMULATOR64 / SIMULATORARM64 / OS64` with `DEPLOYMENT_TARGET=13.0`, `ENABLE_ARC=1`, `ENABLE_BITCODE=0`, merge with `lipo` plus `libtool -static`, then `xcodebuild -create-xcframework` as `SherpaOnnxC.framework`; macOS uses universal `CMAKE_OSX_ARCHITECTURES="arm64;x86_64"` with websocket off and an optional static merge into `install/lib/libsherpa-onnx.a` (build-ios.sh:2631, build-ios-shared.sh:2387, build-macos.sh:3073, build-macos.sh:3104). The iOS framework ships a `module.modulemap` for `sherpa-onnx/c-api/c-api.h` (build-ios.sh:2639, build-macos.sh:3084).
6. Build HarmonyOS in `build-ohos-arm64-v8a.sh:3190` — use `ohos.toolchain.cmake`, ONNX Runtime `1.16.3`, `-DOHOS_ARCH=arm64-v8a / armeabi-v7a / x86_64`, shared libraries with C API on (build-ohos-arm64-v8a.sh:3302).
7. Build NPU/RISC-V variants in `build-rknn-linux-aarch64.sh:3769` — supply vendor SDK roots (`SHERPA_ONNX_RKNN_TOOLKIT2_PATH`, `AXERA_SDK_ROOT`, `AXCL_SDK_ROOT`) with `-DSHERPA_ONNX_ENABLE_RKNN=ON / AXERA=ON / AXCL=ON`; RISC-V uses `riscv64-unknown-linux-gnu-gcc` with `toolchains/riscv64-linux-gnu*.toolchain.cmake`, SpacemiT adding `-DSHERPA_ONNX_ENABLE_SPACEMIT=ON` (build-axera-linux-aarch64.sh:1658, build-axcl-linux-aarch64.sh:1522, build-riscv64-linux-gnu-spacemit.sh:3615, build-riscv64-linux-gnu-spacemit.sh:3681).
8. Build WebAssembly in `build-wasm-simd-asr.sh:3935` — activate Emscripten (`emsdk 4.0.23`), pass `-DSHERPA_ONNX_ENABLE_WASM=ON` plus exactly one task flag (`WASM_ASR`, `WASM_TTS`, `WASM_WEB`, etc.); `build-flutter-web-wasm.sh:1846` copies `sherpa-onnx-wasm-web.js/.wasm` into `flutter/sherpa_onnx_web/assets/` and symlinks the JS wrappers (build-wasm-simd-web.sh:4485).
9. Version and release in `new-release.sh:4812` — bump `1.13.7 → 1.13.8` and version codes `20260901 → 20260910` across `CMakeLists.txt`, `sherpa-onnx/csrc/version.cc`, Android gradle files, `build*.sh`, `pom.xml`, Swift/SPM, Flutter/Dart, HarmonyOS, and CI via `sed -i.bak`; `release.sh:5204` re-reads the version with `grep "SHERPA_ONNX_VERSION" ./CMakeLists.txt`, runs the four Android builds plus `build-ios.sh`, stages `jniLibs/{arm64-v8a,armeabi-v7a,x86_64,x86}` and `build-ios/`, and tars the Android and iOS archives (new-release.sh:4821, release.sh:5223).

No Python function-level pipeline is described in the available pages; the pipeline surface is shell plus CMake.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `CMakeLists.txt` | 649 | Sole version source (`SHERPA_ONNX_VERSION "1.13.8"`) and all `SHERPA_ONNX_ENABLE_*` feature flags |
| `README.md` | 200+ (chunk) | Canonical function, platform, language, framework, and NPU support matrices |
| `build-android-arm64-v8a.sh` (+ armv7/x86-64/x86) | ~720 (chunk ref) | Android ABI builds; shared JNI + ONNX Runtime packaging |
| `build-ios.sh` (+ no-tts/shared variants) | ~2600 (chunk ref) | iOS simulator/device slices, lipo merge, xcframework assembly |
| `build-macos.sh` (+ shared variants) | ~3100 (chunk ref) | Universal macOS build, optional static archive merge |
| `build-ohos-arm64-v8a.sh` (+ armeabi/x86-64) | ~3300 (chunk ref) | HarmonyOS builds against OHOS toolchain and ORT 1.16.3 |
| `build-aarch64-linux-gnu.sh` / `build-arm-linux-gnueabihf.sh` | ~527 (chunk ref) | Embedded-Linux cross builds with alsa-lib and static default |
| `build-riscv64-linux-gnu.sh` / `build-riscv64-linux-gnu-spacemit.sh` | ~3681 (chunk ref) | RISC-V cross builds; SpacemiT backend flag |
| `build-rknn-linux-aarch64.sh` / `build-axera-linux-aarch64.sh` / `build-axcl-linux-aarch64.sh` | ~1500–3700 (chunk ref) | Vendor-NPU builds via RKNN/AXERA/AXCL SDK roots |
| `build-wasm-simd-*.sh` (9 tasks) + `build-flutter-web-wasm.sh` | ~1800–4400 (chunk ref) | Emscripten per-task WASM builds and Flutter web asset install |
| `OPENVINO.md` | 115 | Intel-NPU execution-provider usage and config-file syntax |
| `Package.swift` | 170 | SwiftPM static+shared products, exact `onnxruntime-libs` dependency, xcframework URLs |
| `new-release.sh` | 96 | Version-bump propagation across manifests and workflows |
| `release.sh` | 46 | Android+iOS rebuild and tarball staging |
| `sherpa-onnx/c-api/c-api.h` | n/a in chunk | C API header exported through iOS modulemap |
| `sherpa-onnx/csrc/version.cc` | n/a in chunk | Compiled version string updated by `new-release.sh` |
| `.clang-format` / `.clang-tidy` / `.flake8` / `CPPLINT.cfg` | 110 / 74 / small / small | Format and lint enforcement (Google style, warnings-as-errors, flake8 120) |
| `.gitignore` | 201 | Excludes build dirs, model blobs, audio, native artifacts |
| `jitpack.yml` / `MANIFEST.in` | 23 / 13 | JVM artifact install and Python sdist include/prune lists |
| `toolchains/` | n/a in chunk | CMake toolchain files for Linux-ARM, OHOS, RISC-V cross builds |

## 7. Dependencies

Required (build or runtime) first, with exact constraint strings as stated in the pages:

| Package | Version constraint | Purpose |
|---|---|---|
| ONNX Runtime (Android/iOS/macOS) | `1.28.2` (default via `SHERPA_ONNX_ONNXRUNTIME_VERSION`; `onnxruntime-libs` exact `1.28.2` in `Package.swift`) | Inference backend downloaded and linked per target |
| ONNX Runtime (HarmonyOS) | `1.16.3` | Inference backend for OHOS builds |
| ONNX Runtime (Linux ARM64 GPU) | `"1.11.0"` (`SHERPA_ONNX_LINUX_ARM64_GPU_ONNXRUNTIME_VERSION`) | CUDA/cuDNN-mapped GPU runtime for Linux ARM64 |
| ONNX Runtime with OpenVINO EP | `>= 1.17` (bundled runtime lacks it; must supply `SHERPA_ONNXRUNTIME_INCLUDE_DIR`/`LIB_DIR`) | Intel-NPU execution provider |
| CMake | `3.15` (minimum, `CMakeLists.txt`) | Build configuration |
| Emscripten SDK | `4.0.23` (`emsdk`) | WebAssembly compilation |
| alsa-lib | `v1.2.12` (cross-built in embedded-Linux scripts) | Audio input on embedded Linux |
| Rockchip RKNN Toolkit2 | path via `SHERPA_ONNX_RKNN_TOOLKIT2_PATH` (no numeric pin in chunk) | Rockchip NPU backend |
| Axera SDK / AxCL SDK | paths via `AXERA_SDK_ROOT` / `AXCL_SDK_ROOT` (no numeric pin in chunk) | Axera NPU backends |
| PortAudio | flag `SHERPA_ONNX_ENABLE_PORTAUDIO` default `ON` (no version pin in chunk) | Microphone support |
| Python bindings / flake8 | `SHERPA_ONNX_ENABLE_PYTHON` default `OFF`; flake8 `max-line-length = 120` | Optional Python API and lint |

Packaging and framework references (not linked libraries): Flutter and Tauri demo apps via `flutter` / `tauri` release tags (README.md:61-86); SwiftPM `iOS(.v15)` / `macOS(.v10_15)` targets; JVM AAR/JAR artifacts at `1.13.8` installed via `mvn install:install-file` (`jitpack.yml`); Python sdist include/prune list (`MANIFEST.in`).

## 8. CLI / Usage Surface

Entry points visible in the two pages:

| Entry | Form | Notes |
|---|---|---|
| Per-target shell builds | `build-android-*.sh`, `build-ios*.sh`, `build-macos*.sh`, `build-ohos-*.sh`, `build-aarch64/arm/riscv64*.sh`, `build-rknn/axera/axcl*.sh`, `build-wasm-simd-*.sh` | Each creates `build-<target>`, runs `cmake` + `make -j` + `make install/strip` |
| CLI binaries | enabled by `SHERPA_ONNX_ENABLE_BINARY` (on for top-level builds) | Binary names and flags are not enumerated in the available pages |
| Keyword-spotting invocation | `--provider=openvino`, `--vad-provider=openvino` | Selects OpenVINO execution provider; transducer KWS keeps decoder/joiner on CPU (OPENVINO.md:4950, OPENVINO.md:4996) |
| Provider config file | `provider:config-file <path>` with entries such as `device_type=NPU`, `enable_qdq_optimizer=True` | Optional local file controlling OpenVINO device selection |
| Language bindings | C++, C, Python, Go, C#, Java, Kotlin, JavaScript, Swift, Rust, Dart, Object Pascal, WebAssembly | Verbatim API list (README.md:141-146); binding source trees are outside the analyzed pages |
| Demo apps | Flutter and Tauri pre-built releases (`flutter-releases`, `tauri-releases` tags) | Matrices cover Android/iOS/Windows/macOS/Linux/Web subsets (README.md:63-81) |

Environment and CMake configuration:

| Variable / option | Default | Effect |
|---|---|---|
| `SHERPA_ONNX_ENABLE_PYTHON` | `OFF` (forces `BUILD_SHARED_LIBS=ON`) | Python bindings |
| `SHERPA_ONNX_ENABLE_C_API` | `ON` | C API library |
| `SHERPA_ONNX_ENABLE_WEBSOCKET` | `ON` | Websocket server/client |
| `SHERPA_ONNX_ENABLE_JNI` | `OFF` (auto-on for Android) | JNI interface |
| `SHERPA_ONNX_ENABLE_PORTAUDIO` | `ON` | Microphone support |
| `SHERPA_ONNX_ENABLE_GPU` / `DIRECTML` | `OFF` (force shared libs when on) | NVIDIA GPU / DirectML ORT support |
| `SHERPA_ONNX_ENABLE_TTS` / `SPEAKER_DIARIZATION` | `ON` | TTS and diarization code |
| `SHERPA_ONNX_ENABLE_BINARY` | on for top-level builds | CLI binaries |
| `SHERPA_ONNX_ENABLE_WASM*` (9 flags) | `OFF` | Exactly one `WASM_<TASK>` per WASM build |
| `SHERPA_ONNX_ENABLE_RKNN/AXERA/AXCL/ASCEND_NPU/QNN/SPACEMIT` | `OFF` | Vendor accelerator backends |
| `BUILD_SHARED_LIBS` | `OFF` (`ON` in Android/OHOS scripts) | Shared vs static libraries |
| `SHERPA_ONNX_ONNXRUNTIME_VERSION` | `1.28.2` | ORT download pin for Android/iOS/macOS |
| `SHERPA_ONNXRUNTIME_INCLUDE_DIR` / `LIB_DIR` | unset | Custom ORT (required for OpenVINO EP) with `SHERPA_ONNX_USE_PRE_INSTALLED_ONNXRUNTIME_IF_AVAILABLE=ON` |
| `SHERPA_ONNX_RKNN_TOOLKIT2_PATH` / `AXERA_SDK_ROOT` / `AXCL_SDK_ROOT` | unset | Vendor SDK roots for NPU builds |

## 9. Extensibility Points

- New accelerator backend: add a `SHERPA_ONNX_ENABLE_<VENDOR>` CMake option alongside the existing `RKNN/AXERA/AXCL/ASCEND_NPU/QNN/SPACEMIT` block (CMakeLists.txt:4575) and a matching `build-<vendor>-linux-aarch64.sh` modeled on `build-rknn-linux-aarch64.sh:3769`, threading the SDK root variable through `cmake`.
- New speech function: gate source with a `SHERPA_ONNX_ENABLE_<FUNCTION>` option following `SHERPA_ONNX_ENABLE_TTS` / `SPEAKER_DIARIZATION` (CMakeLists.txt:4569), and for browser delivery add a `SHERPA_ONNX_ENABLE_WASM_<TASK>` flag plus a `build-wasm-simd-<task>.sh` copy of `build-wasm-simd-asr.sh:3935`.
- New OS/ABI target: copy the closest `build-*.sh` (Android for NDK ABIs, `build-ios.sh:2631` for Apple slices, `build-ohos-arm64-v8a.sh:3190` for HarmonyOS, `build-aarch64-linux-gnu.sh:463` for embedded Linux) and adjust toolchain file, `ANDROID_ABI`/`OHOS_ARCH`/`CMAKE_OSX_ARCHITECTURES`, and `BUILD_SHARED_LIBS` default.
- New language binding or server shape: extend the C API surface rooted at `sherpa-onnx/c-api/c-api.h` (exported via the iOS `module.modulemap`) or the websocket server/client gated by `SHERPA_ONNX_ENABLE_WEBSOCKET` (CMakeLists.txt:4553); packaging follows `Package.swift:5042` for SwiftPM, `jitpack.yml:4769` for JVM, and `MANIFEST.in:4796` for Python sdist.
- New OpenVINO device behavior: no code change is needed for device selection; ship a `provider:config-file` (e.g. `device_type=NPU`) and pass `--provider=openvino` / `--vad-provider=openvino` (OPENVINO.md:4960).

## 10. Limitations and Gotchas

- **OpenVINO requires a custom ONNX Runtime build.** The bundled runtime lacks the OpenVINO execution provider; Intel-NPU use needs ORT 1.17+ built with that provider plus explicit `SHERPA_ONNXRUNTIME_INCLUDE_DIR`/`LIB_DIR` and `SHERPA_ONNX_USE_PRE_INSTALLED_ONNXRUNTIME_IF_AVAILABLE=ON` (OPENVINO.md:4911, OPENVINO.md:4930). Expect CPU fallback when the provider is absent (OPENVINO.md:4988).
- **One WASM task per build.** Each `build-wasm-simd-*.sh` enables `-DSHERPA_ONNX_ENABLE_WASM=ON` plus exactly one `SHERPA_ONNX_ENABLE_WASM_<TASK>`; there is no documented multi-task WASM binary in the analyzed pages, so each of ASR, KWS, TTS, VAD, VAD-ASR, NodeJS, web, diarization, and enhancement ships as a separate artifact (build-wasm-simd-asr.sh:3935, build-wasm-simd-web.sh:4485).
- **Android and embedded-Linux defaults diverge.** Android scripts default to `BUILD_SHARED_LIBS=ON` with JNI on and PortAudio off, while embedded-Linux scripts default to static with C API and websocket on (build-android-arm64-v8a.sh:563, build-aarch64-linux-gnu.sh:497, build-aarch64-linux-gnu.sh:527). Copying flags across targets without adjusting these defaults produces missing-symbol or missing-microphone failures.
- **Version is scattered by script.** `SHERPA_ONNX_VERSION "1.13.8"` originates in `CMakeLists.txt:4529` but is replicated by `sed -i.bak` into `version.cc`, gradle files, `build*.sh`, `pom.xml`, Swift/SPM, Flutter/Dart, HarmonyOS, and CI (new-release.sh:4812, new-release.sh:4821); a manual bump in one file alone leaves artifacts inconsistent.
- **Source coverage in these pages is partial.** The `CMakeLists.txt` chunk is truncated at line 4759 (11792 further characters cut) and the Android APK link table shows only the header with rows cut off (README.md:197-203), so claims about lower CMake logic and APK inventory cannot be grounded here.

## 11. How It Compares to Alternatives

The analyzed pages name component-level projects rather than end-to-end substitutes: ONNX Runtime as the shared inference backend (pinned at `1.28.2` / `1.16.3` / `1.11.0` with an OpenVINO-EP variant), `silero-vad` for VAD, `gtcrn` and `DPDFNet` for enhancement, `spleeter` and `UVR` for source separation, and Piper phonemize plus eSpeak-NG references in the disabled `BUILD_PIPER_PHONMIZE_*` / `BUILD_ESPEAK_NG_*` build flags (README.md:107, README.md:114-117, OPENVINO.md:4911, build-aarch64-linux-gnu.sh:417).

- **ONNX Runtime (Microsoft):** the execution engine sherpa-onnx builds on; using it directly gives full operator control but no speech-function packaging, language-binding matrix, or per-board scripts.
- **silero-vad / gtcrn / DPDFNet / spleeter / UVR:** single-task model projects named as the underlying techniques; each covers one function where sherpa-onnx bundles twelve behind one build and API surface.
- **Piper phonemize / eSpeak-NG (TTS front ends):** text-normalization and phonemization components referenced in the build; standalone use covers TTS preprocessing only, not recognition, diarization, or NPU-target packaging.
- **Flutter / Tauri (app frameworks):** the demo-app delivery layer with pre-built releases (README.md:61-86); they are UI shells around the sherpa-onnx libraries, not speech engines themselves.

Positioning: sherpa-onnx is the integration and distribution layer — pinned runtimes, per-target cross-compilation, multi-language bindings, and demo packaging — over single-task models and the ONNX Runtime backend, trading per-model novelty for offline portability across chips, operating systems, and language runtimes.

## Appendix: Selected Code Snippets

1. Top-level CMake version and feature toggles (`CMakeLists.txt`, excerpt via 02-top-level-files.md):

```
set(SHERPA_ONNX_VERSION "1.13.8")
option(SHERPA_ONNX_ENABLE_C_API "Whether to build C API" ON)
option(SHERPA_ONNX_ENABLE_WEBSOCKET "Whether to build webscoket server/client" ON)
```

2. Locally runnable function list (`README.md:105-117`, verbatim via 01-overview.md):

```
This repository supports running the following functions **locally**

  - Speech-to-text (i.e., ASR); both streaming and non-streaming are supported
  - Text-to-speech (i.e., TTS)
  - Speaker diarization
  - Speaker identification
  - Speaker verification
  - Spoken language identification
  - Audio tagging
  - VAD (e.g., [silero-vad][silero-vad])
  - Speech enhancement (e.g., [gtcrn][gtcrn], [DPDFNet](https://github.com/ceva-ip/DPDFNet))
  - Keyword spotting
  - Source separation (e.g., [spleeter][spleeter], [UVR][UVR])
```

3. Platform target list (`README.md:119-139`, verbatim via 01-overview.md):

```
  - x86, ``x86_64``, 32-bit ARM, 64-bit ARM (arm64, aarch64), RISC-V (riscv64), **RK NPU**, **Ascend NPU**
  - Linux, macOS, Windows, openKylin
  - Android, WearOS
  - iOS
  - HarmonyOS
  - NodeJS
  - WebAssembly
  - [NVIDIA Jetson Orin NX][NVIDIA Jetson Orin NX] (Support running on both CPU and GPU)
  - [NVIDIA Jetson Nano B01][NVIDIA Jetson Nano B01] (Support running on both CPU and GPU)
  - [Raspberry Pi][Raspberry Pi]
  - [RV1126][RV1126]
  - [LicheePi4A][LicheePi4A]
  - [VisionFive 2][VisionFive 2]
  - [旭日X3派][旭日X3派]
  - [爱芯派][爱芯派]
  - [RK3588][RK3588]
  - [SpacemiT-K1][SpacemiT-K1]
  - [SpacemiT-K3][SpacemiT-K3]
  - etc
```

4. OpenVINO provider usage note (`OPENVINO.md`, via 02-top-level-files.md): keyword spotting uses `--provider=openvino` and VAD uses `--vad-provider=openvino`, with optional `provider:config-file` files such as `device_type=NPU` / `enable_qdq_optimizer=True`; transducer KWS runs the encoder on OpenVINO and keeps decoder/joiner on CPU, falling back to CPU when OpenVINO is unavailable (OPENVINO.md:4950, OPENVINO.md:4960, OPENVINO.md:4988, OPENVINO.md:4996).
