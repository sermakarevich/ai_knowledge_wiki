# How Voice Agents Handle Latency, Turn-Taking, and Safety | Interview With Kræn Hansen

**Video:** [How Voice Agents Handle Latency, Turn-Taking, and Safety | Interview With Kræn Hansen](https://www.youtube.com/watch?v=gVCU2RoZheQ) — YouTube

## Human Readable TL;DR

Think of a voice agent like a phone interpreter who hears you, thinks, and then speaks back, and every one of those steps adds a little delay. Because silence on a call feels like a dropped line, the agent fills the gaps the way a receptionist would — with background office sounds, a quick "let me look that up for you," and keyboard clicks while it works. It also learns the difference between you nodding along with "yeah, yeah" and actually wanting to cut in, so it does not rudely stop talking every time you murmur. And just like a bank would not let a trainee give loan advice unsupervised, a second supervisor AI listens in and can pull the plug if the conversation goes somewhere it should not.

## TL;DR

The interview describes a standard voice-agent pipeline — speech-to-text, a text-based LLM for reasoning, and expressive text-to-speech — and argues that the hard problems are latency, turn-taking, and safety rather than raw model intelligence. The LLM accounts for roughly 40 to 70% of pipeline latency, and the central design principle is that latency is perceived, so presence cues, narrated tool-calling, and audio feedback matter as much as raw speed. Turn-taking is handled by distinguishing backchannel affirmations from genuine interruptions, while safety is handled by a sidecar guardrail LLM run in either streaming or blocking mode. Everything is framed as tunable: making the stack faster costs expressiveness or correctness, and routing plus layered SDKs let builders fit model capacity, voice continuity, and latency budget to each use case.

---

## Problem & Motivation

The core problem is that voice is unforgiving in a way text chat is not. In text, a few seconds of waiting reads as normal thinking time, but in voice, even a short silence feels like the call dropped, and users repeat themselves or hang up. The motivation is therefore to make talking to a machine feel like talking to a competent human on the phone: responsive, present, and natural, without robotic flatness or creepy over-human-likeness. On top of that, real deployments such as banking support demand hard safety boundaries, so the agent must stay in role, disclose that it is not human when asked, and never drift into forbidden territory like giving financial advice.

## Main Original Ideas

1. **Perceived-latency design.** Rather than treating latency as a pure milliseconds problem, the interview frames it as a perception problem. Keeping audible presence alive with office noise or music, narrating slow work such as tool calls, and playing task sounds like keyboard clicking reassures the caller that the connection is live and work is happening.

2. **Intent-aware turn-taking.** Instead of a naive whoever-speaks-last-wins cutoff, the speech-to-text layer is expected to separate affirmations such as "yeah, yeah, okay" from real attempts to take the floor. This lets users talk over the agent with backchannels without derailing it, while genuine interruptions still get through.

3. **Expressive LLM-driven TTS with a speed cost.** The text model is allowed to direct delivery — laughing, whispering, and adding expressiveness — which makes the voice strikingly human-like, sometimes so much that listeners cannot tell agent from person. The tradeoff is explicit: pushing expressiveness can introduce hesitation artifacts that themselves carry unintended meaning.

4. **Streaming-or-blocking sidecar safety.** Safety is handled by a second LLM standing beside the main pipeline that cuts the conversation off if it goes off the rails. In streaming mode audio passes through and is cut on violation for lower added latency, while in blocking mode everything is verified before audio for stronger safety at higher latency.

5. **Router-to-sub-agent delegation with voice continuity control.** A fast low-intelligence router model, such as a secretary that triages callers, can hand off to a higher-capacity sub-agent for the hard part. The voice can stay identical for a seamless handoff or deliberately change in tonality to signal a shift in authority, for example when moving into loan advice.

6. **Layered, generated SDK surface.** The platform approach is a universal framework-agnostic JavaScript core, a React package with hooks and providers on top, and a React Native package adding native audio input, with headless or prebuilt UI options including an agent view and chat bubble. The whole surface is driven by an open API spec and code generation to keep many SDKs at feature parity.

## Key Findings

The LLM dominates pipeline delay, taking about 40 to 70% of total latency, so model choice and expressiveness settings are first-order latency levers. Across speech-to-text, LLM, and text-to-speech, the general tuning rule holds that making the stack faster makes it less expressive or less correct, which means there is no free lunch and every deployment is a compromise. Expressive synthesis is now good enough to be uncanny, producing support tickets where listeners cannot identify the agent by ear alone, and this is precisely why identity disclosure and anti-impersonation guardrails matter, with slightly higher latency sometimes preferable to an agent that feels deceptively human. On the safety axis, the streaming versus blocking choice cleanly trades responsiveness against assurance, and the router-plus-specialist pattern lets builders spend latency and cost budgets only where the task needs brains.

## Suggestions & Future Directions

The direction sketched in the conversation is more tunability and more agentic SDK tooling rather than a single fixed pipeline. Builders should expect to tune speed against expressiveness and correctness per use case, choose streaming or blocking safety according to risk tolerance, and use fast routers in front of specialist sub-agents to match cost and latency to task difficulty. On the platform side, the stated goal is keeping a growing family of SDKs aligned with feature parity through spec-driven code generation, including generating specifications from implementations and comparing across SDKs to converge the developer experience. The middle "speech engine" tier, where teams bring their own conversational brain and get voice handling from the platform, is positioned as the pragmatic path for anyone who already has text chat and simply wants to give it a voice.

## Authors & Institutions

The video is an interview with Kræn Hansen, speaking from the perspective of the ElevenLabs agents platform team, which is described as a roughly 400-person organization with internal research shipping voice-agent features and verticals. The discussion also references prior platform patterns from MongoDB and Realm in the design of the layered SDK architecture.
