# Technical Analysis: CarverXx/jarvis-v3

**Repository:** https://github.com/CarverXx/jarvis-v3
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: running an always-on voice assistant without depending on cloud LLM, ASR, or TTS services, while still getting both low-latency conversation and multi-step tool execution from a single host. A single LLM call cannot be simultaneously fast enough for chit-chat and capable enough for agentic tool use.

The repo addresses it with a local-first dual-brain design: a fast conversational layer speaks immediately while a separate executor agent performs real work, fronted by a wake-word → ASR → response → TTS voice loop running as systemd services on one Linux box (01-overview.md:19-21, 01-overview.md:27-31). Everything except explicit `web.search` via Tavily stays on the host (01-overview.md:65-69). The primary user is a single technical owner-operator on a high-VRAM Linux workstation with a USB microphone/speaker pair.

## 2. High-Level Architecture

```
Microphone (parec 16 kHz PCM queue)
  │
  ▼
openWakeWord (hey_jarvis_v0.1) + custom verifier ──► Silero VAD (end-of-speech)
  │
  ▼
Qwen3-ASR shim (:8002)
  │
  ▼
Subconscious (SGLang Qwen3.6-35B-A3B-FP8, :8000) ──► direct 1-2 sentence reply
  │                                                    (no tool call, ~300 ms)
  ▼ Invoke_hermes(task=...) via OpenAI tool-calling
Hermes Agent CLI via hermes-shim (:8004) + MCP tools (:8005)
(fs / rag / web / cf / system / notes)
  │
  ▼
Subconscious rephrase (1-2 sentences, Chinese)
  │
  ▼
VoxCPM2 TTS (:8003, 48 kHz PCM) ──► Speaker (mic hard-muted during playback)
  │
  ▼
JSONL event stream ──► jarvis-tui (tui/dashboard.py, 6-panel rich.Live view)
```

Data-flow narrative (01-overview.md:100-121, 01-overview.md:107):

1. Capture and gate: `parec` feeds a 16 kHz PCM queue; openWakeWord model `hey_jarvis_v0.1` plus a custom per-owner verifier and Silero VAD detect the wake phrase and end-of-speech (01-overview.md:100-121, 01-overview.md:75-83).
2. Transcribe: audio goes to the Qwen3-ASR FastAPI shim on :8002 (01-overview.md:125-132).
3. Converse or escalate: the Subconscious (SGLang-served Qwen3.6 on :8000) answers chit-chat directly or emits an `invoke_hermes(task=...)` tool call when the turn needs real work (01-overview.md:44-47).
4. Execute: Hermes runs a multi-step agent loop with retries and summarisation through the MCP tool server on :8005 (`fs`, `rag`, `web`, `cf`, `system`) (01-overview.md:35-40, 01-overview.md:125-132).
5. Speak and observe: VoxCPM2 TTS on :8003 streams 48 kHz audio to the speaker with echo suppression; the daemon state machine (IDLE → LISTENING → PROCESSING → RESPONDING → FOLLOW_UP_LISTEN) emits a JSONL event stream tailed by `jarvis-tui` (01-overview.md:107, 01-overview.md:80-83, 01-overview.md:136-148).

Persistent state lives in: user Markdown vaults under `vault/ref/` + `vault/wiki/` (knowledge base, read via `rag.search` + `fs.read`) (01-overview.md:90-96); voice/wake assets under `assets/` (`jarvis_voice_ref.wav`, `hey_jarvis_verifier.pkl`, wake sounds) (01-overview.md:216-242); runtime logs and `events.jsonl` excluded from git (`.gitignore:45-48`); session identity carried as `X-Session-Id` for Hermes `--resume` mapping (`config.py:129-130`).

## 3. The Dual Brain

The central concept is the split between a fast Subconscious and a slower Hermes executor, because one LLM cannot be both fast and tool-capable (01-overview.md:35-40). Representation: two roles driven by the same SGLang backend but with different latency budgets, prompts, and I/O contracts (01-overview.md:40-47).

Named kinds/types (01-overview.md:40-47):

- Subconscious (潜意识) — conversational layer; model SGLang-served Qwen3.6-35B-A3B-FP8; target TTFB < 1 s, ≤ 2-sentence replies; mechanism OpenAI tool-calling with `invoke_hermes(task=...)` (01-overview.md:44-47).
- Main consciousness / Hermes (主意识) — executor; Hermes Agent CLI on the same SGLang backend; runs `rag.search` / `web.search` / `fs.*` / `system.*` / `cf.*` / note-taking tools; 5–30 s per task with multi-step reasoning, retries, summarisation (01-overview.md:44-47).
- Escalation primitive `invoke_hermes(task=...)` — the single tool the Subconscious may call; e.g. "今天天气" → `invoke_hermes(task="查今天上海天气")` with heartbeat tone → `web.search` → spoken 2-sentence reply; "你好" → direct reply, no tool call (01-overview.md:49-56).
- Wiki-grounded QA pattern — Hermes `rag.search` then `fs.read` on the Markdown file, rephrased by the Subconscious (01-overview.md:58-61).

Key query (verbatim design statement, 01-overview.md:19-21):

> **A local-first, always-on voice assistant with a dual-brain architecture
> that lets a fast conversational LLM speak for you while a tool-calling
> agent actually runs the commands.**

## 4. LLM / External Service Integration

- LLM provider: self-hosted Qwen3.6-35B-A3B-FP8 (hybrid MoE + Gated DeltaNet) served by SGLang at `http://127.0.0.1:8000` with `qwen3_coder` tool parser, 128K context; alternate models Qwen3.6-14B / Llama-3.3-70B swappable with config changes (01-overview.md:40-47, 01-overview.md:125-132, 01-overview.md:159-160, `config.py:135-144`).
- Required local calls: Subconscious chat completions (:8000); Qwen3-ASR transcription shim (:8002); VoxCPM2 streaming TTS (:8003); Hermes Agent CLI via hermes-shim OpenAI-compatible `/v1/chat/completions` (:8004); MCP tool server (:8005) (01-overview.md:125-132).
- Optional external calls: Tavily `web.search` is the only call that leaves the host; Cloudflare (`cf.*`) and system tools depend on user keys (01-overview.md:65-69, `config.py:167-228`).
- Env vars: `SGLANG_URL`, `SGLANG_MODEL` (default `Qwen/Qwen3.6-35B-FP8`), `SGLANG_API_KEY` (set via systemd env), `JARVIS_SESSION_ID`, `JARVIS_SUBCONSCIOUS_PROMPT`, `JARVIS_HERMES_VOICE_PROMPT`, `JARVIS_MODELS_DIR`, `JARVIS_ASSETS_DIR`, optional Tavily/Cloudflare keys under `~/.config/jarvis/`, plus per-port overrides (`VLLM_PORT`, `QWEN3_ASR_URL`, `VOXCPM_URL`, `HERMES_SHIM_URL`) (`config.py:38-54`, `config.py:135-144`, 01-overview.md:165-204, 01-overview.md:246-254).

## 5. The Voice-Turn Pipeline

Primary workflow: wake word → ASR → Subconscious → optional Hermes → TTS (01-overview.md:27-28, 01-overview.md:107). The wiki component pages expose file paths and tuning but not per-function signatures; steps below cite the file:line grounding available.

1. Audio capture (`config.py:57-75`): mic selected by substring hint `MIC_DEVICE_HINT="Poly Sync"` at `MIC_SAMPLE_RATE=16000` in `MIC_CHUNK_MS=32` (512-sample = Silero VAD frame) chunks, with `MIC_INPUT_GAIN=2.5` and soft-clip protection (`config.py:59-66`, `config.py:68-75`).
2. Wake detection (`daemon/wake_word.py`; `config.py:78-91`): openWakeWord `WAKE_WORD_MODEL="hey_jarvis_v0.1"` on onnxruntime at `WAKE_THRESHOLD=0.7`, gated by `VAD_WAKE_THRESHOLD=0.5`; personalised verifier trained from ~20 own-voice samples via `scripts/split_wake_recording.py` + `scripts/train_wake_verifier.py` → `assets/hey_jarvis_verifier.pkl` auto-loaded by `daemon/wake_word.py` (01-overview.md:75-78, 01-overview.md:229-242).
3. Turn-taking (`config.py:95-114`): state machine IDLE → LISTENING → PROCESSING → RESPONDING → FOLLOW_UP_LISTEN with `LISTEN_HARD_TIMEOUT_S=10.0`, `EOS_SILENCE_S=0.5`, `MIN_UTTERANCE_S=0.3`, `FOLLOWUP_WINDOW_S=15.0` (re-speak without wake word), `POST_TTS_GRACE_MS=800` plus mic-queue drain and 1.5 s wake cooldown for echo safety (01-overview.md:80-83, 01-overview.md:107).
4. Transcribe and think (`config.py:135-144`): Qwen3-ASR shim (:8002) → Subconscious on SGLang (:8000) with `SUBCONSCIOUS_HISTORY_N=6` turns and a short Chinese system prompt (`config.py:167-228`); chit-chat answered directly, date/time/weather/news/prices/vault/Cloudflare/service-status/deep tasks routed to `invoke_hermes` (01-overview.md:44-47).
5. Execute (`config.py:117-148`): Hermes runs up to `HERMES_TIMEOUT_S=120` with replies capped at `HERMES_MAX_REPLY_CHARS=500`, session continuity via `SESSION_ID_ENV` / `X-Session-Id` `--resume` mapping, heartbeat beep every `WAITING_BEEP_INTERVAL_S=2.0`; tool results are trusted facts the Subconscious restates in 1–2 sentences, and only `(主意识处理失败`, `(主意识无回应`, `(工具执行失败` prefixes count as failure (`config.py:121-130`, `config.py:146-148`, `config.py:167-228`).
6. Speak and monitor (`config.py:150-165`; 01-overview.md:136-150): wake-confirm hierarchy `awake_tone.wav` → `voxcpm_zai.wav` → `awake.wav`; voice clone from `assets/jarvis_voice_ref.wav` built by `scripts/trim_voice_ref.py` (4–8 s clip); `python tui/dashboard.py` (`jarvis-tui`) renders State, Mic/Wake, ASR, Subconscious, Hermes, TTS panels plus timestamped subsystem errors from the JSONL stream (01-overview.md:71-73, 01-overview.md:216-219, 01-overview.md:136-150).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `config.py` | 232 (`config.py:1-232`) | Single env-driven configuration imported by all services: paths, ports/URLs, audio, wake/VAD, timings, Hermes/session, prompts, log level |
| `requirements.txt` | 22 (`requirements.txt:1-22`) | Pinned Python stack for ASR/TTS/wake/VAD/audio/HTTP services |
| `.gitignore` | ~109 (`.gitignore:1-109`) | Excludes secrets, audio/model assets, logs/runtime state, venv/build, personalization files |
| `daemon/wake_word.py` | cited, line count not in wiki | Loads openWakeWord model plus custom `hey_jarvis_verifier.pkl` |
| `tui/dashboard.py` | cited, line count not in wiki | `jarvis-tui`: tails JSONL event stream, renders 6-panel live dashboard |
| `scripts/trim_voice_ref.py` | cited, line count not in wiki | Trims user clip to `assets/jarvis_voice_ref.wav` for voice cloning |
| `scripts/split_wake_recording.py` | cited, line count not in wiki | Splits batch wake recording into training samples |
| `scripts/train_wake_verifier.py` | cited, line count not in wiki | Trains custom openWakeWord verifier to `assets/hey_jarvis_verifier.pkl` |
| `scripts/audit_no_secrets.py` | cited, line count not in wiki | Pre-push secret scan referenced by `.gitignore` header |
| `systemd/*.sample` | cited, line count not in wiki | Service unit templates for sglang, shims, MCP server, daemon |
| `assets/jarvis_voice_ref.wav` | binary | 4–8 s voice-clone reference reused every TTS response |
| `assets/hey_jarvis_verifier.pkl` | binary | User-specific wake verifier raising recall, cutting false positives |
| `docs/landing.html` | cited, line count not in wiki | Landing page pointer from README |
| `docs/customize.md` | cited (TODO), line count not in wiki | Persona/prompt customization doc |
| `vault/ref/` + `vault/wiki/` | user data dirs | Markdown knowledge base queried via `rag.search` + `fs.read` |
| `user_persona.py` / `user_persona.yaml` | user files, git-ignored | Personalization files kept out of version control |

## 7. Dependencies

Required first, with exact constraint strings (`requirements.txt:1-22`):

| Package | Version constraint | Purpose |
|---|---|---|
| `qwen-asr` | `qwen-asr>=0.0.6` | Qwen3-ASR-1.7B official package (pulls torch 2.11 + cuda13 wheels) |
| `voxcpm` | `voxcpm>=0.1.0` | OpenBMB VoxCPM2 official TTS package |
| `openwakeword` | `openwakeword==0.4.0` | Wake-word detection, pinned to avoid `tflite-runtime` on Linux+Py3.12 |
| `onnxruntime` | `onnxruntime>=1.24` | Runtime for openWakeWord + silero-vad |
| `silero-vad` | `silero-vad>=5.0` | Voice activity detection (ONNX) |
| `sounddevice` | `sounddevice>=0.5.0` | PortAudio/PipeWire audio capture and playback |
| `soundfile` | `soundfile>=0.13.0` | Audio file I/O |
| `numpy` | `numpy>=2.0,<3.0` | Numeric/audio array processing |
| `scipy` | `scipy>=1.12.0` | `scipy.signal` resampling |
| `fastapi` | `fastapi>=0.115.0` | Shim/MCP HTTP services |
| `uvicorn[standard]` | `uvicorn[standard]>=0.30.0` | ASGI server for shims |
| `httpx` | `httpx>=0.28.0` | Inter-service HTTP client |
| `python-multipart` | `python-multipart>=0.0.20` | Form/multipart handling for HTTP shims |
| `pydantic` | `pydantic>=2.0` | Config/payload validation |

Non-pip requirements (01-overview.md:154-160, 01-overview.md:258-269): SGLang server, Hermes Agent CLI pointed at `http://127.0.0.1:8000/v1`, model weights `Qwen/Qwen3.6-35B-A3B-FP8` + `Qwen/Qwen3-ASR-1.7B` + `openbmb/VoxCPM2`, CUDA 12.4+ (tested 13.1), Python 3.12, ≥50 GB VRAM (tested 96 GB RTX PRO 6000), Ubuntu 24.04 with PipeWire/PulseAudio.

## 8. CLI / Usage Surface

Entry points (01-overview.md:165-204, 01-overview.md:136-138, 01-overview.md:216-242):

| Command | Purpose |
|---|---|
| `enable --now sglang mcp-server qwen3-asr-shim voxcpm2-tts hermes-shim jarvis-v3` (systemd units from `systemd/*.sample`) | Start the full stack |
| `jarvis-tui` (i.e. `python tui/dashboard.py`) | Live 6-panel terminal dashboard on the JSONL event stream |
| `python scripts/trim_voice_ref.py --input <clip>` | Build `assets/jarvis_voice_ref.wav` |
| `python scripts/split_wake_recording.py --input <batch> --out-dir <dir> --n <count>` | Split wake-word training samples |
| `python scripts/train_wake_verifier.py` | Train `assets/hey_jarvis_verifier.pkl` |
| `scripts/audit_no_secrets.py` | Pre-push secret audit per `.gitignore` header |

Env-var and config tables (`config.py:15-65`, `config.py:135-148`, 01-overview.md:246-254):

| Variable | Default | Effect |
|---|---|---|
| `JARVIS_MODELS_DIR` | `~/models` | Base dir for ASR/TTS model weights |
| `QWEN3_ASR_MODEL_PATH` | `MODELS_DIR / "Qwen3-ASR-1.7B"` | ASR weights path |
| `VOXCPM_MODEL_PATH` | `MODELS_DIR / "VoxCPM2"` | TTS weights path |
| `HERMES_BIN` | `~/.local/bin/hermes` | Hermes Agent CLI binary |
| `JARVIS_ASSETS_DIR` | `~/jarvis-v3-repo/assets` | Sounds, voice ref, verifier |
| `VLLM_PORT` / `SGLANG_URL` | `8000` / `http://127.0.0.1:8000` | LLM backend endpoint |
| `QWEN3_ASR_SHIM_PORT` / `QWEN3_ASR_URL` | `8002` / `http://127.0.0.1:8002` | ASR shim |
| `VOXCPM_PORT` / `VOXCPM_URL` | `8003` / `http://127.0.0.1:8003` | TTS shim |
| `HERMES_SHIM_PORT` / `HERMES_SHIM_URL` | `8004` / `http://127.0.0.1:8004` | Hermes OpenAI-compat shim |
| `MIC_DEVICE_HINT` / `SPEAKER_DEVICE_HINT` | `"Poly Sync"` / `"Poly Sync"` | Substring device match, not index |
| `JARVIS_SUBCONSCIOUS_PROMPT` | built-in Chinese prompt | Persona override without code edits |
| `JARVIS_HERMES_VOICE_PROMPT` | built-in prompt | Hermes voice-summary prompt override |
| `JARVIS_SESSION_ID` | regenerated per restart | Session continuity for Hermes `--resume` |
| `SGLANG_MODEL` | `Qwen/Qwen3.6-35B-FP8` | Served LLM (14B/70B swappable) |
| `LOG_LEVEL` | `"INFO"` | Logging verbosity |

Install sequence: clone → `python3.12 -m venv` → `pip install -r requirements.txt` → download three model weights → install Hermes CLI → optional Tavily/Cloudflare keys in `~/.config/jarvis/` → install systemd units → enable services → `jarvis-tui` (01-overview.md:165-204).

## 9. Extensibility Points

- New persona/behavior without code: set `JARVIS_SUBCONSCIOUS_PROMPT` / `JARVIS_HERMES_VOICE_PROMPT` (see `docs/customize.md`); Subconscious prompt lives in `config.py:167-228`.
- New tools for Hermes: extend the MCP server on :8005 (`fs` / `rag` / `web` / `cf` / `system` namespaces); Hermes shim on :8004 passes them through.
- New knowledge: add Markdown under `vault/ref/` + `vault/wiki/`; consumed via `rag.search` + `fs.read` with no pipeline change (01-overview.md:90-96).
- New wake sensitivity: retune `WAKE_THRESHOLD`, `VAD_WAKE_THRESHOLD`, `VAD_FOLLOWUP_THRESHOLD` in `config.py:78-91`, or retrain `assets/hey_jarvis_verifier.pkl` via `scripts/split_wake_recording.py` + `scripts/train_wake_verifier.py` loaded by `daemon/wake_word.py`.
- New voice: replace `assets/jarvis_voice_ref.wav` via `scripts/trim_voice_ref.py`; empty/missing falls back to random voice-design voice (`config.py:161-165`).
- New turn-taking: adjust `LISTEN_HARD_TIMEOUT_S`, `EOS_SILENCE_S`, `MIN_UTTERANCE_S`, `FOLLOWUP_WINDOW_S`, `POST_TTS_GRACE_MS` in `config.py:95-114`.
- New observability: extend `tui/dashboard.py` panels consuming the daemon JSONL event stream (01-overview.md:136-150).

## 10. Limitations and Gotchas

- **Hardware floor is high:** ~50 GB VRAM minimum with all three models loaded simultaneously; realistically ≥30 B parameters for reliable Chinese tool-calling, with 14 B / 12 B / small models accepted only with a quality hit (01-overview.md:159-160, 01-overview.md:258-269).
- **Single-machine, single-user Linux assumption:** 5–6 systemd services on one box, PipeWire/PulseAudio with a Poly Sync 10 needing a 16 kHz `.mono-fallback` source; tested only on Ubuntu 24.04 + CUDA 13.1 + RTX PRO 6000 (01-overview.md:123-132, 01-overview.md:154-158).
- **Self-trigger and echo fragility:** TTS output can retrigger the wake word (observed TTS-echo "在" spam fixed by `POST_TTS_GRACE_MS` 500→800 ms plus mic-queue drain and 1.5 s wake cooldown); mitigation depends on hard-muting the mic during TTS (01-overview.md:80-83, `config.py:95-114`).
- **Hermes latency and reply truncation:** deep tasks take 40–90 s against `HERMES_TIMEOUT_S=120`, with spoken replies hard-capped at `HERMES_MAX_REPLY_CHARS=500` (`config.py:121-122`).
- **Narrow capability boundary by design:** calendar, mail, iMessage, WeChat, smart-home, music, calls, video meetings, and booking are refused in one sentence with no tool call; realtime facts must come from tools, never fabrication (`config.py:167-228`).
- **Wiki coverage is thin:** only two component pages (overview + top-level files) ground this analysis; per-function signatures for the daemon, shims, MCP server, and TUI are not cited, and the Status list ends in a truncated empty bullet with Macro-components listing only `top-level-files/` (01-overview.md:273-282).

## 11. How It Compares to Alternatives

- OVOS / Mycroft: full open-source voice stack with skills ecosystem and bus architecture; heavier multi-device platform versus this repo's single-box dual-brain daemon.
- Rhasspy / Home Assistant Wyoming: local-first voice pipeline (wake → STT → intent → TTS) optimized for smart-home intents; intent/HA integration focus versus this repo's general tool-calling Hermes agent.
- Home Assistant Assist + local LLM: appliance-style assistant with year-of-voice pipeline and ESP32 satellites; productized HA path versus this repo's workstation-grade FP8 LLM + agent loop.
- DIY whisper.cpp + Piper + llama.cpp stack: minimal composable local pipeline builders control directly; maximum hackability but no dual-brain escalation, MCP tool namespaces, or TUI event stream.

Positioning: this repo trades the low hardware floor and smart-home focus of Rhasspy/Wyoming/Assist for a workstation-class local agent — one owner, one GPU box, one voice — where a fast talker and a slow tool-executor share the same self-hosted model.

## Appendix: Selected Code Snippets

1. Centralized config contract (`config.py:1-6`):

```
"""JARVIS v3 — centralized configuration (env-driven). All services (shims + daemon) import values from here. Runtime overrides via environment variables (pattern copied from jarvis-v2 config.py)."""
```

2. Secrets guardrail (`.gitignore:1-22`):

```
# JARVIS v3 — gitignore
*.key
*.token
*.pem
*.p12
.env
.env.local
.env.*.local
secrets/
config/*.secret.*
# If you hardcode an API key by mistake, `git diff --cached` will still show
# it. Run `scripts/audit_no_secrets.py` before pushing.
```

3. Pinned Python stack with rationale (`requirements.txt:1-22`):

```
qwen-asr>=0.0.6         # Qwen3-ASR-1.7B 官方 pip 包 (pulls torch 2.11 + cuda13 wheels)
voxcpm>=0.1.0           # OpenBMB VoxCPM2 官方包
openwakeword==0.4.0     # 固定 0.4.0 — 此版本只依赖 onnxruntime，避免 0.6+ 强依赖 tflite-runtime (Linux+Py3.12 无 wheel)
onnxruntime>=1.24       # openwakeword + silero-vad 运行时
silero-vad>=5.0         # Silero VAD (ONNX)
sounddevice>=0.5.0      # PortAudio / PipeWire 采集+播放
soundfile>=0.13.0
numpy>=2.0,<3.0
scipy>=1.12.0           # scipy.signal resample
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
httpx>=0.28.0
python-multipart>=0.0.20
pydantic>=2.0
```

4. Dual-brain design statement (01-overview.md:19-21):

> **A local-first, always-on voice assistant with a dual-brain architecture
> that lets a fast conversational LLM speak for you while a tool-calling
> agent actually runs the commands.**
