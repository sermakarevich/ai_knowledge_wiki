> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Evaluation Framework

**In one sentence:** Because existing GraphRAG studies for text use bespoke datasets, construction heuristics, and evaluation protocols, this paper runs a controlled benchmark of standard RAG against four representative GraphRAG families on QA and query-based summarization under a unified protocol, finding that RAG and GraphRAG are complementary rather than competing, that GraphRAG design choices and even the evaluation protocol itself change conclusions, and that combining them via Selection or Integration yields consistent gains.

## Key points

- **Complementarity, not a winner:** RAG is stronger on single-hop, detail-oriented factual QA; GraphRAG is stronger on multi-hop, reasoning-intensive QA, and produces more corpus-level, diverse summaries for broad summarization.
- **Design choices matter inside GraphRAG:** community-based Global Search trades query-specific details (hurting detail-oriented QA) for corpus-level aggregation (helping broad/diverse summarization output).
- **Evaluation protocol can flip conclusions:** LLM-as-a-Judge scoring of summaries is highly sensitive to the presentation order of candidate summaries — a strong position effect that can confound RAG-vs-GraphRAG comparisons.
- **GraphRAG is not free:** it incurs higher construction cost, retrieval latency, and storage footprint, and performance is sensitive to the quality (and cost) of the graph-construction model (graphs here are built with GPT-4o-mini; GPT-4o results in Appendix L).
- **Hybrid strategies work:** Selection routes queries to RAG or GraphRAG by query type (efficiency-oriented); Integration combines evidence from both paradigms (performance-oriented); both yield consistent improvements across benchmarks.
- **Four GraphRAG families benchmarked:** KG-based (LlamaIndex KG-GraphRAG), community-based (Edge et al.'s Microsoft GraphRAG), text-centric graph-guided (HippoRAG2), and hierarchical summary-based (RAPTOR).
- **Fair-comparison protocol:** retrieval is decoupled from generation — retrieved evidence is saved per method, then a single unified generation script produces all outputs; core settings (256-token chunks, ada-002 embeddings, top-k=10, BAAI/bge-reranker-large reranker, IRCoT for iterative retrieval, Llama-3.1-8B/70B-Instruct generators) are standardized across methods.
- **Tasks and settings covered:** QA in single-hop and multi-hop settings; query-based summarization in single-document (retrieval restricted to that document) and multi-document (retrieval over an index of all documents) scenarios.

---

## Section 1 — Introduction

RAG improves LLMs by retrieving relevant knowledge from external sources and has been deployed in healthcare, law, finance, and education; with LLMs, retrieval further improves faithfulness, mitigates hallucinations, and enhances robustness. Most existing RAG systems retrieve over text corpora. Graphs offer explicit relational structure (knowledge representation, social networks, biomedical discovery, KGs, molecular graphs); an emerging line of work extends GraphRAG to text by constructing graphs from unstructured documents, with reported benefits for global summarization, planning, and reasoning.

**Gap:** most text-GraphRAG studies run under task- and system-specific settings — bespoke datasets, graph-construction heuristics, evaluation protocols — making it hard to draw principled conclusions about *when and why* explicit graph structures help (or hurt), and obscuring practical trade-offs: construction cost, retrieval latency, storage footprint.

**Approach.** A controlled, systematic benchmark of RAG and GraphRAG on widely used text-based tasks: *Question Answering* (QA, single- and multi-hop) and *Query-based Summarization* (single- and multi-document), across four representative GraphRAG categories:

1. **KG-based GraphRAG** — extract a KG from text, retrieve over the KG.
2. **Community-based GraphRAG** — retrieval over community structures and hierarchical abstractions.
3. **Text-centric graph-guided RAG** — retrieve original text chunks with the assistance of a constructed knowledge graph.
4. **Hierarchical summary-based GraphRAG** — hierarchical summaries for multi-granular retrieval without explicit KGs.

A unified evaluation protocol standardizes data preprocessing, retrieval, and generation settings for fair, reproducible cross-paradigm comparison.

**Key findings (four):**

1. RAG and GraphRAG exhibit **complementary behaviors rather than a consistent winner**: RAG — single-hop/detail-oriented factual QA; GraphRAG — multi-hop, reasoning-intensive QA.
2. **GraphRAG design choices matter**: community-based global search can sacrifice query-specific details (hurting detail-oriented QA) while providing corpus-level aggregation (benefiting broad or diverse summarization).
3. **Evaluation protocol can change conclusions**: LLM-as-a-Judge for summarization is highly sensitive to presentation order of candidate summaries (position effects that may confound comparisons).
4. **GraphRAG is not free**: higher construction cost, retrieval latency, storage footprint; performance sensitive to quality (and cost) of graph construction.

**Motivated follow-up — two practical hybrid strategies:**

- **Selection** — route queries to RAG or GraphRAG based on query type, for efficiency.
- **Integration** — combine evidence from both paradigms to maximize performance.

Both yield consistent performance improvements across benchmarks.

**Contributions:**

1. **Systematic Benchmark** — controlled comparison of RAG and multiple GraphRAG variants across QA and query-based summarization under a unified protocol (consistent preprocessing, retrieval, generation) for fair, reproducible comparison.
2. **Strong, Task-Level Findings** — clear complementarities: RAG stronger for factual/detail-oriented QA; GraphRAG benefits reasoning-intensive QA and produces more corpus-level, diverse summaries; outcomes strongly affected by GraphRAG design choices (e.g., local vs. global search).
3. **Hybrid Strategies** — Selection and Integration combine RAG and GraphRAG, achieving consistent improvements and illustrating effectiveness–efficiency trade-offs.
4. **Evaluation and Efficiency Analyses** — failure modes; construction/retrieval/storage costs; sensitivity to graph-construction quality; strong position effects in LLM-as-a-Judge summarization evaluation; practical considerations for reliable (Graph)RAG assessment.

## Section 2 — Related Works

### 2.1 Retrieval-Augmented Generation

- RAG enhances LLMs by retrieving external information: addresses restricted context windows, improves factuality, mitigates hallucinations.
- Most RAG systems process text corpora by splitting documents into chunks; queries retrieve relevant chunks via lexical search or semantic similarity search.
- Beyond vanilla retrieval: pre-retrieval processing, post-retrieval processing, and fine-tuning strategies improve effectiveness on QA, dialogue generation, and summarization.
- Many systems employ reranking and iterative retrieval to refine evidence selection under a fixed context budget.
- Several studies benchmark RAG pipelines and evaluation tools across tasks and domains; however, none provide a controlled comparison between standard RAG and GraphRAG under unified settings on widely used text benchmarks.

### 2.2 Graph Retrieval-Augmented Generation

- Real-world graph-structured data: knowledge graphs, social graphs, molecular graphs. GraphRAG exploits relational signals among connected nodes.
- Early work: retrieval over existing KGs for KG-based QA and fact checking.
- Graph structures can benefit text-centric retrieval, e.g., hyperlink graphs between documents improving QA retrieval.
- Recent directions for constructing graphs from text:
  - **Document-/chunk-level graphs** guiding retrieval over textual units.
  - **Entity–relation graphs** from documents (often with LLM assistance), retrieved at multiple abstraction levels — local neighborhoods or community-level summaries.
  - **Graph-inspired structures without full entity–relation semantics:** RAPTOR — hierarchical summary structures for multi-granular retrieval; HippoRAG and extensions — entity-linked graphs guiding chunk retrieval.
- **Uncharacterized trade-offs:** GraphRAG systems for text are evaluated under heterogeneous protocols (varying construction methods, retrieval configurations, evaluation criteria); graph construction adds costs (indexing time, retrieval latency, storage footprint) and is sensitive to construction-model quality — yet these costs are not consistently characterized across studies. How GraphRAG compares with standard RAG on general text benchmarks, and at what practical cost, remains unclear.

## Section 3 — Evaluation Framework

Fair comparison principle: RAG and GraphRAG are evaluated under identical settings whenever applicable; otherwise each method's default configuration is used while matching key budgets. **Retrieval is decoupled from generation:** retrieved evidence is first saved per method, then a unified generation script produces all outputs conditioned on the saved retrieval results.

### 3.1 RAG Pipeline

Standard dense-retrieval RAG:

1. Segment corpus documents into textual chunks.
2. Build an index by embedding each chunk into a shared vector space.
3. At inference: embed the query, retrieve top-ranked chunks by similarity.

### 3.2 GraphRAG Implementations

Four representative classes, one representative implementation each:

| Class | Representative | How the structure is used |
|---|---|---|
| KG-based | LlamaIndex KG-GraphRAG | KG constructed from text; query entities aligned to nodes; retrieval traverses multi-hop neighborhoods collecting relational triplets *(head, relation, tail)* |
| Community-based | Edge et al. (Microsoft GraphRAG) | KG organized into hierarchical communities via graph clustering; each community has a textual summary/report — lower-level = fine-grained, higher-level = more abstract |
| Text-centric graph-guided | HippoRAG2 | Original text chunks remain the primary retrieval units; an entity-linked graph over chunks guides scoring/traversal — query-relevant entities retrieved first, then their connected chunks |
| Hierarchical summary-based | RAPTOR | Multi-level hierarchical structure; recursively clusters text chunks and generates summaries at each level — coarse-to-fine, multi-granular retrieval without explicit KGs |

Variants evaluated:

- **KG-GraphRAG (Triplets)** — retrieves only triplets.
- **KG-GraphRAG (Triplets+Text)** — retrieves triplets plus their associated source text.
- **Community-GraphRAG (Local)** — *Local Search*: entity neighborhoods and lower-level community reports via entity matching.
- **Community-GraphRAG (Global)** — *Global Search*: high-level community summaries by semantic similarity.

### 3.3 Tasks

Two tasks, each in two granularities:

- **Question Answering** — single-hop and multi-hop.
- **Query-based Summarization** — single-document and multi-document.

Retrieval scope: for **single-document** tasks, retrieval is restricted to the corresponding document; for **multi-document** tasks, retrieval is performed over an index constructed from all documents.

### 3.4 Unified Experimental Settings

Standardized core settings for fair comparison:

| Setting | Value |
|---|---|
| Graph construction model | GPT-4o-mini for KG-GraphRAG, Community-GraphRAG, HippoRAG2 (GPT-4o results in Appendix L) |
| Chunking | ~256 tokens per chunk, all methods |
| Embedding model | OpenAI `text-embedding-ada-002`; queries, chunks, and graph information in a shared vector space |
| Retrieval budget | top-*k* by semantic similarity, *k* = 10 by default |
| Reranking | BAAI/bge-reranker-large cross-encoder reranker — applied to final top-*k* evidence units for all methods supporting reranking |
| Iterative retrieval | IRCoT (retrieval interleaved with intermediate reasoning steps), when enabled |
| Generation backbones | Llama-3.1-8B-Instruct and Llama-3.1-70B-Instruct (two open-source instruction-tuned LLMs of different sizes, to control for generation capacity) |

**Covers:** Sections 1-3 (Introduction, Related Works, Evaluation Framework)
