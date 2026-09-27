> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# dreamtheater123/TurnGuide — In Plain Language

## What is this about?

TurnGuide is a voice-AI project that lets a computer hold a natural,
two-way spoken conversation — talking and listening at the same time,
much like two people on a phone call.

Most voice assistants today are half-duplex: you speak, then wait, then
the assistant replies. TurnGuide is full-duplex, meaning both sides can
speak, pause, or interrupt at any moment.

Its key idea is simple to state: plan what to say in text, but weave
that text together with speech sound-by-sound, turn by turn. The text
keeps the meaning coherent, while the speech layer keeps the timing
and flow natural.

The repository is an inference demo release: scripts that take a mono
recording of one speaker and generate the other speaker's voice in
response, plus Fisher and Candor test clips for fair comparison.

## Why does it matter?

Anyone who has fought with a voice assistant that talks over you — or
freezes while you pause to think — has felt the half-duplex problem.

Real conversation is messy: people overlap, backchannel ("uh-huh"),
interrupt, and change direction mid-sentence. Systems that wait for
silence before replying feel robotic and slow.

TurnGuide matters because it tackles meaning and timing together:

- Coherence: responses should make sense in context, not just sound
  smooth. Guiding speech with text helps the model stay on topic.
- Natural timing: listening while speaking lets the assistant react to
  interruptions instead of ignoring them.
- Benchmarking: shipping shared Fisher/Candor test splits means rival
  approaches can be compared apples-to-apples.
- Reproducibility: a pinned Python/PyTorch/CUDA stack and two
  checkpoints that differ in exactly one setting make experiments
  easier to repeat.

## How does it work?

Think of TurnGuide as a three-stage pipeline: listen, think-and-speak,
then vocalize.

1. Listen: your mono WAV recording is chopped into small pieces and
   converted into discrete speech tokens — a compact alphabet of
   sounds — using a speech tokenizer.

2. Think-and-speak in turns: the model reads your speech tokens in
   chunks of about five. After each chunk, it generates one short
   reply chunk that mixes text tokens (the words/meaning) with speech
   tokens (the sound). Special marker tokens label who is speaking and
   where audio or transcription blocks begin and end.

3. Vocalize: the reply's speech tokens are turned back into audible
   sound by a streaming audio decoder. A flow model predicts the
   sound's shape, a HiFi-GAN vocoder renders the waveform, and
   overlap-smoothing stitches chunks so there are no clicks or gaps.

Two ready-made checkpoints let you pick how much the training cared
about getting the words right versus getting the sound right: one
weights text twice as much as speech (2:1), the other three times as
much (3:1). You switch between them with a single `--model-path` flag.

Under the hood it reuses GLM-4-Voice parts (model, tokenizer, decoder)
whose weights are downloaded separately, and runs in a pinned
Python 3.10 / PyTorch 2.5.0 / CUDA 12.1 environment.

## Where can this be used?

- Smarter voice assistants that allow barging in ("stop, I meant…")
  without restarting the whole exchange.
- Hands-free helpers for driving, cooking, or accessibility, where
  waiting for a beep is impractical.
- Call-center and meeting bots that need to backchannel, take turns,
  and handle overlapping speech gracefully.
- Language-learning or conversation-practice tools where timing and
  interruption feel as important as correct words.
- Research benchmarking: the Fisher/Candor splits give labs a shared
  yardstick for full-duplex quality.

What it is not (in this release): a training codebase or a hosted
product. It is a demo-grade inference stack — you bring a mono WAV
file, it writes the assistant's reply and a stereo mix to an output
folder.

## Conclusions & takeaways

- Full-duplex means listening and speaking simultaneously; TurnGuide
  aims to make that both fluent and meaningful.
- The core trick is interleaving: text guides the content, speech
  tokens carry the delivery, exchanged in small alternating chunks.
- Small design choices are exposed cleanly — e.g. the 2:1 versus 3:1
  text-to-speech training weight — so others can test what matters.
- Streaming vocoding with caching and fade-smoothing is what makes
  chunk-by-chunk replies sound continuous rather than choppy.
- If you remember one thing: TurnGuide treats conversation as
  turn-taking with sound, not just chat with a microphone attached.

## Jargon decoder

| Term | What it really means |
|---|---|
| Full-duplex | Both sides can talk and listen at the same time, like a phone call |
| Half-duplex | Only one side talks at a time, like a walkie-talkie |
| Speech token | A sound chopped into a numbered symbol the AI can process |
| Text token | A word-piece symbol the AI uses to plan meaning |
| Turn-level interleaving | Alternating small bursts of "what to say" and "how it sounds" |
| Loss ratio (2:1, 3:1) | How much training cared about correct words vs. correct sound |
| Speech tokenizer | Tool that converts raw audio into speech tokens |
| Flow model | Component that predicts the sound's shape from tokens |
| HiFi-GAN vocoder | Component that turns that shape into an audible waveform |
| Checkpoint | A saved, ready-to-run copy of a trained model |
| Mono / stereo WAV | One-channel vs. two-channel audio files used as input/output |
