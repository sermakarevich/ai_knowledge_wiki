> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Vui is a real-time streaming conversational voice assistant built around Vui Nano, a small context-aware TTS model, served from a single Python server as a WebRTC/WebSocket voice loop (ASR → LLM → TTS).
## Key points
- Vui ("Voice User Interface", pronounced "vooey") is a real-time voice assistant where speech is transcribed, run through a local LLM, and streamed back as TTS from a single Python server (README.md:31-33).
- Vui Nano is a 219M-active (305M total) Apache 2.0 TTS model with voice cloning, real-time streaming, and CPU execution, trained on real two-speaker conversations (README.md:13-35).
- Unlike isolated-utterance TTS, Vui Nano decodes each reply from a KV cache holding the whole dialogue including the user's turn audio across ~6-minute context, using an explicit speaker-change token to carry prosody, breaths, laughter, hesitations, and overlap (README.md:37-37).
- The voice loop uses WebRTC + WebSocket with VAD-driven turn-taking, speculative LLM prefill while the user is still speaking, sentence-level TTS chunking with backpressure, and barge-in that cancels a reply when the user interrupts (README.md:51-52).
- Distribution covers a one-liner installer (`curl -fsSL https://install.fluxions.ai | bash`), Docker Compose with host or bundled Ollama, PyPI engine `vui-tts`, a standalone Gradio `demo.py`, and a dependency-free pure-C CPU build under `cpu/` (README.md:78-94).
- The assistant is extensible: OpenAI Realtime API-compatible `ws://…/v1/realtime`, one-shot `POST /v1/voice-note` REST endpoint, pluggable ASR (faster-whisper / Moonshine) and LLM backends (Ollama, vLLM, any OpenAI-compatible endpoint), hot-swap models from the UI, cross-session memories in `~/.vui/memories.json`, a ~15-tool thoughts stream, built-in web search, and an optional Claude task server sidecar (README.md:54-66).
---
## Vui Nano model
Context-aware TTS core of the project (README.md:35-39):
> "Most TTS models synthesise one utterance in isolation. Vui Nano generates each reply *inside the conversation*: the whole dialogue so far — your text **and the actual audio of your turn** — lives in the KV cache it decodes from, across a ~6-minute context." (README.md:37-37)
> "The handful of other open models that condition on dialogue acoustics this way are an order of magnitude larger and GPU-only. Vui Nano does it at 219M active parameters, and the C build in [`cpu/`](cpu/README.md) does it on a CPU with no Python, PyTorch, or ONNX at runtime." (README.md:39-39)
- Architecture noted in features: Llama-style decoder + RQ-Transformer head over the Qwen3-TTS-12Hz codec, Apache 2.0 (README.md:49-49).
- Capabilities: voice cloning with 4 shipped presets (`maeve`, `abraham`, `rhian`, `harry`), SQ / WPS conditioning on six speech-quality channels plus words-per-second, ~9× realtime streaming TTS on a 4090 with bf16 inference and CUDA graphs (README.md:53-59).
- Standalone use without the assistant: model card under "Vui Nano", `demo.py` Gradio playground, and [`cpu/`](cpu/README.md) single-binary CPU build (README.md:41-41).
## Voice loop and assistant capabilities
Real-time pipeline and integrations (README.md:51-71):
- Pipeline: WebRTC + WebSocket ASR → LLM → TTS with browser UI, VAD-driven turn-taking, speculative LLM prefill, sentence-level TTS chunking with backpressure; barge-in cancels and listens (README.md:51-52).
- APIs: OpenAI Realtime API-compatible drop-in `ws://…/v1/realtime` for OpenAI-spec clients ([`docs/realtime-api.md`](docs/realtime-api.md)); one-shot voice-note REST `POST /v1/voice-note` running ASR → LLM → TTS in a single HTTP call (README.md:54-55).
- Backends: hot-swap Ollama LLM and ASR backend live from UI; ASR via faster-whisper (GPU) or Moonshine (CPU streaming, ONNX); LLM via Ollama, vLLM, any OpenAI-compatible endpoint (README.md:60-62).
- Memory/tools: facts persisted to `~/.vui/memories.json`; thoughts stream routes voice intent to ~15 tools (memory ops, task control, timers, web search, delegation) with no wake-word grammar; built-in single-query web search via Serper, Brave, or Tavily with fallback to `delegate` for multi-step research (README.md:63-65).
- Task server: optional Claude sidecar for slow/agentic work (Gmail, Calendar, Drive, Slack, multi-step research) via existing Claude Code MCPs, auto-discovered on boot; non-Anthropic backends (Ollama, z.ai, DeepSeek, vLLM, LM Studio, LiteLLM) via Anthropic-compatible `/v1/messages` envelope (README.md:66-67).
- Platforms: Apple Silicon `Engine` auto-dispatch to MLX backend (quantized vui-nano-1.1, ~1.5–2.7× real-time on M4); mobile-ready via documented cloudflared/Tailscale paths; Docker Compose full stack; OpenClaw integration via `openai` realtime provider (README.md:68-71).
## Install and distribution
Verbatim install entry points (README.md:75-103):
```sh
curl -fsSL https://install.fluxions.ai | bash
```
- Clones into `~/vui`, auto-detects Docker vs. native, installs deps (uv, ffmpeg libs, Claude Code CLI), launches on <http://localhost:8080>; native path needs no sudo; TTS weights download from Hugging Face on first render, not during install (README.md:81-81).
| Flag / selector | Meaning (verbatim) |
|---|---|
| `--docker`, `--native` | install mode forwarded to `install.sh` (README.md:83-83) |
| `--llm <backend>` | selects backend forwarded to `install.sh` (README.md:83-83) |
| `--no-claude`, `--no-launch`, `--upgrade`, `--dry-run` | options forwarded to `install.sh`; see `./install.sh --help` (README.md:83-83) |
| `--model <name>` | selects the **Ollama LLM** (default `qwen3.5:4b`), not the TTS checkpoint; change TTS via name/path to `Engine()` (README.md:83-83) |
### Just the model: `pip install vui-tts`
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
- Import name is `vui`; bare `vui` on PyPI is an unrelated package; Python API details in [`docs/python-api.md`](docs/python-api.md); Python 3.12; FlashAttention-2 is the optional `flash` extra (README.md:89-103).
## Quick start (docker-compose and native)
Recommended setup is Ollama on the host plus the Vui container with host networking talking to `localhost:11434`, designed for Linux + NVIDIA GPU (README.md:109-109). Prerequisites (README.md:115-124):
1. Docker with Compose plugin (Docker Desktop 4.x or `docker-ce` ≥ 24).
2. NVIDIA Container Toolkit so the container sees the GPU (`sudo apt install -y nvidia-container-toolkit`, `sudo nvidia-ctk runtime configure --runtime=docker`, `sudo systemctl restart docker`).
3. Ollama on the host (or bundled containerised one).
Core stack (README.md:128-141):
```sh
ollama pull qwen3.5:4b      # on the host
docker compose up -d
```
- Open <http://localhost:8080>, allow mic access; Vui checkpoint and Qwen codec auto-download from Hugging Face on first run into a named volume; bundled Ollama variant: `docker compose --profile ollama up -d` then `docker compose exec ollama ollama pull qwen3.5:4b` (README.md:133-141).
- Optional `claude-task` compose profile: sidecar Claude container on `:8642` for delegated agentic work (README.md:145-147).
```sh
docker compose ps                   # service status
docker compose logs -f vui-stream   # follow streaming server logs
docker compose restart vui-stream   # restart after a code change
docker compose down                 # stop everything
docker compose down -v              # ...and wipe HF cache + Ollama models
```
- Native alternative: both services run as plain Python processes; without task server `vui-stream` works and the "task server" UI pill stays grey; requires ffmpeg shared libraries (`libavcodec`/`libavformat`/`libavutil`), e.g. `sudo apt install ffmpeg` or `brew install ffmpeg`; static-binary PyPI ffmpeg packages do **not** satisfy it; rootless path `./install.sh --native` fetches an LGPL build into `~/.cache/vui/ffmpeg` (see [`docs/rootless-install.md`](docs/rootless-install.md)); then `uv sync` with pre-built flash-attn wheels pinned for Linux x86_64 and aarch64 (README.md:162-188).
- Truncation note: the chunk excerpt ends mid-sentence at "Where it can't run — Jetson p" (README.md:190-190), so remaining native-install requirements (e.g. Jetson behavior) are cut and not covered here.
**Covers:** README.md (project description, Features list, install, pip engine, docker-compose and native quick start); referenced-only paths `cpu/README.md`, `demo.py`, `docs/realtime-api.md`, `docs/python-api.md`, `docs/rootless-install.md`, `install.sh`, `docker-compose.yml` as named in README excerpt
