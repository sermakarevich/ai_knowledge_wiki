---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: The Ultimate Voice AI Tier List: Vapi, LiveKit, Retell, ElevenLabs, Telnyx, Pipecat

### Q1. What is Piotr's core thesis, and how does the 0–2 SMB-weighted rubric implement it?
> [!tip]- Answer
> The thesis is that no single voice AI platform serves every customer, grounded in learnings from 15 million call-center calls and a LinkedIn poll requesting the Vapi/ElevenLabs/Pipecat/Retell comparison. He scores each provider from 0 (terrible) to 2 (perfect), with 1 meaning quite good, applying different per-question weights for small, medium, and large businesses. The rubric covers extensibility, simplicity, latency, UX, features, pricing, debugging, docs/support, with compliance deferred to a follow-up video. See [[wiki/01-voice-ai-tier-list-overview|Scoring rubric]].

### Q2. How do the six platforms score on extensibility, and why can closed-source platforms never earn a 2?
> [!tip]- Answer
> Pipecat alone scores 2 because it is a fully open framework where you can do whatever you want with LLM, TTS, STT, VAD, and analytics choices. Vapi, ElevenLabs, Retell, LiveKit, and Telnyx all score around 1: Vapi has many integrations, ElevenLabs has fewer options, Retell fewer still, and LiveKit is part open source so better than Vapi/ElevenLabs but not fully do-anything. Closed source caps the ceiling, so ElevenLabs can never reach 2 no matter how fast it develops. See [[wiki/01-voice-ai-tier-list-overview|Extensibility]].

### Q3. Why do Vapi, ElevenLabs, and Telnyx score top marks on simplicity while Pipecat scores 0?
> [!tip]- Answer
> Vapi scores 2 for really nice developer ergonomics, ElevenLabs is even a little easier with high-level settings like interrupt-a-lot versus careful tuning, and Telnyx scores 2 with fairly intuitive APIs, while Retell and LiveKit are also simple to get running. Pipecat scores 0 because shipping requires setting up Docker containers and orchestrating production infrastructure, so it is not for builders with little or no programming knowledge. It is amazing if you need full control, but simplicity is not the problem it solves. See [[wiki/01-voice-ai-tier-list-overview|Simplicity]].

### Q4. What drives the latency differences: Vapi's overhead, self-hosting, and Telnyx's collocation?
> [!tip]- Answer
> Vapi adds roughly 150 ms of platform overhead and its infra is US-only, so EU/India customers see higher latency — noticeable but not customer-losing. Pipecat scores 2 because self-hosting lets you optimize latency as far as humanly possible, while Retell and LiveKit both score 2 on benchmarks, Retell sitting ahead of Vapi and near LiveKit. Telnyx leads the group via collocated infrastructure with GPUs, servers, and telephony in the same location as the call, which is hard to replicate. See [[wiki/01-voice-ai-tier-list-overview|Latency]].

### Q5. How do the platforms compare on UX polish and feature richness, especially Retell's and Telnyx's weak spots?
> [!tip]- Answer
> Vapi's dashboard is option-rich with solid call metrics but slow and partly broken, ElevenLabs is really solid for agent-building with a few new-platform bugs, LiveKit is really solid, Retell trails Vapi and ElevenLabs on smoothness, and Pipecat scores 0 on builder UX by design. On features, Vapi, Pipecat, and LiveKit score 2 — LiveKit stands out with timeline-synced transcript observability — while Retell scores 1 for solid telephony but weaker observability and fewer integrations. Telnyx lags on observability though it is heading in the right direction. See [[wiki/01-voice-ai-tier-list-overview|Feature richness]].

### Q6. What are the headline pricing, debugging, and docs/support verdicts across the six platforms?
> [!tip]- Answer
> Vapi charges a simple 5 cents per minute (score 1) while ElevenLabs charges 10 cents on smaller plans — "your pricing sucks" — Retell prices worse, and Telnyx profits mostly (~90%) from telephony rounded up to a full minute. Debugging cuts Vapi from 2 to 1 over random errors, out-of-sync docs, wrong types, and unversioned breaking changes, while LiveKit earns 2 for baked-in observability and Pipecat is "dope" as self-hosted code. Docs/support goes 2 for Vapi (Discord), Pipecat (huge community, sometimes the CEO), and LiveKit, but only 1 for Telnyx on thin docs and weak support. See [[wiki/01-voice-ai-tier-list-overview|Pricing]].

### Q7. Evaluation: a non-technical small business, a mid-size team shipping fast with standard needs, and an enterprise with engineers and strict latency needs each need a platform — which should each pick and why?
> [!tip]- Answer
> The non-technical small business should pick ElevenLabs for the simplest agent builder and solid UX despite higher per-minute pricing, since ease outweighs extensibility at that size. The mid-size team should pick Vapi or LiveKit: Vapi for fast shipping with rich features and good docs, LiveKit as the incredibly solid all-rounder with top observability and latency. The engineering-heavy enterprise should pick Pipecat for full control and optimizable latency, or Telnyx for collocated low-latency telephony, accepting production complexity in exchange. See [[wiki/01-voice-ai-tier-list-overview|Documentation and support]].
