> [[../index|Research]] | [[../overview|Overview]] | [[../digest|Digest]]

# Disagreements — AgentBrain / agent_memory

**Focus:** Which of these 20 agent second-brain GitHub projects are worth using for a system that captures sources, connects ideas, remembers context, and helps agents act on it, and how do they compare across capture, linking, memory/recall, and agentic action?

**Scope:** This file is grounded only in the four topic digests (`topics/01-capture-ingest-lanes/digest.md`, `topics/02-linking-kg-wiki/digest.md`, `topics/03-memory-recall-substrate/digest.md`, `topics/04-agentic-action-harness/digest.md`) and the 20 source summaries they link. No wiki pages, raw sources, or web were consulted.

## Verdict: none found

No real contradictions were found across the 20 sources on any proposition bearing on the focus question. Every candidate pair examined collapses into one of three non-contradictions:

1. **Different systems, system-scoped claims.** Each summary describes its own repo's architecture (e.g. Hindsight requires an LLM on every retain/recall/reflect path [[research_topics/agent_memory/Hindsight/summary|Hindsight]] while MemU forbids any LLM call in the service [[research_topics/agent_memory/MemU/summary|MemU]]; Docsagent does BM25-only lexical retrieval [[research_topics/agent_memory/DocsAgent/summary|Docsagent]] while Hindsight fuses four retrieval strategies [[research_topics/agent_memory/Hindsight/summary|Hindsight]]). No source asserts its choice as a universal claim about all systems, so there is no X vs not-X on the same proposition.
2. **Design choices already framed as differences, not disputes.** The digests' own "Where they differ" sections (entry mouth, keep-gate, graph weight, LLM dependence, store shape, orchestration weight, tenancy) are explicit trade-offs — e.g. VaultCurate keeps no persistent graph while Swarmvault/SageWiki do — and topic-02 states outright: "No contradictions on the linking model itself; differences above are design choices (graph weight, gating mechanism, freshness math), not factual disputes."
3. **Intra-source count/version slips, not cross-source disputes.** CogSecondBrain "33 skills" vs `.cursorrules` "17 skills", Makerskills "20 dirs" vs "21 intents", Agentmemory "1674+ vs 1596+ tests" are snapshot/unit-of-count artifacts within single sources (canonical set vs subset mirror, intents vs dirs, version drift), already flagged in the summaries — not contradictions between sources about what to build or use.

**Nearest tensions checked and rejected:** (a) "local by default / cloud opt-in only" vs OpenWiki's default-on Jina Reader/Google Translate and AgentSecondBrain's required Deepgram-for-voice — the capture digest already carves these out as explicit exceptions/edges, not silent violations; (b) "core indexing/search needs no API key" (linking digest) vs SageWiki's LLM-gated `compile` — a scope mismatch (post-compile serving vs compile-time synthesis), with the digest's phrasing arguably overgeneralised but not contradicted on any identical operation; (c) competing quantitative wins (OpenViking LoCoMo 80–83%, Agentmemory 95.2% R@5, Hindsight LongMemEval SOTA) — different harnesses, metrics, and snapshots, all vendor-reported, so not comparable claims and not in conflict.

**Why this outcome is expected:** the 20 sources are independent repos answering different slices of the focus (capture lanes, linking, recall substrate, action harness) with per-system README/config-level evidence; none refutes another's architecture, and none makes universal claims about capture, linking, memory, or agency that a second source denies.
