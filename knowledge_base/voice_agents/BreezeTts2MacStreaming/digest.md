> [[index|Wiki]] | [[summary|Summary]]

# breezetts2_mac_fast.py — Digest

## 1. [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]]

**In one sentence:** Playback stutter on Mac is caused by redundant depth-decoder recomputation (measured RTF ~1.85 even with ~3 GB 4bit weights), and this rewrite fixes it with intra-frame KV cache reuse, one CPU read-back per frame, and RTF/underflow diagnostics to separate speed problems from expression problems.

## Key points

- Stutter is not caused by model size or quantization: even with ~3 GB 4bit weights, measured RTF stays around 1.85, so 1 second of audio takes ~1.85 seconds to generate.
- The bottleneck (checked against mlx-audio 0.5.1 source) is the Breeze depth decoder: each new acoustic code re-feeds already-produced codes in the frame from scratch with no KV cache reuse, repeated for every code of every frame.
- The fix reuses the intra-frame KV cache, collapsing per-code device sync into one CPU read-back per frame to cut redundant compute and stall time.
- Two depth modes are offered: `cached` (default, intra-frame KV reuse) and `compiled` (whole-frame compiled path, with warm-up timed separately).
- Defaults are 4bit weights (`mlx-community/Breeze-TTS-2-mlx-4bit`), playback on, chunked decoding (`--chunk-frames 2`), and RTF plus underflow reporting; `--runs 2` default means read RTF from the second run.
- Interpretation rule: RTF < 1 means raise `--prebuffer-ms` if dropouts persist; RTF ≥ 1 means buffering cannot help — lower `--cfg-scale`, try `--depth-mode compiled`, or generate offline to WAV.
- Choppy WAV is an expression problem, not a speed problem: dense exclamation marks, ellipses, and tags like `[笑]` / `[叹气]` force register switches; use continuous prose with a gradual emotion instruction instead.

## The argument in five moves

1. Mac playback stutters despite small 4bit weights because measured RTF stays ~1.85, so generation lags behind real time.
2. The cause is the Breeze depth decoder in mlx-audio 0.5.1 re-feeding each frame's existing codes from scratch for every new code, with no KV cache reuse.
3. The rewrite removes that redundancy via intra-frame KV cache reuse plus one CPU read-back per frame, with `cached` and `compiled` depth modes.
4. Sensible defaults and instrumentation (chunked decoding, second-run RTF, underflow counts) let the user tell a speed shortfall from an expression artifact.
5. The decision rule follows: RTF < 1 → raise prebuffer; RTF ≥ 1 → cut cfg-scale, try compiled mode, or go offline; choppy WAV → rewrite the text with continuous prose and gradual emotion, not more buffering.
