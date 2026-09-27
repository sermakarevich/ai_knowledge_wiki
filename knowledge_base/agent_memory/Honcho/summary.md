# Honcho: Memory That Reasons (Plastic Labs)

**Article:** [Honcho — Memory That Reasons](https://honcho.dev/) — Plastic Labs docs + site, 2026-09-10

## Human Readable TL;DR

Imagine a notebook that does not just copy what you say, but thinks about what it means. Every chat, email, or note you give it is turned into clear lessons about who you are. Those lessons grow over time, so the notebook remembers how you change. Later, when you ask a question, it answers from those lessons instead of re-reading a huge pile of old messages. That is what Honcho does for computer programs that talk to people.

## TL;DR

Honcho is a continual-learning memory layer for LLM agents. Incoming messages are processed by Neuromancer, a family of small custom formal-logic reasoning models. The pipeline has three parts: an async Deriver for per-message conclusions, a periodic Dreamer for consolidation, and a query-time Dialectic agent for answers. What is stored is a peer representation: logic conclusions plus session summaries plus a peer card. Vendor-reported scores are state of the art: LongMemEval-S 90.4%, LoCoMo 89.9%, BEAM around 0.63 at 100K scale. Vendor-reported pricing is $2 per million input tokens for ingest and $0.001 to $0.50 per query by reasoning level, with storage and context reads free.

---

## Problem & Motivation

Most AI chat programs forget everything between sessions, or remember only in a shallow way. Old approaches leave three gaps. First, RAG only finds what was said word for word: it misses hidden meaning, breaks when facts change (a user moving from Paris to Rome), and at large scale forces huge raw histories into the prompt, which is slow and costly. Second, store-and-retrieve tools in the mem0 style save isolated facts and return raw matches, so the app developer must assemble context by hand, contradictions are left to app code, and you pay a fee each time you search your own saved data. Third, DIY Postgres-plus-pgvector setups keep full control and data ownership, but every quality fix is your own work — chunking, embeddings, summaries, contradiction handling, evals — the "RAG treadmill" where every improvement costs engineering time. Honcho answers with reasoning-first memory: reason over everything when it arrives, so the useful conclusion is already there when it is needed. Messages save fast to PostgreSQL in about 200 milliseconds vendor-reported while Neuromancer reasons in the background without blocking the reply, and queries then read back small token-efficient conclusions, with vendor-reported 60–90% token savings.

---

## Main Original Ideas

1. **Reasoning-first memory instead of retrieval-first** — Traditional systems store text and search it later. Honcho runs Neuromancer reasoning on every message at write time, so explicit facts, logical follow-ons, patterns, and best guesses are already computed before any question is asked. This shifts cost from query-time stuffing to write-time thinking.
2. **Neuromancer, a dedicated reasoning-model family** — Trained for logical rigor, structured output, and efficiency. The first member, Neuromancer XR, is a fine-tune of Qwen3-8B for explicit plus deductive extraction, vendor-reported to beat frontier models on that step while running cheaper and faster. Its outputs feed consolidation, peer cards, induction, and abduction, with later members planned for the deeper induction and abduction steps.
3. **Peer-centric data model: Workspace, Peer, Session, Message** — A Workspace is the top isolated area (one per customer, or dev/staging/prod); a Peer is any lasting entity — user, agent, group, project, idea — with one ID per Workspace; a Session is one interaction thread; a Message is one time-ordered unit tied to one peer. Learning attaches to peers, so what is learned in one session helps in another, and settings cascade Workspace → Peer → Session so defaults can be overridden where needed.
4. **Representations made of conclusions, summaries, and peer cards** — Conclusions come in four logic types: explicit (directly stated), deductive (must follow from premises), inductive (patterns across at least two supporting conclusions, with confidence), and abductive (simplest likely explanation). Short summaries build about every 20 messages and long ones about every 60 (vendor-reported defaults), peer cards cache basic life facts like name and occupation so simple grounding is never lost, and all three artifacts refine as each new message arrives.
5. **Async Deriver plus periodic Dreamer plus query-time Dialectic** — The Deriver runs Neuromancer XR per message in chronological order per peer, keeping order through per-peer queues. The Dreamer is periodic consolidation (vendor-marked experimental): a deduction specialist for updates, missed implications, contradiction fixes, and peer-card updates, then an induction specialist for habits and traits, gated by vendor-reported thresholds of 50+ new conclusions, 8-hour cooldown, 60-minute idle wait (manual `schedule_dream` bypasses thresholds). The Dialectic is the query agent behind `peer.chat()` and `honcho.chat()`, prefetching relevant conclusions and synthesizing cited answers instead of returning raw matches.
6. **Token-budget context() with ready converters** — The `session.context()` call returns ready history blending summary plus recent messages, capped by a token budget such as 1500 or 2000 (about 40% summary, 60% recent messages vendor-reported when capped). Options include peer targeting, semantic search filtering, session-only recall, and named scopes; `to_openai()` / `to_anthropic()` converters make output directly ready for provider chat APIs.
7. **Pair-scoped perspectives with observe_me and observe_others** — Each observer-and-observed peer pair gets its own vector collection. Observe_me builds Honcho's own view from all of a peer's messages (on by default); observe_others lets one peer view another using only shared sessions, so simulated viewpoints stay true and never become all-knowing. Named scopes further bound recall to chosen sessions (work vs personal), and API keys scope as admin, workspace, peer, or session.

---

## Key Findings

All accuracy numbers below are vendor-reported from the Honcho docs and site, retrieved 2026-09-10. Independent replication is still pending, and judge choice alone can move scores 15–25 points.

| Benchmark | Honcho vendor-reported | Baseline for context |
|---|---|---|
| LongMemEval-S overall, 500 chats of ~115K tokens | 90.4% | 62.6% Claude Haiku 4.5 no-memory baseline vendor-reported (+27.8 points) |
| LongMemEval-S single-session preference | 90.0% | 23.3% baseline vendor-reported |
| LongMemEval-S multi-session reasoning | 85.0% | 46.6% baseline vendor-reported |
| LoCoMo overall, long-conversation QA | 89.9% | See XR ablation and third-party rows below |
| LoCoMo XR ablation, conclusion model only, final writer fixed as Claude 4 Sonnet | 86.9% Neuromancer XR | 80.0% Claude 4 Sonnet, 69.6% Qwen3-8B base, all vendor-reported |
| BEAM-100K scale | 0.630 | LIGHT baseline much lower; outside systems 0.55–0.73 in third-party repeats |
| BEAM-500K scale | 0.646 | Same test family, larger input |
| BEAM-1M scale | 0.618 | LIGHT near 0.34 in third-party repeat |
| BEAM-10M scale | 0.409 | Score drops as input grows to 10M tokens |

Qualitative findings from the wiki pages:

- Mem0 migration path is documented: import raw messages for best quality with full order, speaker labels, summaries, and deductive depth, or import existing memories as conclusions for a fast start without re-reasoning.
- API mapping covers init, peer identity, add, search, list, update, and delete, plus Honcho-only calls: `session.context()`, `peer.chat()`, `honcho.chat()`, peer cards, session summaries, and observation settings.
- Integrations are broad: SDKs via pip/uv (Python) and npm/yarn/pnpm (TypeScript), an MCP server plus skills, plugins for Claude Code, Codex, Cursor, OpenCode, OpenClaw, SillyTavern and others, and frameworks such as LangGraph, CrewAI, Vercel AI SDK, and n8n.
- File uploads (PDF, TXT, JSON) become messages, with streaming, structured outputs, queue-status checks, and webhooks.
- Open core is AGPL-licensed and self-hostable with Docker via `honcho start --setup` plus your own LLM provider key, for VPC or data-residency needs.
- Pricing model is storage plus retrieval free, pay for reasoning: $2.00 per million tokens covering Neuromancer work, context reads $0 unlimited, reasoning queries from $0.001 (minimal) to $0.50 (max, async), all vendor-reported. New accounts get $100 free credits vendor-reported, the quickstart costs about $0.04, and batch uploads allow up to 100 messages per call.
- Caveats are stated in the wiki: LLM-as-judge grading is unstable, vendors pick favorable baselines, and the open harness at github.com/plastic-labs/honcho-benchmarks is provenance, not proof.

---

## Suggestions & Future Directions

1. **Independent replication on all three suites** — Re-run LongMemEval-S, LoCoMo, and BEAM with fixed judges, open prompts, and matched baselines including full-context and mem0-style systems. Report accuracy plus cost, speed, and tokens together, not accuracy alone.
2. **Deepen and test inductive and abductive conclusions** — Measure when cross-conclusion patterns and best-guess explanations help versus hallucinate. Include confidence calibration and contradiction survival over long update chains, with Neuromancer coverage beyond explicit and deductive steps.
3. **Extend modalities beyond chat text** — Bring emails, documents, voice transcripts, images, and user actions into the same Neuromancer pipeline. Keep the same Deriver, Dreamer, and Dialectic guarantees for ordering, consolidation, and attribution.
4. **Validate cost at scale with unit economics** — Publish per-user monthly cost curves for realistic message and query mixes across minimal through max tiers. Confirm the 60–90% token-saving claim against raw-context baselines, including dreaming and high-tier query overhead.
5. **Mature dreaming heuristics and controls** — Tune the 50-conclusion, 8-hour, 60-minute-idle thresholds per workload. Expose per-peer schedules and audit views showing which conclusions were merged, deleted, or promoted during each Dreamer cycle.

---

## Authors & Institutions

Plastic Labs, an engineering-driven AI lab working across ML and cognitive science. There are no single paper authors — the source is the Honcho docs and site, retrieved 2026-09-10. Supporting material includes the Neuromancer XR blog and the open benchmark harness. Neuromancer, Deriver, Dreamer, and Dialectic designs all come from that vendor source, so all state-of-the-art claims above should be read as vendor-reported until independently repeated.
