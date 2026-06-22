# Agent Memory on Elasticsearch: Hybrid Retrieval and DLS

**Article:** [How we built a persistent agent memory layer on Elasticsearch with 0.89 recall and zero tenant leaks (Noam Schwartz, 2026)](https://www.elastic.co/search-labs/blog/agent-memory-elasticsearch)
**Source:** Elasticsearch Labs (Search Labs) -- June 16, 2026

## Human Readable TL;DR

A chatbot forgets everything once a conversation ends -- like talking to someone with no short-term memory. This project gives the agent a real memory: a filing cabinet that survives between chats. It splits memory into three drawers -- a diary of events, a list of stable facts about you, and a set of how-to playbooks -- and uses smart search to pull the right note back at the right time. It also locks each person's drawer so no one sees anyone else's notes, and tested on 168 questions it found the right memory 89% of the time with zero leaks between users.

## TL;DR

Persistent agent memory built on Elasticsearch, split into three indices (episodic, semantic, procedural) by cognitive lifecycle. Recall uses hybrid retrieval (BM25 + Jina v5 dense vectors via RRF) plus cross-encoder reranking, with multiplicative time-decay and use-count scoring. Multi-tenant isolation enforced server-side via Document-Level Security (DLS) API keys. Achieves R@10 0.89 across 168 questions with 0 cross-tenant leaks. Exposed to any client via MCP (`recall_memory`, `write_memory`, `forget_memory`).

---

## Problem & Motivation

Context windows are short-term memory -- they vanish at session end. Agents need long-term memory: a persistent store that survives sessions. Naive approaches couple decay rules, leak data across tenants, or let stale facts outrank fresh ones. This design separates memory by lifecycle, scores by recency + usage, and enforces tenant isolation at the cluster level so isolation is not a code-layer afterthought.

---

## Main Original Ideas

1. **Three memory types per lifecycle.** Splits into three indices to avoid coupling decay and update rules:
   - **Episodic** -- time-stamped user events, written immediately, naturally decay.
   - **Semantic** -- distilled stable facts (e.g. "Sarah owns a Lumio Hub v2").
   - **Procedural** -- multi-step playbooks tracking `success_count` / `failure_count`.

2. **Hybrid retrieval + rerank.** Stage 1 fuses BM25 keyword and Jina v5 dense vectors via Reciprocal Rank Fusion (`rank_constant=30`), fetching 80 candidates per leg. Stage 2 re-scores merged candidates with a Jina v2 cross-encoder. A single write routes content to both inverted index and a `semantic_text` field via `copy_to` + inline inference, keeping storage footprint flat.

3. **Automatic pre-recall.** Agents paraphrase user messages before tool calls, stripping version numbers and proper nouns. System runs an automatic pre-recall on the verbatim user message, injected into the conversation as if the agent had made the call itself.

4. **Consolidation LLM.** Per-turn (or per-session in production), an LLM promotes episodic events into durable facts: new semantic facts with `supporting_episode_ids` for provenance, new procedural playbooks when resolutions don't match existing triggers, and `success_count++`/`failure_count++` updates on user confirmation. Dedup runs hybrid search on candidate facts, drops below-confidence candidates, flags duplicates at similarity >= 0.90.

5. **Supersession over deletion.** Contradictions don't delete -- they supersede. Old docs stay queryable for audit; recalls filter them out.

6. **DLS for tenant isolation.** Each user gets an API key whose role descriptor carries a DLS query; isolation enforced server-side on every query, not in app code.

---

## Key Findings

QA-style passage-retrieval eval over **168 questions**:

| Metric | Result | CI Gate |
|--------|--------|---------|
| **R@10** (avg) | **0.89** (0.85–0.893 across runs) | >= 0.85 |
| **R@5** | ~0.75 | >= 0.75 |
| **Cross-tenant leaks** | **0** | = 0 |

Recall by memory type:

| Type | R@10 | Note |
|------|------|------|
| Procedural | 1.0 | |
| Episodic | 0.98 | |
| Semantic | 0.81 | sibling collisions drag it down |

- Eval gates in CI; build fails below thresholds.
- `CATALOG_SOURCE_PRIOR = 0.85` softly tilts ranking toward user memory on near-ties; reranker can still prefer catalog when clearly more relevant.

---

## Architecture Details

**Hot-path writes.** Every user turn writes one episodic event immediately with `refresh=True` for same-turn visibility -- can write a new device fact and recall against it in the same message.

**Supersession flow:**
1. **Detect** -- agent spots recalled fact contradicting new statement.
2. **Classify** -- `"natural"` (update) vs `"harsh"` (denial, reduced confidence).
3. **Write** -- `write_memory(text=..., supersedes_id=..., contradiction=...)` creates new doc, marks old as `superseded_by`.
4. **Filter** -- recalls apply `filter must_not exists field=superseded_by`.
5. **Audit** -- old docs queryable with `include_superseded=True`.

Agent must supersede *all* facts made false by a new statement, not just the first match. Supports multi-level chains (abc -> xyz -> pqr).

**Time decay (Gauss per index):**
- `offset` (180d) -- flat zone; docs under 180 days get multiplier 1.0.
- `scale` (1825d ~5y) -- distance past offset where multiplier hits 0.5.
- Episodic decays on `timestamp`; semantic on `last_used_at` (bumped on recall). Procedural deliberately exempt -- bumping `last_used_at` rewards "recently tried" not "recently effective".

**Use-count boost:** `1 + log10(1 + use_count) * weight` -- recalled 10x boosts ~1.2x, 100x ~1.4x. Both decay and boost run via Painless in a `function_score` block with `_index` filters scoping effects per memory type.

**Multi-tenant DLS.** Role-descriptor DLS query admits a user's own docs plus the shared catalog (catalog docs lack `user_id`):

```
user_id == "sarah" OR must_not exists: user_id
```

Code layer adds a paranoia `user_id` filter as backup against config drift. Catalog + personal indices resolve in one Elasticsearch query via a `bool.should` pattern.

**MCP integration.** `/api/atlas/mcp/{user_id}` endpoint speaks Model Context Protocol. Any MCP client (Claude Desktop, Cursor, custom agents) gets three tools without rewriting: `recall_memory`, `write_memory`, `forget_memory`.

---

## Suggestions & Future Directions

1. Run consolidation per-session in production (vs per-turn) to reduce LLM cost.
2. Semantic recall (0.81) lags due to sibling collisions -- target for improvement.
3. Open-source implementation on GitHub includes example queries, tool definitions, and bootstrap scripts for per-user DLS keys.

---

## Authors & Institutions

Noam Schwartz (Elastic / Elasticsearch Labs).
