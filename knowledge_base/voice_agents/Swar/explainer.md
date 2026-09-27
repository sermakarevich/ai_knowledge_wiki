> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# vivekananda-2201/Swar — In Plain Language

## What is this about?
Swar is a free, open-source toolkit for talking to a computer by voice.

Think of it as the "conversation manager" between your microphone,
your smart assistant software, and your speakers.

It runs entirely offline on an ordinary laptop CPU — no expensive
graphics card and no cloud service required.

Under the hood it connects three ready-made building blocks:
one that detects when someone is speaking, one that turns speech
into text, and one that turns text back into spoken replies.

You start it from a simple command (`run.py`), tune it through
one settings file (`config.yaml`), and import it in Python
through a single front door (`swar.py`).

## Why does it matter?
Most voice assistants work like a walkie-talkie: you talk, then wait,
then it thinks, then it talks, and you cannot interrupt.

Real human conversation does not work that way. We interrupt,
we talk over each other, and we expect instant reactions.

Swar matters because it makes computer conversation feel natural:
it listens and speaks at the same time, shows what it hears while
you are still talking, and lets you cut it off cleanly.

It also matters for privacy and cost. Because everything runs on
your own machine, your voice never has to be sent to the internet,
and you do not need costly hardware or subscriptions.

Measured results on a mid-range laptop show the assistant starting
to answer in roughly 0.6 to 2.4 seconds, and interruptions cutting
in within about 21 milliseconds without crashing the audio system.

## How does it work?
Imagine an assembly line where every worker runs at the same time
instead of waiting for the previous one to finish.

First, the microphone captures sound. A speech detector watches
the stream and decides "someone started talking" or "they went quiet."

Second, while you are still speaking, a speech-to-text worker writes
down a running draft of your words, updating about twice per second.
You see the guess improve live instead of waiting for silence.

Third, when you finish, the final sentence passes through two filters:
a wake-word checker ("was I actually being addressed?") and a cleanup
filter that hides the AI's private thinking notes so they are never
spoken out loud.

Fourth, your words go to any chatbot brain — local or online.
As the answer streams back, Swar slices it into sentences.

Fifth, a two-worker speaking system takes over: one worker prepares
the audio for the next sentence in the background while the other
worker plays the current sentence through the speakers.

Two safety nets keep interruptions smooth: a tiny cutoff switch stops
playback within milliseconds when you barge in, and a short memory
buffer saves the first words of your interruption so nothing gets lost.

A final guard solves the "talking to itself" problem: a small voice
checker recognizes the computer's own voice coming through the
speakers so it does not mistake itself for a human and interrupt itself.

## Where can this be used?
- A private voice assistant on a laptop or home computer with no internet.
- Hands-free control for workshops, kitchens, or accessibility setups.
- Customer-service or reception kiosks that need natural interruptions.
- Robots, smart-home hubs, and hobby electronics running on modest CPUs.
- Language practice or reading-aloud tools where live transcription helps.
- Research prototypes measuring voice speed: time to first word,
  speaking speed, and interruption delay.

## Conclusions & takeaways
Swar's big idea is simple: good voice interaction is about timing
and coordination, not just accurate transcription.

By running listening, understanding, and speaking at the same time —
and by handling interruptions gracefully — it feels far more human
than the classic wait-your-turn pipeline.

Its trade-off is complexity behind the scenes: several models and
background workers must cooperate. But for the user, that complexity
is hidden behind one command and one settings file.

If you want private, low-cost, interruptible voice chat on hardware
you already own, this is a practical starting point.

## Jargon decoder
| Term | What it means in plain language |
| :--- | :--- |
| Full-duplex runtime | Listening and speaking happen at the same time, like a phone call, not a walkie-talkie. |
| Speech detection (VAD) | The part that notices "someone started talking" versus background silence. |
| Speech-to-text (STT) | The part that converts your spoken words into written text. |
| Text-to-speech (TTS) | The part that converts written answers into a spoken voice. |
| Barge-in / interruption cutoff | Stopping the computer mid-sentence when you start talking, within milliseconds. |
| Wake word | A trigger phrase like "hey assistant" that tells the system it is being addressed. |
| Turn buffer | A short memory that keeps your first words safe when you interrupt. |
| Speaker echo guard | A check that stops the microphone from reacting to the computer's own voice. |
| Time-to-first-audio | How long you wait from finishing your sentence until you hear a reply start. |
| Offline / CPU-first | Everything runs privately on your own processor, with no internet or graphics card needed. |
