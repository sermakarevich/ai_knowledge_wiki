> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** NVIDIA NeMo Speech is a PyTorch toolkit for researchers and developers to create, customize, and deploy ASR, TTS, and Speech-LLM models from existing code and pre-trained checkpoints.
## Key points
- NeMo Speech targets researchers and PyTorch developers working on ASR, TTS, and Speech LLMs, reusing existing code and pre-trained checkpoints to create, customize, and deploy models (README.md:52-54).
- The repo has pivoted to audio, speech, and multimodal LLMs; v2.7.3 was the final pre-split release with additional modalities and v3.0.0 is the current NeMo Speech release (README.md:21-25, README.md:42-43).
- Minimum stack is Python 3.12+, PyTorch 2.7+, and NVIDIA GPU + CUDA for training, while the actively tested baseline is Python 3.13 with PyTorch 2.11/CUDA 12.9 or PyTorch 2.12/CUDA 13.2 pinned in `uv.lock` (README.md:63-67).
- NeMo Speech installs on top of an existing Python/PyTorch/CUDA stack without replacing it via the pip fallback, whereas `uv sync` reproduces the tested stack from `uv.lock` (README.md:67, README.md:84, README.md:121-127).
- Three install paths are supported: `uv sync` from source (recommended), prebuilt/buildable Docker images, and PyPI pip fallback with `asr`/`tts` plus `cu12`/`cu13` extras (README.md:86-94, README.md:100-117, README.md:121-134).
- Checkpoints loading with `torch.load` may require `weights_only=False` via env var `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1`, with a warning to use it only with trusted files due to arbitrary-code-execution risk (README.md:69-73).
- Current checkpoints/demos are published via the HuggingFace Nemotron-Speech collection and build.nvidia.com entries, including MagpieTTS, Parakeet, Canary, and Nemotron-Speech-Streaming/VoiceChat updates from 2025-2026 (README.md:16-17, README.md:27-48).
---
## Scope and positioning
Built for researchers and PyTorch developers working on Speech models including Automatic Speech Recognition (ASR), Text to Speech (TTS), and Speech LLMs (README.md:52-54). It helps users "efficiently create, customize, and deploy new AI models by leveraging existing code and pre-trained model checkpoints" (README.md:52-54). Technical docs live at the NeMo Speech Developer Documentation site (README.md:56-57). This repo pivoted to focus on "audio, speech, and multimodal LLMs"; for other modalities the chunk points to v2.7.3 (README.md:42-43).
## Releases and updates
NeMo Speech 3.0 is release `v3.0.0` in NGC container `26.07.00`; the last pre-split NeMo release was `v2.7.3` in NGC container `26.04` (README.md:21-25). Recent checkpoint updates noted in the chunk (README.md:27-48):
| Date | Item |
| --- | --- |
| 2026-07 | MagpieTTS v2607, 3 new languages (Ar, Ko, Pt) + 9 existing (En, Es, De, Fr, Vi, It, Zh, Hi, Ja) |
| 2026-06 | Nemotron-3.5-ASR-Streaming-0.6B, 40 languages, 80ms-1s latency, cache-aware Fastconformer |
| 2026-04 | Parakeet-unified-en-0.6b, offline + streaming (160ms min) with punctuation/capitalization |
| 2026-03 | Nemotron 3 VoiceChat Early Access on Nemotron Nano v2 LLM backbone; Nemotron-Speech-Streaming v2603 retrain; MagpieTTS v2602 (9 languages) |
| 2026-01 | Nemotron-Speech-Streaming latency-accuracy Pareto checkpoint; MagpieTTS v2512 |
| 2025-08 | Parakeet V3 + Canary V2, 25 European languages |
| 2025-06 | Canary-Qwen-2.5B, 5.63% WER on English Open ASR Leaderboard |
## Requirements
Minimum versions (README.md:63-65):
- `Python 3.12 or above`
- `PyTorch 2.7 or above (CPU, CUDA, etc. — your choice)`
- `NVIDIA GPU + CUDA (required for training; recommended for inference)`
Tested/supported baseline pinned in `uv.lock` and shipped in the official container: `Python 3.13`, `PyTorch 2.11 with CUDA 12.9` or `PyTorch 2.12 with CUDA 13.2` (README.md:67). `torch.load` note verbatim (README.md:69-73):
```bash
TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1
```
Set it before code using `torch.load` only when a checkpoint requires `weights_only=False`, and only with trusted files (README.md:70-73).
## Developer documentation
| Version | Description |
| ------- | ----------- |
| 3.0.0 (latest release) | [NeMo Speech 3.0.0 documentation](https://docs.nvidia.com/nemo/speech/3.0.0/) |
| Nightly | [Documentation for the latest `main` branch](https://docs.nvidia.com/nemo/speech/nightly/) |
Source: README.md:77-80.
## Install — from source with uv (recommended)
Verbatim (README.md:88-94):
```bash
git clone https://github.com/NVIDIA-NeMo/Speech.git
cd Speech
uv sync --extra all --extra cu13     # CUDA 13.x (recommended) — use --extra cu12 for CUDA 12.x
```
Details: installs Python 3.13, PyTorch 2.12, CUDA 13.2 into `.venv/` editable; add `--group test` or `--group docs`; run via `uv run <cmd>` or `source .venv/bin/activate`; `cu12`/`cu13` mutually exclusive on Linux (exactly one, default `cu13`); `--locked --python 3.13` reproduces the container/CI baseline (README.md:94). SpeechLM2/Automodel runs without compiled deps and optionally uses accelerated backends (`Transformer Engine`, `FlashAttention`, `Mamba`, `grouped-GEMM/MoE`, `DeepEP`) from `compiled` (Hopper/Blackwell) or `compiled-a100` (A100) extras built by `docker/Dockerfile` with `GPU_TARGET=h100plus` / `a100` (README.md:96).
## Install — Docker
Latest prebuilt image `26.07.00` (README.md:100-106):
```bash
docker pull nvcr.io/nvidia/nemo-speech:26.07.00
docker run --rm -it --gpus all -v "$PWD:/workspace" nvcr.io/nvidia/nemo-speech:26.07.00 bash
```
Build from source, CUDA 13 / H100+ default (README.md:110-115):
```bash
git clone https://github.com/NVIDIA-NeMo/Speech.git
cd Speech
docker buildx build -f docker/Dockerfile -t nemo-speech .          # CUDA 13 / H100+ (default)
docker run --rm -it --gpus all -v "$PWD:/workspace" nemo-speech bash
```
A100: set `GPU_TARGET=a100`, works with CUDA 12 and 13 (13 default/recommended); see `docker/Dockerfile` header for `BASE_IMAGE`, `GPU_TARGET` (README.md:117).
## Install — from PyPI with pip (fallback)
Verbatim (README.md:121-134):
```bash
uv pip install 'nemo-toolkit[asr,tts]'   # or plain: pip install 'nemo-toolkit[asr,tts]'
```
Install your own PyTorch ≥ 2.7 first; this keeps your build (README.md:121). Do not use `uv sync --locked` here (it would replace the stack); use `uv pip`/`pip` (README.md:127). For the pinned PyTorch build add the CUDA extra plus wheel index (README.md:129-134):
```bash
pip install 'nemo-toolkit[asr,tts,cu13]' --extra-index-url https://download.pytorch.org/whl/cu132   # CUDA 13.x
pip install 'nemo-toolkit[asr,tts,cu12]' --extra-index-url https://download.pytorch.org/whl/cu129   # CUDA 12.x
```
| Flag/extra | Meaning |
| --- | --- |
| `asr`, `tts` | Feature extras installed from PyPI |
| `cu12` / `cu13` | CUDA 12.x / 13.x PyTorch wheel variant (mutually exclusive on Linux) |
| `--extra-index-url .../cu132` / `.../cu129` | Required wheel index since pip/uv pip ignore uv project index config |
| `--extra all` | uv-from-source full extras set |
## Contributing and license
Community contributions welcome via `CONTRIBUTING.md` (README.md:136-139). Licensed under Apache License 2.0 (README.md:141-143).
**Covers:** README.md (project badges, HuggingFace collection, Updates 2025-2026, Introduction, Requirements, Developer Documentation table, Install via uv/Docker/PyPI, Contribute, Licenses)
