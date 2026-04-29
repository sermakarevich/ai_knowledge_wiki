# Practical Guide: Using the CLIO Approach for Large-Scale Document Segmentation

**Based on:** [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse|Clio: Privacy-Preserving Insights into Real-World AI Use]] ([arxiv](https://arxiv.org/abs/2412.13678))

**Your scenario:** Tens to hundreds of thousands of documents. No privacy constraints. Goal: automated topical segmentation, clustering, and hierarchical taxonomy generation.

---

## Pipeline Overview

```
Raw Documents
     |
     v
[KernSeg / LLM]  Split multi-topic docs  -->  Single-topic segments
     |
     v
[LLM] Facet Extraction  -->  Per-document summaries (1-2 sentences each)
     |
     v
[Sentence Transformer]  -->  768-dim embeddings of summaries
     |
     v
[K-Means]               -->  Base-level clusters (flat grouping)
     |
     v
[LLM] Cluster Naming    -->  Title + description per cluster (contrastive)
     |
     v
[LLM] Hierarchy Build   -->  Multi-level taxonomy (propose -> dedup -> assign -> rename)
     |
     v
[UMAP] Projection       -->  2D map for visual exploration
```

---

## Guide Sections

| #   | Section                                                                         | Description                                                                               |
| --- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1   | [[clio-guide/splitting-multi-topic-documents\|Splitting Multi-Topic Documents]] | KernSeg, LLM agentic, and hybrid approaches to split long docs into single-topic segments |
| 2   | [[clio-guide/document-preprocessing\|Document Preprocessing]]                   | Loading, normalizing, and truncating documents                                            |
| 3   | [[clio-guide/facet-extraction\|Facet Extraction via LLM]]                       | Per-document summaries + **Two-Pass Discovery & Enforcement** for categorical facets      |
| 4   | [[clio-guide/embedding\|Embedding]]                                             | Sentence transformer encoding (all-mpnet-base-v2, 768d)                                   |
| 5   | [[clio-guide/k-means-clustering\|K-Means Clustering]]                           | Base-level clustering with dynamic k, filtering, elbow method                             |
| 6   | [[clio-guide/cluster-description-generation\|Cluster Description Generation]]   | Contrastive prompting for cluster names and summaries                                     |
| 7   | [[clio-guide/hierarchy-building\|Hierarchy Building]]                           | Multi-level taxonomy: propose, dedup, assign, rename                                      |
| 8   | [[clio-guide/visualization\|2D Projection and Visualization]]                   | UMAP projection, Plotly scatter plots, tree view                                          |
| 9   | [[clio-guide/cost-estimation\|Cost Estimation]]                                 | Per-step cost breakdown at various scales                                                 |
| 10  | [[clio-guide/scaling-strategies\|Scaling Strategies]]                           | Batch APIs, async, local models, sampling                                                 |
| 11  | [[clio-guide/validation\|Validation and Quality Checks]]                        | Spot checks, cluster coherence, reconstruction tests                                      |
| 12  | [[clio-guide/reference-implementation\|Complete Reference Implementation]]      | End-to-end `clio_pipeline.py` script                                                      |
| 13  | [[clio-guide/parameters-reference\|Parameters Reference]]                       | All CLIO hyperparameters in one table                                                     |

---

## Quick Start

1. Install dependencies -- see [[clio-guide/facet-extraction\|Facet Extraction]] for full list
2. If docs are multi-topic, split them first -- [[clio-guide/splitting-multi-topic-documents\|Splitting]]
3. Run the pipeline end-to-end -- [[clio-guide/reference-implementation\|Reference Implementation]]
4. Check quality -- [[clio-guide/validation\|Validation]]

## Key Design Decisions

- **Topic summary** (free text) gets embedded and clustered -- naming variability is absorbed by cosine similarity
- **Categorical facets** (doc type, domain) require the [[clio-guide/facet-extraction#Categorical facets: The Two-Pass Discovery + Enforcement Pattern\|Two-Pass Discovery + Enforcement Pattern]] to avoid near-duplicate explosion
- **Contrastive cluster descriptions** -- showing in-cluster AND near-cluster-but-excluded samples produces specific, distinctive names. See [[clio-guide/cluster-description-generation\|Cluster Description]]
- **Hierarchy** is built bottom-up by iteratively re-embedding, re-clustering, and LLM-naming. See [[clio-guide/hierarchy-building\|Hierarchy Building]]
