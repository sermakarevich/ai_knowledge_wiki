> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Project Aether — In Plain Language

## What is this about?

Project Aether is an experiment that asks a simple question:
can a normal laptop hold a natural phone-style voice conversation
with an AI — listening and speaking at the same time?

The answer it demonstrates is yes, on one ordinary machine:

an RTX 3050 laptop GPU with only 6 GB of video memory.

There is no cloud server doing the heavy work.
Everything runs locally: hearing you, understanding you,
thinking of a reply, and speaking it back.

The trick is that talking and listening happen simultaneously.
You can interrupt the AI mid-sentence, just like you would
interrupt a person, and it actually stops and listens.

That style is called full-duplex: audio flows in both directions
at once, instead of walkie-talkie style "you talk, then I talk."
The project got there in eleven validated steps (AETHER-1…AETHER-11),
each testing one risk — memory, scheduling, hearing, interruption,
echo — and freezing one piece of the design.

## Why does it matter?

Most voice assistants cheat in one of two ways.

They either send your voice to the cloud, which costs money,
adds delay, and raises privacy questions, or they run locally
but force you to wait your turn, pressing to talk and waiting
for a reply.

Aether shows a third option: a fully local system that still
feels conversational, on hardware millions of people already own.
That matters for three reasons.

First, privacy and cost: your voice never has to leave the laptop.
Second, responsiveness: no network round-trip, so interruptions
are handled in tens of milliseconds, not the better part of a second.

Third, honesty about limits: instead of claiming "it just works,"
the project measures exactly where it breaks — GPU contention,
slow transcription, speaker echo — and fixes each one with data.

For anyone building voice products on a budget, that recipe
is more useful than a demo that only runs on a giant server GPU.

## How does it work?

Think of the system as a small team passing notes down a line.

Your voice enters through the microphone 24,000 times per second.
The first stop is an echo cleaner: because the laptop's own speaker
leaks into its microphone, the system subtracts its own playback
from what it hears, so the AI never mistakes itself for you.

The cleaned voice then splits into two paths.

The fast path is a loudness ear: a voice activity detector that
checks every 20 milliseconds, "did speech just start?"
It needs two frames in a row to be sure, so it answers in about
25–45 milliseconds, and it saves the previous 100 milliseconds
so the start of your word is never clipped.

The slow path is a transcriptionist: a speech recognizer called
Zipformer that runs on the CPU, not the GPU, with about 6% word
error rate. It is accurate and cheap, but slow — roughly 470
milliseconds to get ready and ~0.8 seconds to a useful partial.

A small controller combines both paths: the fast ear stops the AI's
speech almost instantly when you barge in, and the slow path follows
with the actual words. Resetting the transcriptionist takes under
a millisecond.

The brain is a 1.5-billion-parameter language model, Qwen2.5,
compressed to 4-bit precision so it fits on the small GPU.
The mouth is a neural audio codec called Mimi, streaming speech
in 80-millisecond chunks instead of waiting for whole sentences.

One referee keeps brain and mouth from tripping over each other on
the shared GPU. That scheduler, Cooperative Yielding, makes the
language model pause while each audio chunk is processed: zero missed
deadlines over 2,250 chunks in 60-second runs, versus delay spikes
near 99 milliseconds without coordination.

An early shortcut — "ignore echoes by volume" — blocked all echoes
but killed 65–73% of real interruptions, so it was replaced by the
real echo canceller: ~20 decibels of echo removed, 100% of tested
double-talk interruptions preserved.

## Where can this be used?

Anywhere a device should talk and listen naturally without the cloud.

On-device voice assistants on laptops, kiosks, robots, or cars,
where the network is slow, expensive, or untrusted.

Accessibility tools, such as conversational readers or companions
that must accept interruptions gracefully.

Privacy-sensitive settings — clinics, offices, homes — where sending
raw microphone audio to a server is undesirable.

Education and prototyping: because every benchmark script and report
is included, students and builders can rerun each AETHER step and
learn how memory, scheduling, transcription, and echo interact.

The envelope is honest: it is validated for a 6 GB laptop GPU with
16 GB of RAM, clean-speech transcription near 6% error, and echo
cancellation that needs 300–500 milliseconds to settle on startup.
Noisy stadiums and tiny embedded chips are outside that envelope.

## Conclusions & takeaways

Fitting the models in memory was the easy part — the system used
only about 1.6 GB of the 6 GB available.
Sharing the GPU fairly was the hard part, and scheduling fixed it.

Keeping transcription off the GPU kept the design stable even though
transcription stayed slow. Speed was recovered at the pipeline level:
react fast with the ear, understand slowly with the transcriptionist.

Echo cannot be solved with a cheap volume trick; it needs a real
adaptive canceller, and once added, the full stack tested as
production-ready within its stated limits.

The big lesson: natural-feeling voice AI on consumer hardware is less
about a bigger model and more about careful plumbing — measurement,
scheduling, and handling interruptions and echoes well.

## Jargon decoder

| Term | What it really means |
|------|----------------------|
| Full-duplex | Talking and listening at the same time, like a phone call |
| Barge-in | Interrupting the AI mid-sentence and having it stop and listen |
| Neural audio codec (Mimi) | The AI's mouth and ears: turns sound into tokens and back |
| LLM (Qwen2.5-1.5B) | The AI's brain: turns your words into a reply |
| Quantization (NF4 4-bit) | Shrinking the brain so it fits on a small GPU |
| ASR (Zipformer) | The transcriptionist: turns your speech into text |
| VAD | The fast ear: notices "someone started talking" in milliseconds |
| AEC | The echo cleaner: subtracts the speaker sound from the microphone |
| ERLE (~20 dB) | How much quieter the echo gets after cleaning — about 100x less power |
| Cooperative Yielding | A politeness rule: the brain pauses so audio chunks stay on time |
| WER (6.13%) | Transcription error rate: about 6 wrong words per 100 |
| RTF (0.0598) | Transcription speed: processes 1 second of audio in ~0.06 seconds |
