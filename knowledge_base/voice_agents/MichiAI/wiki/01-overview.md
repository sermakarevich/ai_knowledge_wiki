> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** MichiAI is a 530M-parameter multimodal speech LLM for full-duplex interaction that listens and speaks simultaneously with ~80ms latency.
## Key points
- MichiAI is a lightweight, multimodal speech large language model designed for **full-duplex interaction** (README.md:16).
- Unlike traditional serial pipelines (`ASR → LLM → TTS`), MichiAI can listen and speak simultaneously, mimicking natural human conversation with ultra-low latency (README.md:16-17).
- The advertised spec is 530M parameters with ~80ms time-to-first-audio (TTFA) tested on RTX 4090, using continuous embeddings plus rectified flow matching on a SmolLM-360m backbone (README.md:30-36).
- It bypasses slow RVQ decoding in favor of continuous audio latents, enabling high-fidelity audio with fewer forward passes (README.md:42).
- It supports zero-shot voice cloning from a few seconds of audio prompt and mixed text-plus-audio prompting compatible with RAG frameworks (README.md:43-44).
- Its Listening Head maps raw audio into continuous embeddings while generating text tokens, and its Speaking Head predicts audio embeddings via rectified flow matching decoded by a lightweight causal HiFi-GAN vocoder (README.md:51-55).
- Despite 530M parameters and ~5,000 hours of audio training data, it claims to retain text-LLM reasoning without coherence-loss degradation versus 7B+ quantized rivals (README.md:45, README.md:60-67).
---
## Quick Specs
Verbatim spec table from the README (README.md:28-36):

| Feature | Specification |
| :--- | :--- |
| **Model Size** | 530M Parameters |
| **Latency (TTFA)** | ~80ms (tested on RTX 4090) |
| **Architecture** | Continuous Embeddings + Rectified Flow Matching |
| **Base Backbone** | SmolLM-360m |
| **Key Innovation** | No Coherence Loss / Single Step Decoding |

The headline claim is `A full-duplex speech LLM with ~80ms latency.` (README.md:11).

## Key Features
Verbatim feature list (README.md:39-46):

* **Full-Duplex Capability:** Handles interjections and backchanneling implicitly. It "hears" while it "talks."
* **Continuous Audio Latents:** Bypasses the slow decoding of traditional RVQ (Residual Vector Quantization) models. This enables **high-fidelity audio** with much fewer forward passes.
* **Zero-Shot Voice Cloning:** Captures vocal timbre and style from just a few seconds of audio prompt.
* **Multimodal Input:** Supports mixed text and audio prompting, making it compatible with existing RAG (Retrieval-Augmented Generation) frameworks.
* **No Coherence Loss:** Retains the reasoning and linguistic capabilities of the underlying text LLM without the typical degradation seen in speech-to-speech models.
* **Paralinguistics:** Naturally models breathing, laughing, and emotional prosody learned directly from the dataset.

## Architecture Overview
Two heads (README.md:49-55):

### 1. The Listening Head
A multi-modal encoder mapping raw audio into continuous embeddings while simultaneously generating text tokens, covering both semantic meaning and emotional context (README.md:51-52).

### 2. The Speaking Head
Predicts audio embeddings using **Rectified Flow Matching** for fast, high-quality, diverse speech generation, then processes the embeddings through a lightweight, causal **HiFi-GAN vocoder** for real-time streaming (README.md:54-55).

## Performance Comparison
The README frames MichiAI as smaller and trained on less data while maintaining reasoning by reusing pretrained text knowledge (README.md:60). Verbatim table (README.md:62-67):

| Model | Parameters | Audio Training Data | Approach |
| :--- | :--- | :--- | :--- |
| Hertz-dev | 8.5B | 20,000,000 hours | Quantized |
| Moshi | 7B | 7,000,000 hours | Quantized |
| Qwen-Omni | 7B+ | 8,000,000+ hours | Quantized |
| **MichiAI** | **530M** | **~5,000 hours** | **Continuous** |

## Roadmap
Verbatim roadmap checklist (README.md:70-77):

* [x] **Core Architecture:** Continuous Embeddings + Flow Matching implementation.
* [X] **Conversational Tuning:** Training on specific dialogue datasets for better turn-taking.
* [ ] **Scaling:** Implementing a larger LLM backbone.
* [ ] **Multilingual Support:** Integrating non-English datasets.
* [ ] **Hugging Face Space:** Launching a live interactive demo.
* [ ] **Release API client** Release an API client to this repo

No truncated files were noted in the chunk; all claims above come from the README excerpt.

**Covers:** `README.md` (repo root overview: goals, specs, features, architecture, performance comparison, roadmap)
