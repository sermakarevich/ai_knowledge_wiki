> [[index|Wiki]] | [[summary|Summary]]
# awesome full duplex speech-to-speech — Digest
## 1. [[wiki/01-awesome-full-duplex-speech-to-speech|Awesome Full-Duplex Speech-to-Speech]]
**In one sentence:** This chunk is the front matter and skeleton of a curated guide to full-duplex speech-to-speech conversational models, defining continuous simultaneous listening-and-speaking as the break from cascade pipelines and laying out empty-by-section tables for models, representations, datasets, benchmarks, challenges, publications, and open-source/commercial projects.
## Key points
- Full-duplex S2S models process audio continuously, listening and speaking simultaneously without waiting for the user to finish.
- Traditional cascade pipelines run Speech-to-Text -> LLM -> Text-to-Speech, while end-to-end full-duplex models enable active listening, natural interruptions, and instantaneous human-like back-channeling.
- True Full-Duplex (TFD) voice communication is defined as simultaneous listening and speaking with natural turn-taking, overlapping speech, backchanneling, and interruptions, and is framed as a critical milestone toward human-like interaction.
- Half-duplex systems are constrained by sequential listen-think-speak cycles, whereas full-duplex spoken language models (FD-SLMs / FD-SpeechLLMs) enable parallel encoding and generation within unified processing cycles.
- The field underwent a decisive paradigm shift since 2022–2023, accelerated by Moshi (Kyutai, 2024), the SyncLLM framework (Meta AI / UW, 2024), GPT-4o Realtime (OpenAI, 2024), and Gemini Live (Google DeepMind, 2025).
- The guide's scope covers models, audio and speech representations, datasets, benchmarks, challenges, publications, other learning materials, workshops/special sessions, open-source projects, and commercial products.
- The work is versioned as Cyrta 2026 v0.1.0 (accessed 2026-05-28, https://github.com/cyrta/awesome-full-duplex-speech-to-speech) with DOI badge 10.5281/zenodo.20432560.
## The argument in five moves
1. Human-like voice interaction requires true full-duplex communication — simultaneous listening and speaking with turn-taking, overlap, backchanneling, and interruption.
2. Legacy half-duplex cascade pipelines (STT → LLM → TTS) enforce sequential listen-think-speak cycles that block natural conversational behavior.
3. End-to-end full-duplex spoken language models replace the cascade with parallel encoding and generation in unified cycles, enabling continuous active listening.
4. Since 2022–2023, landmark systems (Moshi, SyncLLM, GPT-4o Realtime, Gemini Live) turned this paradigm from research idea into deployed reality.
5. Mapping the now-fast-moving landscape therefore demands a curated guide spanning models, representations, datasets, benchmarks, challenges, publications, and open-source/commercial projects.
