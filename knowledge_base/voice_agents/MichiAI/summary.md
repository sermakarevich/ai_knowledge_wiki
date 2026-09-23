# Technical Analysis: KetsuiLabs/MichiAI

**Repository:** https://github.com/KetsuiLabs/MichiAI
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Serial voice pipelines (`ASR → LLM → TTS`) are half-duplex: the system cannot hear while it speaks, so interjections, backchanneling, and turn-taking incur multi-hundred-millisecond gaps (README.md:16-17). The problem space is real-time spoken dialogue requiring simultaneous listening and speaking with low time-to-first-audio.

MichiAI addresses it with a 530M-parameter multimodal speech LLM built for full-duplex interaction: it "hears" while it "talks" and handles interjections and backchanneling implicitly (README.md:16, README.md:39). The mechanism is continuous audio latents instead of Residual Vector Quantization (RVQ) decoding, claimed to yield high-fidelity audio with fewer forward passes (README.md:30, README.md:42). The primary user is a builder of real-time voice agents who needs sub-100ms response and voice-cloning/prompting hooks rather than a batch transcription or TTS consumer.

## 2. High-Level Architecture

```
              raw audio (mic / prompt)
                        │
                        ▼
              ┌─ Listening Head ──────────┐
              │ audio → continuous        │
              │ embeddings + text tokens  │◄── mixed text+audio prompt
              │ (semantics + emotion)     │
              └─────────┬─────────────────┘
                        │ embeddings / tokens
                        ▼
              ┌─ SmolLM-360m backbone ────┐
              │ reasoning carried over    │
              │ from pretrained text LLM  │
              └─────────┬─────────────────┘
                        ▼
              ┌─ Speaking Head ───────────┐
              │ rectified flow matching → │
              │ audio embeddings          │
              └─────────┬─────────────────┘
                        ▼
              ┌─ causal HiFi-GAN vocoder ─┐
              │ streaming waveform out    │
              └───────────────────────────┘
                        │
                        ▼
                   speaker output
         (Listening Head keeps ingesting
          input audio during synthesis ─ ►
          full-duplex loop)
```

Data-flow narrative: (1) The Listening Head maps raw input audio into continuous embeddings while generating text tokens, covering semantic meaning and emotional context (README.md:51-52). (2) Mixed text-plus-audio prompts enter the same path, which is what makes RAG-style conditioning possible (README.md:43-44). (3) The SmolLM-360m backbone carries the reasoning load, with the design goal of no coherence loss versus the underlying text LLM (README.md:30-36, README.md:45). (4) The Speaking Head predicts audio embeddings via rectified flow matching for fast diverse generation (README.md:54). (5) A lightweight causal HiFi-GAN vocoder decodes embeddings into streaming audio, fixing time-to-first-audio at ~80ms on RTX 4090 (README.md:30-36, README.md:54-55). (6) Listening continues during synthesis, so inbound interjections feed back into step 1 without stopping output (README.md:16-17, README.md:39).

Persistent state: no persistent store is documented in the analyzed wiki pages. State implied by the design is ephemeral session state (audio prompt for voice cloning, dialogue/RAG context) held in memory during a conversation; no database, checkpoint path, or on-disk format is cited.

## 3. Continuous Latents with Listening and Speaking Heads

The central concept is the continuous audio latent plus a two-head split around a frozen-capable text backbone. Representation: audio is carried as continuous embeddings end to end, explicitly positioned against quantized RVQ token approaches (README.md:30, README.md:42).

Named kinds/types, each with its citation:

- **Listening Head** — multimodal encoder mapping raw audio into continuous embeddings while generating text tokens, covering semantics and emotional context (README.md:51-52).
- **Speaking Head** — embedding predictor using rectified flow matching plus a lightweight causal HiFi-GAN vocoder for real-time streaming (README.md:54-55).
- **Continuous Audio Latents** — the shared representation; bypasses slow RVQ decoding for high fidelity with fewer forward passes (README.md:42).
- **Zero-shot voice prompt** — a few-seconds audio prompt capturing timbre and style (README.md:43).
- **Mixed text+audio prompt** — multimodal input mode compatible with RAG frameworks (README.md:44).
- **Paralinguistic channel** — breathing, laughing, emotional prosody modeled from data rather than rules (README.md:46).

Key queries: no query API is documented in the wiki pages. The operative "query" is a mixed prompt: audio and/or text in, streaming audio out. Verbatim capability statement:

```
* **Multimodal Input:** Supports mixed text and audio prompting, making it compatible with existing RAG (Retrieval-Augmented Generation) frameworks.
```

(README.md:43-44 paraphrase boundary: sentence above is verbatim from README.md:43-44 via 01-overview.md:32.)

## 4. LLM / External Service Integration

Providers and models named in the wiki: the text backbone is SmolLM-360m (README.md:30-36); the vocoder family is HiFi-GAN, causal variant for streaming (README.md:54-55). No third-party LLM API provider (OpenAI, Anthropic, hosted inference endpoint) is cited anywhere in the analyzed pages.

Required vs optional calls: no network API calls are documented. Generation is described as local forward passes: embedding encoding, flow-matching embedding prediction, vocoder decoding (README.md:51-55). Voice cloning requires a user-supplied audio prompt of a few seconds (README.md:43); RAG compatibility requires a caller-supplied retrieval context via the mixed-prompt path (README.md:44). Both are inputs, not service calls.

Environment variables: none documented in the analyzed pages. No keys, endpoints, or model URLs are cited.

## 5. Full-Duplex Listen-Speak Pipeline

Primary workflow: open a simultaneous listen/speak loop rather than a turn-based request/response. No source functions are cited in the wiki pages (only README prose and two config files), so each step is anchored to its README line citation instead of a `file.py:line` function reference; no function-level mapping exists in the analyzed material.

1. Ingest inbound audio continuously — Listening Head encodes raw audio to continuous embeddings (README.md:51-52).
2. Fuse optional text context — mixed text-plus-audio prompt enters the same encoder path for RAG-style conditioning (README.md:43-44).
3. Reason over embeddings/tokens — SmolLM-360m backbone preserves text-LLM reasoning without the coherence degradation attributed to speech-to-speech models (README.md:45).
4. Predict output embeddings — Speaking Head applies rectified flow matching for single-step/fast decoding (README.md:30-36, README.md:54).
5. Stream waveform — causal HiFi-GAN vocoder converts embeddings to audio with ~80ms time-to-first-audio on RTX 4090 (README.md:30-36, README.md:54-55).
6. Sustain duplex loop — keep step 1 running during steps 4–5 so interjections and backchanneling are absorbed without halting synthesis (README.md:16-17, README.md:39); emit paralinguistics (breathing, laughter, prosody) learned from data (README.md:46).

## 6. Key Files

The wiki analyzes exactly three files (README.md via 01-overview.md; `.gitignore`, `_config.yml` via 02-top-level-files.md). The table lists all three; the 10–20 file target cannot be met without inventing files, so coverage is stated as-is.

| File | Lines | What It Does |
|------|-------|--------------|
| `README.md` | cited refs :11–:77 | Sole technical source: spec table, feature list, dual-head architecture, comparison table, roadmap |
| `_config.yml` | 1–3 | Jekyll docs-site config: theme, title, description |
| `.gitignore` | 1 | Excludes `dist` build output from version control |

Structural note: no source, training, inference, config-schema, or test files are covered by the analyzed wiki pages. Any file beyond the three above is outside the evidence boundary for this summary.

## 7. Dependencies

No dependency manifest (package.json, requirements, pyproject, Gemfile) is covered by the analyzed wiki pages. Exact version-constraint strings are therefore unavailable.

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| (no manifest in evidence) | unknown | runtime/training dependencies undocumented in analyzed pages |
| `jekyll-theme-minimal` | (constraint string not cited; key `theme` at `_config.yml:1`) | Jekyll theme for the project site |
| SmolLM-360m (model, not package) | unknown | text backbone cited in spec (README.md:30-36) |
| HiFi-GAN, causal variant (model, not package) | unknown | streaming vocoder (README.md:54-55) |

Conceptual (non-package) dependencies implied by the architecture prose: rectified flow matching for embedding prediction and continuous-embedding audio encoding in place of RVQ (README.md:30, README.md:42, README.md:54). Training-data scale is cited as ~5,000 hours (README.md:60-67), but no dataset dependency is named.

## 8. CLI / Usage Surface

Entry points: none documented in the analyzed pages. No scripts, binaries, CLI flags, or Hugging Face Space URL are cited; the live demo and API client are explicitly unshipped roadmap items (README.md:70-77).

| Command | Source | Status |
|---------|--------|--------|
| (none) | — | no CLI commands in evidence |

| Env var | Required? | Purpose |
|---------|-----------|---------|
| (none) | — | no env vars in evidence |

| Config | Keys | Purpose |
|--------|------|---------|
| `_config.yml` | `theme: jekyll-theme-minimal` (`_config.yml:1`), `title: MichiAI` (`_config.yml:2`), `description` (`_config.yml:3`) | docs-site presentation only, not runtime configuration |

Effective usage surface per the wiki: read the README spec and features; configure only the Jekyll site; await the demo/API client. Runtime invocation (Python/JS API, model weights path, sample rate, prompt format) is undocumented in the analyzed material.

## 9. Extensibility Points

- Larger backbone — swap or scale the LLM behind the two heads; roadmap item "Scaling: Implementing a larger LLM backbone" (README.md:70-77). Extension file/class unknown; no code structure in evidence.
- Multilingual support — add non-English datasets; roadmap item "Multilingual Support" (README.md:70-77). Integration point (tokenizer, encoder, data loader) not specified in evidence.
- Voice behavior — new timbres/styles via zero-shot audio prompts rather than code change; input is a few-seconds audio prompt (README.md:43).
- Retrieval conditioning — RAG-style context via the mixed text+audio prompt path (README.md:43-44); no retriever interface is specified.
- Vocoder/synthesis tuning — the causal HiFi-GAN stage (README.md:54-55) is the natural swap point for latency/quality trade-offs; exact module location unknown.
- Client ecosystem — "Release API client" is an open roadmap item (README.md:70-77); the client interface does not yet exist in evidence.
- Docs site — `_config.yml:1-3` (theme, title, description) is the only concrete editable config in evidence.

## 10. Limitations and Gotchas

- **Latency figure is hardware-bound and inconsistent.** ~80ms TTFA is qualified as "tested on RTX 4090" (README.md:30-36), while the site config claims ~75ms (`_config.yml:3`). Expect different numbers on any other GPU; the 5ms discrepancy is unexplained in evidence.
- **No executable surface in evidence.** No code files, weights, CLI, API client, or demo are covered by the wiki; demo and API client are unchecked roadmap boxes (README.md:70-77). Treat all capability claims as README assertions, not verified behavior.
- **English-only and small-data training.** Multilingual support is an open item (README.md:70-77) and audio training is cited at ~5,000 hours versus 7M+ for the named rivals (README.md:60-67), so out-of-language and rare-acoustic conditions are uncharacterized.
- **Rival comparison is self-reported.** The Hertz-dev / Moshi / Qwen-Omni table (README.md:62-67) asserts the coherence and efficiency advantage without benchmarks, metrics, or evaluation harness in evidence.
- **`dist` is git-ignored, so built artifacts are invisible.** `.gitignore:1` excludes `dist`; anyone auditing the built site or bundle must rebuild locally.

## 11. How It Compares to Alternatives

All three named rivals come from the README comparison table (README.md:62-67): Hertz-dev (8.5B, 20,000,000 hours, quantized), Moshi (7B, 7,000,000 hours, quantized), Qwen-Omni (7B+, 8,000,000+ hours, quantized) versus MichiAI (530M, ~5,000 hours, continuous). A fourth reference point is the SmolLM-360m text backbone family (README.md:30-36), a small text LLM rather than a speech rival, included as lineage context.

Hertz-dev, Moshi, and Qwen-Omni represent the large quantized speech-LLM camp: 7B+ parameters and millions of audio hours with RVQ-style discretization. MichiAI positions against them as the lightweight continuous-latent alternative: two orders of magnitude fewer parameters and three orders less audio data, trading the discretization stack for flow-matched continuous embeddings plus a causal vocoder to hit streaming latency on a single high-end consumer GPU. Positioning sentence: where the incumbents buy quality with scale and quantization, MichiAI bets that continuous latents on a small backbone preserve reasoning at a fraction of the compute, with the bet still resting on README claims rather than in-evidence benchmarks or shipped code.

## Appendix: Selected Code Snippets

1. Spec table, `README.md:28-36` (via 01-overview.md:14-22):

```
| Feature | Specification |
| :--- | :--- |
| **Model Size** | 530M Parameters |
| **Latency (TTFA)** | ~80ms (tested on RTX 4090) |
| **Architecture** | Continuous Embeddings + Rectified Flow Matching |
| **Base Backbone** | SmolLM-360m |
| **Key Innovation** | No Coherence Loss / Single Step Decoding |
```

2. Rival comparison, `README.md:62-67` (via 01-overview.md:48-53):

```
| Model | Parameters | Audio Training Data | Approach |
| :--- | :--- | :--- | :--- |
| Hertz-dev | 8.5B | 20,000,000 hours | Quantized |
| Moshi | 7B | 7,000,000 hours | Quantized |
| Qwen-Omni | 7B+ | 8,000,000+ hours | Quantized |
| **MichiAI** | **530M** | **~5,000 hours** | **Continuous** |
```

3. Roadmap, `README.md:70-77` (via 01-overview.md:58-63):

```
* [x] **Core Architecture:** Continuous Embeddings + Flow Matching implementation.
* [X] **Conversational Tuning:** Training on specific dialogue datasets for better turn-taking.
* [ ] **Scaling:** Implementing a larger LLM backbone.
* [ ] **Multilingual Support:** Integrating non-English datasets.
* [ ] **Hugging Face Space:** Launching a live interactive demo.
* [ ] **Release API client** Release an API client to this repo
```

4. Site config, `_config.yml:1-3` (via 02-top-level-files.md:30-33):

```
theme: jekyll-theme-minimal
title: MichiAI
description: Full-duplex speech LLM with ~75ms latency.
```
