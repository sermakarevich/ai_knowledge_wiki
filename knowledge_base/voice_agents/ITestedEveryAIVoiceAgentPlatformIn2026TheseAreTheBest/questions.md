---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: I Tested Every AI Voice Agent Platform in 2026. These are the Best.

### Q1. What are the four components every AI voice agent platform resells, and what cost floor do they set?
> [!tip]- Answer
> Every platform combines speech-to-text, a large language model, text-to-speech, and phone infrastructure, with examples like Deepgram, GPT, ElevenLabs, and Twilio. Adding those vendor costs together sets a floor of around 7.8 cents per minute. Differentiation therefore comes from implementation and vendor choices rather than any proprietary magic. See [[wiki/01-ai-voice-agent-platforms-compared|The shared four-component stack]].

### Q2. Why is sound quality described as a vendor decision rather than a platform decision?
> [!tip]- Answer
> Sound is determined by the chosen text-to-speech model, and Retell, Vapi, Voiceflow, and LiveKit all let builders pick a voice bundle, while Bland runs a closed stack of unknown makeup. ElevenLabs running its own voice bundle natively sounds more crisp, realistic, smooth, and natural than other platforms reusing the same ElevenLabs model. For the most realistic voice regardless of cost, the pick is ElevenLabs. See [[wiki/01-ai-voice-agent-platforms-compared|Sound quality: a vendor decision]].

### Q3. How do the vendor-claimed latencies mislead, and what does each platform exclude from its number?
> [!tip]- Answer
> ElevenLabs claims ~75ms excluding network round trips and application overhead, Vapi claims sub-600 excluding endpointing and transport, and Retell claims 600ms "as low as" excluding the network hop. Bland claims 400ms or "lowest latency on the planet" with no methodology, while its own docs say the agent could wait up to about 2 and 1/2 seconds. In each case the caller-felt delay from pausing, transport, and network is removed from the headline figure. See [[wiki/01-ai-voice-agent-platforms-compared|Latency: vendor claims vs. third-party benchmark]].

### Q4. How was the third-party Secure Benchmark run, and how did the four tested platforms rank?
> [!tip]- Answer
> The benchmark ran the same agent on each platform with the same prompt, pinned model and temperature, over a real phone line, scoring around 1,100 turns each on median latency. Retell was fastest at 1.69 seconds, followed by ElevenLabs at ~1.73s, Vapi at ~2.34s, and LiveKit at ~2.46s. Bland and Voiceflow were not in the benchmark, with Voiceflow estimated at ~2–3s from personal experience. See [[wiki/01-ai-voice-agent-platforms-compared|Latency: vendor claims vs. third-party benchmark]].

### Q5. How do the platforms rank on normalized per-minute cost, and what makes LiveKit different?
> [!tip]- Answer
> Normalized on GPT-4 plus ElevenLabs voice plus Twilio, Vapi averages ~5 cents per minute, Retell ~7 cents, ElevenLabs ~8 cents, and Bland ~11 cents, while Voiceflow uses an undisclosed credit-based system. LiveKit is less a managed platform than an open-source framework requiring Python or JavaScript, but self-hosting workers drops cost from a cent a minute to 500ths of a cent — about 20 times cheaper. The cost winner among managed options therefore depends on which vendors are selected. See [[wiki/01-ai-voice-agent-platforms-compared|Cost per minute]].

### Q6. What did the 90-day status-page check find on production stability?
> [!tip]- Answer
> Over the last 90 days Retell showed 9 incidents, Vapi published ~99.77% API uptime (about 5 hours of outage), and Bland showed 66 incidents, while no exact incident count could be found for ElevenLabs. On availability alone, Vapi was judged probably one of the safest bets. Incident counts are a rough proxy, but the gap between single digits and 66 flags a real maintenance difference. See [[wiki/01-ai-voice-agent-platforms-compared|Production stability]].

### Q7. Evaluation: a phone-first agency with short prompts, a technical team wanting infrastructure ownership, and a regulated firm with long compliance-heavy calls each need a platform — which should each pick and why?
> [!tip]- Answer
> The phone-first agency with prompts under 4,000 tokens should pick Retell for its smooth, low-latency, low-cost phone stack with the right vendors. The technical team should pick LiveKit because it is the only open-source framework and the only one allowing self-hosted workers with full pipeline control. The regulated firm should pick Bland for long messy calls and compliance checklists, accepting higher cost and weaker stability in exchange for that fit. See [[wiki/01-ai-voice-agent-platforms-compared|Who should use what]].
