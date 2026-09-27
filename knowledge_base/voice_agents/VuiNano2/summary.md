# Technical Analysis: fluxions-ai/vui

**Repository:** https://github.com/fluxions-ai/vui
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: open real-time voice assistants typically glue an isolated-utterance TTS model to separate ASR and LLM services, which loses conversational prosody (breaths, laughter, hesitations, overlap, turn-taking rhythm) and adds integration work across processes, backends, and hardware targets (README.md:37-39).

What the repo does: Vui ships a single-Python-server streaming voice assistant (ASR → LLM → TTS) built around Vui Nano, a 219M-active (305M total) Apache 2.0 TTS model that decodes each reply from a KV cache holding the whole dialogue — user text and the actual audio of the user turn — across ~6-minute context with an explicit speaker-change token (README.md:13-37). The loop runs over WebRTC + WebSocket with VAD-driven turn-taking, speculative LLM prefill while the user is still speaking, sentence-level TTS chunking with backpressure, and barge-in that cancels a reply on interruption (README.md:51-52).

Primary user: a developer or self-hoster who wants a locally runnable, extensible voice assistant (Docker Compose with host or bundled Ollama, one-liner installer, PyPI engine `vui-tts`, standalone Gradio `demo.py`, dependency-free pure-C CPU build under `cpu/`) rather than a hosted voice API consumer (README.md:78-94). The assistant layer adds pluggable ASR/LLM backends, hot-swap models from the UI, cross-session memories, a ~15-tool thoughts stream, built-in web search, an OpenAI Realtime-compatible endpoint, a one-shot voice-note REST endpoint, and an optional Claude task-server sidecar (README.md:54-67).

## 2. High-Level Architecture

```text
Browser UI (mic/playback, VAD, model hot-swap)
        │ WebRTC audio + WebSocket control  (README.md:51-52)
        ▼
vui-stream server :8080 ──► ASR worker ──► LLM backend ──► TTS worker ──► playback/drains
        │                    (faster-whisper│ (Ollama/vLLM/     (Vui Nano Engine/
        │                     Moonshine)    │  OpenAI-compat)   │  MLX on Apple Silicon)
        │                                   │                  │  (README.md:60-62, README.md:68-71)
        ├──► thoughts stream (~15 tools: memory, timers, search, delegate) (README.md:63-65)
        ├──► memories store (~/.vui/memories.json) (README.md:63-65)
        ├──► ws://…/v1/realtime (OpenAI Realtime-compatible) + POST /v1/voice-note (README.md:54-55)
        └──► claude task sidecar :8642 (optional, auto-discovered MCPs) (README.md:66-67)
```

Data-flow narrative:

1. Capture and turn-taking: browser captures microphone audio; server-side VAD segments turns and supports barge-in that cancels the in-flight reply and returns to listening (README.md:51-52).
2. Transcription: the ASR worker transcribes turn audio via faster-whisper on GPU or Moonshine (CPU streaming, ONNX) (README.md:60-62).
3. Reasoning with speculation: text goes to the configured LLM (Ollama, vLLM, any OpenAI-compatible endpoint) with speculative prefill while the user is still speaking; the thoughts stream routes intent to ~15 tools without a wake-word grammar (README.md:51-52, README.md:63-65).
4. Conversation-conditioned synthesis: reply sentences stream into Vui Nano, which decodes from the dialogue KV cache (prior text plus user-turn audio) with speaker-change, SQ/WPS conditioning, and voice preset; output is chunked at sentence level with backpressure at ~9× realtime on a 4090 (bf16, CUDA graphs) or ~1.5–2.7× realtime via quantized MLX on M4 (README.md:37-39, README.md:53-59, README.md:68-71).
5. Delivery and persistence: audio streams back to the browser for playback; facts persist to `~/.vui/memories.json`; slow multi-step work delegates to the Claude sidecar on `:8642` (README.md:63-67).

Persistent state lives outside the process: `~/.vui/memories.json` for cross-session facts (README.md:63-65); `~/.cache/vui` for weights, KV disk cache, ffmpeg libs, and `demo_settings.json` for Gradio defaults (demo.py:109-317; install.sh:18-26); named Docker volumes for the Hugging Face cache and Ollama models when composed (README.md:133-141).

## 3. Vui Nano: Conversation-Conditioned Speech Synthesis

Central concept: the reply is not synthesized in isolation but decoded inside the conversation. The whole dialogue so far — text and the actual audio of the user turn — lives in the KV cache the model decodes from, across ~6-minute context, with an explicit speaker-change token carrying prosody, breaths, laughter, hesitations, and overlap (README.md:37-37).

Representation: Llama-style decoder plus RQ-Transformer head over the Qwen3-TTS-12Hz codec; 768-dim, 22 layers, 8 heads with `sq_proj`/`wps_proj` conditioning; 16 codebooks × 2048 entries at 12.5 Hz, 24 kHz output (README.md:49-49; AGENTS.md:33-103). Key modules named in the repo layout: `src/vui/model.py`, `engine.py` (`Engine`/`GenConfig`/`Row`, WPS estimation), `inference.py`, `qwen_codec.py`, `qwen_spk_enc.py`, `rope.py`/`sampling.py`, `tokenizer.py`, `align.py`, `prompt_utils.py`, `streaming.py`, `hf.py`, `config.py`, plus `src/vui/mlx/tts/` for the Apple Silicon backend (AGENTS.md:33-103).

Named kinds/types with file:line:

- Voices: 4 shipped presets `maeve`, `abraham`, `rhian`, `harry` selected by prompt wav such as `prompts/harry.wav` (README.md:53-59; demo.py:28-51).
- Quality/speed conditioning: six speech-quality channels (`sq_dns_sig`, `sq_dns_bak`, `sq_nq_noi`, `sq_nq_disc`, `sq_nq_col`, `sq_nq_loud` defaulting to `0.0` except `sq_nq_loud` at `5.0`) plus `wps_score` (words-per-second), with generation knobs `temperature` (`0.7`), `top_k` (`50`), `rep_penalty` (`1.1`), `rep_window` (`24`), `chunk_words` (`20`), `n_codebooks` (`0`), `eos_threshold` (`0.45`) (demo.py:280-299).
- Engine session handle: `Engine()` with `engine.new_row()` yielding a `Row` exposing `row.render(text, GenConfig(...))` returning `(codes, audio)` (README.md:89-103).
- Codec operating point: `vui-nano-1.1` checkpoint (default `vui-nano-1.1.safetensors`), `max_secs` from config default `15.0`, bf16 inference with CUDA graphs on GPU or quantized MLX on Apple Silicon (demo.py:56-71; demo.py:320-342; README.md:53-59).

Key query (verbatim, README.md:89-103):

```python
from vui.engine import Engine, GenConfig
engine = Engine()                # vui-nano-1.1 downloads from Hugging Face on first use
with engine.new_row() as row:
    codes, audio = row.render("Hello from Vui.", GenConfig(temperature=0.7))
```

## 4. LLM / External Service Integration

The repo calls LLM and search/task APIs; TTS/ASR inference itself is local.

- LLM backends (required for assistant replies, optional for bare TTS): Ollama (default model `qwen3.5:4b`), vLLM, or any OpenAI-compatible endpoint; hot-swappable live from the UI (README.md:60-62, README.md:83-83). Backend resolution order in `resolve_llm_backend()`: explicit `--llm` flag > `VUI_LLM_BACKEND` > reachable Ollama (`/api/version`) > reachable vLLM (`/v1/models`); neither backend up is still fine since TTS/ASR serve regardless (install.sh:118-148).
- Speech models: TTS weights auto-download from Hugging Face on first render/run into cache or a named volume, not during install (README.md:81-81, README.md:133-141); checkpoint resolution via `from vui.hf import download` (demo.py:320-342).
- ASR backends: faster-whisper (GPU) or Moonshine (CPU streaming, ONNX) (README.md:60-62).
- Web search (built-in single-query, fallback to `delegate` for multi-step): Serper, Brave, or Tavily providers (README.md:63-65).
- Task sidecar: optional Claude container on `:8642` for slow/agentic work (Gmail, Calendar, Drive, Slack, multi-step research) via existing Claude Code MCPs auto-discovered on boot; non-Anthropic backends (Ollama, z.ai, DeepSeek, vLLM, LM Studio, LiteLLM) via an Anthropic-compatible `/v1/messages` envelope (README.md:66-67).
- Environment variables attested in excerpts: `VUI_HOME` (default `$HOME/vui`), `VUI_REPO`, `VUI_REF` (default `main`) (bootstrap.sh:10-19); `VUI_REF`, `OLLAMA_HOST`, `VUI_VLLM_URL` (default `http://localhost:8000`), `VUI_TASK_PORT` (default `8642`), `VUI_MODE`, `VUI_FFMPEG_DIR` (default `~/.cache/vui/ffmpeg`), `VUI_FFMPEG_VERSION` (default `7.1`), `VUI_LLM_BACKEND`, `UV_TORCH_BACKEND` (install.sh:18-26, install.sh:118-148, install.sh:190-231).

## 5. The Streaming Voice Loop (ASR → LLM → TTS)

Primary workflow: continuous full-duplex voice conversation served from `python -m vui.serving.stream` on `:8080` (AGENTS.md:21-25). The wiki excerpts name the stage modules but truncate function bodies, so each step is cited to its owning module as attested in the repo-layout record (AGENTS.md:33-103); per-function line citations below that granularity are not present in the available excerpts.

1. Ingest audio — browser captures mic audio; `audio_in_worker.py` / `vad.py` frame and segment speech; barge-in cancels the active reply (README.md:51-52; stage modules per AGENTS.md:33-103).
2. Transcribe turn — `asr_worker.py` with `asr/` backends produces the user-turn text via faster-whisper or Moonshine (README.md:60-62; stage modules per AGENTS.md:33-103).
3. Speculative reasoning — `llm.py` / `llm_backend.py` prefill against Ollama/vLLM/OpenAI-compatible while the user is still speaking; `voice_turn.py` owns turn state; `thoughts.py` + `tools/` route intent to ~15 tools and `prompts.py` / `prompt_routes.py` shape the prompt (README.md:51-52, README.md:63-65; stage modules per AGENTS.md:33-103).
4. Recall and delegate — `memories.py` reads/writes `~/.vui/memories.json`; `tasks.py` delegates slow work to `claude_server.py` on `:8642` via `discover_mcp_tools()` and `MODEL` (README.md:63-67; stage modules per AGENTS.md:33-103).
5. Synthesize with backpressure — `tts_worker.py` (CUDA, latency-sensitive, buffer reuse, CUDA-graph boundaries) or `tts_worker_mlx.py` (Apple Silicon) renders sentence chunks through `Engine`/`Row.render`; `streaming.py` and `drains.py` / `playback.py` manage chunk flow and playback (README.md:51-59; AGENTS.md:107-114).
6. Serve and interoperate — `server.py` (`DEFAULT_SETTINGS`, `n_codebooks`) + `connection.py` + `protocol.py` hold the WebSocket/WebRTC session; `realtime/` serves `ws://…/v1/realtime`, `voice_note_routes.py` serves one-shot `POST /v1/voice-note` (ASR → LLM → TTS in a single HTTP call), `model_routes.py` serves hot-swap, `test_routes.py` serves diagnostics (README.md:54-55; stage modules per AGENTS.md:33-103).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | ~190+ (excerpt to :190) | Product/architecture contract: model, loop, backends, install, compose/native quick start (README.md:13-190) |
| `AGENTS.md` | ~114 | Agent editing contract: `uv` setup, entry points, module map, latency/concurrency conventions (AGENTS.md:3-114) |
| `src/vui/model.py` | n/a in excerpts (768-dim, 22L, 8H per AGENTS.md:33-103) | Speech transformer definition with SQ/WPS conditioning |
| `src/vui/engine.py` | n/a in excerpts | `Engine`/`GenConfig`/`Row` session API and WPS estimation (AGENTS.md:33-103) |
| `src/vui/streaming.py` | n/a in excerpts | Chunked/streaming generation interface incl. `generate_chunked` (demo.py:109-268) |
| `src/vui/serving/stream/server.py` | n/a in excerpts (`DEFAULT_SETTINGS`, `n_codebooks`) | Streaming server, settings, codebook depth (AGENTS.md:33-103) |
| `src/vui/serving/stream/voice_turn.py` | n/a in excerpts | Turn state machine; latency-sensitive with buffer reuse (AGENTS.md:33-114) |
| `src/vui/serving/stream/tts_worker.py` | n/a in excerpts | CUDA TTS worker; latency-sensitive, CUDA-graph boundaries (AGENTS.md:107-114) |
| `src/vui/serving/stream/asr_worker.py` | n/a in excerpts | ASR worker multiplexing faster-whisper/Moonshine (AGENTS.md:33-103) |
| `src/vui/serving/stream/llm.py`, `llm_backend.py` | n/a in excerpts | LLM client and backend abstraction for Ollama/vLLM/compat (AGENTS.md:33-103) |
| `src/vui/serving/stream/thoughts.py`, `tools/` | n/a in excerpts (~15 tools) | Intent routing, memory/timer/search/delegation tools (README.md:63-65) |
| `src/vui/serving/stream/memories.py` | n/a in excerpts | Cross-session fact store over `~/.vui/memories.json` (README.md:63-65) |
| `src/vui/serving/claude_server.py` | n/a in excerpts (`discover_mcp_tools()`, `MODEL`) | Optional task sidecar on `:8642` (AGENTS.md:21-103) |
| `demo.py` | 1492 (truncated past MLX loader) | Gradio playground + `--render` CLI; platform dispatch, settings, checkpoint resolution (demo.py:1-342) |
| `install.sh` | 476 (truncated past ffmpeg fetch) | Rootless installer: backend/mode/GPU/ffmpeg resolution, no sudo (install.sh:7-294) |
| `bootstrap.sh` | 44 (complete) | One-liner bootstrapper: clone/fetch `$VUI_HOME` at `$VUI_REF`, exec `install.sh` (bootstrap.sh:2-43) |
| `pyproject.toml` | n/a in excerpts (`name = "vui"`) | Package identity (`vui-tts` on PyPI), `uv` sources, extras (`mlx`, `claude`, `flash`) (README.md:89-103; AGENTS.md:10-15) |
| `docker-compose.yml`, `docker/` | n/a in excerpts | Full-stack compose (stream, bundled-Ollama and claude-task profiles) (AGENTS.md:21-103) |
| `docs/realtime-api.md`, `docs/python-api.md`, `docs/configuration.md`, `docs/memory-budget.md`, `docs/thoughts-tools.md` | n/a in excerpts | Endpoint, engine API, tuning, memory, and tool contracts (README.md:54-103; AGENTS.md:33-103) |
| `sample_texts.json` | 36+ keys shown (truncated) | Demo/render text fixture with disfluency tokens (`[laugh]`, `[sigh]`, `[hesitate]`) (sample_texts.json:1-36) |

Line counts marked n/a are not stated in the available wiki excerpts; structural importance follows the repo-layout record (AGENTS.md:33-103).

## 7. Dependencies

Required first. Exact constraint strings are quoted as stated in the excerpts; where the excerpts give no version, the constraint is recorded as unstated.

| Package | Version constraint | Purpose |
|---|---|---|
| `python` | `3.12` (AGENTS.md:10-15) | Runtime; `uv`-only sync |
| `vui-tts` (import `vui`; bare `vui` on PyPI is unrelated) | unstated (README.md:89-103) | Engine + optional `server` extra (WebRTC, ASR, demo UI, task server) |
| `torch` (CUDA build) | `cu126` pinned when compute cap < 7.5, else `auto`; `UV_TORCH_BACKEND` override (install.sh:190-231) | Model inference; SDPA/fp32 warning path on old GPUs |
| `flash-attn` | prebuilt wheel via `uv sync` on Linux/CUDA; optional `flash` extra (AGENTS.md:10-15; README.md:89-103) | Attention kernel for the transformer |
| `torchcodec` + system ffmpeg sonames (`libavcodec`/`libavformat`/`libavutil`) | ffmpeg major `7.1` via `VUI_FFMPEG_VERSION`; static-binary PyPI ffmpeg insufficient (install.sh:233-294; README.md:162-188) | Audio decode for torchcodec (`vui.ffmpeg_libs` readiness probe) |
| `faster-whisper` | unstated (README.md:60-62) | GPU ASR backend |
| `moonshine` (ONNX) | unstated (README.md:60-62) | CPU streaming ASR backend |
| `gradio` | unstated (demo.py:1-71) | `demo.py` TTS playground UI |
| `ollama` backend | default LLM `qwen3.5:4b` (README.md:83-83, README.md:128-141) | Local LLM serving (host or bundled profile) |
| `uv` | unstated (AGENTS.md:10-15) | Installer/sync; `pip` unsupported (ignores `[tool.uv.sources]`, source-builds flash-attn) |
| `mlx` (`--extra mlx`) | Apple Silicon arm64/darwin path (demo.py:78-80; AGENTS.md:10-15) | Quantized `vui-nano-1.1` inference at ~1.5–2.7× realtime on M4 |
| `claude` (`--extra claude`, Claude Code CLI) | unstated (AGENTS.md:10-15; README.md:81-81) | Task-server sidecar deps and MCP tooling |
| `docker` + Compose plugin, NVIDIA Container Toolkit | Docker Desktop `4.x` or `docker-ce >= 24` (README.md:115-124) | Containerized full stack with GPU passthrough |
| `serper` / `brave` / `tavily` | unstated (README.md:63-65) | Single-query web search providers |
| `cloudflared` / `tailscale` | unstated, documented paths (README.md:68-71) | Mobile/remote access to the local server |

## 8. CLI / Usage Surface

Entry points (AGENTS.md:21-25; README.md:75-103):

| Entry point | What it does |
|---|---|
| `curl -fsSL https://install.fluxions.ai \| bash` | Bootstrap: clone into `$VUI_HOME` (default `~/vui`) at `$VUI_REF` (default `main`), exec `install.sh` forwarding args (bootstrap.sh:2-43) |
| `./install.sh [--docker \| --native] [--llm <backend>] [--model <name>] [--no-claude] [--no-launch] [--upgrade] [--dry-run]` | Setup + launch; never uses sudo; refuses non-checkouts; `--upgrade` needs clean git tree (install.sh:7-112) |
| `python -m vui.serving.stream` | Streaming server on `:8080`, browser UI at `/` (AGENTS.md:21-25) |
| `python -m vui.serving.claude_server` | Optional Claude task sidecar on `:8642` (AGENTS.md:21-25) |
| `python demo.py [--render --prompt prompts/<voice>.wav --text/-t ... --temperature ... --n-codebooks ... --max-secs ... --eos-threshold ...] [checkpoint]` | Gradio playground or CLI render; checkpoint default `vui-nano-1.1.safetensors` (demo.py:28-71) |
| `pip install vui-tts` / `pip install "vui-tts[server]"` | Engine-only vs engine + assistant stack (README.md:89-103) |
| `docker compose up -d` / `docker compose --profile ollama up -d` / compose `ps`/`logs -f vui-stream`/`restart vui-stream`/`down [-v]` | Full stack, bundled-Ollama variant, and lifecycle ops (README.md:128-147) |
| `ws://…/v1/realtime` | OpenAI Realtime API-compatible drop-in for OpenAI-spec clients (README.md:54-55) |
| `POST /v1/voice-note` | One-shot ASR → LLM → TTS in a single HTTP call (README.md:54-55) |

Environment variables:

| Variable | Default / meaning |
|---|---|
| `VUI_HOME` | `$HOME/vui` clone target (bootstrap.sh:10-19) |
| `VUI_REPO` | `https://github.com/fluxions-ai/vui` (bootstrap.sh:10-19) |
| `VUI_REF` | `main`; ref for `--upgrade` (bootstrap.sh:10-19; install.sh:18-26) |
| `VUI_LLM_BACKEND` | Backend override below explicit `--llm` (install.sh:118-148) |
| `OLLAMA_HOST` | Remote Ollama endpoint, e.g. `gpu-box.lan:11434` (install.sh:18-26) |
| `VUI_VLLM_URL` | Default `http://localhost:8000` (install.sh:18-26) |
| `VUI_TASK_PORT` | Default `8642` (install.sh:18-26) |
| `VUI_MODE` | `native` or `docker`, same as flags (install.sh:18-26) |
| `VUI_FFMPEG_DIR` / `VUI_FFMPEG_VERSION` | Defaults `~/.cache/vui/ffmpeg` / `7.1` (install.sh:18-26) |
| `UV_TORCH_BACKEND` | Explicit torch CUDA build override (install.sh:190-231) |

Config: `DEFAULT_SETTINGS` and `n_codebooks` in `serving/stream/server.py`; `DEFAULTS` table persisted to `demo_settings.json` under `~/.cache/vui` via `_load_settings`/`_save_settings` (temperature, top_k/p, max_duration, six SQ channels, wps_score, rep_penalty/window, chunk_words, n_codebooks, eos_threshold, compile_rq) (AGENTS.md:33-103; demo.py:276-317). Note: `--model <name>` selects the Ollama LLM, not the TTS checkpoint; TTS changes via name/path to `Engine()` (README.md:83-83).

## 9. Extensibility Points

- New LLM backend: extend the `llm_backend.py` backend abstraction and `llm.py` client in `src/vui/serving/stream/`; resolution order lives in `resolve_llm_backend()` in `install.sh:118-148` and UI hot-swap routes in `model_routes.py` (AGENTS.md:33-103).
- New ASR backend: extend `asr_worker.py` / `asr/` beside the faster-whisper and Moonshine paths (README.md:60-62; AGENTS.md:33-103).
- New voice: add a prompt wav under `prompts/` (git-ignored per `.gitignore`:165-187) and pass `--prompt` to `demo.py` or a name/path to `Engine()`; presets today are `maeve`/`abraham`/`rhian`/`harry` (README.md:53-59; demo.py:28-71).
- New assistant tool: add a module under `src/vui/serving/stream/tools/` wired through `thoughts.py`; tool/reference docs live in `docs/thoughts-tools.md` (README.md:63-65; AGENTS.md:33-103).
- New prompt behavior/route: edit `prompts.py` / `prompt_routes.py` and `config.py`; memory tools read/write `memories.py` over `~/.vui/memories.json` (README.md:63-65; AGENTS.md:33-103).
- New API surface: add routes beside `voice_note_routes.py` (`POST /v1/voice-note`), `realtime/` (`ws://…/v1/realtime` per `docs/realtime-api.md`), `model_routes.py`, `test_routes.py` (README.md:54-55; AGENTS.md:33-103).
- New hardware backend: extend `tts_worker_mlx.py` / `src/vui/mlx/tts/` (Apple Silicon) or the pure-C `cpu/` single-binary build; CUDA latency work concentrates in `tts_worker.py` / `voice_turn.py` at buffer-reuse and CUDA-graph boundaries (README.md:68-71; AGENTS.md:107-114).
- New deployment target: extend `docker/` (`Dockerfile.stream`, `Dockerfile.claude`) and `docker-compose.yml` profiles (bundled-Ollama, claude-task) (AGENTS.md:33-103; README.md:133-147).

## 10. Limitations and Gotchas

- **No committed test suite; verification is end-to-end.** UI/streaming changes are checked in the browser UI and model changes via `demo.py` rendering, so regressions have no automated gate (AGENTS.md:27).
- **`pip` is not a supported install path for development.** `pip` ignores `[tool.uv.sources]` and source-builds flash-attn; setup must use `uv sync` (plus `--extra mlx` / `--extra claude` as needed) (AGENTS.md:10-15).
- **Native audio requires system ffmpeg sonames; static binaries fail.** torchcodec dlopens `libtorchcodec_core` per ffmpeg major and needs shared `libavcodec`/`libavformat`/`libavutil`; static-binary PyPI ffmpeg packages do not satisfy the `vui.ffmpeg_libs` probe, and the rootless path fetches an LGPL build into `~/.cache/vui/ffmpeg` (install.sh:233-294; README.md:162-188).
- **`--model` does not select the TTS checkpoint.** It selects the Ollama LLM (default `qwen3.5:4b`); changing the voice model requires a name/path to `Engine()`, and bare `vui` on PyPI is an unrelated package — the engine is `vui-tts` importing as `vui` (README.md:83-103).
- **Single-tenant and env-at-startup assumptions.** `VUI_`-prefixed env vars are read once at startup; workers cross only via `torch.multiprocessing.Queue` with small picklable payloads, and `tts_worker.py`/`voice_turn.py` are latency-sensitive (buffer reuse, CUDA-graph boundaries), constraining how state and payloads can be added (AGENTS.md:107-114).
- **Generated artifacts are git-invisible by design.** Checkpoints, `*.wav`/`*.mp3`/`*.pt`/`*.safetensors`, `prompts/`, `scratch/`, `outputs/`, `cpu/*.onnx`/`*.bin`/`vui_tts`, and most `*.json` are ignored (with only `!sample_texts.json` excepted), so voices, renders, and local memories do not travel with the clone (`.gitignore`:165-187).
- **Wiki-excerpt truncation bounds this analysis.** `demo.py` coverage ends after the MLX loader, `install.sh` after ffmpeg fetching, `sample_texts.json` mid-value, and the README excerpt mid-sentence at Jetson support, so Gradio/CUDA render paths, install tail steps, and device-exclusion behavior below those cut points are not attested here (demo.py:109-268; install.sh:105; sample_texts.json:124; README.md:190-190).

## 11. How It Compares to Alternatives

- **OpenAI Realtime API (hosted):** the managed reference for full-duplex voice with tool use. Vui instead runs the loop locally from one Python server and even exposes a Realtime-compatible `ws://…/v1/realtime` drop-in for OpenAI-spec clients, trading managed quality/ops for self-hosting and backend choice (README.md:54-55).
- **Qwen3-TTS-12Hz family (base codec/model line):** Vui builds its codec and RQ-Transformer head on this line but differentiates with a 219M-active dialogue-conditioned checkpoint, six-channel SQ plus WPS conditioning, shipped voice presets, and CPU/MLX execution paths instead of GPU-only large checkpoints (README.md:39-59).
- **faster-whisper / Moonshine + Ollama / vLLM DIY stacks:** the standard composable recipe Vui adopts for ASR and LLM, but Vui adds the speculative-prefill voice loop, sentence chunking with backpressure, barge-in, the thoughts/tool stream, persistent memories, and hot-swap from the UI rather than leaving integration to the deployer (README.md:51-65).
- **OpenClaw (agent framework with a realtime voice provider):** listed as an integration target via the `openai` realtime provider rather than a competing TTS core; Vui positions as the voice front-end whose task sidecar (`claude_server.py` on `:8642` with MCP discovery) absorbs slow multi-step work that pure voice loops handle poorly (README.md:66-71).

Positioning: Vui is the self-hosted, conversation-conditioned voice loop — small dialogue-aware TTS plus an opinionated ASR → LLM → TTS server with local-first backends and interop endpoints — where hosted realtime APIs optimize for zero-ops quality and DIY stacks optimize for component choice.

## Appendix: Selected Code Snippets

1. Conversation-conditioned synthesis claim (README.md:37-37):

```text
"Most TTS models synthesise one utterance in isolation. Vui Nano generates each reply *inside the conversation*: the whole dialogue so far — your text **and the actual audio of your turn** — lives in the KV cache it decodes from, across a ~6-minute context."
```

2. Engine Python API (README.md:89-103):

```python
from vui.engine import Engine, GenConfig
engine = Engine()                # vui-nano-1.1 downloads from Hugging Face on first use
with engine.new_row() as row:
    codes, audio = row.render("Hello from Vui.", GenConfig(temperature=0.7))
```

3. Agent orientation and setup contract (AGENTS.md:3-15):

```text
"Orientation for AI coding agents working on Vui — a streaming conversational voice assistant (ASR → LLM → TTS) built around a 305M speech transformer over the Qwen3-TTS-12Hz codec."
```

```sh
uv sync                    # base + flash-attn prebuilt wheel (Linux/CUDA)
uv sync --extra mlx        # add Apple Silicon backend
uv sync --extra claude     # add Claude task-server deps
```

4. Bootstrap one-liner and clone contract (bootstrap.sh:2-13; install.sh:28-30):

```sh
# Vui bootstrap — hosted at https://install.fluxions.ai
#
#     curl -fsSL https://install.fluxions.ai | bash
#     curl -fsSL https://install.fluxions.ai | bash -s -- --docker
#
# Clones Vui into $VUI_HOME (default ~/vui), then execs ./install.sh inside it.
# All args after `--` are forwarded to install.sh — see `./install.sh --help`.
```
