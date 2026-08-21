**Figure 2 — Cost Comparison (GraphRAG vs. LightRAG), Legal Dataset**

*What it shows:* Despite the "Figure" label, this is a compact tabular comparison (not a plotted chart) of computational cost, broken down by **phase** (Retrieval Phase vs. Incremental Text Update) and by **cost type** (Tokens consumed vs. API Calls made), for the baseline GraphRAG versus the proposed LightRAG ("Ours"). So the "axes" are the two comparison dimensions: rows = metric (Tokens, API Calls), column groups = phase, and within each phase a GraphRAG column against a LightRAG column.

*Approximate values / trends:*
- **Retrieval phase – Tokens:** GraphRAG on the order of ~6 × 10⁵ tokens (≈610 communities × ~1,000 tokens each), whereas LightRAG is roughly ~10² or less. That is, LightRAG uses ~three to four orders of magnitude fewer tokens.
- **Retrieval phase – API Calls:** GraphRAG on the order of hundreds of calls (≈610,000 / C_max), versus a single call for LightRAG.
- **Incremental text update – Tokens:** GraphRAG scales to ~10⁷‑scale (≈1,399 × 2 × 5,000 plus extraction overhead T_extract), while LightRAG's cost is just the extraction term T_extract.
- **Incremental update – API Calls:** GraphRAG ~thousands (≈1,399 × 2 plus C_extract), versus C_extract for LightRAG.

The consistent trend across every cell is that the LightRAG column is at or near zero/one while the GraphRAG column grows with the number of communities and report size.

*Takeaway:* LightRAG is dramatically more cost‑efficient than GraphRAG in both token consumption and API‑call overhead, in retrieval and when the corpus changes. This efficiency comes from its retrieval mechanism—using very few tokens for keyword generation/retrieval and a single API call—rather than traversing each community report individually as GraphRAG does, making it far more practical for dynamic, large‑scale knowledge bases.