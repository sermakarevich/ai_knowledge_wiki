---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure

### Q1. What scaling problems on LiveKit Cloud motivate moving to LiveKit on Telnyx?

> [!tip]- Answer
> Developers face mounting costs, latency variability, and telephony limitations as voice AI agents move from prototype to production scale. See [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]].

### Q2. How does Telnyx deliver 50% savings on STT and TTS compared to LiveKit Cloud?

> [!tip]- Answer
> Telnyx hosts STT and TTS models on its own GPU infrastructure rather than reselling third-party APIs, removing the reseller markup. The platform claims 50% savings versus LiveKit Cloud pricing, plus waived active session fees during the beta period. See [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]].

### Q3. Why does colocating AI inference with telephony points of presence cut latency to 200ms round trips?

> [!tip]- Answer
> Colocation eliminates hops to external STT/TTS APIs by running inference next to the global telephony points of presence that terminate calls. The result is 200ms round-trip times, described as fast enough that humans don't perceive the pause. See [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]].

### Q4. What four native telephony capabilities does LiveKit on Telnyx include, and what does each do?

> [!tip]- Answer
> The platform natively provides AMR-WB for HD voice, SIP REFER for seamless call transfers, and STIR/SHAKEN attestation for verified caller ID. It also includes full call recording and compliance controls built on Telnyx's carrier infrastructure. See [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]].

### Q5. Why does the prototype-to-production transition demand Telnyx's carrier-grade foundation?

> [!tip]- Answer
> Production voice AI needs infrastructure that scales with the business, connecting agents reliably to the global phone network. While LiveKit handles real-time media well, Telnyx adds the carrier-grade telephony layer enterprises require for that scale. See [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]].

### Q6. What are the steps to deploy a LiveKit agent on Telnyx and start taking calls?

> [!tip]- Answer
> First change the URL to Telnyx via the dashboard or livekit-cli, then package agent.py with a Dockerfile, zip the files, and send them via API call for Telnyx to build and run. Once the agent is running, point a Telnyx phone number at it to take calls immediately. See [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]].

### Q7. For a team running high-volume LiveKit Cloud voice agents sensitive to cost and call quality, would you recommend migrating to LiveKit on Telnyx, and why?

> [!tip]- Answer
> Yes, recommend migration when per-minute STT/TTS costs and telephony gaps (HD voice, transfers, verified caller ID, compliance) dominate at scale, since Telnyx promises 50% savings, 200ms round trips, and native carrier features with familiar tooling. Hold back if the team depends on third-party model providers Telnyx doesn't host or needs pricing verified beyond beta-period waivers. See [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]].
