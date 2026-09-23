> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# awesome full duplex speech-to-speech — In Plain Language

This is a plain-language guide to a curated survey of full-duplex
speech-to-speech conversational models (Cyrta 2026 v0.1.0).

It explains the big idea in everyday words: how voice AI is learning
to listen and talk at the same time, just like people do.

## What is this about?

Imagine talking to a voice assistant today. You speak, then you wait.
It thinks, then it answers. You cannot interrupt it, and it cannot
jump in while you are talking. That is turn-based conversation.

This guide is about the opposite: full-duplex speech-to-speech.

"Full-duplex" simply means both directions at once. The AI keeps
listening continuously while it is speaking, so you can interrupt it,
talk over it, say "uh-huh" or "yeah," and it reacts naturally.

The survey collects everything researchers have learned about this
new style of voice AI in one place: the models, how speech is
represented inside them, the datasets they learn from, the benchmarks
used to test them, the open challenges, key publications, learning
materials, workshops, and open-source and commercial projects.

In one sentence: it maps the shift from "you talk, then I talk" voice
bots to "we talk together" voice companions.

## Why does it matter?

Because turn-taking feels robotic, and real conversation does not work
that way.

When humans talk, we overlap, we nod with little sounds like "mm-hm,"
we stop each other mid-sentence, and we take turns smoothly without
pressing a button or waiting for silence. Today's classic voice
assistants cannot do any of that. They force us to slow down and speak
in rigid blocks.

True full-duplex communication fixes that gap. The survey calls it a
critical milestone toward human-like interaction: simultaneous
listening and speaking with natural turn-taking, overlapping speech,
backchanneling, and interruptions.

It matters for three practical reasons:

1. It is faster and less frustrating. No more waiting through a long
   answer you already want to cut off.
2. It is more accessible and natural. Hesitations, overlaps, and quick
   "yes, go on" signals just work.
3. It unlocks new products. Hands-free helpers, live translators, and
   phone agents all feel far more trustworthy when they converse like
   a person rather than a walkie-talkie.

The timing matters too. Since about 2022–2023 this idea moved from a
research dream to real systems people can try, so someone needed to
organize the fast-moving landscape. That is what this guide does.

## How does it work?

The old way is a relay race with three runners, called a cascade
pipeline:

1. Speech-to-text writes down what you said.
2. A language model thinks up a text reply.
3. Text-to-speech reads that reply out loud.

Each step waits for the previous one to finish. That is why the old
style is called half-duplex: listen, then think, then speak, repeat.

The new way is more like a jazz duet. One unified model does the
listening and the speaking in parallel, inside the same continuous
loop.

Instead of waiting for silence, it processes audio as an ongoing
stream. While it generates its own voice, it keeps one "ear" open for
yours. If you start talking, it notices immediately and can pause,
yield the floor, keep going, or slip in a quick "yeah" — just as the
situation calls for.

Landmark systems showed this is possible: Moshi from Kyutai (2024),
the SyncLLM framework from Meta AI and UW (2024), GPT-4o Realtime
from OpenAI (2024), and Gemini Live from Google DeepMind (2025).

Under the hood, researchers had to rethink several pieces together,
which is why the guide tracks them separately:

- Models: the unified architectures that listen and speak at once.
- Audio and speech representations: how raw sound is turned into a
  compact form the model can reason with and speak back from.
- Datasets: recordings of overlaps, interruptions, and backchannels
  the models learn natural timing from.
- Benchmarks: tests that measure interruption handling, turn-taking
  smoothness, and responsiveness, not just word accuracy.
- Challenges, publications, and projects: what is still hard, who
  wrote it up, and what code or products already exist.

## Where can this be used?

Anywhere people talk to machines with their voice and expect a natural
rhythm:

- Everyday voice assistants that you can interrupt with "stop" or
  "actually, I meant…" without repeating yourself.
- Customer-service phone bots that handle overlapping speech instead
  of talking over callers or freezing at the slightest noise.
- Live translation and meeting helpers that murmur acknowledgments
  while the other person is still speaking.
- Hands-busy settings — driving, cooking, care work — where pressing
  a button or waiting politely is impractical.
- Companionship and coaching tools, language tutors, and accessibility
  aids, where a warm, responsive pace builds trust.
- Research and product teams, who use the guide's lists of models,
  datasets, benchmarks, and open-source projects to pick a starting
  point instead of hunting scattered papers.

The short version: if a half-duplex bot feels like a walkie-talkie,
a full-duplex one aims to feel like a phone call.

## Conclusions & takeaways

- Human-like voice AI needs both ears and mouth open at once: listen-while-speaking.
- End-to-end full-duplex models replace the three-step cascade with
  parallel listening and generating in one loop.
- The field tipped around 2022–2023, and Moshi, SyncLLM, GPT-4o
  Realtime, and Gemini Live proved it works outside the lab.
- Progress depends on the whole stack together: models, representations,
  datasets with real messiness, and benchmarks that reward good timing.
- This survey does not invent a new model. Its value is as a map: one
  curated place to find the pieces, the people, and the open problems.
- Expect the payoff in everyday talk: interruptible, backchanneling,
  fast-yielding voice agents that feel polite rather than robotic.

## Jargon decoder

| Term | What it really means |
| ---- | -------------------- |
| Full-duplex | Listening and speaking at the same time, like a phone call. |
| Half-duplex | Taking turns: listen, then think, then speak, like a walkie-talkie. |
| True Full-Duplex (TFD) | The full package: overlap, interruptions, and smooth turn-taking all working. |
| Speech-to-speech (S2S) | Voice in, voice out — no typing needed on either side. |
| Cascade pipeline | The old three-step chain: speech-to-text, then chatbot, then text-to-speech. |
| FD-SLM / FD-SpeechLLM | One unified AI model that listens and talks in parallel. |
| Backchanneling | Little listener sounds like "uh-huh" that say "I'm following you." |
| Turn-taking | How speakers smoothly hand the conversation back and forth. |
| Representation | How sound waves are converted into compact numbers the AI can work with. |
| Benchmark | A standardized test that scores how well a system handles real conversation. |
