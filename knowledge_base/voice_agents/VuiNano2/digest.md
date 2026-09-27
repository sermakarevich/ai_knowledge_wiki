> [[index|Wiki]] | [[summary|Summary]]
# fluxions-ai/vui — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Vui is a real-time streaming conversational voice assistant built around Vui Nano, a small context-aware TTS model, served from a single Python server as a WebRTC/WebSocket voice loop (ASR → LLM → TTS).
## Key points
- Vui ("Voice User Interface", pronounced "vooey") is a real-time voice assistant where speech is transcribed, run through a local LLM, and streamed back as TTS from a single Python server (README.md:31-33).
- Vui Nano is a 219M-active (305M total) Apache 2.0 TTS model with voice cloning, real-time streaming, and CPU execution, trained on real two-speaker conversations (README.md:13-35).
- Unlike isolated-utterance TTS, Vui Nano decodes each reply from a KV cache holding the whole dialogue including the user's turn audio across ~6-minute context, using an explicit speaker-change token to carry prosody, breaths, laughter, hesitations, and overlap (README.md:37-37).
- The voice loop uses WebRTC + WebSocket with VAD-driven turn-taking, speculative LLM prefill while the user is still speaking, sentence-level TTS chunking with backpressure, and barge-in that cancels a reply when the user interrupts (README.md:51-52).
- Distribution covers a one-liner installer (`curl -fsSL https://install.fluxions.ai | bash`), Docker Compose with host or bundled Ollama, PyPI engine `vui-tts`, a standalone Gradio `demo.py`, and a dependency-free pure-C CPU build under `cpu/` (README.md:78-94).
- The assistant is extensible: OpenAI Realtime API-compatible `ws://…/v1/realtime`, one-shot `POST /v1/voice-note` REST endpoint, pluggable ASR (faster-whisper / Moonshine) and LLM backends (Ollama, vLLM, any OpenAI-compatible endpoint), hot-swap models from the UI, cross-session memories in `~/.vui/memories.json`, a ~15-tool thoughts stream, built-in web search, and an optional Claude task server sidecar (README.md:54-66).

## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** Top-level files define how Vui is cloned, installed, edited, ignored by git, demoed as TTS, and fed example texts.
## Key points
- `AGENTS.md` orients AI coding agents: Vui is a streaming conversational voice assistant (ASR → LLM → TTS) built around a 305M speech transformer over the Qwen3-TTS-12Hz codec (AGENTS.md:3-5).
- Setup is `uv`-only on Python 3.12 (`uv sync`, `--extra mlx`, `--extra claude`) with setuptools-layout imports (`from vui.x import y`), because `pip` ignores `[tool.uv.sources]` and source-builds flash-attn (AGENTS.md:10-15).
- Entry points are `python -m vui.serving.stream` on `:8080`, `python -m vui.serving.claude_server` on `:8642`, `python demo.py` (Gradio) with `demo.py --render --prompt` CLI rendering, and `docker compose up -d`; no test suite is committed, so changes are verified end-to-end via the entry point (AGENTS.md:21-27).
- `bootstrap.sh` is hosted at `https://install.fluxions.ai` (`curl -fsSL https://install.fluxions.ai | bash`), clones Vui into `$VUI_HOME` (default `~/vui`) at `$VUI_REF` (default `main`), then execs `install.sh` forwarding all args (bootstrap.sh:2-13).
- `demo.py` auto-detects platform (MLX on Apple Silicon arm64/darwin, CUDA elsewhere), parses `checkpoint`, `--render`, `--text/-t`, `--prompt/-p` (default `prompts/harry.wav`), `--temperature`, `--n-codebooks`, `--max-secs`, `--eos-threshold`, and exits early into `vui.demo.cli.run` in render mode (demo.py:1-71).
- `install.sh` never uses sudo, validates it runs inside a Vui checkout (`pyproject.toml` + `src/vui` + `name = "vui"`), resolves the LLM backend (explicit flag > `VUI_LLM_BACKEND` > live Ollama > live vLLM > default `vllm`), picks docker vs native, pins the torch CUDA build from GPU compute capability, and fetches ffmpeg shared libs for torchcodec when needed (install.sh:28-30, install.sh:97-100, install.sh:135-148, install.sh:217-231, install.sh:244-294).
- `.gitignore` excludes Python/Docker/venv/IDE artifacts plus repo-specific outputs: `*.pt`, `*.wav`, `*.mp3`, `*.tar.gz`, `*.safetensors`, `*.opus`, `*.log`, `*.json` (with `!sample_texts.json` exception), `checkpoints/`, `scratch/`, `debug_dump/`, `outputs/`, `prompts/`, `todo.md`, and generated `cpu/*.onnx`, `cpu/*.onnx.data`, `cpu/*.bin`, `cpu/vui_tts` (`.gitignore`:165-187).

## The system in five moves
1. Vui is a real-time streaming voice assistant (ASR → LLM → TTS) built around Vui Nano, a small context-aware TTS model served from a single Python server.
2. Vui Nano generates each reply inside the conversation from a KV cache holding the whole dialogue including user-turn audio, carrying prosody and paralinguistics across ~6-minute context.
3. The voice loop sustains real-time interaction via WebRTC/WebSocket with VAD turn-taking, speculative prefill, sentence-level TTS chunking with backpressure, and barge-in cancellation.
4. Distribution and entry points make it installable and runnable anywhere: one-liner installer, Docker Compose, pip vui-tts engine, Gradio demo, and CPU build, with stream server on :8080 and task sidecar on :8642.
5. Top-level files encode the contributor contract: uv-only Python 3.12 setup, no committed test suite, sudo-free install with backend/GPU/ffmpeg resolution, platform auto-detection, and git-ignored runtime outputs.
