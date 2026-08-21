# GraphRAG

Graph-based retrieval-augmented generation: building knowledge graphs from documents and retrieving from graph structure (entities, relations, communities) instead of — or alongside — flat text chunks. Covers canonical systems (Microsoft GraphRAG, HippoRAG, LightRAG), measured retrieval quality (recall@k, MRR, golden multi-hop datasets, LLM-as-judge), and failure modes (ranking drift, hallucination amplification, stale graphs, missing provenance).

Curated source list: [[GraphRAGTop10Materials/index|GraphRAG Top 10 Materials]].

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
- [[ArxivGraphReasoningAgentGRA/summary]] — GRA gives an LLM agent seven unix-style tools to navigate a hybrid knowledge graph like a codebase, beating full-context schema serialization on a 258-question industrial benchmark while reading a third of the tokens.
- [[ArxivGraphScout/summary]] — GraphScout trains a small LLM with flexible code-query and fuzzy-search tools to explore knowledge graphs like an experienced detective, beating much larger models while using far fewer tokens.
- [[ArxivWhyNeighborhoodsMatter/summary]] — Graph-ablation studies on agentic GraphRAG show cited entities are necessary but not sufficient — visited-but-uncited neighborhoods still measurably shape the final answer.
- [[ArxivAgentGL/summary]] — AgentGL trains an LLM agent via a two-stage RL curriculum to navigate native text-attributed graphs with four search tools, beating GNNs, GraphLLMs, GraphRAG, and agentic search baselines on node classification and link prediction.
- [[ArxivPathRouter/summary]] — PathRouter scores agentic GraphRAG trajectories on both answer correctness and evidence-path overlap, routing GRPO rewards and selective teacher distillation accordingly, beating Graph-R1 at every scale with far better out-of-distribution transfer.
- [[ArxivPersonalAI20/summary]] — PAI-2 lets an LLM plan and adapt its knowledge-graph search step by step for personalized agents, beating LightRAG, RAPTOR, and HippoRAG 2 on multi-hop QA benchmarks.
- [[ArxivSodaMem/summary]] — SodaMem builds an evidence-grounded temporal knowledge graph with provenance-tagged facts and a planner-reader retrieval loop, hitting 92.8% on LongMemEval-S at roughly a sixth of a cent per question.
- [[ArxivHiGram/summary]] — HiGram organizes agent memory as a hierarchical graph with localized MicroGraphs and single-path evidence selection, enabling cheap retrieval and targeted rewrite with dependency re-validation, topping LoCoMo and MemConflict at ~7.2% of full-context token usage.
- [[ArxivSAGEGraphMemory/summary]] — SAGE trains a policy-based graph writer and a structure-aware GFM reader in alternating RL rounds, reaching strong zero-shot multi-hop retrieval transfer though it still trails purpose-built long-term-memory systems on specialized benchmarks.
- [[ArxivMemGraphRAG/summary]] — MemGraphRAG fixes GraphRAG's isolated chunk-level extraction with a persistent Three-Layer Global Memory and a three-agent society (Extraction, Conflict Detection, Resolution), achieving the best average accuracy and lowest retrieval latency across five benchmarks.
- [[ArxivGraphPlanner/summary]] — GraphPlanner routes multi-agent LLM workflows via a graph-memory-augmented RL policy that jointly picks role and backbone LLM at each step, beating single- and multi-round routers while generalizing to unseen tasks and models.

## Collections
- [[GraphRAGTop10Materials/index]] — curated top-10 foundational materials (papers, benchmarks, frameworks, production write-ups), 2026-08-20.
- [[AgenticGraphRAGRecentScan/index]] — agentic GraphRAG scan, last 6 months (Feb–Aug 2026): agents traversing KGs, temporal graph memory, RL-trained traversal, multi-agent shared graphs.
