> [[index|Wiki]] | [[digest|Digest]]

# RAG vs. GraphRAG: A Systematic Evaluation and Key Insights — Summary

**Paper:** [RAG vs. GraphRAG: A Systematic Evaluation and Key Insights (Han et al., 2025)](https://arxiv.org/abs/2502.11371)

## Human Readable TL;DR

Everyone building retrieval systems eventually asks: should I bother building a knowledge graph, or is plain vector retrieval (RAG) good enough? This paper answers that with a fair, controlled experiment instead of vibes. The short answer: neither wins outright. Plain RAG is better at pulling out one specific fact from one place. GraphRAG (retrieval over a graph built from your documents) is better at questions that require connecting two or more facts together. GraphRAG also costs more to build and maintain, and how you evaluate GraphRAG can bias the answer you get. Combining the two — either by routing each question to the better tool, or by feeding both into the answer — beats using either alone.

## TL;DR

A unified benchmark of standard RAG against four GraphRAG families (KG-based, community-based, text-centric graph-guided, hierarchical summary-based) across QA and query-based summarization finds complementary strengths — RAG wins single-hop factual QA, GraphRAG wins multi-hop reasoning QA — rather than a single winner. GraphRAG design choices matter (community-based Global Search trades detail for corpus-level breadth), LLM-as-a-Judge scoring for summarization is strongly biased by presentation order, and GraphRAG carries real construction/latency/storage costs on top of sensitivity to the graph-construction model's quality. Two hybrid strategies — Selection (route each query to the better paradigm) and Integration (combine both paradigms' retrieved evidence) — both improve results, with Integration giving the largest overall accuracy gain.

## Problem & Motivation

Text-based GraphRAG studies each use their own datasets, graph-construction heuristics, and evaluation protocols, making it impossible to draw principled, generalizable conclusions about when explicit graph structure actually helps or hurts, and obscuring practical costs (construction time, retrieval latency, storage). This paper fills that gap with one controlled protocol applied to both paradigms.

## Main Original Ideas

1. **A fair-comparison protocol that decouples retrieval from generation** — retrieved evidence is saved per method first, then one unified generation script produces every method's outputs, so differences in results trace to retrieval design, not incidental generation differences.
2. **Four representative GraphRAG families under one roof** — KG-based (LlamaIndex KG-GraphRAG), community-based (Microsoft GraphRAG, Local/Global search), text-centric graph-guided (HippoRAG2), and hierarchical summary-based (RAPTOR), evaluated with matched settings (256-token chunks, ada-002 embeddings, top-k=10, bge-reranker-large, IRCoT, Llama-3.1-8B/70B generators).
3. **Selection and Integration hybrid strategies** that operationalize the complementarity finding into practical systems: Selection routes each query by type for efficiency, Integration concatenates both paradigms' retrieved evidence for maximum accuracy.
4. **A demonstration that LLM-as-a-Judge evaluation for summarization is not trustworthy as-is** — swapping the presentation order of two candidate summaries changes, and sometimes reverses, which one the judge prefers.

## Key Findings

- **RAG wins single-hop, detail-oriented QA; GraphRAG wins multi-hop, reasoning-intensive QA.** No single paradigm dominates across tasks.
- **Community-based Global Search trades detail for breadth** — it aggregates corpus-level information (good for diverse summarization, Comparison/Temporal QA) at the cost of fine-grained detail (bad for detail-oriented QA and NULL/abstention accuracy).
- **KG-based GraphRAG underperforms on QA due to incomplete graphs** — only ~65.8% of HotPotQA and ~65.5% of NQ answer entities appear in the constructed KG.
- **Selection and Integration both improve QA** — on MultiHop-RAG with Llama-3.1-70B, Selection lifts the best baseline by 1.1%, Integration by 6.4% (Integration reaches Overall 77.62 vs. RAG 65.77 / GraphRAG 71.17).
- **GraphRAG is not free** — Community-GraphRAG retrieves ~2.3× more tokens than RAG for comparable results and has the largest storage footprint (165MB vs. RAG's 127MB); KG-GraphRAG has the highest retrieval latency (14,434s vs. RAG's 1,724s on MultiHop-RAG).
- **LLM-as-a-Judge for summarization is order-biased** — reversing which summary is shown first substantially changes, sometimes reverses, the judge's preference.
- **Stronger graph-construction models help, especially at scale** — building graphs with GPT-4o instead of GPT-4o-mini raises MultiHop-RAG Overall from 71.17 to 75.08 (70B backbone), with the biggest gains on Comparison/Temporal queries.

### Results table (selected)

| Benchmark | RAG | Best GraphRAG variant | Integration |
|---|---|---|---|
| NQ (single-hop, F1) | **64.78** | HippoRAG2 61.03 | — |
| HotPotQA (multi-hop, F1) | 60.04 | HippoRAG2 **63.01** | — |
| MultiHop-RAG (Overall, 8B) | 67.02 | HippoRAG2 70.27 | — |
| MultiHop-RAG (Overall, 70B) | 65.77 | Community-GraphRAG (Local) 71.17 | **77.62** |
| SQuALITY (BERTScore F1) | 77.62 | KG-GraphRAG(Triplets+Text) **84.92** | 77.73 |

## Suggestions & Future Directions

The authors point toward a "next generation" of RAG systems that: (1) construct and refine graphs more reliably (better entity/relation coverage), (2) adapt retrieval and aggregation strategy to the query rather than using one fixed pipeline, and (3) deliver stronger reasoning benefits without giving up realistic efficiency — plus more robust, order-invariant evaluation protocols for judge-based comparisons.

## Authors & Institutions

Han et al., 2025 (arXiv:2502.11371). See [source/2502.11371.pdf](source/2502.11371.pdf) for full author list and affiliations.

## Figures

- **Figure 2 (confusion matrices, [[wiki/02-question-answering-results|QA Results]])** — shows the complementarity finding directly: on MultiHop-RAG, 13.6% of queries are GraphRAG-only correct and 11.6% RAG-only correct, meaning the two systems get different questions right.
- **Figure 4 (LLM-as-a-Judge position bias, [[wiki/03-summarization-and-conclusion|Summarization]])** — shows win-rate bars flipping between presentation orders, the paper's evidence that judge-based summarization evaluation is unreliable without order controls.
