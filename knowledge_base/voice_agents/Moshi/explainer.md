> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# kyutai-labs/moshi — In Plain Language

## What is this about?

Moshi is an open-source system for talking to an AI out loud, in real time.

Think of it like a phone call with a voice assistant: you speak, and it
speaks back almost immediately. You can interrupt it, and it can hear you
while it is talking — just like a natural conversation between two people.

Under the hood, Moshi has two halves. One half is "Moshi" itself, the
talking-and-listening brain. The other half is "Mimi", a compressor that
turns raw microphone sound into a compact stream of tokens the brain can
work with, and turns tokens back into audible speech.

The project ships three versions of the same idea:

- A PyTorch version for researchers who want to experiment.
- An MLX version that runs on-device on a Mac or iPhone.
- A Rust version built for fast, reliable production servers.

It also includes a web page you talk through in your browser, and two
ready-made voices: Moshiko (a male-sounding voice) and Moshika
(a female-sounding voice).

## Why does it matter?

Most voice assistants work like walkie-talkies: you talk, then wait, then
they answer. That pause comes from chaining separate steps — convert speech
to text, think of an answer, convert text back to speech.

Moshi removes the walkie-talkie pattern. It listens and speaks at the same
time, so interruptions, quick back-and-forth, and natural timing become
possible. The delay from you speaking to it responding can be as low as
about a fifth of a second on a decent GPU.

It also matters because it is open. The code, the voices, and the audio
compressor are publicly available, so researchers and builders can study,
reuse, and adapt real-time voice conversation instead of starting from
zero or relying on a closed service.

Finally, the same design is already being reused for related jobs, such as
live speech translation (the Hibiki project) and combined speech-to-text
and text-to-speech systems.

## How does it work?

Picture two conveyor belts running side by side: one carries what you are
saying, the other carries what Moshi is saying. Moshi watches both belts
at once, moment by moment.

In plain steps:

1. Your microphone sound enters the Mimi compressor. Mimi squeezes ordinary
   audio into a slow trickle of tokens — roughly a dozen per second —
   so the big model has far less to process.
2. The big model (a 7-billion-parameter Temporal Transformer) reads both
   streams — your tokens and its own tokens — and decides what sound should
   come next.
3. A smaller helper model (the Depth Transformer) sorts out the fine detail
   inside each single moment of sound.
4. As Moshi "speaks", it also silently drafts the words behind its own
   speech — an inner monologue in text. This private text track keeps its
   spoken sentences more coherent.
5. The chosen tokens flow back through Mimi in reverse, which rebuilds them
   into audible speech played through your speakers or headphones.

The speed budget is tight on purpose: Mimi works in 80-millisecond chunks,
the model adds about 80 more milliseconds of lookahead, giving roughly
160 milliseconds of built-in delay before real-world overhead.

To use it, you start a model server (PyTorch, MLX, or Rust) and open either
the web page or a simple command-line client. The web page is recommended
because it cancels your speaker echo; the bare command-line clients do not.

## Where can this be used?

- Hands-free helpers: talking assistants you can interrupt while cooking,
  driving, or working with your hands full.
- Live conversation practice: language tutoring, interview rehearsal, or
  accessibility tools that respond by voice without awkward pauses.
- On-device voice apps: the Mac/iPhone build shows how the same system can
  run locally instead of sending your voice to a distant server.
- Production voice services: the Rust server plus the demo deployment setup
  (web front end, GPU back end, secure routing) show the path from a
  research demo to a hosted chat service.
- Research starting points: real-time translation, custom voices, and new
  dialogue behaviors built on top of the two-stream talking model.

There are honest limits today: it speaks English only, the training data is
not public, changing the voice or personality needs extra fine-tuning done
elsewhere, the small-device builds stop after about five minutes, and the
full-quality model wants a powerful GPU with plenty of memory.

## Conclusions & takeaways

- Moshi proves that natural, interruptible voice chat with an AI is
  practical at around 200 milliseconds of delay.
- The trick is treating conversation as two simultaneous audio streams plus
  a silent text draft, all squeezed through a very low-rate audio codec.
- Shipping three back ends — research, on-device, and production — makes
  one research idea usable by very different audiences.
- If you want to try it, start with the web interface and a ready-made
  voice; reach for the code only when you need to customize or deploy it.
- If you want to build on it, the interesting frontiers are new languages,
  longer conversations, smaller hardware, and custom voices.

## Jargon decoder

| Term | What it really means |
|---|---|
| Full-duplex | Both sides can talk and listen at the same time, like a phone call rather than a walkie-talkie. |
| Foundation model | A large, general-purpose AI model that other projects can reuse and adapt. |
| Neural audio codec (Mimi) | A learned compressor that turns sound into compact tokens and back into sound again. |
| Temporal Transformer (7B) | The large part of Moshi that tracks how conversation unfolds over time. |
| Depth Transformer | The small helper that fills in the fine detail of each instant of sound. |
| Inner monologue | The model's private text draft of what it is saying, used to keep speech sensible. |
| Token | A small chunk — of sound or text — that the model reads and writes. |
| Latency | The delay between you speaking and hearing the reply; lower is better. |
| Checkpoint | A saved, ready-to-use copy of a trained model, such as the Moshiko voice. |
| Quantization (int4/int8/bf16) | Shrinking the model so it uses less memory, at some cost in voice quality. |
