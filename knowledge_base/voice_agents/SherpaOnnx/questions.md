---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: k2-fsa/sherpa-onnx

### Q1. Which speech functions does sherpa-onnx run locally?
> [!tip]- Answer
> It runs speech recognition (streaming and non-streaming), synthesis, source separation, speaker identification, diarization, and verification, plus spoken language identification, audio tagging, VAD, keyword spotting, punctuation, and speech enhancement. Named components include silero-vad for VAD, gtcrn and DPDFNet for enhancement, and spleeter and UVR for separation. The whole stack is local with no cloud dependency. See [[wiki/01-overview|Overview]].

### Q2. Which platforms, boards, and programming languages does sherpa-onnx target?
> [!tip]- Answer
> Architectures span x86/x86_64, 32-bit and 64-bit ARM, and RISC-V across Linux, macOS, Windows, openKylin, Android, WearOS, iOS, HarmonyOS, NodeJS, and WebAssembly. Named edge targets include Jetson Orin NX and Nano B01, Raspberry Pi, RK3588, RV1126, LicheePi4A, VisionFive 2, and SpacemiT-K1/K3. APIs cover C++, C, Python, Go, C#, Java, Kotlin, JavaScript, Swift, Rust, Dart, and Object Pascal. See [[wiki/01-overview|Overview]].

### Q3. What NPU backends and app-framework matrices does sherpa-onnx support?
> [!tip]- Answer
> Five NPU entries are supported: Rockchip (RKNN), Qualcomm (QNN), Ascend, Axera, and Intel via OpenVINO. Flutter and Tauri each have an architecture-by-OS support matrix with pre-built demo apps under flutter and tauri release tags. RISC-V appears as Linux-only in the platform matrix, and HuggingFace Spaces plus pre-built Android APKs let users try models before building. See [[wiki/01-overview|Overview]].

### Q4. How does the root CMakeLists.txt control what gets built?
> [!tip]- Answer
> It declares project(sherpa-onnx) with SHERPA_ONNX_VERSION "1.13.8" as the single version source. Feature selection runs through SHERPA_ONNX_ENABLE_* options for Python, tests, TTS, speaker diarization, C API, websocket, JNI, GPU, nine WASM variants, and RKNN/AXERA/AXCL/QNN/SPACEMIT backends, plus BUILD_SHARED_LIBS. Enabling Python or GPU forces shared libraries on, and JNI auto-enables on Android when neither JNI nor C API is set. See [[wiki/02-top-level-files|Top-level files]].

### Q5. What pattern do the per-target build scripts follow, and how do Android and embedded-Linux builds differ?
> [!tip]- Answer
> Each script creates its own build-<target> directory and runs cmake plus make and install/strip for one target: 4 Android ABIs, 4 iOS variants, 3 macOS variants, 3 HarmonyOS arches, embedded-Linux ARM/RISC-V, NPU boards, and 9 WASM/SIMD profiles. Android builds default to shared libraries producing libsherpa-onnx-jni.so plus libonnxruntime.so with PortAudio off, while embedded-Linux builds default to static with C API and websocket on. iOS and macOS scripts download a pinned ONNX Runtime (1.28.2) and assemble xcframework slices with a module map for the C API header. See [[wiki/02-top-level-files|Top-level files]].

### Q6. How are releases versioned and packaged, and how is Intel NPU execution configured?
> [!tip]- Answer
> new-release.sh bumps the version (1.13.7 to 1.13.8) and version code across CMake, version.cc, Android gradle files, build scripts, pom.xml, Swift/SPM, Flutter/Dart, HarmonyOS, and CI, while release.sh tars Android jniLibs and iOS outputs; Package.swift pins onnxruntime-libs 1.28.2 with static and shared products. Style is locked by Google-based .clang-format, strict clang-tidy with warnings as errors, flake8 max-line-length 120, and MANIFEST.in pruning mobile dirs from the sdist. Intel NPU use needs ONNX Runtime 1.17+ with the OpenVINO provider via --provider=openvino or --vad-provider=openvino plus provider:config-file entries like device_type=NPU, falling back to CPU otherwise. See [[wiki/02-top-level-files|Top-level files]].

### Q7. Would you recommend sherpa-onnx for a fully offline voice assistant on a low-power ARM Linux board, and why?
> [!tip]- Answer
> Yes, conditionally: the offline-first speech stack, static embedded-Linux builds with C API and websocket, ARM/RISC-V cross-compile scripts, 12-language API surface, and NPU options (RKNN, Axera, QNN) fit constrained edge deployment well. Caveats are verifying the exact SoC has a matching build script and NPU SDK, and that compact streaming models exist for the wanted languages. Pilot a small streaming ASR model plus silero VAD on the target board before committing. See [[wiki/02-top-level-files|Top-level files]].
