# Technical Analysis: Akshat21Shah/e3-tts-assessment

**Repository:** https://github.com/Akshat21Shah/e3-tts-assessment
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Problem space: autoregressive neural TTS is too slow for real-time voice interaction when each decode step pays per-layer Python and CUDA-launch overhead. The wiki reports standard HuggingFace `generate()` on the Qwen3-TTS talker costs ~20 ms per decode step for codec tokens generated at 12 Hz, yielding RTF ≈ 0.24, above the real-time threshold (README.md:122).

What the repo does: it keeps the Qwen3-TTS model (`Qwen/Qwen3-TTS-12Hz-0.6B-Base`, ~1.4 GB) but replaces the talker decode loop with a hand-rolled single-launch CUDA megakernel fusing all 28 Transformer layers (128 blocks × 512 threads), cutting decode to 0.86 ms/step and talker RTF to ≈ 0.01 (README.md:122-124). Around that kernel it builds a split-deployment streaming voice agent: laptop microphone → Deepgram cloud STT over WebSocket → Groq LLaMA-3.3-70B streaming LLM (~200 ms) → HTTP POST `/synthesize` over an SSH tunnel to a FastAPI TTS server on a rented GPU → megakernel decode → code predictor → vocoder PCM stream → PyAudio speakers, with end-to-end first audio in ~250 ms and TTFC ≈ 36 ms on RTX 5090 (README.md:9, README.md:53-80, README.md:45). Reported targets are TTFC < 60 ms (achieved 35–38 ms) and RTF < 0.15 (achieved 0.12–0.15) (README.md:83-86).

Primary user: a developer with a microphone-equipped laptop and API keys who rents an hourly cloud GPU (vast.ai, RunPod, Lambda Labs) to run low-latency voice conversations without provider lock-in (README.md:47, README.md:174-191).

Coverage note: the wiki contains only two component pages covering `README.md` (§overview through local-Mac setup, truncated mid-sentence at `01-overview.md:348-350`), `.gitignore`, and `requirements.txt`. Server internals beyond the README summary, the full pipeline source, and the remainder of local run/benchmark/limitations sections are not covered.

## 2. High-Level Architecture

```
Microphone (laptop)
  │
  ▼
Deepgram STT ─── WebSocket real-time ASR (cloud)
  │
  ▼
Groq LLaMA-3.3-70B ─── streaming LLM, ~200 ms (cloud)
  │
  ▼
pipeline.py ─── HTTP POST /synthesize ──► tts_server.py (FastAPI, :8000)
  │              (via SSH tunnel)               │
  │                                       PyTorch prefill (qwen-tts)
  │                                             │
  │                                       CUDA megakernel decode
  │                                       (28 layers, 1 kernel, 0.86 ms/step)
  │                                             │
  │                                       Code predictor (CUDA graph, ~5 ms/frame)
  │                                             │
  │                                       Vocoder ──► int16 PCM stream
  │                                             │
  ◄─────────────────────────────────────────────┘
  │
  ▼
PyAudio ──► Speakers (laptop)
  │
  ▼
AudioInputGate (Pipecat FrameProcessor, echo gate)
```

Data-flow narrative:

1. Capture and transcribe: laptop microphone audio is streamed to Deepgram STT over a WebSocket for real-time ASR (README.md:53-80).
2. Generate reply text: transcript is sent to Groq LLaMA-3.3-70B in streaming mode (~200 ms), producing the response incrementally (README.md:53-80).
3. Forward to GPU: `pipeline.py` issues HTTP POST `/synthesize` through a plain SSH tunnel (`-L 8000:localhost:8000`) to `server/tts_server.py` (FastAPI, port 8000) on the rented GPU server (README.md:53-80, README.md:302-346).
4. Synthesize: the server runs PyTorch prefill via `qwen-tts`, then autoregressive codec generation in the fused CUDA megakernel (0.86 ms/step across all 28 layers), then code predictor (~5 ms/frame under `torch.compile` plus CUDA graph) and vocoder, streaming int16 PCM back; `CHUNK_FRAMES=4` sends the first frame immediately for TTFC and batches the rest at ~3 ms/frame (README.md:53-80, README.md:132-136).
5. Play with echo suppression: PCM bytes (`X-Encoding: int16-le`, `X-Sample-Rate: 24000`) are passed directly to `TTSAudioRawFrame.audio` and played via PyAudio, while `AudioInputGate` drops `AudioRawFrame` events while `_bot_speaking=True` and for 400 ms after `BotStoppedSpeakingFrame` to prevent mic/speaker feedback (README.md:140, README.md:128).

Persistent state: no database or durable store is described. State is ephemeral and in-memory/process-local: pre-allocated CUDA KV-cache buffers bridged zero-copy from prefill via `copy_()`, a captured CUDA graph for the code-predictor loop, the compiled megakernel `.so` cache under `~/.cache/torch_extensions/`, downloaded model weights under `model/` (git-ignored), and the runtime `_bot_speaking` flag plus 400 ms post-speech window in `AudioInputGate` (README.md:166, README.md:132-136, `.gitignore:1-8`, `README.md:128`).

## 3. The Fused Talker: Megakernel-Accelerated Codec Decoder

Representation: the central object is the Qwen3-TTS talker decode step, reframed from "28 sequential layer launches per token" into "one kernel launch per token." The megakernel fuses all 28 talker Transformer layers into a single launch configured as 128 blocks × 512 threads, reducing per-step overhead from ~20 ms to 0.86 ms and talker RTF to ≈ 0.01 (README.md:122-124). Prefill stays in standard PyTorch (`qwen-tts`); only autoregressive decode moves into the kernel, with KV tensors bridged by `copy_()` into pre-allocated CUDA buffers (README.md:166).

Named kinds/types with file:line:

- Talker codec token stream: 12 Hz autoregressive codec tokens; 3072-token TTS codec vocab vs 151,936-token LLM vocab (README.md:122, README.md:146-148).
- `LDG_VOCAB_SIZE` compile-time guard in `kernel.cu`: rewritten by `scripts/patch_kernel.py` to `#ifndef` form so `server/tts_build.py` can compile with `-DLDG_VOCAB_SIZE=3072` (README.md:150-158).
- Slot-0 embedding input: a 1-row fake embedding table holding a pre-computed combined embedding (sum of 16 codec embeddings plus text-guidance vector), always read with `token_id=0` because the kernel expects `embed_weight[token_id × HIDDEN]` for a single integer (README.md:162).
- Zero-copy KV-cache bridge: relies on collapsed 1D m-RoPE for text tokens with `rope_theta=1_000_000` matching, yielding bit-identical values (README.md:166).
- PCM output: raw int16-le bytes at 24000 Hz passed directly to `TTSAudioRawFrame.audio` with no float32 conversion or numpy normalisation (README.md:140).
- Echo-gate frames: `AudioRawFrame` vs `BotStoppedSpeakingFrame` handled by `AudioInputGate` (`_bot_speaking` flag, 400 ms holdover) (README.md:128).

Key queries: the wiki documents no query language; the operative "queries" are the service calls. Verbatim pipeline excerpt (README.md:53-80):

```
pipeline.py ──── HTTP POST /synthesize ───► tts_server.py  (FastAPI, port 8000)
                 (via SSH tunnel)                  │
                                            PyTorch prefill  (qwen-tts)
                                                   │
                                            CUDA megakernel decode
                                            (0.86 ms/step, all 28 layers in 1 kernel)
                                                   │
                                            Code predictor  (CUDA graph, ~5 ms/frame)
                                                   │
                                            Vocoder → int16 PCM stream
```

## 4. LLM / External Service Integration

The repo calls external services for STT and chat LLM; TTS inference itself is self-hosted on the rented GPU.

- Providers: Deepgram (WebSocket real-time ASR) and Groq LLaMA-3.3-70B (streaming chat, ~200 ms) on the laptop side; no external TTS API — synthesis is `Qwen/Qwen3-TTS-12Hz-0.6B-Base` served by `server/tts_server.py` (README.md:53-80, README.md:242-247).
- Required vs optional calls: Deepgram STT and Groq LLM are required for the documented voice loop (Microphone → Deepgram → Groq → `/synthesize` → speakers); the TTS HTTP call is required; health check (`GET /health`) and benchmark (`benchmarks/benchmark.py`) calls are diagnostic/optional (README.md:53-80, README.md:276-296).
- Env vars / credentials: keys are obtained from `console.deepgram.com` and `console.groq.com`; exact variable names are not preserved in the wiki because the source chunk truncates at `01-overview.md:348-350` ("Verify tunnel is work"). Treat key names as unknown from wiki evidence; the wiki confirms keys are needed but does not list them.
- Model download service: HuggingFace (`snapshot_download` of `Qwen/Qwen3-TTS-12Hz-0.6B-Base`, ~1.4 GB) with optional `hf_transfer` acceleration; GPU base image `nvcr.io/nvidia/pytorch:24.01-py3` (Python 3.10, PyTorch 2.3, CUDA 12.1, nvcc) (README.md:242-247, README.md:174-191).

## 5. The Mic-to-Speaker Streaming Pipeline

Step by step (every function/operation cited to the wiki's README line ranges; per-file function signatures are not in the wiki, so steps cite the pipeline stage):

1. `Microphone → Deepgram STT` — stream laptop-mic audio to Deepgram WebSocket real-time ASR (README.md:53-80).
2. `Deepgram transcript → Groq LLaMA-3.3-70B` — streaming chat completion, ~200 ms, producing reply text incrementally (README.md:53-80).
3. `pipeline.py → HTTP POST /synthesize` — forward reply text through SSH tunnel (`ssh -N -f -L 8000:localhost:8000`) to FastAPI `tts_server.py` on port 8000 (README.md:53-80, README.md:302-346).
4. `tts_server.py: PyTorch prefill (qwen-tts)` — standard prefill, then `copy_()` KV tensors into megakernel CUDA buffers (README.md:53-80, README.md:166).
5. `kernel.cu: megakernel decode` — one launch (128 blocks × 512 threads, all 28 layers) per codec step at 0.86 ms/step; compiled with `-DLDG_VOCAB_SIZE=3072` after `scripts/patch_kernel.py` `#ifndef` rewrite; input via slot-0 combined-embedding trick (README.md:122-124, README.md:150-162).
6. `Code predictor + vocoder` — `torch.compile(code_predictor)` 18 ms → 5 ms/frame, CUDA-graph loop eliminating Python overhead, vocoder batching with `CHUNK_FRAMES=4` (first frame immediate, rest ~3 ms/frame) emitting int16-le 24000 Hz PCM (README.md:132-136, README.md:140).
7. `PyAudio → Speakers + AudioInputGate` — stream PCM to speakers; gate drops `AudioRawFrame` while `_bot_speaking=True` and for 400 ms after `BotStoppedSpeakingFrame` (README.md:53-80, README.md:128).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | overview, :9-350 (truncated at :348-350) | Sole design/operations doc captured in wiki: diagram, metrics, architecture decisions, kernel patches, GPU/local setup |
| `pipeline.py` | n/a (cited README.md:53-80) | Laptop-side voice loop: mic → Deepgram → Groq → POST `/synthesize` → PyAudio playback |
| `server/tts_server.py` | n/a (cited README.md:53-80, :220-270) | FastAPI TTS server on :8000: prefill, megakernel decode, code predictor, vocoder PCM stream |
| `server/tts_build.py` | n/a (cited README.md:158) | Compiles megakernel `.so` with `-DLDG_VOCAB_SIZE=3072` (~3 min, cached) |
| `kernel.cu` (vendored `AlpinDale/qwen_megakernel`) | n/a (cited README.md:146-156) | Fused 28-layer decode kernel; `constexpr int LDG_VOCAB_SIZE = 151936` patched to `#ifndef` guard |
| `scripts/patch_kernel.py` | n/a (cited README.md:150-156) | Rewrites `LDG_VOCAB_SIZE` line to `#ifndef`-guarded form |
| `scripts/setup.sh` | n/a (cited README.md:242-247) | Server bring-up: clone megakernel, patch, `pip install -r requirements.txt`, `snapshot_download` model, compile `.so` |
| `benchmarks/benchmark.py` | n/a (cited README.md:276-296) | TTFC/RTF benchmark harness against `/synthesize` |
| `requirements.txt` | 27 lines (`requirements.txt:1-26`) | Pinned dependency stack: inference, qwen-tts, serving, benchmark, Pipecat, STT/LLM SDKs |
| `.gitignore` | 26 lines (`.gitignore:1-25`) | Excludes `model/`, torch-extensions cache, bytecode, venvs, editor files, assessment docs |
| `model/` (directory, git-ignored) | n/a (`.gitignore:1-2`) | Local weights for `Qwen3-TTS-12Hz-0.6B-Base` (~1.4 GB), fetched via `setup.sh` not version control |
| `~/.cache/torch_extensions/` (cache, git-ignored) | n/a (`.gitignore:4-8`) | Compiled megakernel `.so` cache |

Line counts for source files above are unknown from wiki evidence; only `.gitignore` (26 lines) and `requirements.txt` (27 lines) are quoted verbatim in the wiki.

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `torch` | `>=2.3.0` | CUDA-enabled inference, prefill, `torch.compile`, CUDA graphs |
| `transformers` | `>=4.47.0` | Tokenizer / model scaffolding around qwen-tts |
| `safetensors` | `>=0.4.0` | Weight loading |
| `numpy` | `>=1.24.0` | Numeric support (PCM path explicitly avoids numpy normalisation) |
| `qwen-tts` | `>=0.1.1` | Qwen3-TTS prefill, code predictor, vocoder |
| `huggingface_hub` | `>=0.23.0` | `snapshot_download` of `Qwen3-TTS-12Hz-0.6B-Base` |
| `hf_transfer` | `>=0.1.6` | Optional fast HuggingFace downloader |
| `fastapi` | `>=0.110.0` | TTS HTTP server (`tts_server.py`) |
| `uvicorn[standard]` | `>=0.29.0` | ASGI server for FastAPI |
| `pydantic` | `>=2.0.0` | Request/response schemas (`/synthesize`, `/health`) |
| `aiohttp` | `>=3.9.0` | Benchmarking HTTP client |
| `pipecat-ai[silero,local]` | `>=0.0.36` | Voice pipeline incl. `AudioInputGate` frame processor |
| `deepgram-sdk` | `>=3.0.0` | Cloud streaming STT |
| `groq` | `>=0.5.0` | LLaMA-3.3-70B streaming chat client |

All constraints are exact strings from `requirements.txt:1-26`. System-level requirements (not pip): NVIDIA GPU ≥ 16 GB VRAM, CUDA ≥ 11.8, recommended image `nvcr.io/nvidia/pytorch:24.01-py3` (Python 3.10, PyTorch 2.3, CUDA 12.1, nvcc); local Mac needs `portaudio` via brew (README.md:174-191, README.md:302-346). Commented alternative `# pipecat-ai[deepgram,groq]` noted at `requirements.txt:21-22`.

## 8. CLI / Usage Surface

Entry points:

| Entry point | Command | Purpose |
|---|---|---|
| GPU shell | `ssh -p <PORT> root@<IP>` then `tmux new -s main` | Open persistent server session (README.md:220-270) |
| GPU setup | `git clone https://github.com/Akshat21Shah/e3-tts-assessment.git`, `bash scripts/setup.sh` | Clone, patch kernel, install reqs, download model, compile `.so` (README.md:242-247) |
| GPU serve | `python3 server/tts_server.py` until `[server] CUDA graph captured for code_predictor` | Start FastAPI TTS on :8000 (README.md:220-270) |
| Health check | `curl -s http://localhost:8000/health` → `{"status":"ok","sample_rate":24000}` | Smoke test (README.md:276-296) |
| Synth smoke | `POST http://localhost:8000/synthesize` with `{"text":"Hello, this is a test."}` | Single-utterance test (README.md:276-296) |
| Benchmark | `python3 benchmarks/benchmark.py` | TTFC/RTF measurement (README.md:276-296) |
| Local env | `brew install portaudio`; `python3 -m venv .venv`; `pip install "pipecat-ai[local,silero]" deepgram-sdk groq aiohttp numpy` | Mac audio + pipeline deps (README.md:302-346) |
| Tunnel | `ssh -N -f -L 8000:localhost:8000 -p <PORT> root@<IP>` | Expose remote :8000 locally (README.md:302-346) |
| Voice run | `pipeline.py` (exact argv not in wiki; chunk truncates at `01-overview.md:348-350`) | Start mic-to-speaker loop |

Env-var and config tables:

| Variable / key | Required | Notes |
|---|---|---|
| Deepgram API key (`console.deepgram.com`) | yes | Exact env-var name unknown — wiki truncated before listing (README.md:302-346, cut at `01-overview.md:348-350`) |
| Groq API key (`console.groq.com`) | yes | Exact env-var name unknown — same truncation |
| `PORT` / `IP` (SSH) | yes | Vast.ai/RunPod/Lambda connection parameters (README.md:220-270) |

| Config | Value | Where |
|---|---|---|
| TTS port | `8000` | `tts_server.py`, tunnel `-L 8000:localhost:8000` (README.md:53-80) |
| Sample rate | `24000` | `/health` payload, `X-Sample-Rate: 24000` (README.md:276-296, README.md:140) |
| PCM encoding | `int16-le` (`X-Encoding: int16-le`) | Direct to `TTSAudioRawFrame.audio` (README.md:140) |
| `CHUNK_FRAMES` | `4` | Vocoder batching; first frame immediate (README.md:132-136) |
| Kernel launch | `128 blocks × 512 threads` | Fused 28-layer decode (README.md:122-124) |
| Codec vocab | `3072` (`-DLDG_VOCAB_SIZE=3072`) | TTS vs LLM 151936 (README.md:146-158) |
| m-RoPE | collapsed 1D, `rope_theta=1_000_000` | KV-bridge validity condition (README.md:166) |
| Echo holdover | `400 ms` after `BotStoppedSpeakingFrame` | `AudioInputGate` (README.md:128) |

## 9. Extensibility Points

- New decode optimisation: edit the vendored `kernel.cu` megakernel plus `scripts/patch_kernel.py` and `server/tts_build.py` compile flags (`-DLDG_VOCAB_SIZE=...`); this is the only path that changes per-step latency (README.md:150-158).
- New voice/codec model: replace `Qwen/Qwen3-TTS-12Hz-0.6B-Base` in `scripts/setup.sh` `snapshot_download` and re-tune `CHUNK_FRAMES`, slot-0 embedding construction, and vocab guard; KV-bridge must be re-validated against the new model's RoPE config (README.md:242-247, README.md:162-166).
- New STT or LLM provider: modify `pipeline.py` Pipecat graph where Deepgram STT and Groq LLaMA-3.3-70B stages are wired (and the commented `# pipecat-ai[deepgram,groq]` extra at `requirements.txt:21-22`); PCM handoff (`TTSAudioRawFrame.audio`, int16-le/24000) is the stable seam (README.md:53-80, README.md:140).
- Echo/turn-taking policy: extend `AudioInputGate` (the `FrameProcessor` holding `_bot_speaking` and the 400 ms post-speech window) rather than touching the audio path (README.md:128).
- Server behaviour (batching, warmup, schemas): extend `server/tts_server.py` (FastAPI routes `/synthesize`, `/health`), `torch.compile`/CUDA-graph setup, and `CHUNK_FRAMES` batching (README.md:132-136, README.md:276-296).
- Benchmarks and deployment targets: extend `benchmarks/benchmark.py` for new metrics and `scripts/setup.sh` plus the GPU table (RTX 3090/4090, A6000, A100, RTX 5090) for new hosts (README.md:177-183, README.md:276-296).

## 10. Limitations and Gotchas

- **Truncated local-run docs:** the wiki source cuts mid-sentence at `01-overview.md:348-350` ("Verify tunnel is work"), so exact `pipeline.py` argv, env-var names, and benchmark/limitations sections are unknown from wiki evidence — do not guess them.
- **`LDG_VOCAB_SIZE` is a source patch, not a flag:** upstream `kernel.cu` hard-codes `constexpr int LDG_VOCAB_SIZE = 151936`; passing `-D` alone has no effect until `scripts/patch_kernel.py` rewrites it to the `#ifndef` form, and the server must then compile with `-DLDG_VOCAB_SIZE=3072` (README.md:150-158).
- **Slot-0 embedding coupling:** each decode step's input is a Python-side pre-computed sum (16 codec embeddings + text-guidance vector) smuggled through a 1-row table with `token_id=0`; any change to codec count, hidden size, or guidance mixing silently breaks synthesis without touching the kernel (README.md:162).
- **KV-bridge fragility:** zero-copy `copy_()` from PyTorch prefill into kernel buffers is valid only because text-token m-RoPE collapses to 1D and `rope_theta=1_000_000` matches bit-identically; a different RoPE config or theta invalidates the cache (README.md:166).
- **Narrow hardware envelope:** minimum NVIDIA GPU ≥ 16 GB VRAM with CUDA ≥ 11.8 and `nvcc`-capable image (`nvcr.io/nvidia/pytorch:24.01-py3`); headline numbers (TTFC ≈ 36 ms, RTF ≈ 0.13) are benchmarked on RTX 5090 Blackwell (`sm_120a`), with ~3 min first-compile cost for the `.so` (README.md:11, README.md:45, README.md:174-191, README.md:242-247).
- **Tunnel and key management are manual:** the split deployment depends on a hand-maintained `ssh -N -f -L 8000:localhost:8000` tunnel plus separately provisioned Deepgram/Groq keys and `portaudio`; a dropped tunnel or missing key fails the whole loop with no reconnect logic documented in the wiki (README.md:302-346).

## 11. How It Compares to Alternatives

- **AlpinDale `qwen_megakernel` (upstream):** the 151,936-vocab LLM fused-kernel this repo forks and adapts (via `LDG_VOCAB_SIZE` guard, slot-0 trick, KV bridge) to the 3072-token TTS codec vocab (README.md:146-166). Upstream is LLM-only; this repo is the TTS port.
- **Stock HuggingFace Qwen3-TTS (`generate()`):** the baseline the wiki measures against — ~20 ms/step Python/launch overhead per layer, RTF ≈ 0.24, vs 0.86 ms/step and talker RTF ≈ 0.01 with the megakernel (README.md:122-124). Stock is portable and unpatched; this repo trades portability (pinned CUDA, `nvcc`, sm-specific build) for latency.
- **Pipecat voice pipelines with hosted TTS (e.g. Deepgram Aura / ElevenLabs / Cartesia):** same Pipecat/STT/LLM framing (`pipecat-ai`, `deepgram-sdk`, `groq`) but synthesis as a vendor API call instead of a self-hosted GPU server over SSH (requirements.txt:21-26, README.md:47). Hosted APIs remove GPU ops and tunnel management; this repo removes per-character TTS cost and vendor lock-in at the price of running `tts_server.py` yourself.
- **Self-hosted open TTS servers (e.g. Coqui XTTS / Piper / Bark HTTP servers):** conventional per-layer PyTorch inference behind FastAPI on :8000 with standard streaming, without a fused kernel or CUDA-graph code predictor. They are easier to build and retarget; this repo is narrower (Qwen3-TTS-12Hz-0.6B-Base only) but instrumented for TTFC/RTF with `CHUNK_FRAMES=4` batching and `torch.compile` (README.md:132-136).

Positioning: this repo is a latency-focused self-hosted TTS backend plus a thin Pipecat demo loop, differentiated by a single-kernel TTS decode port and split laptop/cloud deployment, not a general voice framework or hosted TTS product.

## Appendix: Selected Code Snippets

1. Fused-decode pipeline diagram (`README.md:53-80`, via `01-overview.md:16-43`):

```
Your laptop (Mac)                           Rented GPU server
────────────────────────────────            ──────────────────────────────────
Microphone
  │
  ▼
Deepgram STT ─────────────────────────────  (WebSocket real-time ASR, cloud)
  │
  ▼
Groq LLaMA-3.3-70B ───────────────────────  (streaming LLM, cloud, ~200 ms)
  │
  ▼
pipeline.py ──── HTTP POST /synthesize ───► tts_server.py  (FastAPI, port 8000)
                 (via SSH tunnel)                  │
                                            PyTorch prefill  (qwen-tts)
                                                   │
                                            CUDA megakernel decode
                                            (0.86 ms/step, all 28 layers in 1 kernel)
                                                   │
                                            Code predictor  (CUDA graph, ~5 ms/frame)
                                                   │
                                            Vocoder → int16 PCM stream
                                                   │
◄──────────────────────────────────────────────────
  │
  ▼
PyAudio → Speakers
```

2. `LDG_VOCAB_SIZE` patch (`README.md:150-156`, via `01-overview.md:64-70`):

```c
#ifndef LDG_VOCAB_SIZE
#define LDG_VOCAB_SIZE 151936
#endif
```

Compiled by `server/tts_build.py` with `-DLDG_VOCAB_SIZE=3072` (README.md:158).

3. `.gitignore` verbatim (`.gitignore:1-25`, via `02-top-level-files.md:15-41`):

```
# Model weights (large binary files – use Git LFS or download via setup.sh)
model/

# Compiled megakernel
~/.cache/torch_extensions/
__pycache__/
*.pyc
*.pyo

# Python venv
venv/
.venv/
env/

# Editor
.DS_Store
.vscode/
*.swp

# Assessment PDFs / personal docs (not needed in source repo)
*.pdf
e3-assessment.txt
Technical assessment mail.txt
takehome_project.docx
takehome_project.txt
```

4. `requirements.txt` verbatim (`requirements.txt:1-26`, via `02-top-level-files.md:53-80`):

```
# Core inference
torch>=2.3.0          # must be CUDA-enabled (e.g. pip install torch --index-url https://download.pytorch.org/whl/cu121)
transformers>=4.47.0
safetensors>=0.4.0
numpy>=1.24.0

# Qwen3-TTS model + HuggingFace download
qwen-tts>=0.1.1
huggingface_hub>=0.23.0
hf_transfer>=0.1.6    # optional fast downloader

# TTS server
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.0.0

# Benchmarking
aiohttp>=3.9.0

# Pipecat voice pipeline
pipecat-ai[silero,local]>=0.0.36
# pipecat-ai[deepgram,groq] — uncomment if those extras are available separately

# STT / LLM services (pipecat integrations)
deepgram-sdk>=3.0.0
groq>=0.5.0
```
