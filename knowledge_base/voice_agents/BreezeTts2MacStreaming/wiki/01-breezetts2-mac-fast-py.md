[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon
**In one sentence:** Playback stutter on Mac is caused by redundant depth-decoder recomputation (measured RTF ~1.85 even with ~3 GB 4bit weights), and this rewrite fixes it with intra-frame KV cache reuse, one CPU read-back per frame, and RTF/underflow diagnostics to separate speed problems from expression problems.
## Key points
- Stutter is not caused by model size or quantization: even with ~3 GB 4bit weights, measured RTF stays around 1.85, so 1 second of audio takes ~1.85 seconds to generate.
- The bottleneck (checked against mlx-audio 0.5.1 source) is the Breeze depth decoder: each new acoustic code re-feeds already-produced codes in the frame from scratch with no KV cache reuse, repeated for every code of every frame.
- The fix reuses the intra-frame KV cache, collapsing per-code device sync into one CPU read-back per frame to cut redundant compute and stall time.
- Two depth modes are offered: `cached` (default, intra-frame KV reuse) and `compiled` (whole-frame compiled path, with warm-up timed separately).
- Defaults are 4bit weights (`mlx-community/Breeze-TTS-2-mlx-4bit`), playback on, chunked decoding (`--chunk-frames 2`), and RTF plus underflow reporting; `--runs 2` default means read RTF from the second run.
- Interpretation rule: RTF < 1 means raise `--prebuffer-ms` if dropouts persist; RTF ≥ 1 means buffering cannot help — lower `--cfg-scale`, try `--depth-mode compiled`, or generate offline to WAV.
- Choppy WAV is an expression problem, not a speed problem: dense exclamation marks, ellipses, and tags like `[笑]` / `[叹气]` force register switches; use continuous prose with a gradual emotion instruction instead.
---
## Quick start
**Covers:** default run, compiled fallback, emotion example, options table

Defaults: 4bit weights, playback on, chunked decoding, RTF and underflow reporting:

```bash
uv run --python 3.12 breezetts2_mac_fast.py
```

If RTF is still ≥ 1, try whole-frame compiled mode (first run pays a compilation cost; warm-up time is reported separately):

```bash
uv run --python 3.12 breezetts2_mac_fast.py \
  --depth-mode compiled
```

With text and emotion control:

```bash
uv run --python 3.12 breezetts2_mac_fast.py \
  --depth-mode compiled \
  --cfg-scale 1 \
  --chunk-frames 4 \
  --prebuffer-ms 640 \
  --text "看到你回来我真的很开心，可想到这些天一直等不到你的消息，心里又有点委屈。" \
  --instruct "同一个人连续自然地说话，保持连贯的语速和气息，情绪从开心渐渐流露出委屈，最后变得柔软安心。" \
  --runs 1 \
  --output breeze_emotion_smooth
```

| Flag | Default | Notes |
|---|---|---|
| `--model` | `mlx-community/Breeze-TTS-2-mlx-4bit` | Already 4bit; re-specifying it changes nothing |
| `--depth-mode` | `cached` | `cached` uses intra-frame KV reuse; `compiled` compiles the whole frame |
| `--chunk-frames` | `2` | Frames per decode chunk. Larger = fewer callbacks, higher first-sound latency |
| `--prebuffer-ms` | — | Audio buffered before playback starts. Only helps if RTF < 1 |
| `--cfg-scale` | `1` | Higher gives stronger instruction adherence at higher compute cost |
| `--no-play` | off | Generate to WAV only, no audio output |
| `--runs` | `2` | Second run excludes warm-up; read RTF from that one |

## What this fixes
**Covers:** real cause of stutter, changes, status, reading results

The real cause of the stutter: generating one frame of audio requires predicting several acoustic codes in sequence, and in mlx-audio 0.5.1 each prediction re-feeds the frame's existing codes through the depth decoder from scratch — "the KV cache for this stage is never reused", producing redundant computation plus extra GPU dispatch overhead.

> "the low-latency figures Breeze publishes officially come from a warmed-up, optimized path on H100. That is not the same code path as the MLX implementation on a Mac, and the two numbers are not directly comparable."

What was changed:
- **Intra-frame KV cache reuse** — eliminates the redundant recomputation described above.
- **One CPU read-back per frame** — the per-code device sync is collapsed into a single transfer, cutting stall time.
- **Sensible defaults** — 4bit weights, playback enabled, chunked decoding out of the box.
- **Retained instrumentation** — RTF and underflow counts are still reported, so a slow run and a choppy-sounding run can be told apart.
- **`--depth-mode compiled`** — an alternative whole-frame compiled path; warm-up is timed and reported separately.

Status: validated against MLX numerical reference tests on small models, covering both 4bit and compiled modes; actual speedup still needs measuring on your own machine, and 3B parameters alone does not guarantee real-time generation.

Reading your results:
- **RTF < 1** — generation outruns playback. If audio still drops out, raise `--prebuffer-ms`.
- **RTF ≥ 1** — buffering cannot fix this. Sustained underflow is expected; reduce `--cfg-scale`, try `--depth-mode compiled`, or generate offline to WAV.
- **The WAV itself sounds choppy** — expression problem, not speed: dense exclamation marks, ellipses, and `[笑]` / `[叹气]` tags ask the model to stop and switch register repeatedly; use continuous prose with gradual emotion instruction instead.
