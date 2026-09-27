---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: CarverXx/jarvis-v3

### Q1. What is the dual-brain architecture in JARVIS v3, and why is cognition split in two?

> [!tip]- Answer
> The Subconscious is a fast conversational layer (SGLang-served Qwen3.6, TTFB under 1 s, one-to-two-sentence replies) that handles chit-chat and persona, while Hermes is a slower executor agent (5–30 s) that runs multi-step tool loops with retries and summarisation. The split exists because a single LLM cannot be both fast enough to speak naturally and smart enough to use tools reliably. See [[wiki/01-overview|Overview]].

### Q2. How does the Subconscious decide when to escalate a turn to Hermes, and what do the two worked examples show?

> [!tip]- Answer
> The Subconscious uses OpenAI-style tool-calling: when a turn needs real work it returns an `invoke_hermes(task=...)` call instead of a direct reply. A weather question triggers escalation with a heartbeat tone, a `web.search`, and a two-sentence spoken summary, while a greeting like "你好" is answered directly in about 300 ms with no tool call. Wiki-grounded QA follows the same pattern via Hermes `rag.search` plus `fs.read`, rephrased by the Subconscious. See [[wiki/01-overview|Overview]].

### Q3. What is the end-to-end voice pipeline, the state machine, and the service layout that carries it?

> [!tip]- Answer
> Audio flows microphone → openWakeWord ("Hey Jarvis") plus Silero VAD → Qwen3-ASR (:8002) → Subconscious (:8000) → optional Hermes CLI via MCP tools (:8005) → VoxCPM2 TTS (:8003) → speaker, moving through IDLE → LISTENING → PROCESSING → RESPONDING → FOLLOW_UP_LISTEN. Five to six systemd services on one Linux box host the LLM, ASR/TTS shims, Hermes shim, MCP tool server, and the main daemon. See [[wiki/01-overview|Overview]].

### Q4. How does the `jarvis-tui` dashboard expose the pipeline, and what stays local versus leaving the host?

> [!tip]- Answer
> `jarvis-tui` tails the daemon's JSONL event stream and renders a six-panel live view covering state transitions, mic/wake levels, ASR transcripts, Subconscious tokens and tool calls, Hermes progress, and TTS output. Everything runs on the host — LLM, ASR, and zero-shot TTS — with only explicit Tavily `web.search` leaving the machine. Echo safety comes from hard-muting the mic during TTS, flushing the input queue on transitions, and a wake cooldown after IDLE. See [[wiki/01-overview|Overview]].

### Q5. What does `.gitignore` keep out of git, and what pre-push check does it prescribe?

> [!tip]- Answer
> It blocks secrets and credentials (`*.key`, `*.token`, `*.pem`, `*.p12`, `.env*`, `secrets/`, `config/*.secret.*`), large or user-specific audio and model artefacts (`assets/*.wav|mp3|flac|m4a|pkl`, wake samples, `scripts/*.wav`), and logs plus runtime state (`logs/`, `events.jsonl`, caches, `user_persona.py|yaml`). The header comment tells contributors to run `scripts/audit_no_secrets.py` before pushing, since `git diff --cached` would still reveal a mistakenly staged key. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. How does `config.py` centralise configuration, and what voice-pipeline tuning does it hard-code?

> [!tip]- Answer
> `config.py` is the single env-overridable configuration imported by every service, covering model paths, the four service ports/URLs, audio device hints, and the dual-brain runtime (Hermes timeout and reply cap, SGLang backend, history depth, prompts). It hard-codes the audio front-end and turn-taking: 32 ms mic chunks, input gain 2.5 with soft-clip, wake threshold 0.7, VAD gates 0.5 and 0.7, and timeouts such as the 10 s listen cap, 0.5 s end-of-speech silence, and 15 s follow-up window. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. What Python stack does `requirements.txt` pin, and why is `openwakeword` held at 0.4.0?

> [!tip]- Answer
> It pins the full voice-loop stack: `qwen-asr` and `voxcpm` for ASR/TTS, `openwakeword` plus `onnxruntime` and `silero-vad` for wake and speech detection, `sounddevice`/`soundfile`/`numpy`/`scipy` for audio I/O, and `fastapi`/`uvicorn`/`httpx`/`python-multipart`/`pydantic` for the HTTP shims. `openwakeword==0.4.0` is pinned because that version depends only on `onnxruntime`, while 0.6+ requires `tflite-runtime`, which has no wheel on Linux with Python 3.12. See [[wiki/02-top-level-files|Top-Level Files]].

### Q8. A privacy-conscious hobbyist with one ~50 GB-VRAM Linux box asks whether to adopt the JARVIS v3 dual-brain, local-first pattern for a home voice assistant — what should you recommend?

> [!tip]- Answer
> Recommend adopting it: the hardware matches the documented minimum for running the LLM, ASR, and TTS simultaneously, and the local-first design keeps all voice and inference on the host except explicit web search. Advise them to budget effort for the voice-personalisation steps (reference clip, wake-verifier training) and the systemd multi-service setup rather than expecting a one-command install. Suggest the smaller-model fallback only if they move to a weaker GPU, accepting reduced Chinese tool-calling quality. See [[wiki/01-overview|Overview]].
