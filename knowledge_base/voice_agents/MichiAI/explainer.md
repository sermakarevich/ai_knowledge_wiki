> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# KetsuiLabs/MichiAI — In Plain Language

Think of MichiAI as a voice assistant that can talk and listen at the same time, like a person does — instead of waiting politely for you to finish every sentence before it even starts thinking.

## What is this about?

Most voice assistants today work like a relay race with three runners.

First, one program turns your speech into text. Then a chatbot thinks up a reply. Then a third program reads the reply out loud. Each step adds delay, and while the assistant is talking, it is effectively deaf.

MichiAI tries to collapse all of that into one compact model. It is a speech-focused language model with about 530 million parameters — small by modern standards — built on top of a small text model called SmolLM-360m.

Its headline promise is simple: you can interrupt it, it can hear you while it speaks, and it starts making sound about 80 milliseconds after it decides what to say (tested on an RTX 4090 graphics card).

It also copies a voice from just a few seconds of example audio, accepts a mix of typed text and spoken audio as input, and picks up human touches like laughing, breathing, and emotional tone.

## Why does it matter?

Normal conversation is full of interruptions, "uh-huh" sounds, and talking over each other. Today's assistants handle that badly because they take turns like walkie-talkies: you speak, then they speak, then you speak.

That turn-taking feels slow and robotic. It also needs big, expensive models to sound smart, because converting speech to text and back tends to throw away meaning and emotion.

MichiAI matters because it claims three things at once:

1. It is much smaller — 530 million parameters versus 7 to 8.5 billion for rivals like Moshi, Hertz-dev, and Qwen-Omni.
2. It trained on far less audio — around 5,000 hours versus millions of hours claimed for those rivals.
3. It supposedly keeps its reasoning ability instead of becoming dumber when speech is added, which is a common failure in speech-to-speech systems.

If those claims hold, you get a fast, cheap voice model that could run on modest hardware instead of a data center.

## How does it work?

Imagine two helpers sitting on either side of a small brain.

On the left is the "Listening Head." While you talk, it turns the raw sound of your voice into a rich internal sketch — not just the words, but the meaning and the mood behind them. It does this at the same time the brain is producing text, so listening never pauses.

In the middle is the familiar text brain, inherited from the SmolLM-360m model. Because MichiAI reuses a model that already understands language, it does not have to relearn grammar and reasoning from scratch.

On the right is the "Speaking Head." Instead of building sound from chunky digital tokens the slow way, it sketches smooth sound patterns directly and then hands them to a small, fast sound generator called a causal HiFi-GAN vocoder. That vocoder turns the sketch into actual audio quickly enough to stream in real time.

Two technical shortcuts make the speed possible:

- Continuous audio sketches instead of step-by-step token decoding, so fewer computation rounds are needed.
- A fast sound-shaping method called rectified flow matching, which produces varied, high-quality speech in one smooth motion rather than many small corrections.

The project also presents itself through a minimal documentation website, with build output kept out of version control — a small sign this is still an early, demo-stage project.

## Where can this be used?

Because it is small and fast, the natural uses are places where waiting even half a second feels wrong:

- Voice assistants and phone agents that need to handle interruptions gracefully.
- Live helpers for games, tutoring, or customer support that react while the user is still talking.
- Personalized narration and accessibility tools, since a few seconds of audio is enough to clone a voice.
- Apps that already combine documents and chat, because MichiAI accepts mixed text-plus-audio prompts that fit alongside retrieval-based assistants.
- On-device or low-cost setups where a 7-billion-parameter model would be too heavy or too slow.

The roadmap still lists bigger models, more languages, a live demo, and an API client as unfinished — so multilingual or production use would have to wait.

## Conclusions & takeaways

The big idea is refreshingly direct: stop chaining three slow programs together and build one small model that hears while it talks.

MichiAI's bet is that smooth sound representations plus a fast voice generator can beat giant models trained on vastly more data, at least for natural, low-delay conversation.

Take it as a promising early prototype, not a finished product. The documentation site is minimal, the demo and API are still on the to-do list, and the speed and quality numbers come from the project's own description.

If you remember one sentence: a tiny talk-and-listen-at-once voice model that answers almost instantly, copies voices from seconds of audio, and aims to stay smart while staying small.

## Jargon decoder

| Term | What it really means |
| :--- | :--- |
| Full-duplex | Can listen and speak at the same time, like a phone call, not a walkie-talkie. |
| ASR → LLM → TTS pipeline | The old three-step relay: speech-to-text, chatbot brain, text-to-speech. |
| Latency / TTFA | How long you wait before hearing the first sound; here about 80 milliseconds. |
| Continuous audio latents | A smooth internal sketch of sound, used instead of slow chunk-by-chunk codes. |
| RVQ (Residual Vector Quantization) | An older method of chopping audio into stacked digital tokens; accurate but slow. |
| Rectified flow matching | A fast technique for turning a rough sound sketch into natural speech in few steps. |
| HiFi-GAN vocoder | A small sound engine that converts the internal sketch into audible waveforms. |
| Zero-shot voice cloning | Copying someone's voice from just a few seconds of audio, with no extra training. |
| RAG (Retrieval-Augmented Generation) | Letting the model look up documents before answering, so replies stay factual. |
| Paralinguistics | The non-word parts of speech: laughter, breathing, sighs, emotional tone. |
| Coherence loss | When adding voice makes a smart text model dumber or more rambling. |
| Backbone model | The ready-made text brain (here SmolLM-360m) that MichiAI builds its voice skills on. |
