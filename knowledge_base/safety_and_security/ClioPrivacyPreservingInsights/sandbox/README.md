> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

# Clio: Privacy-Preserving Insights -- Code Sandbox

Minimal implementation of core ideas from the paper using LangGraph + Ollama.

## What This Implements

- **Facet Extraction:** LLM extracts PII-free topic summaries from conversations (Section 3.1)
- **Semantic Clustering:** Groups similar conversations using TF-IDF + KMeans (Section 3.2)
- **Cluster Description:** LLM generates privacy-preserving cluster titles (Section 3.3)
- **Privacy Auditing:** LLM checks cluster descriptions for PII leakage (Section 3.4)
- **Hierarchy Building:** LLM groups clusters into higher-level categories (Section 3.4)

## What This Does NOT Implement

- Real embedding models (uses TF-IDF as a simple proxy)
- UMAP visualization / interactive map view
- Temporal analysis and faceted breakdowns
- Production-scale clustering with dynamic k selection
- The full 4-layer defense-in-depth privacy architecture
- Concern scoring and safety classifier integration

## Prerequisites

1. Install [Ollama](https://ollama.ai) and pull a model:
   ```bash
   ollama pull llama3.2
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Run

```bash
uv run python run.py
```

## Graph Topology

```
[conversations] -> extract_facets -> cluster_conversations -> describe_clusters -> audit_privacy -> build_hierarchy -> generate_report -> [final_report]
```
