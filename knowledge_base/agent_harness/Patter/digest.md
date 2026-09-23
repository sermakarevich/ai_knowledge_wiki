> [[index|Wiki]] | [[summary|Summary]]
# PatterAI/Patter — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Patter is the open-source Python/TypeScript SDK that gives an AI agent a phone number by owning the full voice stack between the application and the phone network.
## Key points
- Patter gives an AI agent a phone number and handles everything between the agent and the phone network: agent loop, LLM, STT, TTS, real-time voice, audio processing, and carrier (README.md:38).
- The SDK ships in Python (`pip install getpatter`) and TypeScript (`npm install getpatter`) with the same surface, hooks, and events at full parity (README.md:40).
- Every stack layer is provider-swappable in one line across LLM, STT, TTS, realtime engine, and carrier (README.md:41).
- The stack composes in Realtime, Pipeline, or Hybrid mode and claims 27+ provider integrations, 3 voice modes, and 2 SDKs at parity (README.md:46-48).
- On top of the stack sit an automatic LLM fallback chain, identical cross-carrier tools / call transfer / guardrails, and a vendor-neutral OpenTelemetry call trace (README.md:59).
- Local runs use a built-in tunnel and dashboard or a terminal-simulated call with no phone required, with credentials read from environment variables (README.md:42, README.md:79).
- Anonymous opt-out telemetry collects only SDK version and bucketed provider/model and call facts, never content or secrets (README.md:121).
## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** These nine root files define the repo's editor/Git conventions, ignored artifacts, local credential template, runtime pins, commit hygiene and secret scanning, AI-agent contribution contract, and vulnerability reporting policy.
## Key points
- `.editorconfig` enforces UTF-8, LF endings, final newline, space indent size 2 (4 for `*.py`, tabs for `Makefile`), with `trim_trailing_whitespace = false` for markdown (`.editorconfig:1-18`).
- `.env.example` is the local-mode credential template copied via `cp .env.example .env`, requiring one telephony carrier (Twilio active, Telnyx/Plivo commented) plus `OPENAI_API_KEY` by default (`.env.example:4-12`, `.env.example:26-27`).
- `.gitattributes` normalizes all checkins to LF (`* text=auto eol=lf`) and marks lock/minified files linguist-generated and media/font/audio extensions binary (`.gitattributes:1-8`, `.gitattributes:10-18`).
- `.gitignore` keeps secrets, runtimes, and artifacts local: `.env`/`.env.*` (except `.env.example`), `.venv/`, `call-logs/`, `.claude/`/`CLAUDE.md`, `.agents/`/`.crush/`/`.goose/`, `node_modules/`, build/coverage outputs (`.gitignore:7-9`, `.gitignore:23-30`).
- Runtime pins are Node `20` (`.nvmrc:1`) and Python `3.12` (`.python-version:1`).
- `.pre-commit-config.yaml` runs hygiene hooks (trailing-whitespace, end-of-file-fixer, check-yaml/json, large-file cap 3000KB, debug-statements, private-key detection, LF enforcement) plus gitleaks on every commit, while Python ruff is commented out pending a cleanup PR and TS lint is deferred to CI (`.pre-commit-config.yaml:31-33`, `.pre-commit-config.yaml:41-49`, `.pre-commit-config.yaml:52-55`).
- `AGENTS.md` makes feature parity (both SDKs, same PR, `snake_case` ↔ `camelCase`), `CHANGELOG.md` under `## Unreleased`, opt-in backward compatibility, real-path tests with provider-boundary-only mocks, no secrets/PII, no foreign license headers, and async-only I/O blocking requirements, validated by `scripts/pr-validate.sh` (AGENTS.md:13-26, AGENTS.md:38-41).
- `SECURITY.md` routes vulnerability reports to `security@getpatter.com` with 48h acknowledgment / 7-day assessment / 90-day fix targets, scopes in telephony/auth/credential/injection/SSRF issues, and requires coordinated disclosure (SECURITY.md:6-14, SECURITY.md:18-24, SECURITY.md:38-39).
## The system in five moves
1. Patter positions itself as the full voice stack between the application and the phone network, owning the agent loop plus LLM, STT, TTS, realtime voice, audio, and carrier.
2. The builder consumes that stack through one parity API in Python or TypeScript, swapping any provider layer in one line and composing Realtime, Pipeline, or Hybrid modes.
3. Calls run locally via tunnel plus dashboard or terminal simulation, with credentials supplied from environment variables per the `.env.example` carrier template.
4. Cross-cutting behavior hardens the call: automatic LLM fallback, identical cross-carrier tools/transfer/guardrails, and a vendor-neutral OpenTelemetry trace.
5. The repo enforces how that system is built and reported: editor/Git/runtime/commit/secret conventions, parity plus changelog plus real-path-test contribution contract, and a coordinated-disclosure security policy.
