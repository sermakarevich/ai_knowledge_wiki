> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# AreevAI/flowcat — In Plain Language

## What is this about?
Flowcat is a toolkit for building voice agents — programs you can
talk to over a phone call or a browser microphone — written in Rust.

The big idea is simple: everything a call needs lives in one
self-contained program running on your own servers, with no outside
control panel or cloud service in the middle.

When someone speaks, their audio travels down a step-by-step assembly
line: it comes in over some connection, the system figures out when
the person starts and stops talking, converts speech to text, asks a
language model what to say back, converts that answer back to speech,
and plays it to the caller.

If you prefer, you can swap that whole chain for a single
speech-to-speech model that listens and talks directly.

Flowcat is deliberately modeled on an existing Python project called
pipecat, so it feels familiar to people who know that world — same
idea of small processing steps passing typed messages along — but it
is written from scratch in Rust and ships as one fast binary.

Out of the box it includes nothing that talks to the network.
Every outside service — each speech, language, or phone provider —
is an optional add-on you switch on only when you need it.

## Why does it matter?
Running voice agents on phone calls raises three hard problems,
and Flowcat tackles each one head-on.

First is privacy and control. For hospitals, banks, and other
regulated callers, audio and transcripts cannot leave their own
computers. Flowcat runs entirely inside your own network, reads only
its own settings, talks only to providers you configured, and can
even run fully offline with local speech and language models.

Second is cost on long calls. Keeping every minute of past audio
around for the model to re-listen to is expensive. Flowcat's
ContextRelay trick converts old audio context into a short written
summary and feeds the model cheap text instead — roughly seven times
smaller and four times cheaper per unit — while keeping the whole
conversation in mind. It is off by default and works with any provider.

Third is scale. The classic Python approach starts to wobble after
a few hundred simultaneous calls. In the project's own benchmark,
one Flowcat process held steady with flat, sub-millisecond internal
overhead from 10 all the way to 2,000 simultaneous calls on a single
machine, while actual conversation speed still depends on the outside
speech and language providers, which take hundreds of milliseconds.

In short: your infrastructure stays yours, long calls stay affordable,
and one machine goes a long way.

## How does it work?
Picture a phone call as water flowing through pipes.

Audio flows in through a connection — a phone carrier, a browser
voice link, or a plain WebSocket — and each processing step is a
small station along the pipe: detect voice activity, transcribe it,
think of a reply, speak the reply, send it back out.

Each station runs as its own lightweight task and hands neat,
labeled packets to the next station over a bounded queue, so a slow
station cannot flood the rest.

A supervisor drives the whole line, and it knows how to interrupt
politely: if the caller starts talking over the agent, the system
can stop the playback and listen again, just like a human would.

Long-call memory works like a secretary's notes. Instead of replaying
hours of tape, ContextRelay writes down what was said so far as
compact text and hands the model the notes. The live conversation
sounds exactly the same; only the model's reminder is cheaper.

Under the hood the code is split into clean boxes: the core pipeline
framework, the outside provider clients, the connection types, the
phone-carrier message translators, the conversation-brain logic, and
a small demo program. The core box knows nothing about your website
or database — it only talks through narrow plugs, so you can embed
it in any application.

Adding a new provider follows a simple recipe: either it speaks a
genuinely new network protocol and needs a real new client, or it
speaks the same protocol as an existing family and needs only a tiny
adapter with a different address and login. Either way it stays
behind its own on/off switch, so the default build stays lean.

## Where can this be used?
Anywhere a computer needs to hold a spoken conversation that you
fully control.

The most natural fit is phone support lines: a caller dials a normal
number, the carrier forwards the audio to your Flowcat server, and
the agent answers, listens, and responds — all inside your network.

Browser-based voice chat works too: open a web page, grant the
microphone, and talk to an agent served by the included server
program, which reads a simple config file describing the
conversation setup.

Because it can run air-gapped with local models, it suits clinics,
banks, government helplines, and other places where recordings must
never leave the building.

Developers can steer the agent's decisions from Python without
touching the fast audio path: the agent's "brain" can be a small web
service that gets asked what to do at each turn, while the audio
keeps flowing untouched in Rust.

And because each provider is optional, the same core can serve a
tiny offline demo on a laptop or a big deployment talking to dozens
of commercial speech and language services.

## Conclusions & takeaways
Flowcat is best understood as "own your voice stack": one Rust
program, your servers, your providers, your rules.

Its three signature moves are the composable audio pipeline with
polite interruption, the ContextRelay notes-instead-of-tape memory
saver, and the everything-is-optional packaging that keeps the
default build tiny while still offering dozens of providers.

The honest caveats: conversation speed is still set by the outside
speech and language services, not by Flowcat itself, and many of the
provider integrations are tested against saved message samples
rather than live-verified calls.

If you need a private, scalable, provider-flexible voice agent
runtime — and you like the pipecat mental model but want a single
Rust binary — this is exactly that.

## Jargon decoder
| Term | What it really means |
| --- | --- |
| Voice agent | A program you talk to out loud that talks back, over phone or browser |
| Pipeline | The assembly line of steps audio passes through, from microphone to reply |
| VAD / turn-taking | Detecting when the caller starts and stops speaking, so nobody talks over anyone |
| STT | Speech-to-text: turning spoken audio into written words |
| TTS | Text-to-speech: turning written words into spoken audio |
| LLM | The language model that reads the transcript and decides what to say next |
| Speech-to-speech model | One model that listens to audio and talks back directly, skipping the text middle steps |
| ContextRelay | Flowcat's trick of swapping old audio history for short text notes to save cost |
| Transport | The connection carrying audio in and out, such as phone, browser voice, or WebSocket |
| Cargo feature | An optional on/off switch at build time that pulls in one provider or connection type |
