> [[index|Wiki]] | [[summary|Summary]]
# vishnu97770/Real-Time-Voice-Agent — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Real-Time-Voice-Agent is one reusable real-time voice runtime (VAD → streaming ASR → tool-grounded LLM → streaming TTS) worn by swappable per-vertical Agent Profiles so the same engine serves banks, hospitals, telecom, insurance, and admissions without rewriting the core (01-overview.md:11, 01-overview.md:20-25, 01-overview.md:76).
## Key points
- The project separates a fixed runtime (audio capture, VAD, streaming transcription, tool-grounded reasoning, streaming TTS, barge-in, consent gating, audit logging) from per-call configuration profiles (who the agent is, what data it sees, allowed/forbidden actions) (01-overview.md:22-23).
- The real-time loop streams `Client audio → VAD → Streaming ASR → LLM (tool-grounded) → Streaming TTS → Client audio`, with perceived end-to-end latency ~200–700 ms (01-overview.md:31-34, 01-overview.md:40).
- The LLM never states unfetched facts — every account, policy, or application detail is pulled through a scoped tool call — and any state-changing action pauses for explicit caller confirmation and is logged (01-overview.md:38, 01-overview.md:41).
- Outbound calling reuses the same loop under a call-job / call-result contract: the business sends who to call, why, and which profile; the platform conducts the call and returns outcome, transcript reference, and audit trail (01-overview.md:43).
- Every profile inherits non-negotiables: disclose AI identity at call start and never ask for password, PIN, OTP, or full card number (01-overview.md:55).
- The repo currently holds design plus a functional prototype, not a deployed system; outbound telephony (Twilio/LiveKit + SIP), OCR extraction, ML risk model, and persistent storage are specified but not implemented (01-overview.md:72).
- The chunk contains an unresolved merge conflict: HEAD side describes the runtime/profile split and browser prototype, incoming side (`1ec24ea`) describes a Python/frontend-backend stack with `frontend/` and `backend/` run instructions (01-overview.md:17, 01-overview.md:81, 01-overview.md:94-105).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The top-level dependency manifest pins the entire backend runtime — API, data, voice, and ML/document stack — in a single install line.
## Key points
- The component consists of a single top-level file, `requirements.txt`, declared as 1 source file in the chunk (requirements.txt:1).
- A single `pip install` line installs the web/API layer `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `python-multipart`, and `python-dotenv` (requirements.txt:1).
- The same line pins HTTP/database/migration tooling via `httpx`, `sqlalchemy`, `psycopg[binary]`, and `alembic` (requirements.txt:1).
- Real-time voice and Google AI integration come from `livekit-agents[google]~=1.5`, `livekit-plugins-ai-coustics`, `google-adk`, and `google-genai`, plus `twilio` and `apscheduler` (requirements.txt:1).
- Document and tabular processing is covered by `pymupdf`, `pypdf`, `pandas`, `openpyxl`, `pytesseract`, and `Pillow` (requirements.txt:1).
- Numeric/ML, observability, and testing needs are met by `numpy`, `scikit-learn`, `joblib`, `structlog`, `opentelemetry-api`, `opentelemetry-sdk`, `pytest`, and `pytest-asyncio` (requirements.txt:1).
## The system in five moves
1. Start with one fixed voice runtime built once — capture, VAD, streaming ASR, tool-grounded reasoning, streaming TTS, barge-in, consent, audit — configured per call by a swappable Agent Profile.
2. Run every turn through the streaming loop Client audio → VAD → Streaming ASR → LLM → Streaming TTS so reasoning and speech start early for ~200–700 ms perceived latency.
3. Ground every fact in a scoped tool call and gate every state-changing action behind explicit confirmation, disclosure of AI identity, and audit logging.
4. Reuse the same loop for outbound calling under a call-job / call-result contract, letting one engine serve hospital, bank, telecom, insurance, and admissions verticals.
5. Pin the production backend for that design in a single `requirements.txt` install line — FastAPI, Postgres, LiveKit/Google AI, Twilio, documents/OCR, ML, observability, tests — while the repo itself remains design plus prototype with telephony, OCR, ML model, and storage still unimplemented.
