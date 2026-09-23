> [[index|Wiki]] | [[summary|Summary]]
# I Tested Every AI Voice Agent Platform in 2026. These are the Best. — Digest

## 1. [[wiki/01-ai-voice-agent-platforms-compared|AI Voice Agent Platforms Compared (2026): Six Platforms on Voice, Latency, Cost, Stability]]
**In one sentence:** Adam Cheyne compares six AI voice agent platforms (Retell, Vapi, ElevenLabs, Bland, Voiceflow, LiveKit) on sound quality, latency, cost per minute, and production stability, and concludes there is no single winner — each fits a different audience and use case.
## Key points
- All platforms resell the same four components (speech-to-text, LLM, text-to-speech, phone infrastructure — e.g. Deepgram, GPT, ElevenLabs, Twilio), setting a cost floor of around 7.8 cents per minute.
- Sound quality is a text-to-speech vendor decision, not a platform decision; ElevenLabs' own builder sounds "more crisp, and it sounds more realistic, and it sounds more smooth and natural" versus other platforms reusing the same ElevenLabs bundle.
- Third-party Secure Benchmark medians over ~1,100 scored turns each: Retell 1.69s, ElevenLabs ~1.73s, Vapi ~2.34s, LiveKit ~2.46s; Bland and Voiceflow were not in the benchmark, with Voiceflow ~2–3s from personal experience.
- Vendor-claimed latencies exclude real-world time: ElevenLabs ~75ms "excluding network round trips and application overhead," Vapi sub-600 excluding endpointing and transport, Retell 600 "as low as" excluding the network hop, Bland 400ms with no methodology while its docs say the agent "could wait up to about 2 and 1/2 seconds."
- Average cost per minute: Vapi ~5 cents, Retell ~7 cents, ElevenLabs ~8 cents, Bland ~11 cents (Voiceflow undisclosed credit-based system), normalized on GPT-4 + ElevenLabs + Twilio; LiveKit self-hosted workers drop "from a cent a minute to 500ths cent a minute, which is 20 times cheaper."
- Production stability (status pages, last 90 days): Retell 9 incidents, Vapi 99.77% API uptime ("about 5 hours of outage"), Bland 66 incidents, ElevenLabs exact incident count not found — Vapi judged "probably one of the safest bets" on availability.
- Per-audience picks: phone-first AI agencies with prompts under 4,000 tokens → Retell; developers wanting pipeline plus low-code managed platform → Vapi; technical owners wanting own pipeline/infrastructure → LiveKit (only open-source framework, only one where "you can self-host your workers"); best realistic voice regardless of cost → ElevenLabs; client-editable dashboard → Voiceflow; regulated-industry long messy calls and compliance checklist → Bland.

## The argument in five moves
1. Every platform resells the same four-component stack (STT, LLM, TTS, telephony), so differentiation comes from implementation and vendor choices, not magic, with a cost floor around 7.8 cents per minute.
2. Sound quality is decided by the TTS vendor rather than the platform, and ElevenLabs running its own voice bundle natively sounds the most crisp, realistic, smooth, and natural.
3. Vendor latency claims understate what callers feel by excluding network, endpointing, and overhead, while the third-party Secure Benchmark ranks Retell fastest (1.69s median), then ElevenLabs, Vapi, and LiveKit.
4. On normalized per-minute cost Vapi is cheapest and Bland most expensive, with LiveKit self-hosting far cheaper for technical teams, and on 90-day stability Vapi looks safest while Bland shows the most incidents.
5. Therefore no single platform wins overall; the right pick follows the builder's profile — Retell for phone-first agencies, Vapi for developer-managed control, LiveKit for self-hosted ownership, ElevenLabs for best voice, Voiceflow for client editing, Bland for regulated long calls.
