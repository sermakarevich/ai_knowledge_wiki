---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: awesome full duplex speech-to-speech

### Q1. What is full-duplex speech-to-speech processing as defined in this guide?

> [!tip]- Answer
> Full-duplex S2S models process audio continuously, listening and speaking simultaneously without waiting for the user to finish. This continuous simultaneous loop is the defining break from turn-based voice systems. It is what enables the system to react mid-utterance rather than only at turn boundaries. See [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]].

### Q2. How does the guide contrast cascade pipelines with end-to-end full-duplex models?

> [!tip]- Answer
> Traditional cascade pipelines run Speech-to-Text → LLM → Text-to-Speech as sequential staged handoffs. End-to-end full-duplex models replace that chain with a unified simultaneous loop of parallel encoding and generation. The payoff is active listening, natural interruptions, and instantaneous human-like backchanneling. See [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]].

### Q3. What does True Full-Duplex (TFD) voice communication mean, and why is it a milestone?

> [!tip]- Answer
> TFD means simultaneous listening and speaking with natural turn-taking, overlapping speech, backchanneling, and interruptions. The guide frames it as a critical milestone toward human-like interaction. It marks the point where conversational AI stops enforcing rigid wait-your-turn exchanges. See [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]].

### Q4. What is the technical difference between half-duplex systems and full-duplex spoken language models?

> [!tip]- Answer
> Half-duplex (turn-based) systems are constrained by sequential listen-think-speak cycles that handle one direction at a time. Full-duplex spoken language models (FD-SLMs / FD-SpeechLLMs) instead enable parallel encoding and generation within unified processing cycles. That parallelism lets the model keep hearing incoming speech while it is already speaking. See [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]].

### Q5. Which systems does the guide credit with the field's paradigm shift since 2022–2023?

> [!tip]- Answer
> The guide credits Moshi (Kyutai, 2024) and the SyncLLM framework (Meta AI / UW, 2024) on the research side. It pairs them with commercial deployments GPT-4o Realtime (OpenAI, 2024) and Gemini Live (Google DeepMind, 2025). Together these turned full-duplex conversation from research idea into deployed reality. See [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]].

### Q6. What landscape does the guide's table of contents cover, and what is actually in this chunk's tables?

> [!tip]- Answer
> The scope spans models, audio and speech representations, datasets, benchmarks, challenges, publications, other learning materials, workshops/special sessions, open-source projects, and commercial products. In this chunk those sections hold only placeholder lines such as "Table with models listed historically" with no rows or entries. The work is versioned Cyrta 2026 v0.1.0 (accessed 2026-05-28) with DOI badge 10.5281/zenodo.20432560. See [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]].

### Q7. A newcomer asks whether to start from this guide before building a barge-in-capable voice agent — what do you recommend and why?

> [!tip]- Answer
> I would recommend it as an entry map because its table of contents spans the full stack from representations and models to datasets, benchmarks, and commercial products. But I would warn that this chunk is only the overview shell with empty placeholder tables, so the newcomer should verify the linked sections have real depth. Starting here for orientation is sound, yet architecture decisions should rest on the filled-in sources, not this skeleton alone. See [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]].
