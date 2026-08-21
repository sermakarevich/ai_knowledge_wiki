# Why Neighborhoods Matter — Traversal Context and Provenance in Agentic GraphRAG

**Paper:** [Why Neighborhoods Matter: Traversal Context and Provenance in Agentic GraphRAG (Terrenzi et al., 2026)](https://arxiv.org/abs/2605.15109)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

Imagine an AI assistant that answers a question by wandering through a map of connected facts — visiting maybe a dozen "neighborhoods" of information — but at the end only names two or three of them as its sources. Does that short citation list tell you everything it actually used? This paper says no: even the neighborhoods it walked through but never named as sources still nudged the answer. It's like crediting only the two shops you bought something from on a trip, while ignoring that the route you took past a dozen other shops shaped what you noticed and decided to buy.

## TL;DR

The paper studies "agentic GraphRAG" systems — LLM agents that autonomously traverse a knowledge graph, deciding what to query and when to stop, then cite the entities that supported their final answer. Using a 30-question multi-hop QA benchmark built from 2WikiMultiHopQA, the authors run three graph-ablation studies that surgically remove or mask different classes of graph entities (cited, randomly chosen, visited-but-uncited) to test whether final citations are necessary, sufficient, and complete explanations of the answer. Result: cited entities are necessary (removing them tanks accuracy) but not sufficient (restricting the system to only cited entities also hurts accuracy) — visited-but-uncited entities and overall graph structure still measurably shape the answer.

---

## Problem & Motivation

RAG grounds LLM answers in external sources to fight hallucination and enable citation-based attribution. Agentic GraphRAG goes further: an agent autonomously traverses a knowledge graph, deciding what to query and when it has enough evidence, before producing a cited answer. Prior citation-faithfulness work asks whether cited sources genuinely supported the answer — but it assumes the citation set is a *complete* account of what the agent used. Agentic graph traversal breaks that assumption: the agent sees far more of the graph (neighboring nodes, relation patterns, community structure) than it ultimately cites, so an audit framed only around "which sources were cited" may miss part of what actually shaped the response.

---

## Main Original Ideas

1. **Trajectory-level framing of citation faithfulness.** Instead of treating citation faithfulness as a property of the final answer/citation pair, the paper reframes it as a property of the whole graph-traversal trajectory — traversal, structure, and visited-but-uncited entities may all be evidentially relevant.
2. **A graph-ablation methodology for necessity/sufficiency/completeness.** Three studies test whether cited evidence is *necessary* (remove cited entities), *sufficient* (isolate to only cited entities), and whether visited-but-uncited context matters (mask/remove visited-but-uncited entities) — each with a matched control condition (random ablation, text-only isolation, entity-vs-text masking) to separate the specific effect from generic graph-perturbation noise.
3. **Empirical demonstration that cited entities are necessary but not sufficient.** Across six systems (plain LLM, RAG, non-agentic GraphRAG, and three agentic GraphRAG citation regimes), the same qualitative pattern holds: cited-entity removal hurts far more than random removal, but isolating to cited-only entities also hurts — meaning the graph neighborhood around citations carries real evidentiary weight.

---

## Key Findings

**Table 1 — Baseline accuracy and evidence-usage footprint**

| System | Accuracy | Retrieved TUs | Cited TUs | Visited entities | Cited entities |
|---|---|---|---|---|---|
| **Evidence-first (agentic)** | **80.0%** | 1.4 | 1.3 | 10.5 | 1.8 |
| Agentic GraphRAG | 76.0% | 1.5 | 1.6 | 11.9 | 1.9 |
| Visited-only (agentic) | 72.0% | 1.6 | 1.3 | 11.1 | 1.6 |
| GraphRAG (non-agentic) | 60.0% | 13.3 | 1.4 | 15.6 | 1.8 |
| RAG | 56.7% | 5.0 | 1.0 | – | – |
| LLM only | 16.7% | – | – | – | – |

Agentic systems visit ~10-16 entities while citing only ~2 — a large gap between the graph-interaction trace and the final provenance trace.

**Table 2 — Intervention results (25 non-trivial questions)**

| Condition | Agentic GraphRAG | Evidence-first | Visited-only | GraphRAG |
|---|---|---|---|---|
| Baseline accuracy | 76.0% | 80.0% | 72.0% | 60.0% |
| Cited-entity removal → accuracy | ↓ 36.0% | ↓ 32.0% | ↓ 40.0% | ↓ 28.0% |
| Random removal (matched size) → accuracy | ↑ 84.0% | ↓ 76.0% | ↑ 80.0% | ↓ 58.7% |
| Full isolation (cited-only) → accuracy | ↓ 68.0% | ↓ 28.0% | ↓ 24.0% | ↓ 48.0% |
| Text-only isolation → accuracy | ↓ 72.0% | ↓ 60.0% | ↓ 64.0% | → 60.0% |
| Visited-but-uncited entity removal → accuracy | ↓ 68.0% | ↓ 68.0% | ↓ 60.0% | ↓ 56.0% |
| Visited-but-uncited entity text mask → accuracy | ↓ 72.0% | ↓ 60.0% | ↓ 52.0% | ↓ 40.0% |

- Cited-entity removal drops accuracy sharply across every system; random removal of an equal-sized set does not — and sometimes *improves* accuracy — showing the cited-ablation effect is not just generic graph damage.
- Restricting systems to only their originally cited entities (full isolation) still degrades accuracy everywhere, so citations alone don't reconstruct the needed context.
- Text-only isolation (keep graph structure, hide non-cited text) recovers more accuracy than full isolation — the mere presence, position, and connectivity of uncited entities helps traversal and narrows the search space.
- Removing or masking visited-but-uncited entities also hurts accuracy across all systems, confirming that neighborhood/navigational context that never appears in the citation list still does evidentiary work.

See [[wiki/03-results-and-discussion]] for full breakdown of "output changed" rates alongside accuracy.

---

## Suggestions & Future Directions

1. Repeat the interventions on larger benchmarks and richer, real-world knowledge graphs — the current study uses a controlled KB built from a 30-question 2WikiMultiHopQA subset (1,815 entities, 1,692 relationships).
2. Extend to domain-specific knowledge bases beyond the synthetic multi-hop QA setting.
3. Develop citation mechanisms that expose the relevant traversal context, not just the final supporting entities — i.e., provenance interfaces that surface trajectory, not only citation lists.
4. Investigate the interplay between parametric knowledge (what the LLM already knows), cited knowledge, and knowledge acquired purely through traversal.

---

## Authors & Institutions

Riccardo Terrenzi, Maximilian von Zastrow, Serkan Ayvaz (affiliations not stated in the extracted text; arXiv preprint, 2605.15109).

## Figures

![Representation of the three agentic graphRAG systems tested](wiki/images/fig1-agentic-graphrag-systems.png)

![Example of the three graph ablations on a synthetic subgraph](wiki/images/fig2-graph-ablations.png)
