# Qwen3.5-Omni Technical Report

**Paper:** [Qwen3.5-Omni Technical Report (Qwen Team, 2026)](https://arxiv.org/abs/2604.15804)

## Human Readable TL;DR

Imagine a personal assistant that can watch a video, listen to you talking, read text you wrote, think about all of that together, and then answer you out loud in any of dozens of languages — and if it needs help, it can search the web or run a tool on its own without being told to. Qwen3.5-Omni is a single AI model that does all of this at once, in real time, instead of stitching together separate systems for each sense. It splits itself into two cooperating brains: one that "thinks" across all inputs, and one that "talks" back with natural speech. The result is an AI that feels less like a chatbot and more like a coworker who can see, hear, speak, and act.

## TL;DR

Qwen3.5-Omni is a fully omnimodal large language model with a Thinker-Talker architecture that jointly processes text, images, audio, and video, and generates both text and streaming speech. It introduces a Hybrid-Attention Mixture-of-Experts design, a 256k-token context window, multi-codebook RVQ speech codec, and a new Adaptive Rate Interleave Alignment (ARIA) mechanism that unifies text and speech generation into one stable streaming channel. The Plus variant achieves state-of-the-art on 215 audio and audio-visual subtasks, surpassing Gemini-3.1 Pro on most audio benchmarks while matching Qwen3.5-Plus-Instruct on text-only tasks. It further demonstrates agentic behavior (autonomous WebSearch/FunctionCall), zero-shot multilingual voice cloning across 29 languages, and an emergent "Audio-Visual Vibe Coding" capability where executable code is generated directly from audio-visual instructions.

---

## Problem & Motivation

Existing omnimodal models still operate in a passive perception-response paradigm — they describe what they see or hear but do not act. They struggle with scalable agentic behavior, real-time interaction, autonomous tool use, and cross-modal reasoning over long inputs. Streaming speech synthesis in particular suffers from instability (skipped words, bad pronunciation, ambiguous numbers) caused by encoding-rate mismatches between text and speech tokenizers. Integrating vision, audio, text, and action into one coherent real-time system — without sacrificing unimodal performance — is the central challenge this paper tackles.

---

## Main Original Ideas

1. **Hybrid-Attention Mixture-of-Experts (MoE)** — Both Thinker and Talker use a Hybrid MoE framework combined with a Gated Delta Net (GDN) module that reduces KV-cache I/O overhead for long-sequence inference, balancing capacity and efficiency across modalities.
2. **Adaptive Rate Interleave Alignment (ARIA)** — A new streaming-decoding mechanism that unifies the conventional dual-channel text+speech generation into a single-channel interleaved formulation under a monotonic adaptive-rate constraint, fixing the prosody instability caused by tokenizer-rate mismatches.
3. **Multi-Codebook RVQ Codec with Single-Frame Speech Generation** — The Talker predicts Residual Vector Quantization tokens via a lightweight multi-token-prediction (MTP) head, and a causal ConvNet reconstructs waveforms frame by frame, enabling immediate streaming synthesis.
4. **AuT (Audio Transformer) Trained From Scratch on 40M Hours** — A transformer audio encoder with dynamic attention window sizing operating at 6.25 Hz over 128-channel mel-spectrograms, jointly optimized for real-time and offline audio tasks with heavy multilingual coverage.
5. **Audio-Visual Timestamp Interleaving** — Explicit textual timestamps (in seconds) are inserted into audio-visual patches instead of using absolute position IDs, giving contiguous cross-modal temporal alignment that scales to 10 hours of audio or 400 seconds of 720p video at 1 FPS within a 256k context.
6. **Three-Stage Thinker + Four-Stage Talker Post-Training** — Includes Specialist Distillation, On-Policy Distillation (text-conditioned responses distilled into audio-conditioned queries to close the modality gap), and Interaction-Aligned RL for multi-turn persona and code-switching stability; Talker adds DPO with rule-based rewards and GSPO plus speaker fine-tuning.
7. **Native Omni-Agent Behavior** — Autonomous invocation of WebSearch and FunctionCall directly from multimodal inputs, without external orchestration.
8. **Emergent "Audio-Visual Vibe Coding"** — Generates executable code directly from spoken or visual instructions, an unprogrammed capability that emerged from joint omnimodal training.

---

## Key Findings

**Speech recognition and translation (lower is better, WER %):**

| Benchmark | Qwen3.5-Omni-Plus | Gemini-3.1 Pro | GPT-4o-Transcribe |
|---|---|---|---|
| Fleurs avg | **6.6** | 7.3 | 10.4 |

**Zero-shot TTS on SEED-TTS (WER %):**

| Language | Qwen3.5-Omni-Plus |
|---|---|
| Chinese | **0.99** |
| English | **1.26** |

**Cross-lingual speech generation (error rate):**

| Direction | Qwen3.5-Omni | CosyVoice3 |
|---|---|---|
| zh → ko | **4.03** | 14.4 |

Additional qualitative findings:

- **SOTA on 215** audio and audio-visual subtasks; beats Gemini-3.1 Pro on audio understanding, reasoning, recognition, translation, and dialogue; comparable on audio-visual understanding.
- **Unimodal parity preserved** — text performance matches Qwen3.5-Plus-Instruct on MMLU-Pro, C-Eval, IFEval, GPQA, LiveCodeBench v6, BFCL-V4, TAU2Bench; instruction-following is slightly better thanks to OPD and interaction-aligned RL.
- **Video understanding improves** over the text-only counterpart on Video-MME, MLVU, MVBench, LVBench, MMVU, MME-VideoOCR — evidence that joint video-audio training helps vision.
- **Multilingual TTS** — best WER in 22 of 29 languages vs MiniMax-Speech and ElevenLabs; best cross-lingual mixed error rate in 10 of 12 pairs.
- **Streaming latency** — 235 ms first-packet latency for Flash audio input; stable throughput under increased concurrency.
- **Tool use** — 57.2% on OmniGAIA; substantial outperformance of Gemini-3.1 Pro on Qualcomm IVD audio-query QA.
- **Vocabulary upgrade** — 250k BPE tokenizer improves encode/decode efficiency 10–60% across languages.

---

## Suggestions & Future Directions

1. **Extend agentic scope** — expand autonomous tool ecosystems beyond WebSearch and FunctionCall toward more complex multi-tool orchestration.
2. **Push real-time interaction** — continue reducing first-packet and steady-state latency to support more natural conversational pacing and interruption handling.
3. **Broaden speech-generation language coverage** — current synthesis covers 29–36 languages while recognition covers 113; close that gap.
4. **Explore emergent capabilities further** — study Audio-Visual Vibe Coding and other unprogrammed behaviors as a foundation for intuitive multimodal programming interfaces.
5. **Scale context and efficiency jointly** — continue optimizing Hybrid MoE + GDN for longer contexts and higher concurrency serving.
6. **Deeper cross-modal reasoning** — advance from perception-plus-action toward long-horizon multimodal reasoning over hours-long audio and video.

---

## Authors & Institutions

Qwen Team. Specific institutional affiliation beyond "Qwen Team" is not stated in the technical report.
