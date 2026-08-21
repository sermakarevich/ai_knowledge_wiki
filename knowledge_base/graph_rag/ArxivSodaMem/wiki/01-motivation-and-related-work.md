> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Motivation & Related Work

**In one sentence:** Flat RAG diaries and Markdown logs win needle-in-haystack recall but fail on the four pressures that make long-horizon personal assistants hard—currency/conflict, temporal structure, provenance, and association—so SodaMem reframes memory as an evidence-grounded temporal knowledge graph with supersession edges, mandatory provenance, and a planner–reader answering loop.

## Key points

- The paper's thesis: LLM agents accompanying users over weeks must remember *what is currently true*, not merely what was once said; flat RAG and Markdown logs "optimize needle retrieval but underserve currency, provenance, and ordered temporal reasoning."
- The field has shifted from "can the model find a needle in the transcript?" to "can the agent maintain a coherent, updatable model of the user (or environment) and use it under the right conditions?"
- Four failure modes (P1–P4) that Markdown/flat RAG leave unresolved: (P1) currency/conflict, (P2) temporal structure, (P3) provenance, (P4) association.
- Motivation's running example: "I love spicy food" → "I am cutting down on spice" → "What should I cook tonight?"—a Markdown log keeps all three and a flat retriever may surface the first; a temporal graph should supersede (or validity-close) the old preference and still cite the justifying turns.
- Six explicit design principles: evidence first, explicit time (mention/occurrence/validity + query window & sort), writable currency as first-class, multi-signal wide recall, connection-density ranking with soft time bonuses, and toolful planner–reader answering.
- Related work is organized in three axes—benchmarks (LoCoMo, LongMemEval), external memory & structure (MemGPT, MemoryBank, Mem0, HippoRAG, Zep), and indexing/conflict/controllers (SimpleMem, RaMem, Memory-R1, AgeMem)—against which SodaMem differentiates on provenance spans, the three temporal axes, write-time supersession, and a cited planner–reader loop.
- Related work also includes "soft time" handling for user misremembering ("two months ago" for a three-month-old fact): hard temporal filters drop the right evidence, so SodaMem parses query time into a soft window + sort direction and treats window match as a ranking bonus.

---

## Abstract

SodaMem is an evidence-grounded temporal graph memory for LLM agents that (i) extracts typed FactEvents with mandatory provenance spans, (ii) persists mention time, occurrence time, and validity with SUPERSEDES/CONTRADICTS/UPDATES edges under hybrid lexical–dense indexing, and (iii) answers via a planner–reader loop that gathers citable evidence before composing a final response. On LongMemEval-S, the store-of-record configuration reaches 92.8% accuracy (464/500; best of N = 3) at mean $0.00161/question (≈18.3k tokens; median $0.00111 / ≈14.6k) with deepseek-v4-flash. The authors compile public systems with estimable API cost into a cost table and cost–accuracy map; under these estimates SodaMem sits near the accuracy frontier at Flash-tier spend and strictly dominates several higher-cost, lower-accuracy points. Accuracy uses the same Flash model as reader and judge (self-grading); costs exclude ingest/judge and cross-system comparisons are compiled estimates rather than a single-harness bake-off. Code: https://github.com/SodaMem/SodaMem. Authors: Fengrong Wan\*, Chengcan Wu^1, Ningtao Lyu^1, Peking University (arXiv:2608.08055v1 [cs.AI], 8 Aug 2026).

## Introduction

Long-horizon personal memory research has consolidated around "a small set of measurable pressures rather than a single architecture." Benchmarks such as LoCoMo (Maharana et al. 2024) and LongMemEval (Wu et al. 2024) probe multi-session fact recall, knowledge updates, temporal reasoning, preference tracking, and abstention; complementary suites stress implicit state invalidation (Chao et al. 2026), memory-operation correctness (MemOps 2026), prospective triggering (PM-Bench 2026), MemBench-style axes (Tan et al. 2025), and agent–environment experience beyond chat (Wu et al. 2026; He et al. 2026; Hu et al. 2025).

### Failure modes (P1)–(P4)

Systems work spans a familiar pipeline—land, structure, index, link, maintain, retrieve/answer (Agent-Native 2026; Huang et al. 2026; Lewis et al. 2020; Xu et al. 2025; Rasmussen et al. 2025; Liu et al. 2026; Memory-R1 2025; NapMem 2026; Chhikara et al. 2025)—but everyday assistants still hit four failure modes:

- **(P1) Currency / conflict.** Preferences reverse; append-only logs leave "which value is current?" to an LLM over unordered chunks, where deterministic freshness often beats free-form judgment (Reddy and Challaram 2026; Chao et al. 2026).
- **(P2) Temporal structure.** Ordering / "most recently" / relative-date questions break when relative phrases lack a comparable timeline.
- **(P3) Provenance.** Citations to source turns are needed for trust; lossy summaries and opaque vector hits weaken audit.
- **(P4) Association.** Multi-hop synthesis needs entity/claim links beyond cosine neighbors, while avoiding context collapse from episode-wrong but similar memories (Yang et al. 2026).

Our (the authors') stance: for retrospective personal QA, treat memory as an evidence-grounded temporal knowledge graph: typed FactEvents with source spans, temporal axes (mention, occurrence, validity), and SUPERSEDES/CONTRADICTS/UPDATES edges; a planner–reader loop gathers evidence before prose. This complements RL controllers and prospective-memory suites: they prioritize a maintainable, citable state for LongMemEval-style questions, with timeline resolution for temporal misses.

### Method focus

SodaMem is instantiated as a three-stage system (Figure 1, described in the method page):

1. **Ingest:** LLM extraction of FactEvents with provenance hard constraints and modality/calendar post-processing; optional entity-subject prompts to reduce star-graph collapse.
2. **Store & maintain:** SQLite facts plus hybrid BM25–dense indexes; supersession and contradiction edges; dream/maintenance; optional session-anchored timeline resolution for relative dates.
3. **Answer:** hybrid recall, a multi-step planner over memory tools, and a separate reader that emits cited answers.

How SodaMem addresses (P1)–(P4): supersession and validity closing target (P1); timeline resolution and temporal fields on FactEvents target (P2); mandatory source spans and reader citations target (P3); typed predicates, entity roles, and graph edges target (P4), while the planner can expand sessions and inspect cards to reduce episode confusion relative to single-shot RAG.

### Contributions

- **Problem framing.** Synthesize agent-memory research foci and method axes; isolate currency, temporal structure, provenance, and association as the failure modes that Markdown/flat RAG leave unresolved for long-horizon personal assistants.
- **System.** SodaMem's ingest–store–planner–reader pipeline: FactEvent schema, hybrid retrieval, supersession semantics, and a proposed timeline-resolution layer aimed at temporal-reasoning errors.
- **Cost–accuracy evaluation.** On LongMemEval-S, a store-of-record 92.8% run at mean $0.00161/question (≈18.3k tokens; median $0.00111 / ≈14.6k); compile public baselines with estimable API cost into a cost table and cost–accuracy map; analyze the dominated (higher-cost, lower-accuracy) region relative to SodaMem.

## Related Work

### Benchmarks

LoCoMo (Maharana et al. 2024) and LongMemEval (Wu et al. 2024) are the main yardsticks for retrospective personal-memory QA (multi-session recall, updates, temporal reasoning, preference, abstention). Broader suites probe implicit invalidation, memory-operation correctness, prospective triggering, and agent–environment experience (Chao et al. 2026; MemOps 2026; PM-Bench 2026; Tan et al. 2025; Hu et al. 2025; He et al. 2026; Wu et al. 2026). The authors evaluate on LongMemEval-S and treat the others as orthogonal pressures.

### External memory and structure

RAG and long-context readers (Lewis et al. 2020; Karpukhin et al. 2020) serve static corpora; agent settings continually write user state. MemGPT-style paging (Packer et al. 2023), MemoryBank / hierarchical summarization (Zhong et al. 2023; Lee et al. 2024), and Mem0-style extractive APIs (Chhikara et al. 2025) establish the need for an external store. Hierarchical and note/graph designs (NapMem 2026; LightMem 2026; Xu et al. 2025; Rasmussen et al. 2025; Edge et al. 2024; Gutiérrez et al. 2024) move beyond flat chunks via compression, Zettelkasten links, or bi-temporal graphs with edge invalidation. SodaMem is closest to extraction-plus-temporal-graph lines, but requires provenance spans, mention/occurrence/validity axes, write-time supersession, and a cited planner–reader loop.

### Indexing, conflict, and controllers

SimpleMem stresses density gating and multi-view indexes (Liu et al. 2026); RaMem highlights context collapse (Yang et al. 2026); deterministic conflict work favors explicit version marks over free-form freshness judgment (Reddy and Challaram 2026). Parallel lines learn memory-tool policies with RL (Memory-R1 2025; AgeMem 2026) or optimize multi-turn search (Jin et al. 2025). Markdown diaries remain a strong simplicity baseline—cheap but weak on currency, order, provenance, and association. SodaMem is positioned as an engineering-first temporal graph substrate for retrospective personal QA; learned controllers can later sit on the same FactEvent contract.

### Soft time and design principles

Users often misremember windows ("two months ago" for a three-month-old fact); hard temporal filters then drop the right evidence. SodaMem stores comparable temporal fields, parses query time into a soft window plus sort direction, and treats window match as a bonus in ranking confidence. Principles:

1. **Evidence first:** no durable claim without a source span.
2. **Explicit time:** mention, occurrence, and validity; query → window + sort direction.
3. **Writable currency:** supersession/contradiction are first-class; invalid facts are excluded.
4. **Multi-signal wide recall** with per-head expansion, then fusion.
5. **Connection-density ranking** with soft time bonuses and near-duplicate merge.
6. **Toolful answering:** planner–reader gather-then-read (Memory in the Loop 2026).

## Motivation: Currency and multi-signal recall

The running example—"I love spicy food," later "I am cutting down on spice," then "What should I cook tonight?"—illustrates the currency problem: a Markdown log keeps all three turns; a flat retriever may surface the first. A temporal graph should supersede (or validity-close) the old preference, answer from the latest state, and still cite the justifying turns—the pattern behind LongMemEval knowledge-update items (Wu et al. 2024; Reddy and Challaram 2026). Even with correct facts stored, single-channel retrieval is brittle: embeddings can be episode-wrong (Yang et al. 2026), BM25 may miss paraphrase, and entity expansion can explode. Hence SodaMem uses wide multi-signal recall (graph, BM25, dense) and ranks by connection density across auditable links, not cosine alone.

**Covers:** Abstract, Introduction (stance, method focus, P1–P4 failure modes, contributions), Related Work (Benchmarks; External memory and structure; Indexing/conflict/controllers; Soft time and design principles), Motivation (currency & multi-signal recall).
