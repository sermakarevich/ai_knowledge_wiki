> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** End-to-end voice assistant that converts voice to text with Whisper, generates a reply with a Hugging Face LLM, and speaks it back with Edge-TTS, with VAD and tunable voice parameters for low latency.
## Key points
- Converts voice input to text with OpenAI's Whisper, processes it with a Hugging Face LLM, and synthesizes speech back with Edge-TTS as one pipeline (README.md:19).
- Detects voice activity and ignores silence via VAD, with an adjustable threshold in configuration (README.md:23, README.md:122).
- Uses `faster-whisper(tiny)` for STT at 16 kHz mono with VAD threshold `0.1` (README.md:99, README.md:101).
- Restricts LLM output to 60 tokens / 2 sentences for concise, low-latency replies (README.md:106, README.md:125).
- Offers tunable TTS pitch, male/female voice type, and synthesis speed via `edge-tts` (README.md:28, README.md:111).
- Runs in two modes: real-time terminal via `python main.py` and web UI via `streamlit run app.py` (README.md:72, README.md:77).
- Targets sub-500 ms latency via WRTC streaming frameworks, efficient threading/pipelines, and async handoff of transcribed text to the inference API (README.md:119).
---
## Pipeline stages
Voice → `faster-whisper` STT → Hugging Face LLM → `edge-tts` TTS → speech (README.md:19). Declared features (README.md:23, README.md:24, README.md:25, README.md:26, README.md:27, README.md:28):
- **Voice Activity Detection (VAD):** Automatically detects voice activity and ignores silence.
- **Speech-to-Text (STT):** Converts spoken language to text using the `faster-whisper` model.
- **Text-to-Speech (TTS):** Converts text to speech using the `edge-tts` model.
- **Large Language Model (LLM) Integration:** Utilizes a Hugging Face model for generating intelligent responses.
- **Real-Time Response:** Optimized for low latency responses.
- **Tunable Parameters:** Adjust pitch, voice type (male/female), and speed of speech synthesis.

## Entry points and layout
Two run modes (README.md:70, README.md:72, README.md:77):

```bash
python main.py
streamlit run app.py
```

File structure verbatim (README.md:84):

```markdown
- AI-Voice-Assistant-Pipeline/
  - main.py           # Entry point for real-time voice assistant
  - app.py            # Streamlit web interface for the assistant
  - requirements.txt  # Required Python packages
  - utils/
    - stt.py          # Speech-to-Text conversion with Whisper
    - tts.py          # Text-to-Speech conversion with Edge-TTS
    - llm.py          # Large Language Model response generation
  - README.md         # Project documentation
```

Streamlit frontmatter pins the web app (README.md:8, README.md:12, README.md:14):

```yaml
sdk: streamlit
sdk_version: "1.23.1"
app_file: app.py
```

## Model configuration

| Stage | Model | Function | Configuration (README.md:99, README.md:104, README.md:109) |
|---|---|---|---|
| STT | `faster-whisper(tiny)` | Voice input into text | 16 kHz sampling, mono channel, VAD threshold `0.1` |
| LLM | Hugging Face model (selectable) | Text input to response | Restrict output to 60 tokens |
| TTS | `edge-tts` | LLM text back into speech | Tunable `pitch`, `voice type` (male/female), `speed` |

Output restriction (README.md:125): limited to `2 sentences` or `60 new tokens` to ensure concise communication.

VAD location (README.md:122): implemented in `Models\faster_whisper_stt_tiny.py`, classifying speech from threshold frequency and ignoring silence; threshold adjustable in configuration.

## Latency, setup, and operations
Latency guidance (README.md:119): minimize under `500 ms` via Web Real-Time Communication (WRTC) low-latency streaming plus code-level threading/pipelines, e.g. providing transcribed text to the inference API asynchronously.

Setup prerequisites (README.md:33, README.md:34, README.md:35): `Python 3.8+`, `Git`, Hugging Face account for API access. Install (README.md:42, README.md:48, README.md:53):

```bash
git clone https://github.com/your-username/AI-Voice-Assistant-Pipeline.git
python -m venv venv
pip install -r requirements.txt
```

Auth (README.md:60): `Rename .env.example to .env` and assign environment values including the Hugging Face API token.

Operations notes: initial `faster-whisper` download ~2GB needs stable internet (README.md:142); token issues mean checking the environment variable (README.md:144); license is MIT via `LICENSE` (README.md:154).

**Covers:** README.md, AI-Voice-Assistant-Pipeline/ layout (main.py, app.py, requirements.txt, utils/stt.py, utils/tts.py, utils/llm.py)
