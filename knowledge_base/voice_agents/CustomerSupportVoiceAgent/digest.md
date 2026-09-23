> [[index|Wiki]] | [[summary|Summary]]
# 🎙️ AI Voice Agent — Mission Control — Digest
## 1. [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]]
**In one sentence:** A production-ready conversational customer-support voice agent implementing a local/free-tier STT → LLM → TTS pipeline with RAG, ticket management, and a Mission Control HUD, claiming up to 90% lower operating cost than managed voice-AI platforms.
## Key points
- Bypassing managed platforms (Retell AI, Vapi, Synthflow) cuts operating expense by up to **90%** by avoiding high inference markup multipliers.
- Full pipeline is Speech-to-Text → LLM → Text-to-Speech: browser captures 16kHz PCM16 audio over WebSocket, server transcribes locally, Groq reasons, Edge TTS streams back sentence-by-sentence.
- STT is local **Faster-Whisper (`small.en`, 244M params)**; LLM is **Groq (Llama 3.3 70B)**; TTS is neural **edge-tts** with sentence-level streaming plus **PyAV** decode to PCM16 chunks.
- Built-in RAG engine ingests `.txt`/`.md`/`.pdf` files dropped in `knowledge/`, embeds with `all-MiniLM-L6-v2`, and retrieves via local `numpy` cosine similarity into `data/knowledge_index.json`.
- Agent does autonomous support-ticket management that updates existing tickets rather than creating duplicates, plus full-duplex barge-in where interrupts cancel ongoing TTS.
- Backend is Python + FastAPI (WebSocket streaming) with SQLite via SQLAlchemy; frontend is vanilla HTML/CSS/JS in `app/static/`; only API key required is Groq (`GROQ_API_KEY` in `.env`).
- Run flow is `python main.py` then open `http://127.0.0.1:8000` → click **Start Call** → speak; requires Python 3.9+ and a Groq Cloud API key.
## The argument in five moves
1. Managed voice-AI platforms impose high inference markups, so a custom-built agent avoids them and cuts operating expense by up to 90%.
2. The replacement is a complete real-time STT → LLM → TTS loop: 16kHz PCM16 browser audio over WebSocket, energy-based VAD, local Faster-Whisper transcription, Groq Llama 3.3 70B reasoning, and sentence-streamed Edge TTS decoded via PyAV.
3. Domain knowledge comes from an autonomous RAG engine that ingests manuals dropped in `knowledge/` and retrieves them with all-MiniLM-L6-v2 embeddings and local numpy cosine search.
4. The agent behaves like production support staff: it updates existing tickets instead of duplicating them and supports full-duplex barge-in that cancels ongoing TTS, surfaced through a Mission Control HUD on FastAPI and SQLite.
5. The whole stack stays local, free-tier, and reproducible: vanilla frontend, Groq as the only API key, Python 3.9+, `python main.py`, open `http://127.0.0.1:8000` and speak.
