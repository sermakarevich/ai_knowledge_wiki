> PDF location (no source.pdf under 2 MB in run dir): https://github.com/Nikki1404/nemotron_voicechat_11B
# Nikki1404/nemotron_voicechat_11B
Source: https://github.com/Nikki1404/nemotron_voicechat_11B
Kind: repo
Fetched: 2026-09-22T14:26:09.471565+00:00
Tool: git-clone

# Nikki1404/nemotron_voicechat_11B

Commit: db12fd5130360b9df35ab8d00f3acc317191a5bd

## README

# NVIDIA NemotronLabs VoiceChat 11B — Standalone Speech-to-Speech App

This project wraps `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` behind two clearly separated API styles:

- Native WebSocket speech-to-speech endpoint: `ws://HOST:8000/ws/speech_to_speech/`
- OpenAI-compatible HTTP namespace: `/openai-compatible/v1/...`

## Endpoints

```text
GET   /health
GET   /ws/speech_to_speech/health

WS    /ws/speech_to_speech/

GET   /openai-compatible/v1/models
POST  /openai-compatible/v1/audio/speech-to-speech
```

## How microphone mode behaves

Microphone mode is still speech-to-speech.

Flow:

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

Example:

You speak:

```text
"What is the capital of Japan?"
```

The microphone audio is recorded and sent to the server. The VoiceChat model processes the
speech directly and produces its spoken answer. The response audio is streamed back through
the WebSocket, saved as a WAV file, and optionally played immediately.

So file mode and mic mode differ only in where the input audio comes from:

```text
FILE MODE:
sample.wav -> server -> model -> response audio -> response.wav / speakers

MIC MODE:
microphone -> server -> model -> response audio -> response.wav / speakers
```

## Current mic behavior

The included client currently uses push-to-talk style recording:

```bash
python client.py \
  --mode ws \
  --server ws://localhost:8000/ws/speech_to_speech/ \
  --mic \
  --seconds 5 \
  --output mic_response.wav \
  --play
```

Behavior:

1. Client records your microphone for 5 seconds.
2. Audio is split into WebSocket chunks.
3. Chunks are sent to `/ws/speech_to_speech/`.
4. Client commits the utterance.
5. Nemotron VoiceChat generates the spoken response.
6. Server streams response PCM audio back.
7. Client saves it to `mic_response.wav`.
8. `--play` plays it through your speakers.

This is turn-based speech-to-speech:

```text
YOU SPEAK -> STOP -> MODEL RESPONDS WITH AUDIO
```

It is not yet continuous duplex conversation:

```text
YOU SPEAK <-> MODEL SPEAKS AT THE SAME TIME
```

That would require continuous microphone capture, VAD/end-of-turn detection, interruption handling,
and barge-in logic.

## Dependency layout

- `requirements.txt`: complete Docker/server/model Python dependency set.
- `client-requirements.txt`: lightweight dependencies for running `client.py` locally.
- Docker base: `nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04`.
- Python: 3.12 inside the container.
- Docker installs the Python dependencies with `pip install --no-build-isolation -r requirements.txt`.

## Build

```bash
docker build -t nemotron-voicechat:latest .
```

## Run

```bash
docker run --rm -it \
  --gpus all \
  --ipc=host \
  --shm-size=8g \
  -p 8000:8000 \
  nemotron-voicechat:latest
```

## WebSocket file test

```bash
python client.py \
  --mode ws \
  --server ws://localhost:8000/ws/speech_to_speech/ \
  --file sample.wav \
  --output response.wav \
  --play
```

## WebSocket microphone test

```bash
python client.py \
  --mode ws \
  --server ws://localhost:8000/ws/speech_to_speech/ \
  --mic \
  --seconds 5 \
  --output mic_response.wav \
  --play
```

## OpenAI-compatible file test

```bash
python client.py \
  --mode rest \
  --http-server http://localhost:8000 \
  --file sample.wav \
  --output response.wav \
  --play
```

This calls:

```text
POST /openai-compatible/v1/audio/speech-to-speech
```

## OpenAI-compatible microphone test

```bash
python client.py \
  --mode rest \
  --http-server http://localhost:8000 \
  --mic \
  --seconds 5 \
  --output mic_response.wav \
  --play
```

The microphone is recorded locally first, wrapped as WAV, and submitted to the OpenAI-compatible
HTTP endpoint. The returned speech is saved and optionally played.

## Direct curl test

```bash
curl -X POST http://localhost:8000/openai-compatible/v1/audio/speech-to-speech \
  -F "file=@sample.wav" \
  -F "instructions=You are a helpful voice assistant. Answer briefly." \
  -F "response_format=wav" \
  --output response.wav
```

## Audio format

Native WebSocket boundary:

```text
Input : PCM16 mono, 24 kHz
Output: PCM16 mono, 24 kHz
```

The server handles the conversion required by the model internally.


## Top-level layout

- .dockerignore (~5 lines)
- client-requirements.txt (~5 lines)
- client.py (~311 lines)
- Dockerfile (~196 lines)
- README.md (~215 lines)
- requirements.txt (~22 lines)
- server.py (~1338 lines)
- update.py (~171 lines)

