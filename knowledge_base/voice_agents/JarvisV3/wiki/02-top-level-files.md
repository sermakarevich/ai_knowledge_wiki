> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
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
---
## .gitignore — what stays out of git
Verbatim header and secrets rule (`.gitignore:1-22`):
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
Audio/model-asset rules (`.gitignore:30-40`):
```
assets/*.wav
assets/*.mp3
assets/*.flac
assets/*.m4a
assets/*.pkl        # openWakeWord custom verifier (user-specific voiceprint)
assets/*.wav.bak*   # trim/test backups
assets/*.bak*
assets/wake_samples/
scripts/*.wav
```
Logs, Python, editors, vendor, and personalization rules (`.gitignore:45-48`, `.gitignore:53-79`, `.gitignore:85-95`, `.gitignore:100-109`):
```
logs/
*.log
events.jsonl
jarvis-v3-logs/
__pycache__/ / *.py[cod] / build/ / dist/ / *.egg-info/ / ...
venv/ / env/ / .venv/ / .env.venv
.vscode/ / .idea/ / *.swp / *~ / .DS_Store / Thumbs.db
vendor/
*.pid / .pytest_cache/ / .mypy_cache/ / .ruff_cache/ / .coverage / htmlcov/
user_persona.py
user_persona.yaml
```
## config.py — centralized env-driven configuration
Module docstring states the contract verbatim (`config.py:1-6`):
```
"""JARVIS v3 — centralized configuration (env-driven). All services (shims + daemon) import values from here. Runtime overrides via environment variables (pattern copied from jarvis-v2 config.py)."""
```
Paths (`config.py:15-35`):
| Setting | Default | Env override |
|---|---|---|
| `MODELS_DIR` | `~/models` | `JARVIS_MODELS_DIR` |
| `QWEN3_ASR_MODEL_PATH` | `MODELS_DIR / "Qwen3-ASR-1.7B"` | `QWEN3_ASR_MODEL_PATH` |
| `VOXCPM_MODEL_PATH` | `MODELS_DIR / "VoxCPM2"` | `VOXCPM_MODEL_PATH` |
| `HERMES_BIN` | `~/.local/bin/hermes` | `HERMES_BIN` |
| `ASSETS_DIR` | `~/jarvis-v3-repo/assets` | `JARVIS_ASSETS_DIR` |
| `AWAKE_WAV` / `ERROR_WAV` | `ASSETS_DIR / "awake.wav"` / `"error.wav"` | derived, no env |
Service ports and URLs (`config.py:38-54`):
| Setting | Default |
|---|---|
| `VLLM_PORT` | `8000` |
| `QWEN3_ASR_SHIM_PORT` / `QWEN3_ASR_URL` | `8002` / `http://127.0.0.1:8002` |
| `VOXCPM_PORT` / `VOXCPM_URL` | `8003` / `http://127.0.0.1:8003` |
| `HERMES_SHIM_PORT` / `HERMES_SHIM_URL` | `8004` / `http://127.0.0.1:8004` |
| Each port/URL | overridable via same-name env var, e.g. `VLLM_PORT`, `QWEN3_ASR_URL` |
Audio front-end (`config.py:57-75`): name-substring (not index) device hints `MIC_DEVICE_HINT="Poly Sync"` and `SPEAKER_DEVICE_HINT="Poly Sync"` (`config.py:59-60`); `MIC_SAMPLE_RATE=16000`, `TTS_SAMPLE_RATE=48000`, `MIC_CHUNK_MS=32` = 512 samples @ 16 kHz = Silero VAD frame size (`config.py:62-66`); `MIC_INPUT_GAIN=2.5` (~+8 dB, moves Poly Sync 10 speech from ~-35 dBFS into openWakeWord's -25 to -15 dBFS comfort zone, with soft-clip protection) (`config.py:68-75`).
Wake word and VAD (`config.py:78-91`): `WAKE_WORD_MODEL="hey_jarvis_v0.1"` on onnxruntime without `tflite-runtime` (`config.py:80`); `WAKE_THRESHOLD=0.7` (conservative per openWakeWord docs; v2's `0.40` produced noise triggers) (`config.py:84`); `VAD_WAKE_THRESHOLD=0.5` gates openWakeWord to speech-containing audio (`config.py:88`); `VAD_FOLLOWUP_THRESHOLD=0.7` is stricter for follow-up listen (`config.py:91`).
Turn-taking timings in seconds unless noted (`config.py:95-114`):
| Setting | Default | Notes from comments |
|---|---|---|
| `LISTEN_HARD_TIMEOUT_S` | `10.0` | WAKE → first speech give-up time |
| `EOS_SILENCE_S` | `0.5` | VAD silence closing LISTEN window |
| `MIN_UTTERANCE_S` | `0.3` | shorter = drop as accidental noise |
| `FOLLOWUP_WINDOW_S` | `15.0` | re-speak without wake word |
| `POST_TTS_GRACE_MS` | `800` | bumped 500→800 on 2026-04-19 after TTS-echo "在 spam" wake retrigger; pairs with IDLE `mic_q` drain + 1.5 s wake cooldown |
Hermes, session, and dual-brain settings (`config.py:117-148`): `HERMES_TIMEOUT_S=120` (web search / multi-step tasks take 40–90 s), `HERMES_MAX_REPLY_CHARS=500` (`config.py:121-122`); `SESSION_ID_ENV` from `JARVIS_SESSION_ID`, reused across restarts if set else regenerated per daemon restart as `X-Session-Id` for the Hermes shim `--resume` mapping (`config.py:129-130`); `SGLANG_URL="http://127.0.0.1:8000"`, `SGLANG_MODEL="Qwen/Qwen3.6-35B-FP8"`, `SGLANG_API_KEY=""` (set via systemd env), `SUBCONSCIOUS_HISTORY_N=6` user+assistant turns (`config.py:135-144`); `WAITING_BEEP_INTERVAL_S=2.0` heartbeat loop with `WAITING_BEEP_WAV=assets/waiting_beep.wav` (`config.py:146-148`).
Wake-confirm and voice-clone sounds (`config.py:150-165`): hierarchy is `awake_tone.wav` (C6+E6 chime, preferred 2026-04-19, replaces spoken "在") → `voxcpm_zai.wav` → `awake.wav` (`config.py:150-156`); `VOXCPM_REFERENCE_WAV` defaults to `assets/jarvis_voice_ref.wav` (Paul Bettany Iron Man JARVIS from user's YouTube download), empty/missing = voice-design random voice each turn (`config.py:161-165`).
Subconscious system prompt (`config.py:167-228`): kept short and in Chinese to match user style and minimise prefix tokens; persona is 贾维斯, never leak `Hermes` / 潜意识 / 子系统 / 大模型; hard rules are simplified Chinese only, 1–2 sentences, name always 贾维斯 (never `JARVIS`, else TTS spells letters), no architecture self-explanation, no fabricated realtime info; self-answers chit-chat/greetings/arithmetic/common sense; must call `invoke_hermes` for date/time/weekday, knowledge-base/vault/wiki notes, realtime weather/news/prices, Cloudflare, service status, and >3 s deep tasks; unsupported (refuse in one sentence, no tool call) are calendar/mail/iMessage/WeChat/smart-home/music/calls/video-meetings/booking; tool results are trusted facts to restate in 1–2 sentences; only `(主意识处理失败`, `(主意识无回应`, `(工具执行失败` prefixes count as tool failure. Logging is `LOG_LEVEL="INFO"` (`config.py:232`).
## requirements.txt — pinned Python stack
Verbatim with pin rationale (`requirements.txt:1-22`):
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
**Covers:** `.gitignore`, `config.py`, `requirements.txt`
