# RAG & Retrieval

Research on **retrieval-augmented generation, chunking strategies, document segmentation, and knowledge catalogs**. Includes both retrieval-style approaches and alternative paradigms (filesystems, analytical search, skill compilation).

## Papers

- [[AnalyticalSearch/summary]] — Proposes "analytical search" beyond RAG: multi-document synthesis with verifiable, evidence-governed conclusions.
- [[BERAGBayesianEnsembleRAG/summary]] — Replaces concatenative RAG with per-document Bayesian ensemble inference; posterior weights updated token-by-token eliminate lost-in-the-middle bias; BEFT fine-tuning sets new KB-VQA state-of-the-art with 4.6× faster decoding at K=50.
- [[ChopRagMultiDoc/summary]] — CHOP prefixes each chunk with (Category, Nouns, Model) signature; Top-1 Hit Rate 81%→91%.
- [[ChromaFsVirtualFilesystem]] — Mintlify replaced RAG with a virtual filesystem over Chroma; 460x faster init, near-zero cost.
- [[ClioApproachForDocumentSegmentation]] — Practical pipeline: split→embed→cluster→hierarchy→visualize for large-scale document segmentation.
- [[ContextualRagImplementation/summary]] — Open-source implementation of Contextual Retrieval with Qwen3.5, BM25S, RRF, and reranking.
- [[ContextualRetrieval/summary]] — Prepending LLM-generated 50-100 token context to chunks; retrieval failure rate reduced 67%.
- [[Corpus2Skill/summary]] — Compiles a corpus into a hierarchical filesystem of SKILL.md files; +19% Token F1 over agentic RAG.
- [[EfficientRetrievalScalingHILL/summary]] — Jointly trains a hierarchical tree index with a retrieval model via residual quantization for fast beam-search; +2.57% ads gain at Meta at 3.9x vs. 24.6x infra cost.
- [[GoogleCloudKnowledgeCatalog/summary]] — Google's Knowledge Catalog: metadata aggregation + Gemini enrichment + sub-second hybrid search.
- [[GraphER/summary]] — Graph-based RAG reranking via structural, conceptual, and contextual proximity edges; GCS improved Perfect Recall@10 in all 18 tested configs at ~0.5s latency, no persistent KG required.
- [[OnTheoreticalLimitationsOfEmbeddingBasedRetrieval/summary]] — Proves single-vector embeddings have fundamental sign-rank capacity limits; introduces LIMIT benchmark (50k docs, dense qrel) where BM25 scores 93.6% but top dense retrievers collapse below 20% recall@100.
- [[QChunkerLearningQuestionAwareTextChunkingForDomainRagViaMultiAgentDebate]] / [[QChunker/summary]] — 4-agent debate framework for RAG chunking; distilled 3B models beat 14B baselines.
- [[RAGEvaluationTesting/summary]] — Production-ready RAG evaluation: component-wise metrics, offline/online alignment, LLM-judge calibration, regression testing, canary deployment, drift detection.
- [[RAGVisionSurvey/summary]] — Survey of RAG applied to computer vision across visual understanding, generation, and embodied AI; proposes unified taxonomy and identifies limitations (retrieval latency, modality misalignment) with future directions.
- [[SkillRAG/summary]] — Detects retrieval failure via hidden-state probing; routes to typed corrective skills (rewrite, decompose, focus, exit).
- [[UltRAG/summary]] — ULTRAG pairs an LLM query generator with a neural graph executor for zero-shot KG-RAG, achieving SOTA on KGQA benchmarks with 19–167x lower latency and scaling to Wikidata (116M entities).
- [[UnsupervisedTextSegmentationViaKernelChangePointDetectionOnSentenceEmbeddings]] — Training-free text segmentation via kernel change-point detection; matches supervised methods.
- [[WhenToRetrieveDuringReasoning/summary]] — Adaptive retrieval framework for chain-of-thought reasoning models; uncertainty detector + RL policy cuts retrieval calls ~50% while improving answer F1 by 10.1 pp.
- [[clio-guide]] — Implementation guide files (preprocessing, embedding, clustering) for a CLIO-style segmentation pipeline.
