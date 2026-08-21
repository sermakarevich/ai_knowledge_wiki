> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/summary|From Local to Global (Microsoft GraphRAG)]] — this is the original GraphRAG design (community-detection + map-reduce over graph summaries) whose local-reasoning path is exactly what GRAGPOISON targets; reading it first clarifies what "indexing," "entities/relations," and "community summaries" mean before seeing them attacked.
- [[ai_papers/graph_rag/ArxivLightRAG/summary|LightRAG]] — one of the three graph-RAG systems GRAGPOISON is directly evaluated against (comparable ASR to GraphRAG and nano-GraphRAG), confirming the vulnerability is architectural rather than implementation-specific.
- [[ai_papers/graph_rag/ArxivHippoRAG/summary|HippoRAG]] — same attack surface in principle (graph-based retrieval via Personalized PageRank over an LLM-extracted knowledge graph); not tested in this paper, but its degree/centrality-driven retrieval mechanism is structurally similar to the degree-ranking that GRAGPOISON's relation-enhancement step exploits in GraphRAG.
- [[ai_papers/graph_rag/ArxivGraphRAGSurvey/summary|Graph Retrieval-Augmented Generation: A Survey]] — provides the three-stage taxonomy (graph indexing, graph-guided retrieval, graph-enhanced generation) that this paper's threat model maps onto directly: RQ1 targets indexing resilience, GRAGPOISON targets retrieval ranking, and the defenses section targets generation-time trust.
- [[papers/ArxivGraphRAGBench/summary|GraphRAG-Bench]] — benchmarks the accuracy/reasoning quality of GraphRAG, LightRAG, and Microsoft GraphRAG on clean data; this paper is the adversarial-robustness complement those benchmark numbers are missing — a system ranking well on GraphRAG-Bench says nothing about its resilience to GRAGPOISON-style relation poisoning.

_Other GraphRAG-adjacent entries in this KB (`ArxivGraphRAGLinkedInCustomerService`, `ArxivRAGvsGraphRAG`) were still mid-ingestion (source/wiki only, no completed summary.md) as of this writing, so they are not linked here._
