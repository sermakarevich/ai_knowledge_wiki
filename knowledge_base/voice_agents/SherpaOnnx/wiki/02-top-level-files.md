> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repo root holds the build system, style configs, release tooling, and per-platform build scripts that compile the sherpa-onnx C/C++ core for every supported target.
## Key points
- The root `CMakeLists.txt` declares `project(sherpa-onnx)` and pins `SHERPA_ONNX_VERSION "1.13.8"` as the single version source (CMakeLists.txt:4524, CMakeLists.txt:4529).
- Feature selection is done entirely through `SHERPA_ONNX_ENABLE_*` CMake options (Python, tests, TTS, speaker diarization, C API, websocket, JNI, GPU, WASM variants, RKNN/AXERA/AXCL/QNN/SPACEMIT) plus `BUILD_SHARED_LIBS` (CMakeLists.txt:4546, CMakeLists.txt:4558).
- One shell script per target cross-compiles the same tree: 4 Android ABIs, 4 iOS variants, 3 macOS variants, 3 HarmonyOS (OHOS) arches, embedded-Linux ARM/RISC-V, RKNN/Axera/Axcl NPU boards, and 9 WASM/SIMD profiles (build-android-arm64-v8a.sh:546, build-ios.sh:2628, build-ohos-arm64-v8a.sh:3190, build-wasm-simd-asr.sh:3877).
- Android scripts default to `BUILD_SHARED_LIBS=ON` and produce `libsherpa-onnx-jni.so` plus `libonnxruntime.so`, while embedded-Linux scripts default to static (`BUILD_SHARED_LIBS=OFF`) with C API and websocket on (build-android-arm64-v8a.sh:563, build-aarch64-linux-gnu.sh:497, build-aarch64-linux-gnu.sh:527).
- iOS/macOS scripts download a pinned ONNX Runtime (`1.28.2` default), build simulator+device slices, and assemble `SherpaOnnxC.framework` / `sherpa-onnx.xcframework` with a `module.modulemap` for `sherpa-onnx/c-api/c-api.h` (build-ios.sh:2639, build-macos.sh:3084, build-ios-shared.sh:2560).
- Style and packaging are fixed at the root: Google-based `.clang-format`, `bugprone/cppcoreguidelines/modernize/performance` clang-tidy checks with `WarningsAsErrors: '*'`, flake8 `max-line-length = 120`, `Package.swift` static+shared products, and `new-release.sh`/`release.sh` version-bump and artifact logic (`.clang-format:10`, `.clang-tidy:195`, `.flake8:205`, Package.swift:5042, new-release.sh:4821).
- `OPENVINO.md` documents Intel-NPU execution via `--provider=openvino` / `--vad-provider=openvino` with `provider:config-file` syntax (e.g. `device_type=NPU`), falling back to CPU when OpenVINO is unavailable (OPENVINO.md:4946, OPENVINO.md:4972, OPENVINO.md:4988).
---
## Lint and format configs
Style is enforced by three small root configs, quoted verbatim (`.clang-format:6`, `.clang-tidy:121`, `.flake8:199`, `CPPLINT.cfg:4763`):

```
BasedOnStyle: Google          # .clang-format
```
```
Checks: 'bugprone-*, cppcoreguidelines-*, modernize-*, performance-*, ...'
WarningsAsErrors: '*'         # .clang-tidy
```
```
[flake8]
max-line-length = 120         # .flake8
```
```
filter=-./mfc-examples        # CPPLINT.cfg
```

- `.clang-format` (110 lines) sets C++ `Standard: c++17`, `IndentWidth: 4`, `TabWidth: 4`, `UseTab: Never`, `PointerAlignment: Right`, plus a Java section with `JavaImportGroups: [ 'java', 'javax', 'javafx', 'org', 'io', 'com', 'de.gsi' ]` (`.clang-format:19`, `.clang-format:81`, `.clang-format:101`).
- `.clang-tidy` (74 lines) enables `bugprone-*`, `cppcoreguidelines-*`, `hicpp-exception-baseclass`, `hicpp-avoid-goto`, `misc-*`, `modernize-*`, `performance-*` with a subtraction list (e.g. `-bugprone-easily-swappable-parameters`, `-modernize-use-auto`, `-misc-unused-parameters`) and `WarningsAsErrors: '*'` (`.clang-tidy:133`, `.clang-tidy:195`).
- `.gitignore` (201 lines) excludes build outputs (`build`, `build-*`), model blobs (`*.onnx`, `*.pt`, `sherpa-onnx-*`, `*.rknn`), audio (`*.wav`, `*.mp3`), and native artifacts (`*.so`, `*.dylib`, `*.dll`, `*.a`, `*.o`) (`.gitignore:212`, `.gitignore:254`).

## Top-level CMake configuration
`CMakeLists.txt` (649 lines; body truncated in chunk at `CMakeLists.txt:4759` — 11792 further characters cut, so claims below cover only the visible portion) requires CMake 3.15, sets `project(sherpa-onnx)`, and defaults an empty `CMAKE_BUILD_TYPE` to Release with `CMAKE_*_OUTPUT_DIRECTORY` under the build dir (`CMakeLists.txt:4503`, `CMakeLists.txt:4524`, `CMakeLists.txt:4633`).

| CMake option | Default | Meaning in chunk |
|---|---|---|
| `SHERPA_ONNX_ENABLE_PYTHON` | `OFF` | Build Python bindings; forces `BUILD_SHARED_LIBS=ON` when enabled (CMakeLists.txt:4546, CMakeLists.txt:4666) |
| `SHERPA_ONNX_ENABLE_TESTS` / `SHERPA_ONNX_ENABLE_CHECK` | `OFF` | Build tests / assert checks (CMakeLists.txt:4547) |
| `BUILD_SHARED_LIBS` | `OFF` | Shared vs static libraries (CMakeLists.txt:4549) |
| `SHERPA_ONNX_ENABLE_PORTAUDIO` | `ON` | Microphone support via PortAudio (CMakeLists.txt:4550) |
| `SHERPA_ONNX_ENABLE_JNI` | `OFF` | JNI interface; auto-enabled for Android when neither JNI nor C API is set (CMakeLists.txt:4551, CMakeLists.txt:4661) |
| `SHERPA_ONNX_ENABLE_C_API` | `ON` | C API library (CMakeLists.txt:4552) |
| `SHERPA_ONNX_ENABLE_WEBSOCKET` | `ON` | Websocket server/client (CMakeLists.txt:4553) |
| `SHERPA_ONNX_ENABLE_GPU` / `SHERPA_ONNX_ENABLE_DIRECTML` | `OFF` | NVIDIA GPU / DirectML ONNX Runtime support; force shared libs when on (CMakeLists.txt:4554, CMakeLists.txt:4671) |
| `SHERPA_ONNX_ENABLE_WASM*` (9 flags: `WASM`, `WASM_ASR/KWS/VAD/VAD_ASR/TTS/NODEJS/WEB/SPEAKER_DIARIZATION/SPEECH_ENHANCEMENT`) | `OFF` | Select WebAssembly sub-builds (CMakeLists.txt:4558) |
| `SHERPA_ONNX_ENABLE_BINARY` | on for top-level builds | Build CLI binaries (CMakeLists.txt:4568) |
| `SHERPA_ONNX_ENABLE_TTS` / `SHERPA_ONNX_ENABLE_SPEAKER_DIARIZATION` | `ON` | TTS and diarization code (CMakeLists.txt:4569) |
| `SHERPA_ONNX_ENABLE_RKNN/AXERA/AXCL/ASCEND_NPU/QNN/SPACEMIT` | `OFF` | NPU/CPU-vendor backends (CMakeLists.txt:4575) |
| `SHERPA_ONNX_LINUX_ARM64_GPU_ONNXRUNTIME_VERSION` | `"1.11.0"` | Pinned GPU runtime for Linux ARM64 (CUDA/cuDNN mapping in help string) (CMakeLists.txt:4581) |
| `SHERPA_ONNX_USE_STATIC_CRT` | `ON` | Windows `/MT` vs `/MD` runtime selection (CMakeLists.txt:4586) |

Verbatim excerpts:
```
set(SHERPA_ONNX_VERSION "1.13.8")
option(SHERPA_ONNX_ENABLE_C_API "Whether to build C API" ON)
option(SHERPA_ONNX_ENABLE_WEBSOCKET "Whether to build webscoket server/client" ON)
```

## Build scripts by platform
The chunk contains 33 `build-*.sh` scripts plus `build-flutter-web-wasm.sh`; each creates its own `build-<target>` dir, runs `cmake` + `make -j` + `make install/strip`, and disables `BUILD_PIPER_PHONMIZE_*` / `BUILD_ESPEAK_NG_*` exes and tests (build-aarch64-linux-gnu.sh:417, build-wasm-simd-asr.sh:3877).

| Script(s) | Target pattern (verbatim flags) |
|---|---|
| `build-aarch64-linux-gnu.sh`, `build-arm-linux-gnueabihf.sh` | Cross-compile with `aarch64-linux-gnu-gcc` / `arm-linux-gnueabihf-gcc`, cross-build `alsa-lib v1.2.12`, `-DSHERPA_ONNX_ENABLE_PORTAUDIO=ON -DSHERPA_ONNX_ENABLE_C_API=ON -DSHERPA_ONNX_ENABLE_WEBSOCKET=ON` via `toolchains/aarch64-linux-gnu.toolchain.cmake` (build-aarch64-linux-gnu.sh:463, build-aarch64-linux-gnu.sh:517) |
| `build-android-arm64-v8a.sh`, `build-android-armv7-eabi.sh`, `build-android-x86-64.sh`, `build-android-x86.sh` | `ANDROID_ABI arm64-v8a / armeabi-v7a / x86_64 / x86`, default `BUILD_SHARED_LIBS=ON`, ONNX Runtime default `1.28.2` via `SHERPA_ONNX_ONNXRUNTIME_VERSION`, `-DSHERPA_ONNX_ENABLE_JNI=ON -DSHERPA_ONNX_ENABLE_PORTAUDIO=OFF`, output `libsherpa-onnx-jni.so` + copied `libonnxruntime.so` (build-android-arm64-v8a.sh:641, build-android-arm64-v8a.sh:720) |
| `build-ios.sh`, `build-ios-no-tts.sh`, `build-ios-shared.sh`, `build-ios-shared-sherpa-with-static-onnxruntime.sh` | Triple builds `SIMULATOR64 / SIMULATORARM64 / OS64` with `DEPLOYMENT_TARGET=13.0`, `ENABLE_ARC=1`, `ENABLE_BITCODE=0`; `lipo` + `libtool -static` merge then `xcodebuild -create-xcframework` as `SherpaOnnxC.framework` (build-ios.sh:2631, build-ios-no-tts.sh:1888, build-ios-shared.sh:2387) |
| `build-macos.sh`, `build-macos-shared.sh`, `build-macos-shared-sherpa-with-static-onnxruntime.sh` | Universal `CMAKE_OSX_ARCHITECTURES="arm64;x86_64"`, `-DSHERPA_ONNX_ENABLE_WEBSOCKET=OFF`; static variant merges archives with `libtool -static -o install/lib/libsherpa-onnx.a` (build-macos.sh:3073, build-macos.sh:3104) |
| `build-ohos-arm64-v8a.sh`, `build-ohos-armeabi-v7a.sh`, `build-ohos-x86-64.sh` | HarmonyOS via `ohos.toolchain.cmake`, ONNX Runtime `1.16.3`, `-DOHOS_ARCH=arm64-v8a / armeabi-v7a / x86_64`, shared libs with C API on (build-ohos-arm64-v8a.sh:3190, build-ohos-arm64-v8a.sh:3302) |
| `build-riscv64-linux-gnu.sh`, `build-riscv64-linux-gnu-spacemit.sh` | `riscv64-unknown-linux-gnu-gcc` + `toolchains/riscv64-linux-gnu*.toolchain.cmake`; SpacemiT variant adds `-DSHERPA_ONNX_ENABLE_SPACEMIT=ON` (build-riscv64-linux-gnu-spacemit.sh:3615, build-riscv64-linux-gnu-spacemit.sh:3681) |
| `build-rknn-linux-aarch64.sh`, `build-axera-linux-aarch64.sh` (`ax650/ax630c/ax620q`), `build-axcl-linux-aarch64.sh` | Vendor SDK roots (`SHERPA_ONNX_RKNN_TOOLKIT2_PATH`, `AXERA_SDK_ROOT`, `AXCL_SDK_ROOT`) with `-DSHERPA_ONNX_ENABLE_RKNN=ON / AXERA=ON / AXCL=ON` (build-rknn-linux-aarch64.sh:3769, build-axera-linux-aarch64.sh:1658, build-axcl-linux-aarch64.sh:1522) |
| `build-wasm-simd-{asr,kws,tts,vad,vad-asr,nodejs,web,speaker-diarization,speech-enhancement}.sh` | Emscripten (`emsdk 4.0.23`), `-DSHERPA_ONNX_ENABLE_WASM=ON` plus exactly one `SHERPA_ONNX_ENABLE_WASM_<TASK>=ON` (e.g. `WASM_ASR`, `WASM_TTS`, `WASM_WEB`); `build-flutter-web-wasm.sh` copies `sherpa-onnx-wasm-web.js/.wasm` into `flutter/sherpa_onnx_web/assets/` and symlinks the JS wrappers (build-wasm-simd-asr.sh:3935, build-wasm-simd-web.sh:4485, build-flutter-web-wasm.sh:1846) |

## Release, versioning, and packaging
- `new-release.sh` (96 lines) bumps `old_version 1.13.7 → new_version 1.13.8` and `old_version_code 20260901 → new_version_code 20260910` across `CMakeLists.txt`, `sherpa-onnx/csrc/version.cc`, Android gradle files, `build*.sh`, `pom.xml`, Swift/SPM, Flutter/Dart, HarmonyOS, and CI workflows via `sed -i.bak` (new-release.sh:4812, new-release.sh:4821).
- `release.sh` (46 lines) reads the version with `grep "SHERPA_ONNX_VERSION" ./CMakeLists.txt`, runs the four Android builds plus `build-ios.sh`, then stages `jniLibs/{arm64-v8a,armeabi-v7a,x86_64,x86}` and `build-ios/` and tars `sherpa-onnx-v<V>-android.tar.bz2` and `sherpa-onnx-v<V>-ios.tar.bz2` (release.sh:5204, release.sh:5223).
- `Package.swift` (170 lines) targets `iOS(.v15)` / `macOS(.v10_15)`, depends on `onnxruntime-libs` exact `1.28.2`, and exposes `sherpa-onnx` (static) and `sherpa-onnx-shared` products backed by versioned `xcframework` zip URLs with checksums (Package.swift:5030, Package.swift:5042, Package.swift:5049).
- `jitpack.yml` (23 lines) pre-installs the `1.13.8` AAR plus JVM and five native-lib jars, then `mvn install:install-file` for each artifact (jitpack.yml:4769, jitpack.yml:4786).
- `MANIFEST.in` (13 lines) includes `LICENSE`, `README.md`, `CMakeLists.txt`, `c-api-examples`, `sherpa-onnx`, and `cmake`, while pruning `android`, `sherpa-onnx/java-api`, `ios-swift`, and `ios-swiftui` (MANIFEST.in:4796, MANIFEST.in:4806).

## Intel NPU note (OPENVINO.md)
`OPENVINO.md` (115 lines) requires ONNX Runtime ≥ 1.17 built with the OpenVINO Execution Provider (the bundled runtime lacks it) and builds with `SHERPA_ONNXRUNTIME_INCLUDE_DIR/LIB_DIR` plus `-DSHERPA_ONNX_USE_PRE_INSTALLED_ONNXRUNTIME_IF_AVAILABLE=ON` (OPENVINO.md:4911, OPENVINO.md:4930). Usage is `--provider=openvino` for keyword spotting and `--vad-provider=openvino` for VAD, with optional `provider:config-file` files such as `device_type=NPU` / `enable_qdq_optimizer=True`; transducer KWS runs the encoder on OpenVINO and keeps decoder/joiner on CPU (OPENVINO.md:4950, OPENVINO.md:4960, OPENVINO.md:4996).

**Covers:** `.clang-format`, `.clang-tidy`, `.flake8`, `.gitignore`, `CPPLINT.cfg`, `CMakeLists.txt` (visible part only; truncated at chunk line 4759), `build-aarch64-linux-gnu.sh`, `build-android-{arm64-v8a,armv7-eabi,x86-64,x86}.sh`, `build-arm-linux-gnueabihf.sh`, `build-axcl-linux-aarch64.sh`, `build-axera-linux-aarch64.sh`, `build-flutter-web-wasm.sh`, `build-ios{,-no-tts,-shared,-shared-sherpa-with-static-onnxruntime}.sh`, `build-macos{,-shared,-shared-sherpa-with-static-onnxruntime}.sh`, `build-ohos-{arm64-v8a,armeabi-v7a,x86-64}.sh`, `build-riscv64-linux-gnu{,-spacemit}.sh`, `build-rknn-linux-aarch64.sh`, `build-wasm-simd-{asr,kws,nodejs,speaker-diarization,speech-enhancement,tts,vad,vad-asr,web}.sh`, `jitpack.yml`, `MANIFEST.in`, `new-release.sh`, `OPENVINO.md`, `Package.swift`, `release.sh`
