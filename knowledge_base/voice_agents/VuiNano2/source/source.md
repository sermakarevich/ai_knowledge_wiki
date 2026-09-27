PDF: https://github.com/fluxions-ai/vui
# fluxions-ai/vui
Source: https://github.com/fluxions-ai/vui
Kind: repo
Fetched: 2026-09-22T14:54:59.485548+00:00
Tool: git-clone

# fluxions-ai/vui

Commit: 4dfd4ffd91da407b80d5ce7eb35d0ede287b3294

## README

<p align="center">
  <a href="https://fluxions.ai"><img src="docs/fxlogo.png" alt="fluxions.ai" height="64"></a>
</p>

<h1 align="center">Vui — Streaming Conversational Voice Assistant</h1>

<p align="center"><strong>Powered by Vui Nano — a small, context-aware text-to-speech model trained on real conversations: 219M active parameters (305M total), Apache 2.0, voice cloning, real-time streaming, runs on CPU</strong></p>

<p align="center"><em>Pronounced "vooey"</em> (rhymes with <em>Louie</em>) · by <a href="https://fluxions.ai">fluxions.ai</a></p>

<p align="center">
  <a href="https://fluxions.ai/talk"><img src="https://img.shields.io/badge/%F0%9F%8E%99%EF%B8%8F%20Try%20it%20live-fluxions.ai%2Ftalk-brightgreen?style=for-the-badge" alt="Try it live"></a>
  <a href="https://huggingface.co/fluxions/vui"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Model-yellow?style=for-the-badge" alt="Hugging Face"></a>
  <a href="https://discord.fluxions.ai"><img src="https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white&style=for-the-badge" alt="Discord"></a>
</p>

<p align="center"><strong>🎙️ Try it live at <a href="https://fluxions.ai/talk">fluxions.ai/talk</a></strong></p>

<table align="center"><tr><td>
  <video src="https://github.com/user-attachments/assets/d04de946-3b39-4fc1-bbba-5b1c5ba373ee" controls width="564"></video>
</td></tr></table>

📖 **[Launch blog post](https://fluxions.ai/blog/vui-launch)** — design notes, demos, and what's next.

**Vui** is short for **V**oice **U**ser **I**nterface — the layer that lets you talk to a computer and have it talk back.

Vui is a real-time voice assistant: speak into your mic, the model transcribes, runs a local LLM, and streams a TTS reply back — all from a single Python server.

It is built around **Vui Nano — a small, context-aware text-to-speech model trained on real conversations: 219M active parameters (305M total), Apache 2.0, with voice cloning, real-time streaming, and a dependency-free C build that runs on CPU.**

Most TTS models synthesise one utterance in isolation. Vui Nano generates each reply *inside the conversation*: the whole dialogue so far — your text **and the actual audio of your turn** — lives in the KV cache it decodes from, across a ~6-minute context. It was trained on two-speaker dialogue with an explicit speaker-change token, so it carries prosody across turns and produces the things real speech has and read-aloud corpora don't: breaths, laughter, hesitations, and overlap.

The handful of other open models that condition on dialogue acoustics this way are an order of magnitude larger and GPU-only. Vui Nano does it at 219M active parameters, and the C build in [`cpu/`](cpu/README.md) does it on a CPU with no Python, PyTorch, or ONNX at runtime.

Want the TTS model on its own, without the assistant? See [Vui Nano](#vui-nano) for the model card, `demo.py` for a standalone Gradio playground, and [`cpu/`](cpu/README.md) for the single-binary CPU build.

> **Want the latest models and production-grade turn-taking?** This repo is the open core. Our [production API](https://fluxions.ai) ships ongoing model updates and a more advanced turn-taking system, on hardened, low-latency infrastructure built for scale. Get in touch at [fluxions.ai](https://fluxions.ai).



## Features

- **Vui Nano (219M active, 305M total)** — a small, context-aware TTS model trained on real conversations: Llama-style decoder + RQ-Transformer head over the Qwen3-TTS-12Hz codec, Apache 2.0
- **Conversation-conditioned generation** — replies are decoded from a KV cache holding the whole dialogue, including the audio of your turn, so prosody carries across turns (~6-minute context)
- **Real-time voice loop** — WebRTC + WebSocket pipeline (ASR → LLM → TTS) with a browser UI, VAD-driven turn taking, speculative LLM prefill while you're still speaking, sentence-level TTS chunking with backpressure
- **Barge-in** — start talking mid-reply, the model cancels and listens
- **Streaming TTS** — ~9× realtime on a 4090, bf16 inference, CUDA graphs
- **OpenAI Realtime API compatible** — drop-in `ws://…/v1/realtime` for clients written against OpenAI's spec ([`docs/realtime-api.md`](docs/realtime-api.md))
- **One-shot voice-note REST endpoint** — `POST /v1/voice-note` runs the whole ASR → LLM → TTS pipeline in a single HTTP call (audio in, JSON out)
- **Standalone TTS demo** — `demo.py` Gradio playground for the model on its own
- **CPU inference, zero dependencies** — a pure-C engine ([`cpu/`](cpu/README.md)): one binary plus one weight file, no Python, PyTorch, or ONNX at runtime; supports voice cloning and streaming playback
- **Voice cloning** — upload an audio sample to clone any speaker; 4 fine-tuned presets shipped (`maeve`, `abraham`, `rhian`, `harry`)
- **SQ / WPS conditioning** — bias generation on six speech-quality channels and words-per-second
- **Hot-swap models** — pick Ollama LLM and ASR backend live from the UI
- **Pluggable ASR** — faster-whisper (GPU) or Moonshine (CPU streaming, ONNX)
- **Pluggable LLM backends** — Ollama, vLLM, any OpenAI-compatible endpoint
- **Memories** — assistant remembers facts about you across sessions (persisted to `~/.vui/memories.json`)
- **Thoughts stream** — parallel LLM routes voice intent to ~15 tools (memory ops, task control, timers, web search, delegation) without a wake-word grammar; pluggable for your own local tools
- **Built-in web search** — single-query factual lookups ("weather in London", "price of X", "who won the match") via Serper, Brave, or Tavily — one API round-trip, no agent loop; falls through to `delegate` for multi-step research
- **Optional Claude task server** — sidecar agent that handles slow/agentic work (Gmail, Calendar, Drive, Slack, multi-step web research) via your existing Claude Code MCPs; auto-discovered on boot
- **Non-Anthropic task backends** — point the task server at Ollama, z.ai, DeepSeek, vLLM, LM Studio, LiteLLM via the Anthropic-compatible `/v1/messages` envelope
- **Apple Silicon support** — the `Engine` Python API auto-dispatches to an MLX backend (quantized vui-nano-1.1, ~1.5–2.7× real-time on M4; pre-baked weights auto-download when published, otherwise converted once locally), `demo.py` and `demo.py --render` work end-to-end; the streaming-server MLX glue is WIP
- **Mobile-ready** — documented cloudflared and Tailscale paths for phone access with mic over HTTPS
- **Docker compose** — one file brings up the full stack (streaming server + optional bundled Ollama + optional Claude task server)
- **OpenClaw integration** — point OpenClaw's `openai` realtime provider at Vui for a fully-local voice front-end



## Install (one-liner)

```sh
curl -fsSL https://install.fluxions.ai | bash
```

Clones into `~/vui`, auto-detects Docker vs. native, installs deps (uv, ffmpeg libs, Claude Code CLI), and launches the stack on <http://localhost:8080>. The native path needs no sudo. The TTS weights are not pulled here — they download from Hugging Face on first render.

Flags (`--docker`, `--native`, `--llm <backend>`, `--no-claude`, `--no-launch`, `--upgrade`, `--model <name>`, `--dry-run`) forward to `install.sh` — see `./install.sh --help` from the clone for the full list. Note `--model` selects the **Ollama LLM** (default `qwen3.5:4b`), not the TTS checkpoint; to change that, pass a name or path to `Engine()`.



### Just the model: `pip install vui-tts`

If you only want Vui Nano in your own Python — a Pipecat or LiveKit agent, a batch job, a notebook — the engine is on PyPI as [`vui-tts`](https://pypi.org/project/vui-tts/) (the import name is `vui`; the bare `vui` name on PyPI is an unrelated package):

```sh
pip install vui-tts              # engine only: CUDA, or MLX on Apple Silicon
pip install "vui-tts[server]"    # + the streaming voice assistant (WebRTC, ASR, demo UI, task server)
```

```python
from vui.engine import Engine, GenConfig
engine = Engine()                # vui-nano-1.1 downloads from Hugging Face on first use
with engine.new_row() as row:
    codes, audio = row.render("Hello from Vui.", GenConfig(temperature=0.7))
```

Voice cloning and streaming from Python are covered in [`docs/python-api.md`](docs/python-api.md). Python 3.12; FlashAttention-2 is the optional `flash` extra (see [Hardware](#hardware)).



## Quick start (docker-compose, recommended)

The Vui streaming server runs from one compose file. The recommended setup is **Ollama on the host** (most users already have it) plus the Vui container — the container uses host networking and talks to your local Ollama at `localhost:11434`. Designed for **Linux + NVIDIA GPU**.



### Prerequisites

1. **Docker** with the Compose plugin (Docker Desktop 4.x or `docker-ce` ≥ 24).
2. **NVIDIA Container Toolkit** so the container can see the GPU:
   ```sh
   # Debian / Ubuntu — see https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
   sudo apt install -y nvidia-container-toolkit
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```
   Verify: `docker run --rm --gpus all nvidia/cuda:13.0.0-base-ubuntu22.04 nvidia-smi`
3. **[Ollama](https://ollama.com) on the host** (or use the bundled containerised one — see below).



### Bring up the core stack
```sh
ollama pull qwen3.5:4b      # on the host
docker compose up -d
```
Open <http://localhost:8080>, allow mic access, start talking. The Vui checkpoint and Qwen codec download automatically from [Hugging Face](https://huggingface.co/fluxions/vui) on first run and persist in a named volume.

#### No host Ollama? Use the bundled one
If you'd rather have Ollama in a container too:
```sh
docker compose --profile ollama up -d
docker compose exec ollama ollama pull qwen3.5:4b
```
The bundled service is gated behind the `ollama` profile so it's off by default; the Vui container talks to whichever instance is running on `localhost:11434`.



### Optional: Claude task server

The compose file ships a `claude-task` profile — a sidecar Claude container on `:8642` for delegated agentic work (Gmail / Calendar reads, web research). See [Claude task server](#claude-task-server-optional) below for what it does, how to bring it up (compose or native), and how to back it with a non-Anthropic model.



### Common compose commands
```sh
docker compose ps                   # service status
docker compose logs -f vui-stream   # follow streaming server logs
docker compose restart vui-stream   # restart after a code change
docker compose down                 # stop everything
docker compose down -v              # ...and wipe HF cache + Ollama models
```



## Native install (alternative)

If you'd rather skip Docker. Both services run as plain Python processes; the task server is optional — without it `vui-stream` works fine and the "task server" pill in the UI just stays grey.



### Vui streaming server

**System dependency: the ffmpeg shared libraries.** `torchcodec` links against `libavcodec`/`libavformat`/`libavutil` at runtime and won't import without them. Note it's the *libraries* — Vui never runs the `ffmpeg` binary, so the static-binary PyPI packages (`static-ffmpeg`, `imageio-ffmpeg`, `ffmpeg-binaries`) do **not** satisfy it. Docker users get this for free. Otherwise:

```sh
sudo apt install ffmpeg                     # Debian / Ubuntu
brew install ffmpeg                         # macOS
```

No root? `./install.sh --native` fetches an LGPL shared build into `~/.cache/vui/ffmpeg` and preloads it — nothing goes on `LD_LIBRARY_PATH`. See [`docs/rootless-install.md`](docs/rootless-install.md), which also covers building ffmpeg from source.

Then:

```sh
uv sync                  # base + flash-attn pre-built wheel on Linux (x86_64 + aarch64)


# Apple Silicon: MLX installs automatically (platform markers) — plain `uv sync` is enough
```

Pre-built flash-attn wheels are pinned for Linux x86_64 and aarch64, so ARM
servers (Grace-Hopper, Grace-Blackwell) get the real kernel. Where it can't run
— Jetson p

... (truncated, 33972 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
# Distribution name on PyPI is `vui-tts` (`vui` is taken by an unrelated GUI
# toolkit); the import name stays `vui`. `pip install vui-tts` gives the
# inference engine only — `vui.engine.Engine`, the codec, prompts, MLX on
# Apple Silicon — which is what integrations (Pipecat, LiveKit) depend on.
# The voice-assistant server is the `server` extra.
name = "vui-tts"
version = "1.1.4"
description = "Vui Nano — a small, context-aware text-to-speech model trained on real conversations. 219M active params (305M total), Apache 2.0, voice cloning, streaming, runs on CPU. Ships with a full real-time voice assistant (WebRTC, ASR, local LLM, OpenAI Realtime API compatible)."
readme = "README.md"
license = "Apache-2.0"
authors = [{ name = "Fluxions AI", email = "hello@fluxions.ai" }]
keywords = ["tts", "text-to-speech", "speech-synthesis", "voice-cloning", "streaming", "conversational-ai", "mlx", "on-device"]
classifiers = [
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.12",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

requires-python = ">=3.12,<3.13"

# Inference only: what `from vui.engine import Engine` needs on CUDA, MLX and CPU.
# torch is a range, not a pin: torch 2.11–2.12 declare `setuptools<82`, which
# collides with frameworks that pin a newer setuptools (Pipecat locks torch
# 2.13 + setuptools 83), so consumers must be free to take 2.12 or 2.13. This
# checkout's own lock stays on the release-tested 2.11 via
# `[tool.uv] constraint-dependencies` below; torchcodec follows torch
# minor-for-minor (0.11 ↔ 2.11 … 0.13 ↔ 2.13). torchaudio's last release is
# 2.11.0 and it carries no torch pin.
dependencies = [
    "torch>=2.11,<2.14",
    "torchaudio>=2.11,<2.14",
    "torchcodec>=0.11,<0.14",
    "transformers>=4.45",
    "tokenizers>=0.20",
    "safetensors>=0.4",
    "huggingface_hub>=0.26",
    "einops>=0.8",
    "pydantic>=2.9",
    "numpy>=1.24",
    "soundfile>=0.12",
    "julius>=0.2",
    "httpx>=0.27",
    "tiktoken>=0.8",     # tokenizer.py's tiktoken mode (checkpoint-dependent)
    # NOTE: flash-attn is deliberately NOT here — see the `flash` extra below.
    # MLX backend — automatic on Apple Silicon so Engine()'s auto-dispatch
    # works out of the box (same marker mechanism as flash-attn below).
    "mlx>=0.18 ; sys_platform == 'darwin' and platform_machine == 'arm64'",
]

[dependency-groups]
# `uv sync` installs these by default; `--no-dev` skips them. The dev group
# pulls the `server` extra so a checkout has the whole assistant, while
# `pip install vui-tts` stays inference-only.
dev = [
    "pytest",
    "pytest-asyncio",   # the backend/route tests are async
    "vui-tts[server]",
]

[project.optional-dependencies]
# The real-time voice assistant: WebRTC streaming server, ASR, demo UI, task
# server. `uv sync --extra server` / `pip install "vui-tts[server]"`.
server = [
    "openai-whisper",
    "aiohttp>=3.10",
    "aiortc>=1.9",
    "av>=12",            # WebRTC AudioFrame / AudioResampler — aiortc's wire type
    "filelock>=3.16",
    # ASR (faster-whisper default; silero VAD ONNX bundled in serving/stream/)
    "faster-whisper>=1.0",
    "onnxruntime>=1.19",
    # Demo UI
    "gradio>=5.0",
    # Claude task delegation server (`claude_server.py` imports it at module load).
    "claude-agent-sdk>=0.1.70",
    # ctranslate2 (faster-whisper) dlopens libcublas.so.12 at import time;
    # torch brings cu13. This supplies the cu12 ABI ctranslate2 needs.
    "nvidia-cublas-cu12 ; sys_platform == 'linux'",
    "mlx-whisper>=0.4 ; sys_platform == 'darwin' and platform_machine == 'arm64'",
]
# FlashAttention-2. Optional because the pinned wheels carry cubins for
# sm_80/90/100/120 and no PTX, so on anything older (Turing sm_75, Volta
# sm_70) importing it succeeds and the first decode step dies with "no kernel
# image is available". `vui.flash_compat` covers that with a pure-PyTorch SDPA
# path, so the kernel is a speedup, not a requirement.
#
# `install.sh` adds this extra automatically when it detects compute
# capability >= 8.0. By hand: `uv sync --extra flash`.
flash = [
    "flash-attn ; sys_platform == 'linux' and (platform_machine == 'x86_64' or platform_machine == 'aarch64')",
]
# Kept as an alias for older instructions (`uv sync --extra mlx`) — the mlx
# deps now install automatically on Apple Silicon via the markers above.
mlx = [
    "mlx>=0.18 ; sys_platform == 'darwin' and platform_machine == 'arm64'",
    "mlx-whisper>=0.4 ; sys_platform == 'darwin' and platform_machine == 'arm64'",
]
# CPU-streaming ASR backend (Moonshine). Optional — faster-whisper covers the
# default GPU path. Pull this in if you want VUI_ASR=moonshine to work.
moonshine = [
    "moonshine-voice",
]

# NOTE: no `[tool.uv] torch-backend` here on purpose. It only exists in recent
# uv, and uv *errors* on unknown [tool.uv] fields rather than ignoring them — so
# pinning it would make this project unsyncable on an older uv. `install.sh`
# exports UV_TORCH_BACKEND instead, which older uv simply ignores.
#
# The default build (cu130) already covers sm_75 and up. Auto-selection only
# matters below Turing, where recent wheels carry no kernels at all:
#     UV_TORCH_BACKEND=cu126 uv sync     # Volta / Pascal
# `python -m vui.doctor` tells you if the torch you have can't run your GPU.

[tool.uv]
# Pin this checkout (and its lock) to the torch the release was tested on; the
# published package accepts 2.11–2.12 (see `dependencies`).
constraint-dependencies = ["torch==2.11.*", "torchaudio==2.11.*", "torchcodec==0.11.*"]

[tool.uv.sources]
# Pre-built wheels from a community mirror — avoids the (slow + fragile) source
# build of flash-attn. Both are cu130 + cp312.
#
# aarch64 (Grace-Hopper / Grace-Blackwell) gets flash-attn 2.8.3 — the only
# cu130 build published for ARM, and it matches our torch 2.11 pin exactly.
# Its kernels cover sm_80/90/100/120 with no PTX fallback, so Jetson parts
# (Orin sm_87, Thor sm_110) import it fine but fail at launch; vui.flash_compat
# catches that and switches to the PyTorch SDPA path.
flash-attn = [
    { url = "https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.7.12/flash_attn-2.7.4%2Bcu130torch2.10-cp312-cp312-linux_x86_64.whl", marker = "sys_platform == 'linux' and platform_machine == 'x86_64'" },
    { url = "https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.9.22/flash_attn-2.8.3%2Bcu130torch2.11-cp312-cp312-linux_aarch64.whl", marker = "sys_platform == 'linux' and platform_machine == 'aarch64'" },
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"vui" = ["py.typed"]
"vui.serving.stream" = ["index.html", "silero_vad.onnx"]

[tool.pytest.ini_options]
# The backend and route tests are `async def` with no explicit marker.
asyncio_mode = "auto"

```

## Top-level layout

- .gitignore (~187 lines)
- AGENTS.md (~128 lines)
- assets/ (dir, 1 files, ~0 lines)
- bootstrap.sh (~43 lines)
- CHANGELOG.md (~354 lines)
- cpu/ (dir, 10 files, ~3888 lines)
- demo.py (~1491 lines)
- docker/ (dir, 2 files, ~75 lines)
- docker-compose.yml (~121 lines)
- docs/ (dir, 13 files, ~2357 lines)
- install.sh (~475 lines)
- LICENSE (~201 lines)
- pyproject.toml (~149 lines)
- README.md (~574 lines)
- sample_texts.json (~138 lines)
- scripts/ (dir, 1 files, ~162 lines)
- src/ (dir, 111 files, ~30448 lines)
- tests/ (dir, 7 files, ~1421 lines)
- uv.lock (~2180 lines)

