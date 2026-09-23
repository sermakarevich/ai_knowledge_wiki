> [[index|Wiki]] | [[summary|Summary]]
# KetsuiLabs/MichiAI — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** MichiAI is a 530M-parameter multimodal speech LLM for full-duplex interaction that listens and speaks simultaneously with ~80ms latency.

## Key points

- MichiAI is a lightweight, multimodal speech large language model designed for **full-duplex interaction** (README.md:16).
- Unlike traditional serial pipelines (`ASR → LLM → TTS`), MichiAI can listen and speak simultaneously, mimicking natural human conversation with ultra-low latency (README.md:16-17).
- The advertised spec is 530M parameters with ~80ms time-to-first-audio (TTFA) tested on RTX 4090, using continuous embeddings plus rectified flow matching on a SmolLM-360m backbone (README.md:30-36).
- It bypasses slow RVQ decoding in favor of continuous audio latents, enabling high-fidelity audio with fewer forward passes (README.md:42).
- It supports zero-shot voice cloning from a few seconds of audio prompt and mixed text-plus-audio prompting compatible with RAG frameworks (README.md:43-44).
- Its Listening Head maps raw audio into continuous embeddings while generating text tokens, and its Speaking Head predicts audio embeddings via rectified flow matching decoded by a lightweight causal HiFi-GAN vocoder (README.md:51-55).
- Despite 530M parameters and ~5,000 hours of audio training data, it claims to retain text-LLM reasoning without coherence-loss degradation versus 7B+ quantized rivals (README.md:45, README.md:60-67).

## 2. [[wiki/02-top-level-files|top-level-files]]

**In one sentence:** Top-level files configure the docs-site presentation and exclude build output from version control.

## Key points

- The component covers exactly 2 top-level source files: `.gitignore` and `_config.yml` (`.gitignore:1`, `_config.yml:1`).
- `.gitignore` excludes the `dist` build-output directory from version control (`.gitignore:1`).
- `_config.yml` selects the `jekyll-theme-minimal` Jekyll theme for the project site (`_config.yml:1`).
- `_config.yml` sets the site title to `MichiAI` (`_config.yml:2`).
- `_config.yml` sets the site description to `Full-duplex speech LLM with ~75ms latency.` (`_config.yml:3`).

## The system in five moves

1. MichiAI rejects the serial `ASR → LLM → TTS` pipeline in favor of a full-duplex speech LLM that listens and speaks simultaneously.
2. It replaces slow RVQ decoding with continuous audio latents plus rectified flow matching to reach ~80ms time-to-first-audio at 530M parameters on a SmolLM-360m backbone.
3. A Listening Head grounds raw audio in continuous embeddings with semantic and emotional context while a Speaking Head generates speech through a causal HiFi-GAN vocoder, adding zero-shot cloning, RAG-compatible prompting, and paralinguistics without coherence loss.
4. Against 7B+ quantized rivals trained on millions of hours, it claims equal reasoning from only ~5,000 hours of audio, with scaling, multilingual support, and a live demo left to the roadmap.
5. At the repo surface this system is presented through a minimal Jekyll docs site titled `MichiAI`, with `dist` build output excluded from version control.
