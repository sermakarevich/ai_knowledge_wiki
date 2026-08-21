> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# PersonalAI 2.0 — Connections

Related entries elsewhere in this knowledge base, organized by relationship to PAI-2.

## Direct baselines (used in this paper's own experiments)

- [[ai_papers/graph_rag/ArxivLightRAG/summary|LightRAG]] — a simple, fast dual-level (entity + community) GraphRAG baseline that PAI-2 beats by the largest margin (0.16 vs. PAI-2's 0.82 mean LLM-as-a-Judge in the best setup) — useful as the "flat/simple GraphRAG floor" comparison point.
- [[ai_papers/graph_rag/ArxivHippoRAG/summary|HippoRAG]] — the neurobiologically-inspired long-term memory retriever (HippoRAG 2 is PAI-2's strongest baseline, tying or beating PAI-2 on HotpotQA and DiaASQ) — worth reading alongside PAI-2's Section IV/V to see how Personalized PageRank traversal compares to PAI-2's LLM-planned traversal.
- **RAPTOR** (recursive clustering + summary-tree retrieval) — a baseline in PAI-2's evaluation, but not yet ingested into this KB; add as a future paper if deeper comparison is needed.

## Same research lineage (predecessor / same authors' line)

- **PersonalAI 1.0 (PAI-1)** — PAI-2's direct predecessor and the source of its graph-traversal algorithms (BeamSearch, WaterCircles); not yet ingested as a standalone KB entry, but its design and limitations are summarized in [[wiki/01-introduction-and-related-work|Introduction & Related Work]].

## Related agentic-GraphRAG / graph-traversal papers

- [[ai_papers/graph_rag/ArxivPathRouter/summary|PathRouter]] — also tackles agentic GraphRAG, but from a reward-alignment angle (training a router to prefer retrieval paths that actually improve answer quality) rather than PAI-2's prompt-driven planning loop — a complementary approach to the same "flat retrieval isn't adaptive enough" problem.
- [[ai_papers/graph_rag/ArxivGraphScout/summary|GraphScout]] — gives LLMs an intrinsic exploration ability for agentic graph reasoning; closely comparable in spirit to PAI-2's clue-query-driven traversal, worth a side-by-side read on how each frames "the LLM decides where to look next."
- [[ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/summary|From Local to Global (Microsoft GraphRAG)]] — the foundational hierarchical-community-summarization GraphRAG paper; PAI-2's related-work section doesn't cite it directly, but it's the architecture MINE-1's "GraphRAG" baseline (44% retention, wiki page 08) is presumably built on.
- [[ai_papers/graph_rag/ArxivRAGvsGraphRAG/summary|RAG vs. GraphRAG]] — a systematic evaluation of when GraphRAG helps versus plain vector RAG; useful context for judging whether PAI-2's added planning complexity is justified for a given query type (the paper finds vector RAG often matches or beats GraphRAG on local factual questions).

## Related long-term / graph memory for agents

- [[papers/ArxivHiGram/summary|HiGram]] — hierarchical graph memory for LLM agents with path-level localization and rewrite; both HiGram and PAI-2 use graph structure over flat vector memory, but HiGram focuses on maintaining/rewriting the graph over time rather than PAI-2's query-time planning loop.
- [[papers/ArxivSodaMem/summary|SodaMem]] — an evidence-grounded temporal knowledge-graph memory with write-time supersession and a planner–reader answering loop; SodaMem's planner–reader loop is conceptually close to PAI-2's plan-enhancement loop, but SodaMem is built specifically around temporal currency/conflict resolution — one of the exact gaps PAI-2's own Limitations section (wiki page 05) admits it hasn't solved (timestamps as plain text, no supersession mechanism).

## Not yet ingested but referenced by PAI-2 as related work

Think-on-Graph (ToG), Reasoning on Graphs (RoG), Debate on Graph (DoG), Pyramid-Driven Alignment (PDA), and Pseudo-Graph Generation & Atomic Knowledge Verification (PG&AKV) are all cited in [[wiki/01-introduction-and-related-work|Introduction & Related Work]] but have no standalone KB entry yet — candidates for future ingestion if this research line is pursued further.
