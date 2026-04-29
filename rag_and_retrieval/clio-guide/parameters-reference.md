> **Part of:** [[ClioApproachForDocumentSegmentation|CLIO Guide: Document Segmentation]] | **Paper:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|CLIO Paper Summary]]

## Summary of Key CLIO Parameters

| Parameter | CLIO Value | Your Adaptation |
|-----------|-----------|-----------------|
| Extraction model | Claude 3 Haiku | Any cheap model, or local |
| Extraction temperature | 0.2 | 0.2 |
| Description model | Claude 3.5 Sonnet | Any strong model |
| Description temperature | 1.0 | 1.0 |
| Embedding model | all-mpnet-base-v2 | Same, or bge-large |
| Embedding dims | 768 | 768 (or 1024 for bge) |
| Clustering | K-Means | Same |
| k heuristic | ~N/100 | Same |
| In-cluster samples | 50 | 50 (or fewer for small clusters) |
| Contrastive samples | 50 | 50 |
| UMAP n_neighbors | 15 | 15 |
| UMAP min_dist | 0.0 | 0.0 |
| UMAP metric | cosine | cosine |
| Hierarchy levels | 3 | 3 (for 1K+ base clusters) |
| Top-level target | ~10 | 8-15 depending on domain |
| Avg neighborhood size | 40 | 40 |
| Cost per 100K docs | $48.81 | $20-50 (API) or $4-15 (hybrid) |
