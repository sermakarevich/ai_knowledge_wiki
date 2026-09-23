---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: vishnu97770/Real-Time-Voice-Agent

### Q1. What is the runtime vs. profile split at the heart of Real-Time-Voice-Agent?

> [!tip]- Answer
> The runtime (audio capture, VAD, streaming ASR, tool-grounded reasoning, streaming TTS, barge-in, consent gating, audit logging) is built once and never changes per deployment, while the profile (who the agent is, what data it sees, allowed/forbidden actions) is configuration loaded per call. This lets one engine serve hospitals, banks, telecom, insurance, and admissions without rewriting the core. See [[wiki/01-overview|Overview]].

### Q2. Walk through the real-time loop and explain how it achieves ~200–700 ms perceived latency.

> [!tip]- Answer
> Each turn streams Client audio → VAD → Streaming ASR → LLM (tool-grounded) → Streaming TTS → Client audio, with VAD separating speech from silence and enabling barge-in that cuts playback instantly. Streaming ASR emits incremental transcripts so reasoning starts before the caller finishes, and streaming TTS speaks the first reply sentence instead of waiting for the full response. Together these overlaps hold perceived end-to-end latency to roughly 200–700 ms. See [[wiki/01-overview|Overview]].

### Q3. How do tool-grounding, confirmation, and audit logging constrain the LLM's behavior?

> [!tip]- Answer
> The LLM never states unfetched facts: every account, policy, or application detail must be pulled through a scoped tool call rather than recalled. Any state-changing action (freezing a card, filing a claim, rescheduling an appointment) pauses for explicit caller confirmation, is never assumed, and is always logged. See [[wiki/01-overview|Overview]].

### Q4. How does outbound calling work under the call-job / call-result contract, and what guardrails apply to every vertical?

> [!tip]- Answer
> The business sends a call job (who to call, why, which profile), the platform conducts the call on the same voice loop and returns a call result (outcome, transcript reference, audit trail), with the business owning targeting and result handling. Every profile inherits non-negotiables regardless of vertical: disclose AI identity at call start and never ask for password, PIN, OTP, or full card number. See [[wiki/01-overview|Overview]].

### Q5. What does the repo currently contain versus what is specified but unimplemented, and what merge conflict must a reader navigate?

> [!tip]- Answer
> The repo holds design plus a functional prototype: the PRD PDF, the outbound-calling architecture DOCX, and the browser-native voice-agent-console.html prototype with five mock-data profiles, against a target production stack of Python, AsyncIO, Pipecat/LiveKit Agents, and Gemini/Google ADK. Outbound Twilio/LiveKit + SIP telephony, OCR extraction, the ML risk model, and persistent storage are specified but unimplemented. The chunk also carries an unresolved merge conflict between the HEAD runtime/profile description and the incoming 1ec24ea Python frontend/backend stack with its own frontend/ and backend/ run instructions. See [[wiki/01-overview|Overview]].

### Q6. What does the single top-level requirements.txt line pin, grouped by function?

> [!tip]- Answer
> One pip install line pins the whole backend runtime: FastAPI, uvicorn, pydantic, and config helpers for the web/API layer; httpx, SQLAlchemy, psycopg, and alembic for HTTP/database/migrations; and livekit-agents, ai-coustics, google-adk, google-genai, twilio, and apscheduler for voice/AI/scheduling. Document/OCR needs come from pymupdf, pypdf, pandas, openpyxl, pytesseract, and Pillow, while numpy, scikit-learn, joblib, structlog, OpenTelemetry, pytest, and pytest-asyncio cover numeric/ML, observability, and testing. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Would you recommend deploying this repository as-is for live bank fraud-alert calls, and what must be resolved first?

> [!tip]- Answer
> No: it is design plus prototype, not a deployed system, so live fraud-alert use would be unsafe without real telephony, persistent storage, audit durability, and the specified-but-missing OCR and ML risk pieces. I would first resolve the merge conflict to pick one stack, implement and test the Twilio/LiveKit + SIP path with confirmation and audit trails, and validate the no-PIN/OTP guardrails and latency budget under load. Only then could a bank pilot be justified. See [[wiki/01-overview|Overview]].
