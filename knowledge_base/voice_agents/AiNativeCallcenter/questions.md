---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: AI Native Call Center

### Q1. What does "AI-native" mean in this call center, and where does the speech-to-speech connection terminate?
> [!tip]- Answer
> It means a voice model answers every call by default instead of a menu or agent-first routing. FreeSWITCH bridges the caller to a SIP endpoint inside the application, which terminates the provider speech-to-speech connection itself and passes audio straight through (G.711 byte-for-byte where accepted, no decode/resample). See [[wiki/01-ai-native-call-center|AI Native Call Center]].

### Q2. How does the flow engine steer the dialogue without scripting it?
> [!tip]- Answer
> The model owns the words while the flow owns the phase: each phase carries instructions plus a tool list, and transitions fire on tool results. Built-in tools may refuse rather than error — e.g. "the queue is closed" is handed back as something conversational, not a failure. See [[wiki/01-ai-native-call-center|AI Native Call Center]].

### Q3. How does handover to a human agent work, and what does the agent see before the phone rings?
> [!tip]- Answer
> The caller is transferred into real FreeSWITCH `mod_callcenter` queues where agents wait. The agent screen pops via a `PARTY_RINGING` SSE event carrying `userData` before the phone rings, and the bot-phase transcript is already present because the call id is minted before any leg exists. See [[wiki/01-ai-native-call-center|AI Native Call Center]].

### Q4. Why is agent audio in a separate Chrome extension instead of the browser UI?
> [!tip]- Answer
> Agents work in the browser for presence, call control, and callbacks, but audio belongs to the separate `web-sip-phone` extension, which holds the SIP registration with credentials issued at sign-in. The extension has no dialpad — call control is via REST carried over ESL `uuid_phone_event`. See [[wiki/01-ai-native-call-center|AI Native Call Center]].

### Q5. What does "one conversation is one CDR" mean, and how is the voice provider chosen?
> [!tip]- Answer
> The bot leg, queue wait, and agent leg stay one call with one transcript and one recording (not three fragments), with recordings stored on the filesystem or any S3-compatible store. One provider serves every call per deployment, chosen at startup — `qwen`/`doubao` inside mainland China, `openai`/`gemini` elsewhere, or `gateway` — and call language never selects the provider. See [[wiki/01-ai-native-call-center|AI Native Call Center]].

### Q6. What are the key architecture and contributor-contract rules of the project?
> [!tip]- Answer
> The stack is one Go binary (REST API, event stream, embedded web UI) plus PostgreSQL and FreeSWITCH, which reads its directory and queues from the database via Lua behind a static XML dialplan. Every live call is an actor with one goroutine as sole mutator, and the HTTP API is spec-first: `docs/openapi.json` is the single source of truth, so contributors edit the contract and run `make api-generate` before implementing, with `go test -race ./...` and `make api-check` as gates. See [[wiki/01-ai-native-call-center|AI Native Call Center]].

### Q7. Would you recommend deploying this project for a performance-sensitive production call center today, and why?
> [!tip]- Answer
> Not yet for performance-sensitive production: the human path, AI path, product surface, and packaging are verified against live FreeSWITCH and live providers, but capacity and latency targets exist only as design intentions with the benchmark campaign still to come. It suits a team that wants the AI-first, single-record handover model and accepts the one-Go-binary plus FreeSWITCH/PostgreSQL footprint while waiting on performance validation. See [[wiki/01-ai-native-call-center|AI Native Call Center]].
