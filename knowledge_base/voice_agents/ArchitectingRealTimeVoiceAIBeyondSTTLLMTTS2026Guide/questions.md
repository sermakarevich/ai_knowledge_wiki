---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Architecting Real-Time Voice AI: Beyond STT-LLM-TTS (2026 Guide)

### Q1. Why does the guide insist voice AI is a turn-taking problem rather than a transcription problem?
> [!tip]- Answer
> The guide rejects the idea that voice AI is just a microphone plugged into an LLM with a speaker on the other end, because the hard part is orchestration: latency, interruption handling, and conversational timing. A better model or cleaner transcript alone cannot fix an agent that answers too slowly, talks over thinking pauses, or collapses when interrupted. See [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]].

### Q2. How do the sequential and streaming architectures differ, and what latency budget forces the streaming choice?
> [!tip]- Answer
> The historical sequential pattern runs full STT, then the complete LLM response, then whole-audio TTS synthesis, with playback only at the end — agonizingly slow against human timing. The modern streaming pattern overlaps everything incrementally over a single persistent websocket, which is far more responsive but much harder to build. It is forced by the budget: a natural 200–300 ms inter-speaker gap, over-500 ms feeling slow and robotic, and abandonment around 3 seconds. See [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]].

### Q3. How does streaming STT work, and why must downstream logic act only on final transcripts?
> [!tip]- Answer
> Audio streams over a persistent websocket in tiny 50 ms chunks, emitting revisable partial transcripts for live feedback plus confident final transcripts. Partials keep the system feeling alive while the user speaks, but acting on them is dangerous — for example, firing a database lookup on a partial order-number guess means one misheard digit breaks everything. See [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]].

### Q4. What are the two turn-detection thresholds, and how would you tune them for fast versus deliberate speech?
> [!tip]- Answer
> The minimum silence threshold (~600 ms) ends the turn only if STT also judges the sentence semantically complete, letting brief thinking pauses pass without rude interruption. The maximum silence ceiling (~1,500 ms) is a hard stop that makes the AI respond even mid-sentence. Drop the minimum toward 300 ms for fast-paced customer service, or raise the ceiling toward 2,500 ms for deliberate-speech contexts like healthcare. See [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]].

### Q5. What is sentence-level LLM handoff, and what three signals guard barge-in against false positives?
> [!tip]- Answer
> Instead of token-by-token streaming, each complete sentence is yielded to TTS at its boundary (period or question mark), so the agent audibly speaks the first sentence while the LLM still generates the rest. True barge-in then requires stopping playback and generation instantly only when three signals agree: an energy threshold (−45 to −35 dBFS), voice classification as real human speech (e.g., Solero or WebRTC VAD, not a slamming door), and 200–300 ms sustained duration. See [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]].

### Q6. Why does tool calling need a voice-specific design, and how do the preamble and buffering patterns mask backend latency?
> [!tip]- Answer
> A 3-second database or booking lookup is invisible in text chat but is dead air on a live call, where users assume the call dropped, start talking again, and derail everything. The preamble technique has the model audibly narrate before firing the tool ("Let me check that for you"), masking latency with natural filler. Results are buffered mid-turn and flushed only on clean completion, discarded entirely on interruption so a stale confirmation code never answers a question no longer being asked. See [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]].

### Q7. Evaluation: a team proposes shipping a sequential STT-LLM-TTS pipeline with a stronger LLM to "fix" their slow voice agent — should they, and what should they build instead?
> [!tip]- Answer
> They should not ship it, because a stronger LLM leaves the real bottleneck untouched: the sequential pattern cannot meet the sub-500 ms budget, has no tuned turn detection or barge-in guards, and strands tool-call latency as dead air. They should instead invest in the streaming blueprint — 50 ms partial/final STT, 600 ms/1,500 ms turn detection, sentence-level handoff, three-signal barge-in, and preamble plus buffer-or-discard tool calling over one websocket — accepting higher build complexity for a genuinely conversational agent. See [[wiki/01-overview|Welcome to the Explainer: Real-Time Voice AI Beyond STT-LLM-TTS]].
