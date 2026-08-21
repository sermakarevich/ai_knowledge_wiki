> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[graph_rag/ArxivGraphRAGSurvey/summary|GraphRAG Survey]] — surveys graph-based RAG as a three-stage pipeline (graph indexing, graph-guided retrieval, graph-enhanced generation); this paper's flat-chunk failure taxonomy (Missed Top Ranked, Not in Context, etc.) is the vector-RAG baseline that graph-based retrieval is positioned as improving on for multi-hop and relational queries.
- [[graph_rag/ArxivHippoRAG/summary|HippoRAG]] and [[graph_rag/ArxivLightRAG/summary|LightRAG]] — both address specific failure points this paper names (Missing Content / Missed Top Ranked, in particular for multi-hop questions) with a graph-retrieval mechanism instead of pure vector similarity — a same-problem-different-method relationship.
- [[papers/ArxivGraphRAGBench/summary|GraphRAG-Bench]] — a controlled benchmark measuring GraphRAG reasoning quality; contrasts directly with this paper's methodology, which is a qualitative 3-case-study experience report rather than a benchmark with quantitative retrieval metrics.
- [[rag_and_retrieval/AAFLOWScalableAgenticWorkflows/summary|AAFLOW]] — models RAG pipelines as composable operators for throughput/latency optimization; complements this paper's engineering-lessons focus (which is about correctness/failure modes, not throughput) with the performance-engineering side of the same pipeline stages (chunking, retrieval, consolidation).

Other RAG papers currently staged in `/Users/sergii/.kb/papers/` (ArxivARESRAGEvaluation, ArxivGraphRAGLinkedInCustomerService, ArxivGraphRAGUnderFire, ArxivRAGvsGraphRAG) have not yet been synthesized (no `summary.md` present at the time of writing), so they are not linked here — revisit this file once they are filed.
