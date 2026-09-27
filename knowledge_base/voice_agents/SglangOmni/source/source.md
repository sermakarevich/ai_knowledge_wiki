# sgl-project/sglang-omni
Source: https://github.com/sgl-project/sglang-omni
Kind: repo
Fetched: 2026-09-22T14:41:23.610024+00:00
Tool: git-clone
PDF: https://github.com/sgl-project/sglang-omni

# sgl-project/sglang-omni

Commit: 072753f80709d81f3af4f1a77a1c048a81fbe4bd

## README

<div align="center">
<img src="https://raw.githubusercontent.com/sgl-project/sglang-omni/main/docs/_static/image/sgl-omni-logo.svg" alt="logo" width="400"></img>

<p>
<a href="https://pypi.org/project/sglang-omni/"><img src="https://img.shields.io/pypi/v/sglang-omni?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI" alt="PyPI"></a>
<a href="https://github.com/sgl-project/sglang-omni/stargazers"><img src="https://img.shields.io/github/stars/sgl-project/sglang-omni?style=for-the-badge&logo=github&label=stars" alt="GitHub stars"></a>
<a href="https://github.com/sgl-project/sglang-omni/blob/main/LICENSE"><img src="https://img.shields.io/github/license/sgl-project/sglang-omni?style=for-the-badge" alt="license"></a>
<a href="https://github.com/sgl-project/sglang-omni/issues"><img src="https://img.shields.io/github/issues-closed-raw/sgl-project/sglang-omni?style=for-the-badge&label=closed%20issues" alt="closed issues"></a>
<a href="https://github.com/sgl-project/sglang-omni/issues"><img src="https://img.shields.io/github/issues-raw/sgl-project/sglang-omni?style=for-the-badge&label=open%20issues" alt="open issues"></a>
<a href="https://deepwiki.com/sgl-project/sglang-omni"><img src="https://img.shields.io/badge/Ask-DeepWiki-087fca?style=for-the-badge" alt="Ask DeepWiki"></a>
</p>

</div>

--------------------------------------------------------------------------------

<p align="center">
<a href="https://lmsys.org/blog/"><b>Blog</b></a> |
<a href="https://sgl-project.github.io/sglang-omni/"><b>Documentation</b></a> |
<a href="#quick-start"><b>Quick Start</b></a> |
<a href="https://sgl-project.github.io/sglang-omni/index.html"><b>Cookbook</b></a> |
<a href="https://github.com/sgl-project/sglang"><b>SGLang</b></a> |
<a href="https://slack.sglang.io"><b>Join Slack</b></a>
</p>

<p align="center">
⭐ <b><a href="https://github.com/sgl-project/sglang-omni/stargazers">Star SGLang-Omni</a> to help more builders discover open infrastructure for multimodal and speech serving!</b>
</p>

## News

- [2026/09] 🐧 Day-0 support for [AuK](https://huggingface.co/tencent/AuK) and [AuK-Flash](https://huggingface.co/tencent/AuK-Flash): text + voice instructions → 24 kHz speech on `/v1/audio/speech`, audio + editing instructions → edited speech on `/generate`. \[[Cookbook](https://sgl-project.github.io/sglang-omni/cookbook/auk.html)\]
- [2026/09] 🚀 SGLang-Omni **v0.1.6** is on [PyPI](https://pypi.org/project/sglang-omni/). Install with `uv pip install --prerelease=allow "sglang-omni==0.1.6"`. \[[Installation](https://sgl-project.github.io/sglang-omni/get_started/installation.html)\]
- [2026/08] 🎵 Day-0 support for [MiniMax Music 3](https://huggingface.co/MiniMaxAI/MiniMax-Music3): lyrics + caption → 32 kHz stereo song on `/v1/audio/speech`. \[[Cookbook](https://sgl-project.github.io/sglang-omni/cookbook/minimax_music3.html)\]
- [2026/08] 🚀 TTS architecture refactor: shared pipeline state, engine construction, reference encoding, capability metadata, and vocoder scheduling. \[[Roadmap](https://github.com/sgl-project/sglang-omni/issues/985)\] \[[Blog](https://github.com/zhaochenyang20/Awesome-ML-SYS-Tutorial/blob/main/sglang/sglang-omni/tts-refactor.md)\]
- [2026/06] 🔥 MOSS-TTS Local Transformer v1.5 on SGLang-Omni with native-streaming 48 kHz speech. \[[Blog](https://lmsys.org/blog/2026-06-17-moss-tts-local-v15/)\] \[[Cookbook](https://sgl-project.github.io/sglang-omni/cookbook/moss_tts_local.html)\]
- [2026/06] 🔥 Higgs Audio v3 TTS for real-time, controllable speech. \[[Blog](https://lmsys.org/blog/2026-06-04-higgs-audio-v3-tts/)\] \[[Cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html)\]

## About

SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models. Its design target is multi-stage decoding: generation split across heterogeneous stages with different compute patterns, dependency structures, and resource needs. SGLang-Omni owns the pipeline topology, stage lifecycle, inter-stage transport, model-family integration layer, and OpenAI-compatible serving surface, while composing with [SGLang](https://github.com/sgl-project/sglang) for high-performance autoregressive scheduling and model execution where applicable.

- **Multi-stage runtime**: SGLang-Omni models generation as coordinated stages: preprocessing, encoders, autoregressive engines, talkers, decoders, vocoders, and aggregators.
- **Stage-specialized scheduling**: Each stage runs behind a scheduler matched to its workload, from SGLang-backed autoregressive scheduling to lightweight preprocessing and streaming vocoder loops.
- **Transport-aware execution**: A control plane coordinates requests while the relay data plane moves tensor payloads across shared-memory, NCCL, NIXL, and Mooncake backends.
- **API surface**: OpenAI-compatible endpoints expose multimodal chat, speech generation, batch speech, streaming speech, uploaded voices, and transcription.

## What SGLang-Omni Serves

- **Omni chat and speech**: [Qwen3-Omni](https://sgl-project.github.io/sglang-omni/cookbook/qwen3_omni.html), [Ming-Omni](https://sgl-project.github.io/sglang-omni/cookbook/ming_omni.html) — multimodal in, text/audio out.
- **Music generation**: [MiniMax Music 3](https://sgl-project.github.io/sglang-omni/cookbook/minimax_music3.html) — lyrics + caption → 32 kHz stereo song.
- **Speech generation**: [Higgs Audio v3](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html), [MOSS-TTS](https://sgl-project.github.io/sglang-omni/cookbook/moss_tts.html), [MOSS-TTS Local](https://sgl-project.github.io/sglang-omni/cookbook/moss_tts_local.html), [Fish Speech S2-Pro](https://sgl-project.github.io/sglang-omni/cookbook/fishaudio_s2_pro.html), [Qwen3-TTS](https://sgl-project.github.io/sglang-omni/cookbook/qwen3_tts.html), [Voxtral TTS](https://sgl-project.github.io/sglang-omni/cookbook/voxtral_tts.html), [Ming-Omni-TTS](https://sgl-project.github.io/sglang-omni/cookbook/ming_tts.html), [dots.tts](https://sgl-project.github.io/sglang-omni/cookbook/dots_tts.html), [ZONOS2](https://sgl-project.github.io/sglang-omni/cookbook/zonos2.html) — `/v1/audio/speech`, batch, streaming, uploaded voices.
- **Audio transcription and diarization**: [Qwen3-ASR](https://sgl-project.github.io/sglang-omni/cookbook/qwen3_asr.html), [Fun-ASR](https://sgl-project.github.io/sglang-omni/cookbook/fun_asr.html), [ARK-ASR](https://sgl-project.github.io/sglang-omni/cookbook/arkasr.html), [MOSS-Transcribe-Diarize](https://sgl-project.github.io/sglang-omni/cookbook/moss_transcribe_diarize.html) via `/v1/audio/transcriptions`. MOSS-TD supports speaker labels and timestamps (`response_format=verbose_json`).
- **SGLang-Omni Router**: Multi-worker OpenAI-compatible front door — health, readiness, lifecycle, capability discovery. [Router guide](https://sgl-project.github.io/sglang-omni/basic_usage/omni_router.html).

## Hardware Support

| Backend | Status | Notes |
|---------|--------|-------|
| **NVIDIA CUDA** | Supported | Default backend with full model coverage. |
| **Apple Silicon** | Experimental | Qwen3-ASR runs through native MLX or Torch MPS on macOS arm64. Install with [`install.sh`](./install.sh) and follow the [Qwen3-ASR guide](./docs/cookbook/qwen3_asr.md#apple-silicon-mlx). |
| **Intel GPU (XPU)** | Experimental | Intel Arc GPUs via PyTorch XPU. **Qwen3-ASR, Qwen3-TTS, and Qwen3-Omni serve end-to-end** (Omni thinker via multi-XPU tensor parallelism). Install per [Intel XPU guide](./docs/get_started/installation_xpu.md); the backend is auto-detected. |

Additional model guides, including experimental and research-oriented paths, are available in the [Cookbook](https://sgl-project.github.io/sglang-omni/).

## Quick Start

- **macOS Apple Silicon:** from a checkout, run [`./install.sh`](./install.sh) for a one-command Homebrew + uv setup. See [installation](./docs/get_started/installation.md#macos-apple-silicon).
- [Installation](https://sgl-project.github.io/sglang-omni/get_started/installation.html)
- [TTS usage](https://sgl-project.github.io/sglang-omni/basic_usage/tts.html)
- [Qwen3-Omni usage](https://sgl-project.github.io/sglang-omni/basic_usage/qwen3_omni.html)
- [Qwen3-ASR cookbook](https://sgl-project.github.io/sglang-omni/cookbook/qwen3_asr.html)
- [MOSS-Transcribe-Diarize cookbook](https://sgl-project.github.io/sglang-omni/cookbook/moss_transcribe_diarize.html)
- [Omni router](https://sgl-project.github.io/sglang-omni/basic_usage/omni_router.html)
- [Developer reference](https://sgl-project.github.io/sglang-omni/developer_reference/main.html)

## Community & Support

SGLang-Omni welcomes contributors working on inference systems, kernels, scheduling, inter-stage communication, model runners and cache efficiency, model integration, benchmarking, production deployment. Join the [SGLang Slack](https://slack.sglang.io) or read the [developer reference](https://sgl-project.github.io/sglang-omni/developer_reference/main.html).

Organizations interested in supporting SGLang-Omni, TTS, or omni model serving can contact Chenyang Zhao at [zhaochenyang@lmsys.org](mailto:zhaochenyang@lmsys.org).

## Acknowledgments

SGLang-Omni builds on the SGLang ecosystem and on open model work from the TTS, speech, and omni-model communities. We thank the model teams, systems contributors, and partner organizations helping make open multimodal serving faster, more reliable, and easier to extend.


## pyproject.toml

```
[build-system]
requires = ["setuptools>=77.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "sglang-omni"
dynamic = ["version"]
description = "Multi-stage pipeline framework for omni models"
readme = "README.md"
license = "Apache-2.0"
license-files = ["LICENSE"]
requires-python = ">=3.10,<3.13"
dependencies = [
    # Core dependencies
    "pyzmq>=25.0.0",          # ZMQ messaging for control plane
    "msgpack>=1.0.0",         # Message serialization
    "msgspec",                # msgspec.Struct support
    "numpy>=1.24.0",          # Array operations
    "pydantic>=2.0.0",        # Data validation and serialization
    "PyYAML>=6.0",            # YAML config parsing
    "pybase64>=1.4.0",        # Fast base64 decoding for inline media payloads
    "torch==2.13.0",
    "torchvision==0.28.0",
    "accelerate>=0.27.0",     # init_empty_weights for meta initialization
    "transformers==5.12.1",  # Match the pinned sglang stack
    "safetensors>=0.4.3",     # Direct weight loading
    "pillow>=10.0.0",         # Required by AutoImageProcessor
    "huggingface-hub[hf_xet]>=0.36.0",# HF model downloads with Xet transport
    "datasets>=2.14.0",       # Arrow-based SeedTTS dataset loading
    "fastapi>=0.110.0",       # OpenAI-compatible API adapter
    "uvicorn>=0.23.0",        # ASGI server for FastAPI
    # note (yexiaodong): SGLang's PyPI wheel has unconditional CUDA dependencies,
    # so Apple Silicon installs this exact tag from source with the all_mps extra.
    "sglang==0.5.19; sys_platform != 'darwin' or platform_machine != 'arm64'",
    "mlx>=0.32.0; sys_platform == 'darwin' and platform_machine == 'arm64'",  # floor enforced by SGLang's MLX runtime gate
    "mlx-lm; sys_platform == 'darwin' and platform_machine == 'arm64'",
    "flashinfer_python[cu13]==0.6.18; sys_platform != 'darwin' or platform_machine != 'arm64'",  # sglang pin. Do NOT add flashinfer-cubin: PyPI has no matching cubin, and any leftover cubin wheel fails MiniMax DIT import.
    "cache-dit==1.3.0",      # MiniMax Music 3 DIT (hard import, not optional)
    "addict==2.4.0",         # sglang.multimodal_gen server_args; MiniMax DIT import
    "imageio==2.36.0",       # sglang.multimodal_gen vision utils; MiniMax DIT import
    "imageio-ffmpeg==0.5.1", # Pinned with the sglang diffusion extra
    "flash-attn-4>=4.0.0b18; sys_platform != 'darwin' or platform_machine != 'arm64'",  # Required by sglang, pairs with cutlass-dsl 4.6.2
    "kernels>=0.14.1,<0.15; sys_platform != 'darwin' or platform_machine != 'arm64'",  # Match the pinned sglang stack
    "nixl-cu13>=1.1.0; sys_platform != 'darwin' or platform_machine != 'arm64'",  # CUDA 13 relay wheel; the generic nixl/-cu12 wheel breaks on cu130
    "mooncake-transfer-engine-cuda13>=0.3.10; sys_platform != 'darwin' or platform_machine != 'arm64'",  # CUDA 13 relay wheel; generic mooncake-transfer-engine pulls cu12 and breaks import mooncake on cu130
    "logger",
    "httpx",
    "xxhash>=3.0.0",
    # Note: (Jiaxin Deng) the documented install line for the Qwen3-TTS model
    # package is `--no-deps qwen-tts==0.1.1`, and --no-deps is exactly what drops
    # sox, so `import qwen_tts` raises ModuleNotFoundError before a worker binds
    # a port.
    "sox>=1.4.1",
    "av>=16.1.0",
    "qwen-vl-utils==0.0.11",
    "numba==0.65.1",  # Match the pinned sglang stack
    "librosa>=0.11.0",
    "pandas",
    "tabulate",
    "typer>=0.9.0",
    "openai==2.6.1",
    "openai-harmony==0.0.4",
    "soundfile>=0.12.0",
    "mistral_common[audio]>=1.11.0",
    # /v1/realtime — server-side turn detection
    "silero-vad>=5.1",
    "onnxruntime-gpu>=1.17; sys_platform != 'darwin' or platform_machine != 'arm64'",  # CUDAExecutionProvider for the FP32 Smart Turn model
    "onnxruntime>=1.17; sys_platform == 'darwin' and platform_machine == 'arm64'",  # CPUExecutionProvider on Apple Silicon
    "websockets>=12.0",       # FastAPI WebSocket library + example clients
    # Testing
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "jiwer",
    "zhon>=2.0.2",            # note (yzxiao): shared Chinese WER normalization uses zhon.hanzi punctuation.
    "scipy>=1.10.0",
    "openai-whisper==20250625",
    # SeedTTS speaker similarity (WavLM-large SV head). The pip-installed
    # package supplies s3prl.upstream.wavlm.hubconf at runtime, so no source
    # clone is required.
    "s3prl>=0.4.18",
    # S2-Pro
    "tiktoken",
    "hydra-core",
    "omegaconf",
    "torchaudio==2.11.0",
    "torchcodec==0.15.0",
    # Gradio playground
    "gradio>=4.0.0",
    # note (yexiaodong): dots.tts pulls Pynini, whose OpenFst build is not
    # available on Apple arm64 and is unrelated to the Qwen3-ASR path.
    "dots.tts==0.2.1; sys_platform != 'darwin' or platform_machine != 'arm64'",
    # Ming-Omni
    "diffusers==0.37.0",      # Omni's own Ming-Omni pin; not an sglang core dependency
    "x-transformers",          # Ming talker rotary embeddings
    # note (yexiaodong): ZONOS2 text normalization pulls Pynini/OpenFst, which
    # has no usable Apple arm64 wheel and is unrelated to the Qwen3-ASR path.
    "nemo_text_processing==1.2.0; sys_platform != 'darwin' or platform_machine != 'arm64'",
]

[project.optional-dependencies]
audar-tts = [
    "llama-cpp-python==0.3.34",
    "neucodec==0.0.6",
    "torchao==0.13.0",  # NeuCodec's torchtune imports the removed torchao.dtypes.nf4tensor.
]
fun-cosyvoice3 = [
    "conformer==0.3.2",
    "HyperPyYAML==1.2.3",
    "pyworld==0.3.4",
    "setuptools<80",  # Note (yexiaodong): pyworld 0.3.4 imports pkg_resources.
    "wetext==0.0.4",
    "inflect==7.3.1",
    "gdown==5.1.0",
    "wget==3.2",
    "lightning==2.6.5",
    "matplotlib",
]

minicpm-o = [
    "einops>=0.8.1",
    "onnx>=1.18.0",
]

[project.scripts]
sgl-omni = "sglang_omni.cli:app"
sgl-omni-router-py = "sglang_omni_router.python.serve:main"

[project.entry-points."sglang.serve_backends"]
omni = "sglang_omni.cli.sglang_backend:create_backend"

[project.urls]
Documentation = "https://sgl-project.github.io/sglang-omni/"
Issues = "https://github.com/sgl-project/sglang-omni/issues"
Repository = "https://github.com/sgl-project/sglang-omni"

[tool.uv]
# The dependency set pins CUDA-13-only wheels (mooncake-transfer-engine-cuda13,
# nixl-cu13, flash-attn-4); without this, uv's universal resolution also
# solves for platforms those wheels do not support and fails.
environments = [
    "sys_platform == 'linux'",
]
override-dependencies = [
    "protobuf>=6.31.1,<7.0.0; sys_platform != 'darwin' or platform_machine != 'arm64'",
    "protobuf>=7.35.1,<8.0.0; sys_platform == 'darwin' and platform_machine == 'arm64'",
]

[tool.pytest.ini_options]
pythonpath = ["."]
markers = [
    "benchmark: performance benchmark tests (may require GPU and long runtime)",
    "tts_stage(name): select an in-file TTS benchmark CI stage",
    "accelerator: requires accelerator hardware",
]

[tool.ruff.lint]
exclude = ["tests/**"]
select = [
    "B006",     # Mutable argument defaults
    "B009",     # Constant-name getattr without a default
    "B010",     # Constant-name setattr
    "E722",     # No bare except
    "F403",     # No wildcard imports
    "N801",     # Class names
    "N815",     # Class-scope variable names
    "N816",     # Module-scope variable names
    "PGH004",   # No blanket noqa
    "RUF008",   # Mutable dataclass defaults
    "SIM115",   # Context managers for files (not sockets/CUDA streams)
]

[tool.setuptools.packages.find]
where = ["."]
include = [
    "sglang_omni",
    "sglang_omni.*",
    "sglang_omni_router.python",
    "sglang_omni_router.python.*",
]
namespaces = true

[tool.setuptools.dynamic]
version = {attr = "sglang_omni.__version__"}

# Non-Python data files that must ship with the wheel.
[tool.setuptools.package-data]
"sglang_omni.models.auk" = ["LICENSE"]
"sglang_omni.models.fishaudio_s2_pro" = ["fish_speech/configs/*.yaml"]
"sglang_omni.models.higgs_tts" = ["configs/*.json"]
"sglang_omni.models.minicpm_o.components.token2wav" = ["THI

... (truncated, 95 more characters)
```

## Top-level layout

- .claude/ (dir, 10 files, ~3924 lines)
- .dockerignore (~9 lines)
- .editorconfig (~25 lines)
- .github/ (dir, 50 files, ~5070 lines)
- .gitignore (~67 lines)
- .isort.cfg (~4 lines)
- .pre-commit-config.yaml (~83 lines)
- AGENTS.md (~4 lines)
- benchmarks/ (dir, 74 files, ~30802 lines)
- CLAUDE.md (~4 lines)
- docker/ (dir, 5 files, ~334 lines)
- docs/ (dir, 91 files, ~17338 lines)
- examples/ (dir, 62 files, ~3685 lines)
- install.sh (~344 lines)
- LICENSE (~202 lines)
- OmniTyper/ (dir, 42 files, ~6805 lines)
- playground/ (dir, 33 files, ~9942 lines)
- pyproject.toml (~191 lines)
- pyproject_cpu.toml (~117 lines)
- pyproject_npu.toml (~162 lines)
- pyproject_rocm.toml (~121 lines)
- pyproject_xpu.toml (~117 lines)
- README.md (~85 lines)
- scripts/ (dir, 7 files, ~2001 lines)
- sglang_omni/ (dir, 641 files, ~175634 lines)
- sglang_omni_router/ (dir, 72 files, ~38646 lines)
- tests/ (dir, 533 files, ~185370 lines)

