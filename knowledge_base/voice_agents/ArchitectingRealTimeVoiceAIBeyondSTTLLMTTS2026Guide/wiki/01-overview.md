> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS
**In one sentence:** Real-time voice AI is a turn-taking orchestration problem — not just STT-LLM-TTS plumbing — won only by a streaming architecture that hits a sub-500 ms latency budget via streaming STT, tuned turn detection, sentence-level LLM handoff, guarded barge-in, and voice-optimized tool calling over a single persistent websocket.
## Key points
- Voice is a turn-taking and orchestration problem (latency, interruptions, timing), not a transcription or prompt/model problem.
- The historical sequential pattern (full STT → full LLM → full TTS, then playback) is agonizingly slow and cannot meet human timing.
- The modern production standard is the streaming pattern, where data streams and overlaps incrementally for responsiveness at much higher build complexity.
- Human conversation has a 200–300 ms natural inter-speaker gap; any response delay over 500 ms feels noticeably slow/robotic, and around 3 seconds users abandon, assuming the system is broken or the call dropped.
- Streaming STT processes audio in tiny 50 ms chunks over a persistent websocket, emitting revisable partial transcripts for liveness while downstream logic acts only on final transcripts.
- Turn detection uses audio silence patterns with two tunable numbers: ~600 ms minimum silence (only ends turn if STT judges the sentence semantically complete) and ~1,500 ms maximum silence ceiling (hard stop even if unfinished).
- Sentence-level LLM handoff yields each complete sentence (period/question mark boundary) immediately to TTS, so the agent speaks the first sentence while the LLM still generates the rest.
- True barge-in requires a three-signal check (energy + voice classification + duration) and voice-optimized tool calling uses a preamble narration plus result buffering/discarding on interruption to mask backend latency without injecting stale results.
---
## The core illusion
**Covers:** chunk 01 intro framing

> "Voice is a turn-taking problem, not a transcription problem."

The chunk opens by rejecting the idea that voice AI is just "plugging a microphone into an LLM and strapping a speaker to the other end." The hard part is orchestration: latency, handling interruptions, and timing the conversational back-and-forth.

## Sequential vs. streaming architecture
**Covers:** chunk 01 architecture history

| Pattern | How it works | Trade-off |
|---|---|---|
| Sequential (historical) | Speak → full STT transcription → complete LLM text response → whole-audio TTS synthesis → only then playback | Agonizingly slow; cannot meet the latency budget |
| Streaming (modern production standard) | Everything happens incrementally; data streams and overlaps continuously | Incredibly responsive but much harder to build |

## The latency budget
**Covers:** chunk 01 timing constraints

| Metric | Value from chunk |
|---|---|
| Natural human gap between speakers | 200–300 ms |
| Budget for response delay | Sub-500 ms; over 500 ms feels noticeably slow/robotic |
| Abandonment point | ~3 seconds: users assume the system is broken / a cellular dead zone and hang up before the AI formulates its first thought |

## Component 1 — Streaming speech-to-text
**Covers:** chunk 01, component one

- Persistent websocket connection; audio processed in tiny 50-millisecond chunks.
- Two event types: partial transcripts (live continuous feedback, constantly revised best guess while the user speaks) and final transcripts.
- Rule: use partials so the system feels alive, but act only on the final confident result — e.g., never fire a database lookup on a partial guess of an order number, since one misspoken digit breaks everything.

## Component 2 — Turn detection
**Covers:** chunk 01, component two

| Control | Value in chunk | Behavior |
|---|---|---|
| Minimum silence threshold | Commonly ~600 ms | Ends the turn only if STT also thinks the sentence is semantically complete; lets users take brief thinking pauses without rude interruption |
| Maximum silence ceiling | Often ~1,500 ms | Hard stop: AI responds even if the sentence sounds unfinished |

Tuning examples from the chunk: drop the minimum to 300 ms for fast-paced customer service; raise the ceiling to 2,500 ms for deliberate-speech contexts like healthcare.

## Component 3 — Sentence-level LLM handoff
**Covers:** chunk 01, component three

Not raw token-by-token handoff: the handoff unit is a complete sentence. The instant a sentence boundary (period or question mark) appears in the accumulating buffer, that whole sentence is yielded directly to TTS, so the AI starts audibly speaking the first sentence while the LLM generates the rest in the background.

## Component 4 — Barge-in handling
**Covers:** chunk 01, component four

On user interruption: stop playback and cancel text generation instantly, but without false positives from background noise.

| Signal | Requirement in chunk |
|---|---|
| 1. Energy threshold | −45 to −35 dB full scale (dBFS) volume |
| 2. Voice classification | Must be actual human voice, e.g., Solero or WebRTC VAD models distinguishing speech from a slamming door |
| 3. Minimum duration | 200–300 ms sustained duration guard |

Why the duration guard matters: a single loud cough might pass volume and voice checks, but because it does not sustain for 200 ms it is blocked from triggering a false barge-in.

## Component 5 — Voice-optimized tool calling
**Covers:** chunk 01, component five

- Problem: a 3-second database/booking lookup is invisible in text chat but is dead air on a live call — users assume the call dropped, start talking again, and everything derails.
- Preamble technique: explicitly instruct the model to audibly narrate actions before firing the tool, e.g. "Let me check that for you." or "Just one moment while I pull that up.", masking backend latency with natural filler.
- Result buffering pattern: accumulate tool results mid-turn, flush downstream on clean completion, but discard completely if the user interrupted — sending stale results (e.g., an old confirmation code) into a changed conversation answers a question no longer being asked.

## Blueprint recap
**Covers:** chunk 01 closing

All five components — streaming STT, precise turn detection, sentence-level handoff, robust barge-in guards, and buffered tool calling — orchestrated over a single persistent websocket connection elevate the experience from a clunky robotic phone tree to a responsive conversational partner, closing with the provocation that an agent hitting sub-500 ms while handling interruptions, thinking pauses, and tool fetches may be "a better listener than most humans."

**Covers:** chunk 01-welcome-to-the-explainer-today-we-re (video intro framing real-time voice AI beyond STT-LLM-TTS)
