# Technical Analysis: PatterAI/Patter

**Repository:** https://github.com/PatterAI/Patter
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Closed voice-AI platforms bundle the agent loop, model selection, speech processing, and carrier behavior into one vendor-controlled API and billing unit. The builder cannot change a single layer without migrating the whole system, and carrier-specific behavior diverges across deployments.

PatterAI/Patter addresses this by implementing the full call path between application code and the phone network as a provider-swappable SDK (README.md:38, README.md:46). The builder supplies only agent configuration (system prompt, engine, tools); the SDK owns the agent loop, speech-to-text, text-to-speech, realtime voice handling, audio processing, and telephony carrier integration, composed in Realtime, Pipeline, or Hybrid mode (README.md:46). The same surface is shipped in Python (`pip install getpatter`) and TypeScript (`npm install getpatter`) at stated parity (README.md:40). Cross-cutting behavior — LLM fallback chain, tools/call transfer/guardrails, OpenTelemetry call trace — is defined once and applied identically on every carrier (README.md:59).

Primary user: application developer building an inbound or outbound telephone agent who wants to retain control of each stack layer and run the same code locally and in production.

## 2. High-Level Architecture

```
Application code (systemPrompt, engine, tools)
        │
        ▼
Patter({ carrier, phoneNumber }) ──► phone.agent({ engine, ... })
        │                                      │
        ▼                                      ▼
Telephony layer ──► Realtime / Pipeline / Hybrid composition ──► Provider layer
(Twilio │ Telnyx │ Plivo)          (LLM │ STT │ TTS │ Audio)       (OpenAI, Deepgram, ElevenLabs, ...)
        │                                      │
        ▼                                      ▼
Phone network ◄── Webhook / tunnel ◄── serve({ agent, tunnel }) ──► Observability / guardrails
                                                     │
                                                     ▼
                                              call-logs/ (local transcripts)
```

Data-flow narrative:

1. Provisioning: developer constructs `Patter`/`phone` with a carrier object (`Twilio`, `Telnyx`, `Plivo`) and a `phoneNumber`; credentials resolve from environment variables (README.md:79).
2. Agent binding: `phone.agent()` binds a voice engine (`OpenAIRealtime` or pipeline components), `systemPrompt`/`system_prompt`, and `firstMessage`/`first_message` to that number (README.md:90-96, README.md:108-114).
3. Serving: `phone.serve({ agent, tunnel: true })` exposes a webhook; `tunnel: true` spawns a Cloudflare quick tunnel for local development, while production uses a static `webhook_url` or ngrok (README.md:117).
4. Call execution: inbound audio passes through the carrier adapter into the selected mode (all-in-one realtime engine or discrete STT → LLM → TTS with VAD/suppression), with the LLM fallback chain available mid-call and tools/transfer/guardrails enforced independent of carrier (README.md:46, README.md:59).
5. Observation: each call emits a vendor-neutral OpenTelemetry trace; local runs add a dashboard view or terminal-simulated call with no phone required (README.md:42, README.md:59).

Persistent state: no database or committed store is described in the analyzed pages. Runtime state lives in environment configuration (`.env`, git-ignored per `.gitignore:7-9`), per-call transcripts under `call-logs/` (explicitly never committed per `.gitignore:23-30`), and ephemeral tunnel/webhook bindings. `*.db`/`*.sqlite` are ignored build artifacts, not a defined store (`.gitignore:1-44`).

## 3. The Full Voice Stack (Core Abstraction)

Representation: the central abstraction is a layered voice stack object — one `Patter` instance parameterized by carrier plus one `agent` parameterized by engine — that hides telephony and media plumbing behind provider interfaces swappable in one line (README.md:41).

Named kinds/types with providers (README.md:50-57):

- **LLM — text generation** (README.md:50-57): OpenAI, Anthropic, Google Gemini, Groq, Cerebras.
- **STT — speech-to-text** (README.md:50-57): Deepgram, AssemblyAI, Cartesia, Soniox, Speechmatics, Whisper, Fish Audio.
- **TTS — text-to-speech** (README.md:50-57): ElevenLabs, OpenAI, Cartesia, LMNT, Rime, Telnyx, Fish Audio.
- **Realtime — all-in-one voice** (README.md:50-57): OpenAI Realtime, Gemini Live, Ultravox, ElevenLabs ConvAI.
- **Telephony — phone carriers** (README.md:50-57): Twilio, Telnyx, Plivo.
- **Audio — VAD and suppression** (README.md:50-57): Silero VAD, Krisp, DeepFilterNet.
- **Voice modes** (README.md:46-48): Realtime, Pipeline, Hybrid; stated totals are 27+ integrations, 3 modes, 2 SDKs at parity (README.md:48).

Key query (construction is the query; exact parameter names per README.md:90-96):

```typescript
const phone = new Patter({ carrier: new Twilio(), phoneNumber: "+15550001234" });
const agent = phone.agent({
  engine: new OpenAIRealtime(),
  systemPrompt: "You are a friendly receptionist for Acme Corp.",
  firstMessage: "Hello! How can I help?",
});
await phone.serve({ agent, tunnel: true });
```

## 4. LLM / External Service Integration

The repository calls external LLM, speech, and telephony APIs by design; there is no offline-only path for a live call except terminal simulation for development (README.md:42).

| Layer | Providers | Required vs optional |
|---|---|---|
| LLM | OpenAI, Anthropic, Google Gemini, Groq, Cerebras (README.md:50-57) | Required: one LLM or all-in-one realtime engine per agent; fallback chain entries optional (README.md:59) |
| STT | Deepgram, AssemblyAI, Cartesia, Soniox, Speechmatics, Whisper, Fish Audio (README.md:50-57) | Required in Pipeline/Hybrid mode; subsumed by realtime engine in Realtime mode |
| TTS | ElevenLabs, OpenAI, Cartesia, LMNT, Rime, Telnyx, Fish Audio (README.md:50-57) | Required in Pipeline/Hybrid mode; subsumed by realtime engine in Realtime mode |
| Realtime | OpenAI Realtime, Gemini Live, Ultravox, ElevenLabs ConvAI (README.md:50-57) | Optional alternative to discrete STT+LLM+TTS |
| Telephony | Twilio, Telnyx, Plivo (README.md:50-57) | Required: exactly one carrier per `Patter` instance (README.md:79) |
| Audio | Silero VAD, Krisp, DeepFilterNet (README.md:50-57) | Optional processing layer |
| Observability | OpenTelemetry trace per call (README.md:59) | Built in, vendor-neutral |

Environment variables (`.env.example:9-38`, README.md:79):

| Variable | Role |
|---|---|
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_PHONE_NUMBER` | Default active carrier |
| `TELNYX_API_KEY` / `TELNYX_CONNECTION_ID` / `TELNYX_PHONE_NUMBER` | Alternative carrier (DTMF, transfer, recording) |
| `PLIVO_AUTH_ID` / `PLIVO_AUTH_TOKEN` / `PLIVO_PHONE_NUMBER` | Alternative carrier (WS audio streaming, mu-law 8 kHz, V3 signature) |
| `OPENAI_API_KEY` | Default voice provider (OpenAI Realtime) |
| `DEEPGRAM_API_KEY` / `ELEVENLABS_API_KEY` | Pipeline-mode STT/TTS alternative |
| `ANTHROPIC_API_KEY` | Optional custom LLM for pipeline mode with `on_message` |
| `WEBHOOK_URL` | Omit to auto-tunnel via Cloudflare |
| `PORT` | Commented; default `8000` |

## 5. The Call Path: Provision to Serve (Main Pipeline)

Primary workflow is provision → configure → serve → call, with each step named by its SDK call. Function-level `file.py:line` references below use the only function citations present in the analyzed pages (README.md); SDK-internal implementations under `libraries/` are named in AGENTS.md:45-55 without line numbers and are listed as structural pointers, not verified call sites.

1. Install SDK — `pip install getpatter` (Python, README.md:99-115) or `npm install getpatter` (TypeScript, README.md:81-97).
2. Copy credential template — `cp .env.example .env` then fill carrier plus provider keys (`.env.example:4-5`, README.md:79).
3. Construct telephony binding — `Patter(carrier=Twilio(), phone_number="+15550001234")` in Python (README.md:108-114); `new Patter({ carrier: new Twilio(), phoneNumber: "+15550001234" })` in TypeScript (README.md:90-96). Carrier swap is a one-line constructor change, e.g. `Twilio` to `Telnyx` or `Plivo` (README.md:79).
4. Define agent — `phone.agent(engine=OpenAIRealtime(), system_prompt=..., first_message=...)` in Python (README.md:108-114); `phone.agent({ engine: new OpenAIRealtime(), systemPrompt: ..., firstMessage: ... })` in TypeScript (README.md:90-96).
5. Serve — `await phone.serve(agent, tunnel=True)` in Python (README.md:108-114); `await phone.serve({ agent, tunnel: true })` in TypeScript (README.md:90-96). `tunnel: true` points the number at a Cloudflare quick tunnel; production sets a static webhook URL (README.md:117).
6. Operate — place/receive calls; terminal simulation exercises the same agent without a phone (README.md:42). Telemetry, guardrails, tools, and trace apply per call (README.md:59, README.md:121).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | Line refs to 167 | Defines SDK surface, provider matrix, quickstarts, telemetry, templates; sole behavioral source in analyzed pages (README.md:38-167) |
| `AGENTS.md` | 68 | Agent contribution contract: dual-SDK parity, changelog, compatibility, test, logging rules; validated by `scripts/pr-validate.sh` (AGENTS.md:13-26, AGENTS.md:38-41) |
| `libraries/python/getpatter/client.py` | Unknown (named in AGENTS.md:45-55) | Structural pointer: Python SDK client entry |
| `libraries/python/getpatter/models.py` | Unknown (named in AGENTS.md:45-55) | Structural pointer: Python data models |
| `libraries/python/getpatter/server.py` | Unknown (named in AGENTS.md:45-55) | Structural pointer: Python webhook/server handling |
| `libraries/python/getpatter/telephony/` | Unknown (named in AGENTS.md:45-55) | Structural pointer: Python carrier adapters |
| `libraries/python/getpatter/providers/` | Unknown (named in AGENTS.md:45-55) | Structural pointer: Python LLM/STT/TTS provider integrations |
| `libraries/python/getpatter/services/` | Unknown (named in AGENTS.md:45-55) | Structural pointer: Python auxiliary services |
| `libraries/typescript/src/client.ts` | Unknown (named in AGENTS.md:45-55) | Structural pointer: TypeScript SDK client entry |
| `libraries/typescript/src/types.ts` | Unknown (named in AGENTS.md:45-55) | Structural pointer: TypeScript type definitions |
| `libraries/typescript/src/server.ts` | Unknown (named in AGENTS.md:45-55) | Structural pointer: TypeScript server handling |
| `libraries/typescript/src/stream-handler.ts` | Unknown (named in AGENTS.md:45-55) | Structural pointer: TypeScript media stream handling |
| `libraries/typescript/src/telephony/` | Unknown (named in AGENTS.md:45-55) | Structural pointer: TypeScript carrier adapters |
| `.env.example` | 39 | Credential template: one required carrier plus default/optional provider keys (`.env.example:4-38`) |
| `.pre-commit-config.yaml` | 70 | Commit hygiene and gitleaks secret scan; documents disabled ruff and deferred TS lint (`.pre-commit-config.yaml:12-55`) |
| `.gitignore` | 44 | Excludes secrets, runtimes, `call-logs/`, coverage, agent-local state (`.gitignore:1-44`) |
| `SECURITY.md` | 41 | Vulnerability reporting route, response targets, scope, disclosure rule (SECURITY.md:6-39) |
| `.editorconfig` / `.gitattributes` | 19 / 19 | Line-ending, charset, indent, and binary/generated classification (`.editorconfig:1-18`, `.gitattributes:1-18`) |
| `.nvmrc` / `.python-version` | 1 / 1 | Runtime pins: Node 20, Python 3.12 (`.nvmrc:1`, `.python-version:1`) |

## 7. Dependencies

No manifest (`package.json`, `requirements.txt`, `pyproject.toml`) is covered in the analyzed pages; the table below records only constraints stated verbatim there, required first.

| Package | Version constraint | Purpose |
|---|---|---|
| `getpatter` (npm) | `npm install getpatter` (no version string in analyzed pages, README.md:81-97) | TypeScript SDK distribution |
| `getpatter` (pip) | `pip install getpatter` (no version string in analyzed pages, README.md:99-115) | Python SDK distribution |
| Node.js | `20` (`.nvmrc:1`) | TypeScript runtime pin |
| Python | `3.12` (`.python-version:1`) | Python runtime pin |
| `pre-commit-hooks` | `v4.6.0` (`.pre-commit-config.yaml:41-55`) | Whitespace, EOF, YAML/JSON, large-file, debug-statement, private-key, line-ending hooks |
| `gitleaks` | `v8.18.4` (`.pre-commit-config.yaml:41-55`) | Secret scanning on every commit |
| `astral-sh/ruff-pre-commit` | `v0.6.9`, commented out (`.pre-commit-config.yaml:12-18`) | Disabled Python lint/format pending cleanup PR |
| Cloudflare quick tunnel | No version string (README.md:117) | Local webhook exposure when `tunnel: true` |
| Agent Skills bundle (`patterai/skills`) | Installed via `npx skills add patterai/skills` (README.md:67-75) | Coding-agent instructions; no version string in analyzed pages |

Provider SDKs and carrier APIs (OpenAI, Twilio, Deepgram, ElevenLabs, and others in section 4) carry no version constraints in the analyzed pages.

## 8. CLI / Usage Surface

Entry points (README.md:81-115, AGENTS.md:45-55):

| Entry | Form |
|---|---|
| TypeScript construct | `new Patter({ carrier: new Twilio(), phoneNumber: "+15550001234" })` (README.md:90-96) |
| TypeScript agent | `phone.agent({ engine: new OpenAIRealtime(), systemPrompt, firstMessage })` (README.md:90-96) |
| TypeScript serve | `await phone.serve({ agent, tunnel: true })` (README.md:90-96) |
| Python construct | `Patter(carrier=Twilio(), phone_number="+15550001234")` (README.md:108-114) |
| Python agent | `phone.agent(engine=OpenAIRealtime(), system_prompt=..., first_message=...)` (README.md:108-114) |
| Python serve | `await phone.serve(agent, tunnel=True)` (README.md:108-114) |
| Validation | `bash scripts/pr-validate.sh` (~3–5 min); `bash scripts/pr-validate.sh --quick` (~30 s) (AGENTS.md:38-41) |
| Template run | `git clone https://github.com/PatterAI/patter-inbound-agent`, `cp .env.example .env`, `pip install -r requirements.txt && python main.py` (README.md:141-145) |
| Skills install | `npx skills add patterai/skills` (README.md:67-75) |

Commands:

| Command | Effect |
|---|---|
| `getpatter telemetry disable` (README.md:123) | Disables anonymous usage telemetry via CLI |
| `pre-commit run --all-files` (`.pre-commit-config.yaml:5-8`) | Runs hygiene hooks plus gitleaks manually |

Env-var and config tables:

| Variable | Effect |
|---|---|
| `PATTER_TELEMETRY_DISABLED=1` (also honours `DO_NOT_TRACK=1`; auto-off in CI/tests) (README.md:123) | Disables telemetry via environment |
| `PATTER_TELEMETRY_DEBUG=1` (README.md:123) | Inspects telemetry payload without sending |
| `Patter(telemetry=False)` / `new Patter({ telemetry: false })` (README.md:123) | Disables telemetry via constructor |
| `TWILIO_*` / `TELNYX_*` / `PLIVO_*`, `OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`, `ANTHROPIC_API_KEY`, `WEBHOOK_URL`, `PORT` (`.env.example:9-38`) | Carrier, provider, webhook, and port configuration |

Templates (each a self-contained repo with Python and TypeScript, README.md:127-138): `patter-inbound-agent`, `patter-outbound-calls`, `patter-tool-calling`, `patter-custom-voice`, `patter-dynamic-variables`, `patter-custom-llm`, `patter-dashboard`, `patter-production`.

## 9. Extensibility Points

- New LLM/STT/TTS/realtime provider: add a provider adapter alongside the existing per-layer modules under `libraries/python/getpatter/providers/` or the TypeScript `src/` provider surface (layout per AGENTS.md:45-55), preserving the one-line swap convention (README.md:41).
- New carrier: add an adapter under `libraries/python/getpatter/telephony/` or `libraries/typescript/src/telephony/` (AGENTS.md:45-55) and expose it as a `Patter` carrier option with environment-variable credentials following the `.env.example:9-38` pattern.
- Custom voice pipeline: compose discrete STT and TTS providers (e.g. Deepgram plus ElevenLabs per the `patter-custom-voice` template, README.md:129-138) or bring a custom LLM via the `patter-custom-llm` template and pipeline `on_message` hook (`.env.example:9-38`).
- Tools, transfer, guardrails: extend the carrier-invariant tool/transfer/guardrail layer described in README.md:59 so behavior stays identical across Twilio, Telnyx, and Plivo.
- Observability: extend the vendor-neutral OpenTelemetry per-call trace (README.md:59) rather than adding carrier-specific logging.
- Any functional change must ship in both SDKs in the same PR with `snake_case` ↔ `camelCase` mapping, matching field order/defaults/error classes, a `CHANGELOG.md` entry under `## Unreleased`, and real-path tests mocking only the paid/external boundary (AGENTS.md:13-26).

## 10. Limitations and Gotchas

- **Analysis scope is README- and root-level only.** The analyzed pages cite `README.md` and nine root configuration/policy files; SDK internals under `libraries/` are named but not excerpted (AGENTS.md:45-55), so call-path internals, error handling, and concurrency behavior cannot be verified from this source set.
- **Python lint is disabled with known backlog.** `ruff`/`ruff-format` at `v0.6.9` is commented out because its first run produced 132 findings including 14 fixture/side-effect-import-breaking `F401` removals, pending a dedicated cleanup PR (`.pre-commit-config.yaml:12-18`); TypeScript lint is likewise deferred to CI (`.pre-commit-config.yaml:26-30`).
- **Dual-SDK parity is a per-PR tax.** Every feature must land in Python and TypeScript together with mapped naming, matching defaults/errors, changelog entry, and boundary-only-mocked tests, or CI/review blocks it (AGENTS.md:13-26); `snake_case`/`camelCase` drift and async-only I/O violations (`logging.getLogger("getpatter")`, never `print()`/bare `console.*`) are the explicitly called-out failure modes.
- **Local tunnel is not production.** `tunnel: true` uses a Cloudflare quick tunnel for development while production requires a static `webhook_url` or ngrok (README.md:117); webhook reliability, number provisioning, and recording/transfer behavior can differ between the two paths and across the three carriers despite the identical-tools claim (README.md:59, `.env.example:9-38`).
- **Carrier matrix has sharp edges.** Telnyx notes DTMF/transfer/recording specifics and Plivo notes WS audio streaming, mu-law 8 kHz, and V3 signatures in the credential template (`.env.example:9-38`); one-line carrier swaps (README.md:79) still require re-verifying audio format, transfer, and recording paths.
- **Telemetry defaults to on.** Collection of SDK version and bucketed provider/model and call facts is opt-out, not opt-in; disabling requires constructor flag, CLI command, or `PATTER_TELEMETRY_DISABLED=1`/`DO_NOT_TRACK=1` (README.md:121-123).

## 11. How It Compares to Alternatives

- **Vapi:** hosted voice-agent platform with managed infrastructure and per-minute pricing; Patter positions the SDK as self-hosted code the builder runs, trading managed operations for layer-by-layer provider choice and carrier portability.
- **Retell AI:** hosted low-latency voice API with managed telephony; Patter keeps the agent loop and media path inside the builder's process and makes tools, transfer, guardrails, and OpenTelemetry traces carrier-invariant (README.md:59) rather than platform-defined.
- **Twilio Programmable Voice / Telnyx / Plivo used directly:** carrier APIs plus separately integrated STT/LLM/TTS; Patter sits above exactly these carriers (README.md:50-57) and standardizes tools, transfer, and tracing across them, at the cost of adopting its dual-SDK parity and contribution constraints (AGENTS.md:13-26).
- **LiveKit Agents / Pipecat:** open-source realtime media frameworks with pipeline composition; Patter overlaps on Realtime/Pipeline/Hybrid composition and provider swapping (README.md:46) but is telephone-number-centric, with carrier provisioning, tunnel-to-production serving, and call templates as the primary surface (README.md:79-145).

Positioning: Patter is the telephone-number-first, self-hosted alternative for builders who accept a two-SDK contribution contract in exchange for owning every swappable layer between the agent and the phone network.

## Appendix: Selected Code Snippets

TypeScript quickstart (README.md:81-97):

```typescript
import { Patter, Twilio, OpenAIRealtime } from "getpatter";

const phone = new Patter({ carrier: new Twilio(), phoneNumber: "+15550001234" });
const agent = phone.agent({
  engine: new OpenAIRealtime(),
  systemPrompt: "You are a friendly receptionist for Acme Corp.",
  firstMessage: "Hello! How can I help?",
});
await phone.serve({ agent, tunnel: true });
```

Python quickstart (README.md:99-115):

```python
from getpatter import Patter, Twilio, OpenAIRealtime

phone = Patter(carrier=Twilio(), phone_number="+15550001234")
agent = phone.agent(
    engine=OpenAIRealtime(),
    system_prompt="You are a friendly receptionist for Acme Corp.",
    first_message="Hello! How can I help?",
)
await phone.serve(agent, tunnel=True)
```

Editor and Git baseline (`.editorconfig:1-18`):

```
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.{md,mdx}]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

PR validation contract (AGENTS.md:38-41):

```bash
bash scripts/pr-validate.sh          # mirrors PR-blocking CI (~3-5 min)
bash scripts/pr-validate.sh --quick  # pre-commit + lint (~30 s)
```
