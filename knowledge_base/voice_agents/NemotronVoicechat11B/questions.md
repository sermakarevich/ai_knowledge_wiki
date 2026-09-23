---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Nikki1404/nemotron_voicechat_11B

### Q1. What two API styles does the repo expose, and what endpoints does each include?
> [!tip]- Answer
> The repo exposes a native WebSocket speech-to-speech API (`WS /ws/speech_to_speech/` plus `GET /ws/speech_to_speech/health`) and an OpenAI-compatible HTTP namespace (`GET /openai-compatible/v1/models` and `POST /openai-compatible/v1/audio/speech-to-speech`), alongside a top-level `GET /health`. The dual style lets streaming clients use WebSockets while OpenAI-tooled clients use plain HTTP. See [[wiki/01-overview|Overview]].

### Q2. How do microphone mode and file mode differ, and what do they have in common?
> [!tip]- Answer
> Both modes are fully speech-to-speech and converge on the same output: response audio saved as WAV and optionally played through speakers. They differ only in the input source — live microphone capture (PCM16 mono 24 kHz chunks sent over WebSocket) versus an uploaded audio file such as `sample.wav`. See [[wiki/01-overview|Overview]].

### Q3. Why is the included client turn-based rather than full-duplex, and what would duplex require?
> [!tip]- Answer
> The client is push-to-talk: it records a fixed window (e.g. `--seconds 5`), sends the chunks, commits the utterance, then waits for the spoken reply in a `YOU SPEAK -> STOP -> MODEL RESPONDS WITH AUDIO` cycle. It is not continuous duplex, so both sides cannot speak at once; duplex would need continuous mic capture, VAD/end-of-turn detection, and interruption plus barge-in handling. See [[wiki/01-overview|Overview]].

### Q4. What are the server's key configuration defaults and its startup validation steps?
> [!tip]- Answer
> `server.py` defaults to `MODEL_ID=nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` at `MODEL_PATH=/app/models/NVIDIA-NemotronLabs-VoiceChat-11B` on `DEVICE=cuda`, with `CLIENT_SAMPLE_RATE=24000`, `OUTPUT_CHUNK_MS=80`, `MAX_CONCURRENT=1`, and `MIN_GPU_VRAM_GB=40`. At startup it requires CUDA when configured, enforces the VRAM minimum, checks the model path exists, builds the model via `build_model`, and records `model_load_ms`. See [[wiki/02-top-level-files|Top-level-files]].

### Q5. How does the server run blocking Nemotron inference without stalling the async event loop?
> [!tip]- Answer
> The blocking pipeline (`load_wav_16k_mono`, `encode_system_prompt`, `run_offline_inference`) runs in `_infer_sync` inside `asyncio.to_thread`, guarded by an `asyncio.Semaphore(MAX_CONCURRENT)` so only one inference runs at a time. It raises `RuntimeError` when no audio is returned and reports prep/inference timings plus input/output durations. Output tensors are resampled to 24 kHz PCM16 via `tensor_audio_to_pcm16_24k`. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What event protocol does the client use in WebSocket mode, and how does REST mode differ?
> [!tip]- Answer
> WebSocket mode sends `session.update` (PCM 24 kHz in/out, instructions), chunked `input_audio_buffer.append` events with base64 audio, then `input_audio_buffer.commit`, and consumes `response.output_audio.delta`, `response.output_audio_transcript.done`, and `response.done`/`error`. REST mode instead wraps normalized PCM as WAV and POSTs it to `/openai-compatible/v1/audio/speech-to-speech` with `instructions` and `response_format=wav`, reporting `X-Prep-Ms`/`X-Inference-Ms`-style timing headers. Both modes normalize input via `load_audio_pcm16_24k` (mono-mix, resample, clip, int16). See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Should you deploy this repo as-is for a low-VRAM demo that needs true simultaneous barge-in, and what would you change?
> [!tip]- Answer
> No, I would not deploy it as-is: the server enforces a 40 GB VRAM minimum with single-concurrency inference, so a low-VRAM box fails startup, and the client is turn-based push-to-talk with no interruption support. For the demo I would keep the dual API but add continuous capture with VAD/end-of-turn plus server-side barge-in, and either provision a 40 GB+ GPU or rework the single-model path for smaller hardware. See [[wiki/01-overview|Overview]].
