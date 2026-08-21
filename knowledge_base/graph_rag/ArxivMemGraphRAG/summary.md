# MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation

**Paper:** [MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation (Wu et al., 2026)](https://arxiv.org/abs/2606.00610)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

Imagine ten people each reading a different page of a report and jotting down notes with no idea what the others wrote — you'd end up with contradictory, disconnected facts. That's how most "GraphRAG" systems build their knowledge graphs today, which is why they sometimes give worse answers than a plain search-and-summarize system. MemGraphRAG gives the note-takers a shared notebook: as each one extracts facts, they check the notebook for contradictions, resolve them by looking at the original text, and filter out topics nobody else cares about. The result is a cleaner, better-connected knowledge graph and more accurate answers, retrieved faster than any competing method.

## TL;DR

MemGraphRAG identifies isolated, chunk-level knowledge extraction as the root cause of GraphRAG's thematic irrelevance, logical inconsistency, and structural fragmentation, and fixes it with a persistent Three-Layer Global Memory (Ontology/Fact/Passage) shared by a three-agent society (Extraction, Conflict Detection, Conflict Resolution) during graph construction, plus a memory-guided Personalized PageRank retrieval pass at query time. Across five benchmarks and twelve baselines it achieves the best average generation accuracy (59.25%), the densest and most locally-clustered index graphs, and the lowest retrieval latency (0.061s), while also improving other retrievers' accuracy when they consume its graph instead of their own.

---

## Problem & Motivation

Real-world corpora are unstructured and information is sparsely distributed; naive RAG's chunking disrupts long-range dependencies, and GraphRAG's promise — structured graphs for multi-hop reasoning — often fails to deliver because the constructed graphs are low quality. The root cause: extraction LLMs process document chunks independently with no global view of the corpus, producing three systematic defects — thematic irrelevance (off-topic triples), logical inconsistency (contradictory facts), and structural fragmentation (disconnected subgraphs) — that outweigh GraphRAG's structural advantages and can push it below vanilla RAG.

---

## Main Original Ideas

1. **Three-Layer Global Memory.** A persistent shared repository with an Ontology Layer (schemas + frequencies), Fact Layer (instantiated triples), and Passage Layer (source evidence), bidirectionally indexed (schema-instance, fact-evidence), giving every agent global context instead of a chunk-local view.
2. **Multi-Agent Group (Extract / Detect / Resolve).** An Extraction Agent writes into all three memory layers jointly; a Conflict Detection Agent asynchronously scans for mutually-exclusive, temporal, or granularity conflicts; a Conflict Resolution Agent adjudicates using retrieved provenance passages rather than heuristics.
3. **Unified Schema Filtering.** New schemas are "candidates" and are promoted to "stable" only once their extraction frequency crosses a threshold τ, suppressing thematically irrelevant, low-frequency noise before it reaches the graph.
4. **Memory-Guided Bridging.** The Fact Graph is augmented with type-based edges (shared stable schema types) and similarity-based edges (high embedding-similarity entities) to repair structural fragmentation.
5. **Memory-guided online retrieval.** Query-time retrieval filters candidates from all three memory layers, initializes node weights via three complementary signals (fact similarity for entities, hub-suppressed schema similarity for types, information-density-weighted similarity for passages), then runs Personalized PageRank (damping λ=0.5) to select final context.

---

## Key Findings

| Metric | MemGraphRAG | Strongest baseline |
|---|---|---|
| Avg. generation accuracy (5 datasets, Table 1) | **59.25%** | HippoRAG2, +2.10 pts |
| G-Bench Medical retrieval time | **0.061s** | LightRAG 11.052s, HippoRAG 1.586s |
| G-Bench Medical Complex Reasoning (Recall/Relevance) | **90.42 / 82.64** | best among all baselines |
| Backbone-robustness avg (llama-3-70b-instruct) | **58.41%** | HippoRAG2 55.41% |
| Avg. Degree / Clustering Coeff. (G-Medical) | **14.37 / 0.527** | HippoRAG2 13.31 / 0.497 |

- Its constructed graph is a drop-in improvement for other retrievers: swapping MemGraphRAG's graph into HippoRAG, HippoRAG2, MS-GraphRAG, and LazyGraphRAG improves every one of them on every dataset (e.g. HippoRAG 51.07% → 51.78%).
- Ablations show Conflict Resolution matters most (removing it costs the largest accuracy drop on HotpotQA), followed by Schema Filtering, Hub Suppression, and the Information Density term.
- Qualitative case studies show the Resolution Agent correctly picking "1643" over a conflicting "1645" birth year using provenance passages, and Schema Filtering dropping a noise triple ("Patient prefers Tea") while keeping stable clinical patterns.

---

## Suggestions & Future Directions

The authors acknowledge a unimodal limitation: non-text elements (charts, diagrams, images) must be transcribed to text first, losing visual/spatial semantics. Future work proposes extending the Global Hierarchical Graph with multimodal nodes (e.g. embedding visual patches into the Fact or Passage Layer) to enable cross-modal claim verification.

---

## Authors & Institutions

Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, Jinsong Su. Funded by the Natural Science Foundation of Fujian Province of China and the Public Technology Service Platform Project of Xiamen. Presented at KDD 2026, Jeju Island, Republic of Korea.
