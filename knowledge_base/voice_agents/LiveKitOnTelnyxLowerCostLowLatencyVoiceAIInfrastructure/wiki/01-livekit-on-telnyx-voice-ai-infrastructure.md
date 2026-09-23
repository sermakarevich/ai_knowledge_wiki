> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# LiveKit on Telnyx: Voice AI Infrastructure You Control
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
---
## Dramatically Lower Cost
**Covers:** lower-cost hosted STT/TTS section

Telnyx hosts speech to text (STT) and text-to-speech (TTS) models on its own GPU infrastructure rather than reselling third-party APIs.

| Claim | Detail |
|---|---|
| Savings | 50% savings compared to LiveKit Cloud pricing |
| Beta offer | Waived active session fees during the beta period |

## Ultra-Low Latency
**Covers:** latency / colocation section

Colocating AI inference with global telephony points of presence eliminates hops to external APIs.

| Claim | Detail |
|---|---|
| Round-trip time | 200ms round-trip times, "fast enough that humans don't perceive the pause" |

## Enterprise Telephony, Built In
**Covers:** carrier telephony features section

Telnyx brings over a decade of carrier infrastructure to the LiveKit framework; these are native platform capabilities:

- AMR-WB for HD voice
- SIP REFER for seamless call transfers
- STIR/SHAKEN attestation for verified caller ID
- Full call recording/compliance controls

## Why It Matters
**Covers:** prototype-to-production transition section

> "Voice AI Agents are moving from prototype to production, and that transition demands infrastructure that scales with your business."

While LiveKit is great at real-time media, Telnyx specializes in the telephony layer that connects agents to the global phone network. LiveKit on Telnyx combines the framework developers trust with the carrier-grade foundation enterprises require.

## The Deployment
**Covers:** deployment steps section

> "Deploying your LiveKit agents on Telnyx couldn't be easier."

1. Change your URL to Telnyx using the dashboard or livekit-cli tool you already know.
2. Create your agent (agent.py) and package it with a Dockerfile.
3. Zip the files and send them to Telnyx via API call.
4. After this, Telnyx builds and runs your agent in its runtime environment.
5. Once your agents are running, point your Telnyx phone number to your agent and start taking calls immediately.

**Covers:** LiveKit on Telnyx hosted voice-AI platform: lower cost, low latency, telephony features and deployment overview.
