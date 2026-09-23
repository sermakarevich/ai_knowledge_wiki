> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# nari-labs/nari-qwen3-tts — In Plain Language

## What is this about?
This project is a ready-to-run way to turn text into spoken audio.

It takes one specific text-to-speech model — Qwen3-TTS 1.7B CustomVoice —
and serves it over the network so apps can request speech and play it back.

You send it text, pick a voice, and get audio back in either one complete
file or as a stream that starts playing before the rest has finished.

It also accepts text bit by bit over a persistent connection, so speech can
start while the sentence is still being typed or generated.

Everything ships as a Docker image that runs on a single powerful GPU host,
with a familiar OpenAI-style request shape for the speech endpoint.

## Why does it matter?
Waiting for audio is painful. If a voice assistant pauses too long before
speaking, the conversation feels broken.

This project focuses on that first moment of sound: how fast the first bit
of audio arrives after you send text.

It claims about 10 requests per second with the first audio arriving in
under 50 milliseconds for most requests, on one NVIDIA H100.

Even at 20 requests per second, it claims the first audio still arrives in
under 80 milliseconds for most requests, while playback stays real-time.

That matters because it means one expensive GPU can handle many simultaneous
users without everyone noticing delays.

It is tested mainly with English, so expectations for other languages should
stay cautious.

## How does it work?
Think of it as a small restaurant kitchen with three speed settings.

First, you choose a profile: fastest first audio, balanced, or maximum total
output. The fastest mode uses smaller starting audio chunks; the throughput
mode uses larger chunks and batches to serve more people at once.

Second, experts can fine-tune the recipe with a small settings file that
builds on top of one of those three profiles. Mistakes in that file — such
as unknown options or a mismatched base profile — stop startup early, before
the model even loads. The final settings and a checksum are printed at boot.

Third, the server warms up before accepting real traffic. It stays in a
not-ready state until two things finish: a GPU speed-up step called CUDA
Graph capture, plus one full practice speech request.

Fourth, normal traffic flows through a few simple doors: health and readiness
checks, a model list, a speech endpoint for one-shot or streaming audio, and
a separate streaming endpoint for live, incremental text.

Finally, the everyday runtime is deliberately boring: one fixed Python
version, one container port, one reserved GPU, a persistent cache folder so
the model does not need re-downloading, and a regular health check.

## Where can this be used?
Anywhere a computer needs to speak quickly and naturally.

A voice assistant or customer-support bot can start answering out loud
almost immediately, instead of leaving an awkward silence.

A live narration tool can read out generated text as it arrives — for
example, news updates, sports commentary, or navigation instructions.

An accessibility reader can voice articles, messages, or app content with
less lag between pressing play and hearing sound.

A creative tool can preview many voice lines fast, because one GPU can serve
several requests per second without long queues.

A developer prototype benefits too: the OpenAI-shaped request makes it easy
to swap this local high-speed voice engine into an existing app.

## Conclusions & takeaways
The big idea is simple: make one good voice model fast enough for real use.

Speed comes from engineering around the model — profiles, batching, chunk
sizes, GPU warm-up — not from changing the model itself.

The trade-off is explicit: favor instant first audio, balanced behavior, or
total throughput, depending on what your app needs.

The operational stance is strict: fail fast on bad settings, prove readiness
with warm-up, and keep the deployment pinned and reproducible.

If you remember one thing, remember this: this repo is about serving speech
quickly and reliably from a single GPU, not about training a new voice.

## Jargon decoder
| Term | What it means in plain language |
|---|---|
| Text-to-speech (TTS) | Turning written text into spoken audio. |
| Time-to-first-audio (TTFA) | How long until you hear the first sound, not the whole clip. |
| RPS (requests per second) | How many speech requests the server handles each second. |
| p95 | The experience of almost everyone: 95 out of 100 requests are this fast or faster. |
| H100 | A powerful NVIDIA graphics chip used here to run the voice model fast. |
| CUDA Graph capture | A one-time GPU warm-up trick that makes repeated work start faster. |
| Profile (ttfa / balanced / throughput) | A preset speed setting: fastest start, middle ground, or most total output. |
| Engine-config overlay | A small settings file that tweaks one of the preset speed settings. |
| Streaming vs. non-streaming | Getting audio piece by piece as it is made versus waiting for one full file. |
| WebSocket | A persistent connection for sending text gradually and getting audio back. |
| Health vs. readiness check | Two status doors: one says the server is alive, the other says it is ready for users. |
| Cache volume | A saved folder where the downloaded model lives so it is kept between restarts. |
