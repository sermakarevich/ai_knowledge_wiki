# Sakana Fugu: Multi-Agent System as a Model

**Source:** [Sakana Fugu](https://sakana.ai/fugu/) (Sakana AI, 2025)

## Human Readable TL;DR

Imagine instead of asking one expert a question, you had a team of specialists who automatically divide the work, check each other's answers, and give you a final result -- without you having to manage any of them. Sakana Fugu does this with AI: it looks like a single AI to your app, but behind the scenes it coordinates multiple specialized AI models working together. The result beats any single AI on hard tasks like coding or research, without you changing how you call the API.

## TL;DR

Sakana Fugu is a multi-agent orchestration layer exposed as a single OpenAI-compatible API. Backed by two ICLR 2026 papers (TRINITY and Conductor), it dynamically routes tasks across specialized LLM roles (Thinker, Worker, Verifier) and uses RL-trained coordination strategies. Both Fugu and Fugu Ultra variants benchmark at or above frontier models (Fable 5 / Mythos Preview) on coding, reasoning, and science benchmarks.

---

## Problem & Motivation

Single LLMs hit a ceiling on multi-step, complex tasks -- no one model excels at planning, execution, and verification simultaneously. Integrating multiple models requires custom orchestration logic that is expensive to build and brittle to maintain. Fugu solves both: it provides multi-agent coordination internally while presenting a unified, drop-in OpenAI-compatible API to the caller.

---

## Main Original Ideas

1. **TRINITY architecture** -- Evolved lightweight coordinator assigns three roles to distinct LLMs: Thinker (reasoning/planning), Worker (execution), and Verifier (quality check). Roles interact over multiple turns, enabling self-correction that single-pass models lack.

2. **Conductor (RL-trained coordinator)** -- A coordinator trained via reinforcement learning to discover natural-language coordination strategies. Outperforms individual models on challenging reasoning benchmarks without requiring human-designed protocols.

3. **Unified OpenAI-compatible API** -- All multi-agent complexity is hidden behind a standard chat-completions interface. Automatic model selection and switching; single blended pricing with no fee stacking when multiple agents coordinate.

4. **Provider/model exclusion controls** -- Users can exclude specific models or providers to satisfy data privacy, compliance, or organizational requirements -- enabling enterprise adoption without giving up orchestration benefits.

---

## Key Findings

| Benchmark | Fugu | Fugu Ultra |
|---|---|---|
| SWE Bench Pro | 59.0 | 73.7 |
| LiveCodeBench | 92.9 | 93.2 |
| Humanity's Last Exam | 47.2 | 50.0 |
| GPQA-D | 95.5 | 95.5 |

- Both variants perform "shoulder-to-shoulder with Fable 5 and Mythos Preview" per Sakana's claims
- No export control restrictions (relevant for non-US enterprises constrained by frontier model access)
- Real-world results reported by users: code review finding 20+ issues vs 3 per competing tools; patent landscape analysis in hours vs 3--4 days; 100× speedup on specific CUDA tasks during paper reproduction

---

## Suggestions & Future Directions

- EU/EEA availability pending GDPR compliance (not yet available)
- Deeper agent pools accessible through Fugu Ultra tier suggest continued scaling of coordination width
- RL-based coordination discovery (Conductor) leaves open further reward shaping for domain-specific tasks

---

## Product Details

**Two variants:**
- **Fugu** -- balanced performance/latency for everyday work
- **Fugu Ultra** -- maximum quality, deeper agent pools

**Pricing:**
- Subscriptions: $20 / $100 / $200 per month
- Pay-as-you-go: Fugu Ultra at $5 input / $30 output per 1M tokens (higher rates for contexts >272K)

**Research basis:** TRINITY and Conductor, both published at ICLR 2026

---

## Authors & Institutions

Sakana AI
