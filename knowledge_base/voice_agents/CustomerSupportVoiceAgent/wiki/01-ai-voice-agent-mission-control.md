> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# 🎙️ AI Voice Agent — Mission Control
**In one sentence:** A production-ready conversational customer-support voice agent implementing a local/free-tier STT → LLM → TTS pipeline with RAG, ticket management, and a Mission Control HUD, claiming up to 90% lower operating cost than managed voice-AI platforms.
## Key points
- Bypassing managed platforms (Retell AI, Vapi, Synthflow) cuts operating expense by up to **90%** by avoiding high inference markup multipliers.
- Full pipeline is Speech-to-Text → LLM → Text-to-Speech: browser captures 16kHz PCM16 audio over WebSocket, server transcribes locally, Groq reasons, Edge TTS streams back sentence-by-sentence.
- STT is local **Faster-Whisper (`small.en`, 244M params)**; LLM is **Groq (Llama 3.3 70B)**; TTS is neural **edge-tts** with sentence-level streaming plus **PyAV** decode to PCM16 chunks.
- Built-in RAG engine ingests `.txt`/`.md`/`.pdf` files dropped in `knowledge/`, embeds with `all-MiniLM-L6-v2`, and retrieves via local `numpy` cosine similarity into `data/knowledge_index.json`.
- Agent does autonomous support-ticket management that updates existing tickets rather than creating duplicates, plus full-duplex barge-in where interrupts cancel ongoing TTS.
- Backend is Python + FastAPI (WebSocket streaming) with SQLite via SQLAlchemy; frontend is vanilla HTML/CSS/JS in `app/static/`; only API key required is Groq (`GROQ_API_KEY` in `.env`).
- Run flow is `python main.py` then open `http://127.0.0.1:8000` → click **Start Call** → speak; requires Python 3.9+ and a Groq Cloud API key.
---
## 💸 Why build custom?
**Covers:** Why Build Custom section

| Claim | Detail from chunk |
|---|---|
| Cost reduction | "consumes up to **90% less operating expense metrics**" vs managed platforms |
| Platforms bypassed | Retell AI, Vapi, Synthflow ("minimizes high inference markup multipliers") |
| Mechanism | "Exposing local Whisper layouts and direct Async generators" |

## 🏗️ System architecture
**Covers:** System Architecture section

> "A production-ready, conversational AI Customer Support Voice Agent. Built to demonstrate a complete system architecture (Speech-to-Text → LLM → Text-to-Speech) using high-performance local and free-tier components."

## ✨ Features
**Covers:** Features section

- **Autonomous RAG Engine:** "drop your manuals (`.txt`, `.md`, `.pdf`) into the `knowledge/` folder, and the AI will answer questions based on them."
- **Ultra-Accurate STT:** "Powered by **Faster-Whisper** (`small.en`, 244M params) for superior recognition of names and accents."
- **Low-Latency Streaming:** "Sentence-level **Text-to-Speech streaming** — hear the response instantly as it generates."
- **Fast LLM Inference:** "**Groq (Llama 3.3 70B)** for millisecond reasoning and professional support persona."
- **Smart Ticket Tracking:** "the AI updates existing tickets rather than cluttering with duplicates."
- **Barge-in Logic:** "Full duplex support — interrupts cancel ongoing TTS and process new speech immediately."
- **Mission Control UI:** "Cyberpunk dark-mode HUD with live waveforms, real-time ticket tracking, and system health status."
- **Zero-Cost STT/TTS:** "Runs entirely on high-performance local models and free-tier neural APIs."

## 🛠️ Tech stack
**Covers:** Tech Stack section

| Layer | Components from chunk |
|---|---|
| Backend | Python + FastAPI (WebSocket streaming) |
| Frontend | Vanilla HTML/CSS/JS (**Share Tech Mono + Fira Code + IBM Plex Sans** fonts) |
| Database | SQLite via SQLAlchemy |
| AI | `faster-whisper` (local STT), `edge-tts` (neural TTS), `groq` (Llama 3.3 LLM) |

## 📂 Project structure
**Covers:** Project Structure section

```text
.
├── app/
│   ├── core/
│   │   ├── config.py         # Environment config
│   │   └── logger.py         # Logging middleware
│   ├── db/
│   │   └── database.py       # SQLAlchemy models
│   ├── routers/
│   │   └── websocket.py      # Real-time streaming handler
│   ├── services/
│   │   ├── agent.py          # LLM logic & tool definitions
│   │   ├── rag.py            # RAG Engine (Retrieval-Augmented Generation)
│   │   └── whisper_client.py # Whisper STT & Edge TTS
│   ├── static/
│   │   ├── index.html        # Dashboard UI
│   │   ├── script.js         # Audio capture & WebSocket logic
│   │   └── style.css         # Dark-mode styling
│   └── main.py               # FastAPI app application factory
├── data/
│   └── knowledge_index.json  # RAG vector index
├── knowledge/                # Text files & PDFs for RAG
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
└── .env                      # API keys (Groq only)
```

## 🚀 Getting started
**Covers:** Getting Started (prerequisites, setup, configure, run)

Prerequisites: Python 3.9+ and a Groq Cloud API key.

```bash
git clone https://github.com/Abdullah-Zafarr/Customer-Support-Voice-Agent-.git
cd Customer-Support-Voice-Agent-

python -m venv .venv
.\.venv\Scripts\activate        # Windows


# source .venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

Configure — create `.env` in root:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

Run:

```bash
python main.py
```

> "Open **http://127.0.0.1:8000** → Click **Start Call** → Speak."

## 🔍 Retrieval-Augmented Generation (RAG)
**Covers:** RAG section

- **Automated Ingestion:** "The server automatically scans the `knowledge/` directory on startup."
- **Neural Search:** "Uses the `all-MiniLM-L6-v2` transformer model to convert text into high-dimensional vectors."
- **Lightweight Index:** "uses a local `numpy`-based cosine similarity search for sub-millisecond retrieval" with "No complex database needed".
- **Supported Formats:** "Just drag and drop `.md`, `.txt`, or `.pdf` files into the `knowledge/` folder."

## 🧠 Pipeline
**Covers:** Pipeline section

1. Browser captures audio → 16kHz PCM16 via WebSocket.
2. Server-side **Energy-Based VAD** triggers transcription.
3. **Faster-Whisper (small.en)** transcribes locally.
4. **Groq (Llama 3.3)** generates response + tool arguments.
5. **Edge TTS** generates audio **sentence-by-sentence** for lowest possible latency.
6. **PyAV** decodes → PCM16 chunks streamed instantly to browser.

## 📄 License
**Covers:** License section

> "Copyright (c) 2026 **BRICLIX**. All rights reserved."
> "Proprietary and Confidential. No part of this repository may be copied, modified, or distributed without explicit written permission from the copyright owner."
