> [[index|Wiki]] | [[summary|Summary]]
# Nikki1404/nemotron_voicechat_11B — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** This repo wraps `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` as a standalone speech-to-speech app exposing a native WebSocket endpoint and an OpenAI-compatible HTTP namespace.
## Key points
- Wraps `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` behind two separated API styles: native WebSocket speech-to-speech and OpenAI-compatible HTTP (README.md:9-12).
- Exposes `GET /health`, `GET /ws/speech_to_speech/health`, `WS /ws/speech_to_speech/`, plus `GET /openai-compatible/v1/models` and `POST /openai-compatible/v1/audio/speech-to-speech` (README.md:16-24).
- Microphone mode is still speech-to-speech: mic PCM16 mono 24 kHz goes through `client.py` to `/ws/speech_to_speech/`, is resampled to model input rate, and response PCM chunks stream back for save/playback (README.md:28-58).
- File mode and mic mode differ only in input audio source; both produce response audio saved as WAV and optionally played (README.md:72-80).
- Included client is turn-based push-to-talk (`YOU SPEAK -> STOP -> MODEL RESPONDS WITH AUDIO`), not continuous duplex; duplex would need continuous capture, VAD/end-of-turn, interruption and barge-in logic (README.md:84-120).
- Dependency/build layout splits `requirements.txt` (Docker/server/model) from `client-requirements.txt` (lightweight local client), on `nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04` with Python 3.12 installed via `pip install --no-build-isolation -r requirements.txt` (README.md:122-128).
- Native WebSocket audio boundary is PCM16 mono 24 kHz in and out, with model-required conversion handled internally by the server (README.md:212-221).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** Top-level files implement a FastAPI Nemotron VoiceChat 11B speech-to-speech server plus a dual-mode (WebSocket/REST) Python client, with split server/client dependency files and a scratch `update.py` probe.
## Key points
- `server.py` configures model identity and paths via `MODEL_ID` (`nvidia/NVIDIA-NemotronLabs-VoiceChat-11B`) and `MODEL_PATH` (`/app/models/NVIDIA-NemotronLabs-VoiceChat-11B`), with `DEVICE=cuda`, `HOST=0.0.0.0`, `PORT=8001` (server.py:40-53).
- `server.py` exposes the API-facing rate `CLIENT_SAMPLE_RATE=24000` and maps internal rates via `MODEL_INPUT_SR=SOURCE_SR` / `MODEL_OUTPUT_SR=TARGET_SR`, with `OUTPUT_CHUNK_MS=80`, `MAX_CONCURRENT=1`, `MIN_GPU_VRAM_GB=40` (server.py:56-69).
- `server.py` runs blocking Nemotron inference (`load_wav_16k_mono`, `encode_system_prompt`, `run_offline_inference`) inside `asyncio.to_thread` behind an `asyncio.Semaphore(MAX_CONCURRENT)` (server.py:229-322).
- `server.py` startup validates CUDA visibility, enforces the VRAM minimum, checks `MODEL_PATH` exists, calls `build_model(MODEL_PATH, DEVICE)`, and records `model_load_ms` (server.py:330-483).
- `client.py` fixes `CLIENT_SR=24000`, `CHANNELS=1`, `DTYPE="int16"` and converts any input file to mono PCM16 24 kHz via `load_audio_pcm16_24k` with linear-interpolation resampling (client.py:20-46).
- `client.py` WebSocket mode sends `session.update`, chunked `input_audio_buffer.append`, and `input_audio_buffer.commit`, then consumes `response.output_audio.delta`, `response.output_audio_transcript.done`, `response.done` / `error` (client.py:101-156).
- `client.py` REST mode wraps PCM as WAV and posts to `/openai-compatible/v1/audio/speech-to-speech` with `instructions` and `response_format=wav`, reporting `X-Model-Load-Ms` / `X-Prep-Ms` / `X-Inference-Ms` style headers (client.py:209-248).
- Dependency layout splits a pinned server file (`requirements.txt:1-7`) from a 5-line client file (`client-requirements.txt:1-5`); `server.py` content after `health` (~server.py:597) was truncated in the chunk and is not covered here.

## The system in five moves
1. The repo frames NVIDIA's Nemotron VoiceChat 11B model as a deployable speech-to-speech service with two API styles: a native WebSocket endpoint and an OpenAI-compatible HTTP namespace.
2. The client normalizes every input — mic capture or audio file — to PCM16 mono 24 kHz and drives turn-based push-to-talk sessions via session setup, chunked append, and commit events.
3. The FastAPI server validates GPU/VRAM and model path at startup, then funnels blocking NeMo offline inference through a single-concurrency semaphore and background threads.
4. Inference resamples client audio to the model input rate, runs system-prompt encoding plus offline generation, and converts output tensors back to 24 kHz PCM16 for streaming deltas or WAV responses.
5. Both transports converge on the same artifact — response audio saved as WAV and optionally played — while reporting latency and timing headers, with continuous duplex explicitly out of scope.
