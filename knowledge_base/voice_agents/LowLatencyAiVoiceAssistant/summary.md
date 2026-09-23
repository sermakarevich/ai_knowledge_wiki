# Technical Analysis: Ankur2606/Low-latency-AI-Voice-Assistant

**Repository:** https://github.com/Ankur2606/Low-latency-AI-Voice-Assistant
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

The problem space is terminal- and browser-driven spoken interaction with an LLM without assembling STT, dialogue, and TTS stages by hand: microphone capture, silence filtering, transcription, response generation, and audible reply must run as one loop with bounded latency. The repo addresses it with a fixed three-stage voice pipeline: voice input is transcribed with `faster-whisper(tiny)`, answered by a Hugging Face model, and spoken back with `edge-tts` (README.md:19). Voice activity detection ignores silence with an adjustable threshold (README.md:23, README.md:122), LLM output is capped at 60 tokens / 2 sentences for concise replies (README.md:106, README.md:125), and TTS pitch, voice type, and speed are tunable (README.md:28, README.md:111). Two run modes serve the same pipeline: a real-time terminal loop via `python main.py` and a web UI via `streamlit run app.py` (README.md:72, README.md:77). The primary user is a Python developer prototyping a local voice assistant on a workstation with microphone, speakers, Python 3.8+, Git, and a Hugging Face account (README.md:33, README.md:34, README.md:35).

## 2. High-Level Architecture

```
Microphone ─ ► VAD / capture ─ ► faster-whisper(tiny) STT ─ ► history_context ─ ► LLM ─ ► response text ─ ► TTS ─ ► Speakers
     │                │                        │                       │              │               │                │
     │                ▼                        ▼                       ▼              ▼               ▼                ▼
 app.py          Models\faster_          16 kHz mono,          in-memory list   60 tokens /    edge-tts cloud   play_audio /
 main.py         whisper_stt_tiny.py     VAD threshold 0.1     of {User,        2 sentences    or Kokoro-82M    direct stream
                                          (README.md:99,       Assistant}       (README.md:106, local
                                           README.md:101)      dicts             README.md:125)
```

Data flow in 5 steps. (1) Audio is captured from the microphone and gated by VAD, which classifies speech against a threshold frequency and discards silence; the threshold is adjustable in configuration (README.md:122, README.md:23). (2) Speech is transcribed by `faster-whisper(tiny)` at 16 kHz mono with VAD threshold `0.1` (README.md:99, README.md:101). (3) Transcribed text plus a flattened history string is passed to the Hugging Face LLM, whose output is restricted to 60 tokens or 2 sentences (README.md:104, README.md:106, README.md:125). (4) Response text is synthesized by `edge-tts` with tunable pitch, voice type (male/female), and speed, or by local Kokoro-82M streaming when selected (README.md:109, README.md:28, main.py:48-53). (5) Audio is played back and the turn is appended to history for the next iteration (app.py:28-38, main.py:21-45). Latency is addressed by WRTC low-latency streaming, threading/pipelines, and asynchronous handoff of transcribed text to the inference API, targeting sub-500 ms (README.md:119). Persistent state lives nowhere on disk: per-session chat state is an in-memory list (`st.session_state.conversation_history` in app.py:9-11; a local `conversation_history` list of single-key dicts in main.py:21-45). Secrets live in `.env` (renamed from `.env.example`), excluded by `.gitignore` (.env.example:1-4, .gitignore:1-19).

## 3. The Conversational Turn

The central concept is the conversational turn: a `{User, Assistant}` pair appended to an ordered history that is flattened into a single context string on each iteration. Representation is a list of single-key dicts, e.g. `{"User": transcribed_text}` and `{"Assistant": response}` (main.py:21-45), rendered in the web UI as `**You**: ...` / `**Assistant**: ...` markdown (app.py:28-38). Named kinds: (a) session history `st.session_state.conversation_history`, initialized when absent (app.py:9-11); (b) CLI history `conversation_history`, a plain list built up inside `main_interaction_loop` (main.py:21-45); (c) flattened context `history_context` / `user_inputs`, a space-joined string of `key: value` pairs passed alongside the current utterance to the LLM (main.py:21-45, app.py:41-72). Key query — history flattening in main.py:21-45:

```
conversation_history.append({"User": transcribed_text})
history_context = ' '.join(
    [f"{key}: {value}" for entry in conversation_history for key, value in entry.items()]
)
response = generate_llm_response(transcribed_text, history_context)
conversation_history.append({"Assistant": response})
```

The web variant aggregates prior user turns as `user_inputs = ' '.join([entry['User'] for entry in st.session_state.conversation_history])` before calling `generate_llm_response(transcribed_text, user_inputs)` (app.py:41-72). No vector store, summarizer, or truncation policy is documented; context grows linearly per session.

## 4. LLM / External Service Integration

Providers: Hugging Face inference for response generation and Microsoft Edge TTS cloud synthesis as the default voice backend, with an optional local Kokoro-82M backend that streams directly to speakers without file I/O (README.md:19, README.md:104, README.md:109, main.py:48-53). Required calls per turn: `generate_llm_response(transcribed_text, history_context)` followed by `convert_text_to_speech(response, ...)` and `play_audio(audio_file)` (app.py:41-72, main.py:21-45, main.py:48-53). Optional call: `stream_kokoro_tts(response)` when `use_kokoro` is set, replacing the Edge-TTS convert-plus-play pair (main.py:14-17, main.py:48-53). STT is local (`faster-whisper`) and TTS synthesis parameters (pitch, voice, speed/rate) are passed per call (README.md:99, README.md:109, app.py:60-63). Env vars:

| Variable | Source | Required |
|---|---|---|
| `HF_API_KEY` | .env.example:1-4 | yes, Hugging Face API access |
| `GROQ_API_KEY` | .env.example:1-4 | yes, per template (Groq-backed generation path) |

Setup renames `.env.example` to `.env` and assigns values including the Hugging Face token (README.md:60). Token failures are diagnosed by checking the environment variable (README.md:144).

## 5. The Speak-Transcribe-Respond-Speak-Back Pipeline

The primary workflow is identical in both entry points: capture/transcribe, generate, synthesize, play, record. Each function below is cited to the call site documented in the wiki.

Step 1 — `capture_and_transcribe_audio` (app.py:41-72, main.py:21-45). Microphone audio is captured and transcribed via `faster-whisper(tiny)` with VAD gating at 16 kHz mono, threshold `0.1` (README.md:99, README.md:101, README.md:122). In `app.py` it is driven as `asyncio.run(capture_and_transcribe_audio())` after the Start Speaking button (app.py:41-72); in `main.py` as `await capture_and_transcribe_audio()` at the top of each loop iteration (main.py:21-45).

Step 2 — stop-word check (main.py:21-45). The CLI loop tests `if 'stop' in transcribed_text.lower()` and breaks with `Goodbye!`; the web loop has no documented exit keyword and ends when the button flow completes (main.py:21-45, app.py:41-72).

Step 3 — history assembly (app.py:41-72, main.py:21-45). The turn is appended (`{"User": transcribed_text}`) and prior turns are flattened into `history_context` / `user_inputs` as described in section 3.

Step 4 — `generate_llm_response` (app.py:41-72, main.py:21-45). Called as `generate_llm_response(transcribed_text, user_inputs)` (web) or `generate_llm_response(transcribed_text, history_context)` (CLI); output constrained to 60 tokens / 2 sentences (README.md:106, README.md:125).

Step 5 — `convert_text_to_speech` + `play_audio`, or `stream_kokoro_tts` (app.py:41-72, main.py:48-53). Web: `asyncio.run(convert_text_to_speech(response, voice=voice, pitch=f"{pitch}Hz", rate=f"{speed}%"))` then `play_audio(audio_file)` with sign-prefix handling for non-negative pitch/speed (app.py:60-63). CLI Edge-TTS path uses fixed defaults `rate="+0%"`, `pitch="+0Hz"` (main.py:48-53); Kokoro path calls `stream_kokoro_tts(response)` with no file I/O (main.py:48-53).

Step 6 — `update_conversation` / `display_conversation` (app.py:28-38). The `(transcribed_text, response)` pair is appended to session history and rendered; the CLI equivalent appends `{"Assistant": response}` and loops (app.py:28-38, main.py:21-45). `main_interaction_loop(use_kokoro=False)` is launched via `asyncio.run(...)` under `if __name__ == "__main__":` with the `--kokoro` flag mapped to the parameter (main.py:12-17, main.py:59-68).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `app.py` | 1-72 | Streamlit entry point; page config, sidebar voice controls, button-driven capture → LLM → TTS flow, history helpers |
| `main.py` | 12-68 | CLI entry point; async interaction loop, stop-keyword exit, TTS backend branch, `--kokoro` flag parsing |
| `utils/audio_processing.py` | cited via app.py:1-7, main.py:21-45 | Microphone capture and Whisper transcription (`capture_and_transcribe_audio`); README layout names this `utils/stt.py` |
| `utils/llm_interaction.py` | cited via app.py:1-7, app.py:41-72 | LLM response generation (`generate_llm_response`); README layout names this `utils/llm.py` |
| `utils/tts_conversion.py` | cited via app.py:1-7, main.py:48-53 | Speech synthesis and playback (`convert_text_to_speech`, `play_audio`, `stream_kokoro_tts`); README layout names this `utils/tts.py` |
| `Models\faster_whisper_stt_tiny.py` | cited at README.md:122 | VAD plus tiny-model STT implementation referenced by configuration docs |
| `requirements.txt` | 1-14 | Python dependency list for STT, TTS, LLM, Streamlit, audio playback |
| `packages.txt` | 1-5 | apt system build dependencies for audio (`build-essential`, ALSA, PortAudio, PyAudio) |
| `.env.example` | 1-4 | Secrets template declaring `HF_API_KEY` and `GROQ_API_KEY` |
| `.gitignore` | 1-19 | Excludes bytecode, secrets, virtualenvs, OS files, local audio/test artifacts |
| `README.md` | 8-154 | Documentation: frontmatter, pipeline description, file layout, setup, model config, latency, troubleshooting, license |
| `LICENSE` | cited at README.md:154 | MIT license text |
| `assets/listening_audio.gif` | cited at app.py:41-72 | Listening indicator image shown during capture in the web UI |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `sounddevice` | (none) | Microphone capture / audio I/O |
| `numpy` | (none) | Audio buffer numerics |
| `faster-whisper` | (none) | Local STT (`tiny` model) |
| `edge-tts` | (none) | Cloud TTS synthesis |
| `dspy` | (none) | LLM interaction layer |
| `soundfile` | (none) | Audio file read/write |
| `streamlit` | (none) | Web UI framework |
| `streamlit-webrtc` | (none) | WebRTC audio in the browser UI |
| `python-dotenv` | (none) | Load `.env` secrets |
| `pygame` | (none) | Audio playback backend |
| `asyncio` | (none) | Async orchestration of capture/synthesis |
| `huggingface-hub` | `==0.24.6` | Hugging Face API/model access (only pinned Python package) |
| `webrtcvad` | (commented out) | VAD; present but disabled in requirements.txt:8 |
| `build-essential` | (apt, unpinned) | Native build toolchain for audio packages |
| `libasound-dev` | (apt, unpinned) | ALSA headers for audio I/O |
| `portaudio19-dev` | (apt, unpinned) | PortAudio headers for `sounddevice`/PyAudio |
| `python3-pyaudio` | (apt, unpinned) | PyAudio system package |
| `python3-distutils` | (apt, unpinned) | Packaging utilities for builds |

Constraints are exact strings from requirements.txt:1-14 and packages.txt:1-5; only `huggingface-hub==0.24.6` carries a version pin (requirements.txt:4).

## 8. CLI / Usage Surface

Entry points:

| Entry point | Command | Behavior |
|---|---|---|
| Terminal loop | `python main.py` | Forever transcribe → LLM → TTS; spoken `stop` exits (README.md:72, main.py:12-33) |
| Web UI | `streamlit run app.py` | Button-driven speak → transcribe → respond → speak-back with sidebar voice controls (README.md:77, app.py:41-72) |

Commands and flags:

| Command | Flag | Action |
|---|---|---|
| `python main.py` | `-k`, `--kokoro` | `action="store_true"`, passed as `main_interaction_loop(use_kokoro=args.kokoro)`; selects Kokoro-82M local TTS over Edge-TTS cloud (main.py:59-68) |

Env vars:

| Variable | Set via | Effect |
|---|---|---|
| `HF_API_KEY` | `.env` (from `.env.example`) | Authenticates Hugging Face calls (README.md:60, .env.example:1-4) |
| `GROQ_API_KEY` | `.env` (from `.env.example`) | Second declared secret, Groq-backed generation path (.env.example:1-4) |

Config (sidebar in app.py:13-17; CLI uses fixed defaults in main.py:48-53):

| Setting | Web control | Range / options | Default | CLI equivalent |
|---|---|---|---|---|
| Pitch | `st.sidebar.slider("Pitch", -10, 10, 0, 1)` | -10 to +10, step 1, formatted `f"{pitch}Hz"` with `+` prefix when non-negative | 0 | `pitch="+0Hz"` fixed |
| Speed/rate | `st.sidebar.slider("Speed", -50, 50, 0, 1)` | -50 to +50, step 1, formatted `f"{speed}%"` with `+` prefix when non-negative | 0 | `rate="+0%"` fixed |
| Voice | `st.sidebar.selectbox("Voice", [...])` | `en-US-JennyNeural`, `en-US-GuyNeural` | JennyNeural | not parameterized |

Setup commands (README.md:42, README.md:48, README.md:53):

```bash
git clone https://github.com/your-username/AI-Voice-Assistant-Pipeline.git
python -m venv venv
pip install -r requirements.txt
```

## 9. Extensibility Points

- New STT model or VAD tuning: replace or reparameterize the faster-whisper call and the `0.1` VAD threshold documented in README.md:99 and README.md:101; VAD logic location is given as `Models\faster_whisper_stt_tiny.py` (README.md:122).
- New LLM or prompt policy: edit the `generate_llm_response` implementation imported in app.py:1-7 and called in app.py:41-72 and main.py:21-45; the 60-token / 2-sentence cap (README.md:106, README.md:125) is the first policy to parameterize.
- New TTS backend or voice: extend the `use_kokoro` branch in main.py:48-53 and the `convert_text_to_speech(response, voice=..., pitch=..., rate=...)` call in app.py:41-72; sidebar widgets in app.py:13-17 define the voice-parameter surface to widen.
- New interface: duplicate either `main_interaction_loop` (main.py:12-17) for headless/terminal use or the Start Speaking button block (app.py:41-72) for web use; both consume the same three functions.
- History and memory: replace the list-of-dicts plus string-join pattern (app.py:28-38, main.py:21-45) with truncation, summarization, or a store; no such policy exists currently.
- Secrets and deployment targets: add keys to `.env.example` (currently .env.example:1-4) and system libraries to `packages.txt` (currently packages.txt:1-5).

## 10. Limitations and Gotchas

- **Module paths in docs and code disagree.** The README layout lists `utils/stt.py`, `utils/tts.py`, `utils/llm.py` (README.md:84), while `app.py` imports `utils.audio_processing`, `utils.llm_interaction`, `utils.tts_conversion` (app.py:1-7). Treat imports as authoritative and expect stale references.
- **History grows without bound.** Context is a space-joined string over all prior turns (app.py:41-72, main.py:21-45) with no truncation or summarization, so long sessions inflate prompt size and latency against the 60-token output cap (README.md:106).
- **CLI has no voice tuning.** Pitch, speed, and voice are adjustable in the Streamlit sidebar (app.py:13-17) but hardcoded to `rate="+0%"`, `pitch="+0Hz"` in the CLI Edge-TTS path (main.py:48-53).
- **First run needs ~2 GB download and stable internet** for the `faster-whisper` model (README.md:142); offline or metered environments stall at startup.
- **VAD path uses a Windows-style literal** (`Models\faster_whisper_stt_tiny.py`, README.md:122), which risks path-handling errors on POSIX systems if used verbatim.
- **`webrtcvad` is commented out** in requirements.txt:8, so the documented VAD behavior depends on whichever VAD ships with the faster-whisper path rather than a separately installed `webrtcvad`.

## 11. How It Compares to Alternatives

- **pipecat-ai/pipecat:** full-duplex, interruption-capable pipeline framework with transport, VAD, and turn-taking abstractions; this repo is a single sequential script loop with keyword-stop and no barge-in handling.
- **livekit/agents:** managed realtime transport plus STT/LLM/TTS plugin graph with room-scale deployment; this repo runs locally or in Streamlit with in-memory history and file/dotenv configuration only.
- **openai/openai-realtime-console (WebRTC realtime API demos):** server-side audio-in/audio-out model over a persistent realtime connection; this repo chains three discrete local/cloud calls per turn with explicit convert-then-play steps.
- **KoljaB/RealtimeVoiceChat (and similar faster-whisper + edge-tts hobby stacks):** closest functional analogue — same STT/TTS pair and short-reply capping for latency; this repo adds the dual terminal/Streamlit entry points and the Kokoro-82M local-TTS option.

Positioning: a minimal instructive baseline for turn-based voice interaction on commodity hardware, not a realtime conversation framework; adopt it for prototyping the STT → LLM → TTS loop, and move to Pipecat or LiveKit Agents when interruption handling, multi-user transport, or production session management is required.

## Appendix: Selected Code Snippets

1. Streamlit imports and session-state init (app.py:1-11):

```
import streamlit as st
import asyncio
from utils.audio_processing import capture_and_transcribe_audio
from utils.llm_interaction import generate_llm_response
from utils.tts_conversion import convert_text_to_speech, play_audio

st.set_page_config(page_title="Voice Assistant", layout="wide")
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
```

2. Button-driven pipeline with sign handling (app.py:41-72):

```
if st.button("Start Speaking"):
    status_placeholder.text("Listening... 🎙️")
    image_placeholder=st.image("assets/listening_audio.gif", width=150, caption="Listening...")
    transcribed_text = asyncio.run(capture_and_transcribe_audio())
    ...
    user_inputs = ' '.join([entry['User'] for entry in st.session_state.conversation_history])
    response = generate_llm_response(transcribed_text, user_inputs)
    ...
    audio_file = asyncio.run(convert_text_to_speech(response, voice=voice, pitch=f"{pitch}Hz", rate=f"{speed}%"))
    try:
        play_audio(audio_file)
    except Exception as e:
        st.error(f"Error playing audio: {e}")
    update_conversation(transcribed_text, response)
```

3. CLI loop with stop condition and TTS branch (main.py:12-53):

```
async def main_interaction_loop(use_kokoro=False):
    """Main loop for capturing speech, generating responses, and playing audio."""
    if use_kokoro:
        print("🎤 TTS Engine: Kokoro-82M (local)")
    else:
        print("🎤 TTS Engine: Edge-TTS (cloud)")
    ...
    transcribed_text = await capture_and_transcribe_audio()
    if 'stop' in transcribed_text.lower():
        print("Goodbye!")
        break
    ...
    if use_kokoro:
        # Kokoro streams audio directly to speakers — no file I/O
        stream_kokoro_tts(response)
    else:
        audio_file = await convert_text_to_speech(response, rate="+0%", pitch="+0Hz")
        play_audio(audio_file)
```

4. Secrets template and Python dependencies (`.env.example:1-4`, `requirements.txt:1-14`):

```
# Rename the file to .env

HF_API_KEY=Hugging-Face-Api-Key
GROQ_API_KEY=Your-Groq-Api-Key
```

```
sounddevice
numpy
faster-whisper
huggingface-hub==0.24.6
edge-tts
dspy
soundfile
# webrtcvad
streamlit
streamlit-webrtc
python-dotenv
pygame
asyncio
```
