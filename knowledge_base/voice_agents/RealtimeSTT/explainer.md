> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# KoljaB/RealtimeSTT — In Plain Language

## What is this about?

RealtimeSTT is a Python library that turns spoken words into written text, live.

Think of it as a smart microphone helper: you speak, and it hands your
program back the words — either once per sentence or word-by-word as you talk.

In just a few lines of code, a developer can build an app that listens on
the microphone, waits for someone to speak, and prints out what was said.

It also works without a microphone: an app can push sound chunks into it
from a file, a stream, a web call, or another program, and get text back.

Under the hood it combines three jobs: noticing when someone is speaking,
converting that speech to text, and optionally waking up only when it hears
a magic word like "Hey computer."

For bigger setups, it ships an optional production server so web browsers
can stream audio over the network and get transcripts back.

## Why does it matter?

Most voice apps are hard to build because audio is messy and continuous.

People pause, mumble, interrupt each other, and leave long silences. A good
voice tool must know when speech starts and stops, keep up without long
delays, and not confuse background noise for talking.

RealtimeSTT matters because it packages all of that plumbing into one
simple thing: an `AudioToTextRecorder` object with a `text()` method.

Instead of wiring up audio drivers, timers, speech models, and networking
by hand, a hobbyist can prototype a voice assistant in an afternoon, and a
team can run the same idea as a shared network service.

It also matters because computers differ: some have powerful graphics cards
(GPUs), others have plain CPUs. RealtimeSTT offers a recommended setup for
each, so the app stays fast in both cases.

Finally, it supports live updates plus a careful final answer: you see quick
draft words while talking, then one clean authoritative sentence at the end.

## How does it work?

Picture an assembly line with four stations.

1. **Listen.** The library either opens your microphone or accepts sound
   chunks you feed it. The sound must be simple pulse audio: 16-bit, one
   channel, 16,000 samples per second — or it resamples it for you.

2. **Notice speech.** A voice activity detector watches the stream and
   marks "someone is talking" versus "silence." It uses proven detectors
   called WebRTC VAD and Silero VAD, so it does not transcribe empty air.

3. **Transcribe.** Once speech is detected, a speech-to-text engine turns
   sound into words. The default engine is called `faster_whisper`, a good
   all-around choice, especially with a GPU.

   On plain CPUs, the recommended pair splits the job: a small fast model
   (Nemotron streaming) shows live draft words from only the newest sound,
   and a second model (Parakeet) reads the whole sentence once at the end
   for the final high-quality result. This avoids re-reading everything
   over and over.

4. **Wake up and report.** Optionally, the library sleeps until it hears a
   wake word, using Porcupine or OpenWakeWord. Along the way it fires event
   callbacks — small "hey, this happened" messages for recording started,
   speech detected, live words ready, final sentence ready, or wake word
   heard — so your app can react.

For web use, the packaged FastAPI server does the same thing over the
network. It keeps each visitor's session separate, limits how many heavy
AI jobs run at once, checks health and capabilities, locks to the local
machine by default, and requires a secret token plus encryption for
outside access.

## Where can this be used?

- **Voice assistants.** A home robot or desktop helper that listens for a
  wake word, then answers questions or runs commands.

- **Dictation tools.** Speak instead of type: notes, emails, or documents
  appear as continuous text with live feedback.

- **Browser voice apps.** A website streams microphone audio to the
  production server over WebSockets and shows captions or commands in
  real time.

- **Hands-free prototypes.** Quick experiments — a workshop demo, a student
  project, or a hackathon idea — where speech input is needed in a few
  lines of Python.

- **Call and meeting helpers.** Feeding recorded or streamed call audio in
  from another process to get transcripts without touching a microphone.

- **Accessibility tools.** Live captions for people who prefer reading over
  listening, running locally for privacy.

## Conclusions & takeaways

RealtimeSTT is best understood as "speech-to-text with the boring parts
already solved": listening, speech detection, fast drafts, clean finals,
wake words, and a network server.

Its big idea is two-speed transcription: show fast rough words instantly,
then commit one careful final sentence. That gives both speed and trust.

Its second big idea is choice with sane defaults: beginners get a simple
default that works, while production users get a tuned CPU or GPU recipe
and a hardened server with sessions, limits, and authentication.

If you remember one thing: it turns a microphone or a stream of sound
chunks into text events your program can use, in a handful of lines.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Speech-to-text | Turning spoken audio into written words. |
| Voice activity detection (VAD) | The skill of telling "person talking" apart from silence or noise. |
| Transcription engine | The AI model that actually converts sound into text. |
| `faster_whisper` | The default all-around engine; fast and good, great with a GPU. |
| Realtime / live transcript | Rough draft words shown while you are still speaking. |
| Final transcript | The single clean, checked sentence delivered when you finish. |
| Wake word | A trigger phrase like "Hey assistant" that wakes the listener up. |
| PCM audio (16-bit mono, 16 kHz) | Plain raw sound data: simple, uncompressed, one channel, standard quality. |
| FastAPI server | A network service that lets browsers send audio and receive text. |
| Session isolation | Keeping each user's audio and results separate and private. |
| Bearer token / TLS | A secret password plus encryption to keep network voice traffic safe. |
| CPU vs GPU profile | Two tuned setups: one for ordinary processors, one for graphics cards. |
