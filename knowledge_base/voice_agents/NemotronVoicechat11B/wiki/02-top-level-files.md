> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
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
---
## Dockerignore
Verbatim (`.dockerignore:1-5`):
```text
.git
__pycache__
*.pyc
*.wav
outputs/
```

## Dependencies
Server deps, verbatim (`requirements.txt:1-22`):
```text
transformers==4.56.0
tokenizers==0.22.0
lhotse==1.32.2
huggingface-hub==0.34.4
hf-xet==1.1.9
torchcodec==0.10.0
torch_audiomentations
jinja2

ninja
packaging
wheel
einops

fastapi
uvicorn[standard]
python-multipart

numpy
soundfile
websockets
requests
```
Client deps, verbatim (`client-requirements.txt:1-5`):
```text
numpy
requests
soundfile
sounddevice
websockets
```

## Client audio helpers
Constants, verbatim (`client.py:20-22`):
```python
CLIENT_SR = 24000
CHANNELS = 1
DTYPE = "int16"
```
- `load_audio_pcm16_24k(path: str) -> bytes` (`client.py:33`): `sf.read(..., dtype="float32")`, mono-mix via `mean(axis=1)`, linear-interpolation resample when `sr != CLIENT_SR`, clip to `[-1.0, 1.0]`, scale by `32767.0` to `<i2` bytes.
- `record_mic(seconds: float) -> bytes` (`client.py:49`): `sd.rec(int(seconds * CLIENT_SR), samplerate=CLIENT_SR, channels=CHANNELS, dtype=DTYPE)` then `sd.wait()`.
- `save_pcm16_wav(path, pcm_bytes, sample_rate=CLIENT_SR)` (`client.py:62`): mono, sampwidth 2, `wave`-written frames.
- `play_pcm16(pcm_bytes, sample_rate=CLIENT_SR)` (`client.py:71`): `sd.play` + `sd.wait()`.
- `pcm_to_wav_bytes(pcm_bytes, sample_rate=CLIENT_SR)` (`client.py:199`) and `ws_to_http(ws_url)` (`client.py:192`): `wss->https`, else `http` (used to derive REST base URL).

## Client WebSocket mode
`run_ws(args, pcm_bytes)` (`client.py:77`): connects with `max_size=None, ping_interval=20, ping_timeout=60`, reads `session.id` from first event, then session setup verbatim (`client.py:101-115`):
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
Chunked upload (`client.py:117-135`):
```python
chunk_bytes = int(CLIENT_SR * 2 * args.chunk_ms / 1000)
# per chunk: event("input_audio_buffer.append", audio=base64...)
# optional: await asyncio.sleep(args.chunk_ms / 1000.0) when args.realtime_send
# then: event("input_audio_buffer.commit")
```
Receive loop event types (`client.py:142-156):

| Event type | Action |
|---|---|
| `response.output_audio.delta` | `base64.b64decode(msg["delta"])`, extend output; first sets TTFA |
| `response.output_audio_transcript.done` | `transcript = msg.get("transcript", "")` |
| `response.done` | record time, `server_metrics = msg.get("metrics", {})`, break |
| `error` | `raise RuntimeError(...)` |

Then sends `session.close`, saves WAV via `save_pcm16_wav(args.output, ...)`, and prints CLIENT LATENCY (`Connection latency`, `Send audio`, `Connection -> event`, `COMMIT -> TTFA`, `COMMIT -> response`, `E2E TOTAL`) plus SERVER LATENCY metrics dict and RESULT transcript/audio path.

## Client REST mode
`run_rest(args, pcm_bytes)` (`client.py:209`): target verbatim (`client.py:211`):
```python
url = base.rstrip("/") + "/openai-compatible/v1/audio/speech-to-speech"
```
where `base = args.http_server or ws_to_http(args.server)`. Posts `files={"file": ("input.wav", wav_bytes, "audio/wav")}` with `data={"instructions": ..., "response_format": "wav"}` and `timeout=args.timeout` (`client.py:217-224`). Saves `resp.content` to `args.output` and reports `Request -> response`, `E2E TOTAL`, headers `X-Model-Load-Ms`, `X-Prep-Ms`, `X-Inference-Ms`, `X-Total-Ms`, `X-Input-Duration-S`, `X-Output-Duration-S`, `X-Agent-Transcript` (`client.py:233-248`).

## Client CLI
`parse_args()` (`client.py:256`):

| Flag | Default / choices |
|---|---|
| `--mode` | `ws` (choices `ws`, `rest`) |
| `--server` | `ws://localhost:8000/ws/speech_to_speech/` |
| `--http-server` | `None` (e.g. `http://localhost:8000`) |
| `--file` / `--mic` | mutually exclusive, required |
| `--seconds` | `5.0` |
| `--output` | `nemotron_response.wav` |
| `--instructions` | `"You are a helpful AI voice assistant. Answer naturally and concisely in spoken English."` |
| `--chunk-ms` | `80` |
| `--realtime-send` | store_true |
| `--play` | store_true |
| `--timeout` | `600.0` |

`main()` (`client.py:297-307`): `--file` → `load_audio_pcm16_24k`, else `record_mic(args.seconds)`; `--mode ws` → `asyncio.run(run_ws(...))`, else `run_rest(...)`.

## Server config
Verbatim (`server.py:40-69`):
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
Defaults (`server.py:72-92`):
```python
DEFAULT_SYSTEM_PROMPT = (
    "You are an AI voice assistant developed by NVIDIA. "
    "Answer naturally in a spoken conversational style. "
    "Be concise and helpful."
)
app = FastAPI(title="NVIDIA NemotronLabs VoiceChat 11B Speech-to-Speech API", version="1.0.0")
model = None
model_load_ms = None
inference_lock = asyncio.Semaphore(MAX_CONCURRENT)
```
NeMo imports (`server.py:26-33`): `TARGET_SR, SOURCE_SR, build_model, encode_system_prompt, load_wav_16k_mono, run_offline_inference` from `nemo.collections.speechlm2.inference.utils.offline_voicechat`.

## Server helpers and inference
- `now_ms()` (`server.py:100`), `make_event(event_type, **kwargs)` with `event_id=uuid4` (`server.py:103-109`).
- `pcm16_bytes_to_wav_file(pcm_bytes, sample_rate=CLIENT_SAMPLE_RATE)` (`server.py:112`): trims odd trailing byte, `<i2` → float32 `/32768.0`, `tempfile.mkstemp(suffix=".wav")`, `sf.write(..., subtype="PCM_16")`.
- `upload_to_temp_file(data, suffix=".wav")` (`server.py:146-159`): `mkstemp` + `Path(path).write_bytes(data)`.
- `tensor_audio_to_pcm16_24k(audio_tensor, audio_len)` (`server.py:161`): slices `[:audio_len]`, `torchaudio.functional.resample(MODEL_OUTPUT_SR, CLIENT_SAMPLE_RATE)` when different, clamps `[-1.0, 1.0]`, scales `*32767.0` to `<i2`.
- `tensor_audio_to_wav_bytes(audio_tensor, audio_len)` (`server.py:199`): `sf.write(buffer, audio, MODEL_OUTPUT_SR, format="WAV", subtype="PCM_16")`.
- `_infer_sync(wav_path, system_prompt)` (`server.py:229`): `load_wav_16k_mono(wav_path, device=DEVICE)` → `encode_system_prompt(model, system_prompt, device=DEVICE)` (timed as `prep_ms`) → `run_offline_inference(model, input_signal, input_signal_lens, prompt_tokens, prompt_token_lens)` (timed as `inference_ms`); raises `RuntimeError("Nemotron VoiceChat returned no audio.")` when `result.get("audio") is None`; returns `text, audio, audio_len, prep_ms, inference_ms, input_duration_s (wav_1d.shape[0]/MODEL_INPUT_SR), output_duration_s (audio_len/MODEL_OUTPUT_SR)`.
- `infer(wav_path, system_prompt)` (`server.py:313`): `async with inference_lock: return await asyncio.to_thread(_infer_sync, wav_path, system_prompt)`.

## Server startup and basic endpoints
`startup_event()` (`server.py:330`): prints `MODEL_ID/MODEL_PATH/DEVICE`; when `DEVICE.startswith("cuda")` requires `torch.cuda.is_available()`, logs GPU name/VRAM/torch version, raises on `total_vram_gb < MIN_GPU_VRAM_GB`; raises when `MODEL_PATH` missing; `await asyncio.to_thread(build_model, MODEL_PATH, DEVICE)` with `OutOfMemoryError` → `empty_cache()` + `RuntimeError`; records `model_load_ms`; logs allocated/reserved GB.
- `GET /` (`server.py:535`): returns `service=nemotron-voicechat-standalone`, `model=MODEL_ID`, `status=ready/loading`, `websocket=/ws/speech_to_speech/`, `openai_compatible=/openai-compatible/v1/audio/speech-to-speech`, `port=PORT`.
- `GET /health` (`server.py:~560-597` visible part): returns `status=ok/not_ready`, `model, device, model_load_ms, cuda_available`, plus `gpu/gpu_total_gb/gpu_allocated_gb` when CUDA present. Remaining `health` tail and all endpoints after it were truncated in the chunk (18499 chars cut) and are not described here.

## Update probe
`update.py:4` posts to `https://qwen3-tts-150916788856.us-central1.run.app/v1/audio/speech` with payload verbatim (`update.py:6-14`):
```python
{"model": "qwen3-tts-0.6b", "input": "I cannot believe we finally made it!",
 "voice": "Aiden", "instructions": "Speak happily and with excitement.",
 "response_format": "wav", "speed": 1.0, "language": "English"}
```
Uses `requests.post(url, json=payload, stream=True, timeout=300)` (`update.py:18-23`), streams `iter_content(chunk_size=65536)` to `openai_test.wav` (`update.py:33`), times TTFB/TTFA/total (`update.py:46-54`), prints server headers `X-Server-Inference-MS`, `X-Server-Encoding-MS`, `X-Server-Total-MS`, `X-Audio-Duration-S`, `X-RTF` (`update.py:80-98`). The file tail appends a curl command, a LiveKit TTS warning JSON, an optimization-opportunities note list, and Dia `[S1]/[S2]` speaker/long-generation notes (`update.py:~104-167`).

**Covers:** .dockerignore, client-requirements.txt, client.py, requirements.txt, server.py (visible portion only; truncated after health endpoint), update.py
