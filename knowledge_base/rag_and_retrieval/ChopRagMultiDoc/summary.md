# CHOP: Chunkwise Context-Preserving Framework for RAG on Multi Documents

**Paper:** [CHOP: Chunkwise Context-Preserving Framework for RAG on Multi Documents (Park, Kim, Kim, Yoon, 2026)](https://arxiv.org/pdf/2604.15802)

## Human Readable TL;DR

Imagine a librarian filing pages from dozens of similar product manuals into one big folder. If two pages both talk about "the filter," the librarian can't tell which product they belong to and keeps pulling the wrong one. CHOP solves this by stamping every page with a small sticky note that says what product family, what part, and what model it's about — and it checks each new page to see if it still belongs to the same manual or if a new one just started. With those sticky notes attached, searching the folder becomes dramatically more accurate.

## TL;DR

CHOP is a context-preserving chunking framework for RAG that addresses retrieval confusion in corpora with near-duplicate documents. Each chunk is prefixed with a compact CNM signature (Category, Nouns, Model) produced by an LLM-based extractor, and a Continuity Decision Module decides whether consecutive chunks inherit the previous CNM or trigger re-extraction. On MRAMG-Bench product manuals, CHOP reaches a Top-1 Hit Rate of 90.77% versus 81.28% for fixed-length chunking and 70.77% for cosine chunking, with consistent gains in MRR, NDCG, and downstream generation metrics.

---

## Problem & Motivation

Standard RAG pipelines split documents into fixed-length chunks and embed them independently. This breaks down in multi-document corpora with high lexical overlap (e.g., product manuals, statutes, policy books) for three reasons:

- **Fragmented references:** Length-based segmentation severs coreference and local references ("this method", "Eq. (3)", "the filter"), so chunks lose the anchor that gives them meaning.
- **Semantic collisions:** When many documents describe similar things, their embeddings cluster together and the retriever cannot discriminate which manual a passage belongs to.
- **Discourse blindness:** Chunks are scored independently, ignoring definitions, coreference links, and topic transitions that span chunk boundaries.

The result is retrieval ambiguity, weak grounding, and hallucinations downstream. CHOP targets this gap by making each chunk carry context about the document it came from, without retraining the retriever.

---

## Main Original Ideas

1. **CNM-Extractor (Category–Noun–Model).** An LLM produces a compact triplet signature for each chunk — the broad product family, 1–2 key nouns (with the first constrained to the form `<category> <specific noun>`), and the specific model or series name. Output is strict JSON; absent fields are null. This signature is prefixed to the chunk before embedding, stabilizing the contextual frame and disambiguating references.

2. **Continuity Decision Module.** An LLM-based binary classifier over adjacent chunk pairs (C_i, C_{i+1}) that decides whether C_{i+1} continues the same document flow or starts a new one. If TRUE, the next chunk inherits the previous CNM; if FALSE, a fresh CNM is extracted. This keeps CNM piecewise constant across topically coherent spans and resets cleanly at boundaries, preventing label contamination.

3. **Context-aware prefixing as a retrieval fix without retraining.** Rather than changing the embedder, index, or similarity metric, CHOP regularizes the embedding space purely via prefix injection. This makes it a drop-in upgrade for existing RAG stacks and directly reduces embedding collisions among near-duplicate segments.

---

## Key Findings

**Retrieval performance on MRAMG-Bench (reconstructed single-file manuals):**

| Method | Top-1 Hit | Top-3 Hit | Top-3 MRR | Top-3 NDCG | Top-10 NDCG |
|---|---|---|---|---|---|
| Native-500T (fixed 500-token) | 0.8128 | 0.9103 | 0.8551 | 0.8656 | 0.8698 |
| Cosine-Chunking | 0.7077 | 0.8974 | 0.7944 | 0.8309 | 0.8389 |
| **CHOP** | **0.9077** | **0.9641** | **0.9325** | **0.9380** | **0.9291** |

**Generation performance (QA on retrieved evidence):**

| Method | Top-5 F1 | Top-5 ROUGE-L | Top-5 BERTScore | Top-10 F1 |
|---|---|---|---|---|
| Native-500T | 0.3792 | 0.3394 | 0.7338 | 0.4072 |
| Cosine-Chunking | 0.3351 | 0.2962 | 0.7206 | 0.3577 |
| **CHOP** | **0.3814** | **0.3412** | **0.7349** | **0.4080** |

- CHOP's advantage is largest at Top-1 (+9.5 points over Native-500T, +20 over Cosine) and persists in ranking metrics (MRR, NDCG) even as Hit Rates converge at higher K.
- Up to **+7.53% in NDCG@10** over baselines.
- Cosine-Chunking underperforms fixed chunking across the board, suggesting sentence-level topic segmentation alone is insufficient without contextual anchoring.
- Generation gains track retrieval gains — higher-quality evidence propagates into higher-quality answers — with K=5–10 identified as the practical operating sweet spot.

---

## Suggestions & Future Directions

1. **Adaptive prefixing.** Move beyond the fixed CNM triplet toward signatures that adapt to evolving domain knowledge.
2. **Dynamic continuity modeling.** Extend the Continuity Decision Module to handle streaming inputs where document boundaries are unknown ahead of time.
3. **Lightweight inference strategies.** Reduce the computational and latency cost of invoking an LLM for every chunk — a practical bottleneck since CHOP calls the LLM twice per chunk (extraction + continuity).

---

## Authors & Institutions

Hyunseok Park (HDC LABS), Jihyeon Kim (HDC LABS), Jongeun Kim (HDC LABS), Dongsik Yoon (HDC LABS, corresponding author) — Republic of Korea.
