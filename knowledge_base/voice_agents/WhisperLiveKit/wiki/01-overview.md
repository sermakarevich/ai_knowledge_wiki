[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** WhisperLiveKit is a real-time streaming speech-transcription/translation kit with a multi-backend server, `wlk` CLI, and WebSocket plus OpenAI-compatible API, built on simultaneous-speech research for low-latency incremental processing.
## Key points
- WhisperLiveKit does real-time streaming transcription/translation using simultaneous-speech research (Simul-Whisper/Streaming with AlignAtt, NLLB-based NLLW, WhisperStreaming with LocalAgreement, Streaming Sortformer diarization, Qwen3-ASR-causal, AlignAtt4LLM) instead of naively running Whisper on every audio batch, which loses context and cuts words mid-syllable (01-overview.md:9-17).
- The backend supports multiple concurrent users and uses Voice Activity Detection to reduce overhead when no voice is detected (01-overview.md:26).
- Installation is `pip install whisperlivekit` and the `wlk` CLI covers server start (`wlk --model base --language en`, `wlk run whisper:tiny`), offline file transcription (`wlk transcribe meeting.wav`), subtitle generation (`wlk transcribe --format srt podcast.mp3 -o podcast.srt`), model management (`wlk models`, `wlk pull large-v3`, `wlk rm large-v3`), and benchmarking (`wlk bench`) (01-overview.md:32-72).
- The server exposes an OpenAI-compatible REST endpoint (`POST http://localhost:8000/v1/audio/transcriptions`), works with the OpenAI Python SDK (`OpenAI(base_url="http://localhost:8000/v1", api_key="unused")`), and a native real-time WebSocket (`ws://localhost:8000/asr`) with per-session query parameters `language`, `target_language`, `context`, `mode`, and `token` (01-overview.md:76-103).
- Optional backends and stacks are installed as extras via `uv sync --extra <name>` or `pip install -e ".[<name>]"`, including `mlx-whisper`, `funasr`, `voxtral-mlx`, `cpu`, `cu129`, `translation`, `sentence_tokenizer`, `voxtral-hf`, `qwen3-vllm`, `qwen3-streaming`, `qwen3-vllm-metal`, `diarization-sortformer`, `diarization-diart`, and `canary` (01-overview.md:117-132).
- Heavy extras have environment conflicts declared in `[tool.uv].conflicts` in `pyproject.toml`: `qwen3-vllm` needs a separate environment from `cu129`, `voxtral-hf`/`qwen3-vllm-metal`/vLLM stacks conflict with one another, and `canary` conflicts with `voxtral-hf` and `qwen3-vllm-metal` but is compatible with `diarization-sortformer` (01-overview.md:155).
- Accuracy/speed claims are backed by reproducible LibriVox/Project Gutenberg scatter benchmarks (6 minutes of audiobook audio per language: 30s + 60s + 120s + 180s, H100-measured, raw results in `benchmarks/h100_scatter/`, reproducible with `python scripts/run_scatter_benchmark.py`), plus companion clients including the bundled web UI at `http://localhost:8000`, a native SwiftUI macOS client, and a `chrome-extension` audio-capture demo (01-overview.md:159-176).
---
## Research backends
WhisperLiveKit is explicitly positioned as simultaneous-speech research applied to streaming, not chunked offline Whisper (01-overview.md:17):
- Simul-Whisper/Streaming (SOTA 2025) — ultra-low latency transcription using AlignAtt policy (01-overview.md:9).
- NLLW (2025), based on distilled NLLB (2022, 2024) — simultaneous translation from and to 200 languages (01-overview.md:10).
- WhisperStreaming (SOTA 2023) — low-latency transcription using LocalAgreement policy (01-overview.md:11).
- Streaming Sortformer (SOTA 2025) — real-time speaker diarization (01-overview.md:12).
- Qwen3-ASR-causal (2026) — causal streaming audio encoder where each audio block is encoded exactly once, with constant compute per audio second and append-only transcripts (01-overview.md:13).
- AlignAtt4LLM (IWSLT 2026) — simultaneous translation with decoder-only LLMs via attention-gated commits and append-only output (01-overview.md:14).
## Architecture
- Architecture diagram is referenced by URL with the caption: "The backend supports multiple concurrent users. Voice Activity Detection reduces overhead when no voice is detected." (01-overview.md:24-26).
## Installation & Quick Start
Verbatim install (01-overview.md:32-33):
```bash
pip install whisperlivekit
```
Verbatim quick-start commands (01-overview.md:39-72):
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
## API compatibility
Compatibility-oriented subsets of popular APIs (01-overview.md:76-93):
```bash
# OpenAI-compatible REST API
curl http://localhost:8000/v1/audio/transcriptions -F file=@audio.wav

# Works with the OpenAI Python SDK
client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

# Native WebSocket for real-time streaming
ws://localhost:8000/asr
```
Per-session WebSocket query parameters (01-overview.md:95-103):
| param | example | effect |
|---|---|---|
| `language` | `?language=fr` | transcription language for this session (one shared engine serves mixed-language sessions) |
| `target_language` | `?target_language=de` | translation target for this session (server must run with `--target-language`) |
| `context` | `?context=WhisperLiveKit%2C+Qwen3-ASR` | terminology, names, or phrase-list text used to condition this session; supported by Whisper-family and SimulStreaming backends |
| `mode` | `?mode=diff` | incremental snapshot/diff protocol instead of resending the full state (experimental, for integrators building their own client, see `diff_protocol.py`); the bundled web UI uses `full` |
| `token` | `?token=...` | API token when the server runs with `--api-token` (also accepted as an `Authorization: Bearer` header) |
Complete API reference is in `docs/API.md` (01-overview.md:105); available languages are listed in `whisperlivekit/whisper/tokenizer.py` (01-overview.md:108); GPU setup/env fixes are in `docs/troubleshooting.md` (01-overview.md:109); SSL/HTTPS options are in the Parameters section (01-overview.md:110).
## Optional dependencies & GPU profiles
Optional-dependency matrix, verbatim (01-overview.md:117-132):
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
Notes verbatim in substance (01-overview.md:134-155):
- Diart profile is limited to Python 3.11 and 3.12 because Diart 0.9.2 requires NumPy below 2; Sortformer is the diarization path on Python 3.13.
- Supported GPU profiles:
```bash
# Profile A: Sortformer diarization
uv sync --extra cu129 --extra diarization-sortformer

# Profile B: Voxtral HF + translation
uv sync --extra cu129 --extra voxtral-hf --extra translation

# Profile C: Qwen3-ASR vLLM
uv sync --extra qwen3-vllm
```
- `qwen3-vllm` uses vLLM's CUDA wheel stack and must be installed in a separate environment from `cu129`; conflicting heavy extras are declared in `[tool.uv].conflicts` in `pyproject.toml`.
## Benchmarks
- Charts `benchmark_scatter_en_aware.png` and `benchmark_scatter_fr_aware.png` show speed vs. accuracy for English and French (01-overview.md:159-164).
- Method: 6 minutes of public LibriVox audiobook recordings per language (30s + 60s + 120s + 180s), ground truth from Project Gutenberg, measured on NVIDIA H100 (CUDA); the qwen3 causal tower is English-only so it appears only on the English chart (01-overview.md:166).
- Reproduction: `python scripts/run_scatter_benchmark.py` (picks mlx-whisper and voxtral-mlx on Apple Silicon instead of CUDA-only backends); raw results in `benchmarks/h100_scatter/`; other-hardware results solicited via issue/PR (01-overview.md:166-167).
- Voxtral performance numbers are in `BENCHMARK.md` (01-overview.md:203).
## Companion clients
- Web-page audio capture: instructions under `chrome-extension`, with demo image `chrome-extension/demo-extension.png` (01-overview.md:170-176).
- Native SwiftUI macOS client at `macos/WhisperLiveKitMac` (01-overview.md:106).
- Bundled web UI served at `http://localhost:8000` uses `full` state protocol rather than experimental `diff` (01-overview.md:42-102).
## Voxtral backend
- Supports Voxtral Mini (4B-parameter Mistral AI speech model) with 100+ languages and automatic language detection; per-chunk detection is described as more reliable than Whisper `--language auto` and not biased toward English (01-overview.md:183-186).
- Verbatim (01-overview.md:188-200):
```bash
# Apple Silicon (native MLX, recommended)
pip install -e ".[voxtral-mlx]"
wlk --backend voxtral-mlx

# Linux/GPU (HuggingFace transformers)
pip install transformers torch
wlk --backend voxtral
```
- Voxtral uses its own streaming policy and does not use LocalAgreement or SimulStreaming (01-overview.md:202).
## FunASR / SenseVoiceSmall
- Optional backend runs SenseVoiceSmall through WLK's existing LocalAgreement and VAC/VAD pipeline (01-overview.md:209-211).
- Verbatim (01-overview.md:213-222):
```bash
pip install "whisperlivekit[funasr]"
wlk --backend funasr --language auto
```
```bash
wlk --backend funasr --model_dir /path/to/SenseVoiceSmall --language yue
```
- Supports transcription in Mandarin (`zh`), Cantonese (`yue`), English (`en`), Japanese (`ja`), Korean (`ko`), and automatic detection; FunASR uses LocalAgreement only and selecting it with the default policy switches that policy automatically (01-overview.md:224-227).
- Does not support `--direct-english-translation`; WLK keeps voice-activity control rather than enabling FunASR's internal VAD; the compatibility contract does not cover arbitrary FunASR models; SenseVoiceSmall has its own model license (01-overview.md:227-231).
## Qwen3-ASR streaming — chunk truncated
- The chunk introduces `qwen3-streaming` as Qwen3-ASR through plain HF Transformers with a bounded-recompute audio cache, but the sentence is cut mid-phrase at "the pretrained audio to" (01-overview.md:235-239); no further claims from that section are included.
## Truncation note
- Truncated in the source chunk and therefore not covered here: the remainder of the Qwen3-ASR streaming section after 01-overview.md:239, and the macro-component listing cut after `top-level-files/` at 01-overview.md:240-243.
**Covers:** repo overview grounded in README-level install/usage/architecture material and the files it names: `pyproject.toml` (`[tool.uv].conflicts`, extras), `docs/API.md`, `docs/troubleshooting.md`, `whisperlivekit/whisper/tokenizer.py`, `diff_protocol.py`, `BENCHMARK.md`, `benchmarks/h100_scatter/`, `scripts/run_scatter_benchmark.py`, `macos/WhisperLiveKitMac`, `chrome-extension/`.
