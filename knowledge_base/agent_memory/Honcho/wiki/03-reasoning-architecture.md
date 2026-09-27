> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Reasoning Architecture: Neuromancer, Deriver, Dreamer, Dialectic

**In one sentence:** Honcho treats memory as reasoning, using the Neuromancer model family to turn messages into formal-logic conclusions in the background and a query agent to assemble answers on demand.

## Key points

- Neuromancer is Honcho's family of small custom reasoning models, where Neuromancer XR is a fine-tune of Qwen3-8B that extracts explicit statements and deductive conclusions (vendor-reported to beat frontier models on this task while running cheaper and faster).
- The Deriver is the per-message background worker that runs Neuromancer over each new message to produce explicit and deductive conclusions, keeping chronological order per peer through session queues.
- The Dreamer is the periodic consolidation worker that revisits stored conclusions with a deduction specialist for updates and contradictions and an induction specialist for patterns, and it only runs when all schedule conditions are met.
- Dreamer scheduling is vendor-reported as: at least 50 new conclusions since the last dream, at least 8 hours cooldown since the last dream, plus a 60-minute idle timer that resets if new messages arrive.
- The Dialectic is the query-time agent that answers peer.chat() and honcho.chat() requests by prefetching relevant conclusions and synthesizing a response, rather than returning raw matches.
- Query reasoning levels control cost and depth from minimal ($0.001 per query, single semantic search) through low ($0.01, default), medium ($0.05), high ($0.10, async (asynchronous, runs in background)), to max ($0.50, async research-grade).
- Storage and retrieval with context() is vendor-reported as free and unlimited, so users pay for ingestion reasoning at $2.00 per million tokens and for Dialectic queries, not for keeping data.

---

## Why reasoning instead of storage

Traditional RAG (Retrieval-Augmented Generation, a method that chunks text, embeds it, and returns the closest matches) only returns what was explicitly said. Other systems store pre-chosen facts or fixed knowledge graphs. The problem is that both miss hidden meaning, handle contradictions poorly, and leave the app developer to assemble context by hand.

Honcho takes the opposite approach: reason over everything when it arrives, so the useful conclusion is already there when it is needed. Messages are stored immediately in PostgreSQL (a widely used open-source database), a reasoning task is enqueued, and the API (Application Programming Interface, the way code talks to Honcho) returns fast. The heavy thinking happens asynchronously, meaning in the background without blocking the reply.

## Formal logic framework

Honcho structures memory with four kinds of conclusions:

- **Explicit:** what was directly stated, used as premises for the rest.
- **Deductive:** conclusions that must follow from the premises.
- **Inductive:** patterns across multiple conclusions, requiring at least two supporting conclusions, each with a confidence level.
- **Abductive:** the simplest likely explanation for observed behavior.

LLM (Large Language Model, the AI model type behind this reasoning) outputs are stored in a consistent JSON (JavaScript Object Notation, a standard text format for structured data) shape with premises linked to conclusions. The source docs give this schema for the explicit plus deductive foundation:

```json
{
    "explicit": [
        {
            "content": "premise 1"
        },
        ...
        {
            "content": "premise n"
        }
    ],
    "deductive": [
        {
            "premises": [
                "premise 1",
                ...
                "premise n"
            ],
            "conclusion": "conclusion 1"
        },
        ...
    ]
}
```

Peer cards (short biographical facts such as name, occupation, and interests) and session summaries are built on top of the same foundation.

## Neuromancer model family

Neuromancer is the name for Honcho's custom small models for formal-logic reasoning. The vendor says off-the-shelf LLMs can do logic but are not tuned for it, so Neuromancer models are trained for three goals: logical rigor (follow formal rules, not plausible-sounding text), structured output (consistent JSON with premises and conclusions), and efficiency (smaller, faster, cheaper than frontier models).

Neuromancer XR is the first released member, vendor-described as a fine-tune of Qwen3-8B for explicit and deductive extraction. In a vendor-reported LoCoMo ablation where the final answer writer was always Claude 4 Sonnet, Neuromancer XR scored 86.9% overall versus 80.0% for Claude 4 Sonnet and 69.6% for base Qwen3-8B as the conclusion-derivation model. Neuromancer outputs then feed consolidation, peer cards, induction, and abduction.

## Write path: Deriver and Summarizer

The write path runs every time messages arrive:

1. Messages are stored immediately and a background reasoning task is enqueued, so writes stay fast.
2. The Deriver runs Neuromancer XR per message to extract explicit statements and deductive conclusions, processed in chronological order per peer.
3. The Summarizer builds rolling session summaries in parallel, vendor-described as short summaries about every 20 messages and long summaries about every 60 messages.
4. Conclusions, summaries, and peer cards are indexed in vector collections (search indexes for similarity lookup), one collection per observer-observed peer pair.

## Dreamer: periodic consolidation

Dreaming is vendor-marked as experimental. It is like sleep for the memory system: waking reasoning captures what happened, dreaming reflects on what it all means by reasoning over existing conclusions at the peer-representation level.

A dream cycle runs two specialists in sequence:

- **Deduction specialist:** finds knowledge updates such as a job change, fills in missed logical implications, resolves contradictions by deleting outdated conclusions, and updates peer cards.
- **Induction specialist:** finds patterns such as habits, preferences, personality traits, and correlations, only when at least two source conclusions support the pattern.

Automatic scheduling requires all of these to be true: at least 50 new conclusions since the last dream, at least 8 hours since the last dream, and dreaming enabled in configuration. When thresholds are met, Honcho waits for 60 minutes of inactivity; any new message cancels the pending dream and resets the timer. Manual schedule_dream calls bypass the thresholds but still skip if a dream is already pending or running. Dreams never span workspaces or different peer pairs.

## Query path: Dialectic and reasoning levels

The query path is served by Dialectic, a query-time agent:

- `peer.chat()` is anchored to one observer-observed pair and prefetches that pair's relevant conclusions.
- `honcho.chat()` is workspace-wide with no anchor, so it must search first and then read pair by pair with observer-to-observed attribution.
- `context()` is session-level retrieval that blends summaries with recent messages, with options for token budget, peer target, and semantic filtering, plus converters to OpenAI and Anthropic message formats.

Reasoning levels control Dialectic depth, tools, thinking budget, iterations, and output tokens. Vendor-reported per-query prices are minimal $0.001, low $0.01, medium $0.05, high $0.10, and max $0.50, where minimal is instant single-search and high and max run async for deeper research-style answers.

Write and query paths together look like this:

```
WRITE PATH (background)              QUERY PATH (on demand)
------------------------              ----------------------

app -> session.add_messages           app -> peer.chat() / context()
  |                                     |
  v                                     v
PostgreSQL store + enqueue           Dialectic agent
  |                                     |
  +--> Deriver (Neuromancer XR)         +--> prefetch conclusions
  |     explicit + deductive            +--> read pair-by-pair
  +--> Summarizer                       +--> synthesize answer
        short / long summaries

        |
        v
Dreamer (periodic: 50 conclusions,
  8h cooldown, 60-min idle)
  Deduction + Induction specialists
```

## Memory as Reasoning philosophy

The vendor's "Memory as Reasoning" idea says memory should predict, not just store. Formal logic gives an AI-native scaffold: LLMs (Large Language Models) are vendor-described as able to apply rigorous rules across thousands of conclusions without cognitive fatigue (human-style tired thinking) or belief resistance (rejecting ideas that clash with existing beliefs). Because conclusions keep their premises, they stay composable, meaning they can be stored, retrieved, combined, and re-reasoned by the Deriver, Dreamer, and Dialectic without rebuilding the pipeline.

**Covers:** reasoning.md, dreaming.md, architecture.md internals (docs v3, retrieved 2026-09-10)
