> [[index|Wiki]]

**Paper:** [Graph Retrieval-Augmented Generation: A Survey (Peng et al., 2024)](https://arxiv.org/abs/2408.08921)

## The problem

Retrieval-Augmented Generation (RAG) — feeding an LLM extra text pulled from a document store — reduces hallucination, but it has three real-world weaknesses: it ignores relationships between entities (a citation network's links are invisible to plain text similarity), it stuffs long, redundant text into the prompt (the "lost in the middle" problem), and it can't see the "global" picture needed for summarization tasks. GraphRAG addresses all three by retrieving from a pre-built graph database (knowledge graph or similar) instead of flat text, pulling out nodes, triples, paths, or subgraphs that carry explicit relational structure.

## The framework

The survey formalizes GraphRAG as a three-stage pipeline, and organizes essentially the entire paper around it:

1. **Graph-Based Indexing (G-Indexing)** — obtain or build the graph (from open knowledge graphs like Wikidata/Freebase/DBpedia, domain KGs like CMeKG, or self-constructed graphs from documents/tables/tickets), then index it via graph structure, text conversion, vector embeddings, or a hybrid of these, which sets the granularity available to retrieval.
2. **Graph-Guided Retrieval (G-Retrieval)** — given a query, pull the most relevant graph elements. The design space spans retriever type (rule-based/non-parametric, language-model-based, GNN-based), retrieval paradigm (one-shot, iterative, multi-stage), and granularity (node, triplet, path, subgraph, or a hybrid mix), plus enhancement steps (query expansion/decomposition, and post-retrieval merging/pruning of the retrieved knowledge).
3. **Graph-Enhanced Generation (G-Generation)** — turn the retrieved graph into something a generator can consume (a GNN, a language model, or a hybrid of both), using either a "graph language" (edge tables, natural-language descriptions, code-like formats, syntax trees, node sequences) or graph embeddings, then optionally enhance generation before, during, or after the main generation step.

Each stage is analyzed along two further axes that cut across the whole survey: how components are trained (training-free with prompted LLMs, training-based with supervised fine-tuning, or jointly trained retriever+generator), and where GraphRAG gets used in practice.

## Key findings across chapters

- No single retriever type wins outright: non-parametric methods are fast but less accurate, while LM- and GNN-based retrievers are more accurate but expensive — leading to popular hybrids that use an LLM to plan and a graph algorithm to execute.
- Graph format matters a lot for generation quality: a good graph-to-text representation must be complete, concise (to avoid overloading context), and comprehensible to the LLM; the same subgraph can be rendered five different ways (edge table, natural language, code-like, syntax tree, node sequence).
- GraphRAG already supports a wide task set — KBQA, commonsense QA, entity linking, relation extraction, fact verification, link prediction, dialogue, recommendation — and real industrial systems exist (Microsoft GraphRAG, NebulaGraph, Antgroup's DB-GPT stack, Neo4j's NaLLM and LLM Graph Builder).
- Evaluation remains a weak point: most benchmarks are borrowed from generic QA/KBQA rather than purpose-built for GraphRAG, though newer benchmarks (STARK, GraphQA, GRBENCH, CRAG) are starting to fill the gap.

## Why it matters

As the first systematic survey of the field, this paper gives practitioners and researchers a common taxonomy and vocabulary for a rapidly proliferating set of techniques, and it's candid about the field's open problems: current methods mostly assume static, text-only, small-scale graphs, lack lossless ways to compress retrieved context, and have no standardized benchmark — all flagged as priorities for future work.
