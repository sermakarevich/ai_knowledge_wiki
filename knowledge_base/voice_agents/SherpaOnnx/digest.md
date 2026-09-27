> [[index|Wiki]] | [[summary|Summary]]
# k2-fsa/sherpa-onnx — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** sherpa-onnx is a library for running speech functions locally across many platforms, operating systems, and programming-language APIs.
## Key points
- Runs speech recognition, synthesis, source separation, speaker identification/diarization/verification, language identification, audio tagging, VAD, keyword spotting, punctuation, and speech enhancement locally (README.md:15-29, README.md:105-117).
- Supports streaming and non-streaming speech-to-text, naming silero-vad for VAD, gtcrn and DPDFNet for enhancement, and spleeter and UVR for source separation (README.md:107, README.md:114-117).
- Targets x86/x86_64, 32-bit ARM, 64-bit ARM (arm64, aarch64), RISC-V (riscv64), RK NPU, Ascend NPU, plus Linux, macOS, Windows, openKylin, Android, WearOS, iOS, HarmonyOS, NodeJS, and WebAssembly (README.md:121-127).
- Targets named edge boards and SoCs including NVIDIA Jetson Orin NX, Jetson Nano B01, Raspberry Pi, RV1126, LicheePi4A, VisionFive 2, 旭日X3派, 爱芯派, RK3588, SpacemiT-K1, and SpacemiT-K3 (README.md:128-138).
- Exposes APIs in C++, C, Python, Go, C#, Java, Kotlin, JavaScript, Swift, Rust, Dart, and Object Pascal, plus WebAssembly support (README.md:43-57, README.md:143-146).
- Ships Flutter and Tauri framework matrices with pre-built demo apps under flutter and tauri release tags (README.md:61-86).
- Supports Rockchip NPU (RKNN), Qualcomm NPU (QNN), Ascend NPU, Axera NPU, and Intel NPU via OpenVINO (README.md:90-98).
## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** The repo root holds the build system, style configs, release tooling, and per-platform build scripts that compile the sherpa-onnx C/C++ core for every supported target.
## Key points
- The root `CMakeLists.txt` declares `project(sherpa-onnx)` and pins `SHERPA_ONNX_VERSION "1.13.8"` as the single version source (CMakeLists.txt:4524, CMakeLists.txt:4529).
- Feature selection is done entirely through `SHERPA_ONNX_ENABLE_*` CMake options (Python, tests, TTS, speaker diarization, C API, websocket, JNI, GPU, WASM variants, RKNN/AXERA/AXCL/QNN/SPACEMIT) plus `BUILD_SHARED_LIBS` (CMakeLists.txt:4546, CMakeLists.txt:4558).
- One shell script per target cross-compiles the same tree: 4 Android ABIs, 4 iOS variants, 3 macOS variants, 3 HarmonyOS (OHOS) arches, embedded-Linux ARM/RISC-V, RKNN/Axera/Axcl NPU boards, and 9 WASM/SIMD profiles (build-android-arm64-v8a.sh:546, build-ios.sh:2628, build-ohos-arm64-v8a.sh:3190, build-wasm-simd-asr.sh:3877).
- Android scripts default to `BUILD_SHARED_LIBS=ON` and produce `libsherpa-onnx-jni.so` plus `libonnxruntime.so`, while embedded-Linux scripts default to static (`BUILD_SHARED_LIBS=OFF`) with C API and websocket on (build-android-arm64-v8a.sh:563, build-aarch64-linux-gnu.sh:497, build-aarch64-linux-gnu.sh:527).
- iOS/macOS scripts download a pinned ONNX Runtime (`1.28.2` default), build simulator+device slices, and assemble `SherpaOnnxC.framework` / `sherpa-onnx.xcframework` with a `module.modulemap` for `sherpa-onnx/c-api/c-api.h` (build-ios.sh:2639, build-macos.sh:3084, build-ios-shared.sh:2560).
- Style and packaging are fixed at the root: Google-based `.clang-format`, `bugprone/cppcoreguidelines/modernize/performance` clang-tidy checks with `WarningsAsErrors: '*'`, flake8 `max-line-length = 120`, `Package.swift` static+shared products, and `new-release.sh`/`release.sh` version-bump and artifact logic (`.clang-format:10`, `.clang-tidy:195`, `.flake8:205`, Package.swift:5042, new-release.sh:4821).
- `OPENVINO.md` documents Intel-NPU execution via `--provider=openvino` / `--vad-provider=openvino` with `provider:config-file` syntax (e.g. `device_type=NPU`), falling back to CPU when OpenVINO is unavailable (OPENVINO.md:4946, OPENVINO.md:4972, OPENVINO.md:4988).
## The system in five moves
1. sherpa-onnx promises a full local speech stack — recognition, synthesis, diarization, enhancement, separation, VAD, and more — with no cloud dependency.
2. It makes that stack portable, covering desktop, mobile, embedded, edge boards, and WebAssembly across a dozen programming-language APIs.
3. It extends portability to accelerators, supporting Rockchip, Qualcomm, Ascend, Axera, and Intel NPUs alongside CPU/GPU builds.
4. A single CMake core with feature-flag options unifies all of this, with per-target shell scripts cross-compiling the same tree for Android, iOS, macOS, HarmonyOS, embedded Linux, and WASM profiles.
5. Root-level style configs, version-pinning, and release scripts lock the matrix together so one version number ships consistently everywhere.
