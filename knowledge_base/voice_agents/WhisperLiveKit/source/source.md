# QuentinFuxa/WhisperLiveKit
Source: https://github.com/QuentinFuxa/WhisperLiveKit
Kind: repo
Fetched: 2026-09-22T14:56:40.238891+00:00
Tool: git-clone
PDF: https://github.com/QuentinFuxa/WhisperLiveKit (no source.pdf fetched; see repo URL)

# QuentinFuxa/WhisperLiveKit

Commit: 363e4f6d029694d9c81ae548beddd9d3c88a3637

## README

### Powered by Leading Research:

- Simul-[Whisper](https://arxiv.org/pdf/2406.10052)/[Streaming](https://arxiv.org/abs/2506.17077) (SOTA 2025) - Ultra-low latency transcription using [AlignAtt policy](https://arxiv.org/pdf/2305.11408). 
- [NLLW](https://github.com/QuentinFuxa/NoLanguageLeftWaiting) (2025), based on [distilled](https://huggingface.co/entai2965/nllb-200-distilled-600M-ctranslate2) [NLLB](https://arxiv.org/abs/2207.04672) (2022, 2024) - Simulatenous translation from & to 200 languages.
- [WhisperStreaming](https://github.com/ufal/whisper_streaming) (SOTA 2023) - Low latency transcription using [LocalAgreement policy](https://www.isca-archive.org/interspeech_2020/liu20s_interspeech.pdf)
- [Streaming Sortformer](https://arxiv.org/abs/2507.18446) (SOTA 2025) - Advanced real-time speaker diarization
- [Qwen3-ASR-causal](https://github.com/QuentinFuxa/Qwen3-ASR-causal) (2026) - Causal streaming audio encoder for Qwen3-ASR: each audio block is encoded exactly once, constant compute per audio second, append-only transcripts.
- [AlignAtt4LLM](https://github.com/QuentinFuxa/Alignatt4LLM) ([IWSLT 2026](https://arxiv.org/abs/2606.03967)) - Simultaneous translation with decoder-only LLMs: attention-gated commits, append-only output.


> **Why not just run a simple Whisper model on every audio batch?** Whisper is designed for complete utterances, not real-time chunks. Processing small segments loses context, cuts off words mid-syllable, and produces poor transcription. WhisperLiveKit uses state-of-the-art simultaneous speech research for intelligent buffering and incremental processing.




### Architecture

<img alt="Architecture" src="https://raw.githubusercontent.com/QuentinFuxa/WhisperLiveKit/refs/heads/main/architecture.png" />

*The backend supports multiple concurrent users. Voice Activity Detection reduces overhead when no voice is detected.*



### Installation & Quick Start

```bash
pip install whisperlivekit
```

#### Quick Start

```bash



# Start the server — open http://localhost:8000 and start talking
wlk --model base --language en




# Auto-pull model and start server
wlk run whisper:tiny



# Transcribe a file (no server needed)
wlk transcribe meeting.wav



# Generate subtitles
wlk transcribe --format srt podcast.mp3 -o podcast.srt



# Manage models
wlk models                             # See what's installed
wlk pull large-v3                      # Download a model
wlk rm large-v3                        # Delete a model



# Benchmark speed and accuracy
wlk bench
```

#### API Compatibility

WhisperLiveKit exposes compatibility-oriented subsets of popular APIs:

```bash


# OpenAI-compatible REST API
curl http://localhost:8000/v1/audio/transcriptions -F file=@audio.wav



# Works with the OpenAI Python SDK
client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")



# Native WebSocket for real-time streaming
ws://localhost:8000/asr
```

Per-session WebSocket query parameters:

| param | example | effect |
|---|---|---|
| `language` | `?language=fr` | transcription language for this session (one shared engine serves mixed-language sessions) |
| `target_language` | `?target_language=de` | translation target for this session (server must run with `--target-language`) |
| `context` | `?context=WhisperLiveKit%2C+Qwen3-ASR` | terminology, names, or phrase-list text used to condition this session; supported by Whisper-family and SimulStreaming backends |
| `mode` | `?mode=diff` | incremental snapshot/diff protocol instead of resending the full state (experimental, for integrators building their own client, see `diff_protocol.py`); the bundled web UI uses `full` |
| `token` | `?token=...` | API token when the server runs with `--api-token` (also accepted as an `Authorization: Bearer` header) |

See [docs/API.md](docs/API.md) for the complete API reference.
For a native SwiftUI macOS client, see [macos/WhisperLiveKitMac](macos/WhisperLiveKitMac).

> - See [here](whisperlivekit/whisper/tokenizer.py) for the list of all available languages.
> - Check the [troubleshooting guide](docs/troubleshooting.md) for step-by-step fixes collected from recent GPU setup/env issues.
> - For HTTPS requirements, see the **Parameters** section for SSL configuration options.




#### Optional Dependencies

| Feature | `uv sync` | `pip install -e` |
|-----------|-------------|-------------|
| **Apple Silicon MLX Whisper backend** | `uv sync --extra mlx-whisper` | `pip install -e ".[mlx-whisper]"` |
| **FunASR SenseVoiceSmall** | `uv sync --extra funasr` | `pip install -e ".[funasr]"` |
| **Voxtral (MLX backend, Apple Silicon)** | `uv sync --extra voxtral-mlx` | `pip install -e ".[voxtral-mlx]"` |
| **CPU PyTorch stack** | `uv sync --extra cpu` | `pip install -e ".[cpu]"` |
| **CUDA 12.9 PyTorch stack** | `uv sync --extra cu129` | `pip install -e ".[cu129]"` |
| **Translation** | `uv sync --extra translation` | `pip install -e ".[translation]"` |
| **Sentence tokenizer** | `uv sync --extra sentence_tokenizer` | `pip install -e ".[sentence_tokenizer]"` |
| **Voxtral (HF backend)** | `uv sync --extra voxtral-hf` | `pip install -e ".[voxtral-hf]"` |
| **Qwen3-ASR vLLM (CUDA)** | `uv sync --extra qwen3-vllm` | `pip install -e ".[qwen3-vllm]"` |
| **Qwen3-ASR streaming (HF, CUDA/MPS/CPU)** | `uv sync --extra qwen3-streaming` | `pip install -e ".[qwen3-streaming]"` |
| **Qwen3-ASR vLLM Metal (Apple Silicon)** | Install vLLM with the official vllm-metal script first, then `uv sync --extra qwen3-vllm-metal` | Install vLLM with the official vllm-metal script first, then `pip install -e ".[qwen3-vllm-metal]"` |
| **Speaker diarization (Sortformer / NeMo 3)** | `uv sync --extra diarization-sortformer` | `pip install -e ".[diarization-sortformer]"` |
| *[Not recommended]* Speaker diarization with Diart (Python 3.11 or 3.12) | `uv sync --extra diarization-diart` | `pip install -e ".[diarization-diart]"` |
| **Canary-1b-v2 (NeMo, CUDA/CPU)** | `uv sync --extra canary` | `pip install -e ".[canary]"` |

The Diart profile is limited to Python 3.11 and 3.12 because Diart 0.9.2 requires NumPy below 2. Use Sortformer for diarization on Python 3.13.

Supported GPU profiles:

```bash


# Profile A: Sortformer diarization
uv sync --extra cu129 --extra diarization-sortformer



# Profile B: Voxtral HF + translation
uv sync --extra cu129 --extra voxtral-hf --extra translation



# Profile C: Qwen3-ASR vLLM
uv sync --extra qwen3-vllm
```

`qwen3-vllm` uses vLLM's CUDA wheel stack and must be installed in a separate environment from `cu129`. Several heavy extras (`voxtral-hf`, `qwen3-vllm-metal`, and the vLLM stacks) intentionally conflict with one another and must be installed in separate environments; the authoritative list is `[tool.uv].conflicts` in `pyproject.toml`. The `canary` extra conflicts with `voxtral-hf` and `qwen3-vllm-metal`, but is compatible with `diarization-sortformer` (both pull `nemo-toolkit[asr]`).

See **Parameters & Configuration** below on how to use them.

<p align="center">
<img src="benchmark_scatter_en_aware.png" alt="Speed vs Accuracy — English" width="700">
</p>
<p align="center">
<img src="benchmark_scatter_fr_aware.png" alt="Speed vs Accuracy — French" width="700">
</p>

Benchmarks use 6 minutes of public [LibriVox](https://librivox.org/) audiobook recordings per language (30s + 60s + 120s + 180s), with ground truth from [Project Gutenberg](https://www.gutenberg.org/). The figures above were measured on an NVIDIA H100 (CUDA); the qwen3 causal tower is English-only, so it only appears on the English chart. Fully reproducible with `python scripts/run_scatter_benchmark.py` (the script picks a matching combo set on Apple Silicon: mlx-whisper and voxtral-mlx instead of the CUDA-only backends). Raw results: [benchmarks/h100_scatter/](benchmarks/h100_scatter/).
We are actively looking for benchmark results on other hardware (different NVIDIA GPUs, Apple Silicon chips, cloud instances). If you run the benchmarks on your machine, please share your results via an issue or PR!


#### Use it to capture audio from web pages.

Go to `chrome-extension` for instructions.

<p align="center">
<img src="https://raw.githubusercontent.com/QuentinFuxa/WhisperLiveKit/refs/heads/main/chrome-extension/demo-extension.png" alt="WhisperLiveKit Demo" width="600">
</p>




### Voxtral Backend

WhisperLiveKit supports [Voxtral Mini](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602),
a 4B-parameter speech model from Mistral AI that natively handles 100+ languages with automatic
language detection. Whisper also supports auto-detection (`--language auto`), but Voxtral's per-chunk
detection is more reliable and does not bias towards English.

```bash


# Apple Silicon (native MLX, recommended)
pip install -e ".[voxtral-mlx]"
wlk --backend voxtral-mlx



# Linux/GPU (HuggingFace transformers)
pip install transformers torch
wlk --backend voxtral
```

Voxtral uses its own streaming policy and does not use LocalAgreement or SimulStreaming.
See [BENCHMARK.md](BENCHMARK.md) for performance numbers.



### FunASR / SenseVoiceSmall

Install the optional backend and run
[SenseVoiceSmall](https://huggingface.co/FunAudioLLM/SenseVoiceSmall) through
WLK's existing LocalAgreement and VAC/VAD pipeline:

```bash
pip install "whisperlivekit[funasr]"
wlk --backend funasr --language auto
```

Use a verified local model snapshot without executing remote model code:

```bash
wlk --backend funasr --model_dir /path/to/SenseVoiceSmall --language yue
```

The initial integration supports SenseVoiceSmall transcription in Mandarin
(`zh`), Cantonese (`yue`), English (`en`), Japanese (`ja`), Korean (`ko`), and
automatic detection. FunASR uses LocalAgreement only; selecting it with the
default policy switches that policy automatically. It does not support
`--direct-english-translation`, and WLK remains responsible for voice activity
control rather than enabling FunASR's internal VAD. This compatibility contract
does not cover arbitrary FunASR models. SenseVoiceSmall is distributed under
its [model license](https://github.com/modelscope/FunASR/blob/main/MODEL_LICENSE).



### Qwen3-ASR streaming (HF Transformers)

`qwen3-streaming` runs Qwen3-ASR through plain HF Transformers with a
bounded-recompute audio cache: the pretrained audio to

... (truncated, 18450 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=83.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "whisperlivekit"
version = "0.2.26"
description = "Real-time speech-to-text models"
readme = "README.md"
authors = [{ name = "Quentin Fuxa" }]
license = "Apache-2.0"
license-files = ["LICENSE"]
requires-python = ">=3.11, <3.14"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
]
dependencies = [
    "fastapi>=0.141.1",
    "librosa",
    "soundfile",
    "uvicorn",
    "websockets",
    "huggingface-hub>=0.25.0",
    "faster-whisper>=1.2.0",
    "torch>=2.6.0",
    "torchaudio>=2.0.0",
    "tqdm",
    "tiktoken",
    "python-multipart>=0.0.31",
    "starlette>=1.3.1",
]

[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "datasets>=2.14",
    "librosa",
    "deepgram-sdk==7.8.1",
    "psutil>=5.9",
    "matplotlib>=3.8",
]
translation = ["nllw"]
sentence_tokenizer = ["mosestokenizer", "wtpsplit"]
funasr = ["funasr~=1.4.1"]
mlx-whisper = [
    'mlx>=0.11.0; sys_platform == "darwin" and platform_machine == "arm64"',
    'mlx-whisper>=0.4.0; sys_platform == "darwin" and platform_machine == "arm64"',
]
voxtral-mlx = [
    'mlx>=0.11.0; sys_platform == "darwin" and platform_machine == "arm64"',
    'mlx-whisper>=0.4.0; sys_platform == "darwin" and platform_machine == "arm64"',
    "mistral-common[audio]",
]
# In-process MLX translation backend via mlx-lm (Hunyuan-MT as first config;
# TranslateGemma etc. via the config registry). Requires mlx-lm>=0.31.3 which
# pulls transformers>=5; conflicts with qwen3-asr-causal[streaming] which pins
# transformers==4.57.6. Declare the conflict below; install only one.
mlx-llm-mt = [
    'mlx>=0.31.2,<0.32; sys_platform == "darwin" and platform_machine == "arm64"',
    'mlx-lm>=0.31.3,<0.32; sys_platform == "darwin" and platform_machine == "arm64"',
]
voxtral-hf = [
    "transformers>=5.2.0; python_version >= '3.10'",
    "mistral-common[audio]",
    "accelerate>=0.12",
]
qwen3-vllm-metal = [
    "qwen3-asr-causal[metal]>=0.1.0",
]
qwen3-vllm = [
    "qwen3-asr-causal[vllm]>=0.1.0",
]
qwen3-streaming = [
    "qwen3-asr-causal[streaming]>=0.1.0",
]
listen = ["sounddevice>=0.4.6"]
cpu = ["torch>=2.6.0", "torchaudio>=2.0.0"]
cu129 = [
    "torch>=2.6.0",
    "torchaudio>=2.0.0",
    'triton>=2.0.0; platform_machine == "x86_64" and (sys_platform == "linux" or sys_platform == "linux2")',
]
diarization-sortformer = [
    "nemo-toolkit[asr]>=3.0,<4",
    "onnx>=1.22.0",
]
canary = [
    "nemo-toolkit[asr]>=3.0,<4",
    "kaldialign>=0.12.0",
    "onnx>=1.22.0",
]
diarization-diart = [
    "diart==0.9.2; python_version < '3.13'",
    "matplotlib<3.11; python_version < '3.13'",
    "torch<2.9.0; python_version < '3.13'",
    "torchaudio<2.9.0; python_version < '3.13'",
    "torchvision<0.24.0; python_version < '3.13'",
]

[dependency-groups]
dev = ["rich>=14.3.3", "ruff==0.16.*"]

[tool.uv]
# Resolve Diart's Python <3.13 dependency graph separately from Python 3.13.
environments = ["python_version < '3.13'", "python_version >= '3.13'"]
# Override the retired nightly URL inherited from qwen3-asr-causal.
override-dependencies = [
    "vllm-metal[stt] @ https://github.com/vllm-project/vllm-metal/releases/download/v0.2.0/vllm_metal-0.2.0-cp312-cp312-macosx_11_0_arm64.whl ; python_version == '3.12' and sys_platform == 'darwin' and platform_machine == 'arm64'",
]
conflicts = [
    [
        { extra = "cpu" },
        { extra = "cu129" },
    ],
    [
        { extra = "diarization-diart" },
        { extra = "cu129" },
    ],
    [
        { extra = "voxtral-hf" },
        { extra = "diarization-sortformer" },
    ],
    [
        { extra = "qwen3-vllm" },
        { extra = "cu129" },
    ],
    [
        { extra = "qwen3-vllm" },
        { extra = "voxtral-hf" },
    ],
    [
        { extra = "qwen3-vllm" },
        { extra = "diarization-diart" },
    ],
    [
        { extra = "qwen3-vllm" },
        { extra = "qwen3-vllm-metal" },
    ],
    [
        { extra = "qwen3-streaming" },
        { extra = "qwen3-vllm-metal" },
    ],
    [
        { extra = "qwen3-vllm-metal" },
        { extra = "voxtral-hf" },
    ],
    [
        { extra = "qwen3-vllm-metal" },
        { extra = "diarization-sortformer" },
    ],
    [
        { extra = "qwen3-vllm-metal" },
        { extra = "diarization-diart" },
    ],
    [
        { extra = "qwen3-streaming" },
        { extra = "voxtral-hf" },
    ],
    [
        { extra = "canary" },
        { extra = "voxtral-hf" },
    ],
    [
        { extra = "canary" },
        { extra = "qwen3-vllm-metal" },
    ],
    [
        { extra = "mlx-llm-mt" },
        { extra = "qwen3-streaming" },
    ],
    [
        { extra = "mlx-llm-mt" },
        { extra = "qwen3-vllm" },
    ],
    [
        { extra = "mlx-llm-mt" },
        { extra = "qwen3-vllm-metal" },
    ],
]

[tool.uv.sources]
qwen3-asr-causal = { path = "third_party/qwen3-asr-causal", editable = true }
torch = [
    { index = "pytorch-cpu", extra = "cpu", marker = "platform_system != 'Darwin'" },
    { index = "pytorch-cpu", extra = "diarization-diart", marker = "platform_system != 'Darwin'" },
    { index = "pytorch-cu129", extra = "cu129", marker = "platform_system == 'Linux' and platform_machine == 'x86_64'" },
]
torchaudio = [
    { index = "pytorch-cpu", extra = "cpu", marker = "platform_system != 'Darwin'" },
    { index = "pytorch-cpu", extra = "diarization-diart", marker = "platform_system != 'Darwin'" },
    { index = "pytorch-cu129", extra = "cu129", marker = "platform_system == 'Linux' and platform_machine == 'x86_64'" },
]
torchvision = [
    { index = "pytorch-cpu", extra = "diarization-diart", marker = "platform_system != 'Darwin'" },
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[[tool.uv.index]]
name = "pytorch-cu129"
url = "https://download.pytorch.org/whl/cu129"
explicit = true

[project.urls]
Homepage = "https://github.com/QuentinFuxa/WhisperLiveKit"

[project.scripts]
whisperlivekit-server = "whisperlivekit.basic_server:main"
wlk = "whisperlivekit.cli:main"
wlk-test = "whisperlivekit.test_client:main"

[tool.ruff]
target-version = "py311"
line-length = 120
exclude = [".git", "__pycache__", "build", "dist", ".eggs", ".claude", "scripts", "third_party", "run_benchmark.py"]

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
ignore = ["E501", "E741"]
per-file-ignores = {"whisperlivekit/whisper/*" = ["F401", "F841", "E731", "W"], "whisperlivekit/simul_whisper/mlx/*" = ["F401", "E731", "W"], "whisperlivekit/simul_whisper/mlx_encoder.py" = ["E731", "F821"], "whisperlivekit/silero_vad_iterator.py" = ["F401"]}

[tool.setuptools]
packages = [
    "whisperlivekit",
    "whisperlivekit.diarization",
    "whisperlivekit.simul_whisper",
    "whisperlivekit.simul_whisper.mlx",
    "whisperlivekit.whisper",
    "whisperlivekit.whisper.assets",
    "whisperlivekit.whisper.normalizers",
    "whisperlivekit.web",
    "whisperlivekit.local_agreement",
    "whisperlivekit.qwen3_streaming",
    "whisperlivekit.voxtral_mlx",
    "whisperlivekit.silero_vad_models",
    "whisperlivekit.benchmark",
]

[tool.setuptools.package-data]
whisperlivekit = ["web/*.html", "web/*.css", "web/*.js", "web/src/*.svg", "calibrations/*.json"]
"whisperlivekit.whisper.assets" = ["*.tiktoken", "*.npz"]
"whisperlivekit.whisper.normalizers" = ["*.json"]
"whisperlivekit.silero_vad_models" = ["*.jit", "*.onnx"]

```

## Top-level layout

- .dockerignore (~14 lines)
- .github/ (dir, 11 files, ~730 lines)
- .gitignore (~139 lines)
- .gitmodules (~3 lines)
- architecture.png (~0 lines)
- benchmark_scatter_en_aware.png (~0 lines)
- benchmark_scatter_fr_aware.png (~0 lines)
- benchmarks/ (dir, 30 files, ~5098 lines)
- CHANGES.md (~3 lines)
- chrome-extension/ (dir, 11 files, ~102 lines)
- CITATION.cff (~20 lines)
- CLAUDE.md (~28 lines)
- CODE_OF_CONDUCT.md (~83 lines)
- compose.yml (~52 lines)
- CONTRIBUTING.md (~51 lines)
- demo.png (~0 lines)
- DEV_NOTES.md (~91 lines)
- Dockerfile (~83 lines)
- Dockerfile.cpu (~80 lines)
- docs/ (dir, 13 files, ~2026 lines)
- JARVISLAB_AGENTS.md (~186 lines)
- LICENSE (~210 lines)
- macos/ (dir, 11 files, ~1899 lines)
- MANIFEST.in (~1 lines)
- pyproject.toml (~253 lines)
- README.md (~577 lines)
- scripts/ (dir, 11 files, ~2030 lines)
- SECURITY.md (~13 lines)
- tests/ (dir, 27 files, ~8395 lines)
- third_party/ (dir, 0 files, ~0 lines)
- uv.lock (~13252 lines)
- whisperlivekit/ (dir, 125 files, ~133842 lines)
- wlk-architecture.svg (~375 lines)
- wlk.png (~0 lines)

