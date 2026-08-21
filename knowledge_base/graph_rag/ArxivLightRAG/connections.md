> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/summary|GraphRAG: From Local to Global]] — the primary baseline LightRAG benchmarks against throughout; both build an LLM-extracted knowledge graph from documents, but GraphRAG retrieves via community detection and community-report summarization, while LightRAG retrieves via dual-level keyword matching directly over entities/relations — LightRAG's central claim is that this is both cheaper to update and roughly as good or better on retrieval quality.
- [[ai_papers/graph_rag/ArxivGraphRAGSurvey/summary|A Survey on GraphRAG]] — frames graph-RAG generically as a three-stage pipeline (graph indexing, graph-guided retrieval, graph-enhanced generation); LightRAG is a concrete instance of that pipeline, useful for placing LightRAG's specific design choices (dual-level retrieval, incremental merge) within the wider design space the survey maps out.
- [[ai_papers/graph_rag/ArxivHippoRAG/summary|HippoRAG]] — a different graph-based retrieval design (OpenIE triples + Personalized PageRank over the graph) aimed at multi-hop QA; shares the "build a knowledge graph, retrieve from graph structure instead of chunks" problem framing with LightRAG but uses a different retrieval mechanism (graph-traversal-via-PageRank vs. LightRAG's dual-level keyword + vector matching) — a useful same-problem-different-method comparison.

_Note: two related in-progress entries — `ArxivGraphRAGBench` and `ArxivRAGvsGraphRAG` — exist under `/Users/sergii/.kb/papers/` but have no `summary.md` yet (still mid-pipeline), so they are not linked here._
