> [[index|Wiki]] | [[summary|Summary]]

# HippoRAG — Connections

## Within this knowledge base

- **[[ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/index|Microsoft GraphRAG (From Local to Global)]]** — HippoRAG's own related-work section (wiki/05) explicitly places Microsoft GraphRAG in the same "offline knowledge-integration" camp as itself, alongside RAPTOR and MemWalker. The key contrast: GraphRAG integrates knowledge by *summarizing* communities of the graph bottom-up (Leiden clustering + map-reduce over community summaries), so any new data requires re-running summarization; HippoRAG integrates knowledge by simply adding nodes/edges to its graph, with no re-summarization step. GraphRAG targets global, query-focused sensemaking over a whole corpus; HippoRAG targets precise multi-hop passage retrieval for QA — different retrieval objectives built on a similar "LLM-built graph as index" foundation.
- **[[ai_papers/graph_rag/ArxivGraphRAGSurvey/index|Graph Retrieval-Augmented Generation: A Survey]]** — the survey's three-stage GraphRAG pipeline (indexing, retrieval, generation) is a useful frame for placing HippoRAG precisely: HippoRAG's indexing stage is LLM-driven OpenIE producing a schemaless entity-relation graph, and its retrieval stage is Personalized PageRank rather than the survey's more common graph-traversal or subgraph-extraction retrievers. Worth reading the survey's retrieval-stage taxonomy alongside wiki/02-methodology to see where PPR-seeded retrieval sits relative to other graph-retrieval strategies.
- **[[ai_papers/rag_and_retrieval/GraphRAGTop10Materials/index|GraphRAG — Top 10 Materials]]** — curated reading list covering GraphRAG system design, measured retrieval quality, and failure modes; HippoRAG is a natural addition to lens 1 (system understanding) given its explicit ablations of OpenIE and PPR components, and to lens 2 given its transparent recall@k tables across three multi-hop benchmarks.
- `papers/ArxivLightRAG` and `papers/ArxivRAGvsGraphRAG` exist in this KB but are not yet finalized (no `summary.md`/`index.md` present as of this writing) — once finalized, LightRAG (a lighter-weight graph-RAG variant) and the RAG-vs-GraphRAG comparison paper would be natural companions to link here; re-check and add links once those folders complete their pipelines.

## Mentioned by the paper but not yet in this KB

HippoRAG's own related-work section (wiki/05-related-work-conclusion) names several systems this KB does not yet contain a folder for — flagged here as candidates for future ingestion:

- **RAPTOR** (recursive abstractive summarization for tree-organized retrieval) — one of HippoRAG's direct single-step retrieval baselines (wiki/03) and also grouped with it in the "offline knowledge-integration" related-work camp (wiki/05). HippoRAG beats RAPTOR on MuSiQue and 2WikiMultiHopQA in the reported benchmarks.
- **MemWalker** — grouped alongside RAPTOR and GraphRAG as an offline-summarization-based long-term-memory approach; distinguished from HippoRAG by its reliance on re-summarization when new data arrives.
- **Think-on-Graph** — not mentioned in this paper's related work at all (the paper predates or simply omits it); no direct comparison exists in the source text, so no connection can be honestly drawn here beyond both being graph-based retrieval-augmented methods.

## Suggested next reads

1. If evaluating GraphRAG-family systems for a production knowledge-integration use case, read this paper's [[wiki/04-discussions|ablations]] alongside Microsoft GraphRAG's community-summarization approach to decide between "graph + PageRank" (cheap incremental updates, simple graph search) and "graph + hierarchical summarization" (better for corpus-wide sensemaking, costlier updates).
2. The [[wiki/06-appendix-pipeline-errors|error analysis]] (NER 48%, OpenIE 28%, PPR 24% of errors) is a useful checklist when debugging any LLM-built-knowledge-graph retrieval system, not just HippoRAG specifically.
