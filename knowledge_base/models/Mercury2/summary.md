# Introducing Mercury 2

**Article:** [Introducing Mercury 2 (Inception, Stefano Ermon, 2026)](https://www.inceptionlabs.ai/blog/introducing-mercury-2)

## Human Readable TL;DR

Most AI chatbots write answers one word at a time, like a person typing a sentence letter by letter. Mercury 2 instead sketches a rough draft of the whole answer at once, then quickly polishes it -- like a artist blocking in a whole painting before refining details, rather than drawing one brushstroke at a time. That trick lets it "type" over 1,000 words a second while still reasoning carefully, which matters for anything needing fast back-and-forth: chat, live transcription, autocomplete, or an AI agent that has to think many times in a row.

## TL;DR

Inception announced Mercury 2, a diffusion-based (non-autoregressive) language model that generates text via parallel iterative refinement instead of sequential token-by-token decoding. It reaches 1,009 tokens/second on NVIDIA Blackwell GPUs -- over 5x faster than conventional autoregressive models at comparable quality -- while supporting a 128K context window, tunable reasoning, native tool use, and schema-aligned JSON output. It is priced at $0.25/1M input and $0.75/1M output tokens, OpenAI-API-compatible, and available immediately via API and chat interface.

---

## Problem & Motivation

Autoregressive LLMs generate one token at a time, so latency scales with output length and compounds badly in multi-step production settings (agent loops, multi-hop RAG, voice turns) where many inference calls chain together. Inception's premise is that production AI is bottlenecked by this per-call latency, forcing a tradeoff between reasoning depth/quality and responsiveness. Mercury 2 targets removing that tradeoff -- "reasoning-grade quality inside real-time latency budgets."

---

## Main Original Ideas

1. **Diffusion-based parallel decoding.** Rather than predicting tokens left-to-right, Mercury 2 generates output via parallel refinement steps that converge on a full response in a small number of denoising iterations, rather than one forward pass per token.
2. **Decoupling reasoning quality from latency.** The architecture is positioned to let the model "think" (tunable reasoning) without paying the usual linear latency cost of longer autoregressive chains-of-thought.
3. **Drop-in production compatibility.** OpenAI API compatibility plus native tool use and schema-aligned JSON output means the speed gain requires no application-level redesign for teams already targeting the OpenAI API shape.

---

## Key Findings

| Metric | Value |
|---|---|
| Generation speed | 1,009 tokens/second (NVIDIA Blackwell GPUs) |
| Speed vs. conventional autoregressive models | >5x faster |
| Context window | 128K tokens |
| Input price | $0.25 / 1M tokens |
| Output price | $0.75 / 1M tokens |

- Quality is claimed "competitive with leading speed-optimized models" (no head-to-head benchmark table published in the announcement).
- Customer testimonials cited report roughly "at least twice" the speed of competing solutions in their own deployments.
- Positioned use cases: real-time code autocomplete/refactoring, agentic multi-step workflows, voice interfaces, and multi-hop search/RAG.

---

## Suggestions & Future Directions

The post does not enumerate explicit limitations, benchmarks methodology, or a research roadmap -- it is a product-launch announcement, not a technical paper. Open questions left unaddressed: which benchmark suite backs the "competitive quality" claim, model size/parameter count, and training data/recipe details.

---

## Authors & Institutions

Stefano Ermon, CEO, Inception (Inception Labs).
