---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: breezetts2_mac_fast.py

### Q1. Why does playback stutter on Mac even with small 4bit weights?
> [!tip]- Answer
> The stutter is not caused by model size or quantization: even with ~3 GB 4bit weights, measured RTF stays around 1.85, so 1 second of audio takes ~1.85 seconds to generate and playback starves. Generation therefore lags behind real time regardless of the small download size. See [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]].

### Q2. What is the exact bottleneck in the depth decoder, and which source was it checked against?
> [!tip]- Answer
> Generating one frame of audio requires predicting several acoustic codes in sequence, and in mlx-audio 0.5.1 each prediction re-feeds the frame's already-produced codes through the depth decoder from scratch with no KV cache reuse. This repeats for every code of every frame, adding redundant computation plus extra GPU dispatch overhead. See [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]].

### Q3. What two code changes fix the bottleneck, and what depth modes do they map to?
> [!tip]- Answer
> The fix adds intra-frame KV cache reuse to eliminate the redundant recomputation, and collapses the per-code device sync into one CPU read-back per frame to cut stall time. These ship as two depth modes: `cached` (default, intra-frame KV reuse) and `compiled` (whole-frame compiled path, with warm-up timed separately). See [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]].

### Q4. What are the default run commands, and what do the key flags control?
> [!tip]- Answer
> The default run is `uv run --python 3.12 breezetts2_mac_fast.py` with 4bit weights (`mlx-community/Breeze-TTS-2-mlx-4bit`), playback on, chunked decoding (`--chunk-frames 2`), and RTF plus underflow reporting. Key flags are `--depth-mode` (`cached` default vs `compiled` whole-frame), `--cfg-scale` (default 1; higher gives stronger instruction adherence at higher compute cost), `--prebuffer-ms` (audio buffered before playback, only helps if RTF < 1), and `--runs 2` (read RTF from the second run, excluding warm-up). See [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]].

### Q5. How do you read the RTF and underflow results to decide the next step?
> [!tip]- Answer
> RTF < 1 means generation outruns playback, so if audio still drops out, raise `--prebuffer-ms`. RTF ≥ 1 means buffering cannot fix it and sustained underflow is expected — instead lower `--cfg-scale`, try `--depth-mode compiled`, or generate offline to WAV with `--no-play`. The reported underflow counts separate a slow run from a choppy-sounding one. See [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]].

### Q6. Why can the WAV itself sound choppy even when speed is fine, and how should the text be rewritten?
> [!tip]- Answer
> A choppy WAV is an expression problem, not a speed problem: dense exclamation marks, ellipses, and tags like `[笑]` / `[叹气]` force the model to stop and switch register repeatedly. The fix is continuous prose with a gradual emotion instruction (e.g. staying one coherent person whose mood shifts gradually) rather than more buffering. The emotion example uses `--cfg-scale 1 --chunk-frames 4 --prebuffer-ms 640 --runs 1` with such an instruction. See [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]].

### Q7. Your Mac still reports RTF ≥ 1 in cached mode and the script's status notes the speedup is unmeasured on your machine — what would you recommend trying next, and why?
> [!tip]- Answer
> I would recommend trying `--depth-mode compiled` first (accepting the separately-timed warm-up cost), then lowering `--cfg-scale` toward 1, and falling back to offline WAV generation with `--no-play` if RTF stays above 1. This follows the page's decision rule that buffering cannot help when RTF ≥ 1, while its status section warns that validation covered only numerical reference tests and 3B parameters alone do not guarantee real-time generation. I would also discount official H100 low-latency figures, since the page notes they come from a warmed-up optimized path that is not the Mac MLX code path. See [[wiki/01-breezetts2-mac-fast-py|breezetts2_mac_fast.py — rewritten streaming loop for Breeze-TTS-2 on Apple Silicon]].
