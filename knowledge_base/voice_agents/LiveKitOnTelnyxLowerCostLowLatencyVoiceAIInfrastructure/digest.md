> [[index|Wiki]] | [[summary|Summary]]

# LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure — Digest

## 1. [[wiki/01-livekit-on-telnyx-voice-ai-infrastructure|LiveKit on Telnyx: Voice AI Infrastructure You Control]]

**In one sentence:** LiveKit on Telnyx is a fully hosted platform running LiveKit agents on Telnyx-owned infrastructure to cut costs, reduce latency, and add enterprise telephony at scale.

## Key points

- Developers on LiveKit Cloud face mounting costs, latency variability, and telephony limitations at scale.
- LiveKit on Telnyx runs LiveKit agents on Telnyx-owned infrastructure as a fully hosted platform.
- Telnyx hosts STT and TTS models on its own GPU infrastructure rather than reselling third-party APIs.
- The platform delivers 50% savings compared to LiveKit Cloud pricing, plus waived active session fees during the beta period.
- Colocating AI inference with global telephony points of presence eliminates hops to external APIs.
- The platform delivers 200ms round-trip times, fast enough that humans don't perceive the pause.
- Native telephony capabilities include AMR-WB for HD voice, SIP REFER for seamless call transfers, STIR/SHAKEN attestation for verified caller ID, and full call recording/compliance controls.
- Deployment is: change URL to Telnyx via dashboard or livekit-cli, package agent.py with a Dockerfile, zip and send via API call, then Telnyx builds and runs the agent; point a Telnyx phone number at the agent to take calls.

## The argument in five moves

1. Voice AI agents are moving from prototype to production, so scaling demands infrastructure that grows with the business.
2. LiveKit Cloud hits limits at scale: mounting costs, latency variability, and telephony gaps.
3. Telnyx answers by hosting LiveKit agents plus STT/TTS models on its own GPU and carrier infrastructure, cutting costs by 50% versus LiveKit Cloud.
4. Colocating inference with global telephony points of presence removes external-API hops and reaches 200ms round trips humans don't perceive as a pause.
5. Carrier-grade telephony comes built in — HD voice, seamless transfers, verified caller ID, and recording/compliance controls.
6. Migration stays familiar: switch the URL, package agent.py with a Dockerfile, zip and send via API, then point a Telnyx number at the agent and take calls.
