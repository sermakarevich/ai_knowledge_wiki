# How To Implement Contextual RAG From Anthropic

**Source:** [How To Implement Contextual RAG From Anthropic (Together AI, 2024)](https://docs.together.ai/docs/how-to-implement-contextual-rag-from-anthropic)
**See also:** [[../ContextualRetrieval/summary|Contextual Retrieval -- Original Anthropic Paper]]

## Human Readable TL;DR

Imagine you have a book and you need to help people find answers in it quickly. You cut the book into small cards, but each card loses the "big picture" -- like reading "sales grew 3%" without knowing which company. This guide shows how to fix that: before filing each card, you ask a small AI to write a one-line summary on it explaining what it's about. Then you use two different search methods (one looks for exact keywords, the other understands meaning), merge their results, and let a judge pick the best matches. The whole thing runs locally with free open-source models -- no paid API keys needed for the AI part.

## TL;DR

A line-by-line open-source implementation of Anthropic's Contextual Retrieval using Together AI's inference stack. Each chunk is prepended with LLM-generated context (Qwen3.5-9B), embedded with multilingual-e5-large-instruct for dense retrieval, indexed with BM25S for sparse retrieval, fused via Reciprocal Rank Fusion, reranked with Mxbai-Rerank-Large-V2, and passed to a large LLM (gpt-oss-120b) for final generation. Demonstrates prompt caching feasibility for bulk chunk contextualization.

---

## Problem & Motivation

Standard RAG systems chunk documents into small pieces for retrieval, but chunking strips away the surrounding context that makes each piece meaningful. A chunk saying "the company grew 3%" is useless without knowing which company or time period. Anthropic's Contextual Retrieval paper proposed fixing this by prepending LLM-generated context to each chunk before indexing. This Together AI guide provides a concrete, runnable, open-source implementation of that idea using their hosted model endpoints.

---

## Main Original Ideas

1. **Context-Augmented Chunks via Small LLM** -- Each chunk is sent to a cost-effective model (Qwen3.5-9B) alongside the full document. The model generates a succinct explanation of the chunk's meaning in context, which is prepended to the chunk before indexing. Prompt caching makes this feasible at scale.

2. **Hybrid Search (Dense + Sparse)** -- Chunks are indexed in two parallel systems: a dense vector index (multilingual-e5-large-instruct embeddings) for semantic similarity, and a BM25 keyword index for exact lexical matching.

3. **Reciprocal Rank Fusion (RRF)** -- Results from both retrieval systems are combined using RRF (K=60), which assigns scores based on reciprocal rank positions across lists, avoiding the need to normalize different scoring scales.

4. **Reranking for Precision** -- The fused top candidates pass through a dedicated reranker (Mxbai-Rerank-Large-V2) to surface the most semantically relevant chunks before final generation.

5. **Five-Stage Pipeline** -- The complete flow: chunk augmentation --> dual-index creation --> hybrid retrieval --> rank fusion --> reranking --> LLM generation.

---

## Implementation Details

### Models Used

| Role | Model | Notes |
|---|---|---|
| Context generation | Qwen/Qwen3.5-9B | Small, fast, cost-effective for bulk contextualization |
| Embedding | intfloat/multilingual-e5-large-instruct | Dense vector representations |
| Sparse retrieval | BM25S (library) | Keyword-based lexical search |
| Reranking | mixedbread-ai/Mxbai-Rerank-Large-V2 | Requires Together AI Dedicated Endpoint |
| Final generation | openai/gpt-oss-120b | Large model for answer synthesis |

### Chunking Strategy

- Naive fixed-size chunking: 250 characters with 30-character overlap
- Rationale: context generation compensates for naive boundaries

### Context Generation Prompt

```
Given the document below, we want to explain what the chunk captures in the document.
{WHOLE_DOCUMENT}
Here is the chunk we want to explain:
{CHUNK_CONTENT}
Answer ONLY with a succinct explanation of the meaning of the chunk in the context of the whole document above.
```

### Retrieval Pipeline

1. **Vector retrieval** -- Embed query, compute cosine similarity against chunk embeddings, return top-k
2. **BM25 retrieval** -- Tokenize query, retrieve top-k from BM25 index
3. **RRF fusion** -- Merge both ranked lists using `score = Σ 1/(rank + K)` where K=60
4. **Rerank** -- Pass fused candidates to reranker, select top-n (e.g., 3)
5. **Generate** -- Feed reranked chunks + query to large LLM

### Dependencies

```
together        # LLM inference, embeddings, reranking
tiktoken        # Token counting
beautifulsoup4  # Web scraping (demo data)
bm25s           # BM25 sparse retrieval
numpy           # Cosine similarity
```

---

## Key Findings

- The guide demonstrates the full pipeline on Paul Graham's "Founder Mode" essay as a test document
- Context-augmented chunks contain richer information for both semantic and keyword search
- RRF effectively merges results from fundamentally different scoring systems without normalization
- The reranker significantly improves precision by filtering the fused candidate set
- Small models (3B--9B parameters) are sufficient for chunk contextualization

---

## Suggestions & Future Directions

1. **Prompt caching** -- The guide notes that caching the full document's key/value matrices across chunk-level LLM calls is critical for cost-effective contextualization at scale
2. **Model flexibility** -- The pipeline is model-agnostic; any embedding, reranking, or generation model can be swapped in
3. **Chunk strategy tuning** -- The naive 250-char fixed chunking is a starting point; semantic or recursive chunking could improve results
4. **Dedicated endpoints** -- The reranker (Mxbai) requires a Together AI Dedicated Endpoint, adding cost/complexity

---

## Authors & Institutions

Together AI (no individual authors credited). Implementation based on Anthropic's Contextual Retrieval research by Daniel Ford et al.
