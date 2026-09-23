> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The top-level dependency manifest pins the entire backend runtime — API, data, voice, and ML/document stack — in a single install line.
## Key points
- The component consists of a single top-level file, `requirements.txt`, declared as 1 source file in the chunk (requirements.txt:1).
- A single `pip install` line installs the web/API layer `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `python-multipart`, and `python-dotenv` (requirements.txt:1).
- The same line pins HTTP/database/migration tooling via `httpx`, `sqlalchemy`, `psycopg[binary]`, and `alembic` (requirements.txt:1).
- Real-time voice and Google AI integration come from `livekit-agents[google]~=1.5`, `livekit-plugins-ai-coustics`, `google-adk`, and `google-genai`, plus `twilio` and `apscheduler` (requirements.txt:1).
- Document and tabular processing is covered by `pymupdf`, `pypdf`, `pandas`, `openpyxl`, `pytesseract`, and `Pillow` (requirements.txt:1).
- Numeric/ML, observability, and testing needs are met by `numpy`, `scikit-learn`, `joblib`, `structlog`, `opentelemetry-api`, `opentelemetry-sdk`, `pytest`, and `pytest-asyncio` (requirements.txt:1).
---
## requirements.txt
Verbatim excerpt (requirements.txt:1):
```
pip install fastapi "uvicorn[standard]" pydantic pydantic-settings python-multipart python-dotenv httpx sqlalchemy "psycopg[binary]" alembic "livekit-agents[google]~=1.5" livekit-plugins-ai-coustics google-adk google-genai twilio apscheduler pymupdf pypdf pandas openpyxl pytesseract Pillow numpy scikit-learn joblib structlog opentelemetry-api opentelemetry-sdk pytest pytest-asyncio
```
| Group | Packages (requirements.txt:1) |
|---|---|
| Web / API / config | `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `python-multipart`, `python-dotenv` |
| HTTP / DB / migrations | `httpx`, `sqlalchemy`, `psycopg[binary]`, `alembic` |
| Voice / AI / scheduling | `livekit-agents[google]~=1.5`, `livekit-plugins-ai-coustics`, `google-adk`, `google-genai`, `twilio`, `apscheduler` |
| Documents / tables / OCR | `pymupdf`, `pypdf`, `pandas`, `openpyxl`, `pytesseract`, `Pillow` |
| Numeric / ML / observability / tests | `numpy`, `scikit-learn`, `joblib`, `structlog`, `opentelemetry-api`, `opentelemetry-sdk`, `pytest`, `pytest-asyncio` |

**Covers:** requirements.txt
