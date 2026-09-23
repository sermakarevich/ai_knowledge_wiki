> [[index|Wiki]] | [[summary|Summary]]
# Akshat21Shah/e3-tts-assessment — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** A real-time streaming voice agent where laptop-mic speech is transcribed by Deepgram, answered by Groq LLaMA-3.3-70B, and synthesised by Qwen3-TTS on a rented GPU via a hand-rolled CUDA megakernel so the user hears a response within ~250 ms (README.md:9).
## Key points
- Delivers sub-60 ms time-to-first-chunk (TTFC) by replacing the slow HuggingFace autoregressive decoder in Qwen3-TTS with a hand-rolled CUDA megakernel, achieving TTFC ≈ 36 ms and RTF ≈ 0.13 on RTX 5090 Blackwell (README.md:11, README.md:45).
- Splits work so GPU-heavy TTS inference runs on a cheap rented cloud GPU while the laptop handles only audio I/O, Deepgram cloud STT, and Groq cloud LLM calls, joined by a plain SSH tunnel with no provider lock-in (README.md:47).
- Streams end-to-end as Microphone → Deepgram STT (WebSocket real-time ASR) → Groq LLaMA-3.3-70B (streaming, ~200 ms) → HTTP POST /synthesize via SSH tunnel → FastAPI TTS server on port 8000 → PyTorch prefill → CUDA megakernel decode → code predictor → vocoder PCM stream → PyAudio speakers (README.md:53-80).
- Fuses all 28 talker Transformer layers into one CUDA kernel launch (128 blocks × 512 threads), cutting ~20 ms/step HuggingFace generate() overhead to 0.86 ms/step and talker RTF to ≈ 0.01 (README.md:122-124).
- Prevents mic/speaker feedback loops with AudioInputGate, a Pipecat FrameProcessor that drops AudioRawFrame events while _bot_speaking=True and for 400 ms after BotStoppedSpeakingFrame (README.md:128).
- Sends raw int16 PCM bytes (X-Encoding: int16-le, X-Sample-Rate: 24000) passed directly to TTSAudioRawFrame.audio with no float32 conversion or numpy normalisation (README.md:140).
- Adapts the 151,936-vocab LLM megakernel to the 3072-token TTS codec vocab via an LDG_VOCAB_SIZE #ifndef guard, a slot-0 embedding trick, and a zero-copy KV-cache bridge relying on collapsed 1D m-RoPE with rope_theta=1_000_000 (README.md:148-166).
## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** The top-level files define what is excluded from version control and the pinned Python dependency stack for inference, serving, benchmarking, and the voice pipeline.
## Key points
- `.gitignore` excludes the `model/` weights directory, directing users to Git LFS or `setup.sh` download instead (`.gitignore:1-2`).
- `.gitignore` excludes the compiled megakernel cache `~/.cache/torch_extensions/` plus `__pycache__/`, `*.pyc`, and `*.pyo` (`.gitignore:4-8`).
- `.gitignore` excludes Python virtual environments `venv/`, `.venv/`, and `env/` (`.gitignore:10-13`).
- `.gitignore` excludes editor/OS artifacts `.DS_Store`, `.vscode/`, and `*.swp` (`.gitignore:15-18`).
- `.gitignore` excludes assessment/personal docs `*.pdf`, `e3-assessment.txt`, `Technical assessment mail.txt`, `takehome_project.docx`, and `takehome_project.txt` (`.gitignore:20-25`).
- `requirements.txt` pins the core inference stack `torch>=2.3.0` (CUDA-enabled), `transformers>=4.47.0`, `safetensors>=0.4.0`, and `numpy>=1.24.0` (`requirements.txt:1-5`).
- `requirements.txt` pins the model/download layer `qwen-tts>=0.1.1`, `huggingface_hub>=0.23.0`, and optional fast downloader `hf_transfer>=0.1.6`, plus the serving, benchmarking, and voice-pipeline layers `fastapi`/`uvicorn`/`pydantic`, `aiohttp`, `pipecat-ai[silero,local]`, `deepgram-sdk`, and `groq` (`requirements.txt:7-26`).
## The system in five moves
1. Laptop captures mic audio and streams it through Deepgram real-time STT and Groq LLaMA-3.3-70B so reply text is ready in ~200 ms.
2. Heavy TTS work is offloaded to a cheap rented GPU server reached over a plain SSH tunnel, keeping the laptop to audio I/O plus cloud STT/LLM calls.
3. The Qwen3-TTS talker bottleneck (~20 ms/step via HuggingFace generate) is removed by fusing all 28 layers into one CUDA megakernel launch at 0.86 ms/step.
4. The LLM megakernel is adapted to TTS via the LDG_VOCAB_SIZE 3072 guard, slot-0 combined-embedding trick, and zero-copy KV-cache bridge, with torch.compile, CUDA graphs, and vocoder batching for TTFC 35–38 ms and RTF 0.12–0.15.
5. Pipecat wires the loop with AudioInputGate echo suppression and raw int16 PCM at 24 kHz straight to speakers, while .gitignore/requirements.txt pin the reproducible inference, serving, and pipeline stack.
