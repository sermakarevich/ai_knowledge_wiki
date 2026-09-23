---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: PatterAI/Patter

### Q1. What does Patter own in the voice stack, and what does the builder supply?

> [!tip]- Answer
> The builder supplies only the agent, while Patter owns the agent loop plus LLM, STT, TTS, realtime voice, audio processing, and the telephony carrier. This positioning is why Patter describes itself as the full stack between the application and the phone network. See [[wiki/01-overview|Overview]].

### Q2. How do the Python and TypeScript SDKs relate, and how is provider swapping done?

> [!tip]- Answer
> Both SDKs expose the same surface, hooks, and events at full parity (`pip install getpatter` / `npm install getpatter`), differing only in naming conventions such as `phone_number` versus `phoneNumber`. Every layer — LLM, STT, TTS, realtime engine, and carrier — is swappable in one line. See [[wiki/01-overview|Overview]].

### Q3. What are the three voice composition modes and the cross-cutting behaviors on top of them?

> [!tip]- Answer
> Calls compose in Realtime, Pipeline, or Hybrid mode across 27+ provider integrations spanning LLM, STT, TTS, realtime, telephony, and audio layers. On top sits an automatic LLM fallback chain, identical cross-carrier tools / call transfer / guardrails, and a vendor-neutral OpenTelemetry call trace. See [[wiki/01-overview|Overview]].

### Q4. How do local development, telemetry, and starter templates work in Patter?

> [!tip]- Answer
> Local runs use a built-in tunnel and dashboard or a terminal-simulated call with no phone required, with credentials read from environment variables and `tunnel: true` pointing the number at a Cloudflare tunnel. Telemetry is anonymous and opt-out, collecting only SDK version and bucketed provider/model and call facts, never content or secrets. Eight self-contained template repos (inbound, outbound, tool calling, custom voice, and others) give clone-and-run starting points. See [[wiki/01-overview|Overview]].

### Q5. What do `.env.example`, `.nvmrc`/`.python-version`, and `.gitignore` establish for a local checkout?

> [!tip]- Answer
> `.env.example` is copied via `cp .env.example .env` and requires one carrier (Twilio active, Telnyx/Plivo commented) plus `OPENAI_API_KEY` by default. Runtimes are pinned to Node 20 and Python 3.12. `.gitignore` keeps secrets, runtimes, and artifacts local, including `.env` files, `.venv/`, `node_modules/`, and `call-logs/` with caller PII. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What contribution contract do `AGENTS.md`, `.pre-commit-config.yaml`, and `SECURITY.md` enforce?

> [!tip]- Answer
> `AGENTS.md` requires same-PR Python/TypeScript parity with `snake_case` ↔ `camelCase` mapping, a `CHANGELOG.md` entry under `## Unreleased`, real-path tests mocking only the provider boundary, and async-only I/O, validated by `scripts/pr-validate.sh`. Pre-commit runs whitespace, YAML/JSON, large-file, private-key, and LF hooks plus gitleaks, with ruff commented out pending cleanup. `SECURITY.md` routes reports to `security@getpatter.com` with 48h/7-day/90-day targets and coordinated disclosure. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. (Evaluation) A small team needs a phone-numbered receptionist agent in both Python and TypeScript with swappable voice providers — should they adopt Patter?

> [!tip]- Answer
> Yes for this fit: Patter's parity SDKs, one-line provider swaps, Realtime/Pipeline/Hybrid modes, and tunnel-plus-dashboard local runs directly match the need. The team should still weigh the contribution burden of maintaining both-SDK parity and confirm the LLM fallback, guardrails, and OpenTelemetry trace cover their reliability requirements. See [[wiki/01-overview|Overview]].
