# Introducing Contextual Retrieval

**Paper:** [Introducing Contextual Retrieval (Daniel Ford et al., Anthropic, 2024)](https://www.anthropic.com/engineering/contextual-retrieval)

## Human Readable TL;DR

When AI systems need to look up information in large documents, they first chop those documents into small pieces -- like cutting a book into individual paragraphs. The problem is that each paragraph loses the context of what came before it, like reading a sentence that says "the company grew 3%" without knowing which company. Contextual Retrieval fixes this by adding a short explainer sentence to each piece before storing it -- like writing "This is about ACME Corp's Q2 2023 finances" at the top of that paragraph. This simple trick, combined with two different search methods and a re-ranking step, cuts retrieval failures by 67%.

## TL;DR

Contextual Retrieval addresses the context loss inherent in RAG chunking by using Claude to prepend chunk-specific explanatory context (50--100 tokens) before computing embeddings and BM25 indices. Combining Contextual Embeddings with Contextual BM25 reduces top-20-chunk retrieval failure rate by 49% (5.7% to 2.9%), and adding reranking achieves a 67% reduction (5.7% to 1.9%). Prompt caching makes the one-time contextualization cost just $1.02 per million document tokens.

---

## Problem & Motivation

Traditional RAG systems break documents into small chunks for embedding-based retrieval, but this chunking destroys context. A chunk stating "The company's revenue grew by 3% over the previous quarter" loses information about which company, which quarter, and what the baseline was. This context loss directly causes retrieval failures -- the system cannot match a user's query to the right chunk because the chunk itself is ambiguous. Standard BM25 (lexical) and embedding (semantic) retrieval methods both suffer from this problem, and simply combining them (hybrid search) does not resolve the underlying context gap.

---

## Main Original Ideas

1. **Contextual Embeddings** -- Uses Claude (specifically Claude 3 Haiku) to generate a short, chunk-specific context (50--100 tokens) that is prepended to each chunk before computing its embedding. The context situates the chunk within the full document, adding details like entity names, time periods, and document type that would otherwise be lost.

2. **Contextual BM25** -- Applies the same contextual prepending to chunks before building BM25 (lexical/TF-IDF) indices. This ensures that both semantic and lexical retrieval benefit from the restored context, improving exact-match queries (e.g., error codes, specific terms) alongside semantic similarity.

3. **Prompt-Cached Contextualization** -- Leverages Claude's prompt caching to make bulk contextualization cost-effective. The full document is cached once, then each chunk is contextualized against it without re-processing the entire document. This brings the cost down to $1.02 per million document tokens (assuming 800-token chunks, 8k-token documents).

4. **Stacked Retrieval Pipeline** -- Demonstrates that combining contextual embeddings + contextual BM25 + reranking yields compounding improvements, with each layer adding measurable gains on top of the previous one.

---

## Key Findings

| Retrieval Method | Failure Rate | Reduction vs Baseline |
|---|---|---|
| Baseline (embeddings only) | 5.7% | -- |
| Contextual Embeddings | 3.7% | **35%** |
| Contextual Embeddings + Contextual BM25 | 2.9% | **49%** |
| Contextual Embeddings + Contextual BM25 + Reranking | 1.9% | **67%** |

- Embeddings + BM25 (hybrid) consistently outperforms embeddings alone
- Voyage and Gemini Text 004 were the best-performing embedding models tested
- Top-20 chunk retrieval outperformed top-5 and top-10 configurations
- Contextual approaches improved performance across every embedding-source combination tested (codebases, fiction, ArXiv papers, science papers)
- Reranking (tested with Cohere reranker) adds latency but significantly improves precision
- For knowledge bases under 200,000 tokens (~500 pages), including the entire knowledge base in the prompt via prompt caching is simpler and eliminates the need for RAG entirely

---

## Suggestions & Future Directions

1. **Domain-specific contextualizer prompts** -- The generic prompt works well, but custom prompts tailored to specific domains (legal, medical, code) may yield further improvements.

2. **Chunk boundary optimization** -- Chunk size, boundary placement, and overlap all affect retrieval performance but were not deeply explored in this work.

3. **Alternative rerankers** -- Only Cohere's reranker was tested; Voyage and other reranking models may perform differently.

4. **Response generation evaluation** -- The post focuses on retrieval accuracy (recall@20) but notes that evaluating whether contextualized chunks improve final response quality is an important next step.

5. **Scaling considerations** -- The reranking step (retrieve 150, rerank to 20) introduces latency; optimizing this pipeline for real-time applications remains open.

---

## Authors & Institutions

Daniel Ford (research and writing), Orowa Sikder, Gautam Mittal, Kenneth Lien, Samuel Flamini, Lauren Polansky, Alex Albert, Susan Payne, Stuart Ritchie, Brad Abrams -- all at Anthropic.
