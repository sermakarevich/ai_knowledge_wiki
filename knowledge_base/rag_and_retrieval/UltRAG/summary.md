# UltRAG: a Universal Simple Scalable Recipe for Knowledge Graph RAG

**Paper:** [UltRAG: a Universal Simple Scalable Recipe for Knowledge Graph RAG (Georgiev et al., 2026)](https://arxiv.org/abs/2603.28773)

## Human Readable TL;DR

Imagine a fact-checker who can look things up in a massive, interconnected encyclopedia with billions of entries. AI assistants often make things up because they can't reliably search these huge encyclopedias. This paper builds a "lookup assistant" (ULTRAG) that pairs an AI writer with a specialized lookup engine -- the writer says "find me everything connected to X via these relationships," and a purpose-built graph-search tool does the retrieval accurately. The result is a fact-checker that's both more accurate than previous systems AND much faster (up to 167x), even on encyclopedias with 116 million entries.

## TL;DR

ULTRAG is a modular KG-RAG framework that routes LLM-generated structured queries to neural query executors (ULTRAQUERY) instead of symbolic or text-retrieval engines. By pairing any off-the-shelf LLM with a pre-trained neural graph query executor -- without retraining either -- ULTRAG-OTS achieves zero-shot state-of-the-art on inductive KGQA benchmarks, outperforms fine-tuned transductive baselines, and scales to Wikidata (116M entities, 1.6B triples) at 19--167x lower latency than competing KG-RAG approaches.

---

## Problem & Motivation

LLMs hallucinate -- they generate confident but factually wrong content. RAG over document corpora is well-established, but adapting RAG to Knowledge Graphs (KGs) is non-trivial: multi-hop reasoning requires executing structured graph queries, not just retrieving passages. Existing KG-RAG methods either fail on complex queries (agent/path-based approaches) or don't scale beyond small benchmark graphs (GNN-based or symbolic query approaches). No prior method has been demonstrated end-to-end on Wikidata-scale KGs (116M entities).

---

## Main Original Ideas

1. **Neural Query Execution as LLM Tool** -- Instead of giving the LLM raw graph access or forcing it to do symbolic query execution, ULTRAG wraps a pre-trained neural query executor (ULTRAQUERY) as a callable tool. The LLM generates a structured query; the neural executor fuzzy-executes it over the KG. This separation is key: the neural executor tolerates both LLM-generated query noise and KG incompleteness -- two failure modes that break symbolic executors.

2. **ULTRAG Framework (Algorithm 1)** -- A general plug-and-play recipe: (a) LLM generates a query φ in a custom DSL, (b) entity linker L maps text mentions to KG entities via embedding similarity, (c) neural executor X runs the query, returning fuzzy membership scores over all entities, (d) arbitrator LLM ranks and produces the final answer. The loop can iterate (sufficiency check D), though ULTRAG-OTS uses a single pass.

3. **Custom DSL for Stable Query Generation** -- ULTRAG-OTS replaces the nested BetaE tuple format with a flat infix DSL (`entity -> P31` for projection, `AND(q1, q2)` for intersection). This reduces LLM-generated invalid query rates from 15--30% to under 1%, directly improving end-to-end accuracy.

4. **SEPPR (Seed Entity Personalized PageRank)** -- To handle Wikidata-scale graphs on a single GPU, SEPPR runs 5 steps of personalized PageRank from seed entities (damping α = 0.85), extracts the top-30,000 nodes, and caps edges at 500,000. This makes ULTRAQUERY operate on a tractable local subgraph without sacrificing answer recall.

5. **Prompt Caching for Cost Efficiency** -- Because KG relation type lists are static per graph, they can be cached in the LLM prompt. ULTRAG-OTS achieves 94--96% cache hit rates, keeping API costs comparable to baselines (within 23--27% overhead) despite using 25--62x more input tokens.

---

## Key Findings

### ULTRAG-OTS vs Baselines -- Question-Specific Subgraphs

| Model | GTSQA Hits | GTSQA F1 | KGQAGen Hits | KGQAGen F1 |
|---|---|---|---|---|
| SubgraphRAG (200) | 84.34 | 81.62 | 89.76 | 86.28 |
| GNN-RAG | 76.76 | 74.90 | 82.56 | 78.92 |
| RoG | 76.51 | 73.99 | 88.43 | 84.92 |
| **ULTRAG-OTS** | **92.66** | **89.29** | **92.04** | **88.82** |

**+8.32% Hits / +8.03% F1** over the best baseline (SubgraphRAG) on GTSQA.

### Wikidata Scale (PPR subgraphs, ground-truth seeds)

| Model | GTSQA Hits | GTSQA F1 |
|---|---|---|
| SubgraphRAG (200) | 63.29 | 59.56 |
| RoG | 62.55 | 58.93 |
| **ULTRAG-OTS** | **86.74** | **82.08** |

### Neural vs Symbolic Executor Gains (WikiKG2)

| Metric | Avg. Improvement |
|---|---|
| MRR | +18.58% |
| Hit@1 | +15.40% |
| Hit@3 | +21.14% |
| Hit@10 | +24.09% |

Gains grow with query complexity: 3-hop MRR gain is +31.52%.

### Efficiency (GTSQA, WikiKG2, ground-truth seeds)

| Model | Non-API Time (s) | API Cost | Cache Hit % |
|---|---|---|---|
| SubgraphRAG (200) | 16.7 ± 3.8 | $0.012 | 0% |
| GNN-RAG | 9.9 ± 2.3 | $0.012 | 0% |
| RoG | 1.9 ± 0.5 | $0.011 | 0% |
| **ULTRAG-OTS** | **0.10 ± 0.0** | $0.014 | 93.77% |

**167x faster** than SubgraphRAG, **99x faster** than GNN-RAG, **19x faster** than RoG.

### Multi-LLM Flexibility (GTSQA, Wikidata)

| Config | Hits | F1 | Cost |
|---|---|---|---|
| GPT-5 × 2 | 86.74 | 82.08 | $0.017 |
| GPT-5 → GPT-5-mini | 82.37 | 78.41 | $0.009 |
| GPT-5-mini × 2 | 75.71 | 71.60 | $0.004 |
| DeepSeek-reasoner × 2 | 75.77 | 72.05 | $0.005 |

Cheapest config (GPT-5-mini × 2) still beats most baselines at 4x lower cost than GPT-5 setup.

---

## Suggestions & Future Directions

1. **Temporal Knowledge Graphs** -- ULTRAG-OTS has no native support for temporal queries. The authors suggest extending to Temporal KGs (e.g., TFLEX framework by Lin et al., 2023).

2. **Knowledge HyperGraphs** -- Current reliance on ULTRA as the link predictor limits performance on hypergraph settings. Integration with HYPER (Huang et al., 2025c) is a natural extension.

3. **Better Foundation Models** -- Improvements to ULTRA/ULTRAQUERY (e.g., SEMMA by Arun et al., 2025) would directly translate to better ULTRAG performance with no other changes.

4. **Multi-Iteration Sufficiency** -- ULTRAG-OTS uses a single query iteration (D always returns True). Enabling multi-round querying could improve performance on highly complex questions.

5. **Query Complexity Ceiling** -- The performance gap between ground-truth queries and LLM-generated queries grows from 4.32% MRR at 1-hop to 13.53% at 4-hop. Better LLM query generation or query verification would close this gap.

---

## Authors & Institutions

Dobrik Georgiev, Kheeran K. Naidu, Alberto Cattaneo, Federico Monti, Carlo Luschi, Daniel Justus -- all from **Graphcore Research**
