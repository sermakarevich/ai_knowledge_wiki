# OpenMOSS/MOSS-TTS
> PDF location: https://github.com/OpenMOSS/MOSS-TTS (no source.pdf fetched; use Source URL below)
Source: https://github.com/OpenMOSS/MOSS-TTS
Kind: repo
Fetched: 2026-09-22T14:22:16.587519+00:00
Tool: git-clone

# OpenMOSS/MOSS-TTS

Commit: 934d6826b084c46a0d033402174d5f8ac4ed2519

## README

# MOSS-TTS Family

<br>

<p align="center">
  <img src="./assets/OpenMOSS_Logo.svg" height="70" align="middle" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="./assets/mosi-logo.png" height="50" align="middle" />
</p>

<div align="center">
  <a href="https://www.star-history.com/openmoss/moss-tts#badges">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/badge?repo=OpenMOSS/MOSS-TTS&amp;type=trending&amp;theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/badge?repo=OpenMOSS/MOSS-TTS&amp;type=trending" />
      <img alt="GitHub Trending Repository of the Day" src="https://api.star-history.com/badge?repo=OpenMOSS/MOSS-TTS&amp;type=trending" />
    </picture>
  </a>
</div>


<div align="center">
  <a href="https://clawhub.ai/luogao2333/moss-tts-voice"><img src="https://img.shields.io/badge/🦞_OpenClaw-Skills-8A2BE2" alt="OpenClaw"></a>
  <a href="https://huggingface.co/collections/OpenMOSS-Team/moss-tts"><img src="https://img.shields.io/badge/Huggingface-Models-orange?logo=huggingface&amp"></a>
  <a href="https://www.modelscope.cn/collections/openmoss/MOSS-TTS"><img src="https://img.shields.io/badge/ModelScope-Model-7B61FF?logo=modelscope&logoColor=white"></a>
  <a href="https://mosi.cn/#models"><img src="https://img.shields.io/badge/Blog-View-blue?logo=internet-explorer&amp"></a>
  <a href="https://arxiv.org/abs/2603.18090"><img src="https://img.shields.io/badge/Arxiv-2603.18090-red?logo=Arxiv&amp"></a>

  <a href="https://studio.mosi.cn"><img src="https://img.shields.io/badge/AIStudio-Try-green?logo=internet-explorer&amp"></a>
  <a href="https://studio.mosi.cn/docs/moss-tts"><img src="https://img.shields.io/badge/API-Docs-00A3FF?logo=fastapi&amp"></a>
  <a href="https://x.com/Open_MOSS"><img src="https://img.shields.io/badge/Twitter-Follow-black?logo=x&amp"></a>
  <a href="https://discord.gg/Ahu78PH4p"><img src="https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&amp"></a>
  <a href="./assets/wechat.jpg"><img src="https://img.shields.io/badge/WeChat-Join-07C160?logo=wechat&amp;logoColor=white" alt="WeChat"></a>
  <a href="./assets/lark.png"><img src="https://img.shields.io/badge/Lark-Join-3370FF" alt="Lark"></a>
</div>


[English](README.md) | [简体中文](README_zh.md)


MOSS‑TTS Family is an open‑source **speech and sound generation model family** from [MOSI.AI](https://mosi.cn/#hero) and the [OpenMOSS team](https://www.open-moss.com/). It is designed for **high‑fidelity**, **high‑expressiveness**, and **complex real‑world scenarios**, covering stable long‑form speech, multi‑speaker dialogue, voice/character design, environmental sound effects, and real‑time streaming TTS.


**Start here:** [Quickstart](#quickstart) · [Model weights](https://huggingface.co/collections/OpenMOSS-Team/moss-tts) · [Listen to samples](#demo) · [Fine-tuning](#fine-tuning) · [Serving backends](#accelerated-inference-backends)

### Choose a model for your task

| What you want to build | Start with |
| --- | --- |
| Speech and voice cloning on a CPU or in a browser | [MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano) |
| Multilingual long-form narration and voice cloning | [MOSS-TTS-v1.5](#moss-tts-v15) · [Local Transformer v1.5](#moss-tts-local-transformer-v15) |
| Multi-speaker dialogue, podcasts, and dubbing | [MOSS-TTSD](https://github.com/OpenMOSS/MOSS-TTSD) |
| Real-time streaming speech | [MOSS-TTS-Realtime](moss_tts_realtime/README.md) |
| Voice design or environmental sound effects | [Released models](#released-models) · [MOSS-SoundEffect v2](moss_soundeffect_v2/README.md) |

## News
* 2026.6.18: 🚀 [MOSS-TTS-Local-Transformer-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5) receives **Day-0 support** in [SGLang-Omni](https://github.com/sgl-project/sglang-omni) — the first inference backend to support the `MossTTSLocal` architecture, with an OpenAI-compatible `/v1/audio/speech` endpoint, streaming, and voice cloning. See the cookbooks: [`moss_tts_local`](https://github.com/sgl-project/sglang-omni/blob/main/docs/cookbook/moss_tts_local.md), [`moss_tts`](https://github.com/sgl-project/sglang-omni/blob/main/docs/cookbook/moss_tts.md).
* 2026.6.18: 🚀 Released [MOSS-TTS-Local-Transformer-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Local-Transformer-v1.5), a **4B** `MossTTSLocal` checkpoint that inherits all v1.5 features (language tags, stable cloning, explicit pause control, etc.), scales the backbone from Qwen3-1.7B to Qwen3-4B, and uses **MOSS-Audio-Tokenizer-v2** for native **48 kHz stereo** output.
* 2026.6.7: 🚀 Released [MOSS-Audio-Tokenizer-v2](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-v2), natively supporting 48 kHz stereo input and output. Check out the [MOSS-Audio-Tokenizer repository](https://github.com/OpenMOSS/MOSS-Audio-Tokenizer) for more details!

<details>
<summary>Earlier updates</summary>

* 2026.6.2: 🚀 [vLLM-Omni](https://github.com/vllm-project/vllm-omni) now supports the full MOSS-TTS series (`MossTTSDelay`, `MossTTSRealtime`, and `MossTTSNano` architectures), including MOSS-TTS-v1.5, MOSS-TTS, MOSS-TTSD, MOSS-SoundEffect, MOSS-VoiceGenerator, MOSS-TTS-Realtime, and MOSS-TTS-Nano. See the [recipe](https://github.com/vllm-project/vllm-omni/blob/main/recipes/OpenMOSS/MOSS-TTS.md) and [examples](https://github.com/vllm-project/vllm-omni/tree/main/examples/offline_inference/text_to_speech/moss_tts).
* 2026.5.26: 🚀 Released [MOSS-SoundEffect-v2.0](https://huggingface.co/OpenMOSS-Team/MOSS-SoundEffect-v2.0), a new text-to-audio model using a **DiT backbone with the Flow Matching objective**, generating **48 kHz** bilingual sound effects up to **30 seconds** — see [`moss_soundeffect_v2/`](https://github.com/OpenMOSS/MOSS-TTS/tree/main/moss_soundeffect_v2).
* 2026.5.26: 🚀 Released [MOSS-TTS-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5), with stronger multilingual synthesis when language tags are provided, more stable voice cloning, better long-reference short-text cloning, punctuation-following prosody, and explicit pause control via `[pause X.Ys]`.
* 2026.5.6: 🚀 MOSS-TTS and MOSS-Audio-Tokenizer now support `mlx-audio`. Visit the [mlx-audio GitHub repository](https://github.com/Blaizzy/mlx-audio) for details.
* 2026.4.29: 📝 MOSS-TTS 2.0 is coming soon! We are collecting TTS feedback, suggestions, and feature requests via the [requirements collection form](https://acnc6zeentra.feishu.cn/share/base/form/shrcnyAe1LwqKWjCSuW4wiZ2Hef).
* 2026.4.13: 🚀 MOSS-TTS-Nano, our ~100M-parameter model, is now available! It supports multilingual voice cloning, 48 kHz stereo input/output, and streaming output on just 4 CPU cores. Check the [GitHub repository](https://github.com/OpenMOSS/MOSS-TTS-Nano) and our [blog](https://openmoss.github.io/MOSS-TTS-Nano-Demo/) for more details.
* 2026.3.31: 📄 Our technical reports for [MOSS-TTSD](https://arxiv.org/pdf/2603.19739) and [MOSS-VoiceGenerator](https://arxiv.org/pdf/2603.28086) are now available on arXiv!
* 2026.3.26: 📘 Added a tutorial on fine-tuning the MOSS-TTS-Realtime!
* 2026.3.20: 📄 Our [technical report](https://arxiv.org/pdf/2603.18090) is now available on arXiv!
* 2026.3.18: 🚀 Added a first-class MOSS-TTS `llama.cpp` implementation in the companion repository [`OpenMOSS/llama.cpp`](https://github.com/OpenMOSS/llama.cpp/tree/moss-tts-firstclass), including end-to-end docs and a runnable pipeline for GGUF backbone inference plus ONNX audio codec decoding. See the [first-class e2e guide](https://github.com/OpenMOSS/llama.cpp/blob/moss-tts-firstclass/docs/moss-tts-firstclass-e2e.md).
* 2026.3.16: 📘 Added a tutorial on fine-tuning the MossTTSLocal architecture, suitable for MOSS-TTS-Local-Transformer!
* 2026.3.12: 🚀 Added SGLang backend support for the `MossTTSDelay` architecture, enabling efficient inference for MOSS-TTS (Delay) and MOSS-SoundEffect, with around **3× faster** generation throughput!
* 2026.3.11: 📘 Added a tutorial on fine-tuning the MossTTSDelay architecture, suitable for MOSS-TTS(Delay), MOSS-TTSD, MOSS-VoiceGenerator, and MOSS-SoundEffect!
* 2026.3.10: ⚡️ Significantly optimized the VRAM usage of llama.cpp inference pipeline. Now 8B model fits onto 8GB GPUs!
* 2026.3.4: 🚀 Added **PyTorch-free inference support** — enabling lightweight on-device deployment via **llama.cpp + ONNX Runtime**. Quantized **GGUF weights** are released at [OpenMOSS-Team/MOSS-TTS-GGUF](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-GGUF), and the **ONNX audio tokenizer** is available at [OpenMOSS-Team/MOSS-Audio-Tokenizer-ONNX](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-ONNX). See the [llama.cpp backend](#llamacpp-backend-torch-free-inference) for details.
* 2026.3.4: 🎉 We add MOSS-TTS skills in [ClawHub](https://clawhub.ai) of 🦞 OpenClaw: [feishu-voice-tts](https://clawhub.ai/helloeveryworlds/feishu-voice-tts) and [moss-tts-voice](https://clawhub.ai/luogao2333/moss-tts-voice).
* 2026.2.10: 🎉🎉🎉 We have released [MOSS-TTS Family](https://huggingface.co/collections/OpenMOSS-Team/moss-tts). Check our [Blog](https://mosi.cn/#models) for more details! Our **Huggingface Space** is here: [MOSS-TTS](https://huggingface.co/spaces/OpenMOSS-Team/MOSS-TTS), [MOSS-TTSD-v1.0](https://huggingface.co/spaces/OpenMOSS-Team/MOSS-TTSD-v1.0), [MOSS-VoiceGenerator](https://huggingface.co/spaces/OpenMOSS-Team/MOSS-VoiceGenerator).

</details>

## Demo

<div align="center">
  <video src="https://gist.github.com/user-attachments/assets/fdce9f66-20ec-45e8-9615-89606ae2fbe8" width="70%" poster=""> </video>
</div>

## Contents

- [MOSS-TTS Family](#moss-tts-family)
  - [News](#news)
  - [Demo](#demo)
  - [Contents](#contents)
  - [Introduction](#introduction)
  - [Model Architecture](#model-architecture)
  - [Released Models](#released-models)
  - [Supported Languages](#supported-languages)
  - [MOSS-TTS-v1.5](#moss-tts-v15)
  - [MOSS-TTS-Local-Transformer-v1.5](#moss-tts-local-transformer-v15)
  - [Quickstart](#quickstart)
    - [OpenClaw API Skills](#openclaw-api-skills)
    - [Environment Setup](#environment-setup)
      - [Using Conda](#using-conda)
      - [Using `uv`](#using-uv)
      - [(Optional) Install FlashAttention 2](#optional-install-flashattention-2)
    - [MOSS‑TTS Basic Usage](#mosstts-basic-usage)
  - [Fine-Tuning](#fine-tuning)
  - [llama.cpp Backend (Torch-Free Inference)](#llamacpp-backend-torch-free-inference)
    - [Quick Start](#quick-start)
    - [Installation Profiles](#installation-profiles)
    - [Model Weights](#model-weights)
    - [Configuration](#configuration)
  - [Accelerated Inference Backends](#accelerated-inference-backends)
    - [SGLang-Omni](#sglang-omni)
    - [vLLM-Omni](#vllm-omni)
  - [Evaluation](#evaluation)
    - [MOSS‑TTS](#mosstts)
    - [MOSS‑TTSD](#mossttsd)
      - [Objective Evaluation](#objective-evaluation)
      - [Subjective Evaluation](#subjective-evaluation)
    - [MOSS‑VoiceGenerator](#mossvoicegenerator)
    - [MOSS‑TTS-Realtime](#mosstts-realtime)
  - [MOSS-TTS-Nano](#moss-tts-nano)
    - [Introduction](#introduction-1)
    - [Model Weights](#model-weights-1)
  - [MOSS-Audio-Tokenizer](#moss-audio-tokenizer)
    - [Introduction](#introduction-2)
    - [Model Weights](#model-weights-2)
    - [Objective Reconstruction Evaluation](#objective-reconstruction-evaluation)
  - [📚 More Information](#-more-information)
    - [🌟 Community Projects](#-community-projects)
  - [LICENSE](#license)
  - [Citation](#citation)
  - [Star History](#star-history)


## Introduction

<p align="center">
  <img src="./assets/moss_tts_family.jpeg" width="85%" />
</p>

When a single piece of audio needs to **sound like a real person**, **pronounce every word accurately**, **switch speaking styles across content**, **remain stable over tens of minutes**, and **support dialogue, role‑play, and real‑time interaction**, a single TTS model is often not enough. The **MOSS‑TTS Family** breaks the workflow into five production‑ready models that can be used independent

... (truncated, 43079 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "moss-tts"
version = "0.1.0"
description = "MOSS-TTS dependencies and utilities"
readme = "README.md"
requires-python = ">=3.10"
license = { file = "LICENSE" }
authors = [{ name = "OpenMOSS Team" }]
dependencies = [
  "safetensors==0.6.2",
  "numpy==2.1.0",
  "orjson==3.11.4",
  "tqdm==4.67.1",
  "PyYAML==6.0.3",
  "einops==0.8.1",
  "scipy==1.16.2",
  "librosa==0.11.0",
  "tiktoken==0.12.0",
  "psutil",
  "packaging",
  "ninja",
  "setuptools",
  "wheel",
  "gradio"
]

[project.optional-dependencies]
flash-attn = ["flash-attn"]
finetune = [
    "accelerate>=1.10.1",
    "wandb>=0.16.0",
]
finetune-deepspeed = [
    "accelerate>=1.10.1",
    "deepspeed>=0.16.0",
    "wandb>=0.16.0",
]

# Default PyTorch runtime stack for the original pipeline.
torch-runtime = [
    "torch==2.9.1+cu128",
    "torchaudio==2.9.1+cu128",
    "torchcodec==0.8.1",
    "transformers==5.0.0",
    "accelerate>=1.10.1",
]

# llama.cpp backend — torch-free core
llama-cpp = [
    "numpy>=2.0",
    "pyyaml>=6.0",
    "tokenizers>=0.20",
    "soundfile>=0.12",
]
# llama.cpp + ONNX Runtime audio tokenizer
llama-cpp-onnx = [
    "numpy>=2.0",
    "pyyaml>=6.0",
    "tokenizers>=0.20",
    "soundfile>=0.12",
    "onnxruntime-gpu>=1.19",
]
# llama.cpp + TensorRT audio tokenizer
llama-cpp-trt = [
    "numpy>=2.0",
    "pyyaml>=6.0",
    "tokenizers>=0.20",
    "soundfile>=0.12",
    "tensorrt>=10.0",
    "cuda-python>=12.0",
]
# torch-accelerated LM heads (optional, auto-detected)
llama-cpp-torch = [
    "torch>=2.4",
]

[project.scripts]
moss-tts-llama-cpp = "moss_tts_delay.llama_cpp.pipeline:main"

[project.urls]
Homepage = "https://github.com/OpenMOSS-Team/MOSS-TTS"
Repository = "https://github.com/OpenMOSS-Team/MOSS-TTS"

[tool.setuptools]
py-modules = []

```

## Top-level layout

- .gitignore (~216 lines)
- .gitmodules (~3 lines)
- assets/ (dir, 28 files, ~127 lines)
- clis/ (dir, 5 files, ~3945 lines)
- community/ (dir, 3 files, ~817 lines)
- configs/ (dir, 4 files, ~237 lines)
- docs/ (dir, 5 files, ~1284 lines)
- LICENSE (~201 lines)
- MANIFEST.in (~22 lines)
- moss_audio_tokenizer/ (dir, 0 files, ~0 lines)
- moss_soundeffect_v2/ (dir, 31 files, ~6762 lines)
- moss_tts_delay/ (dir, 35 files, ~8535 lines)
- moss_tts_local/ (dir, 16 files, ~4627 lines)
- moss_tts_local_v1.5/ (dir, 19 files, ~7197 lines)
- moss_tts_realtime/ (dir, 28 files, ~7918 lines)
- pyproject.toml (~89 lines)
- README.md (~783 lines)
- README_zh.md (~794 lines)
- scripts/ (dir, 3 files, ~1521 lines)

