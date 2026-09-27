> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** sherpa-onnx is a library for running speech functions locally across many platforms, operating systems, and programming-language APIs.
## Key points
- Runs speech recognition, synthesis, source separation, speaker identification/diarization/verification, language identification, audio tagging, VAD, keyword spotting, punctuation, and speech enhancement locally (README.md:15-29, README.md:105-117).
- Supports streaming and non-streaming speech-to-text, naming silero-vad for VAD, gtcrn and DPDFNet for enhancement, and spleeter and UVR for source separation (README.md:107, README.md:114-117).
- Targets x86/x86_64, 32-bit ARM, 64-bit ARM (arm64, aarch64), RISC-V (riscv64), RK NPU, Ascend NPU, plus Linux, macOS, Windows, openKylin, Android, WearOS, iOS, HarmonyOS, NodeJS, and WebAssembly (README.md:121-127).
- Targets named edge boards and SoCs including NVIDIA Jetson Orin NX, Jetson Nano B01, Raspberry Pi, RV1126, LicheePi4A, VisionFive 2, 旭日X3派, 爱芯派, RK3588, SpacemiT-K1, and SpacemiT-K3 (README.md:128-138).
- Exposes APIs in C++, C, Python, Go, C#, Java, Kotlin, JavaScript, Swift, Rust, Dart, and Object Pascal, plus WebAssembly support (README.md:43-57, README.md:143-146).
- Ships Flutter and Tauri framework matrices with pre-built demo apps under flutter and tauri release tags (README.md:61-86).
- Supports Rockchip NPU (RKNN), Qualcomm NPU (QNN), Ascend NPU, Axera NPU, and Intel NPU via OpenVINO (README.md:90-98).
---
## Supported functions
Verbatim matrix from the chunk (README.md:13-29):

|Speech recognition| [Speech synthesis][tts-url] | [Source separation][ss-url] |
|------------------|------------------|-------------------|
|   ✔️              |         ✔️        |       ✔️           |

|Speaker identification| [Speaker diarization][sd-url] | Speaker verification |
|----------------------|-------------------- |------------------------|
|   ✔️                  |         ✔️           |            ✔️           |

| [Spoken Language identification][slid-url] | [Audio tagging][at-url] | [Voice activity detection][vad-url] |
|--------------------------------|---------------|--------------------------|
|                 ✔️              |          ✔️    |                ✔️         |

| [Keyword spotting][kws-url] | [Add punctuation][punct-url] | [Speech enhancement][se-url] |
|------------------|-----------------|--------------------|
|     ✔️            |       ✔️         |      ✔️             |

## Supported platforms
Verbatim matrix (README.md:34-40):

|Architecture| Android | iOS     | Windows    | macOS | linux | HarmonyOS |
|------------|---------|---------|------------|-------|-------|-----------|
|   x64      |  ✔️      |         |   ✔️      | ✔️    |  ✔️    |   ✔️   |
|   x86      |  ✔️      |         |   ✔️      |       |        |        |
|   arm64    |  ✔️      | ✔️      |   ✔️      | ✔️    |  ✔️    |   ✔️   |
|   arm32    |  ✔️      |         |           |       |  ✔️    |   ✔️   |
|   riscv64  |          |         |           |       |  ✔️    |        |

## Supported programming languages
Verbatim matrices plus WebAssembly note (README.md:42-57):

| 1. C++ | 2. C  | 3. Python | 4. JavaScript |
|--------|-------|-----------|---------------|
|   ✔️    | ✔️     | ✔️         |    ✔️          |

|5. Java | 6. C# | 7. Kotlin | 8. Swift |
|--------|-------|-----------|----------|
| ✔️      |  ✔️    | ✔️         |  ✔️       |

| 9. Go | 10. Dart | 11. Rust | 12. Pascal |
|-------|----------|----------|------------|
| ✔️     |  ✔️       |   ✔️      |    ✔️       |

`It also supports WebAssembly.`

## Supported frameworks
Flutter matrix (README.md:63-70):

|Architecture| Android | iOS     | Windows | macOS | Linux | Web |
|------------|---------|---------|---------|-------|-------|-----|
|   x64      |  ✔️      |         |  ✔️     | ✔️    |  ✔️    |  ✔️  |
|   x86      |  ✔️      |         |         |       |       |  ✔️  |
|   arm64    |  ✔️      |  ✔️     |  ✔️     | ✔️    |  ✔️    |  ✔️  |
|   arm32    |  ✔️      |         |         |       |       |  ✔️  |

`- Pre-built Flutter demo apps: [flutter releases][flutter-releases]`

Tauri matrix (README.md:74-81):

|Architecture| Android | iOS     | Windows | macOS | Linux |
|------------|---------|---------|---------|-------|-------|
|   x64      |  ✔️      |         |  ✔️     | ✔️    |  ✔️    |
|   x86      |  ✔️      |         |         |       |       |
|   arm64    |  ✔️      |  ✔️     |  ✔️     | ✔️    |  ✔️    |
|   arm32    |  ✔️      |         |         |       |       |

`- Pre-built Tauri demo apps: [tauri releases][tauri-releases]`

Link definitions verbatim (README.md:83-86):

```
[flutter-url]: https://flutter.dev
[tauri-url]: https://v2.tauri.app
[flutter-releases]: https://github.com/k2-fsa/sherpa-onnx/releases/tag/flutter
[tauri-releases]: https://github.com/k2-fsa/sherpa-onnx/releases/tag/tauri
```

## Supported NPUs
Verbatim matrices (README.md:90-96):

| [1. Rockchip NPU (RKNN)][rknpu-doc] | [2. Qualcomm NPU (QNN)][qnn-doc]  | [3. Ascend NPU][ascend-doc] |
|-------------------------------------|-----------------------------------|-----------------------------|
|     ✔️                              |                  ✔️               |     ✔️                      |

| [4. Axera NPU][axera-npu] | [5. Intel NPU (OpenVINO)][openvino-npu] |
|---------------------------|------------------------------------------|
|     ✔️                    |                    ✔️                    |

Verbatim (README.md:98, README.md:100):

```
[openvino-npu]: OPENVINO.md
[Join our discord](https://discord.gg/fJdxzg2VbG)
```

## Introduction: local functions, platforms, APIs
Verbatim list of local functions (README.md:105-117):

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

Verbatim platform list (README.md:119-139):

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

Verbatim API list (README.md:141-146):

```
with the following APIs

  - C++, C, Python, Go, ``C#``
  - Java, Kotlin, JavaScript
  - Swift, Rust
  - Dart, Object Pascal
```

## Huggingface Spaces and Android APK links
The chunk contains a `Links for Huggingface Spaces` details block listing browser-tryable spaces for speaker diarization, ASR, Whisper ASR, TTS, subtitles, audio tagging, source separation, and Whisper spoken-language identification (README.md:148-164), followed by a WebAssembly spaces table covering silero-vad VAD, Zipformer/Paraformer streaming ASR, VAD+ASR combos (Zipformer CTC, SenseVoice, Whisper tiny.en, Moonshine tiny, GigaSpeech, WenetSpeech, ReazonSpeech, GigaSpeech2, TeleSpeech-ASR, Paraformer-large/small, Dolphin-base), Matcha/Piper TTS, speaker diarization, and ZipVoice/Pocket voice cloning (README.md:165-194).
The chunk's `Links for pre-built Android APKs` section is truncated: it shows only the opening `<details>` block, the summary line `You can find pre-built Android APKs for this repository in the following table`, and the table header `| Description | URL` (README.md:197-203), then cuts off; the APK rows are not present so their contents are not described here.

**Covers:** README.md (repo root: supported functions, platforms, languages, Flutter/Tauri frameworks, NPUs, introduction, Huggingface Spaces links, truncated Android APK links)
