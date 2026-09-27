> PDF location (no local PDF archived): https://github.com/k2-fsa/sherpa-onnx
# k2-fsa/sherpa-onnx
Source: https://github.com/k2-fsa/sherpa-onnx
Kind: repo
Fetched: 2026-09-22T14:42:11.571338+00:00
Tool: git-clone

# k2-fsa/sherpa-onnx

Commit: 040afe360a38e25daaa325ce8889abf93ea02609

## README

<div align="center">

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/k2-fsa/sherpa-onnx)

</div>

 ### Supported functions

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


### Supported platforms

|Architecture| Android | iOS     | Windows    | macOS | linux | HarmonyOS |
|------------|---------|---------|------------|-------|-------|-----------|
|   x64      |  ✔️      |         |   ✔️      | ✔️    |  ✔️    |   ✔️   |
|   x86      |  ✔️      |         |   ✔️      |       |        |        |
|   arm64    |  ✔️      | ✔️      |   ✔️      | ✔️    |  ✔️    |   ✔️   |
|   arm32    |  ✔️      |         |           |       |  ✔️    |   ✔️   |
|   riscv64  |          |         |           |       |  ✔️    |        |

### Supported programming languages

| 1. C++ | 2. C  | 3. Python | 4. JavaScript |
|--------|-------|-----------|---------------|
|   ✔️    | ✔️     | ✔️         |    ✔️          |

|5. Java | 6. C# | 7. Kotlin | 8. Swift |
|--------|-------|-----------|----------|
| ✔️      |  ✔️    | ✔️         |  ✔️       |

| 9. Go | 10. Dart | 11. Rust | 12. Pascal |
|-------|----------|----------|------------|
| ✔️     |  ✔️       |   ✔️      |    ✔️       |


It also supports WebAssembly.

### Supported frameworks

#### [Flutter][flutter-url]

|Architecture| Android | iOS     | Windows | macOS | Linux | Web |
|------------|---------|---------|---------|-------|-------|-----|
|   x64      |  ✔️      |         |  ✔️     | ✔️    |  ✔️    |  ✔️  |
|   x86      |  ✔️      |         |         |       |       |  ✔️  |
|   arm64    |  ✔️      |  ✔️     |  ✔️     | ✔️    |  ✔️    |  ✔️  |
|   arm32    |  ✔️      |         |         |       |       |  ✔️  |

- Pre-built Flutter demo apps: [flutter releases][flutter-releases]

#### [Tauri][tauri-url]

|Architecture| Android | iOS     | Windows | macOS | Linux |
|------------|---------|---------|---------|-------|-------|
|   x64      |  ✔️      |         |  ✔️     | ✔️    |  ✔️    |
|   x86      |  ✔️      |         |         |       |       |
|   arm64    |  ✔️      |  ✔️     |  ✔️     | ✔️    |  ✔️    |
|   arm32    |  ✔️      |         |         |       |       |

- Pre-built Tauri demo apps: [tauri releases][tauri-releases]

[flutter-url]: https://flutter.dev
[tauri-url]: https://v2.tauri.app
[flutter-releases]: https://github.com/k2-fsa/sherpa-onnx/releases/tag/flutter
[tauri-releases]: https://github.com/k2-fsa/sherpa-onnx/releases/tag/tauri

### Supported NPUs

| [1. Rockchip NPU (RKNN)][rknpu-doc] | [2. Qualcomm NPU (QNN)][qnn-doc]  | [3. Ascend NPU][ascend-doc] |
|-------------------------------------|-----------------------------------|-----------------------------|
|     ✔️                              |                  ✔️               |     ✔️                      |

| [4. Axera NPU][axera-npu] | [5. Intel NPU (OpenVINO)][openvino-npu] |
|---------------------------|------------------------------------------|
|     ✔️                    |                    ✔️                    |

[openvino-npu]: OPENVINO.md

[Join our discord](https://discord.gg/fJdxzg2VbG)


## Introduction

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

on the following platforms and operating systems:

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

with the following APIs

  - C++, C, Python, Go, ``C#``
  - Java, Kotlin, JavaScript
  - Swift, Rust
  - Dart, Object Pascal

### Links for Huggingface Spaces

<details>
<summary>You can visit the following Huggingface spaces to try sherpa-onnx without
installing anything. All you need is a browser.</summary>

| Description                                           | URL                                     | 中国镜像                               |
|-------------------------------------------------------|-----------------------------------------|----------------------------------------|
| Speaker diarization                                   | [Click me][hf-space-speaker-diarization]| [镜像][hf-space-speaker-diarization-cn]|
| Speech recognition                                    | [Click me][hf-space-asr]                | [镜像][hf-space-asr-cn]                |
| Speech recognition with [Whisper][Whisper]            | [Click me][hf-space-asr-whisper]        | [镜像][hf-space-asr-whisper-cn]        |
| Speech synthesis                                      | [Click me][hf-space-tts]                | [镜像][hf-space-tts-cn]                |
| Generate subtitles                                    | [Click me][hf-space-subtitle]           | [镜像][hf-space-subtitle-cn]           |
| Audio tagging                                         | [Click me][hf-space-audio-tagging]      | [镜像][hf-space-audio-tagging-cn]      |
| Source separation                                     | [Click me][hf-space-source-separation]  | [镜像][hf-space-source-separation-cn]  |
| Spoken language identification with [Whisper][Whisper]| [Click me][hf-space-slid-whisper]       | [镜像][hf-space-slid-whisper-cn]       |

We also have spaces built using WebAssembly. They are listed below:

| Description                                                                              | Huggingface space| ModelScope space|
|------------------------------------------------------------------------------------------|------------------|-----------------|
|Voice activity detection with [silero-vad][silero-vad]                                    | [Click me][wasm-hf-vad]|[地址][wasm-ms-vad]|
|Real-time speech recognition (Chinese + English) with Zipformer                           | [Click me][wasm-hf-streaming-asr-zh-en-zipformer]|[地址][wasm-hf-streaming-asr-zh-en-zipformer]|
|Real-time speech recognition (Chinese + English) with Paraformer                          |[Click me][wasm-hf-streaming-asr-zh-en-paraformer]| [地址][wasm-ms-streaming-asr-zh-en-paraformer]|
|Real-time speech recognition (Chinese + English + Cantonese) with [Paraformer-large][Paraformer-large]|[Click me][wasm-hf-streaming-asr-zh-en-yue-paraformer]| [地址][wasm-ms-streaming-asr-zh-en-yue-paraformer]|
|Real-time speech recognition (English) |[Click me][wasm-hf-streaming-asr-en-zipformer]    |[地址][wasm-ms-streaming-asr-en-zipformer]|
|VAD + speech recognition (Chinese) with [Zipformer CTC](https://k2-fsa.github.io/sherpa/onnx/pretrained_models/offline-ctc/icefall/zipformer.html#sherpa-onnx-zipformer-ctc-zh-int8-2025-07-03-chinese)|[Click me][wasm-hf-vad-asr-zh-zipformer-ctc-07-03]| [地址][wasm-ms-vad-asr-zh-zipformer-ctc-07-03]|
|VAD + speech recognition (Chinese + English + Korean + Japanese + Cantonese) with [SenseVoice][SenseVoice]|[Click me][wasm-hf-vad-asr-zh-en-ko-ja-yue-sense-voice]| [地址][wasm-ms-vad-asr-zh-en-ko-ja-yue-sense-voice]|
|VAD + speech recognition (English) with [Whisper][Whisper] tiny.en|[Click me][wasm-hf-vad-asr-en-whisper-tiny-en]| [地址][wasm-ms-vad-asr-en-whisper-tiny-en]|
|VAD + speech recognition (English) with [Moonshine tiny][Moonshine tiny]|[Click me][wasm-hf-vad-asr-en-moonshine-tiny-en]| [地址][wasm-ms-vad-asr-en-moonshine-tiny-en]|
|VAD + speech recognition (English) with Zipformer trained with [GigaSpeech][GigaSpeech]    |[Click me][wasm-hf-vad-asr-en-zipformer-gigaspeech]| [地址][wasm-ms-vad-asr-en-zipformer-gigaspeech]|
|VAD + speech recognition (Chinese) with Zipformer trained with [WenetSpeech][WenetSpeech]  |[Click me][wasm-hf-vad-asr-zh-zipformer-wenetspeech]| [地址][wasm-ms-vad-asr-zh-zipformer-wenetspeech]|
|VAD + speech recognition (Japanese) with Zipformer trained with [ReazonSpeech][ReazonSpeech]|[Click me][wasm-hf-vad-asr-ja-zipformer-reazonspeech]| [地址][wasm-ms-vad-asr-ja-zipformer-reazonspeech]|
|VAD + speech recognition (Thai) with Zipformer trained with [GigaSpeech2][GigaSpeech2]      |[Click me][wasm-hf-vad-asr-th-zipformer-gigaspeech2]| [地址][wasm-ms-vad-asr-th-zipformer-gigaspeech2]|
|VAD + speech recognition (Chinese 多种方言) with a [TeleSpeech-ASR][TeleSpeech-ASR] CTC model|[Click me][wasm-hf-vad-asr-zh-telespeech]| [地址][wasm-ms-vad-asr-zh-telespeech]|
|VAD + speech recognition (English + Chinese, 及多种中文方言) with Paraformer-large          |[Click me][wasm-hf-vad-asr-zh-en-paraformer-large]| [地址][wasm-ms-vad-asr-zh-en-paraformer-large]|
|VAD + speech recognition (English + Chinese, 及多种中文方言) with Paraformer-small          |[Click me][wasm-hf-vad-asr-zh-en-paraformer-small]| [地址][wasm-ms-vad-asr-zh-en-paraformer-small]|
|VAD + speech recognition (多语种及多种中文方言) with [Dolphin][Dolphin]-base          |[Click me][wasm-hf-vad-asr-multi-lang-dolphin-base]| [地址][wasm-ms-vad-asr-multi-lang-dolphin-base]|
|Speech synthesis (Piper, English)                                                                  |[Click me][wasm-hf-tts-piper-en]| [地址][wasm-ms-tts-piper-en]|
|Speech synthesis (Piper, German)                                                                   |[Click me][wasm-hf-tts-piper-de]| [地址][wasm-ms-tts-piper-de]|
|Speech synthesis (Matcha, Chinese)                                                                  |[Click me][wasm-hf-tts-matcha-zh]| [地址][wasm-ms-tts-matcha-zh]|
|Speech synthesis (Matcha, English)                                                                  |[Click me][wasm-hf-tts-matcha-en]| [地址][wasm-ms-tts-matcha-en]|
|Speech synthesis (Matcha, Chinese+English)                                                          |[Click me][wasm-hf-tts-matcha-zh-en]| [地址][wasm-ms-tts-matcha-zh-en]|
|Speaker diarization                                                                         |[Click me][wasm-hf-speaker-diarization]|[地址][wasm-ms-speaker-diarization]|
|Voice cloning with ZipVoice (Chinese+English)                                               |[Click me][wasm-hf-voice-cloning-zipvoice]|[地址][wasm-ms-voice-cloning-zipvoice]|
|Voice cloning with Pocket TTS (English)                                               |[Click me][wasm-hf-voice-cloning-pocket]|[地址][wasm-ms-voice-cloning-pocket]|

</details>

### Links for pre-built Android APKs

<details>

<summary>You can find pre-built Android APKs for this repository in the following table</summary>

| Description                            | URL                         

... (truncated, 40045 more characters)

## pom.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.k2fsa.sherpa.onnx</groupId>
    <artifactId>sherpa-onnx-android</artifactId>
    <version>1.13.8</version>
    <url>https://github.com/k2-fsa/sherpa-onnx</url>
    <packaging>pom</packaging>
    <description>First Android Library</description>

    <licenses>
      <license>
        <name>The Apache Software License, Version 2.0</name>
        <url>http://www.apache.org/licenses/LICENSE-2.0.txt</url>
        <distribution>repo</distribution>
      </license>
    </licenses>
</project>

```

## setup.py

```
#!/usr/bin/env python3

import os
import re
from pathlib import Path

import setuptools

from cmake.cmake_extension import (
    BuildExtension,
    bdist_wheel,
    cmake_extension,
    get_binaries,
    is_windows,
    need_split_package,
)


def read_long_description():
    with open("README.md", encoding="utf8") as f:
        readme = f.read()
    return readme


def get_package_version():
    with open("CMakeLists.txt") as f:
        content = f.read()

    match = re.search(r"set\(SHERPA_ONNX_VERSION (.*)\)", content)
    latest_version = match.group(1).strip('"')

    cmake_args = os.environ.get("SHERPA_ONNX_CMAKE_ARGS", "")
    extra_version = ""
    if "-DSHERPA_ONNX_ENABLE_GPU=ON" in cmake_args:
        extra_version = "+cuda"

    cuda_version = os.environ.get("SHERPA_ONNX_CUDA_VERSION", "")
    if cuda_version:
        extra_version += cuda_version

    latest_version += extra_version

    return latest_version


package_name = "sherpa_onnx"

with open("sherpa-onnx/python/sherpa_onnx/__init__.py", "a") as f:
    f.write(f"__version__ = '{get_package_version()}'\n")


def get_binaries_to_install():
    if need_split_package():
        return None

    cmake_args = os.environ.get("SHERPA_ONNX_CMAKE_ARGS", "")
    if "-DSHERPA_ONNX_ENABLE_BINARY=OFF" in cmake_args:
        return None

    bin_dir = Path("build") / "sherpa_onnx" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".exe" if is_windows() else ""

    binaries = get_binaries()

    exe = []
    for f in binaries:
        suffix = "" if (".dll" in f or ".lib" in f) else suffix
        t = bin_dir / (f + suffix)
        exe.append(str(t))
    return exe


setuptools.setup(
    name=package_name,
    python_requires=">=3.7",
    version=get_package_version(),
    author="The sherpa-onnx development team",
    author_email="dpovey@gmail.com",
    package_dir={
        "sherpa_onnx": "sherpa-onnx/python/sherpa_onnx",
    },
    packages=["sherpa_onnx"],
    data_files=(
        [
            (
                ("Scripts", get_binaries_to_install())
                if is_windows()
                else ("bin", get_binaries_to_install())
            )
        ]
        if get_binaries_to_install()
        else None
    ),
    url="https://github.com/k2-fsa/sherpa-onnx",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    ext_modules=[cmake_extension("_sherpa_onnx")],
    cmdclass={"build_ext": BuildExtension, "bdist_wheel": bdist_wheel},
    zip_safe=False,
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
            "sherpa-onnx-cli=sherpa_onnx.cli:cli",
        ],
    },
    license="Apache licensed, as found in the LICENSE file",
    install_requires=["sherpa-onnx-core==1.13.8"] if need_split_package() else None,
)

with open("sherpa-onnx/python/sherpa_onnx/__init__.py", "r") as f:
    lines = f.readlines()

with open("sherpa-onnx/python/sherpa_onnx/__init__.py", "w") as f:
    for line in lines:
        if "__version__" in line:
            # skip __version__ = "x.x.x"
            continue
        f.write(line)

```

## Top-level layout

- .clang-format (~110 lines)
- .clang-tidy (~73 lines)
- .flake8 (~8 lines)
- .github/ (dir, 314 files, ~65626 lines)
- .gitignore (~200 lines)
- android/ (dir, 777 files, ~35103 lines)
- build-aarch64-linux-gnu.sh (~124 lines)
- build-android-arm64-v8a.sh (~265 lines)
- build-android-armv7-eabi.sh (~220 lines)
- build-android-x86-64.sh (~199 lines)
- build-android-x86.sh (~180 lines)
- build-arm-linux-gnueabihf.sh (~63 lines)
- build-axcl-linux-aarch64.sh (~128 lines)
- build-axera-linux-aarch64.sh (~210 lines)
- build-flutter-web-wasm.sh (~37 lines)
- build-ios-no-tts.sh (~232 lines)
- build-ios-shared-sherpa-with-static-onnxruntime.sh (~257 lines)
- build-ios-shared.sh (~236 lines)
- build-ios.sh (~237 lines)
- build-macos-shared-sherpa-with-static-onnxruntime.sh (~92 lines)
- build-macos-shared.sh (~101 lines)
- build-macos.sh (~112 lines)
- build-ohos-arm64-v8a.sh (~142 lines)
- build-ohos-armeabi-v7a.sh (~126 lines)
- build-ohos-x86-64.sh (~142 lines)
- build-riscv64-linux-gnu-spacemit.sh (~72 lines)
- build-riscv64-linux-gnu.sh (~72 lines)
- build-rknn-linux-aarch64.sh (~103 lines)
- build-wasm-simd-asr.sh (~64 lines)
- build-wasm-simd-kws.sh (~59 lines)
- build-wasm-simd-nodejs.sh (~65 lines)
- build-wasm-simd-speaker-diarization.sh (~63 lines)
- build-wasm-simd-speech-enhancement.sh (~63 lines)
- build-wasm-simd-tts.sh (~63 lines)
- build-wasm-simd-vad-asr.sh (~70 lines)
- build-wasm-simd-vad.sh (~64 lines)
- build-wasm-simd-web.sh (~63 lines)
- c-api-examples/ (dir, 69 files, ~7362 lines)
- CHANGELOG.md (~1553 lines)
- cmake/ (dir, 58 files, ~5153 lines)
- CMakeLists.txt (~648 lines)
- CPPLINT.cfg (~1 lines)
- cxx-api-examples/ (dir, 63 files, ~7071 lines)
- dart-api-examples/ (dir, 202 files, ~8129 lines)
- dotnet-examples/ (dir, 154 files, ~6506 lines)
- ffmpeg-examples/ (dir, 5 files, ~573 lines)
- flutter/ (dir, 160 files, ~13144 lines)
- flutter-examples/ (dir, 1264 files, ~63717 lines)
- go-api-examples/ (dir, 151 files, ~5107 lines)
- harmony-os/ (dir, 307 files, ~20930 lines)
- ios-swift/ (dir, 18 files, ~1342 lines)
- ios-swiftui/ (dir, 80 files, ~5552 lines)
- java-api-examples/ (dir, 164 files, ~8203 lines)
- jitpack.yml (~22 lines)
- kotlin-api-examples/ (dir, 55 files, ~6240 lines)
- lazarus-examples/ (dir, 11 files, ~1186 lines)
- LICENSE (~202 lines)
- MANIFEST.in (~12 lines)
- mfc-examples/ (dir, 48 files, ~4087 lines)
- new-release.sh (~95 lines)
- nodejs-addon-examples/ (dir, 94 files, ~7606 lines)
- nodejs-examples/ (dir, 53 files, ~3585 lines)
- OPENVINO.md (~114 lines)
- Package.swift (~169 lines)
- pascal-api-examples/ (dir, 137 files, ~8665 lines)
- pom.xml (~19 lines)
- python-api-examples/ (dir, 102 files, ~18220 lines)
- README.md (~737 lines)
- release.sh (~45 lines)
- rust-api-examples/ (dir, 102 files, ~9336 lines)
- scripts/ (dir, 848 files, ~102980 lines)
- setup.py (~123 lines)
- sherpa-onnx/ (dir, 1124 files, ~169793 lines)
- Sources/ (dir, 1 files, ~2297 lines)
- spm-examples/ (dir, 4 files, ~61 lines)
- swift-api-examples/ (dir, 82 files, ~6619 lines)
- tauri-examples/ (dir, 52 files, ~23264 lines)
- toolchains/ (dir, 5 files, ~1009 lines)
- wasm/ (dir, 55 files, ~11821 lines)

