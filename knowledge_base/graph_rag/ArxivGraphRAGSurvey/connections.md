> [[index|Wiki]] | [[summary|Summary]]

# Graph Retrieval-Augmented Generation: A Survey — Connections

## Within this knowledge base

- [[ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/summary|Microsoft GraphRAG (From Local to Global)]] — this survey's G-Indexing/G-Retrieval/G-Generation taxonomy (Sec 5-7) directly covers Microsoft GraphRAG as a canonical example: entity-KG construction + community detection maps to "text indexing (subgraph-level, LLM-generated summaries)" (Sec 5.2.2), and its map-reduce-over-community-summaries answer strategy maps to "post-generation enhancement" (Sec 7.3.3). The survey also names it explicitly in its industrial-systems inventory (Sec 9.4).
- [[ai_papers/graph_rag/graph_rag|GraphRAG category page]] — this survey is the natural entry point for the whole `graph_rag` category: it supplies the shared vocabulary (retriever type, retrieval paradigm, retrieval granularity, graph-to-text formats) that the category's other papers can be read against.

## Being ingested in parallel (not yet linkable)

- ArxivHippoRAG, ArxivLightRAG (at `papers/ArxivHippoRAG/` and `papers/ArxivLightRAG/`) — other GraphRAG-family papers currently being processed into this knowledge base. Both only have `source/` and `wiki/` subfolders so far, no `summary.md`; link to them once their top-level synthesis exists. Based on the survey's taxonomy, HippoRAG would likely map to the "non-parametric/PPR-based retriever + iterative retrieval" corner (Sec 6.1.1/6.4.2, Personalized PageRank pruning), and LightRAG to "hybrid indexing" plus "dual-level (low/high) retrieval granularity" — but this is a prediction, not yet verified against their wiki content.

## Where this fits in the broader KB

This survey serves as the taxonomy/map for the `graph_rag` category: someone landing on any individual GraphRAG paper (Microsoft GraphRAG, HippoRAG, LightRAG, or future additions) should read this survey first to get the vocabulary the category uses — G-Indexing/G-Retrieval/G-Generation stages, retrieval granularity (node/triplet/path/subgraph), and the graph-to-text conversion formats (adjacency table, natural language, code-like, syntax tree, node sequence). Without that frame, individual system papers read as one-off tricks rather than points on a shared design space.

Relative to the `rag_and_retrieval` category (plain-text RAG, chunking, document segmentation), this survey is the explicit bridge: Sec 2.1 positions GraphRAG as a branch of RAG that swaps a text corpus for a graph database, and Sec 1's three named RAG limitations (neglecting relationships, redundant information, lacking global information) are the stated reasons anyone would move from that category into this one. No single `rag_and_retrieval` entry was found to warrant a direct citation here; the relationship is at the category level, not the paper level.

Note: there is a pending fleet task (`fleet-gragmv02`) to move this paper's folder from `papers/ArxivGraphRAGSurvey/` into `ai_papers/graph_rag/`. Once that move happens, the cross-folder links above (`ai_papers/graph_rag/...`) will need to be revisited/shortened to category-relative form.
