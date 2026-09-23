> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Forced End-of-Utterance for Voice Agent Latency
**In one sentence:** Conversational voice agents suffer multi-second silence-buffer latency waiting for the speech detector to finalize transcripts, and Speechmatics' force end-of-utterance message lets you decisively trigger finalization in under 250 milliseconds.
## Key points
- Voice-agent turn-taking stalls for "a couple of seconds" after the user stops speaking, breaking conversational flow.
- Traditional endpointing waits for a detected period of silence plus a silence buffer before finalizing the transcript, and only then can the LLM response begin.
- Silence-based finalization is acceptable for notetaking and captions but too slow and indecisive for conversational voice agents.
- Sending a force end-of-utterance message tells the server "I'm done talking. Give me the finalized transcript," bypassing the silence wait.
- Any turn-detection signal — VAD, push-to-talk, or in the demo a 3D-printed big red button — can trigger the force end-of-utterance message via a simple script call.
- The demo visualization shows partial transcripts still processing at the top and finalized transcripts with forced end-of-utterance at the bottom, with final results returned in under 250 milliseconds.
- The feature is available in the Speechmatics voice SDK as well as the real-time API and real-time SDK, covering high-level and low-level integrations, with Pipecat and LiveKit support coming soon.
---
## The latency problem
**Covers:** silence-buffer/VAD end-of-turn latency problem

| Mechanism | Behavior |
|---|---|
| Traditional speech detection | Waits for a detected period of silence plus a silence buffer until the user has finished talking |
| Transcript finalization | System finalizes the transcript only after silence is detected, before any LLM response can start |
| User impact | "Nothing for a couple of seconds," which "can kill the flow of conversation and make it feel weird" |
| Fit | "Fine for notetaking and captions" but conversational voice agents "need something faster and more decisive" |

## Forced end-of-utterance
**Covers:** Speechmatics force-end-of-utterance trigger (button/VAD/push-to-talk), sub-250ms finalized transcripts and SDK/Pipecat/LiveKit availability

| Item | Detail |
|---|---|
| Feature | Speechmatics force end of utterance — "take control and remove that awkward latency" |
| Usage | "As simple as calling force end of utterance"; sending the message means "I'm done talking. Give me the finalized transcript" |
| Triggers | "You can hook up any one of your turn detection models, like VAD or Push-to-talk"; demo uses a "3D printed this big red button" |
| Visualization | "Partial transcripts still being processed at the top, with finalized transcripts and forced end of utterance at the bottom"; pressing the button makes "the server will immediately give us the final transcript" |
| Demo utterances | "Hi, there. Could you book me a table for two tonight at 7 p.m., please?" and "Remind me to check the oven in 15 minutes" |
| Latency | Final result back "in under 250 milliseconds" |
| Availability | "Available in the Speechmatics voice SDK as well as a real-time API and real-time SDK"; "coming soon to voice agent frameworks like Pipecat and LiveKit" |
