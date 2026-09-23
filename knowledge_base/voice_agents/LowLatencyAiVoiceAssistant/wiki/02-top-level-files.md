> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The top-level files provide two entry points — a Streamlit web UI (`app.py`) and a CLI loop (`main.py`) — that both chain audio capture/transcription → LLM response → TTS playback, plus env, ignore, and dependency files that configure keys and builds.
## Key points
- `app.py` implements the Streamlit entry point, wiring `capture_and_transcribe_audio`, `generate_llm_response`, and `convert_text_to_speech`/`play_audio` into a button-driven speak → transcribe → respond → speak-back flow (app.py:1-6, app.py:41-65).
- `app.py` keeps per-session chat state in `st.session_state.conversation_history` and renders it with `update_conversation` / `display_conversation` helpers (app.py:9-11, app.py:28-38).
- `main.py` implements the CLI/terminal entry point as `async def main_interaction_loop(use_kokoro=False)`, looping forever over transcribe → LLM → TTS with a spoken `stop` exit condition (main.py:12-33).
- `main.py` selects the TTS backend by flag: local Kokoro-82M streaming via `stream_kokoro_tts(response)` versus cloud Edge-TTS via `convert_text_to_speech` + `play_audio` (main.py:14-17, main.py:48-53).
- `.env.example` declares the only two required secrets, `HF_API_KEY` and `GROQ_API_KEY`, renamed to `.env` at setup time (.env.example:1-4).
- `requirements.txt` pins the Python stack (`faster-whisper`, `edge-tts`, `dspy`, `streamlit`, `streamlit-webrtc`, `pygame`, `huggingface-hub==0.24.6`, and others) while `packages.txt` lists the apt system build dependencies for audio (`build-essential`, `libasound-dev`, `portaudio19-dev`, `python3-pyaudio`) (requirements.txt:1-14, packages.txt:1-5).
- `.gitignore` excludes bytecode, secrets, virtualenvs, OS files, and local audio/test artifacts (`__pycache__/`, `.env`, `venv/`, `.DS_Store`, `Testing/audio files`, `s-to-s`) (.gitignore:1-19).
---
## app.py — Streamlit entry point
Streamlit page config plus imports of the three pipeline stages (app.py:1-7):
```
import streamlit as st
import asyncio
from utils.audio_processing import capture_and_transcribe_audio
from utils.llm_interaction import generate_llm_response
from utils.tts_conversion import convert_text_to_speech, play_audio

st.set_page_config(page_title="Voice Assistant", layout="wide")
```
Session-state history init (app.py:9-11):
```
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
```
Tunable voice settings in the sidebar with exact parameter names and ranges (app.py:13-17):

| Widget | Variable | Options / range | Default |
|---|---|---|---|
| `st.sidebar.slider("Pitch", -10, 10, 0, 1)` | `pitch` | −10 to +10, step 1 | 0 |
| `st.sidebar.slider("Speed", -50, 50, 0, 1)` | `speed` | −50 to +50, step 1 | 0 |
| `st.sidebar.selectbox("Voice", ["en-US-JennyNeural", "en-US-GuyNeural"])` | `voice` | JennyNeural / GuyNeural | JennyNeural |

Button-driven three-step flow (app.py:41-72):
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
Sign handling: non-negative `pitch`/`speed` values are prefixed with `+` before formatting as `f"{pitch}Hz"` / `f"{speed}%"` (app.py:60-63). History helpers append `{User, Assistant}` dicts and render them as `**You**: …` / `**Assistant**: …` markdown (app.py:28-38).

## main.py — CLI entry point
Async loop signature and engine banner (main.py:12-17):
```
async def main_interaction_loop(use_kokoro=False):
    """Main loop for capturing speech, generating responses, and playing audio."""
    if use_kokoro:
        print("🎤 TTS Engine: Kokoro-82M (local)")
    else:
        print("🎤 TTS Engine: Edge-TTS (cloud)")
```
Loop body: transcribe, `stop` keyword exits, history is a list of single-key dicts flattened into `history_context` for the LLM call (main.py:21-45):
```
transcribed_text = await capture_and_transcribe_audio()
if 'stop' in transcribed_text.lower():
    print("Goodbye!")
    break
conversation_history.append({"User": transcribed_text})
history_context = ' '.join(
    [f"{key}: {value}" for entry in conversation_history for key, value in entry.items()]
)
response = generate_llm_response(transcribed_text, history_context)
conversation_history.append({"Assistant": response})
```
TTS branch with fixed Edge-TTS defaults (main.py:48-53):
```
if use_kokoro:
    # Kokoro streams audio directly to speakers — no file I/O
    stream_kokoro_tts(response)
else:
    audio_file = await convert_text_to_speech(response, rate="+0%", pitch="+0Hz")
    play_audio(audio_file)
```
CLI flag table (main.py:59-68):

| Flag | Action | Help text |
|---|---|---|
| `-k`, `--kokoro` | `action="store_true"`, passed as `main_interaction_loop(use_kokoro=args.kokoro)` | `"Use Kokoro-82M local TTS instead of Edge-TTS (cloud)"` |

Launched via `asyncio.run(main_interaction_loop(use_kokoro=args.kokoro))` under `if __name__ == "__main__":` (main.py:59-68).

## .env.example — secrets template
Verbatim content (.env.example:1-4):
```
# Rename the file to .env

HF_API_KEY=Hugging-Face-Api-Key
GROQ_API_KEY=Your-Groq-Api-Key
```

## .gitignore — excluded paths
Verbatim content (.gitignore:1-19):
```
# Ignore Python bytecode
__pycache__/
*.pyc

# Ignore environment files
.env

# Ignore virtual environments
venv/
.env/
*.env

# Ignore system files
.DS_Store
Thumbs.db

Testing/audio files

s-to-s
```

## packages.txt and requirements.txt — system and Python dependencies
`packages.txt` verbatim (packages.txt:1-5):
```
build-essential
libasound-dev
portaudio19-dev
python3-pyaudio
python3-distutils
```
`requirements.txt` verbatim (requirements.txt:1-14):
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
Note: `webrtcvad` is present but commented out (requirements.txt:8); `huggingface-hub` is the only pinned version (`==0.24.6`) (requirements.txt:4).

**Covers:** `app.py`, `main.py`, `.env.example`, `.gitignore`, `packages.txt`, `requirements.txt`
