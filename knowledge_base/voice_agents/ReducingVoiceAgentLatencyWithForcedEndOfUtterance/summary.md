# Reducing Voice Agent Latency with Forced End-of-Utterance

**Video:** [Reducing Voice Agent Latency with Forced End-of-Utterance](https://www.youtube.com/watch?v=pbQ1NwdQVLc) — Speechmatics

## Human Readable TL;DR

Talking to most voice agents today feels like using a walkie-talkie with a long, awkward pause, because after you finish speaking the system keeps listening just to make sure you are really done. This video shows a way to skip that waiting game by telling the speech recognizer directly that the speaker has finished, much like raising your hand or ringing a doorbell instead of waiting to be noticed. In the demo this is done with a big red button, but in practice any signal such as voice activity detection or push-to-talk can play the same role. The result is a finalized transcript in under a quarter of a second, so the conversation keeps flowing instead of stalling for a couple of seconds after every turn.

## TL;DR

Conversational voice agents built on streaming speech recognition stall because traditional endpointing only finalizes a transcript after detecting a period of silence plus a silence buffer, which leaves a couple of seconds of dead air before the language model can even start responding. The video presents Speechmatics' force end-of-utterance message as a decisive alternative: the client tells the server the utterance is complete and the server immediately returns the finalized transcript, reportedly in under 250 milliseconds. Any turn-detection signal, from voice activity detection to push-to-talk, can trigger the message with a simple script call, and the feature is available in the Speechmatics voice SDK as well as the real-time API and real-time SDK, with support for agent frameworks such as Pipecat and LiveKit on the way.

---

## Problem & Motivation

The core problem is turn-taking latency in conversational voice agents. Traditional speech detection waits for a detected period of silence plus an additional silence buffer before deciding the user has finished talking, and only after that wait does transcript finalization happen and the downstream language-model response begin. From the user's perspective this shows up as nothing happening for a couple of seconds after they stop speaking, which breaks the flow of conversation and makes the interaction feel strange and unnatural. While this cautious, silence-based approach is perfectly fine for notetaking and captions, where a short delay barely matters, conversational agents need something faster and more decisive, since every extra beat of silence erodes the feeling of talking to a responsive partner. The motivation is therefore to take control of endpointing and remove that awkward latency rather than passively waiting out the silence buffer.

## Main Original Ideas

1. **Forced end-of-utterance as explicit finalization control.** Rather than letting the server infer the end of a turn from silence alone, the client sends an explicit force end-of-utterance message that means, in effect, the speaker is done talking and the finalized transcript should be returned right away. This turns endpointing from a passive waiting process into an active decision, bypassing the silence wait entirely and letting the rest of the agent pipeline start immediately.

2. **Pluggable turn-detection triggers.** The forced-finalization message is decoupled from any single detector, so it can be hooked up to whatever turn-detection signal a builder prefers, including voice activity detection models or push-to-talk. The video dramatizes this flexibility with a 3D-printed big red button wired through a simple script call, making the point that endpointing becomes whatever event the application trusts as the end of the user's turn rather than a fixed server-side silence threshold.

3. **Streaming UX with partials on top and forced finals below.** The demo visualizes the interaction as partial transcripts still being processed at the top and finalized transcripts with forced end-of-utterance at the bottom, so viewers can see the moment the button press converts an in-progress hypothesis into an immediate final result. This framing presents forced finalization as a small, composable primitive inside the existing streaming pipeline rather than a separate recognition mode, available consistently across the high-level voice SDK and the lower-level real-time API and real-time SDK.

## Key Findings

The central result demonstrated is speed: pressing the trigger makes the server immediately return the final transcript, with the final result coming back in under 250 milliseconds instead of after a multi-second silence wait. The mechanism is also deliberately simple to adopt, described as as simple as calling force end of utterance, so builders can wire it to an existing voice activity detector, a push-to-talk control, or a custom signal with minimal integration work. The demo utterances, including a restaurant booking request and a spoken reminder, illustrate ordinary conversational turns where that saved delay directly determines whether the exchange feels fluid or stilted. Availability is broad within the Speechmatics ecosystem, covering the voice SDK for high-level integration alongside the real-time API and real-time SDK for lower-level control, which means teams at different layers of the stack can use the same finalization primitive.

## Suggestions & Future Directions

The clearest direction stated in the material is expansion into popular voice-agent frameworks, with support for Pipecat and LiveKit described as coming soon, so builders working in those ecosystems can use forced end-of-utterance without dropping down to raw API calls. More broadly, the decoupled trigger design invites experimentation with smarter turn-taking signals, since any detector the builder trusts can become the event that finalizes the transcript. This points toward agents that combine fast acoustic cues with richer conversational judgment about when a speaker is truly finished, keeping the decisiveness of forced finalization while reducing the risk of cutting a user off mid-thought.

## Authors & Institutions

The wiki material attributes the feature and demonstration to Speechmatics, whose voice SDK, real-time API, and real-time SDK carry the force end-of-utterance capability. Individual presenters or authors are not named in the wiki content, so credit here goes to the Speechmatics team behind the video and the SDK feature rather than to specific listed authors.
