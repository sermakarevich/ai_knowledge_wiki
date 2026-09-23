> [[index|Wiki]] | [[summary|Summary]]
# Reducing Voice Agent Latency with Forced End-of-Utterance — Digest

## 1. [[wiki/01-forced-end-of-utterance-latency|Forced End-of-Utterance for Voice Agent Latency]]
**In one sentence:** Conversational voice agents suffer multi-second silence-buffer latency waiting for the speech detector to finalize transcripts, and Speechmatics' force end-of-utterance message lets you decisively trigger finalization in under 250 milliseconds.
## Key points
- Voice-agent turn-taking stalls for "a couple of seconds" after the user stops speaking, breaking conversational flow.
- Traditional endpointing waits for a detected period of silence plus a silence buffer before finalizing the transcript, and only then can the LLM response begin.
- Silence-based finalization is acceptable for notetaking and captions but too slow and indecisive for conversational voice agents.
- Sending a force end-of-utterance message tells the server "I'm done talking. Give me the finalized transcript," bypassing the silence wait.
- Any turn-detection signal — VAD, push-to-talk, or in the demo a 3D-printed big red button — can trigger the force end-of-utterance message via a simple script call.
- The demo visualization shows partial transcripts still processing at the top and finalized transcripts with forced end-of-utterance at the bottom, with final results returned in under 250 milliseconds.
- The feature is available in the Speechmatics voice SDK as well as the real-time API and real-time SDK, covering high-level and low-level integrations, with Pipecat and LiveKit support coming soon.

## The argument in five moves
1. Conversational voice agents stall for a couple of seconds after the user stops speaking, killing conversational flow.
2. The stall comes from traditional endpointing, which waits for a silence period plus a silence buffer before finalizing the transcript that the LLM response depends on.
3. Silence-based finalization is fine for notetaking and captions but too slow and indecisive for conversational agents, which need something faster and more decisive.
4. The force end-of-utterance message takes control: any turn-detection signal (VAD, push-to-talk, button) triggers it, telling the server "I'm done talking. Give me the finalized transcript" and bypassing the silence wait.
5. The demo proves it out — partial transcripts on top, forced finalized transcripts at the bottom, final result back in under 250 milliseconds — and the feature ships in the voice SDK, real-time API, and real-time SDK, with Pipecat and LiveKit support coming soon.
