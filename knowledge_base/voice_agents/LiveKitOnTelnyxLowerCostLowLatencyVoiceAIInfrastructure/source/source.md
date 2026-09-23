> PDF location: https://telnyx.com/release-notes/livekit-on-telnyx-voice-ai-infrastructure (no source.pdf fetched; article source — see Source field below)
# LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure
Source: https://telnyx.com/release-notes/livekit-on-telnyx-voice-ai-infrastructure
Kind: article
Fetched: 2026-09-22T08:40:11.485714+00:00
Tool: urllib

LiveKit on Telnyx: Lower Cost, Low Latency Voice AI Infrastructure

Release notes

# LiveKit on Telnyx: Voice AI Infrastructure You Control

### 6, Apr 2026

Developers building voice AI agents on LiveKit Cloud face mounting costs, latency variability, and telephony limitations at scale. LiveKit on Telnyx is a fully hosted platform that runs your LiveKit agents on Telnyx-owned infrastructure, delivering dramatic cost reductions, ultra-low latency, and enterprise telephony capabilities.

### Dramatically Lower Cost

Telnyx hosts speech to text (STT) and text-to-speech (TTS) models on its own GPU infrastructure rather than reselling third-party APIs. The result: 50% savings compared to LiveKit Cloud pricing, plus waived active session fees during the beta period.

### Ultra-Low Latency

Colocating AI inference with global telephony points of presence eliminates hops to external APIs. You get 200ms round-trip times, fast enough that humans don't perceive the pause.

### Enterprise Telephony, Built In

Telnyx brings over a decade of carrier infrastructure to the LiveKit framework: AMR-WB for HD voice, SIP REFER for seamless call transfers, STIR/SHAKEN attestation for verified caller ID, and full call recording/compliance controls. These are native platform capabilities.

### Why It Matters

Voice AI Agents are moving from prototype to production, and that transition demands infrastructure that scales with your business. While LiveKit is great at real-time media, Telnyx specializes in the telephony layer that connects agents to the global phone network. LiveKit on Telnyx combines the framework developers trust with the carrier-grade foundation enterprises require.

### The Deployment

Deploying your LiveKit agents on Telnyx couldn't be easier.

Change your URL to Telnyx using the dashboard or livekit-cli tool you already know

Create your agent (agent.py) and package it with a Dockerfile

Zip the files and send them to Telnyx via API call

After this, Telnyx builds and runs your agent in its runtime environment.

Once your agents are running, point your Telnyx phone number to your agent and start taking calls immediately.

Learn more about migrating from LiveKit Cloud to LiveKit on Telnyx in our quickstart guide, or explore our plugin documentation for lightweight STT and TTS integration.

Start building

### Ask AI
