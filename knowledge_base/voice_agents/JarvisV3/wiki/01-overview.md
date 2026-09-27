> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** JARVIS v3 is a local-first, always-on voice assistant with a dual-brain architecture where a fast conversational LLM speaks while a tool-calling agent executes real work (01-overview.md:19-21, 01-overview.md:27-31).
## Key points
- JARVIS v3 is a local-first always-on voice assistant that runs entirely on the host with no cloud LLM/ASR/TTS, except explicit `web.search` via Tavily (01-overview.md:27-31, 01-overview.md:65-69).
- It splits cognition into two brains: a Subconscious conversational layer and a Hermes executor agent, because one LLM cannot be both fast and smart with tools (01-overview.md:35-40).
- The Subconscious uses OpenAI tool-calling with `invoke_hermes(task=...)` to escalate turns needing real work, while Hermes runs a multi-step agent loop with retries and summarisation (01-overview.md:44-47).
- The voice pipeline is wake word ("Hey Jarvis") → ASR → Subconscious → optional Hermes → TTS, with a state machine IDLE → LISTENING → PROCESSING → RESPONDING → FOLLOW_UP_LISTEN (01-overview.md:27-28, 01-overview.md:107).
- Five to six systemd services on one Linux box serve the LLM (:8000), ASR (:8002), TTS (:8003), Hermes shim (:8004), MCP tools (:8005), plus the main daemon (01-overview.md:123-132).
- The `jarvis-tui` dashboard tails a JSONL event stream and renders a 6-panel live view of state, mic/wake, ASR, Subconscious, Hermes, and TTS (01-overview.md:136-148).
- Personalisation is via a 4–8 s voice-cloning reference clip, an openWakeWord custom verifier trained on ~20 own-voice samples, and two prompt env vars without code edits (01-overview.md:71-78, 01-overview.md:210-252).
---
## Dual-brain architecture
The chunk defines the split explicitly (01-overview.md:40-47):
| | Subconscious (潜意识) | Main consciousness / Hermes (主意识) |
|---|---|---|
| **Model** | SGLang-served Qwen3.6-35B-A3B-FP8 (hybrid MoE + Gated DeltaNet) | Hermes Agent CLI driven by the same SGLang backend |
| **Role** | Conversational layer — replies to chit-chat, handles persona, decides when to escalate | Executor — runs `rag.search` / `web.search` / `fs.*` / `system.*` / `cf.*` / note-taking tools through an MCP server |
| **Latency target** | TTFB < 1 s, ≤ 2 sentence replies | 5–30 s depending on tool depth |
| **Mechanism** | OpenAI tool-calling — if the turn smells like "needs real work", return a `tool_calls[0]` with `invoke_hermes(task=...)` | Real agent loop: multi-step reasoning, tool retries, result summarisation |
Verbatim design statement (01-overview.md:19-21):
> **A local-first, always-on voice assistant with a dual-brain architecture
> that lets a fast conversational LLM speak for you while a tool-calling
> agent actually runs the commands.**
Two worked examples ground the mechanism (01-overview.md:49-56): "今天天气" triggers `invoke_hermes(task="查今天上海天气")` with heartbeat tone → `web.search` → 2-sentence spoken reply via VoxCPM2 48 kHz audio; "你好" replies directly with ~300 ms round-trip and no tool call. Wiki-grounded QA uses Hermes `rag.search` then `fs.read` on the Markdown file, rephrased by the Subconscious (01-overview.md:58-61).
## End-to-end pipeline and services
Audio flow is Microphone → `parec` (PulseAudio) → 16 kHz PCM queue → openWakeWord (`hey_jarvis_v0.1`) + custom verifier and Silero VAD for end-of-speech → Qwen3-ASR :8002 → Subconscious (SGLang Qwen3.6, :8000) → optional Hermes Agent CLI via MCP :8005 (`fs` / `rag` / `web` / `cf` / ...) → VoxCPM2 TTS :8003 → Speaker (01-overview.md:100-121). Services table (01-overview.md:125-132):
| Service | Port | What it does |
|---|---|---|
| `sglang` | :8000 | Serves Qwen3.6-35B-A3B-FP8 (128K ctx, qwen3_coder tool parser) |
| `qwen3-asr-shim` | :8002 | FastAPI wrapper over `qwen_asr` Python API |
| `voxcpm2-tts` | :8003 | FastAPI streaming 48 kHz int16 PCM, zero-shot voice cloning |
| `hermes-shim` | :8004 | OpenAI `/v1/chat/completions` wrapper over Hermes Agent CLI |
| `mcp-server` | :8005 | MCP tool server (fs / web / rag / cf / system namespaces) |
| `jarvis-v3` | — | Main daemon: mic, wake, VAD, state machine, audio player, TUI event emitter |
The chunk states "5 systemd services run on a single Linux box" but then lists 6 rows including the daemon (01-overview.md:123-132).
## Terminal dashboard
`jarvis-tui` (i.e. `python tui/dashboard.py`) tails the daemon's JSONL event stream and renders a live six-panel `rich.Live` TUI (01-overview.md:136-138). Panels (01-overview.md:140-146): State (node + transitions, session id); Mic/Wake (RMS dBFS + 30-s sparkline + peak wake score); ASR (transcript + language + elapsed); Subconscious (user message + streaming tokens + tool call); Hermes ("running …Xs" pulse, final reply + success/fail); TTS (progress bar, chars remaining, elapsed). Subsystem errors surface in the bottom panel with timestamp and component tag (01-overview.md:149-150).
## Local-first features
Everything local: vLLM/SGLang LLM, Qwen3-ASR STT, VoxCPM2 zero-shot TTS with only Tavily web search leaving the host (01-overview.md:65-69). Voice cloning needs one 4–8 s clean reference clip reused for every response (01-overview.md:71-73). Wake personalisation trains an `openWakeWord` verifier on 20 own-voice samples via `scripts/split_wake_recording.py` to raise recall and cut TV/family/podcast false positives (01-overview.md:75-78). Echo safety: daemon hard-mutes mic during TTS, flushes input queue on transitions, 1.5 s wake-cooldown after IDLE to break self-trigger loops (01-overview.md:80-83). Knowledge-base hook: point at a Markdown wiki under `vault/ref/` + `vault/wiki/` and the agent uses `rag.search` (keyword match) + `fs.read` to answer from user notes (01-overview.md:90-96).
## Install, personalise, requirements
Install targets Linux server + USB mic/speaker; tested on RTX PRO 6000 Blackwell 96 GB, Ubuntu 24.04, CUDA 13.1 with Plantronics Poly Sync 10 needing a 16 kHz `.mono-fallback` PulseAudio source (01-overview.md:154-158). Needs ≥50 GB VRAM for the FP8 stack; Qwen3.6-14B / Llama-3.3-70B swappable with config changes (01-overview.md:159-160). Walk-through is clone → `python3.12 -m venv` → `pip install -r requirements.txt` → download `Qwen/Qwen3.6-35B-A3B-FP8`, `Qwen/Qwen3-ASR-1.7B`, `openbmb/VoxCPM2` → install Hermes Agent CLI pointed at `http://127.0.0.1:8000/v1` → optional Tavily/Cloudflare keys in `~/.config/jarvis/` → install `systemd/*.sample` units → `enable --now sglang mcp-server qwen3-asr-shim voxcpm2-tts hermes-shim jarvis-v3` → `jarvis-tui` (01-overview.md:165-204). Personalisation: `python scripts/trim_voice_ref.py --input <clip>` writes `assets/jarvis_voice_ref.wav` (01-overview.md:216-219); `python scripts/split_wake_recording.py --input <batch> --out-dir <dir> --n <count>` plus `python scripts/train_wake_verifier.py` writes `assets/hey_jarvis_verifier.pkl` auto-loaded by `daemon/wake_word.py` (01-overview.md:229-242). Persona without code edits via exact env names `JARVIS_SUBCONSCIOUS_PROMPT` and `JARVIS_HERMES_VOICE_PROMPT`, details in `docs/customize.md` (TODO) (01-overview.md:246-254). Requirements table (01-overview.md:258-265):
| | Minimum | Tested |
|---|---|---|
| GPU VRAM | ~50 GB (SGLang Qwen3.6 + VoxCPM2 + Qwen3-ASR, all loaded simultaneously) | 96 GB (RTX PRO 6000 Blackwell) |
| CPU | 8 cores (wake+VAD is pure CPU) | 16 cores |
| RAM | 32 GB | 96 GB |
| OS | Linux with PipeWire/PulseAudio | Ubuntu 24.04.4 LTS |
| Python | 3.12 | 3.12.x |
| CUDA | 12.4+ | 13.1 |
≈30 B is the realistic minimum for reliable Chinese tool-calling; smaller Qwen3-14B / Gemma-3-12B / Mistral-Small accepted with quality hit (01-overview.md:267-269). Landing page pointer: `docs/landing.html` (01-overview.md:23-25).
## Status and truncation note
Claimed done: wake → ASR → Subconscious → optional Hermes → TTS end-to-end; 5 systemd services auto-start surviving restart (SIGKILL + autoresume tested); custom verifier loaded; VoxCPM2 cloning with RMS stddev < 1 dB (01-overview.md:273-276). The chunk's Status list ends with a truncated empty bullet (01-overview.md:277) and its Macro-components section lists only `top-level-files/` with no further detail (01-overview.md:279-282); those cut contents are not guessed here.
**Covers:** README (voice-interaction premise, dual-brain table, pipeline diagram, services/requirements tables, install/personalise commands, TUI panels, status list) as captured in chunks/01-overview.md; referenced-only paths `docs/landing.html`, `docs/customize.md`, `vault/ref/`, `vault/wiki/`, `daemon/wake_word.py`, `scripts/*`, `systemd/*`, `tui/dashboard.py`
