---
type: Video
title: Sebastian Raschka on Kimi K3, GLM-5.2, DeepSeek V4 and the Open-Weight AI Explosion
description: Sebastian Raschka and Hugo Bowne-Anderson trace three months of open-weight LLM progress (DeepSeek V4, GLM-5.2, Qwen 3.5/3.6, Kimi K3) through architecture (latent MoE, hybrid attention, residual tricks), the shrinking frontier gap, model-harness coupling, local inference tradeoffs, and inference-time effort routing.
generated: { by: claude/claude-sonnet-5, at: 2026-08-03T14:30:00Z }
sources:
  - id: original
    resource: https://www.youtube.com/watch?v=pEf21w0r-vY
  - id: local-copy
    resource: source/transcript.md
tags: [llm-architecture, open-weight-models, mixture-of-experts, agent-harness, inference]
---

# Sebastian Raschka on Kimi K3, GLM-5.2, DeepSeek V4 and the Open-Weight AI Explosion

A Vanishing Gradients podcast interview (host Hugo Bowne-Anderson, guest Sebastian Raschka) recorded the day Kimi K3's weights were released, using that live moment to review roughly three months of open-weight LLM progress. The central claim: open-weight models are closing the gap with proprietary frontier models faster than ever, less through fundamentally new training math than through targeted architecture tweaks (latent MoE, hybrid/linear attention, extra residual paths), product-layer polish, and how tightly models are now trained inside their own coding-agent harnesses. Worth ingesting for its live, blow-by-blow architectural read of Kimi K3 and for Raschka's recurring "understand it as a timeline, one component at a time" framing, which is a genuinely useful mental model for keeping up with a fast-moving field without chasing every release.

## Read This Folder

- [[summary|Summary]] — technical summary (start here for a refresher)
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-kimi-k3-architecture\|Kimi K3's Architecture]] | Kimi Linear scaled up, latent MoE (Nemotron 3 Ultra analogy), residual attention, growing implementation complexity |
| [[wiki/02-architecture-innovations-hybrid-attention\|Hybrid Attention and Targeted Architecture Innovations]] | Gated DeltaNet / Kimi Delta Attention / Mamba-2, DeepSeek V4 highway connections, looped transformers |
| [[wiki/03-open-weight-vs-frontier-gap\|The Shrinking Open-Weight vs. Frontier Gap]] | Compressed release cadence, product- vs. training-layer gains, multimodal affordances (GLM-5.2, Kimi K3) |
| [[wiki/04-harness-model-coupling-and-overfitting\|Harness-Model Coupling and the Overfitting Question]] | Native-harness advantage, RLVR-on-own-harness hypothesis, Claude Code token-usage anecdote |
| [[wiki/05-local-and-self-hosted-inference\|Local and Self-Hosted Inference: Hardware and Tradeoffs]] | DGX Spark vs. Mac M4/M5, self-hosting challenges, OpenRouter as a middle ground |
| [[wiki/06-inference-time-effort-levels-and-routing\|Inference-Time Effort Levels and the Case for Automatic Routing]] | Size/effort "two levers," Kimi K3 budget-token RLVR penalty, harness-should-decide argument |
| [[wiki/07-pretraining-post-training-trends\|Pre-Training and Post-Training Trends]] | Training transparency limits, synthetic data, ~30T-token datasets, multi-stage SFT/RLVR pipelines, the "1+1" efficiency probe |
| [[wiki/08-outlook-building-blocks-and-next-book\|Outlook: Building Blocks, Career Advice, and What's Next]] | Book progression (LLM → reasoning model → likely agent-harness book), "marathon not a sprint" advice |

## Original Source

- [source/transcript.md](source/transcript.md) — full timestamped transcript, retrieved 2026-08-03

_Note: diagrams Raschka shared live on screen (his architecture-comparison gallery) were referenced verbally in the conversation but not captured as images in this ingestion — no screenshot/browser tool was used. Where a wiki page describes a diagram, it does so in words rather than citing an unavailable figure._
