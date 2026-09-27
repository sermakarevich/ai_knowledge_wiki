---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: fluxions-ai/vui

### Q1. What is Vui in one sentence, and what is Vui Nano?

> [!tip]- Answer
> Vui ("Voice User Interface", pronounced "vooey") is a real-time streaming conversational voice assistant that transcribes speech, runs it through a local LLM, and streams back TTS from a single Python server. Vui Nano is its 219M-active (305M total) Apache 2.0 TTS core with voice cloning, real-time streaming, and CPU execution, trained on real two-speaker conversations. See [[wiki/01-overview|Overview]].

### Q2. How does Vui Nano differ from isolated-utterance TTS models?

> [!tip]- Answer
> Unlike isolated-utterance TTS, Vui Nano generates each reply inside the conversation, decoding from a KV cache holding the whole dialogue including the actual audio of the user's turn across ~6-minute context. An explicit speaker-change token carries prosody, breaths, laughter, hesitations, and overlap across turns. It is a Llama-style decoder with an RQ-Transformer head over the Qwen3-TTS-12Hz codec. See [[wiki/01-overview|Overview]].

### Q3. How does the real-time voice loop sustain low-latency interaction?

> [!tip]- Answer
> The loop runs ASR → LLM → TTS over WebRTC plus WebSocket with VAD-driven turn-taking and barge-in that cancels a reply when the user interrupts. It uses speculative LLM prefill while the user is still speaking plus sentence-level TTS chunking with backpressure to keep speech flowing. ASR is pluggable (faster-whisper on GPU or Moonshine streaming on CPU) and LLMs are hot-swappable from the UI across Ollama, vLLM, or any OpenAI-compatible endpoint. See [[wiki/01-overview|Overview]].

### Q4. What are Vui's install and distribution paths?

> [!tip]- Answer
> The one-liner `curl -fsSL https://install.fluxions.ai | bash` clones into `~/vui`, auto-detects Docker vs native, and launches on `http://localhost:8080`, with TTS weights downloading from Hugging Face on first render. The pip path is `pip install vui-tts` for the engine only or `pip install "vui-tts[server]"` for the streaming assistant, plus a standalone Gradio `demo.py` and a dependency-free pure-C CPU build under `cpu/`. Docker Compose supports host Ollama (`ollama pull qwen3.5:4b`, `docker compose up -d`) or a bundled-Ollama profile, with an optional Claude task-server sidecar. See [[wiki/01-overview|Overview]].

### Q5. What does AGENTS.md require of contributors editing Vui?

> [!tip]- Answer
> Setup is `uv`-only on Python 3.12 (`uv sync`, with `--extra mlx` for Apple Silicon and `--extra claude` for the task server), because `pip` ignores `[tool.uv.sources]` and source-builds flash-attn. Entry points are `python -m vui.serving.stream` on `:8080`, `python -m vui.serving.claude_server` on `:8642`, `python demo.py` for the Gradio playground, and `docker compose up -d`. No test suite is committed, so changes are verified end-to-end via the entry point. See [[wiki/02-top-level-files|Top-level files]].

### Q6. What do bootstrap.sh, install.sh, demo.py, and .gitignore each do at the repo root?

> [!tip]- Answer
> `bootstrap.sh`, hosted at `https://install.fluxions.ai`, clones Vui into `$VUI_HOME` (default `~/vui`) at `$VUI_REF` (default `main`) and execs `install.sh` forwarding all args. `install.sh` never uses sudo, validates it runs inside a Vui checkout, resolves the LLM backend (explicit flag over env over live Ollama over live vLLM), picks docker vs native, and pins the torch CUDA build plus ffmpeg shared libs. `demo.py` auto-detects MLX on Apple Silicon vs CUDA elsewhere with `checkpoint`, `--render`, `--text`, `--prompt`, and sampling flags, while `.gitignore` excludes runtime outputs like checkpoints, audio, logs, and `cpu/` build artifacts. See [[wiki/02-top-level-files|Top-level files]].

### Q7. (Evaluation) A solo developer on Apple Silicon with no GPU server wants the fastest path to talking TTS experiments with preset voices — which entry point should they pick and why?

> [!tip]- Answer
> Recommend `python demo.py` with a shipped preset prompt such as `prompts/harry.wav`, since it auto-detects Apple Silicon and uses the MLX backend without Docker or CUDA setup. It exposes the four fine-tuned preset voices plus temperature and codebook controls for quick iteration, deferring the full `:8080` streaming server and Docker install until a live assistant is needed. This avoids backend, GPU, and ffmpeg resolution overhead while staying inside the documented contributor workflow. See [[wiki/02-top-level-files|Top-level files]].
