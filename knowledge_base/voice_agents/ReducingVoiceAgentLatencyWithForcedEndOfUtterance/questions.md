---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Reducing Voice Agent Latency with Forced End-of-Utterance

### Q1. Why does a conversational voice agent stall for "a couple of seconds" after the user stops speaking?
> [!tip]- Answer
> Traditional endpointing waits for a detected period of silence plus a silence buffer before it decides the user has finished talking. The transcript is finalized only after that silence wait, so the LLM response cannot begin until the wait completes. See [[wiki/01-forced-end-of-utterance-latency|The latency problem]].

### Q2. Why is silence-based finalization fine for notetaking and captions but wrong for conversational voice agents?
> [!tip]- Answer
> Notetaking and captions only need an accurate record, so waiting out the silence buffer is acceptable. Conversational agents need fast, decisive turn-taking, and multi-second gaps kill the flow and make the interaction feel weird. See [[wiki/01-forced-end-of-utterance-latency|The latency problem]].

### Q3. What does sending a force end-of-utterance message do, and what latency does it achieve?
> [!tip]- Answer
> It tells the server "I'm done talking. Give me the finalized transcript," bypassing the silence wait entirely. The server immediately returns the final transcript, with the demo showing the final result back in under 250 milliseconds. See [[wiki/01-forced-end-of-utterance-latency|Forced end-of-utterance]].

### Q4. What signals can trigger forced end-of-utterance, and what did the demo use?
> [!tip]- Answer
> Any turn-detection signal can trigger it, such as a VAD model or push-to-talk, via a simple script call. The demo used a 3D-printed big red button as a stand-in trigger so pressing it forced immediate finalization. See [[wiki/01-forced-end-of-utterance-latency|Forced end-of-utterance]].

### Q5. What does the demo visualization show, and which utterances does it use?
> [!tip]- Answer
> Partial transcripts still being processed appear at the top, while finalized transcripts with forced end-of-utterance appear at the bottom. The demo utterances are "Hi, there. Could you book me a table for two tonight at 7 p.m., please?" and "Remind me to check the oven in 15 minutes." See [[wiki/01-forced-end-of-utterance-latency|Forced end-of-utterance]].

### Q6. Where is forced end-of-utterance available, and what framework support is coming?
> [!tip]- Answer
> It is available in the Speechmatics voice SDK as well as the real-time API and real-time SDK, covering high-level and low-level integrations. Support for voice agent frameworks like Pipecat and LiveKit is coming soon. See [[wiki/01-forced-end-of-utterance-latency|Forced end-of-utterance]].

### Q7. Evaluation: a team proposes relying on a shorter silence buffer alone instead of wiring a turn-detection signal to forced end-of-utterance — would you recommend this?
> [!tip]- Answer
> No, prefer forced end-of-utterance driven by an explicit turn signal, since a shorter silence buffer still guesses from silence and risks cutting users off or lagging on pauses. An explicit VAD or push-to-talk trigger decisively finalizes the transcript in under 250 milliseconds without the silence-wait tradeoff. See [[wiki/01-forced-end-of-utterance-latency|Forced end-of-utterance]].
