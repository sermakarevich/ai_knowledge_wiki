# index-tts/index-tts
> PDF/original location (no source.pdf bundled, <2 MB rule N/A): https://github.com/index-tts/index-tts
Source: https://github.com/index-tts/index-tts
Kind: repo
Fetched: 2026-09-22T14:11:56.430706+00:00
Tool: git-clone

# index-tts/index-tts

Commit: ee40fa7d6c6b8a2c7f06105f9f1e65775b74868c

## README

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/indextts_icon_dark.png"/>
  <img src="assets/indextts_icon_light.png" width="300"/>
</picture>

**An Industrial-Level Controllable and Efficient Zero-Shot Text-to-Speech System**

[简体中文](docs/README_zh.md) | English | [日本語](docs/README_ja.md) | [Español](docs/README_es.md) | [العربية](docs/README_ar.md)

[![GitHub Stars](https://img.shields.io/github/stars/index-tts/index-tts?style=flat&logo=github)](https://github.com/index-tts/index-tts/stargazers)
[![arXiv](https://img.shields.io/badge/arXiv-2601.03888-b31b1b?logo=arxiv)](https://arxiv.org/abs/2601.03888)
[![Discord](https://img.shields.io/badge/Discord-join-5865F2?logo=discord&logoColor=white)](https://discord.gg/uT32E7KDmy)

</div>

IndexTTS is a zero-shot text-to-speech system that clones a voice from a single
reference audio clip. The latest release, **IndexTTS-2.5**, supports Chinese,
English, Japanese, Spanish and Arabic, with fine-grained emotion control,
speaking speed control, pronunciation control (Pinyin / CMU phonemes /
Japanese Kana), and faster inference than IndexTTS-2.

---

## 🗂️ Model Zoo

| Model | Demos | Paper | ModelScope | HuggingFace |
| :--- | :---: | :---: | :---: | :---: |
| **IndexTTS-2.5** | [![Demo](https://img.shields.io/badge/Demo-Page-orange?logo=github)](https://index-tts.github.io/index-tts2-5.github.io/) [![Studio](https://img.shields.io/badge/Studio-ModelScope-purple?logo=modelscope)](https://modelscope.cn/studios/IndexTeam/IndexTTS-2.5) [![Space](https://img.shields.io/badge/Space-HuggingFace-blue?logo=huggingface)](https://huggingface.co/spaces/IndexTeam/IndexTTS-2.5-Demo) | [![Paper](https://img.shields.io/badge/Paper-arXiv-red?logo=arxiv)](https://arxiv.org/abs/2601.03888) | [![ModelScope](https://img.shields.io/badge/ModelScope-Model-purple?logo=modelscope)](https://modelscope.cn/models/IndexTeam/IndexTTS-2.5) | [![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-blue?logo=huggingface)](https://huggingface.co/IndexTeam/IndexTTS-2.5) |
| **IndexTTS-2** | [![Demo](https://img.shields.io/badge/Demo-Page-orange?logo=github)](https://index-tts.github.io/index-tts2.github.io/) | [![Paper](https://img.shields.io/badge/Paper-arXiv-red?logo=arxiv)](https://arxiv.org/abs/2506.21619) | [![ModelScope](https://img.shields.io/badge/ModelScope-Model-purple?logo=modelscope)](https://modelscope.cn/models/IndexTeam/IndexTTS-2) | [![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-blue?logo=huggingface)](https://huggingface.co/IndexTeam/IndexTTS-2) |
| **IndexTTS-1.5** | [![Demo](https://img.shields.io/badge/Demo-Page-orange?logo=github)](https://index-tts.github.io/) | [![Paper](https://img.shields.io/badge/Paper-arXiv-red?logo=arxiv)](https://arxiv.org/abs/2502.05512) | [![ModelScope](https://img.shields.io/badge/ModelScope-Model-purple?logo=modelscope)](https://modelscope.cn/models/IndexTeam/IndexTTS-1.5) | [![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-blue?logo=huggingface)](https://huggingface.co/IndexTeam/IndexTTS-1.5) |
| **IndexTTS** | [![Demo](https://img.shields.io/badge/Demo-Page-orange?logo=github)](https://index-tts.github.io/) | [![Paper](https://img.shields.io/badge/Paper-arXiv-red?logo=arxiv)](https://arxiv.org/abs/2502.05512) | [![ModelScope](https://img.shields.io/badge/ModelScope-Model-purple?logo=modelscope)](https://modelscope.cn/models/IndexTeam/Index-TTS) | [![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-blue?logo=huggingface)](https://huggingface.co/IndexTeam/Index-TTS) |

## 📣 News

- `2026/08/10` 🔥 We release **IndexTTS-2.5**
  - Now supports Chinese, English, Japanese, Spanish and Arabic, with faster inference than IndexTTS-2, while keeping the cross-lingual and timbre-emotion disentanglement capabilities.
  - Improved controllability of Chinese Pinyin, English CMU phonemes and Japanese Kana.
  - Speaking speed control via `duration_factor` (0.5x–2.0x duration).
  - Production deployment supported via [vLLM](https://recipes.vllm.ai/IndexTeam/IndexTTS-2.5).
- `2025/09/08` 🔥 We release **IndexTTS-2**
  - The first autoregressive TTS model with precise synthesis duration control, supporting both controllable and uncontrollable modes. <i>This functionality is not yet enabled in this release.</i>
  - Highly expressive emotional speech synthesis, with emotion control through multiple input modalities.
- `2025/05/14` 🔥 We release **IndexTTS-1.5**, significantly improving the model's stability and its performance in English.
- `2025/03/25` 🔥 We release **IndexTTS-1.0** with model weights and inference code.
- `2025/02/12` 🎉 We submitted our paper to arXiv, and released our demos and test sets.

## 🎬 Demos

<div align="center">

**IndexTTS-2.5: The Future of Voice, Now Generating**

[![IndexTTS2.5 Demo](assets/index2.5_video_cover.png)](https://www.bilibili.com/video/BV1uvMk6ZEdK/)

**IndexTTS-2: The Future of Voice, Now Generating**

[![IndexTTS2 Demo](assets/IndexTTS2-video-pic.png)](https://www.bilibili.com/video/BV136a9zqEk5)

</div>

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have [git](https://git-scm.com/downloads) installed, then download
this repository:

```bash
git clone https://github.com/index-tts/index-tts.git && cd index-tts
```

Example audio files are downloaded on demand from HuggingFace/ModelScope the
first time the WebUI starts, so Git LFS is no longer required.

### 2. Install Dependencies

We use [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage
the project's dependency environment. It is **required** for a reliable
installation:

```bash
pip install -U uv  # or see the link above for other install methods
```

```bash
uv sync --all-extras
```

This automatically creates a `.venv` project directory and installs the correct
versions of Python and all required dependencies.

If the download is slow, use a local mirror, e.g. one of these mirrors in China:

```bash
uv sync --all-extras --default-index "https://mirrors.aliyun.com/pypi/simple"

uv sync --all-extras --default-index "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
```

> [!TIP]
> **Available Extra Features:**
>
> - `--all-extras`: Automatically adds *every* extra feature listed below. You can
>   remove this flag if you want to customize your installation choices.
> - `--extra webui`: Adds WebUI support (recommended).
> - `--extra deepspeed`: Adds DeepSpeed support (may speed up inference on some
>   systems).

> [!IMPORTANT]
> **Windows:** DeepSpeed may be difficult to install. You can skip it by removing
> the `--all-extras` flag and adding the other feature flags manually.
>
> **Linux/Windows:** If you see a CUDA error during installation, make sure
> NVIDIA's [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) version
> **12.8** (or newer) is installed on your system.

### 3. Download Models

Download the required models via [uv tool](https://docs.astral.sh/uv/guides/tools/#installing-tools):

Via `huggingface-cli`:

```bash
uv tool install "huggingface-hub"

# IndexTTS-2.5
hf download IndexTeam/IndexTTS-2.5 --local-dir=checkpoints

# IndexTTS-2
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints_2
```

Or via `modelscope`:

```bash
uv tool install "modelscope"

# IndexTTS-2.5
modelscope download --model IndexTeam/IndexTTS-2.5 --local_dir checkpoints

# IndexTTS-2
modelscope download --model IndexTeam/IndexTTS-2 --local_dir checkpoints_2
```

> [!IMPORTANT]
> If the commands above aren't available, carefully read the `uv tool` output —
> it will tell you how to add the tools to your system's PATH.

> [!NOTE]
> Some small models are downloaded automatically on first run. If your network
> has slow access to HuggingFace, set a mirror before running the code:
>
> ```bash
> export HF_ENDPOINT="https://hf-mirror.com"
> ```

### 4. Check GPU Acceleration

To diagnose your environment and see which GPUs are detected, use the included
utility:

```bash
uv run tools/gpu_check.py
```

## 💻 Usage

### 🌐 Web Demo

```bash
# IndexTTS-2.5 (default)
uv run webui.py

# IndexTTS-2
uv run webui.py --version 2 --model_dir ./checkpoints_2
```

Open your browser and visit `http://127.0.0.1:7860` to see the demo.

You can adjust the settings to enable BF16 (IndexTTS-2.5) / FP16 (IndexTTS-2)
inference (lower VRAM usage), DeepSpeed acceleration, compiled CUDA kernels for
speed, etc. All available options can be seen via:

```bash
uv run webui.py -h
```

> [!IMPORTANT]
> **FP16/BF16** (half-precision) inference is faster and uses less VRAM, with
> very small quality loss.
>
> **DeepSpeed** *may* speed up inference on some systems, but it could also make
> it slower — it depends on your hardware, drivers and OS. Try both ways.
>
> All `uv` commands **automatically activate** the correct per-project virtual
> environment. Do *not* manually activate any environment before running `uv`
> commands, as that can cause dependency conflicts.

### 🚀 Serving with vLLM

For production deployment, see the [vLLM recipe for IndexTTS](https://recipes.vllm.ai/IndexTeam/IndexTTS-2.5).

### 📝 Python API

To run scripts, use `uv run <file.py>` so the code runs inside the `uv`
environment. You may also need to add the current directory to `PYTHONPATH`:

```bash
# IndexTTS2.5
PYTHONPATH="$PYTHONPATH:." uv run indextts/infer_v2_5.py \
  --cfg_path checkpoints/config.yaml \
  --model_dir checkpoints \
  --text "Hello world" \
  --lang EN
```

The default `--prompt_wav` lives in `examples/`, which is populated the first
time the WebUI starts. To fetch it without the WebUI:

```bash
uv run python -c "from indextts.utils.examples_downloader import ensure_examples_available; ensure_examples_available()"
```

For IndexTTS2, use the Python API below — `indextts/infer_v2.py` runs a
benchmark loop against a hardcoded `checkpoints/` directory, not the
`checkpoints_2` layout from step 3.

#### 0. Initialize IndexTTS

```python
# IndexTTS2
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints_2/config.yaml", model_dir="checkpoints_2", use_fp16=False, use_cuda_kernel=False, use_deepspeed=False)

# IndexTTS2.5
from indextts.infer_v2_5 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints", use_bf16=True)
```

#### 1. Voice cloning with a single reference audio

```python
text = "Translate for me, what is a surprise!"

# IndexTTS2
tts.infer(spk_audio_prompt='examples/voice_01.wav', text=text, output_path="gen.wav", verbose=True)

# IndexTTS2.5 (multilingual, with language selection)
tts.infer(spk_audio_prompt='examples/voice_01.wav', text=text, lang="EN", output_path="gen.wav", verbose=True)
```

#### 2. Emotion control with a separate emotional reference audio

```python
text = "酒楼丧尽天良，开始借机竞拍房间，哎，一群蠢货。"

# IndexTTS2
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", emo_audio_prompt="examples/emo_sad.wav", verbose=True)

# IndexTTS2.5
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, lang="ZH", output_path="gen.wav", emo_audio_prompt="examples/emo_sad.wav", verbose=True)
```

#### 3. Adjust emotion intensity with `emo_alpha`

When an emotional reference audio is specified, `emo_alpha` adjusts how much it
affects the output. Valid range: `0.0 - 1.0`, default: `1.0` (100%).

```python
text = "酒楼丧尽天良，开始借机竞拍房间，哎，一群蠢货。"

# IndexTTS2
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", emo_audio_prompt="examples/emo_sad.wav", emo_alpha=0.9, verbose=True)

# IndexTTS2.5
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", lang="ZH", emo_audio_prompt="examples/emo_sad.wav", emo_alpha=0.9, verbose=True)
```

#### 4. Emotion control with an emotion vector

You can omit the emotional reference audio and instead provide an 8-float list
specifying the intensity of each emotion, in the order
`[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]`.
Use `use_random` to introduce stoc

... (truncated, 12305 more characters)

## pyproject.toml

```
[project]
name = "indextts"
version = "2.0.0"
description = "IndexTTS2: A Breakthrough in Emotionally Expressive and Duration-Controlled Auto-Regressive Zero-Shot Text-to-Speech"
authors = [{ name = "Bilibili IndexTTS Team" }]
license = "LicenseRef-Bilibili-IndexTTS"
license-files = ["LICEN[CS]E*", "INDEX_MODEL_LICENSE*"]
readme = "README.md"
classifiers = [
  "Development Status :: 5 - Production/Stable",

  "Intended Audience :: Science/Research",
  "Intended Audience :: Developers",

  "Topic :: Scientific/Engineering",
  "Topic :: Scientific/Engineering :: Artificial Intelligence",

  "Natural Language :: English",
  "Natural Language :: Chinese (Simplified)",

  "Programming Language :: Python :: 3",

  "Operating System :: OS Independent",
]
requires-python = ">=3.10,<3.12"
dependencies = [
  # IMPORTANT: Always run `uv lock` or `uv lock --upgrade` to resolve dependencies
  # and update the lockfile after editing anything below.
  # WARNING: Ensure that you don't have a local `uv.toml` which overrides PyPI
  # while generating the lockfile: https://github.com/astral-sh/uv/issues/15741
  "accelerate==1.8.1",
  "cn2an==0.5.22",
  "cython==3.0.7",
  "descript-audiotools==0.7.2",
  "einops>=0.8.1",
  "ffmpeg-python==0.2.0",
  "fugashi>=1.2.0",
  "unidic-lite>=1.0.0",
  "g2p-en==2.1.0",
  "jieba==0.42.1",
  "json5==0.10.0",
  "keras==2.9.0",
  "librosa==0.10.2.post1",
  "matplotlib==3.10.0",
  "modelscope==1.27.0",
  "munch==4.0.0",
  "numba==0.63.0",
  "numpy==2.2.6",
  "omegaconf>=2.3.0",
  "opencv-python==4.9.0.80",
  "pandas==2.3.2",
  "safetensors==0.5.2",
  "sentencepiece>=0.2.1",
  "tensorboard==2.20.0",
  "textstat>=0.7.10",
  "tokenizers==0.21.0",
  "torch==2.8.*",
  "torchaudio==2.8.*",
  "requests>=2.28",
  "tqdm>=4.67.1",
  "transformers==4.52.1",
  "openai-whisper>=20231117",
  "fugashi[unidic-lite]",

  # Use "wetext" on Windows/Mac, otherwise "WeTextProcessing" on Linux.
  "wetext>=0.0.9; sys_platform != 'linux'",
  "WeTextProcessing; sys_platform == 'linux'",
]

[project.optional-dependencies]
# To install the WebUI support, use `uv sync --extra webui` (or `--all-extras`).
webui = [
  "gradio==5.45.0",
]
# To install the DeepSpeed support, use `uv sync --extra deepspeed` (or `--all-extras`).
deepspeed = [
  "deepspeed==0.17.1",
]
# To install the GPT2 acceleration engine, use `uv sync --extra accel` (or `--all-extras`).
# NOTE: flash-attn 2.8.3.post1 also requires triton at import time on Windows.
accel = [
  "flash-attn==2.8.3.post1",
  "nvidia-cuda-runtime-cu12",
  "nvidia-cudnn-cu12",
  "triton-windows==3.1.0.post17; sys_platform == 'win32'",
]
# To install torch.compile support for s2mel, use `uv sync --extra torch_compile` (or `--all-extras`).
# On Windows this is satisfied by the triton-windows package above.
torch_compile = [
  "triton-windows==3.1.0.post17; sys_platform == 'win32'",
]
test = [
  "pytest>=7.0",
]

[tool.pytest.ini_options]
markers = [
    "gpu: tests that require GPU and model checkpoints (deselect with '-m not gpu')",
]

[project.urls]
Homepage = "https://github.com/index-tts/index-tts"
Repository = "https://github.com/index-tts/index-tts.git"

[project.scripts]
# Set the installed binary names and entry points.
indextts = "indextts.cli:main"
indextts2 = "indextts.cli_v2:main"

[build-system]
# How to build the project as a CLI tool or PyPI package.
# NOTE: Use `uv tool install -e .` to install the package as a CLI tool.
requires = ["hatchling >= 1.27.0"]
build-backend = "hatchling.build"

[tool.uv.extra-build-dependencies]
# Build against our CUDA-enabled PyTorch: DeepSpeed picks its GPU targets from it,
# and flash-attn reads its version and C++ ABI flag to fetch a matching prebuilt
# wheel instead of compiling.
deepspeed = [{ requirement = "torch", match-runtime = true }]
flash-attn = [{ requirement = "torch", match-runtime = true }]

[tool.uv.sources]
# Install PyTorch with CUDA support on Linux/Windows (CUDA doesn't exist for Mac).
# NOTE: We must explicitly request them as `dependencies` above. These improved
# versions will not be selected if they're only third-party dependencies.
torch = [
  { index = "pytorch-cuda", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]
torchaudio = [
  { index = "pytorch-cuda", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]
torchvision = [
  { index = "pytorch-cuda", marker = "sys_platform == 'linux' or sys_platform == 'win32'" },
]

[[tool.uv.index]]
name = "pytorch-cuda"
# Use PyTorch built for NVIDIA Toolkit version 12.8.
# Available versions: https://pytorch.org/get-started/locally/
url = "https://download.pytorch.org/whl/cu128"
# Only use this index when explicitly requested by `tool.uv.sources`.
explicit = true

```

## Top-level layout

- .gitattributes (~2 lines)
- .github/ (dir, 3 files, ~110 lines)
- .gitignore (~38 lines)
- .python-version (~1 lines)
- archive/ (dir, 3 files, ~1196 lines)
- assets/ (dir, 11 files, ~0 lines)
- backends/ (dir, 49 files, ~7042 lines)
- checkpoints/ (dir, 1 files, ~1728 lines)
- cli_tests/ (dir, 6 files, ~5112 lines)
- DISCLAIMER (~43 lines)
- docs/ (dir, 6 files, ~3553 lines)
- examples/ (dir, 6 files, ~27 lines)
- indextts/ (dir, 225 files, ~63420 lines)
- LICENSE (~57 lines)
- LICENSE_ZH.txt (~52 lines)
- MANIFEST.in (~3 lines)
- pyproject.toml (~143 lines)
- README.md (~556 lines)
- tests/ (dir, 8 files, ~978 lines)
- tools/ (dir, 8 files, ~791 lines)
- uv.lock (~3049 lines)
- webui.py (~1377 lines)

