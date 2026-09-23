> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** This repo wraps `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` as a standalone speech-to-speech app exposing a native WebSocket endpoint and an OpenAI-compatible HTTP namespace.
## Key points
- Wraps `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` behind two separated API styles: native WebSocket speech-to-speech and OpenAI-compatible HTTP (README.md:9-12).
- Exposes `GET /health`, `GET /ws/speech_to_speech/health`, `WS /ws/speech_to_speech/`, plus `GET /openai-compatible/v1/models` and `POST /openai-compatible/v1/audio/speech-to-speech` (README.md:16-24).
- Microphone mode is still speech-to-speech: mic PCM16 mono 24 kHz goes through `client.py` to `/ws/speech_to_speech/`, is resampled to model input rate, and response PCM chunks stream back for save/playback (README.md:28-58).
- File mode and mic mode differ only in input audio source; both produce response audio saved as WAV and optionally played (README.md:72-80).
- Included client is turn-based push-to-talk (`YOU SPEAK -> STOP -> MODEL RESPONDS WITH AUDIO`), not continuous duplex; duplex would need continuous capture, VAD/end-of-turn, interruption and barge-in logic (README.md:84-120).
- Dependency/build layout splits `requirements.txt` (Docker/server/model) from `client-requirements.txt` (lightweight local client), on `nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04` with Python 3.12 installed via `pip install --no-build-isolation -r requirements.txt` (README.md:122-128).
- Native WebSocket audio boundary is PCM16 mono 24 kHz in and out, with model-required conversion handled internally by the server (README.md:212-221).
---
## Endpoints
Verbatim endpoint map (README.md:16-24):
```text
GET   /health
GET   /ws/speech_to_speech/health

WS    /ws/speech_to_speech/

GET   /openai-compatible/v1/models
POST  /openai-compatible/v1/audio/speech-to-speech
```
Two API styles (README.md:9-12):
- Native WebSocket speech-to-speech endpoint: `ws://HOST:8000/ws/speech_to_speech/`
- OpenAI-compatible HTTP namespace: `/openai-compatible/v1/...`

## Speech-to-speech flow
Microphone mode flow, verbatim (README.md:32-58):
```text
Microphone
   |
   |  PCM16 mono, 24 kHz
   v
client.py
   |
   | WebSocket audio chunks
   v
/ws/speech_to_speech/
   |
   | resample to model input rate
   v
Nemotron VoiceChat
   |
   | speech response
   v
server.py
   |
   | PCM16 audio chunks
   v
client.py
   |
   +--> save response.wav
   |
   +--> play through speakers when --play is used
```
File vs. mic sources, verbatim (README.md:74-80):
```text
FILE MODE:
sample.wav -> server -> model -> response audio -> response.wav / speakers

MIC MODE:
microphone -> server -> model -> response audio -> response.wav / speakers
```

## Microphone behavior
Push-to-talk example, verbatim (README.md:87-94):
```bash
python client.py \
  --mode ws \
  --server ws://localhost:8000/ws/speech_to_speech/ \
  --mic \
  --seconds 5 \
  --output mic_response.wav \
  --play
```
Behavior sequence (README.md:96-106): record mic for 5 seconds, split into WebSocket chunks, send to `/ws/speech_to_speech/`, commit utterance, model generates spoken response, server streams response PCM back, client saves to `mic_response.wav`, `--play` plays through speakers. Turn-based, verbatim (README.md:107-117):
```text
YOU SPEAK -> STOP -> MODEL RESPONDS WITH AUDIO
```
Not continuous duplex (README.md:113-120):
```text
YOU SPEAK <-> MODEL SPEAKS AT THE SAME TIME
```
Duplex would require continuous microphone capture, VAD/end-of-turn detection, interruption handling, and barge-in logic.

## Dependencies, build, and run
| Item | Value (README.md:122-128) |
|---|---|
| Server/model deps | `requirements.txt` |
| Local client deps | `client-requirements.txt` |
| Docker base | `nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04` |
| Python | 3.12 inside container |
| Install | `pip install --no-build-isolation -r requirements.txt` |

Build, verbatim (README.md:130-134):
```bash
docker build -t nemotron-voicechat:latest .
```
Run, verbatim (README.md:138-145):
```bash
docker run --rm -it \
  --gpus all \
  --ipc=host \
  --shm-size=8g \
  -p 8000:8000 \
  nemotron-voicechat:latest
```

## Client tests
| Test | Command flags (README.md:147-200) |
|---|---|
| WebSocket file | `--mode ws`, `--server ws://localhost:8000/ws/speech_to_speech/`, `--file sample.wav`, `--output response.wav`, `--play` |
| WebSocket mic | `--mode ws`, `--server ws://localhost:8000/ws/speech_to_speech/`, `--mic`, `--seconds 5`, `--output mic_response.wav`, `--play` |
| OpenAI-compatible file | `--mode rest`, `--http-server http://localhost:8000`, `--file sample.wav`, `--output response.wav`, `--play` → `POST /openai-compatible/v1/audio/speech-to-speech` |
| OpenAI-compatible mic | `--mode rest`, `--http-server http://localhost:8000`, `--mic`, `--seconds 5`, `--output mic_response.wav`, `--play` (mic recorded locally, wrapped as WAV, submitted over HTTP) |

Direct curl test, verbatim (README.md:204-210):
```bash
curl -X POST http://localhost:8000/openai-compatible/v1/audio/speech-to-speech \
  -F "file=@sample.wav" \
  -F "instructions=You are a helpful voice assistant. Answer briefly." \
  -F "response_format=wav" \
  --output response.wav
```

## Audio format
Native WebSocket boundary, verbatim (README.md:214-219):
```text
Input : PCM16 mono, 24 kHz
Output: PCM16 mono, 24 kHz
```
The server handles the conversion required by the model internally (README.md:221).

**Covers:** README.md (project purpose, endpoints, mic/file flows, dependency/build/run layout, client and curl tests, audio format)
