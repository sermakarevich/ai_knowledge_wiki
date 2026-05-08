# Qwen3.6-35B-A3B: Agentic Coding Power, Now Open to All

**Blog post:** [Qwen3.6-35B-A3B: Agentic Coding Power, Now Open to All (Qwen Team, Alibaba, 2026)](https://qwen.ai/blog?id=qwen3.6-35b-a3b)
**Model:** [Qwen/Qwen3.6-35B-A3B on Hugging Face](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)

## Human Readable TL;DR

Imagine a very large library of knowledge (35 billion "books"), but instead of reading all of them for every question, a smart librarian only picks the 3 most relevant ones each time -- giving you expert-level answers at a fraction of the effort. That's Qwen3.6-35B-A3B: a model as capable as a giant AI, but fast and efficient enough to run on a single high-end laptop or gaming PC. It's particularly good at writing and fixing code -- even complex, multi-file software projects -- and it can see images and videos too. Alibaba released it for free under an open license, so anyone can download and run it locally.

## TL;DR

Qwen3.6-35B-A3B is an open-weight sparse Mixture-of-Experts (MoE) multimodal language model with 35B total parameters but only 3B active per forward pass. It introduces a novel hybrid architecture combining Gated DeltaNet (linear attention) layers and Gated Attention layers interleaved with MoE FFN blocks, trained with Multi-Token Prediction (MTP). The model achieves state-of-the-art open-weight performance on agentic coding (73.4% SWE-bench Verified), supports 262K native context (1M+ via YaRN), and runs efficiently on consumer hardware.

---

## Problem & Motivation

Frontier coding and agentic AI capabilities have been largely locked behind proprietary, cloud-only APIs. Existing open-weight models either require enormous compute to run locally (dense 70B+) or sacrifice quality when shrunk to affordable sizes. The challenge is delivering frontier-level agentic coding, tool use, and multimodal understanding at a compute budget accessible to individuals and small teams -- i.e., models that run on a single RTX 4090 or Apple Silicon laptop.

---

## Main Original Ideas

1. **Sparse MoE with extreme activation ratio** -- 35B total parameters but only 3B active per token (12:1 sparsity). Uses 256 experts with 8 routed + 1 shared expert activated per token, with an expert intermediate dimension of 512. This delivers the representational capacity of a 35B dense model at the compute cost of a 3B model.

2. **Gated DeltaNet hybrid architecture** -- Instead of pure Transformer attention, Qwen3.6 uses a novel hybrid layer pattern: for every 4 layers, 3 use Gated DeltaNet (a hardware-efficient linear attention mechanism with 32 value heads and 16 QK heads) and 1 uses standard Gated Attention (16Q/2KV heads). Both layer types are paired with MoE FFN blocks. This is a significant architectural departure from standard Transformers.

3. **Thinking Preservation across conversation turns** -- The model supports retaining the chain-of-thought reasoning tokens (`<think>...</think>`) from historical messages in the context, enabling downstream turns to build on previous reasoning steps rather than discarding them. This is configurable via `preserve_thinking` in the chat template.

4. **Switchable thinking/non-thinking modes** -- The same model weights support two inference modes: a deep chain-of-thought "thinking" mode for hard reasoning and a fast "non-thinking" instruct mode for latency-sensitive tasks. Thinking can be disabled per-request via `enable_thinking: false`.

5. **Multi-Token Prediction (MTP) training** -- The model is trained with MTP, which predicts multiple future tokens simultaneously during training. This improves both training efficiency and final model quality, especially for code generation.

6. **Native MCP tool integration** -- Built-in first-class support for Model Context Protocol (MCP) tool calling. MCPMark benchmark score of 37.0 (vs. 18.1 for Gemma 4-31B), more than doubling nearest open-weight competitor.

---

## Key Findings

### Coding & Agentic Benchmarks

| Benchmark | Qwen3.6-35B-A3B | Gemma 4-31B | Notes |
|-----------|-----------------|-------------|-------|
| SWE-bench Verified | **73.4%** | 52.0% | Internal scaffold; non-standard |
| SWE-bench Multilingual | **67.2%** | -- | |
| SWE-bench Pro | **49.5%** | -- | |
| Terminal-Bench 2.0 | **51.5%** | 42.9% | |
| MCPMark (tool use) | **37.0** | 18.1 | 2x advantage |
| QwenWebBench | **1,397 ELO** | 978 (prev gen) | +43% over prior Qwen |
| LiveCodeBench v6 | **80.4%** | -- | |

### Reasoning & Knowledge Benchmarks

| Benchmark | Score |
|-----------|-------|
| MMLU-Pro | 85.2% |
| MMLU-Redux | 93.3% |
| GPQA | 86.0% |
| SuperGPQA | 64.7% |
| AIME26 | **92.7%** |

### Vision-Language Benchmarks

| Benchmark | Score |
|-----------|-------|
| MMMU | 81.7% |
| MMMU-Pro | 75.3% |
| MathVista (mini) | 86.4% |
| RealWorldQA | 85.3% |
| MMBench-EN-DEV v1.1 | 92.8% |
| VideoMME (w/ subtitles) | 86.6% |
| VideoMMMU | 83.7% |
| OmniDocBench 1.5 | 89.9% |

### Inference Performance on Consumer Hardware

| Hardware | Throughput | Quantization |
|----------|-----------|-------------|
| RTX 4090 (24GB) | 120+ tok/s | BF16 / int8 |
| Apple Silicon 64GB M4/M5 | 35--50 tok/s | Q4_K_S GGUF |

- SWE-bench was measured with Alibaba's internal agent scaffold -- not directly comparable to standard leaderboard runs.
- Vision and RealWorldQA results are self-reported; independent validation is pending.

---

## Suggestions & Future Directions

1. **Standardized agentic evaluation** -- The non-standard scaffold used for SWE-bench makes direct comparison difficult; the community needs agreed-upon agentic scaffolds.
2. **Third-party vision benchmark validation** -- Self-reported multimodal results (especially RealWorldQA 85.3%) require independent confirmation.
3. **Longer video understanding** -- YaRN scaling to 1M tokens opens door to hour-scale video processing; further work on video-specific training is suggested.
4. **Smaller MoE variants** -- The "A3B" active-parameter point is validated; future work may explore further efficiency points (A1B, A7B) along the sparsity-quality curve.
5. **Extended MCP ecosystem** -- First-class MCP support is a differentiator; growing the tool ecosystem around this integration is an explicit direction.

---

## Authors & Institutions

Qwen Team, Alibaba Group. Released April 16, 2026. License: Apache 2.0.

**Resources:** [GitHub](https://github.com/QwenLM/Qwen3.6) | [Hugging Face](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | [LM Studio](https://lmstudio.ai/models/qwen/qwen3.6-35b-a3b)
