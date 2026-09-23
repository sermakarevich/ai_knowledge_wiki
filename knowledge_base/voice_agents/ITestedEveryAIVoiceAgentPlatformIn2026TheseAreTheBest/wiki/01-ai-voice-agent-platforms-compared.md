> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# AI Voice Agent Platforms Compared (2026): Six Platforms on Voice, Latency, Cost, Stability
**In one sentence:** Adam Cheyne compares six AI voice agent platforms (Retell, Vapi, ElevenLabs, Bland, Voiceflow, LiveKit) on sound quality, latency, cost per minute, and production stability, and concludes there is no single winner — each fits a different audience and use case.
## Key points
- All platforms resell the same four components (speech-to-text, LLM, text-to-speech, phone infrastructure — e.g. Deepgram, GPT, ElevenLabs, Twilio), setting a cost floor of around 7.8 cents per minute.
- Sound quality is a text-to-speech vendor decision, not a platform decision; ElevenLabs' own builder sounds "more crisp, and it sounds more realistic, and it sounds more smooth and natural" versus other platforms reusing the same ElevenLabs bundle.
- Third-party Secure Benchmark medians over ~1,100 scored turns each: Retell 1.69s, ElevenLabs ~1.73s, Vapi ~2.34s, LiveKit ~2.46s; Bland and Voiceflow were not in the benchmark, with Voiceflow ~2–3s from personal experience.
- Vendor-claimed latencies exclude real-world time: ElevenLabs ~75ms "excluding network round trips and application overhead," Vapi sub-600 excluding endpointing and transport, Retell 600 "as low as" excluding the network hop, Bland 400ms with no methodology while its docs say the agent "could wait up to about 2 and 1/2 seconds."
- Average cost per minute: Vapi ~5 cents, Retell ~7 cents, ElevenLabs ~8 cents, Bland ~11 cents (Voiceflow undisclosed credit-based system), normalized on GPT-4 + ElevenLabs + Twilio; LiveKit self-hosted workers drop "from a cent a minute to 500ths cent a minute, which is 20 times cheaper."
- Production stability (status pages, last 90 days): Retell 9 incidents, Vapi 99.77% API uptime ("about 5 hours of outage"), Bland 66 incidents, ElevenLabs exact incident count not found — Vapi judged "probably one of the safest bets" on availability.
- Per-audience picks: phone-first AI agencies with prompts under 4,000 tokens → Retell; developers wanting pipeline plus low-code managed platform → Vapi; technical owners wanting own pipeline/infrastructure → LiveKit (only open-source framework, only one where "you can self-host your workers"); best realistic voice regardless of cost → ElevenLabs; client-editable dashboard → Voiceflow; regulated-industry long messy calls and compliance checklist → Bland.
---
## Intro and judging criteria
Author intro: "my name is Adam Cheyne, and I've been running my own AI agency, Legacy AI, over the past two years, building AI voice agents for more than 52 different clients worldwide." Goal: "ranking this top six AI voice agent platforms right now in 2026 and beyond," judged on "how fast they are, how good does it actually sounds, how much it cost per minute, and how stable it is and maintenance for that system."
**Covers:** intro, six-platform framing, four judging factors

## The shared four-component stack
"Every single AI voice agent platform is not magic. They're all reselling you on the same four components. Speech-to-text, which transcribes audio into text, a large language model, text-to-speech, turning text from the large language model into audio, and a phone line or a phone infrastructure." Examples given: Deepgram (STT), GPT (LLM), ElevenLabs (TTS), Twilio (telephony). "So, if you just add all of them together, it could cost around 7.8 cents, and that's the floor."
**Covers:** shared-stack explanation and 7.8-cent floor

## Sound quality: a vendor decision
"Sound, as you heard from what I said just now, is not really a platform decision. It's a vendor decision of the text-to-speech model." Retell, Vapi, Voiceflow, and LiveKit "all let you pick their own voice bundle," while "Bland actually runs its own closed stack, so no one really knows what that text-to-speech layer really is," and "ElevenLabs, of course, is the voice bundle." Even though others can reuse the ElevenLabs TTS model, ElevenLabs running it natively sounds "more crisp, and it sounds more realistic, and it sounds more smooth and natural." Pick for realism: "I'll be picking ElevenLabs." Flexible alternatives usable inside Retell/Vapi: "Katia is one that I use a lot, as well as the latest Fish Audio."
**Covers:** voice-quality comparison and ElevenLabs pick

## Latency: vendor claims vs. third-party benchmark
Self-reported numbers from docs/marketing:

| Platform | Claimed latency | Documented caveat |
|---|---|---|
| Bland | lowest latency on the planet / 400 milliseconds | "no methodology at all," docs say agent "could wait up to about 2 and 1/2 seconds" |
| ElevenLabs | around 75 milliseconds | "excluding network round trips and application overhead"; "the time to first audio is always larger and often substantially larger than that number" |
| Vapi | sub-600 | "total excludes the end pointing and transport time"; endpointing "is the pause where the agent works out if you've stopped talking or known as end of turn"; "3 to 800 milliseconds of the thing the caller actually feels is removed from the number" |
| Retell | 600 ("as low as" 600) | "excludes again the network hop to the user" |
| Voiceflow | not explicitly stated | personal experience "usually it's around 2 to 3 seconds latency" |

Third-party Secure Benchmark (same agent on each platform, same prompt, same pinned model/temperature, real phone line, "around 1,100 scored turns each," median):

| Platform | Median latency |
|---|---|
| Retell | 1.69 seconds |
| ElevenLabs | around 1.73 seconds |
| Vapi | around 2.34 seconds |
| LiveKit | around 2.46 seconds |
| Bland / Voiceflow | not in this benchmark |

Smoothness pick: "I would probably pick Life Kit and Retell. Just because Life Kit actually gives you so much more control over the infrastructure, and therefore you can have a much more control over the overall latency. Whereas Retell is just a smooth and low latency infrastructure overall."
**Covers:** latency claims, caveats, Secure Benchmark results

## Cost per minute
"Vapi on the average cost around per minute like 5 cents, Retell 7 cents, Eleven Labs 8 cents, Bland 11." Voiceflow: "they don't really disclose it anymore in the pricing page. They also use a different credit-based system." Normalized comparison basis: "we all agreed to use GPT-4 LLM and Eleven Labs for the voice and Twilio as the phone line." Cost winner: "probably going to be around Retell, Life Kit, and Vapi, depending again on which vendors you're using." LiveKit caveat: "less of a managed voice agent platform, but more of a open-source framework that you can have maximum control"; "you do have to be technical and it's not a no-code platform. You do have to know Python or JavaScript." Self-hosting payoff: "you can self-host your workers, which drop you from a cent a minute to 500ths cent a minute, which is 20 times cheaper."
**Covers:** per-minute costs, normalization vendors, LiveKit self-hosting

## Production stability
Question asked: "how many incidents or how many outage do these platforms actually have per month?" Findings from status pages: "Retell's status page in last 90 days, there were nine incidents. And Vapi publishes its API uptime of around 99.77% over 90 days. So, that's about 5 hours of outage. Well, Bland's status page actually shows 66 different incidents. Whereas for 11 Labs, I really couldn't find the exact number of incidents in the status page." Availability verdict: "in terms of availability, Vapi is probably one of the safest bets on this regard."
**Covers:** 90-day incidents/uptime comparison

## Who should use what
"So, based on the above four factors, here's what I actually think":

| Audience / need | Recommendation |
|---|---|
| AI agency, phone-first, prompts under 4,000 tokens, smooth + cheap with correct STT/LLM/TTS vendors | Retell AI |
| Developer wanting pipeline control plus a low-code interface, managed platform | Vapi |
| Technical, want to own the pipeline and infrastructure | LiveKit ("the only open-source framework," "the only one where you can self-host your workers") |
| Don't care about cost, want best realistic-sounding voice | ElevenLabs Voice Agent Builder |
| Client needs to tweak things quickly via dashboard | Voiceflow |
| Regulated industry, long messy calls, long compliance checklist | Bland AI |

Closing: "it's not really one voice agent platform that beats all the others. Each one of them has his own specific use case and it depends on who you are and who you're building these AI voice agents for."
**Covers:** per-audience recommendations and no-single-winner conclusion
