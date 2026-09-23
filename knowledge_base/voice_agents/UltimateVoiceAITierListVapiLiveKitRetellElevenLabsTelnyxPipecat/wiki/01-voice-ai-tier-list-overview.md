> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Voice AI Tier List Overview and Scoring Rubric

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

---

## Intro and premise

Piotr opens: "Hi, my name is Piotr. I'm glad to have you here."

He says he did not want to "essentially service a LM for you guys to tell you what I found" and instead wants it personalized: "how I feel about the platforms and what problems they solve and for whom."

Core thesis quote: "I don't believe every platform serves every single customer. It's just not doable."

**Covers:** intro, LinkedIn poll, 15M calls premise

## Scoring rubric

He made "a spreadsheet... to help judge different voice AI providers along the way."

Approach: "judging provider by a size of your business," divided into "three types: small, medium, and large businesses," where "each question has different weight applied to it."

Scale verbatim: "from zero to two, where zero is terrible, two is perfect, and one is quite good."

Categories judged: extensibility, simplicity, latency, UX, feature richness, pricing, debugging experience, documentation and support, plus compliance/regulation deferred to a future video.

**Covers:** rubric, SMB weighting, 0–2 scale

## Extensibility: custom logic, integrations, infrastructure

Definition: "How extensible is the platform for custom logic integrations and infrastructure?" — i.e. swapping LLM, text-to-speech, speech-to-text, VAD options, and attaching custom analytics.

| Provider | Score | Rationale in chunk |
|---|---|---|
| Vapi | 1 | Closed source but "a lot of different integrations" |
| ElevenLabs | 1 | "Worse than Vapi," fewer options, developing fast, never a 2 because closed source |
| Pipecat | 2 | "You can do whatever you want with this framework" |
| Retell | 1 | Closed source with even fewer options, but some baked-in integrations |
| LiveKit | 1 | Part open source, better than Vapi/ElevenLabs, but not fully do-anything |
| Telnyx | ~1 | "Similar story to ElevenLabs or Vapi or LiveKit" |

**Covers:** extensibility comparison

## Simplicity: shipping an agent that works

Definition: "How simple it is to ship an agent that works?"

| Provider | Score | Rationale in chunk |
|---|---|---|
| Vapi | 2 | "Really really nice developer ergonomics"; agent-creation flow fine for getting started and "very, very, very simple debugging" but not recommended as the main approach |
| ElevenLabs | 2+ | "Even a little bit easier" with high-level interruption settings like "interrupt a lot or don't interrupt" instead of careful tuning |
| Pipecat | 0 | "You need to set up Docker container and like orchestrate everything"; "not an easy framework" and not for little/no programming knowledge; "amazing if you need it" |
| Retell | simple | "Also very simple" |
| LiveKit | simple | "Hitting the ground running is very simple" |
| Telnyx | 2 | APIs and "fairly intuitive platform" |

**Covers:** simplicity comparison

## Latency: low and consistent end-to-end

Definition: "How low and consistent is end-to-end conversational latency?"

- Vapi: infra in US only "at least to my knowledge so far," so EU/India customers see higher latency; platform-added latency "probably roughly around 150 milliseconds" based on benchmarks seen — "not going to make your customers go away" but worth noting.
- ElevenLabs: "very new to the game," infra not thought to be optimized; assumed similar to Vapi.
- Pipecat: 2 — "definitely have an option to host it yourself" and "make it as good as humanly possible."
- Retell: 2 — benchmarks put it "in front of Vapi" and "just behind LiveKit or on par almost on par with LiveKit."
- LiveKit: 2 — latency "really good."
- Telnyx: best of the group — "collocated infrastructure," meaning "GPUs, servers, everything lies within similar location to where the phone call is being made"; "not that easy to get collocated everything."

**Covers:** latency comparison, 150 ms figure, collocation

## UX: builder dashboard polish

Definition: "How polished is the builder dashboard and overall user experience?"

- Vapi: UI "kind of slow" but many options, intuitive navigation, solid call metrics and filtering; "not all of their stuff works."
- ElevenLabs: "really solid" UX for making an agent, with "few bugs here and there" because new and improving daily.
- Pipecat: 0 — not bad, but not user-friendly; "very developer-friendly" with full extensibility and analytics, since best builder UX is not the problem it solves.
- Retell: 1 or 2 — "not as advanced as Vapi and probably doesn't feel as smooth as ElevenLabs."
- LiveKit: "really solid."
- Telnyx: deferred — "going to have to think about a little bit more and maybe fill it in later."

**Covers:** UX comparison

## Feature richness: telephony, tools, orchestration, observability

Definition: "How complete is the platform across telephony tools, orchestration, observability, and agent features?"

| Provider | Score | Rationale in chunk |
|---|---|---|
| Vapi | 2 | Lacking working emotion detection and has couple bugs, but fixes fairly quickly; "really solid" |
| ElevenLabs | below Vapi | "Not there yet," improving daily, fewer integrations than Vapi |
| Pipecat | 2 | "You can hook up everything you want to it" plus US phone number out of the box |
| Retell | 1 | Solid telephony setup, but observability "not as good" and fewer integrations than Vapi |
| LiveKit | 2 | Many hooks plus "very solid observability" with timeline synchronized to transcript navigation |
| Telnyx | below par | "Observability not there yet... hopefully it's going to improve" but "going in the right direction" |

**Covers:** feature richness comparison

## Pricing

- Vapi: "very simple. 5 cents per minute. It's not the best, not the worst. One."
- ElevenLabs: "10 cents per minute on a smaller plans and a little bit less on the bigger plans"; verdict quote: "Your pricing sucks."
- Pipecat: "very solid pricing."
- Retell: 0 — "They have worse pricing."
- LiveKit: "very solid."
- Telnyx: "also very solid"; side note: Telnyx makes money "not via agent thing platform, it's via telephony because they round up to a full minute," estimated as "probably 90% of their revenue from the platform."

**Covers:** pricing comparison, 5 cents and 10 cents figures

## Debugging experience

- Vapi: revised from 2 to 1 — logs/transcripts/filtering helped find large-scale issues, but errors are "completely random" in quality (example: clear OpenRouter custom-LLM error surfaced as "it didn't work. Sorry"), docs "sometimes are out of sync, the types are simply wrong," and unversioned changes "break your production."
- ElevenLabs: 1 — not error handling per se but closed-source pain on complex MCP/tool-call/prompt/variable cases plus limited docs and online support.
- Pipecat: "dope."
- Retell: 1 — closed-source, "similar story."
- LiveKit: 2 — "baked-in observability that's really really solid" plus better documentation experience.
- Telnyx: 1 — little direct experience; based on Googling, support is unhelpful "unless you make a credit thread about it."

**Covers:** debugging comparison

## Documentation and support, plus compliance deferral

- Vapi: 2 — "Not everything is documented, but 99% or more," plus usually helpful Discord replies.
- ElevenLabs: "not as great, unfortunately."
- Pipecat: huge community; "you can probably also sometimes get it from the CEO himself. So, awesome."
- Retell: "not always as easy."
- LiveKit: 2 — "huge amount of community and in general support."
- Telnyx: 1 — docs "still lacking a little bit" and unclear where to insert things in certain cases, compounded by weak support.
- Compliance/regulation: explicitly deferred — "most important, actually, but I'm not going to answer it here because I'm going to make another video," citing its size and "couple different platforms very specific to this issue."
- Closing caveat: scores understate ElevenLabs for small and probably medium businesses; Pipecat "for small businesses, not really"; LiveKit "incredibly solid" with "awesome" speech detection; Resemble.ai noted as strong on complex features and API despite observability gaps.

**Covers:** docs/support comparison, compliance deferral, closing reflections

**Covers:** chunk 01-hi-my-name-is-piotr-i-m, tier-list intro through SMB-weighted rubric and Vapi/LiveKit/Retell/ElevenLabs/Telnyx/Pipecat comparison
