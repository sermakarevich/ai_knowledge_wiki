**Figure 8 — Discovered math retrieval harness.** This is not a quantitative plot but a directed pipeline diagram (a small DAG with no axes), so "trends" read as the flow of control. The structure is a three‑stage fan‑out/fan‑in:

- **Stage 1 (top):** a single *Query* node.
- **Stage 2 (router):** the query passes to a *Lexical router* that classifies it using keyword and regular‑expression cues, then branches into exactly **four** subject‑specific retrieval policies (each a leaf policy box):
  - *Combinatorics* — BM25 with a top‑~20 candidate set, deduplicated to ~8, then reranked, keeping ~3.
  - *Geometry* — a fixed small set (about one fixed reference plus ~2 BM25 hits), no reranking.
  - *Number theory* — BM25 top‑~12, reranked, keeping ~3.
  - *Algebra/Other* — BM25 top‑~10, reranked, with an adaptive (query‑dependent) keep count.
- **Stage 3 (bottom):** all four policy outputs converge on a single *Build final prompt* node, into which the retrieved examples are inserted.

**Takeaway:** the harness replaces a one‑size‑fits‑all retriever with a router that, on lexical signals, dispatches each query to a tailored retrieval policy (different candidate pool sizes, dedup, and reranking/keep decisions per math subject), and then composes the selected examples into the final prompt. In short, it is a subject‑conditional retrieval‑then‑prompting pipeline rather than a single uniform retrieval step. (Numeric parameters such as the ~20/~12/~10 pool sizes and ~3 kept examples should be treated as approximate.)