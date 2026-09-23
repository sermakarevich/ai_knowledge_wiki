> PDF location: https://github.com/krafton-ai/Raon-Speech (no source.pdf fetched; see Source field below)

# krafton-ai/Raon-Speech
Source: https://github.com/krafton-ai/Raon-Speech
Kind: repo
Fetched: 2026-09-22T14:38:12.633919+00:00
Tool: git-clone

# krafton-ai/Raon-Speech

Commit: afec41185e27653aa905d4ad28a7b8497681275e

## README

# Raon-Speech

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/Raon-Speech-Gradient-White.png">
    <img src="assets/Raon-Speech-Gradient-Black.png" alt="Raon-Speech Logo" width="360">
  </picture>
</div>
<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/Raon-Speechchat-Gradient-White.png">
    <img src="assets/Raon-Speechchat-Gradient-Black.png" alt="Raon-SpeechChat Logo" width="360">
  </picture>
</div>

<p align="center">
  <a href="https://www.krafton.ai/ko/"><img src="https://img.shields.io/badge/Homepage-KRAFTON%20AI-blue?style=flat&logo=google-chrome&logoColor=white" alt="Homepage"></a>
  <a href="https://github.com/krafton-ai/Raon-Speech"><img src="https://img.shields.io/badge/GitHub-Raon%20Speech-white?style=flat&logo=github&logoColor=black" alt="GitHub"></a>
  <a href="https://huggingface.co/KRAFTON"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-KRAFTON-yellow?style=flat" alt="Hugging Face"></a>
  <a href="https://x.com/Krafton_AI"><img src="https://img.shields.io/badge/X-KRAFTON%20AI-white?style=flat&logo=x&logoColor=black" alt="X"></a>
</p>

**Links**
- GitHub: https://github.com/krafton-ai/Raon-Speech
- Official Demo: https://raon.krafton.ai
- Hugging Face Org: https://huggingface.co/KRAFTON
- Speech model card: https://huggingface.co/KRAFTON/Raon-Speech-9B
- SpeechChat (Full-Duplex) model card: https://huggingface.co/KRAFTON/Raon-SpeechChat-9B
- Technical Report: https://huggingface.co/KRAFTON/Raon-Speech-9B/resolve/main/Technical_Report_Raon_Speech.pdf

Raon is a speech model built on HuggingFace Ecosystem.  
This repo contains two tracks:

- Raon-Speech (Offline SpeechLM): `TTS`, `STT`, `SpeechChat`, `TextQA`
- Raon-SpeechChat (Offline/Realtime Full-Duplex)

Both tracks share the same core model family and processor stack under `src/raon/`.

## Key Features

- **SpeechLLM Model:** Raon-Speech is a 9B bilingual (English/Korean) SpeechLM for speech understanding, answering, and generation.
- **Full-Duplex Model:** Raon-SpeechChat extends Raon-Speech to natural real-time full-duplex conversation and shows strong interaction quality, especially on turn-taking, backchanneling, and interruption handling.
- **Training Scale:** Raon-Speech is trained on 1M+ hours of curated English-Korean speech-text data and achieves state-of-the-art average performance across 42 speech and text benchmarks against similarly sized baselines. Raon-SpeechChat is continually trained on 116K hours of time-aligned dialogue data.
- **System Design:** The system is built with a staged LLM-to-SpeechLM training recipe and a full-duplex design based on causal streaming, interleaved speech-text modeling, explicit interaction-state modeling, and text lookahead.
- **Task Coverage:** Unified multi-task support for `STT`, `TTS`, `TextQA`, and `SpeechChat`, with optional speaker-conditioned TTS and TTS continuation from reference audio.
- **Transformers Integration:** Hugging Face Transformers integration via `AutoModel.from_pretrained(..., trust_remote_code=True)`.
- **Open Release:** We open-source model checkpoints, the training and inference pipeline, an interactive demo, and three Korean speech benchmarks: KVoiceBench, KOpenAudioBench, and KMMAU.

## Benchmark Results

Overall performance comparison of Raon-Speech and Raon-SpeechChat against baseline models across diverse benchmarks.

<div align="center">
  <img src="https://huggingface.co/KRAFTON/Raon-Speech-9B/resolve/main/assets/raon-speech-speechchat.png" alt="Raon-Speech Benchmark Results" width="800">
</div>

Raon-Speech is optimized for low-latency, real-time speech generation while maintaining strong performance across ASR, speech generation, spoken QA, audio understanding, and text QA tasks. In the benchmarks above, Raon-Speech shows consistently high cross-domain scores, while Raon-SpeechChat performs strongly on conversational speech capabilities such as pause handling, backchanneling, smooth turn-taking, interruption handling, overlap robustness, and multi-turn dialogue. 

On single-GPU streaming TTS setups, the model runs faster than real time on both RTX 6000 Pro and L40S, with sub-second time-to-first-token latency. Measured with LibriSpeech `test-clean` samples on single-GPU setups via streaming TTS. All values are averaged.

| Metric | RTX 6000 Pro Blackwell | L40S |
|---|---:|---:|
| `RTF` | `0.27` (`3.7x` real-time) | `0.45` (`2.2x` real-time) |
| `TTFT` | `617 ms` | `887 ms` |
| `TBT` | `135 ms` | `233 ms` |

- `RTF`: Real-Time Factor. Lower is faster; values below `1.0` indicate faster-than-real-time synthesis.
- `TTFT`: Time to First Token.
- `TBT`: Time Between Tokens.

## Requirements

- Python `>=3.11`
- CUDA GPU recommended (`bfloat16` / `float16`)
- PyTorch + Torchaudio matching your CUDA environment

## Model Loading (Local or Hugging Face Hub)

All model entry points accept either:

- local checkpoint directory
- Hugging Face `repo_id` (downloaded automatically by `from_pretrained`)

Examples:

```bash
# Edit preset variables in the script first, then run:
bash scripts/infer.sh
# or
bash scripts/duplex_infer.sh
```

```python
from raon import RaonPipeline

pipe = RaonPipeline("KRAFTON/Raon-Speech-9B", device="cuda", dtype="bfloat16")
# or
pipe = RaonPipeline("KRAFTON/Raon-SpeechChat-9B", device="cuda", dtype="bfloat16")
```

If you want to pre-download first:

```bash
hf download KRAFTON/Raon-Speech-9B --local-dir /path/to/model_dir
# or
hf download KRAFTON/Raon-SpeechChat-9B --local-dir /path/to/model_dir
```

## Execution Modes

### Mode 1: `raon` installed (recommended)

After `pip install -e .` (or `uv sync`), all entry points are supported:

- `scripts/infer.sh`, `scripts/duplex_infer.sh`
- `scripts/train.sh`, `scripts/duplex_train.sh`
- `demo/run_gradio_demo.sh`, `demo/run_gradio_duplex_demo.sh`
- Python API: `from raon import RaonPipeline`

### Mode 2: without `raon` install

Supported:

- Raon-Speech Gradio demo (`demo/gradio_demo.py`) has a fallback that loads Hub remote code when `raon` import fails.
  Run directly from HF repo:

```bash
# from repo root
bash demo/run_gradio_demo.sh
```

- Pure Transformers flow using Hub remote code (advanced):
  `AutoModel.from_pretrained(..., trust_remote_code=True)`.

  See examples: `examples/message_example.ipynb` and `examples/duplex_example.ipynb`.
  Minimal pipeline load without `raon` install:

```python
import torch
from transformers import AutoConfig
from transformers.dynamic_module_utils import get_class_from_dynamic_module

MODEL_ID = "KRAFTON/Raon-Speech-9B"

config = AutoConfig.from_pretrained(MODEL_ID, trust_remote_code=True)
RaonPipeline = get_class_from_dynamic_module(
    "modeling_raon.RaonPipeline",
    MODEL_ID,
    revision=getattr(config, "_commit_hash", None),
)

pipe = RaonPipeline(MODEL_ID, device="cuda", dtype="bfloat16")
```

Not supported as-is:

- `python -m raon.*` module commands (used by `scripts/*.sh`)
- Raon-SpeechChat (Full-duplex) realtime demo runtime (`demo/gradio_duplex_demo.py`) because runtime code imports `raon.*` modules.

## Environment Setup

### Option A: `venv` + `pip`

```bash
git clone https://github.com/krafton-ai/Raon-Speech
cd Raon-Speech
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Option B: `uv`

```bash
git clone https://github.com/krafton-ai/Raon-Speech
cd Raon-Speech
uv sync
```

### Demo dependencies (optional)

The realtime full-duplex demo needs extra packages (`sglang`, `gradio`, `fastapi`, `uvicorn`):

```bash
pip install -e ".[demo]"
# or
uv sync --extra demo
```

### FlashAttention (optional)

If you want to use FlashAttention during training, install it separately:

```bash
pip install flash-attn
```

## Project Layout

```text
Raon-Speech/
├── src/raon/                 # package code
│   ├── models/               # RaonModel / RaonDuplexModel
│   ├── modules/              # audio encoder, tokenizer, speaker encoder, etc.
│   ├── utils/                # processor, datasets, losses, prompts, special tokens
│   ├── train.py              # SpeechLLM training entry
│   ├── duplex_train.py       # Full-duplex training entry
│   ├── generate.py           # SpeechLLM JSONL inference entry
│   ├── duplex_generate.py    # Full-duplex inference entry
│   └── pipeline.py           # high-level API (RaonPipeline)
├── scripts/                  # shell wrappers
├── demo/                     # Gradio demos
├── config/                   # inference configs
├── data/                     # sample datasets
└── examples/                 # notebooks and scripts
```

## Model Architecture

- One shared backbone: `RaonModel` (LM backbone + audio encoder + Mimi codec path).
- Two model types:
  `raon` (Raon-Speech) and `raon_duplex` (Raon-SpeechChat).
- Main trainable blocks include text/audio alignment and audio code prediction
  (`input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor`).

## SpeechLLM

### Data Format (JSONL)

Each line is one sample.

| Field | Type | Description |
|---|---|---|
| `conversations` | `list[dict]` | turns with `from` (`human`/`gpt`) and `value` |
| `audios` | `list[str]` | audio paths consumed by `<audio>` tags in order |
| `speaker_ref_audios` | `list[str]` | optional speaker reference audio for TTS |
| `channel` | `str` | `tts`, `stt`, `speech-chat`, `textqa` |
| `system` | `str` | optional system prompt |

Sample eval data is under `data/speechllm/eval`.

### Inference

```bash
bash scripts/infer.sh
```

- task defaults come from `config/infer.yaml`
- edit the preset variables at the top of `scripts/infer.sh` for quick runs
- `--attn_implementation` controls attention backend (default `sdpa`; use `fa` for FlashAttention)
- `--data_dir` is scanned for JSONL files, and each line is treated as one sample.

Advanced CLI example:

```bash
python -m raon.generate \
  --model_path /path/to/model \
  --data_dir /path/to/data_dir \
  --output_dir /path/to/output_dir \
  --config /path/to/config.yaml \
  --batch_size 4 \
  --attn_implementation sdpa
```

### Pipeline API

```python
from raon import RaonPipeline

pipe = RaonPipeline("/path/to/model", device="cuda", dtype="bfloat16", config="/path/to/config.yaml")

text = pipe.stt("/path/to/stt.wav")
audio, sr = pipe.tts("Hello!", speaker_audio="/path/to/speaker_ref.wav")
ans1 = pipe.speech_chat("/path/to/speech-chat.wav")
ans2 = pipe.textqa("What did the speaker say?", audio="/path/to/textqa.wav")

pipe.save_audio((audio, sr), "/path/to/tts.wav")
```

Continuation TTS is also supported:

```python
audio, sr = pipe.tts_continuation(
    target_text="Continue this sentence.",
    ref_audio="/path/to/speaker_ref.wav",
    ref_text="Optional transcription of ref audio.",
)
```

See:

- `examples/message_example.py`
- `examples/message_example.ipynb`

### Training

```bash
bash scripts/train.sh
```

Common options:

- edit the preset variables at the top of `scripts/train.sh`
- `NPROC_PER_NODE` controls multi-GPU torchrun
- `MASTER_PORT` sets the torchrun rendezvous port
- `USE_SPEAKER_EMBEDDING` toggles speaker-conditioning inputs

Notes:

- Current training code freezes these modules: `audio_encoder`, `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor`, `speaker_encoder`
- Default training attention implementation is `sdpa`; to use FlashAttention, pass `--attn_implementation fa`

## Full-Duplex

### Data Format (JSONL)

Training (`duplex_train.py`) expects one JSON object per line with stereo audio metadata.

Required top-level fields:

| Field | Type | Description |
|---|---|---|
| `audio_path` | `str` | Path to stereo wav (`2` channels). |
| `language` | `str` | Language code (for prompt selection), e.g. `eng`, `kor`. |
| `channel` | `str` | Duplex channel type, e.g. `full_duplex` or `duplex_instruct`. |
| `speak_first` | `list[int or bool]` | Per-channel initial speaking mode for the two channels. `1`/`true` means that

... (truncated, 4685 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "raon"
version = "0.1.0"
description = "RAON: speechllm fine-tuning and inference for speech generation tasks"
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
license = { text = "Apache-2.0" }
dependencies = [
    "accelerate>=1.10.1",
    "einops",
    "kernels",
    "numpy",
    "pydantic>=2.11.10",
    "requests",
    "soundfile>=0.13.1",
    "speechbrain",
    "tensorboard",
    "torch",
    "torchaudio",
    "transformers>=4.57.1,<5.0",
    "tqdm",
    "ipykernel>=7.0.1",
    "datasets>=3.0.0",
]

[project.optional-dependencies]
demo = [
    "fastapi>=0.115.0",
    "gradio>=4.0.0",
    "sglang==0.5.9",
    "uvicorn[standard]>=0.30.0",
]
dev = [
    "mypy>=1.11.2",
    "pytest>=8.0.0",
    "pytest-forked>=1.6.0",
    "ruff>=0.7.0",
]

[project.urls]
Homepage = "https://github.com/YOUR_ORG/raon"
Repository = "https://github.com/YOUR_ORG/raon"

[tool.setuptools]
packages = { find = { where = ["src"], include = ["raon*"] } }
include-package-data = true

[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (downloads models, runs inference on CPU)",
]

[tool.ruff]
line-length = 125
target-version = "py311"

[tool.ruff.format]
indent-style = "space"
quote-style = "double"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "Q"]
ignore = ["E203", "E402"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["E402", "F401", "F403", "F811"]

[tool.ruff.lint.isort]
known-first-party = ["raon", "demo"]

[tool.mypy]
python_version = "3.11"
warn_unused_configs = true
ignore_missing_imports = true
disallow_untyped_defs = true
warn_return_any = true
warn_unused_ignores = false
show_error_codes = true

```

## Top-level layout

- .gitignore (~216 lines)
- assets/ (dir, 4 files, ~0 lines)
- config/ (dir, 2 files, ~56 lines)
- data/ (dir, 39 files, ~62 lines)
- demo/ (dir, 19 files, ~4434 lines)
- examples/ (dir, 3 files, ~943 lines)
- LICENSE (~178 lines)
- NOTICE (~39 lines)
- pyproject.toml (~88 lines)
- README.md (~481 lines)
- requirements.txt (~17 lines)
- scripts/ (dir, 5 files, ~266 lines)
- src/ (dir, 34 files, ~16119 lines)

