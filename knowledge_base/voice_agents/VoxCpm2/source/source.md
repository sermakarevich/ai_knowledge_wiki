# OpenBMB/VoxCPM
Source: https://github.com/OpenBMB/VoxCPM
Kind: repo
Fetched: 2026-09-22T14:51:23.323554+00:00
Tool: git-clone
PDF location: https://github.com/OpenBMB/VoxCPM (no source.pdf; repo clone only)

# OpenBMB/VoxCPM

Commit: f772e498a45fbb5fb8e13fbf9b9c48be9fe33e69

## README

<h2 align="center">VoxCPM2: Tokenizer-Free TTS for Multilingual Speech Generation, Creative Voice Design, and True-to-Life Cloning</h2>

<p align="center">
  <b>English</b> | <a href="./README_zh.md">中文</a>
</p>

<p align="center">
  <a href="https://github.com/OpenBMB/VoxCPM/"><img src="https://img.shields.io/badge/Project%20Page-GitHub-blue" alt="Project Page"></a>
  <a href="https://huggingface.co/spaces/OpenBMB/VoxCPM-Demo"><img src="https://img.shields.io/badge/Live%20Playground-Demo-orange" alt="Live Playground"></a>
  <a href="https://voxcpm.readthedocs.io/en/latest/"><img src="https://img.shields.io/badge/Docs-ReadTheDocs-8CA1AF" alt="Documentation"></a>
  <a href="https://huggingface.co/openbmb/VoxCPM2"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-VoxCPM2-yellow" alt="Hugging Face"></a>
  <a href="https://modelscope.cn/models/OpenBMB/VoxCPM2"><img src="https://img.shields.io/badge/ModelScope-VoxCPM2-purple" alt="ModelScope"></a>
  <a href="https://openbmb.github.io/voxcpm2-demopage/"><img src="https://img.shields.io/badge/DemoPage-Audio Samples-red" alt="DemoPage"></a>
  <a href="https://arxiv.org/abs/2606.06928"><img src="https://img.shields.io/badge/arXiv-VoxCPM2%20Technical%20Report-red" alt="VoxCPM2 Technical Report"></a>
</p>

<div align="center">
  <img src="assets/voxcpm_logo.png" alt="VoxCPM Logo" width="35%">
  <br><br>
  <a href="https://trendshift.io/repositories/17704" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17704" alt="OpenBMB%2FVoxCPM | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</div>

<br>

<p align="center">
  👋 Join our community for discussion and support!
  <br>
  <a href="./assets/feishu-group.png" style="display:inline-block;vertical-align:middle; margin-left: 10px;">
    <img src="./assets/feishu-logo.png" width="16" height="16" style="vertical-align:middle;"> Feishu
  </a>
  &nbsp;|&nbsp;
  <a href="https://discord.gg/KZUx7tVNwz" style="display:inline-block;vertical-align:middle;">
    <img src="./assets/discord-logo.png" width="16" height="16" style="vertical-align:middle;"> Discord
  </a>
  &nbsp;|&nbsp;
  <a href="https://modelbest.feishu.cn/wiki/UtWxwcERfiRIpIkBOjuc3h9tn1D?fromScene=spaceOverview" style="display:inline-block;vertical-align:middle;">
    📚 MiniCPM Wiki
  </a>
</p>

VoxCPM is a **tokenizer-free** Text-to-Speech system that directly generates continuous speech representations via an end-to-end **diffusion autoregressive architecture**, bypassing discrete tokenization to achieve highly natural and expressive synthesis.

**VoxCPM2** is the latest major release — a **2B** parameter model trained on **over 2 million hours** of multilingual speech data, now supporting **30 languages**, **Voice Design**, **Controllable Voice Cloning**, and **48kHz** studio-quality audio output. Built on a [MiniCPM-4](https://github.com/OpenBMB/MiniCPM) backbone.

### ✨ Highlights

- 🌍 **30-Language Multilingual** — Input text in any of the 30 supported languages and synthesize directly, no language tag needed
- 🎨 **Voice Design** — Create a brand-new voice from a natural-language description alone (gender, age, tone, emotion, pace …), no reference audio required
- 🎛️ **Controllable Cloning** — Clone any voice from a short reference clip, with optional style guidance to steer emotion, pace, and expression while preserving the original timbre
- 🎙️ **Ultimate Cloning** — Reproduce every vocal nuance: provide both reference audio and its transcript, and the model continues seamlessly from the reference, faithfully preserving every vocal detail — timbre, rhythm, emotion, and style (same as VoxCPM1.5)
- 🔊 **48kHz High-Quality Audio** — Accepts 16kHz reference audio and directly outputs 48kHz studio-quality audio via AudioVAE V2's asymmetric encode/decode design, with built-in super-resolution — no external upsampler needed
- 🧠 **Context-Aware Synthesis** — Automatically infers appropriate prosody and expressiveness from text content
- ⚡ **Real-Time Streaming** — RTF as low as ~0.3 on NVIDIA RTX 4090, and ~0.13 accelerated by [Nano-vLLM](https://github.com/a710128/nanovllm-voxcpm) or [vLLM-Omni](https://github.com/vllm-project/vllm-omni) — official vLLM omni-modal serving for VoxCPM2 with PagedAttention and an OpenAI-compatible API
- 📜 **Fully Open-Source & Commercial-Ready** — Weights and code released under the [Apache-2.0](LICENSE) license, free for commercial use

**🌍 Supported Languages (30)**  
Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Lao, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese

Chinese Dialect: 四川话, 粤语, 吴语, 东北话, 河南话, 陕西话, 山东话, 天津话, 闽南话

### News

- **[2026.04]** 🔥 We release **VoxCPM2** — 2B, 30 languages, Voice Design & Controllable Voice Cloning, 48kHz audio output! [Weights](https://huggingface.co/openbmb/VoxCPM2) | [Docs](https://voxcpm.readthedocs.io/en/latest/) | [Playground](https://huggingface.co/spaces/OpenBMB/VoxCPM-Demo) | [Technical Report](https://arxiv.org/abs/2606.06928)
- **[2025.12]** 🎉 Open-source **VoxCPM1.5** [weights](https://huggingface.co/openbmb/VoxCPM1.5) with SFT & LoRA fine-tuning. (**🏆 #1 GitHub Trending**)
- **[2025.09]** 🔥 Release VoxCPM [Technical Report](https://arxiv.org/abs/2509.24650).
- **[2025.09]** 🎉 Open-source **VoxCPM-0.5B** [weights](https://huggingface.co/openbmb/VoxCPM-0.5B) (**🏆 #1 HuggingFace Trending**)

---

## Contents

- [Quick Start](#-quick-start)
  - [Installation](#installation)
  - [Python API](#python-api)
  - [CLI Usage](#cli-usage)
  - [Web Demo](#web-demo)
  - [Production Deployment](#-production-deployment-nano-vllm)
  - [On-Device Inference (llama.cpp-omni)](#-on-device-inference-llamacpp-omni)
- [Models & Versions](#-models--versions)
- [Performance](#-performance)
- [Fine-tuning](#%EF%B8%8F-fine-tuning)
- [Documentation](#-documentation)
- [Ecosystem & Community](#-ecosystem--community)
- [Risks and Limitations](#%EF%B8%8F-risks-and-limitations)
- [Citation](#-citation)

---

## 🚀 Quick Start

### Installation

```sh
pip install voxcpm
```

> **Requirements:** Python ≥ 3.10 (<3.13), PyTorch ≥ 2.5.0, CUDA ≥ 12.0. See [Quick Start Docs](https://voxcpm.readthedocs.io/en/latest/quickstart.html) for details.

### Python API

#### 🗣️ Text-to-Speech

```python
from voxcpm import VoxCPM
import soundfile as sf

model = VoxCPM.from_pretrained(
  "openbmb/VoxCPM2",
  load_denoiser=False,
)

wav = model.generate(
    text="VoxCPM2 is the current recommended release for realistic multilingual speech synthesis.",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("demo.wav", wav, model.tts_model.sample_rate)
print("saved: demo.wav")
```

If you prefer downloading from ModelScope first, you can use:

```bash
pip install modelscope
```

```python
from modelscope import snapshot_download
snapshot_download("OpenBMB/VoxCPM2", local_dir='./pretrained_models/VoxCPM2') # specify the local directory to save the model

from voxcpm import VoxCPM
import soundfile as sf
model = VoxCPM.from_pretrained("./pretrained_models/VoxCPM2", load_denoiser=False)

wav = model.generate(
    text="VoxCPM2 is the current recommended release for realistic multilingual speech synthesis.",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("demo.wav", wav, model.tts_model.sample_rate)
```

#### 🎨 Voice Design

Create a voice from a natural-language description — no reference audio needed. **Format:** put the description in parentheses at the start of `text`(e.g. `"(your voice description)The text to synthesize."`):

```python
wav = model.generate(
    text="(A young woman, gentle and sweet voice)Hello, welcome to VoxCPM2!",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("voice_design.wav", wav, model.tts_model.sample_rate)
```

#### 🎛️ Controllable Voice Cloning

Upload a reference audio. The model clones the timbre, and you can still use control instructions to adjust speed, emotion, or style.

```python
wav = model.generate(
    text="This is a cloned voice generated by VoxCPM2.",
    reference_wav_path="path/to/voice.wav",
)
sf.write("clone.wav", wav, model.tts_model.sample_rate)

wav = model.generate(
    text="(slightly faster, cheerful tone)This is a cloned voice with style control.",
    reference_wav_path="path/to/voice.wav",
    cfg_value=2.0,
    inference_timesteps=10,
    seed=42,
)
sf.write("controllable_clone.wav", wav, model.tts_model.sample_rate)
```

#### 🎙️ Ultimate Cloning

Provide both the reference audio and its exact transcript for audio-continuation-based cloning with every vocal nuance reproduced. For maximum cloning similarity, pass the same reference clip to both `reference_wav_path` and `prompt_wav_path` as shown below:

```python
wav = model.generate(
    text="This is an ultimate cloning demonstration using VoxCPM2.",
    prompt_wav_path="path/to/voice.wav",
    prompt_text="The transcript of the reference audio.",
    reference_wav_path="path/to/voice.wav", # optional, for better simliarity 
)
sf.write("hifi_clone.wav", wav, model.tts_model.sample_rate)
```

**🔄 Streaming API**

```python
import numpy as np

chunks = []
for chunk in model.generate_streaming(
    text="Streaming text to speech is easy with VoxCPM!",
):
    chunks.append(chunk)
wav = np.concatenate(chunks)
sf.write("streaming.wav", wav, model.tts_model.sample_rate)
```



### CLI Usage

```bash
# Voice design (no reference audio needed)
voxcpm design \
  --text "VoxCPM2 brings studio-quality multilingual speech synthesis." \
  --output out.wav

# Controllable voice cloning with style control
voxcpm design \
  --text "VoxCPM2 brings studio-quality multilingual speech synthesis." \
  --control "Young female voice, warm and gentle, slightly smiling" \
  --seed 42 \
  --output out.wav

# Voice cloning (reference audio)
voxcpm clone \
  --text "This is a voice cloning demo." \
  --reference-audio path/to/voice.wav \
  --output out.wav

# Ultimate cloning (prompt audio + transcript)
voxcpm clone \
  --text "This is a voice cloning demo." \
  --prompt-audio path/to/voice.wav \
  --prompt-text "reference transcript" \
  --reference-audio path/to/voice.wav \ # optional, for better simliarity
  --output out.wav

# Batch processing
voxcpm batch --input examples/input.txt --output-dir outs

# Optional post-generation timestamps with stable-ts
pip install "voxcpm[timestamps]"
voxcpm design \
  --text "VoxCPM2 brings studio-quality multilingual speech synthesis." \
  --output out.wav \
  --timestamps \
  --timestamp-level word \
  --timestamp-language en

# Character timestamps are best-effort and are derived from word alignment
voxcpm design \
  --text "欢迎使用 VoxCPM2。" \
  --output out.wav \
  --timestamps \
  --timestamp-level char \
  --timestamp-language zh

# Help
voxcpm --help
```

### Web Demo

```bash
python app.py --port 8808  # then open in browser: http://localhost:8808
```

Use `--device` to choose the runtime device:

```bash
python app.py --device auto
```

Supported values are `auto`, `cpu`, `mps`, `cuda`, and `cuda:N`. On Apple Silicon Macs, `auto` uses MPS when available.

### 🚢 Production Deployment (Nano-vLLM)

For high-throughput serving, use **[Nano-vLLM-VoxCPM](https://github.com/a710128/nanovllm-voxcpm)** — a dedicated inference engine built on Nano-vLLM with concurrent request support and an async API.

```bash
pip install nano-vllm-voxcpm
```

```python
from nanovllm_voxcpm import VoxCPM
import numpy as np, soundfile as sf

server = VoxCPM.from_pretrained(model="/path/to/VoxCPM", devices=[0])
chunks = list(server.generate(target_text="Hello from VoxCPM!"))
sf.write("out.wav", np.concatenate(chunks), 48000)
server.stop()
```

> **RTF as low as ~0.13 on NVIDIA RTX 4090** (vs ~0.3 with the standard PyTorch implementation), with support for batched concurrent requests and a FastAPI HTTP server. See the [N

... (truncated, 29917 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=64", "wheel", "setuptools_scm>=8"]
build-backend = "setuptools.build_meta"

[project]
name = "voxcpm"
dynamic = ["version"]
description = "VoxCPM: Tokenizer-Free TTS for Context-Aware Speech Generation and True-to-Life Voice Cloning"
readme = "README.md"
license = "Apache-2.0"
authors = [
    {name = "OpenBMB", email = "openbmb@gmail.com"}
]
maintainers = [
    {name = "OpenBMB", email = "openbmb@gmail.com"}
]
keywords = ["voxcpm", "text-to-speech", "tts", "speech-synthesis", "voice-cloning", "ai", "deep-learning", "pytorch"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
requires-python = ">=3.10"
dependencies = [
    "torch>=2.5.0",
    "torchaudio>=2.5.0",
    "torchcodec",
    "transformers>=4.36.2",
    "einops",
    "gradio>=6,<7",
    "inflect",
    "addict",
    "wetext",
    "modelscope>=1.22.0",
    "datasets>=3,<4",
    "huggingface-hub",
    "pydantic",
    "tqdm",
    "simplejson",
    "sortedcontainers",
    "soundfile",
    "librosa",
    "matplotlib",
    "funasr",
    "spaces",
    "argbind",
    "safetensors"

]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov>=2.0",
    "black>=21.0",
    "flake8>=3.8",
    "pre-commit>=2.0",
]
timestamps = [
    "stable-ts>=2.19.1",
]

[project.scripts]
voxcpm = "voxcpm.cli:main"

[project.urls]
Homepage = "https://github.com/OpenBMB/VoxCPM"
Repository = "https://github.com/OpenBMB/VoxCPM.git"
Documentation = "https://github.com/OpenBMB/VoxCPM#readme"
"Bug Tracker" = "https://github.com/OpenBMB/VoxCPM/issues"

[tool.setuptools.packages.find]
where = ["src"]
include = ["voxcpm*"]

[tool.setuptools.package-dir]
"" = "src"

[tool.setuptools_scm]
version_scheme = "post-release"

[tool.black]
line-length = 120
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

```

## Top-level layout

- .dockerignore (~26 lines)
- .github/ (dir, 1 files, ~54 lines)
- .gitignore (~13 lines)
- app.py (~606 lines)
- app_old.py (~292 lines)
- assets/ (dir, 8 files, ~0 lines)
- conf/ (dir, 6 files, ~175 lines)
- docker/ (dir, 4 files, ~301 lines)
- examples/ (dir, 3 files, ~6 lines)
- LICENSE (~201 lines)
- lora_ft_webui.py (~1331 lines)
- pyproject.toml (~100 lines)
- README.md (~697 lines)
- README_zh.md (~690 lines)
- scripts/ (dir, 4 files, ~1372 lines)
- src/ (dir, 38 files, ~7497 lines)
- tests/ (dir, 6 files, ~1330 lines)
- uv.lock (~5263 lines)

