# Honcho: AI-Native Memory System

**Source:** [Honcho — Memory That Reasons](https://www.honcho.dev/) (Plastic Labs)
**Related:** [[../HonchoQuickstart/summary|Honcho Quickstart (docs)]]

## Human Readable TL;DR

Honcho is a paid, hosted "memory brain" you bolt onto an AI agent so it remembers people and context across conversations instead of forgetting everything between sessions. Instead of just storing a transcript, it also quietly re-reads and reasons over what it stored (they call this "dreaming") so it can answer questions like "what does this user care about?" later, cheaply and in about a fifth of a second. It's aimed at anyone building AI companions, coding assistants, game NPCs, tutors, or support bots that need to feel like they "know" the user over time.

## TL;DR

Honcho (by Plastic Labs) is a commercial memory-as-a-service layer for AI agents: it ingests conversation/session data, runs continuous background reasoning ("Dreaming") over it via proprietary "Neuromancer" models, and exposes a `context()` call (curated memory + history, unlimited/free) plus an on-demand `.chat()` reasoning call (five priced tiers). The homepage markets it as state-of-the-art on LongMem, LoCoMo, and BEAM memory benchmarks, claiming 60-90% token savings and ~200ms context retrieval, with model-agnostic support (OpenAI, Anthropic, custom) and SDKs for Python/TypeScript plus a Claude Code plugin.

---

## Problem & Motivation

Stateful AI agents (companions, coding assistants, NPCs, tutors, support bots) lose context across sessions unless developers either stuff full history into the prompt (expensive, doesn't scale) or build a bespoke memory pipeline (complex, ongoing maintenance burden). Honcho positions itself as a drop-in managed layer that both stores conversation history and continuously reasons over it, so applications get persistent, evolving understanding of each user/agent without owning the memory infrastructure.

---

## Core Product & Architecture

1. **Neuromancer** — Plastic Labs' proprietary reasoning models that sit on top of raw storage, described as enabling "learning beyond explicit facts" (i.e., inferring traits/preferences, not just retrieving stored text).

2. **Sessions & Peers** — the data model: any user, agent, NPC, or group can be modeled as a "peer" inside a "session," letting the same memory substrate represent multi-party conversations (this matches the `Peer`/`Session`/`Workspace` primitives documented in the Honcho Quickstart).

3. **Dreaming** — asynchronous, background reasoning that continuously re-processes and optimizes stored memory (consolidation/insight-generation) independent of the request path, rather than only reasoning synchronously when queried.

4. **Granular Control** — knobs for search, token budgets, summarization, and scoped perspectives, so an application can trade off cost/latency/detail per call.

5. **API surface** — automatic ingestion that triggers reasoning on every incoming message; `context()` returns curated reasoning plus raw history; `.chat()` performs on-demand reasoning at five selectable tiers (minimal → max).

---

## Key Claims & Pricing

**Benchmark claims** (as marketed, not independently verified on this page):
- State-of-the-art on LongMem, LoCoMo, and BEAM memory benchmarks
- LoCoMo: 90.4% · LongMem-S: 90.4% · BEAM 100K: 0.630
- 60–90% token savings vs. naive context-stuffing
- ~200ms context retrieval latency

**Pricing:**
| Component | Cost |
|---|---|
| Ingestion (storage + reasoning) | $2.00 / million messages |
| `context()` calls | Unlimited, no additional cost |
| `.chat()` reasoning — Minimal | $0.001 / query |
| `.chat()` reasoning — Low | $0.01 / query |
| `.chat()` reasoning — Medium | $0.05 / query |
| `.chat()` reasoning — High | $0.10 / query |
| `.chat()` reasoning — Max | $0.50 / query |

**Programs:** startups that raised <$5M get $1,000 in credits + 12 months subsidized pricing; enterprise gets custom plans with dedicated support.

**Target use cases called out:** AI companions, coding agents (learning team conventions/architecture), gaming NPC memory, adaptive education (misconception tracking), customer support (cross-channel context), and productivity tools.

**Integrations/SDKs:** `uv add honcho-ai` (Python), `npx skills add plastic-labs/honcho` (Agent Skill), a Claude Code plugin ("Claude-Honcho"), OpenClaw (WhatsApp/Telegram/Discord/Slack), and "Hermes Agent" (a reference agent with Honcho memory built in — see [[../../research_topics/agent_harness/HermesAgent/summary|Hermes Agent summary]]). Model-agnostic: works with OpenAI, Anthropic, or custom models.

---

## Suggestions & Future Directions

1. Cross-reference the benchmark numbers (LoCoMo/LongMem/BEAM) against the independent "Are We Ready For An Agent-Native Memory System?" survey ([[../AreWeReadyForAnAgentNativeMemorySystem/summary|summary]]) before taking Honcho's "SOTA" claim at face value — that paper finds no single memory architecture dominates across workloads.
2. For hands-on evaluation, start from the existing [[../HonchoQuickstart/summary|Honcho Quickstart]] notes (Python/TypeScript setup already captured) rather than re-deriving API basics from the marketing page.
3. Worth checking `evals.honcho.dev` directly for the underlying benchmark methodology, since the homepage only surfaces headline scores.
4. Pricing is per-reasoning-operation, not per-token — worth modeling cost against a real workload's message volume + `.chat()` tier mix before committing.

---

## Resources
- Docs: honcho.dev/docs
- GitHub: github.com/plastic-labs/honcho
- Benchmarks: evals.honcho.dev
- Discord: discord.gg/honcho
- App/signup: app.honcho.dev · Chat demo: honcho.chat
