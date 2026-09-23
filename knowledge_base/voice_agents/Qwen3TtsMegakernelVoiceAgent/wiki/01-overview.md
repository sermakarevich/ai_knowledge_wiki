> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** A real-time streaming voice agent where laptop-mic speech is transcribed by Deepgram, answered by Groq LLaMA-3.3-70B, and synthesised by Qwen3-TTS on a rented GPU via a hand-rolled CUDA megakernel so the user hears a response within ~250 ms (README.md:9).
## Key points
- Delivers sub-60 ms time-to-first-chunk (TTFC) by replacing the slow HuggingFace autoregressive decoder in Qwen3-TTS with a hand-rolled CUDA megakernel, achieving TTFC ≈ 36 ms and RTF ≈ 0.13 on RTX 5090 Blackwell (README.md:11, README.md:45).
- Splits work so GPU-heavy TTS inference runs on a cheap rented cloud GPU while the laptop handles only audio I/O, Deepgram cloud STT, and Groq cloud LLM calls, joined by a plain SSH tunnel with no provider lock-in (README.md:47).
- Streams end-to-end as Microphone → Deepgram STT (WebSocket real-time ASR) → Groq LLaMA-3.3-70B (streaming, ~200 ms) → HTTP POST /synthesize via SSH tunnel → FastAPI TTS server on port 8000 → PyTorch prefill → CUDA megakernel decode → code predictor → vocoder PCM stream → PyAudio speakers (README.md:53-80).
- Fuses all 28 talker Transformer layers into one CUDA kernel launch (128 blocks × 512 threads), cutting ~20 ms/step HuggingFace generate() overhead to 0.86 ms/step and talker RTF to ≈ 0.01 (README.md:122-124).
- Prevents mic/speaker feedback loops with AudioInputGate, a Pipecat FrameProcessor that drops AudioRawFrame events while _bot_speaking=True and for 400 ms after BotStoppedSpeakingFrame (README.md:128).
- Sends raw int16 PCM bytes (X-Encoding: int16-le, X-Sample-Rate: 24000) passed directly to TTSAudioRawFrame.audio with no float32 conversion or numpy normalisation (README.md:140).
- Adapts the 151,936-vocab LLM megakernel to the 3072-token TTS codec vocab via an LDG_VOCAB_SIZE #ifndef guard, a slot-0 embedding trick, and a zero-copy KV-cache bridge relying on collapsed 1D m-RoPE with rope_theta=1_000_000 (README.md:148-166).
---
## Pipeline and metrics
End-to-end flow (verbatim, README.md:53-80):

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

Targets vs. achieved (README.md:83-86):

| Metric | Definition | Target | Achieved |
|---|---|---|---|
| **TTFC** | ms from HTTP request to first audio byte | < 60 ms | 35–38 ms |
| **RTF** | inference time / audio duration | < 0.15 | 0.12–0.15 |

## Architecture decisions
- Why a megakernel: Qwen3-TTS talker autoregressively generates codec tokens at 12 Hz; standard `generate()` costs ~20 ms/decode step in Python/CUDA launch overhead per layer, giving RTF ≈ 0.24, too slow for real-time (README.md:122).
- Server optimisations (README.md:132-136):

| Optimisation | Effect |
|---|---|
| `torch.compile(code_predictor)` | 18 ms → 5 ms per frame |
| CUDA graph for code-predictor loop | Eliminates Python overhead |
| Vocoder batching (`CHUNK_FRAMES=4`) | First frame sent immediately (TTFC); rest batched at 3 ms/frame |

## Kernel modifications
Three changes to the AlpinDale megakernel, written for 151,936-token LLM vocab (README.md:146):
1. `LDG_VOCAB_SIZE` patch: `kernel.cu` had `constexpr int LDG_VOCAB_SIZE = 151936`, not overridable by `-D`; `scripts/patch_kernel.py` rewrites it to (README.md:150-156):

```c
#ifndef LDG_VOCAB_SIZE
#define LDG_VOCAB_SIZE 151936
#endif
```

`server/tts_build.py` then compiles with `-DLDG_VOCAB_SIZE=3072` (README.md:158).
2. Slot-0 embedding trick: kernel reads `embed_weight[token_id × HIDDEN]` for a single integer token, but each TTS step input is a sum of 16 codec embeddings plus a text-guidance vector; fix pre-computes the combined embedding in Python, writes it into row 0 of a 1-row fake embedding table, and always passes `token_id=0` (README.md:162).
3. Zero-copy KV-cache bridge: prefill runs in standard PyTorch (qwen-tts); KV tensors are `copy_()` directly into the megakernel's pre-allocated CUDA buffers, valid because Qwen3 m-RoPE collapses to 1D RoPE for text tokens and `rope_theta=1_000_000` matches — values bit-identical (README.md:166).

## Deployment split
- GPU server minimum: NVIDIA GPU ≥ 16 GB VRAM, CUDA ≥ 11.8; recommended image `nvcr.io/nvidia/pytorch:24.01-py3` (Python 3.10, PyTorch 2.3, CUDA 12.1, nvcc); platforms vast.ai (used here), RunPod, Lambda Labs (README.md:174-191).
- GPU options (README.md:177-183):

| GPU | VRAM | approx. $/hr (vast.ai) | Notes |
|---|---|---|---|
| RTX 3090 | 24 GB | ~$0.25 | Good baseline |
| RTX 4090 | 24 GB | ~$0.40 | Recommended — fast + affordable |
| A6000 | 48 GB | ~$0.60 | Professional grade |
| A100 40GB | 40 GB | ~$1.00 | Datacenter |
| RTX 5090 | 32 GB | ~$1.20 | Benchmarked here (sm_120a) |

- Server bring-up: `ssh -p <PORT> root@<IP>`, `tmux new -s main`, `git clone https://github.com/Akshat21Shah/e3-tts-assessment.git`, `bash scripts/setup.sh`, then `python3 server/tts_server.py` until `[server] CUDA graph captured for code_predictor` (README.md:220-270).
- `setup.sh` does: clone `AlpinDale/qwen_megakernel`, patch `kernel.cu` with `#ifndef LDG_VOCAB_SIZE`, `pip install -r requirements.txt`, download `Qwen/Qwen3-TTS-12Hz-0.6B-Base` (~1.4 GB) via `snapshot_download`, compile megakernel `.so` with `VOCAB=3072` (~3 min, cached) (README.md:242-247).
- Health/smoke: `curl -s http://localhost:8000/health` → `{"status":"ok","sample_rate":24000}`; synth via `POST http://localhost:8000/synthesize` with `{"text":"Hello, this is a test."}`; benchmarks via `python3 benchmarks/benchmark.py` (README.md:276-296).
- Local Mac: `brew install portaudio`, `python3 -m venv .venv`, `pip install "pipecat-ai[local,silero]" deepgram-sdk groq aiohttp numpy`; keys from console.deepgram.com and console.groq.com; tunnel `ssh -N -f -L 8000:localhost:8000 -p <PORT> root@<IP>` (README.md:302-346).
- Truncation note: the source chunk ends mid-sentence at `01-overview.md:348-350` ("Verify tunnel is work") followed only by a macro-component marker, so the remainder of the local run/benchmark/limitations/env-var sections is cut and not covered here.

**Covers:** README.md overview (what-this-is, how-it-works diagram, architecture decisions, kernel modifications, Part A GPU-server setup, Part B local-Mac setup as far as the chunk extends)
