> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[ai_papers/graph_rag/ArxivHippoRAG/summary|HippoRAG]] — one of the nine methods GraphRAG-Bench evaluates directly; HippoRAG's own paper claims state-of-the-art multi-hop QA via Personalized PageRank, and GraphRAG-Bench independently confirms HippoRAG as a top-2 performer on both generation accuracy and reasoning fidelity (R/AR) — a rare case of a method's own claims and a third-party benchmark agreeing.
- [[ai_papers/graph_rag/ArxivLightRAG/summary|LightRAG]] — also one of the nine benchmarked methods; LightRAG's paper claims strong results at low token/API cost, but GraphRAG-Bench shows it only gets "slight gains" over the GPT-4o-mini baseline on generation accuracy, a more tempered result than LightRAG's own reported comparisons.
- [[ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/summary|From Local to Global (Microsoft GraphRAG)]] — the "GraphRAG" method benchmarked here is this paper's community-detection/map-reduce approach; GraphRAG-Bench extends its evaluation from query-focused summarization (the original paper's task) to college-level multi-hop reasoning, finding it lands in the top-3 for both accuracy and reasoning.
- [[ai_papers/graph_rag/ArxivGraphRAGSurvey/summary|Graph Retrieval-Augmented Generation: A Survey]] — the survey's three-stage taxonomy (graph indexing, graph-guided retrieval, graph-enhanced generation) maps directly onto GraphRAG-Bench's own metric families (construction, retrieval, generation) plus its added fourth dimension, reasoning fidelity — GraphRAG-Bench can be read as putting the survey's taxonomy to an empirical test.

_Other GraphRAG-adjacent entries currently in this KB (`ArxivGraphRAGLinkedInCustomerService`, `ArxivGraphRAGUnderFire`, `ArxivRAGvsGraphRAG`, `ArxivSevenFailurePointsRAG`, `ArxivARESRAGEvaluation`) were still mid-ingestion (source/wiki only, no completed summary.md) as of this writing, so they are not linked here — revisit once they finalize._
