> [[index|Wiki]] | [[summary|Summary]]
# AI Native Call Center — Digest
## 1. [[wiki/01-ai-native-call-center|AI Native Call Center]]
**In one sentence:** An open-source call center where a voice model is the default answerer over a speech-to-speech connection, steered by a flow engine and handing over to human agents in FreeSWITCH queues when needed, all inside one Go binary plus PostgreSQL and FreeSWITCH with one unified call record.
## Key points
- Calls arrive at FreeSWITCH and are answered by a voice model over a speech-to-speech connection the application terminates itself, with audio passed straight to the provider (G.711 byte-for-byte where accepted, no decode/resample).
- The model owns the dialogue while the flow owns the phase: phases carry instructions plus a tool list, transitions fire on tool results, and built-in tools may *refuse* (e.g. "the queue is closed" is conversational, not an error).
- Handover goes into `mod_callcenter` queues; the agent screen pops via a `PARTY_RINGING` SSE event with `userData` before the phone rings, and the bot-phase transcript is already present because the call id is minted before any leg exists.
- Agents work in the browser (presence, call control, callbacks) but audio belongs to the separate `web-sip-phone` Chrome extension, which holds the SIP registration with credentials issued at sign-in and has no dialpad — control is via REST carried over ESL `uuid_phone_event`.
- One conversation is one CDR with one transcript and one recording (not three fragments); recordings go to filesystem or any S3-compatible store.
- One provider answers every call per deployment, chosen at startup: `qwen`/`doubao` inside mainland China, `openai`/`gemini` elsewhere, or `gateway`; call language never selects the provider.
- The stack is one Go binary (REST API, event stream, embedded web UI) plus PostgreSQL and FreeSWITCH; FreeSWITCH reads its directory and queues from the database via Lua, with a static XML dialplan delegating to Lua lookups.
## The argument in five moves
1. Answer every call with a voice model by default, terminating the speech-to-speech provider connection inside the application with audio passed straight through.
2. Steer the dialogue without scripting it: the model owns the words while the flow owns the phase, with phase instructions, tool lists, and tool-result transitions plus conversational refusals.
3. Hand over to humans through real FreeSWITCH `mod_callcenter` queues, with the agent screen popping before the phone rings and the bot-phase transcript already present.
4. Keep one conversation unified as one CDR with one transcript and one recording, served by one Go binary plus PostgreSQL and FreeSWITCH with a database-driven switch configuration.
5. Ship a single provider per deployment chosen at startup plus a reproducible path from docker compose seed to spec-first building and extension without any cascaded ASR + LLM + TTS pipeline.
