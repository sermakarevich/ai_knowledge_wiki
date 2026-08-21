> [[index|Wiki]] | [[summary|Summary]]

# RAG vs. GraphRAG — Connections

This paper is part of a batch of GraphRAG-related papers being ingested into the KB in parallel (2026-08-20). Related entries found so far:

- [[../../ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/summary|From Local to Global: A GraphRAG Approach]] (Edge et al.) — this is the community-based GraphRAG system (Microsoft GraphRAG, Local/Global search) that this paper directly benchmarks and whose LLM-as-a-Judge summarization conclusions this paper's position-bias experiment specifically re-examines and complicates.
- [[../../ai_papers/graph_rag/ArxivHippoRAG/summary|HippoRAG]] — the text-centric graph-guided family; this paper evaluates HippoRAG2 (the successor system) as one of its four representative GraphRAG implementations and finds it the strongest GraphRAG variant on multi-hop QA.
- [[../../ai_papers/graph_rag/ArxivGraphRAGSurvey/summary|GraphRAG Survey]] — provides the three-stage pipeline framing (indexing, retrieval, generation) this paper's four-family taxonomy sits within; read the survey first for the landscape, this paper for the controlled head-to-head numbers.
- [[../ArxivGraphRAGBench/summary|GraphRAG-Bench]] — a domain-specific reasoning benchmark for GraphRAG; complements this paper's general-domain QA/summarization benchmark with a harder, domain-specific reasoning angle.
- [[../ArxivSevenFailurePointsRAG/summary|Seven Failure Points When Engineering a RAG System]] — catalogs RAG failure modes at a systems-engineering level; this paper's NULL/abstention failures under IRCoT and Integration (small model over-generating instead of abstaining) are a concrete instance of the kind of failure that survey catalogs.
- [[../ArxivGraphRAGUnderFire/summary|GraphRAG under Fire]] — examines GraphRAG's robustness to adversarial/poisoned input; a natural next read after this paper's cost/quality trade-off analysis, since a graph that's cheap to poison undercuts the "reasoning benefit" this paper credits to GraphRAG.

Not yet linkable (still mid-pipeline as of 2026-08-20, no `summary.md` present): `ArxivGraphRAGLinkedInCustomerService`, `ArxivARESRAGEvaluation`. Revisit this file once those land.
