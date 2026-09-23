> PDF location: https://github.com/Akshat21Shah/e3-tts-assessment (no source.pdf fetched; repo source — see Source field below)
# Akshat21Shah/e3-tts-assessment
Source: https://github.com/Akshat21Shah/e3-tts-assessment
Kind: repo
Fetched: 2026-09-22T14:35:13.639327+00:00
Tool: git-clone

# Akshat21Shah/e3-tts-assessment

Commit: df8f66d7993bbdb88eab7a7e1ba7bbc95e08a4b6

## README

# Megakernel-Accelerated Qwen3-TTS Voice Agent

> **Real-time streaming voice agent:** speak into your laptop mic → Deepgram transcribes speech → Groq LLaMA-3.3-70B generates a reply → Qwen3-TTS synthesises audio on a rented GPU using a hand-rolled CUDA megakernel → you hear the response within ~250 ms.
>
> **TTFC ≈ 36 ms · RTF ≈ 0.13** (RTX 5090, Blackwell)

---

## Table of Contents

1. [What this is](#1-what-this-is)
2. [How it works](#2-how-it-works)
3. [Repo layout](#3-repo-layout)
4. [Architecture decisions](#4-architecture-decisions)
5. [Kernel modifications](#5-kernel-modifications)
6. [Part A — GPU server setup](#6-part-a--gpu-server-setup-remote-machine)
   - [Which GPU to rent and where](#61-which-gpu-to-rent-and-where)
   - [Rent on vast.ai step by step](#62-rent-a-gpu-on-vastai--step-by-step)
   - [SSH into the server](#63-ssh-into-the-server)
   - [Clone and run one-shot setup](#64-clone-repo-and-run-one-shot-setup)
   - [Start the TTS server](#65-start-the-tts-server)
   - [Quick smoke test](#66-quick-smoke-test)
   - [Run benchmarks](#67-run-benchmarks-optional)
7. [Part B — Local machine setup (Mac)](#7-part-b--local-machine-setup-mac)
   - [Install system dependencies](#71-install-system-dependencies)
   - [Clone repo and install packages](#72-clone-repo-and-install-python-packages)
   - [Get API keys](#73-get-api-keys)
   - [Open SSH tunnel](#74-open-ssh-tunnel-to-tts-server)
   - [Run the voice agent](#75-run-the-voice-agent)
8. [Benchmark results](#8-benchmark-results)
9. [Potential performance improvements](#9-potential-performance-improvements)
10. [Limitations](#10-simplifications--known-limitations)
11. [Environment variables](#11-environment-variables-reference)

---

## 1. What this is

A **sub-60 ms time-to-first-chunk (TTFC) voice agent** built by replacing the slow HuggingFace autoregressive decoder in the Qwen3-TTS model with a hand-rolled CUDA megakernel. The result is a natural-sounding, low-latency voice assistant you can speak to in real time.

The TTS heavy lifting (GPU inference) runs on a cheap rented cloud GPU. Your laptop only handles audio I/O, speech recognition (Deepgram, cloud), and LLM calls (Groq, cloud). The two sides are connected via a plain SSH tunnel — no cloud provider lock-in, no special networking.

---

## 2. How it works

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

**Key metrics:**
| Metric | Definition | Target | Achieved |
|---|---|---|---|
| **TTFC** | ms from HTTP request to first audio byte | < 60 ms | 35–38 ms |
| **RTF** | inference time / audio duration | < 0.15 | 0.12–0.15 |

---

## 3. Repo layout

```
e3-tts-assessment/
├── server/
│   ├── tts_server.py     # FastAPI TTS server — CUDA graphs + vocoder batching
│   ├── tts_talker.py     # TTSTalkerDecoder — megakernel adapter + KV-cache bridge
│   └── tts_build.py      # JIT-compiles megakernel .so with VOCAB=3072
├── pipeline/
│   └── pipeline.py       # Pipecat 1.1.0 voice agent (Deepgram → Groq → TTS)
├── benchmarks/
│   └── benchmark.py      # TTFC / RTF measurement (WARMUP=1, RUNS=3)
├── scripts/
│   ├── setup.sh          # One-shot setup for GPU server
│   └── patch_kernel.py   # Patches kernel.cu with #ifndef LDG_VOCAB_SIZE
├── requirements.txt      # Python deps for GPU server
└── README.md
```

| Component | Runs on | Why |
|---|---|---|
| `server/` | GPU server | Needs NVIDIA GPU |
| `pipeline/` | Your laptop | Needs mic + speakers |
| `benchmarks/` | Either | Talks to server over HTTP |
| `scripts/` | GPU server | Sets up GPU environment |

---

## 4. Architecture decisions

### Why a CUDA megakernel

The Qwen3-TTS talker is a 28-layer Transformer that autoregressively generates codec tokens at 12 Hz. Standard HuggingFace `generate()` costs ~20 ms per decode step (Python/CUDA kernel launch overhead per layer). At 12 tokens/second that gives RTF ≈ 0.24 — too slow for real-time.

The [AlpinDale megakernel](https://github.com/AlpinDale/qwen_megakernel) fuses all 28 layers into **one CUDA kernel launch** (128 blocks × 512 threads). No Python overhead between layers → **0.86 ms/step** → talker RTF ≈ 0.01.

### AudioInputGate (echo prevention)

Without AEC hardware, the laptop mic picks up speaker output → Deepgram transcribes the bot's own voice → LLM responds again → infinite loop. `AudioInputGate` is a Pipecat `FrameProcessor` that drops all `AudioRawFrame` events while `_bot_speaking=True` and for 400 ms after `BotStoppedSpeakingFrame`, preventing the feedback loop entirely.

### Additional server optimisations

| Optimisation | Effect |
|---|---|
| `torch.compile(code_predictor)` | 18 ms → 5 ms per frame |
| CUDA graph for code-predictor loop | Eliminates Python overhead |
| Vocoder batching (`CHUNK_FRAMES=4`) | First frame sent immediately (TTFC); rest batched at 3 ms/frame |

### Audio format

The server sends raw int16 PCM bytes (`X-Encoding: int16-le`, `X-Sample-Rate: 24000`). The pipeline passes these **directly** to `TTSAudioRawFrame.audio` — no float32 conversion, no numpy normalisation.

---

## 5. Kernel modifications

The [AlpinDale megakernel](https://github.com/AlpinDale/qwen_megakernel) was written for LLMs with a 151,936-token vocabulary. Three changes were needed for TTS:

### 1. LDG_VOCAB_SIZE patch

`kernel.cu` had `constexpr int LDG_VOCAB_SIZE = 151936` which a `-D` compiler flag cannot override. `scripts/patch_kernel.py` rewrites it to:

```c
#ifndef LDG_VOCAB_SIZE
#define LDG_VOCAB_SIZE 151936
#endif
```

`server/tts_build.py` then compiles with `-DLDG_VOCAB_SIZE=3072` (the TTS codec vocabulary size).

### 2. Slot-0 embedding trick

The kernel reads `embed_weight[token_id × HIDDEN]` expecting a single integer token. In TTS, each decode step's input is a sum of 16 codec embeddings + a text-guidance vector — no single integer. Fix: pre-compute the combined embedding on the Python side, write it into row 0 of a 1-row fake embedding table, and always pass `token_id=0` to the kernel.

### 3. Zero-copy KV cache bridge

Prefill runs in standard PyTorch (qwen-tts). KV tensors are `copy_()` directly into the megakernel's pre-allocated CUDA buffers. This works because Qwen3's m-RoPE collapses to 1D RoPE for text tokens and `rope_theta=1_000_000` matches — values are bit-identical.

---

## 6. Part A — GPU server setup (remote machine)

### 6.1 Which GPU to rent and where

**Minimum requirements:** NVIDIA GPU with ≥ 16 GB VRAM, CUDA ≥ 11.8.

**Recommended GPUs** (cheapest to fastest):
| GPU | VRAM | approx. $/hr (vast.ai) | Notes |
|---|---|---|---|
| RTX 3090 | 24 GB | ~$0.25 | Good baseline |
| RTX 4090 | 24 GB | ~$0.40 | Recommended — fast + affordable |
| A6000 | 48 GB | ~$0.60 | Professional grade |
| A100 40GB | 40 GB | ~$1.00 | Datacenter |
| RTX 5090 | 32 GB | ~$1.20 | Benchmarked here (sm_120a) |

**Recommended Docker image:** `nvcr.io/nvidia/pytorch:24.01-py3`
(includes Python 3.10, PyTorch 2.3, CUDA 12.1, nvcc — everything needed)

**Recommended platforms:**
- [vast.ai](https://vast.ai) — cheapest, most GPU variety (used in this project)
- [RunPod](https://runpod.io) — slightly easier UI
- [Lambda Labs](https://lambdalabs.com) — more stable pricing

---

### 6.2 Rent a GPU on vast.ai — step by step

1. **Create account** at [vast.ai](https://vast.ai), add a payment method ($5 minimum).

2. **Add your SSH public key**
   - On your laptop: `cat ~/.ssh/id_rsa.pub` (or `id_ed25519.pub`)
   - vast.ai dashboard → **Account** → **SSH Keys** → paste your key

3. **Search for an instance**
   - **Search** tab → set filters: GPU RAM ≥ 16 GB · CUDA ≥ 11.8 · Disk ≥ 30 GB
   - Under **Image**, search for `nvcr.io/nvidia/pytorch:24.01-py3`
   - Select an RTX 4090 or similar → click **Rent**

4. **Enable port 8000**
   - In the instance settings, add port **8000** to open ports

5. **Copy the SSH command** shown in the instance panel:
   ```
   ssh -p <PORT> root@<IP>
   ```

---

### 6.3 SSH into the server

```bash
ssh -p <PORT> root@<IP>
```

Start a tmux session so the server keeps running after you disconnect:

```bash
tmux new -s main
```

---

### 6.4 Clone repo and run one-shot setup

```bash
# Inside the GPU server (in tmux)
git clone https://github.com/Akshat21Shah/e3-tts-assessment.git
cd e3-tts-assessment

bash scripts/setup.sh
```

`setup.sh` does:
1. Clones [AlpinDale/qwen_megakernel](https://github.com/AlpinDale/qwen_megakernel)
2. Patches `kernel.cu` with `#ifndef LDG_VOCAB_SIZE` guard
3. `pip install -r requirements.txt` (includes `qwen-tts`, `huggingface_hub`, `hf_transfer`, `fastapi`, etc.)
4. Downloads `Qwen/Qwen3-TTS-12Hz-0.6B-Base` weights (~1.4 GB) via Python `snapshot_download`
5. Compiles the CUDA megakernel `.so` with `VOCAB=3072` — takes ~3 min, cached after

> **Note on `huggingface-cli`:** `setup.sh` uses Python's `huggingface_hub.snapshot_download()` directly instead of the CLI, because `huggingface-cli` is not always on `$PATH` on fresh vast.ai instances even after `pip install`.

> **If `nvcc` is not found:**
> ```bash
> apt-get update && apt-get install -y cuda-toolkit-12-1
> export PATH=/usr/local/cuda/bin:$PATH
> ```

---

### 6.5 Start the TTS server

```bash
# In a new tmux window: Ctrl+B C
python3 server/tts_server.py
```

Wait for:
```
[server] CUDA graph captured for code_predictor
INFO:     Application startup complete.
```

Detach from tmux: `Ctrl+B D` — server keeps running.

---

### 6.6 Quick smoke test

```bash
curl -s http://localhost:8000/health
# → {"status":"ok","sample_rate":24000}

# Optional: play audio (requires alsa-utils)
curl -s -X POST http://localhost:8000/synthesize \
     -H "Content-Type: application/json" \
     -d '{"text":"Hello, this is a test."}' \
  | aplay -r 24000 -f S16_LE -c 1
```

---

### 6.7 Run benchmarks (optional)

```bash
python3 benchmarks/benchmark.py
# Outputs TTFC and RTF for 4 test sentences
```

---

## 7. Part B — Local machine setup (Mac)

### 7.1 Install system dependencies

```bash
# Requires Homebrew (https://brew.sh)
brew install portaudio    # PyAudio microphone dependency
```

---

### 7.2 Clone repo and install Python packages

```bash
git clone https://github.com/Akshat21Shah/e3-tts-assessment.git
cd e3-tts-assessment

python3 -m venv .venv
source .venv/bin/activate

pip install "pipecat-ai[local,silero]" deepgram-sdk groq aiohttp numpy
```

> **macOS Python 3.13 SSL fix** (if you see certificate errors):
> ```bash
> bash "/Applications/Python 3.13/Install Certificates.command"
> ```

---

### 7.3 Get API keys

**Deepgram** (speech-to-text, free tier):
1. Sign up at [console.deepgram.com](https://console.deepgram.com)
2. Create a new API key

**Groq** (LLM, free tier with generous limits):
1. Sign up at [console.groq.com](https://console.groq.com)
2. Go to **API Keys → Create API Key**

---

### 7.4 Open SSH tunnel to TTS server

```bash
# Replace PORT and IP with your vast.ai instance values
ssh -N -f -L 8000:localhost:8000 -p <PORT> root@<IP>

# Verify tunnel is work

... (truncated, 4715 more characters)

## Top-level layout

- .gitignore (~25 lines)
- benchmarks/ (dir, 1 files, ~53 lines)
- pipeline/ (dir, 1 files, ~217 lines)
- README.md (~464 lines)
- requirements.txt (~26 lines)
- scripts/ (dir, 2 files, ~93 lines)
- server/ (dir, 3 files, ~641 lines)

