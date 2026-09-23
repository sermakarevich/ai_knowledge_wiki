---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Akshat21Shah/e3-tts-assessment

### Q1. What is this voice agent, and how does the end-to-end streaming loop fit together?

> [!tip]- Answer
> It is a real-time voice agent where laptop-mic speech is transcribed by Deepgram over WebSocket, answered by streaming Groq LLaMA-3.3-70B (~200 ms), and synthesised by Qwen3-TTS on a rented cloud GPU behind a plain SSH tunnel, so the user hears a reply within ~250 ms. The full path is microphone → Deepgram STT → Groq LLM → HTTP POST /synthesize to FastAPI port 8000 → PyTorch prefill → CUDA megakernel decode → code predictor → vocoder PCM stream → PyAudio speakers. The laptop handles only audio I/O plus cloud STT/LLM calls while all GPU-heavy TTS runs remotely. See [[wiki/01-overview|Overview]].

### Q2. Why was the hand-rolled CUDA megakernel necessary, and what did it achieve numerically?

> [!tip]- Answer
> The Qwen3-TTS talker autoregressively generates codec tokens at 12 Hz, and standard HuggingFace `generate()` cost ~20 ms per decode step in Python/CUDA launch overhead per layer, giving RTF ≈ 0.24 — too slow for real-time. Fusing all 28 talker Transformer layers into a single kernel launch (128 blocks × 512 threads) cut decode to 0.86 ms/step and talker RTF to ≈ 0.01. End to end this delivered TTFC ≈ 35–38 ms against a < 60 ms target and RTF ≈ 0.12–0.15 against a < 0.15 target on RTX 5090 Blackwell. See [[wiki/01-overview|Overview]].

### Q3. What three changes adapted the 151,936-vocab LLM megakernel to the 3072-token TTS codec vocab?

> [!tip]- Answer
> First, `scripts/patch_kernel.py` rewrites `kernel.cu`'s hard `constexpr int LDG_VOCAB_SIZE = 151936` into an `#ifndef` guard so `server/tts_build.py` can compile with `-DLDG_VOCAB_SIZE=3072`. Second, the slot-0 embedding trick pre-computes each step's combined input (sum of 16 codec embeddings plus a text-guidance vector) in Python, writes it into row 0 of a 1-row fake embedding table, and always passes `token_id=0`. Third, a zero-copy KV-cache bridge `copy_()`s PyTorch prefill KV tensors directly into the megakernel's pre-allocated CUDA buffers, valid because Qwen3 m-RoPE collapses to 1D RoPE for text tokens with matching `rope_theta=1_000_000`. See [[wiki/01-overview|Overview]].

### Q4. Beyond the megakernel, which server-side optimisations protect TTFC and per-frame cost?

> [!tip]- Answer
> `torch.compile(code_predictor)` cuts the code predictor from 18 ms to ~5 ms per frame, and a CUDA graph over the code-predictor loop eliminates the remaining Python overhead. Vocoder batching with `CHUNK_FRAMES=4` sends the first frame immediately to protect TTFC, then batches the rest at ~3 ms/frame. Together a frame costs roughly 5 ms + 0.9 ms + 3 ms ≈ 8.9 ms against 83 ms of audio. See [[wiki/01-overview|Overview]].

### Q5. How does the pipeline prevent mic/speaker feedback, and what audio format crosses the wire?

> [!tip]- Answer
> `AudioInputGate`, a Pipecat `FrameProcessor`, drops all `AudioRawFrame` events while `_bot_speaking=True` and for 400 ms after `BotStoppedSpeakingFrame`, stopping the mic from re-transcribing the bot's own speaker output into an infinite loop. The server sends raw int16 PCM bytes (`X-Encoding: int16-le`, `X-Sample-Rate: 24000`) that are passed directly into `TTSAudioRawFrame.audio` with no float32 conversion or numpy normalisation. See [[wiki/01-overview|Overview]].

### Q6. What does `.gitignore` exclude, and why?

> [!tip]- Answer
> It excludes the `model/` weights directory so large binaries come from Git LFS or the `setup.sh` download instead, plus the compiled megakernel cache (`~/.cache/torch_extensions/`, `__pycache__/`, `*.pyc`, `*.pyo`) and Python virtual environments (`venv/`, `.venv/`, `env/`). It also ignores editor/OS artifacts (`.DS_Store`, `.vscode/`, `*.swp`) and assessment or personal docs (`*.pdf`, `e3-assessment.txt`, `Technical assessment mail.txt`, `takehome_project.docx`, `takehome_project.txt`). See [[wiki/02-top-level-files|top-level-files]].

### Q7. What dependency layers does `requirements.txt` pin?

> [!tip]- Answer
> It pins core inference (`torch>=2.3.0` CUDA-enabled, `transformers>=4.47.0`, `safetensors>=0.4.0`, `numpy>=1.24.0`) and the model/download layer (`qwen-tts>=0.1.1`, `huggingface_hub>=0.23.0`, optional `hf_transfer>=0.1.6`). Serving and benchmarking are covered by `fastapi`/`uvicorn`/`pydantic` and `aiohttp`, while the voice pipeline uses `pipecat-ai[silero,local]` with `deepgram-sdk` and `groq` as the STT/LLM integrations. See [[wiki/02-top-level-files|top-level-files]].

### Q8. A small team wants to reproduce this real-time voice agent as cheaply as possible — what would you recommend?

> [!tip]- Answer
> Recommend renting an RTX 3090 (~$0.25/hr on vast.ai, ≥16 GB VRAM, CUDA ≥11.8) with the `nvcr.io/nvidia/pytorch:24.01-py3` image and the documented `setup.sh` flow, since the 5090 beat both targets with wide margin and the 3090 is listed as a good baseline with likely headroom. Keep the SSH-tunnel split for the prototype but replace it with authenticated TLS before any production use, and step up to the RTX 4090 (~$0.40/hr) only if the 3090 misses the RTF < 0.15 target. See [[wiki/01-overview|Overview]].
