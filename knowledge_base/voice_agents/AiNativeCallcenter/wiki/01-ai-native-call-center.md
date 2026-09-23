[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# AI Native Call Center
**In one sentence:** An open-source call center where a voice model is the default answerer over a speech-to-speech connection, steered by a flow engine and handing over to human agents in FreeSWITCH queues when needed, all inside one Go binary plus PostgreSQL and FreeSWITCH with one unified call record.
## Key points
- Calls arrive at FreeSWITCH and are answered by a voice model over a speech-to-speech connection the application terminates itself, with audio passed straight to the provider (G.711 byte-for-byte where accepted, no decode/resample).
- The model owns the dialogue while the flow owns the phase: phases carry instructions plus a tool list, transitions fire on tool results, and built-in tools may *refuse* (e.g. "the queue is closed" is conversational, not an error).
- Handover goes into `mod_callcenter` queues; the agent screen pops via a `PARTY_RINGING` SSE event with `userData` before the phone rings, and the bot-phase transcript is already present because the call id is minted before any leg exists.
- Agents work in the browser (presence, call control, callbacks) but audio belongs to the separate `web-sip-phone` Chrome extension, which holds the SIP registration with credentials issued at sign-in and has no dialpad — control is via REST carried over ESL `uuid_phone_event`.
- One conversation is one CDR with one transcript and one recording (not three fragments); recordings go to filesystem or any S3-compatible store.
- One provider answers every call per deployment, chosen at startup: `qwen`/`doubao` inside mainland China, `openai`/`gemini` elsewhere, or `gateway`; call language never selects the provider.
- The stack is one Go binary (REST API, event stream, embedded web UI) plus PostgreSQL and FreeSWITCH; FreeSWITCH reads its directory and queues from the database via Lua, with a static XML dialplan delegating to Lua lookups.
---
## Try it
**Covers:** AI-native call center overview: model-first answering, flow engine, human handover, single Go binary + FreeSWITCH architecture

Deploy via `git clone https://github.com/rasonyang/ai-native-callcenter`, `cp .env.example .env` (two lines: `FS_EXTERNAL_IP` and `ALIYUN_API_KEY`), `docker compose up -d` in `deploy/`. First start builds the app (minutes); later starts take seconds. Open `http://<host>:8080`, sign in as `admin` / `aicc@123` (every password is `aicc@123`). Seeded with a team, two queues, six published bilingual flows (each behind English, Chinese, and US numbers; main line 800-555-0199), eighteen simulated customer telephones, and a week of history.

## What it does

Answers with a model, not a menu: the AI leg is a SIP endpoint inside the application; FreeSWITCH bridges the caller to it.

Steers without scripting: a phase may carry its own line (greeting, hand-over script, goodbye) spoken as written — "`doubao` is handed the words to speak, the other four providers are instructed to repeat them word for word." Persona, rules, and voice are published and versioned together.

Bilingual with explicit provider choice: English and Chinese throughout; three providers are profiles of one protocol while `doubao` and `gemini` each speak a different one with their own client.

## How it fits together

```
                    ┌──────────── one Go binary ────────────┐
  caller ──▶ FreeSWITCH ──▶ SIP UAS ──▶ provider (Realtime, speech-to-speech)
                 │            │
                 │            └─ flow engine: phases, tools, transfers
                 │
                 ├─ mod_callcenter queues ──▶ agents (browser + web-sip-phone)
                 │
                 └─ ESL ──▶ call registry ──▶ REST + SSE ──▶ web interface
                                                    │
                                              PostgreSQL
```

Design notes:

| Note | Detail |
|---|---|
| Domain model | Genesys-lineage: a **call** aggregates **parties**; leg events are `PARTY_*`, call-scoped ones are `CALL_*` |
| Concurrency | Every live call is an actor — one goroutine as sole mutator, snapshots by mailbox; nothing in `internal/telephony` locks call state; AI leg excepted (mutexes over playback/recording state shared by its goroutines) |
| Switch config | Dialplan is static XML deciding nothing alone; each rule hands to a Lua script; adding extension/queue/number is a database change |

Full design in `docs/design/`, starting with `00-overview.md`.

## Building

```sh
make dev-up            # PostgreSQL in Docker
cd web && npm install && npm run build && cd ..
make build             # bin/aicc, with the interface embedded
./bin/aicc useradd -username admin -password '…' -role ADMIN
./bin/aicc
```

Frontend work: `make web-dev` runs Vite on 5173 against API on 8080. Checks: `go test -race ./...` ("always -race; it has caught real bugs here"), `make lint` (go vet, gofmt, oxlint), `make api-check` (API contract gate). HTTP API is spec-first: `docs/openapi.json` is the single source of truth; Go server and TypeScript client are generated from it — "Edit the contract, run `make api-generate`, then implement. Never the other way round."

## Extending it

| Extension | Mechanism |
|---|---|
| New voice provider | A profile, not a client (`docs/provider-extension.md`) |
| New flow | A JSON document validated at load (see `internal/seed/flows/` for a working bilingual one) |
| New screen | Follow the design system in `web/CLAUDE.md`, binding rather than advisory |
| External integration | A service behind the flow's backend URL, never code in this tree |

## Status and license

Human path, AI path, product surface, and packaging are built and verified against live FreeSWITCH and live providers. Performance is not yet claimed: capacity budget and latency target exist (design 06) plus an in-repo load-test harness (`docs/load-tests.md`), but "the benchmark campaign itself is still to come, so treat the budget as an intention rather than a measurement." Deliberately absent and staying so: "any cascaded ASR + LLM + TTS pipeline inside this process." License: Apache-2.0.
