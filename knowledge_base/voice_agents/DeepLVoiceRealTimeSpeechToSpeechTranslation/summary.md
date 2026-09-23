# DeepL Voice: Real-Time Speech-to-Speech Translation | IJCAI

**Article:** [DeepL Voice: Real-Time Speech-to-Speech Translation](https://doi.org/10.24963/ijcai.2026/962) — IJCAI Proceedings, Demo Track, 2026

## Human Readable TL;DR

Imagine a business video call where everyone speaks a different language yet hears each other almost instantly, like having an invisible interpreter whispering in your ear without ever interrupting. DeepL Voice is that interpreter built as a product: it listens with its own live transcription engine, translates steadily without the words flickering and rewriting themselves, and speaks across 18 input and more than 30 output languages. It plugs into everyday tools like Teams, Zoom, and mobile apps so global meetings just flow. The more futuristic touches, like speaking in your own cloned voice, are still being built in the lab.

## TL;DR

DeepL Voice is a production-grade cascaded real-time speech-to-speech translation system for global business communication, launched in November 2024, built on proprietary real-time ASR models described as delivering competitive transcription quality. Its translation layer uses stable text streaming that eliminates translation flickering while maintaining low latency, supporting 18 input languages and 30+ target languages. The system ships as three offerings — DeepL Voice for Meetings (Microsoft Teams/Zoom integration), DeepL Voice for Conversations (mobile apps), and the DeepL API for Voice — with customizable formality and glossary support for business-appropriate communication and voice-cloning TTS still under development. The stated strategy is pragmatic and incremental: operate a cascaded system in production now while exploring end-to-end solutions in parallel.

---

## Problem & Motivation

Global business communication breaks down when participants do not share a language, and real-time meetings demand translation that is both fast and stable enough not to distract. Flickering translations that constantly rewrite themselves, weak transcription, and tools that do not fit existing meeting workflows all make live speech translation unusable in practice. DeepL Voice is motivated by this product gap rather than a purely algorithmic one: deliver a production-grade system that businesses can already use in calls, conversations, and APIs, while continuing to explore end-to-end approaches in parallel instead of waiting for them to mature.

---

## Main Original Ideas

1. **Pragmatic incremental strategy** — Rather than betting the product on exploratory end-to-end speech translation, DeepL Voice ships a production-grade cascaded speech-to-speech system now and investigates end-to-end solutions in parallel, trading research novelty for deployability and reliability in business settings.

2. **Proprietary real-time ASR foundation** — The system grounds translation quality in its own proprietary real-time automatic speech recognition models, which are described as achieving competitive transcription quality, so downstream translation starts from a strong live transcript.

3. **Stable low-latency translation streaming** — The translation layer streams text in a stable form that eliminates the flickering rewrites common in live translation while keeping latency low, addressing the readability and trust problem that makes unstable live captions hard to follow in meetings.

4. **Business-ready product family** — The work packages the technology as three concrete offerings, namely DeepL Voice for Meetings integrated with Microsoft Teams and Zoom, DeepL Voice for Conversations delivered through mobile apps, and the DeepL API for Voice, so the same core system covers scheduled meetings, in-person dialogue, and programmatic use.

5. **Business-appropriate output controls** — Customizable formality and glossary support let organizations tune translations to the right tone and terminology, treating enterprise acceptability as a first-class feature alongside speed and coverage, with voice-cloning TTS positioned as the next step still under development.

---

## Key Findings

The system reached production status with a November 2024 launch and is presented as a deployed solution for global business communication rather than a prototype. It supports 18 input languages and more than 30 target languages, a breadth that covers the mainstream meeting scenarios the product targets. Transcription quality is reported as competitive via the proprietary real-time ASR models, and the stable streaming design is reported to remove translation flickering without sacrificing low latency. The three delivery surfaces of Meetings, Conversations, and API show the same core pipeline working across conferencing integrations, mobile interaction, and developer access. Voice-cloning text-to-speech remains unreleased, confirming that output speech personalization is future work rather than a current claim.

---

## Suggestions & Future Directions

The clearest stated direction is completing the voice-cloning text-to-speech capability so translated speech can preserve the speaker's voice character, which would close the loop from input speech to natural-sounding output speech. A second direction is the parallel exploration of end-to-end solutions, which could eventually replace or complement the cascaded pipeline if they prove production-ready on latency, stability, and quality. Further work naturally includes extending language coverage, hardening business controls such as formality and glossaries, and deepening integration with meeting and conversation workflows as deployment experience accumulates.

---

## Authors & Institutions

Johannes Ernesti, Peter Kaiser, Jonas Heinze, Elnaz Shafaei-Bajestan, Kristina Geißler, Weiyue Wang, Johannes Beck, Sascha Brinker, and Thorben Finke, presented in the Demo Track of the Proceedings of the Thirty-Fifth International Joint Conference on Artificial Intelligence (pages 8385–8388); institutional affiliations are not listed in the verified wiki pages.
