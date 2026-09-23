# Technical Analysis: Nikki1404/nemotron_voicechat_11B

**Repository:** https://github.com/Nikki1404/nemotron_voicechat_11B
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Cascaded voice assistants chain separate ASR, LLM, and TTS stages, which increases integration surface and end-to-end latency. The underlying checkpoint (`nvidia/NVIDIA-NemotronLabs-VoiceChat-11B`) addresses this by performing streaming speech understanding and generation in a single 11B end-to-end model, but a raw checkpoint is not network-callable.

This repo addresses the deployment gap, not model research: it is a Dockerized FastAPI wrapper that hosts the checkpoint on a GPU server and exposes two API styles — a native WebSocket speech-to-speech endpoint and an OpenAI-compatible HTTP namespace (01-overview.md:3, 01-overview.md:5). Both file mode and microphone mode funnel through the same speech-to-speech core over a PCM16 mono 24 kHz boundary, with server-side resampling to the model input rate (01-overview.md:7, 01-overview.md:11). The bundled client is turn-based push-to-talk (`YOU SPEAK -> STOP -> MODEL RESPONDS WITH AUDIO`), not continuous duplex (01-overview.md:9). The primary user is an application developer who needs a self-hosted speech-in/speech-out endpoint for demos or integration work.

## 2. High-Level Architecture

```text
microphone / sample.wav
  │ PCM16 mono 24 kHz (client.py:20-46)
  ▼
client.py (ws chunks | wav POST)
  │ WebSocket audio chunks / HTTP multipart
  ▼
FastAPI server.py (:40-69 config, :330-483 startup)
  │ resample to model input rate, semaphore(MAX_CONCURRENT=1)
  ▼
NeMo offline_voicechat (build_model / run_offline_inference via asyncio.to_thread)
  │ speech response tensor + transcript
  ▼
server.py (tensor -> PCM16 24 kHz / WAV bytes)
  │
  ├─► WS events (response.output_audio.delta / response.done)
  └─► HTTP WAV body + X-*-Ms headers
  ▼
client.py (save response.wav, optional --play)
```

Data-flow narrative:

1. **Capture/normalize (client-side).** File input is decoded and normalized to mono PCM16 24 kHz by `load_audio_pcm16_24k` (client.py:33); mic input is recorded at the same rate by `record_mic` (client.py:49). This fixes a single audio boundary for both transports.
2. **Transport.** WebSocket mode opens `/ws/speech_to_speech/` and streams base64 PCM chunks; REST mode wraps PCM as WAV and POSTs to `/openai-compatible/v1/audio/speech-to-speech` (02-top-level-files.md:73-110).
3. **Admission and model call (server-side).** Requests pass through an `asyncio.Semaphore(MAX_CONCURRENT)` (server.py:229-322) and blocking NeMo inference runs in `asyncio.to_thread`, so the event loop is not blocked while GPU inference runs.
4. **Inference.** `_infer_sync` (server.py:229) loads the utterance WAV, encodes the system prompt, and calls `run_offline_inference`, timing prep vs. inference separately and raising when no audio is returned.
5. **Return.** The server resamples the output tensor to PCM16 24 kHz for WebSocket deltas or WAV bytes for HTTP, and the client saves `response.wav` / `mic_response.wav` and optionally plays it (01-overview.md:57-64, 02-top-level-files.md:103-110).

Persistent state lives in three places: the loaded NeMo model held in the server process (`model`, server.py:154), the model checkpoint directory (`MODEL_PATH`, default `/app/models/NVIDIA-NemotronLabs-VoiceChat-11B`, server.py:40-53), and temp WAV files created per request (`tempfile.mkstemp`, server.py:112, server.py:146-159). There is no database or cross-request session store described in the wiki pages.

## 3. The Speech-to-Speech Session

The central concept is a **speech-to-speech session**: one committed spoken utterance maps to one spoken response plus transcript, carried either as a WebSocket event sequence or as a single HTTP request/response.

Representation: on the wire the session is a JSON event stream (WebSocket) or a multipart form + WAV body (HTTP). Audio payload is base64 PCM16 mono 24 kHz inside events, or a WAV file over HTTP. Server-side the session materializes as a temp WAV file (`pcm16_bytes_to_wav_file`, server.py:112; `upload_to_temp_file`, server.py:146-159) plus in-memory output PCM accumulation on the client.

Named kinds/types with file:line:

- `session.update` — negotiates audio formats and instructions (client.py:101-115).
- `input_audio_buffer.append` — one base64 PCM chunk upload (client.py:117-135).
- `input_audio_buffer.commit` — ends the turn, triggers inference (client.py:117-135).
- `response.output_audio.delta` — one base64 PCM response chunk (client.py:142-156).
- `response.output_audio_transcript.done` — final transcript string (client.py:142-156).
- `response.done` — terminal event carrying `metrics` dict (client.py:142-156).
- `error` — terminal failure, client raises `RuntimeError` (client.py:142-156).
- `session.close` — client-sent teardown after `response.done` (02-top-level-files.md:103).

Key query (session setup, verbatim, client.py:101-115):

```python
event(
    "session.update",
    session={
        "audio": {
            "input": {"format": {"type": "audio/pcm", "rate": CLIENT_SR}},
            "output": {"format": {"type": "audio/pcm", "rate": CLIENT_SR}},
        },
        "instructions": args.instructions,
        "tools": [],
    },
)
```

## 4. LLM / External Service Integration

The serving path calls no external LLM or third-party API. The "LLM" is the local checkpoint `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` (server.py:40-53), loaded via NeMo `build_model` from `MODEL_PATH` at startup (server.py:330-483) and invoked via `encode_system_prompt` / `run_offline_inference` from `nemo.collections.speechlm2.inference.utils.offline_voicechat` (server.py:26-33, server.py:229). All inference calls are required (every turn runs them); there are no optional model calls in the serving path.

Environment variables controlling model/inference (server.py:40-69): `MODEL_ID` (default `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B`), `MODEL_PATH` (default `/app/models/NVIDIA-NemotronLabs-VoiceChat-11B`), `DEVICE` (default `cuda`), `OUTPUT_CHUNK_MS` (default `80`), `MAX_CONCURRENT` (default `1`), `MIN_GPU_VRAM_GB` (default `40`).

One non-serving external call exists in the scratch probe `update.py:4`, which POSTs to `https://qwen3-tts-150916788856.us-central1.run.app/v1/audio/speech` (update.py:6-23) for a Qwen3-TTS latency comparison. It is not part of the server or client pipelines.

## 5. The Turn-Based Inference Pipeline

Primary workflow: fixed-length utterance in, spoken response out, over either transport.

1. **Acquire audio — `load_audio_pcm16_24k` (client.py:33) / `record_mic` (client.py:49).** `--file` path is decoded with `sf.read(dtype="float32")`, mixed to mono, linear-interpolation resampled to 24 kHz, clipped and scaled to int16 bytes; `--mic` path records `seconds` (default 5.0) via `sounddevice` at `CLIENT_SR=24000` (client.py:20-22).
2. **Open session — `run_ws` (client.py:77).** Connects with `max_size=None, ping_interval=20, ping_timeout=60`, reads `session.id` from the first event, sends `session.update` with input/output PCM format and `args.instructions`.
3. **Stream and commit — chunk loop inside `run_ws` (client.py:117-135).** PCM is sliced into `chunk_bytes = CLIENT_SR * 2 * chunk_ms / 1000` pieces, each sent as `input_audio_buffer.append` (base64), optionally paced by `--realtime-send`, then finalized with `input_audio_buffer.commit`.
4. **Server-side ingest — `pcm16_bytes_to_wav_file` (server.py:112) / `upload_to_temp_file` (server.py:146-159).** Odd trailing bytes are trimmed, int16 is converted to float32, and the utterance is written to a temp `.wav` for the NeMo loader.
5. **Inference — `_infer_sync` (server.py:229) via `infer` (server.py:313).** `load_wav_16k_mono` → `encode_system_prompt` (timed as `prep_ms`) → `run_offline_inference` (timed as `inference_ms`); raises `RuntimeError("Nemotron VoiceChat returned no audio.")` on empty result; returns text, audio tensor, lengths, and durations. `infer` serializes through `inference_lock` and `asyncio.to_thread`.
6. **Convert output — `tensor_audio_to_pcm16_24k` (server.py:161) / `tensor_audio_to_wav_bytes` (server.py:199).** Output tensor is sliced to `audio_len`, resampled from `MODEL_OUTPUT_SR` to 24 kHz when different, clamped and scaled to int16 (WS) or written as WAV bytes (HTTP).
7. **Consume — receive loop inside `run_ws` (client.py:142-156) / `run_rest` (client.py:209).** WS accumulates `response.output_audio.delta` chunks (first chunk marks TTFA), captures transcript on `response.output_audio_transcript.done`, breaks on `response.done`; REST POSTs `files={"file": ("input.wav", wav_bytes, "audio/wav")}` with `instructions`/`response_format` (client.py:217-224) and saves `resp.content`.
8. **Persist/report — tail of `run_ws` / `run_rest` (client.py:103-110 per wiki).** Saves WAV via `save_pcm16_wav` (client.py:62), optionally plays via `play_pcm16` (client.py:71), and prints client latencies plus server metrics/headers (`X-Model-Load-Ms`, `X-Prep-Ms`, `X-Inference-Ms`, `X-Total-Ms`, durations, transcript).
9. **Dispatch — `main` (client.py:297-307) / `parse_args` (client.py:256).** Selects file vs. mic source and `ws` vs. `rest` mode; argument defaults are documented in section 8.

Startup/serve functions: `startup_event` (server.py:330) validates CUDA, VRAM, and `MODEL_PATH`, builds the model, and records `model_load_ms`; route handlers `GET /` (server.py:535) and `GET /health` (server.py:~560-597) report readiness. Endpoints after `health` were truncated in the analyzed chunks and are not covered here (02-top-level-files.md:172).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `server.py` | server.py:26-483+ | FastAPI app: config, NeMo inference helpers, startup validation, health/root routes, WS + OpenAI-compatible endpoints (tail past health truncated in chunks) |
| `client.py` | client.py:20-307 | Dual-mode client: audio helpers, WS turn protocol, REST POST, CLI dispatch, latency reporting |
| `requirements.txt` | requirements.txt:1-22 | Pinned server/model deps (transformers, torchcodec, FastAPI stack) plus unpinned CUDA-build helpers |
| `client-requirements.txt` | client-requirements.txt:1-5 | Unpinned lightweight client deps (numpy, requests, soundfile, sounddevice, websockets) |
| `README.md` | README.md:9-221 | Endpoint map, mic/file flows, push-to-talk semantics, Docker build/run, client and curl tests, audio format |
| `Dockerfile` | build refs README.md:122-145 | Builds `nemotron-voicechat:latest` from CUDA 12.4.1 runtime + Python 3.12 + server requirements |
| `.dockerignore` | .dockerignore:1-5 | Excludes `.git`, `__pycache__`, `*.pyc`, `*.wav`, `outputs/` from the image |
| `update.py` | update.py:4-167 | Scratch Qwen3-TTS latency probe plus appended curl/LiveKit/Dia notes; not part of serving |
| `sample.wav` (artifact) | README.md:147-210 refs | Example file-mode input used in WS, REST, and curl tests |
| `response.wav` / `mic_response.wav` (artifacts) | README.md:32-80 refs | Default client output paths for file and mic turns |

## 7. Dependencies

Required (server) — exact constraint strings from requirements.txt:1-22:

| Package | Version constraint | Purpose |
|---|---|---|
| transformers | `==4.56.0` | HF model/tokenizer stack for the checkpoint |
| tokenizers | `==0.22.0` | Tokenization backend pinned with transformers |
| lhotse | `==1.32.2` | Speech data/cut utilities used by NeMo audio path |
| huggingface-hub | `==0.34.4` | Checkpoint download/access for `MODEL_ID` |
| hf-xet | `==1.1.9` | Fast checkpoint transfer backend |
| torchcodec | `==0.10.0` | Audio codec/decoding support |
| torch_audiomentations | (unpinned) | Audio augmentation utilities |
| jinja2 | (unpinned) | Prompt/chat-template rendering |
| ninja | (unpinned) | Native extension build backend (`--no-build-isolation`) |
| packaging | (unpinned) | Build/packaging helper |
| wheel | (unpinned) | Build/packaging helper |
| einops | (unpinned) | Tensor rearrangement ops |
| fastapi | (unpinned) | HTTP/WebSocket server framework |
| uvicorn[standard] | (unpinned) | ASGI server |
| python-multipart | (unpinned) | Multipart form parsing for file upload endpoint |
| numpy | (unpinned) | PCM/tensor numeric conversions |
| soundfile | (unpinned) | WAV read/write |
| websockets | (unpinned) | WS client transport |
| requests | (unpinned) | HTTP client (REST mode, update probe) |

Required (client) — `client-requirements.txt:1-5`, all unpinned: `numpy` (PCM math), `requests` (REST POST), `soundfile` (file decode), `sounddevice` (mic record + playback), `websockets` (WS mode).

## 8. CLI / Usage Surface

Entry points: `server.py` (GPU Docker service; `HOST=0.0.0.0`, `PORT=8001` per server.py:40-53, mapped to host 8000 in the documented `docker run`); `client.py` (local CLI); `update.py` (scratch probe, not a product entry point).

Endpoints (README.md:16-24; server.py:535+):

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Service info: service name, model, status, WS and OpenAI-compatible paths |
| GET | `/health` | Readiness: status, model, device, `model_load_ms`, CUDA/VRAM stats |
| GET | `/ws/speech_to_speech/health` | WebSocket sub-system health |
| WS | `/ws/speech_to_speech/` | Native speech-to-speech turn protocol |
| GET | `/openai-compatible/v1/models` | Model list (OpenAI-style) |
| POST | `/openai-compatible/v1/audio/speech-to-speech` | File-based speech-to-speech (`file`, `instructions`, `response_format`) |

Client commands (README.md:87-210; client.py:256-307):

```bash
python client.py --mode ws --server ws://localhost:8000/ws/speech_to_speech/ --file sample.wav --output response.wav --play
python client.py --mode ws --server ws://localhost:8000/ws/speech_to_speech/ --mic --seconds 5 --output mic_response.wav --play
python client.py --mode rest --http-server http://localhost:8000 --file sample.wav --output response.wav --play
curl -X POST http://localhost:8000/openai-compatible/v1/audio/speech-to-speech -F "file=@sample.wav" -F "instructions=..." -F "response_format=wav" --output response.wav
docker build -t nemotron-voicechat:latest . && docker run --rm -it --gpus all --ipc=host --shm-size=8g -p 8000:8000 nemotron-voicechat:latest
```

Client flags (`parse_args`, client.py:256):

| Flag | Default / choices |
|---|---|
| `--mode` | `ws` (choices `ws`, `rest`) |
| `--server` | `ws://localhost:8000/ws/speech_to_speech/` |
| `--http-server` | `None` (e.g. `http://localhost:8000`) |
| `--file` / `--mic` | Mutually exclusive, one required |
| `--seconds` | `5.0` |
| `--output` | `nemotron_response.wav` |
| `--instructions` | `You are a helpful AI voice assistant. Answer naturally and concisely in spoken English.` |
| `--chunk-ms` | `80` |
| `--realtime-send` | `store_true` (pace chunk upload) |
| `--play` | `store_true` (speaker playback) |
| `--timeout` | `600.0` |

Server env vars (server.py:40-69):

| Var | Default | Effect |
|---|---|---|
| `MODEL_ID` | `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` | Advertised model identity |
| `MODEL_PATH` | `/app/models/NVIDIA-NemotronLabs-VoiceChat-11B` | Local checkpoint dir; startup fails if missing |
| `DEVICE` | `cuda` | Inference device; `cuda*` requires `torch.cuda.is_available()` |
| `OUTPUT_CHUNK_MS` | `80` | Response streaming chunk size |
| `MAX_CONCURRENT` | `1` | Inference semaphore width |
| `MIN_GPU_VRAM_GB` | `40` | Startup gate; below this the server refuses to start |

## 9. Extensibility Points

- **New endpoint or transport:** extend `server.py` (FastAPI app, server.py:72-92); add routes beside `GET /` (server.py:535) and `GET /health` (server.py:~560-597). The post-health handler source was truncated in the chunks, so read the live file before editing WS/REST handlers.
- **Prompt/behavior control:** change `DEFAULT_SYSTEM_PROMPT` (server.py:72-92) or pass per-turn `instructions` via `session.update` (client.py:101-115) / REST `data={"instructions": ...}` (client.py:217-224); no prompt-template framework is present.
- **Concurrency/throughput:** raise `MAX_CONCURRENT` (server.py:56-69) and replace the single `inference_lock` (server.py:154) with queueing/batching; currently one request holds the GPU.
- **Audio I/O:** modify `load_audio_pcm16_24k` / `record_mic` / `save_pcm16_wav` / `play_pcm16` (client.py:33-71) for new sample rates, channels, or VAD-gated capture; server converters `tensor_audio_to_pcm16_24k` (server.py:161) and `tensor_audio_to_wav_bytes` (server.py:199) are the matching server-side seams.
- **Duplex operation:** extend `run_ws` (client.py:77) with continuous capture, VAD/end-of-turn, and interruption/barge-in; the current commit-then-respond contract has no such logic (README.md:113-120).
- **Client transports:** extend `run_rest` (client.py:209) or `ws_to_http` (client.py:192) for auth headers, retries, or new response formats.

## 10. Limitations and Gotchas

- **Single-flight GPU inference.** `MAX_CONCURRENT=1` (server.py:56-69) plus one `asyncio.Semaphore` means a second concurrent turn waits or times out; the service is a demo/single-user deployment, not a multi-tenant server.
- **40 GB VRAM gate.** Startup raises unless the GPU reports at least `MIN_GPU_VRAM_GB=40` (server.py:330-483), so consumer-grade GPUs cannot run the documented container without lowering the gate (and then risking OOM in `build_model`).
- **Push-to-talk only, despite the full-duplex model.** The client records a fixed `--seconds` window, commits, then waits; there is no VAD, end-of-turn detection, interruption, or barge-in (README.md:107-120). Latency figures labeled `COMMIT -> TTFA` measure turn latency, not conversational overlap.
- **Port and rate mismatches bite.** `PORT=8001` is hardcoded in `server.py:40-53` while docs use 8000 (container mapping resolves it, bare-metal runs do not); the wire rate is fixed at PCM16 mono 24 kHz (client.py:20-22, README.md:212-221) and any deviation depends on linear-interpolation resampling in `load_audio_pcm16_24k` (client.py:33) and server-side conversion.
- **Truncated source coverage.** Wiki analysis of `server.py` stops after `health` (~server.py:597; 18499 chars cut), so WS handler, OpenAI-compatible POST handler, and error paths are unverified from wiki alone — read `server.py` directly before modifying serving logic (02-top-level-files.md:12, 02-top-level-files.md:172).

## 11. How It Compares to Alternatives

- **NVIDIA NeMo / SpeechLM2 sample serving:** NVIDIA's own NeMo inference scripts expose the same `offline_voicechat` utilities (`build_model`, `run_offline_inference`) without a product API; this repo adds FastAPI routes, Docker packaging, and a demo client at the cost of hardcoding a single-model, single-concurrency server.
- **OpenAI Realtime API (`gpt-4o-realtime` WebSocket):** a hosted full-duplex speech API with session events, VAD, and interruption handling; this repo mirrors the event naming (`session.update`, `input_audio_buffer.append/commit`, `response.done`) but is self-hosted, turn-based, and carries the full 40 GB GPU burden locally.
- **Kyutai Moshi:** an open-weights full-duplex speech model with a Rust/Python streaming server aimed at true overlap and barge-in; this repo wraps a different checkpoint family and currently demonstrates only push-to-talk, so Moshi-style duplex requires client/server rework here.
- **LiveKit Agents / Pipecat:** production voice-agent frameworks that compose STT, LLM, TTS, VAD, and telephony transports with multi-user session management; this repo is narrower — one end-to-end model, one GPU, no pipeline composition — and simpler to run for single-model evaluation.

Positioning: this repo is a single-model self-hosting shim for evaluating Nemotron VoiceChat 11B over the network, not a voice-agent platform; choose it for local checkpoint demos, and choose a hosted realtime API or an agent framework when duplex, scale, or pipeline flexibility matters.

## Appendix: Selected Code Snippets

Server config (server.py:40-69):

```python
MODEL_ID = os.getenv("MODEL_ID", "nvidia/NVIDIA-NemotronLabs-VoiceChat-11B")
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/NVIDIA-NemotronLabs-VoiceChat-11B")
DEVICE = os.getenv("DEVICE", "cuda")
HOST = "0.0.0.0"
PORT = 8001
CLIENT_SAMPLE_RATE = 24000
MODEL_INPUT_SR = SOURCE_SR
MODEL_OUTPUT_SR = TARGET_SR
OUTPUT_CHUNK_MS = int(os.getenv("OUTPUT_CHUNK_MS", "80"))
MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT", "1"))
MIN_GPU_VRAM_GB = float(os.getenv("MIN_GPU_VRAM_GB", "40"))
```

Client constants and chunk upload (client.py:20-22, client.py:117-135):

```python
CLIENT_SR = 24000
CHANNELS = 1
DTYPE = "int16"
```

```python
chunk_bytes = int(CLIENT_SR * 2 * args.chunk_ms / 1000)
# per chunk: event("input_audio_buffer.append", audio=base64...)
# optional: await asyncio.sleep(args.chunk_ms / 1000.0) when args.realtime_send
# then: event("input_audio_buffer.commit")
```

REST target (client.py:211, client.py:217-224):

```python
url = base.rstrip("/") + "/openai-compatible/v1/audio/speech-to-speech"
```

Endpoint map (README.md:16-24):

```text
GET   /health
GET   /ws/speech_to_speech/health

WS    /ws/speech_to_speech/

GET   /openai-compatible/v1/models
POST  /openai-compatible/v1/audio/speech-to-speech
```
