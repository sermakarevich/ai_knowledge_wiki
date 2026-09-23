# LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure

**Article:** [LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure](https://telnyx.com/release-notes/livekit-on-telnyx-voice-ai-infrastructure) — Telnyx Release Notes, n.d.

## Human Readable TL;DR

Think of LiveKit as a great engine for real-time voice conversations and Telnyx as the private highway system plus power plant it now runs on. Instead of renting expensive third-party speech services over the public internet, Telnyx hosts the ears and voice of the AI on its own GPUs right next to its global phone network, like putting the kitchen next to the dining room so food arrives hot and fast. The result is phone agents that answer in about 200 milliseconds with clearer sound and verified caller ID, while costing roughly half as much to run, and moving an agent over is as simple as changing an address and shipping a zip file.

## TL;DR

LiveKit on Telnyx is a fully hosted platform that runs LiveKit agents on Telnyx-owned infrastructure to make production voice AI cheaper, faster, and telephony-ready at scale. By self-hosting STT and TTS models on its own GPUs and colocating inference with global telephony points of presence, it claims 50% savings over LiveKit Cloud pricing with waived active session fees during beta and 200ms round-trip times. The platform adds native carrier capabilities including AMR-WB HD voice, SIP REFER transfers, STIR/SHAKEN attestation, and call recording and compliance controls, with a familiar deployment flow of changing the LiveKit URL, packaging the agent with a Dockerfile, deploying via API, and pointing a Telnyx number at the agent.

---

## Problem & Motivation

Voice AI agents are moving from prototype to production, and that transition exposes the limits of developer-friendly clouds when scale, cost, and phone-network realities arrive. Teams building on LiveKit Cloud face mounting inference costs from resold third-party STT and TTS APIs, latency variability from extra network hops to external services, and gaps in enterprise telephony such as HD voice codecs, clean call transfers, caller ID verification, and compliance-grade recording. Telnyx frames the motivation as a division of strengths: LiveKit excels at the real-time media framework developers trust, while Telnyx brings over a decade of carrier infrastructure that connects agents to the global phone network, and combining them gives enterprises a carrier-grade foundation that scales with the business.

## Main Original Ideas

1. **Self-hosted speech stack on Telnyx GPUs** — rather than reselling third-party speech APIs, Telnyx hosts STT and TTS models on its own GPU infrastructure, which underpins the cost advantage and tighter control over performance and scaling.

2. **Colocated inference and telephony** — AI inference is placed alongside global telephony points of presence so media and model calls avoid hops to external APIs, directly targeting lower and more predictable round-trip latency.

3. **Carrier-native telephony built in** — the platform treats enterprise voice features as native capabilities, including AMR-WB for HD voice quality, SIP REFER for seamless call transfers, STIR/SHAKEN attestation for verified caller ID, and full call recording and compliance controls.

4. **Frictionless LiveKit-compatible deployment** — developers keep the LiveKit workflow they know by changing the URL via dashboard or livekit-cli, packaging agent.py with a Dockerfile, zipping and sending it via API for Telnyx to build and run, then pointing a Telnyx phone number at the running agent to take calls immediately.

## Key Findings

The central quantitative claims are 50% savings compared to LiveKit Cloud pricing, with active session fees waived during the beta period, and 200ms round-trip times described as fast enough that humans do not perceive the pause. Qualitatively, the platform presents LiveKit framework compatibility with Telnyx carrier operations as sufficient for prototype-to-production migration, where cost, latency, and telephony compliance are the binding constraints. The deployment model is reported as fully hosted: Telnyx builds and runs the submitted agent in its runtime environment, leaving number routing as the final step to production traffic.

## Suggestions & Future Directions

The implied direction is to validate the cost and latency claims under production load and to expand beta usage while session fees are waived, giving teams a low-risk path to migrate existing LiveKit agents. Enterprises with strict recording, verification, and transfer requirements are positioned as the natural early adopters, since those carrier features arrive without separate integration work. Longer term, the colocation of inference and telephony suggests further optimization of voice quality, transfer handling, and global routing as voice agents scale from pilots to always-on phone channels.

## Authors & Institutions

Telnyx, via its Release Notes publication channel.
