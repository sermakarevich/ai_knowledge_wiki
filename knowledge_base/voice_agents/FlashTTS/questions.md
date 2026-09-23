---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: ASLP-lab/FlashTTS
### Q1. What is FlashTTS and what are its headline claims?
> [!tip]- Answer
> FlashTTS is an open-source low-latency streaming TTS framework built on a lagged multi-track architecture with parallel Multi-Token Prediction and an X-pred mean-flow decoder. It claims 2-NFE token-to-mel generation at 325 ms first-packet latency while preserving zero-shot voice cloning and cross-lingual intelligibility. See [[wiki/01-overview|Overview]].
### Q2. What is the end-to-end FlashTTS inference pipeline?
> [!tip]- Answer
> The pipeline is Text/Speech Input → Text Tokenizer plus CAMPPlus Speaker Extractor → decoder-only LLM with MTP → X-pred mean-flow module at 2 NFE → HiFi-GAN vocoder → 24 kHz audio. Core code splits into `cosyvoice/` for the LLM, tokenizer, and frontend and `jit_meanflow_xpred/` for token-to-mel plus vocoding, with `third_party/` for CAMPPlus and Matcha-TTS. See [[wiki/01-overview|Overview]].
### Q3. How does FlashTTS streaming chunking work?
> [!tip]- Answer
> The lagged multi-track frontend stacks streaming text and speech tracks so synthesis starts without sentence-level buffering. Decoding uses a 24-token first chunk, then an 18-token hop with 6-token lookahead per step over a 24-token context, emitting 18 tokens per chunk. See [[wiki/01-overview|Overview]].
### Q4. How do you run FlashTTS inference, and what speaker conditioning does zero-shot cloning use?
> [!tip]- Answer
> Run `python examples/inference.py --mode flash_tts` with text plus a reference wav for full TTS, `--mode meanflow_only` with a token file plus reference wav to test the acoustic model alone, and add `--stream` for chunked mode. Zero-shot cloning conditions on a 192-dim CAMPPlus embedding extracted from 16 kHz single-channel reference audio via mel-spectrogram plus DTDNN layers. See [[wiki/01-overview|Overview]].
### Q5. What does the repo's `.gitignore` exclude, and why?
> [!tip]- Answer
> It excludes Python build and cache artifacts (`__pycache__/`, `*.py[cod]`, `build/`, `dist/`, `*.egg-info/`), virtual environments and IDE state, and large binary weights (`*.pt`, `*.pth`, `*.ckpt`, `ckpts/`, `checkpoints/`, `pretrained_models/`). It also excludes runtime outputs (`*.log`, `inference_output/`, `outputs/`), OS files, notebook checkpoints, and local secrets, so only source and configs are versioned while weights are fetched. See [[wiki/02-top-level-files|Top-level-files]].
### Q6. What does `requirements.txt` pin for compute, serving, and audio?
> [!tip]- Answer
> It pins `torch==2.3.1` with `torchaudio==2.3.1` from the CUDA 12.1 wheel index as the compute base, alongside serving pieces (`fastapi`/`uvicorn`/`gradio`/`grpcio`) and training pieces (`lightning`, `hydra-core`, `diffusers`, `transformers`). Platform-conditional pins install `deepspeed`, `onnxruntime-gpu`, and `tensorrt-cu12*` only on Linux and plain `onnxruntime` on macOS/Windows, plus an audio toolchain of `librosa`, `soundfile`, `pyworld`, `openai-whisper`, and `wetext`. See [[wiki/02-top-level-files|Top-level-files]].
### Q7. Would you recommend FlashTTS for a low-latency multilingual voice-cloning product?
> [!tip]- Answer
> Yes, provided you can verify the 325 ms first-packet claim on your own GPU and reference-audio setup, since native streaming, 2-NFE acoustic decoding, and zero-shot cloning across Chinese, English, French, German, Japanese, and Korean directly match that need. The main caveats are its research-demo maturity and CosyVoice/F5-TTS-derived complexity, so confirm 2-step output quality for your voices before committing. See [[wiki/01-overview|Overview]].
