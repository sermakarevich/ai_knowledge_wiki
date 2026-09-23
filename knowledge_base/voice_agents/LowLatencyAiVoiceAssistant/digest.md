> [[index|Wiki]] | [[summary|Summary]]
# Ankur2606/Low-latency-AI-Voice-Assistant — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** End-to-end voice assistant that converts voice to text with Whisper, generates a reply with a Hugging Face LLM, and speaks it back with Edge-TTS, with VAD and tunable voice parameters for low latency.
- Converts voice input to text with OpenAI's Whisper, processes it with a Hugging Face LLM, and synthesizes speech back with Edge-TTS as one pipeline (README.md:19).
- Detects voice activity and ignores silence via VAD, with an adjustable threshold in configuration (README.md:23, README.md:122).
- Uses `faster-whisper(tiny)` for STT at 16 kHz mono with VAD threshold `0.1` (README.md:99, README.md:101).
- Restricts LLM output to 60 tokens / 2 sentences for concise, low-latency replies (README.md:106, README.md:125).
- Offers tunable TTS pitch, male/female voice type, and synthesis speed via `edge-tts` (README.md:28, README.md:111).
- Runs in two modes: real-time terminal via `python main.py` and web UI via `streamlit run app.py` (README.md:72, README.md:77).
- Targets sub-500 ms latency via WRTC streaming frameworks, efficient threading/pipelines, and async handoff of transcribed text to the inference API (README.md:119).
## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The top-level files provide two entry points — a Streamlit web UI (`app.py`) and a CLI loop (`main.py`) — that both chain audio capture/transcription → LLM response → TTS playback, plus env, ignore, and dependency files that configure keys and builds.
- `app.py` implements the Streamlit entry point, wiring `capture_and_transcribe_audio`, `generate_llm_response`, and `convert_text_to_speech`/`play_audio` into a button-driven speak → transcribe → respond → speak-back flow (app.py:1-6, app.py:41-65).
- `app.py` keeps per-session chat state in `st.session_state.conversation_history` and renders it with `update_conversation` / `display_conversation` helpers (app.py:9-11, app.py:28-38).
- `main.py` implements the CLI/terminal entry point as `async def main_interaction_loop(use_kokoro=False)`, looping forever over transcribe → LLM → TTS with a spoken `stop` exit condition (main.py:12-33).
- `main.py` selects the TTS backend by flag: local Kokoro-82M streaming via `stream_kokoro_tts(response)` versus cloud Edge-TTS via `convert_text_to_speech` + `play_audio` (main.py:14-17, main.py:48-53).
- `.env.example` declares the only two required secrets, `HF_API_KEY` and `GROQ_API_KEY`, renamed to `.env` at setup time (.env.example:1-4).
- `requirements.txt` pins the Python stack (`faster-whisper`, `edge-tts`, `dspy`, `streamlit`, `streamlit-webrtc`, `pygame`, `huggingface-hub==0.24.6`, and others) while `packages.txt` lists the apt system build dependencies for audio (`build-essential`, `libasound-dev`, `portaudio19-dev`, `python3-pyaudio`) (requirements.txt:1-14, packages.txt:1-5).
- `.gitignore` excludes bytecode, secrets, virtualenvs, OS files, and local audio/test artifacts (`__pycache__/`, `.env`, `venv/`, `.DS_Store`, `Testing/audio files`, `s-to-s`) (.gitignore:1-19).
## The system in five moves
1. Capture voice and gate on activity via VAD so silence is ignored before transcription.
2. Transcribe speech to text with `faster-whisper(tiny)` at 16 kHz mono.
3. Generate a concise reply with a Hugging Face LLM capped at 60 tokens / 2 sentences.
4. Speak the reply back with Edge-TTS (or local Kokoro-82M in CLI mode) with tunable pitch, voice, and speed.
5. Drive the whole loop from either the Streamlit button flow in `app.py` or the async `stop`-to-exit loop in `main.py`, configured via `.env` keys and the pinned Python/system dependencies.
