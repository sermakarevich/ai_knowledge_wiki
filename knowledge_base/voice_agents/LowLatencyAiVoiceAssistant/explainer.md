> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Ankur2606/Low-latency-AI-Voice-Assistant — In Plain Language

## What is this about?

This project is a do-it-yourself voice assistant you can talk to out loud.

You speak into your microphone, it writes down what you said,
thinks up a short reply, and then speaks that reply back to you.

Think of it like a very simple version of Siri or Alexa,
but built from open parts you can see, change, and run yourself.

It has two ways to use it: a terminal mode where you just talk
in a loop until you say "stop", and a web page with a button
you press to start speaking and a visible chat history.

There is nothing magical here — it chains three ready-made tools
together: one for hearing, one for thinking, and one for speaking.

## Why does it matter?

Normal voice assistants are closed boxes: you cannot see how they work
or change how they behave.

This project matters because it shows the whole recipe in the open,
using free and widely available building blocks.

It also cares about speed. A voice assistant feels broken if it pauses
for several seconds before answering, so this project is designed
around keeping replies fast and short.

The answers are deliberately capped at about two sentences,
so the assistant feels snappy instead of rambling.

It also lets you adjust the voice itself — higher or lower pitch,
faster or slower speech, male or female voice — which makes the same
assistant usable for different tastes and needs.

## How does it work?

The assistant runs in a five-step loop every time you speak.

First, it listens to your microphone but ignores silence.
A gatekeeper step called voice activity detection decides
whether anyone is actually talking, so background quiet is skipped.

Second, it turns your speech into text using a small, fast model
from the Whisper family. It listens at telephone-like quality
(16 kHz, single channel), which is enough for speech and keeps
the work light.

Third, it sends that text to a language model that writes a short reply.
The reply is capped at roughly 60 tokens, or about two sentences,
so answers stay brief and quick to generate.

Fourth, it turns the reply text back into spoken audio.
By default it uses a cloud voice service, but the terminal mode
can switch to a local streaming voice engine instead,
which reads the reply straight to your speakers.

Fifth, it plays the audio back to you, saves both sides of the exchange
in a conversation history, and goes back to listening.

Under the hood, it uses tricks like threading, pipelines, and handing
transcribed text to the next step without waiting, all aimed at keeping
total delay under about half a second.

You need only two secrets to run it: API keys for the language-model
services, stored in a private file. The rest is a pinned list of Python
packages plus a few audio system libraries for microphone support.

## Where can this be used?

Anywhere you want a simple talk-in, talk-back helper.

A hobbyist can use it as a starting point for a custom home assistant,
a study aid that reads answers aloud, or a hands-free helper
while cooking, driving, or working at a bench.

A student can use it to learn how voice systems fit together,
because each stage — hearing, thinking, speaking — is a separate
module that can be swapped or experimented with.

A prototype builder can use it to demo a voice interface quickly:
press a button on a web page, speak, and hear a reply, with the
voice style adjustable on the spot through sidebar sliders.

It also works as a test bed for low-latency ideas, such as shorter
answers, smaller speech models, and local versus cloud voices,
before committing to a bigger production system.

## Conclusions & takeaways

The big idea is simple: a usable voice assistant is just three steps
in a loop — hear, think, speak — plus careful attention to speed.

Short answers are a feature, not a limitation: capping replies keeps
the conversation feeling live and natural.

Ignoring silence early saves work later, and small efficiency choices
(streaming, threading, light audio settings) add up to a system
that feels responsive.

Finally, offering two front ends — a plain terminal loop and a friendly
web page — makes the same engine approachable for both tinkerers
and non-technical users.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Voice Activity Detection (VAD) | A gatekeeper that checks whether anyone is actually speaking, so silence is ignored. |
| Speech-to-Text (STT) | Turning spoken words from the microphone into written text the computer can process. |
| Text-to-Speech (TTS) | Turning written reply text back into a spoken voice you can hear. |
| Large Language Model (LLM) | The "brain" step: software that reads your words and writes a human-like reply. |
| Whisper / faster-whisper (tiny) | A small, fast version of a speech-recognition model used here to transcribe your voice. |
| Edge-TTS | A cloud service that converts text into natural-sounding speech. |
| Kokoro-82M | An alternative local voice engine that speaks without sending text to the cloud. |
| Token | A small chunk of text the language model reads or writes; 60 tokens is roughly a sentence or two. |
| Streamlit | A toolkit for building the project's simple web page with a button, sliders, and chat history. |
| Latency | The delay between you finishing a sentence and hearing the assistant's reply. |
