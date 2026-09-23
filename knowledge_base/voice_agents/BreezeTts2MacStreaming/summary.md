# breezetts2_mac_fast.py

**Article:** [breezetts2_mac_fast.py](https://github.com/xzf-thu/BreezeTTS2_Mac_Streaming) — GitHub /

## Human Readable TL;DR

Playing AI-generated speech on a Mac stuttered like a video call on a bad connection, even though the model itself was already shrunk down to a small 4-bit download. The culprit turned out to be wasted repeat work: for every slice of sound, the program kept re-reading the lines it had just written, like re-reading a whole paragraph each time you add a word. This rewrite fixes that by remembering what was already computed within each slice and by carrying the finished sound over to the speaker in one trip instead of many small ones, plus it adds a speedometer so you can tell whether choppiness comes from slowness or just from overly dramatic punctuation in the script.

## TL;DR

The `breezetts2_mac_fast.py` rewrite targets stuttering Breeze-TTS-2 streaming playback on Apple Silicon, where measured real-time factor stays around 1.85 despite ~3 GB 4-bit weights. It attributes the bottleneck to the depth decoder in mlx-audio 0.5.1 re-feeding already-produced acoustic codes from scratch with no intra-frame KV cache reuse, and fixes it with intra-frame KV reuse plus a single CPU read-back per frame. It ships with 4-bit defaults, chunked decoding, `--depth-mode cached`/`compiled` options, and RTF plus underflow diagnostics that distinguish speed problems from expression problems.

---

## Problem & Motivation

Streaming Breeze-TTS-2 on a Mac stutters badly enough to break real-time use, and the obvious suspects do not explain it. The weights are already quantized to 4-bit at roughly 3 GB, yet one second of audio still takes about 1.85 seconds to generate, so the player constantly runs dry. Tracing against the mlx-audio 0.5.1 source points to the Breeze depth decoder rather than model size or quantization: producing one audio frame requires predicting several acoustic codes in sequence, and each prediction re-feeds the frame's existing codes through the decoder from scratch because the KV cache for that stage is never reused, adding both redundant computation and repeated device dispatch overhead. Confusion is compounded by official low-latency figures measured on a warmed-up, optimized H100 path that is not comparable to the MLX-on-Mac code path, leaving Mac users without a realistic baseline or a way to tell whether choppy output means the machine is too slow or the input text is simply hard to render expressively.

## Main Original Ideas

1. **Intra-frame KV cache reuse** — the core fix keeps the depth decoder's key-value state across the successive acoustic codes within a frame instead of recomputing from scratch for every code, directly removing the redundant work identified in the mlx-audio path.

2. **One CPU read-back per frame** — per-code device synchronization is collapsed into a single transfer per frame, which cuts stall time from repeated round-trips while preserving the numerical behavior validated against the MLX reference.

3. **Two depth modes with separated warm-up accounting** — `cached` mode is the default intra-frame reuse path, while `compiled` mode offers a whole-frame compiled alternative whose compilation cost is timed and reported separately so that first-run and steady-state numbers are not conflated.

4. **RTF and underflow instrumentation as a diagnostic rule** — the script retains real-time-factor and buffer-underflow reporting with an explicit interpretation rule, turning raw speed numbers into an actionable decision between buffering, lowering guidance cost, switching depth modes, or rendering offline.

## Key Findings

Validation against MLX numerical reference tests on small models covers both 4-bit and compiled modes, confirming the rewrite preserves correctness, though the actual speedup still needs to be measured on each user's own machine since 3B parameters alone do not guarantee real-time generation. The diagnostic split proves practically important: when RTF is below 1, generation outruns playback and raising `--prebuffer-ms` can absorb dropouts, but when RTF stays at or above 1, buffering cannot help and sustained underflow is expected. A separate class of choppiness lives in the WAV itself rather than in delivery timing, caused by dense exclamation marks, ellipses, and inline tags such as laughter or sigh markers that force repeated register switches. Defaults of 4-bit weights, playback on, `--chunk-frames 2`, and `--runs 2` (reading RTF from the second, post-warm-up run) make the standard measurement inexpensive and repeatable.

## Suggestions & Future Directions

For slow runs the recommended escalations are to lower `--cfg-scale` to cut guidance compute, try `--depth-mode compiled` when the cached path still misses real time, or fall back to offline WAV generation with `--no-play` when sustained real time is unreachable. For dropout-only runs with healthy RTF, increasing `--prebuffer-ms` or adjusting `--chunk-frames` trades first-sound latency against callback frequency and buffer depth. For choppy-but-fast runs the fix is editorial rather than computational: replace exclamation-heavy, tag-dense scripts with continuous prose and a single gradual emotion instruction that lets the voice move smoothly from one feeling to the next. Remaining work is empirical, namely benchmarking RTF and underflow counts across Mac configurations to quantify the cached versus compiled trade-off and to establish which machines can genuinely sustain streaming.

## Authors & Institutions

The wiki source does not name individual authors or institutions; the work is presented as a community rewrite of the Breeze-TTS-2 Mac streaming loop built on the MLX ecosystem, referencing the Breeze-TTS-2 model family, the mlx-audio implementation, and the `mlx-community/Breeze-TTS-2-mlx-4bit` weights.
