> [[index|Wiki]] | [[summary|Summary]]

# Architecting Real-Time Voice AI: Beyond STT-LLM-TTS (2026 Guide) — Digest

## 1. [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]]

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

## The argument in five moves

1. Voice AI is a turn-taking and orchestration problem — latency, interruptions, timing — not a transcription or model problem, so the historical sequential pattern (full STT → full LLM → full TTS, then playback) fails human timing.
2. The bar is the human conversational gap (200–300 ms) with a sub-500 ms response budget and abandonment around 3 seconds, which forces the modern streaming pattern where data streams and overlaps incrementally over a single persistent websocket.
3. Liveness comes from streaming STT in 50 ms chunks — partials for aliveness, finals for action — paired with tuned turn detection (~600 ms minimum gated on semantic completeness, ~1,500 ms maximum hard stop) so pauses don't trigger rude interruptions.
4. Responsiveness is compounded by sentence-level LLM handoff (speak the first sentence while the rest generates) guarded by true barge-in (energy + voice classification + duration) that stops playback and generation instantly without false positives from noise.
5. Backend latency is masked, not eliminated: voice-optimized tool calling narrates actions aloud before firing the tool and buffers results mid-turn, discarding them on interruption so stale answers never land in a changed conversation.
