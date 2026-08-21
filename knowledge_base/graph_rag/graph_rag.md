# GraphRAG

Graph-based retrieval-augmented generation: building knowledge graphs from documents and retrieving from graph structure (entities, relations, communities) instead of — or alongside — flat text chunks. Covers canonical systems (Microsoft GraphRAG, HippoRAG, LightRAG), measured retrieval quality (recall@k, MRR, golden multi-hop datasets, LLM-as-judge), and failure modes (ranking drift, hallucination amplification, stale graphs, missing provenance).

Curated source list: [[../rag_and_retrieval/GraphRAGTop10Materials/index|GraphRAG Top 10 Materials]].

## Papers
- [[ArxivGraphRAGLocalToGlobal/summary]] — Builds a knowledge graph from a corpus, summarizes it into topic communities, and answers global "what are the themes" queries via map-reduce over those summaries, beating vector RAG on comprehensiveness and diversity.
- [[ArxivGraphRAGSurvey/summary]] — First systematic survey of GraphRAG, framing it as a three-stage pipeline (graph indexing, graph-guided retrieval, graph-enhanced generation) that grounds RAG in relational graph structure instead of flat text.
- [[ArxivHippoRAG/summary]] — Mimics the hippocampus's memory-indexing role by building a knowledge graph from OpenIE triples and retrieving via Personalized PageRank, beating single-step retrievers on multi-hop QA while being far cheaper and faster than iterative methods.
- [[ArxivARESRAGEvaluation/summary]] — ARES automatically evaluates RAG systems on context relevance, faithfulness, and answer relevance using synthetic data and prediction-powered inference, beating RAGAS with far fewer human annotations.
- [[ArxivLightRAG/summary]] — Builds an LLM-constructed knowledge graph with dual-level (specific-entity + broad-theme) retrieval and incremental graph updates, beating NaiveRAG/HyDE/RQ-RAG and most GraphRAG results at far lower token/API cost.
- [[ArxivRAGvsGraphRAG/summary]] — A controlled benchmark of RAG against four GraphRAG families finds neither wins outright: RAG excels at single-hop factual QA, GraphRAG at multi-hop reasoning, and combining both beats either alone.
- [[ArxivGraphRAGBench/summary]] — A 1,018-question, textbook-derived benchmark with expert rationales shows GraphRAG genuinely improves multi-hop reasoning, but the benefit is method- and domain-specific, not universal.
- [[ArxivSevenFailurePointsRAG/summary]] — From three real RAG deployments, catalogues seven recurring failure points (missing content, missed top-ranked docs, not in context, not extracted, wrong format, incorrect specificity, incomplete answers) and argues fixing them requires ongoing runtime calibration, not just better prompting.
- [[ArxivGraphRAGUnderFire/summary]] — GraphRAG resists conventional RAG poisoning, but a new attack, GRAGPOISON, poisons a single shared relation to corrupt every query depending on it, reaching up to 98.2% attack success with minimal poisoning text.
- [[ArxivGraphRAGLinkedInCustomerService/summary]] — LinkedIn built a knowledge graph over support tickets (intra-ticket structure plus inter-ticket similarity/clone links) for RAG-based QA, lifting MRR from 0.522 to 0.927 and cutting live median resolution time 28.6%.
