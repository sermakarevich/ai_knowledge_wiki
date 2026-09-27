> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Critical Analysis: k2-fsa/sherpa-onnx

## Claims vs. evidence

- **Claim: full local speech stack with no cloud dependency.** Supported by an
  explicit 12-function matrix (ASR streaming + non-streaming, TTS, diarization,
  identification, verification, language ID, audio tagging, VAD, KWS,
  punctuation, enhancement, separation) — all check-marked in the README.
- **Claim: runs everywhere.** Supported in unusual detail: 5-architecture
  platform matrix (x64/x86/arm64/arm32/riscv64 × Android/iOS/Windows/macOS/
  Linux/HarmonyOS), plus named boards (Jetson Orin NX/Nano, Raspberry Pi,
  RV1126, LicheePi4A, VisionFive 2, RK3588, SpacemiT-K1/K3), plus NodeJS and
  WebAssembly, plus Flutter/Tauri framework matrices with pre-built demo apps.
- **Claim: one core, every target.** Supported by the root `CMakeLists.txt`
  (single `SHERPA_ONNX_VERSION "1.13.8"`, `SHERPA_ONNX_ENABLE_*` feature flags)
  and ~33 per-target `build-*.sh` scripts (4 Android ABIs, 4 iOS variants,
  3 macOS, 3 HarmonyOS, embedded ARM/RISC-V, NPU boards, 9 WASM profiles).
- **Claim: NPU acceleration.** Partially supported: RKNN, QNN, Ascend, Axera,
  and Intel-via-OpenVINO matrices are check-marked, but OpenVINO needs
  ONNX Runtime ≥ 1.17 with the EP built in (bundled runtime lacks it) and KWS
  splits encoder (OpenVINO) from decoder/joiner (CPU) — acceleration is real
  but conditional, not drop-in.
- **Evidence gaps:** the covered material contains no accuracy, WER/MOS, or
  latency benchmarks; the Android APK table is truncated (header only, no rows);
  the `CMakeLists.txt` body is truncated mid-file; quality claims therefore
  rest on Hugging Face Spaces / WASM demo links, not on measured results.

## Genuinely new vs. repackaged

- **Repackaged:** the named models are third-party — silero-vad, gtcrn,
  DPDFNet, spleeter, UVR — and the WASM demo list (Zipformer, Paraformer,
  SenseVoice, Whisper, Moonshine, Matcha, Piper, ZipVoice) reads as a model
  zoo, not novel research. The inference engine is pinned ONNX Runtime
  (default `1.28.2`), not a new runtime.
- **Genuinely valuable integration:** the novelty is systems work, not models —
  one C/C++ core with a stable C API (`c-api.h` shipped as an xcframework
  module), 12 language bindings (C++ through Pascal), 9 WASM sub-builds,
  vendor NPU shims, and version-locked release tooling (`new-release.sh`
  bumps one version across CMake, Gradle, SPM, Flutter, HarmonyOS, CI).
- **Verdict on novelty:** thin as research, substantial as infrastructure — a
  portability and packaging layer over community models and ONNX Runtime.

## Weaknesses and blind spots

- **Breadth-vs-maintenance risk:** ~33 cross-compile scripts, per-ABI JNI
  outputs, lipo-merged xcframeworks, and separate Flutter/Tauri release tags
  imply a large test matrix; the digest shows style gates (clang-tidy as
  errors, flake8-120) but no test-coverage evidence (tests default `OFF`).
- **Runtime version skew:** iOS/macOS/SPM pin ONNX Runtime `1.28.2`, HarmonyOS
  scripts pin `1.16.3`, and the Linux-ARM64 GPU option defaults to `1.11.0` —
  three vintages in one release invites subtle behavioral drift.
- **Fragmented outputs:** 9 WASM single-task builds (ASR vs KWS vs TTS vs
  VAD-ASR …), static embedded builds vs shared Android builds, websocket
  on in some targets and off in macOS — consumers must pick the right slice.
- **NPU fine print:** each vendor backend needs its SDK root
  (`RKNN_TOOLKIT2_PATH`, `AXERA_SDK_ROOT`, …) and OpenVINO needs a custom
  runtime plus config files (`device_type=NPU`); "supports NPU" means
  "supports it if you bring the toolchain."
- **No quality story in scope:** no WER, diarization error rate, MOS, or
  latency numbers appear in the digest/wiki; model selection guidance and
  update cadence for the bundled third-party models are unstated.

## Applicability

- **Good fit:** offline/edge speech (kiosk, mobile, embedded Linux, RISC-V
  boards), privacy-sensitive transcription, keyword-spotting + VAD front ends,
  batch audio tagging/punctuation/enhancement pipelines, and browser-side
  demos via WASM without backend GPU spend.
- **Poor fit:** anyone needing SOTA accuracy guarantees, managed model
  updates, or a single `pip install` server experience — this is a native
  build matrix first, a Python package second (Python bindings default `OFF`).
- **Relevance to my work**
  - **AI/ML engineering:** fastest path to a local baseline for STT/TTS/VAD
    experiments; C API + pinned runtime make perf comparisons reproducible,
    but budget time for CMake/NPU toolchain friction and runtime skew.
  - **Agentic systems:** VAD + streaming ASR + KWS + TTS cover the voice loop
    (listen → transcribe → act → speak) fully on-device; attractive for
    low-latency voice agents, provided agent-side eval measures WER/latency
    since the repo supplies none.
  - **Elisity data platform:** on-prem audio preprocessing (VAD-gated
    transcription, diarization, tagging, enhancement) without shipping audio
    to the cloud fits data-governance constraints; the static embedded and
    websocket builds suit sidecar ingestion, but model provenance/versioning
    must be wrapped in platform-level controls.

## What this changes

- It collapses "which edge speech framework?" to a solved distribution
  problem: one version number, one C API, script-per-target builds from
  data-center GPU hosts down to RISC-V and WASM.
- It normalizes NPU execution as a build flag rather than a rewrite, even if
  each vendor still exacts a toolchain tax.
- It does not change the modeling frontier — progress here is measured in
  targets covered and bindings shipped, and evaluation burden shifts entirely
  to the adopter.

## Verdict

- Useful, unglamorous infrastructure: a broad, honest, well-tooled packaging
  layer over borrowed models, with real but conditional NPU support and no
  in-scope quality evidence.
- **trial** — prototype on-device STT/TTS/VAD against measured accuracy and
  latency before committing; do not adopt as a platform-wide speech standard
  until benchmarks and model-update policy are established.
