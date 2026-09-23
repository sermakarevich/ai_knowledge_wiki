> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# breezetts2_mac_fast.py — In Plain Language

## What is this about?

Imagine you ask your Mac to read a sentence out loud, and the voice
keeps stopping and starting, like a car jerking forward in traffic.

That is the problem this script tackles. It is a rewritten playback
loop for Breeze-TTS-2, a text-to-speech voice model, running on
Apple Silicon Macs.

The key discovery is surprising: the stutter is not because the
model is too big. Even when the model is shrunk down to about
3 GB with 4-bit compression, it still takes roughly 1.85 seconds
to generate each second of speech. So the voice can never keep up
with real-time listening, and you hear gaps.

The culprit is one small but busy part of the pipeline called the
depth decoder. To produce a single slice of audio (a "frame"), it
has to predict several sound codes one after another. But the old
code re-did all its previous work from scratch for every single
code — like re-reading an entire paragraph each time you add one
new word. That wasted effort is what made everything slow.

This script rewrites that loop so the wasted work goes away, and
adds clear speed measurements so you can tell what is actually
going wrong when playback still stumbles.

## Why does it matter?

Because without this fix, the numbers mislead you.

You might assume a small 4-bit model should run fast on a Mac, or
that the smooth speed figures published for big server GPUs apply
to your laptop. They do not. Those official figures come from a
warmed-up, highly tuned path on a server-grade H100 chip — a
completely different road from the Mac path. Comparing the two is
like comparing a race track time to a rush-hour commute.

This matters in practice for three reasons:

First, it saves you from pointless tuning. Re-specifying the same
4-bit model or re-downloading weights changes nothing — the
bottleneck is repeated computation, not file size.

Second, it separates two problems people constantly mix up: "too
slow" versus "sounds choppy." A slowdown needs engineering fixes
(faster decoding, lighter settings, offline rendering). A choppy
but complete recording needs better writing (smoother text and
emotion instructions). Treating one like the other wastes hours.

Third, it gives you honest dials: a speed score (RTF), a dropout
counter (underflows), and two decoding modes, so your next step is
a decision, not a guess.

## How does it work?

Think of the script as a smarter assembly line with a supervisor
watching the conveyor belt.

Step 1 — Remember instead of recompute. The old loop threw away
its short-term memory (the "KV cache") inside each audio frame and
recalculated everything per code. The rewrite keeps that memory
alive for the whole frame, so each new code builds on the last
instead of starting over. This is the default `cached` mode.

Step 2 — Fewer trips across the bridge. The old loop also synced
with the chip after every single code, like calling the warehouse
after packing each item. The rewrite packs the whole frame, then
makes one single trip to fetch the result. Fewer stops, less
waiting around.

Step 3 — Offer a second engine. If the machine still lags, you can
switch to `--depth-mode compiled`, which compiles the whole-frame
path up front. The first run pays a one-time warm-up cost (timed
and reported separately), and later runs benefit.

Step 4 — Sensible starting settings. Out of the box it uses 4-bit
weights, turns playback on, decodes in small chunks of 2 frames,
and runs twice so you can read the speed score from the second,
warmed-up run rather than the slow first one.

Step 5 — Report, then decide. After each run it reports RTF (does
generation beat the clock?) and underflow counts (how often did
playback run dry?). The rule of thumb is simple: if RTF is below 1
but audio still drops, add more starter buffer with
`--prebuffer-ms`. If RTF is 1 or above, buffering cannot save you —
lower `--cfg-scale`, try compiled mode, or render to a WAV file
offline and listen afterwards.

A final twist: if even the finished WAV file sounds choppy, that is
not a speed problem at all. Text full of exclamation marks,
trailing dots, and stage directions like laughter or sigh tags asks
the voice to slam on the brakes and change character every few
words. The fix is calmer, continuous prose plus one gradual
emotion instruction, such as "start happy, grow a little hurt,
end soft and reassured."

## Where can this be used?

Anywhere you want a natural-sounding Chinese-capable voice on a
Mac without renting server GPUs:

- Reading assistants and accessibility tools that speak text aloud
  in real time on a laptop.
- Voice prototyping for apps, games, or demos where you iterate on
  lines and emotions quickly.
- Offline narration: bedtime stories, course audio, or podcast
  drafts rendered to WAV files overnight.
- Emotion experiments: testing how one smooth instruction ("stay
  the same person, shift mood gradually") compares against choppy
  tag-heavy scripts.
- Performance debugging: using the RTF and underflow numbers as a
  template for diagnosing any on-device generative-audio pipeline.

The pattern itself travels well: whenever a decoder repeats work
inside a small unit (a frame, a chunk, a patch), caching within
that unit plus batching the device transfers is usually the first
win to try before buying bigger hardware.

## Conclusions & takeaways

- Small does not mean fast: a 3 GB model can still run at 1.85x
  real time if one stage repeats its own work.
- The fix is memory, not muscle: reusing the within-frame cache
  and syncing once per frame removes the redundancy at its root.
- Measure before you tune: read RTF from the warmed-up second run,
  then follow the decision rule (buffer if fast, lighten or go
  offline if slow, rewrite text if the WAV itself is choppy).
- Server numbers do not transfer: H100 figures and Mac figures
  describe different code paths on different machines.
- Words shape the voice: continuous prose with gradual emotion
  beats punctuation fireworks and constant register-switch tags.

## Jargon decoder

| Term | What it really means |
|---|---|
| RTF (real-time factor) | How many seconds of computing each second of audio costs; below 1 is faster than live, above 1 lags behind. |
| Underflow | Playback ran out of ready audio and had to skip; a counter of how often the speaker went hungry. |
| KV cache | The model's short-term notes on what it already computed, reused so it does not redo old work. |
| Depth decoder | The sub-model that predicts the stack of sound codes for each audio frame, one code at a time. |
| Acoustic code | A small numbered token describing a slice of sound; several stack up to make one frame audible. |
| 4-bit weights | A compressed copy of the model (~3 GB) that trades a little precision for much less memory. |
| Compiled mode | An alternative engine that pre-builds the whole-frame path; first run is slow, later runs are quicker. |
| Prebuffer | Starter audio saved up before pressing play, a cushion that only helps when generation is already fast enough. |
| cfg-scale | A knob for how strictly the voice obeys your style instruction; higher means clingier but costlier. |
| Chunked decoding | Generating audio a few frames at a time so playback can start early instead of waiting for everything. |
