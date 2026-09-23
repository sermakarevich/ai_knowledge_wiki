> [[index|Wiki]] | [[summary|Summary]]

# The Ultimate Voice AI Tier List: Vapi, LiveKit, Retell, ElevenLabs, Telnyx, Pipecat — Digest

## 1. [[wiki/01-voice-ai-tier-list-overview|Voice AI Tier List Overview and Scoring Rubric]]

**In one sentence:** Piotr ranks Vapi, ElevenLabs, Pipecat, Retell, LiveKit, and Telnyx on a 0–2 scale weighted for small, medium, and large businesses using learnings from 15 million call-center calls, arguing no single platform serves every customer.

## Key points

- Motivation comes from a LinkedIn poll where viewers requested "Vapi versus ElevenLabs versus Pipecat versus Retell" and from the author's learnings from 15 million calls in a call center.
- Scoring uses a 0–2 scale where 0 is terrible, 1 is quite good, and 2 is perfect, with different weights per question for small, medium, and large businesses.
- Extensibility scores: Vapi 1, ElevenLabs below Vapi but still 1, Pipecat 2, Retell 1, LiveKit 1 (part open source, better than Vapi/ElevenLabs but not fully open), Telnyx similar to Vapi/ElevenLabs/LiveKit.
- Simplicity of shipping a working agent: Vapi 2, ElevenLabs even simpler than Vapi, Pipecat 0 (requires Docker and orchestration for production), Retell simple, LiveKit simple, Telnyx 2.
- Latency: Vapi adds roughly 150 ms of platform overhead with US-only infra; Pipecat 2 because self-hosting can be optimized; Retell 2 and LiveKit 2 on benchmarks; Telnyx leads via collocated GPUs, servers, and telephony.
- Feature richness: Vapi 2, Pipecat 2, LiveKit 2, Retell 1 (solid telephony but weaker observability and fewer integrations), ElevenLabs below Vapi as a newer platform.
- Pricing and support: Vapi is 5 cents per minute (score 1); ElevenLabs is 10 cents per minute on smaller plans and less on bigger plans ("Your pricing sucks"); Telnyx makes ~90% of revenue from telephony rounded up to a full minute; Vapi docs/support 2 via Discord, Pipecat and LiveKit 2 for community, Telnyx 1.
- Debugging: Vapi revised from 2 to 1 for random/unhelpful errors, out-of-sync docs, wrong types, and unversioned breaking changes; ElevenLabs 1, Retell 1, LiveKit 2 for timeline-synced transcript observability, Telnyx 1 based on online reports of unhelpful support.

## The argument in five moves

1. No single voice AI platform serves every customer, so buyers should judge providers by business size using learnings from 15 million call-center calls.
2. A 0–2 rubric (terrible to perfect) with per-question SMB weights makes the Vapi, ElevenLabs, Pipecat, Retell, LiveKit, and Telnyx comparison personalized rather than generic.
3. Closed platforms (Vapi, ElevenLabs, Retell, LiveKit, Telnyx) trade simplicity for capped extensibility, while open Pipecat offers full control at the cost of production complexity.
4. Latency, features, and pricing split the field: Telnyx/Retell/LiveKit lead on latency, Vapi/Pipecat/LiveKit lead on features, and ElevenLabs/Retell lose on per-minute pricing.
5. Debugging and docs decide production readiness: LiveKit and Pipecat earn top marks for observability and community, while Vapi's score drops on random errors and breaking changes.
6. The tier list therefore favors ElevenLabs for small businesses, LiveKit across sizes, and Pipecat only where engineering capacity exists, with compliance deferred to a follow-up.
