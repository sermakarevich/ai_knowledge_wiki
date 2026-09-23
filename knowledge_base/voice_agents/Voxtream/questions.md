---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: herimor/voxtream

### Q1. What is VoXtream2 in one sentence, and what makes it "full-stream"?

> [!tip]- Answer
> VoXtream2 is a zero-shot full-stream text-to-speech model with dynamic speaking-rate control that can be updated mid-utterance on the fly. It clones a voice from a short prompt and streams synthesized speech as it generates, rather than waiting for the whole utterance. See [[wiki/01-overview|Overview]].

### Q2. How does VoXtream2's dynamic speaking-rate control work?

> [!tip]- Answer
> It uses distribution matching and classifier-free guidance to enable fine-grained speaking-rate adjustment during generation. The target rate is given in syllables per second (e.g. 2.0) and can be changed mid-utterance, including via the interactive demo. See [[wiki/01-overview|Overview]].

### Q3. What streaming performance does VoXtream2 claim, and on what hardware?

> [!tip]- Answer
> It runs 4x faster than real-time with 74 ms first-packet latency in full-stream mode on a consumer GPU (RTX3090: 74 ms FPL, 0.256 RTF uncompiled; 63 ms, 0.173 compiled). The `voxtream-benchmark` entry point reproduces RTF and first-packet latency, with a `--compile` flag trading initial compile time for faster inference. See [[wiki/01-overview|Overview]].

### Q4. What are VoXtream2's input contract and runtime limits?

> [!tip]- Answer
> The voice prompt should be 3–10 s of audio (max 20 s, longer is trimmed) and the text max 1000 characters (longer trimmed), with an optional speaking rate in syllables per second. It needs 2.2 Gb VRAM (+2 Gb with speech enhancement), caps generation at 1 minute, and was tested on Ubuntu 22.04 / CUDA 12 / PyTorch 2.4. See [[wiki/01-overview|Overview]].

### Q5. Through which interfaces can a user run VoXtream2?

> [!tip]- Answer
> Entry points are the `voxtream` CLI (output-streaming and `--full-stream` modes with `--spk-rate` and `--prompt-enhancement` flags), the Python API (`SpeechGenerator.generate_stream` with `prompt_audio_path`, `text`, `speaking_rate`), the `voxtream-app` Gradio demo, the `voxtream-server` websocket server plus client, and `voxtream-benchmark`. Prompt text masking additionally allows acoustic prompts in any language for translingual cloning. See [[wiki/01-overview|Overview]].

### Q6. What do the Voxtream repository-root files define for licensing, attribution, packaging, and code quality?

> [!tip]- Answer
> The root carries dual licenses (Apache 2.0 in LICENSE-APACHE, MIT copyright 2025 Nikita Torgashov), a NOTICE attributing the Depth Transformer to SesameAI, and ATTRIBUTION.md requiring CC BY 4.0 credit to the Emilia and HiFiTTS-2 datasets behind released weights. Packaging pins the stack in requirements.txt (torch, moshi, transformers, gradio, hydra-core, whisper, silero-vad) and MANIFEST.in assets/configs, while pre-commit enforces black, isort, ruff, and mypy, and .gitignore excludes artifacts like experiments/ and audio .npy files. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. (Evaluation) A team wants low-latency live voice cloning on a consumer GPU with adjustable speaking pace — should they pick VoXtream2, and with what caveats?

> [!tip]- Answer
> Yes, VoXtream2 is a strong fit: zero-shot cloning from a 3–10 s prompt, 74 ms first-packet latency at 4x real-time on an RTX3090-class GPU, and mid-utterance rate control suit live use. Caveats are the 1-minute generation cap, 2.2 Gb (+2 Gb with enhancement) VRAM need, eSpeak NG and CUDA-stack prerequisites, and the consent requirement prohibiting cloning someone's voice without permission. See [[wiki/01-overview|Overview]].
