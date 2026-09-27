> [[index|Wiki]] | [[summary|Summary]]
# CarverXx/jarvis-v3 — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** JARVIS v3 is a local-first, always-on voice assistant with a dual-brain architecture where a fast conversational LLM speaks while a tool-calling agent executes real work (01-overview.md:19-21, 01-overview.md:27-31).
## Key points
- JARVIS v3 is a local-first always-on voice assistant that runs entirely on the host with no cloud LLM/ASR/TTS, except explicit `web.search` via Tavily (01-overview.md:27-31, 01-overview.md:65-69).
- It splits cognition into two brains: a Subconscious conversational layer and a Hermes executor agent, because one LLM cannot be both fast and smart with tools (01-overview.md:35-40).
- The Subconscious uses OpenAI tool-calling with `invoke_hermes(task=...)` to escalate turns needing real work, while Hermes runs a multi-step agent loop with retries and summarisation (01-overview.md:44-47).
- The voice pipeline is wake word ("Hey Jarvis") → ASR → Subconscious → optional Hermes → TTS, with a state machine IDLE → LISTENING → PROCESSING → RESPONDING → FOLLOW_UP_LISTEN (01-overview.md:27-28, 01-overview.md:107).
- Five to six systemd services on one Linux box serve the LLM (:8000), ASR (:8002), TTS (:8003), Hermes shim (:8004), MCP tools (:8005), plus the main daemon (01-overview.md:123-132).
- The `jarvis-tui` dashboard tails a JSONL event stream and renders a 6-panel live view of state, mic/wake, ASR, Subconscious, Hermes, and TTS (01-overview.md:136-148).
- Personalisation is via a 4–8 s voice-cloning reference clip, an openWakeWord custom verifier trained on ~20 own-voice samples, and two prompt env vars without code edits (01-overview.md:71-78, 01-overview.md:210-252).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** Top-level files define repo-wide guardrails and defaults — `.gitignore` blocks secrets, binaries, and runtime state from git, `config.py` centralises every path, port, audio, wake-word, timing, and LLM setting behind env vars, and `requirements.txt` pins the ASR/TTS/wake/VAD/audio/HTTP dependency set.
## Key points
- `.gitignore` never commits secrets or credentials (`*.key`, `*.token`, `*.pem`, `*.p12`, `.env*`, `secrets/`, `config/*.secret.*`) and tells contributors to run `scripts/audit_no_secrets.py` before pushing (`.gitignore:14-25`).
- `.gitignore` keeps large/user-specific audio and model artefacts out of git, including `assets/*.wav|mp3|flac|m4a|pkl`, `assets/wake_samples/`, and `scripts/*.wav` (`.gitignore:30-40`).
- `.gitignore` excludes logs and runtime state (`logs/`, `*.log`, `events.jsonl`, `jarvis-v3-logs/`), standard Python/venv build outputs, editors/OS files, `vendor/`, caches, and user personalization files `user_persona.py|yaml` (`.gitignore:45-48`, `.gitignore:53-79`, `.gitignore:85-95`, `.gitignore:100-109`).
- `config.py` is the single env-driven configuration imported by all services (shims + daemon), following the jarvis-v2 `config.py` pattern (`config.py:1-6`).
- `config.py` centralises paths (`MODELS_DIR`, `QWEN3_ASR_MODEL_PATH`, `VOXCPM_MODEL_PATH`, `HERMES_BIN`, `ASSETS_DIR`, `AWAKE_WAV`, `ERROR_WAV`), four service ports/URLs (`VLLM_PORT`, `QWEN3_ASR_SHIM_PORT`, `VOXCPM_PORT`, `HERMES_SHIM_PORT` and matching `*_URL`), and audio device hints plus sample rates (`MIC_DEVICE_HINT`, `SPEAKER_DEVICE_HINT`, `MIC_SAMPLE_RATE`, `TTS_SAMPLE_RATE`) (`config.py:15-27`, `config.py:31-44`, `config.py:49-65`).
- `config.py` hard-codes voice-pipeline tuning: 32 ms mic chunks, `MIC_INPUT_GAIN=2.5` with soft-clip protection, `WAKE_WORD_MODEL=hey_jarvis_v0.1` with `WAKE_THRESHOLD=0.7`, VAD gates `0.5` (wake) / `0.7` (follow-up), and turn-taking timeouts (`LISTEN_HARD_TIMEOUT_S=10.0`, `EOS_SILENCE_S=0.5`, `MIN_UTTERANCE_S=0.3`, `FOLLOWUP_WINDOW_S=15.0`, `POST_TTS_GRACE_MS=800`) (`config.py:66-114`).
- `config.py` defines the dual-brain runtime: Hermes limits (`HERMES_TIMEOUT_S=120`, `HERMES_MAX_REPLY_CHARS=500`), regenerable `SESSION_ID_ENV`, SGLang backend (`SGLANG_URL`, `SGLANG_MODEL=Qwen/Qwen3.6-35B-FP8`, `SGLANG_API_KEY`, `SUBCONSCIOUS_HISTORY_N=6`), waiting/wake sounds (`WAITING_BEEP_*`, `AWAKE_TONE_WAV`, `AWAKE_ZAI_WAV`), voice-clone reference (`VOXCPM_REFERENCE_WAV`), the Chinese `SUBCONSCIOUS_SYSTEM_PROMPT`, and `LOG_LEVEL=INFO` (`config.py:117-232`).
- `requirements.txt` pins the full Python stack: `qwen-asr`, `voxcpm`, `openwakeword==0.4.0` (pinned to avoid `tflite-runtime` on Linux+Py3.12) plus `onnxruntime`/`silero-vad`, audio I/O (`sounddevice`, `soundfile`, `numpy>=2.0,<3.0`, `scipy`), HTTP services (`fastapi`, `uvicorn[standard]`, `httpx`, `python-multipart`), and `pydantic>=2.0` (`requirements.txt:1-22`).

## The system in five moves
1. A local-first always-on voice assistant splits cognition into a fast Subconscious speaker and a Hermes tool-calling executor.
2. Turns flow wake word → ASR → Subconscious → optional Hermes → TTS through an IDLE → LISTENING → PROCESSING → RESPONDING → FOLLOW_UP_LISTEN state machine.
3. Six local services (LLM :8000, ASR :8002, TTS :8003, Hermes shim :8004, MCP tools :8005, main daemon) plus a 6-panel `jarvis-tui` dashboard carry the pipeline, with only Tavily web search leaving the host.
4. The repo guards this with `.gitignore` rules keeping secrets, voice/model artefacts, logs, and runtime state out of git.
5. `config.py` centralises every path, port, audio, wake-word, VAD, timing, and dual-brain setting behind env vars, from mic gain and wake thresholds to Hermes timeouts and the Chinese Subconscious prompt.
6. `requirements.txt` pins the matching ASR/TTS/wake/VAD/audio/HTTP stack so the whole voice loop reproduces on one Linux box.
