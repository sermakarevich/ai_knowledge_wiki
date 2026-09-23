---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: 🎙️ AI Voice Agent — Mission Control
### Q1. Why build a custom voice agent instead of using Retell AI, Vapi, or Synthflow?
> [!tip]- Answer
> Building custom avoids high inference markup multipliers charged by managed voice-AI platforms, cutting operating expense by up to 90%. The tradeoff is owning the full STT → LLM → TTS stack with local Whisper layouts and direct async generators. See [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]].
### Q2. What are the six stages of the real-time voice pipeline, from mic to speaker?
> [!tip]- Answer
> The browser captures 16kHz PCM16 audio over WebSocket, then server-side energy-based VAD triggers transcription. Faster-Whisper (small.en) transcribes locally, Groq Llama 3.3 70B generates the response plus tool arguments, and Edge TTS synthesizes sentence-by-sentence with PyAV decoding to PCM16 chunks streamed to the browser. See [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]].
### Q3. Which models and services power STT, LLM reasoning, and TTS, and why this mix?
> [!tip]- Answer
> STT is local Faster-Whisper small.en (244M params) for accurate recognition of names and accents at zero cost. Reasoning is Groq-hosted Llama 3.3 70B for millisecond inference with a professional support persona, and TTS is neural edge-tts streamed sentence-by-sentence for instant playback. Only the Groq key is required. See [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]].
### Q4. How does the built-in RAG engine ingest and retrieve domain knowledge?
> [!tip]- Answer
> The server auto-scans the knowledge/ directory on startup for .md, .txt, and .pdf files. Text is embedded with the all-MiniLM-L6-v2 transformer and searched locally with numpy cosine similarity, persisting to data/knowledge_index.json with no vector database needed. See [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]].
### Q5. How do smart ticket tracking and barge-in make the agent behave like production support staff?
> [!tip]- Answer
> The agent updates existing support tickets rather than creating duplicates, keeping tracking clean across turns. Full-duplex barge-in cancels ongoing TTS the moment the caller interrupts and processes the new speech immediately. Both surface live in the Mission Control HUD. See [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]].
### Q6. What is the tech stack, project layout, and run flow to start a call?
> [!tip]- Answer
> The backend is Python + FastAPI with WebSocket streaming and SQLite via SQLAlchemy, and the frontend is vanilla HTML/CSS/JS in app/static/ with services split into agent.py, rag.py, and whisper_client.py. Prerequisites are Python 3.9+ and a GROQ_API_KEY in .env; run python main.py, open http://127.0.0.1:8000, click Start Call, and speak. See [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]].
### Q7. (Evaluation) A small support team wants to deploy this repo as its live customer-support line next week — what would you recommend and why?
> [!tip]- Answer
> I would recommend a staged pilot over an immediate cutover, because the stack leans on free-tier Edge TTS, energy-based VAD, and a proprietary BRICLIX license with no stated evals or scaling story. Keep the cost win, validate transcription accuracy, barge-in, and ticket-dedup behavior on recorded calls first, then clarify licensing and load limits before going live. See [[wiki/01-ai-voice-agent-mission-control|🎙️ AI Voice Agent — Mission Control]].
