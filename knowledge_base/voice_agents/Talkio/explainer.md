> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Talkio — In Plain Language

## What is this about?

Talkio (pronounced "TAWK-yo", like "Tokyo" starting with "talk") is a small
TypeScript library for building voice agents — programs you talk to that
talk back, like a phone assistant or a voice chatbot.

A voice agent has three jobs: hear what you said (speech-to-text), decide
what to say next (a language model), and speak the answer out loud
(text-to-speech). Talkio does not do any of those three jobs itself.

Instead, Talkio is the coordinator in the middle. You plug in whichever
hearing, thinking, and speaking services you like, and Talkio manages the
hard middle part: whose turn it is to talk, what happens when someone
interrupts, how to cancel work that is no longer needed, and how to stream
audio so answers start playing quickly.

It is explicitly an early alpha, "vibe-engineered" experiment: good for
prototypes, not yet ready for production, with rough edges and an API that
may change.

## Why does it matter?

Building a voice agent sounds simple — record, transcribe, think, speak —
but the details are full of traps.

People interrupt. They pause mid-sentence without being finished. Answers
take too long to start, leaving awkward silence. When the user cuts in,
half-finished computer work (an answer being written, audio being made)
keeps running and collides with the new request. Several things happen at
once, and simple step-by-step code falls apart.

The usual fixes each demand a price: adopt a whole server setup, accept one
vendor's transport layer, lock yourself to one AI company, or pay per-minute
fees to a hosted platform that hides the details but limits your choices.

Talkio matters because it offers the opposite deal: a free, open-source
(Apache-2.0) coordination engine with no servers, no required vendors, and
no preferred transport. If you want full control over models and deployment
and only need someone to handle the conversation plumbing, that gap is what
Talkio fills.

## How does it work?

Think of Talkio as a stage manager with six assistants working at the same
time: one listens (speech-to-text), one watches for voice activity, one
decides when your turn is over, one asks the language model for a reply,
one turns reply text into audio, and one lines up that audio for playback.

You set it up in three steps. First, you bring your own providers — for
example, Deepgram for hearing and speaking plus any language model you
like. Second, you tell Talkio what to do with events: "when the person
finishes a turn, log it; when a bit of computer-spoken audio is ready, play
it." Third, you start the agent and feed it small chunks of microphone
audio as they arrive.

While the conversation runs, Talkio keeps a state machine — a strict map of
what is happening now (listening, transcribing, responding, streaming) — so
behavior stays predictable even when events overlap. If you start talking
while the agent is speaking, a two-layer detector notices: a fast voice
sensor reacts in about a tenth of a second, with the transcriber as backup,
ignoring blips shorter than 200 milliseconds. Talkio then cancels the old
reply, stops making its audio, clears the playback queue, and tidies up.

To keep things feeling fast, Talkio does not wait for the whole answer
before speaking. As soon as the first complete sentence exists, it starts
turning that sentence into audio while the rest is still being written. If
the agent needs time for a slow task, it can say a filler phrase out loud —
"Checking the weather in Tokyo..." — instead of leaving silence. Built-in
meters track how long the first word and first audio took, how many turns
finished or were interrupted, and where errors came from.

## Where can this be used?

Anywhere JavaScript runs and anywhere voice comes from: a website
microphone, a phone call, a mobile app, or a video-call audio track. It
runs on Node.js, Bun, Deno, and edge environments, and accepts audio over
WebSockets, streamed HTTP, or an external real-time connection.

Typical prototype uses: a voice demo on a website, a phone-tree experiment,
a hands-free helper inside an app, or the conversational backend behind a
larger hosted voice product. The worked example pairs Deepgram hearing and
speaking with a small chat model through a streaming helper library.

Pick Talkio when you are working in TypeScript, want to choose and swap
models freely, and want to deploy anywhere yourself. Pick something else
when you already live inside a video-call platform, need dozens of
ready-made provider plugins in Python, want a single vendor's guarded
real-time API, or would rather pay a hosted service to handle servers,
scaling, and phone lines for you.

## Conclusions & takeaways

Talkio splits the problem cleanly: models and microphones are yours,
conversation traffic control is its.

Its big ideas are bringing your own models, reacting to interruptions fast
but cancelling cleanly, speaking sentence by sentence to cut perceived
delay, narrating slow work with filler phrases, and measuring each turn so
you can see what is slow or broken.

The catch is maturity: a tiny early project with a handful of commits,
one provider package so far, custom-provider recipes for everything else,
and an honest warning not to trust it in production yet. Treat it as a
flexible prototype engine, not finished infrastructure.

## Jargon decoder

| Term | Plain definition |
| ---- | ---------------- |
| Speech-to-text (STT) | Technology that turns spoken audio into written words. |
| Language model (LLM) | The "thinking" service that writes the agent's reply text. |
| Text-to-speech (TTS) | Technology that turns reply text into spoken audio. |
| Turn-taking | Deciding when the person is done so the agent may reply. |
| Interruption handling | Noticing the person cut in and stopping the old reply. |
| Voice activity detection (VAD) | A fast sensor that notices "someone is speaking now." |
| State machine / actor | A strict map of allowed situations plus helpers that each manage one job. |
| Cancellation (AbortSignal) | A stop message passed everywhere so outdated work quits cleanly. |
| Sentence-level streaming | Speaking the first finished sentence before the full reply exists. |
| Filler phrase | A short spoken update ("Let me check...") covering a slow task. |
| Backpressure | Slowing or trimming audio output when playback cannot keep up. |
| Provider-agnostic | Works with any hearing, thinking, or speaking service you choose. |
