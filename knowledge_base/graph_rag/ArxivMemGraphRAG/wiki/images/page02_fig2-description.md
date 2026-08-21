**Figure 2 — Technical Summary**

The figure contains two panels that together diagnose *why* graph‑augmented RAG underperforms and *why* a common fix (filtering triples) fails.

**Left panel — Relevance vs. Recall (bubble chart).**
- *Axes:* X = Recall (%) (~20–85), the fraction of needed evidence that is actually retrieved; Y = Relevance (%) (~20–80), how much of the retrieved context is pertinent to the query.
- *Encoding:* bubble diameter ∝ LLM‑ACC (generation accuracy, ~50‑scale).
- *Points (approx. values as labeled):* Vanilla RAG ≈ (Recall 74, Relevance 63); GraphRAG ≈ (44, 47); GrNIRAG ≈ (65, 38); a fourth GraphRAG‑style point sits low on relevance.
- *Trend/takeaway:* graph‑based systems sit at the *low‑recall, low‑relevance* corner relative to vanilla RAG — they retrieve less of the needed evidence *and* less relevant context, confirming the "thematic irrelevance / logical inconsistency / fragmentation" problem rather than a simple recall win.

**Right panel — Effect of triple filtering (dual‑axis bar + line).**
- *Axes:* X = Filter Rate (0, 20, 40, 60, 80); left Y = LLM‑ACC (~40–70); right Y = Triple Number (~5k–15k).
- *Series:* blue bars = number of remaining triples; red line = LLM‑ACC.
- *Trend:* both decline monotonically as the filter rate rises. The triple count falls from its maximum at 0% filter to its minimum at 80%, and LLM‑ACC drops from roughly the mid‑60s down to about the low‑50s.
- *Takeaway:* aggressively removing "irrelevant" (schema‑frequency) triples does **not** improve generation accuracy — it correlates with *lower* LLM‑ACC. So naive graph‑quality filtering is counterproductive.

**Overall message:** GraphRAG‑style pipelines lose both recall and relevance versus vanilla RAG, and the intuitive remedy of pruning triples to raise graph quality actually hurts final accuracy. This motivates the paper's alternative — enforcing *global* consistency (the shared memory in MemGraphRAG) instead of local triple filtering.