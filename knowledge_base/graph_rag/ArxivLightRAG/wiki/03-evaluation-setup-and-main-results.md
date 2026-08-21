> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation Setup and Main Results (RQ1)

**In one sentence:** Empirical evaluation on four UltraDomain textbooks (600K–5M tokens, 125 high-level corpus-wide questions per dataset) shows LightRAG outperforms NaiveRAG, RQ-RAG, and HyDE on every dimension and dataset, and beats GraphRAG on the three million-token corpora, with its largest margins on the biggest dataset (Legal).

## Key points

- Four research questions frame the evaluation: RQ1 (vs. baselines), RQ2 (dual-level retrieval + graph indexing contribution), RQ3 (case examples), RQ4 (cost and adaptability to data changes); this chunk answers RQ1.
- Datasets: Agriculture, CS, Legal, and Mix, selected from the UltraDomain benchmark (428 college textbooks, 18 domains), each 600,000–5,000,000 tokens.
- Question generation follows Edge et al. (2024): an LLM creates 5 fake RAG users × 5 tasks × 5 questions requiring whole-corpus understanding = 125 questions per dataset.
- Baselines: Naive RAG (chunk + vector similarity), RQ-RAG (query decomposition/rewriting/disambiguation), HyDE (hypothetical-document retrieval), and GraphRAG (entity/relation graph with community reports).
- Setup: nano vector DB, GPT-4o-mini for all LLM operations, chunk size 1200, gleaning fixed at 1 for both GraphRAG and LightRAG.
- Evaluation is LLM-as-judge (GPT-4o-mini) pair-wise on 4 dimensions — Comprehensiveness, Diversity, Empowerment, Overall — with answer order alternated to remove position bias; results reported as win rates.
- Win rates: LightRAG beats NaiveRAG 61.2–85.6% overall, RQ-RAG 60.0–85.6% overall, and HyDE 57.6–75.2% overall across datasets; its single weakest overall result is 57.6% vs. HyDE on Mix.
- vs. GraphRAG: LightRAG wins Overall on Agriculture (54.8 vs. 45.2), CS (52.0 vs. 48.0), and Legal (52.8 vs. 47.2), but loses Overall on Mix (49.6 vs. 50.4) and Empowerment on Mix (49.2 vs. 50.8).

---

## Evaluation: Research Questions (Section 4)

The evaluation section opens by stating the goal: empirical assessments on benchmark data to assess the effectiveness of LightRAG, organized around four research questions:

- **(RQ1):** How does LightRAG compare to existing RAG baseline methods in terms of generation performance?
- **(RQ2):** How do dual-level retrieval and graph-based indexing enhance the generation quality of LightRAG?
- **(RQ3):** What specific advantages does LightRAG demonstrate through case examples in various scenarios?
- **(RQ4):** What are the costs associated with LightRAG, as well as its adaptability to data changes?

## Experimental Settings (4.1)

### Evaluation Datasets

Four datasets are selected from the **UltraDomain benchmark** (Qian et al., 2024). UltraDomain data is sourced from **428 college textbooks** across **18 distinct domains** (including agriculture, social sciences, humanities). Each selected dataset contains **between 600,000 and 5,000,000 tokens** (details in the paper's Table 4). The four domains:

- **Agriculture:** agricultural practices — beekeeping, hive management, crop production, disease prevention.
- **CS:** computer science including data science and software engineering; highlights machine learning and big data processing, with content on recommendation systems, classification algorithms, and real-time analytics using Spark.
- **Legal:** corporate legal practices — corporate restructuring, legal agreements, regulatory compliance, governance; focus on legal and financial sectors.
- **Mixed:** literary, biographical, and philosophical texts spanning cultural, historical, and philosophical studies.

### Question Generation

Following the method of Edge et al. (2024): all text content of each dataset is consolidated as context. An LLM generates **5 RAG users** (each with a textual description of expertise and traits), **5 tasks per user** (each emphasizing one potential user intention), and **5 questions per user-task combination** that require understanding of the entire corpus. Total: **125 questions per dataset**.

### Baselines

| Baseline | Mechanism |
|---|---|
| **Naive RAG** (Gao et al., 2023) | Standard baseline: segment raw texts into chunks, store in a vector DB via text embeddings; retrieve chunks by highest similarity of query vector representations. |
| **RQ-RAG** (Chan et al., 2024) | LLM decomposes the query into sub-queries using rewriting, decomposition, and disambiguation to enhance search accuracy. |
| **HyDE** (Gao et al., 2022) | LLM generates a hypothetical document from the query; that document retrieves relevant chunks used to form the answer. |
| **GraphRAG** (Edge et al., 2024) | LLM extracts entities/relations as nodes/edges with descriptions, aggregates nodes into communities, and generates community reports for global information; retrieves by traversing communities for high-level queries. |

### Implementation and Evaluation Details

- Vector storage: **nano vector database**.
- All LLM-based operations in LightRAG default to **GPT-4o-mini**.
- **Chunk size = 1200** across all datasets; **gleaning = 1** for both GraphRAG and LightRAG.
- Ground truth is hard for high-level semantic RAG queries, so the evaluation builds on Edge et al. (2024)'s **LLM-based multi-dimensional comparison**: **GPT-4o-mini** ranks each baseline against LightRAG (prompt in Appendix 7.3.4). Four dimensions:
  1. **Comprehensiveness** — how thoroughly the answer addresses all aspects and details;
  2. **Diversity** — how varied and rich in perspectives/insights;
  3. **Empowerment** — how well the answer lets the reader understand the topic and make informed judgments;
  4. **Overall** — cumulative performance across the three preceding criteria.
- The LLM compares the two answers on each dimension and picks the superior one; the three dimensions' winners are then combined to determine the overall better answer. **Answer placement is alternated** to mitigate order bias, and **win rates** are computed as the final metric.

## Comparison of LightRAG with Existing RAG Methods — RQ1 (4.2)

LightRAG is compared against each baseline across all four datasets and dimensions. Results (Table 1, win rates %):

### Table 1: Win rates (%) of baselines vs. LightRAG

**vs. NaiveRAG**

| Dimension | Agriculture (NaiveRAG / LightRAG) | CS (NaiveRAG / LightRAG) | Legal (NaiveRAG / LightRAG) | Mix (NaiveRAG / LightRAG) |
|---|---|---|---|---|
| Comprehensiveness | 32.4 / 67.6 | 38.4 / 61.6 | 16.4 / 83.6 | 38.8 / 61.2 |
| Diversity | 23.6 / 76.4 | 38.0 / 62.0 | 13.6 / 86.4 | 32.4 / 67.6 |
| Empowerment | 32.4 / 67.6 | 38.8 / 61.2 | 16.4 / 83.6 | 42.8 / 57.2 |
| Overall | 32.4 / 67.6 | 38.8 / 61.2 | 15.2 / 84.8 | 40.0 / 60.0 |

**vs. RQ-RAG**

| Dimension | Agriculture (RQ-RAG / LightRAG) | CS (RQ-RAG / LightRAG) | Legal (RQ-RAG / LightRAG) | Mix (RQ-RAG / LightRAG) |
|---|---|---|---|---|
| Comprehensiveness | 31.6 / 68.4 | 38.8 / 61.2 | 15.2 / 84.8 | 39.2 / 60.8 |
| Diversity | 29.2 / 70.8 | 39.2 / 60.8 | 11.6 / 88.4 | 30.8 / 69.2 |
| Empowerment | 31.6 / 68.4 | 36.4 / 63.6 | 15.2 / 84.8 | 42.4 / 57.6 |
| Overall | 32.4 / 67.6 | 38.0 / 62.0 | 14.4 / 85.6 | 40.0 / 60.0 |

**vs. HyDE**

| Dimension | Agriculture (HyDE / LightRAG) | CS (HyDE / LightRAG) | Legal (HyDE / LightRAG) | Mix (HyDE / LightRAG) |
|---|---|---|---|---|
| Comprehensiveness | 26.0 / 74.0 | 41.6 / 58.4 | 26.8 / 73.2 | 40.4 / 59.6 |
| Diversity | 24.0 / 76.0 | 38.8 / 61.2 | 20.0 / 80.0 | 32.4 / 67.6 |
| Empowerment | 25.2 / 74.8 | 40.8 / 59.2 | 26.0 / 74.0 | 46.0 / 54.0 |
| Overall | 24.8 / 75.2 | 41.6 / 58.4 | 26.4 / 73.6 | 42.4 / 57.6 |

**vs. GraphRAG**

| Dimension | Agriculture (GraphRAG / LightRAG) | CS (GraphRAG / LightRAG) | Legal (GraphRAG / LightRAG) | Mix (GraphRAG / LightRAG) |
|---|---|---|---|---|
| Comprehensiveness | 45.6 / 54.4 | 48.4 / 51.6 | 48.4 / 51.6 | 50.4 / 49.6 |
| Diversity | 22.8 / 77.2 | 40.8 / 59.2 | 26.4 / 73.6 | 36.0 / 64.0 |
| Empowerment | 41.2 / 58.8 | 45.2 / 54.8 | 43.6 / 56.4 | 50.8 / 49.2 |
| Overall | 45.2 / 54.8 | 48.0 / 52.0 | 47.2 / 52.8 | 50.4 / 49.6 |

### Conclusions drawn by the authors

**1. The Superiority of Graph-enhanced RAG Systems in Large-Scale Corpora.** When handling large token counts and complex queries requiring thorough understanding of the dataset's context, graph-based RAG systems (LightRAG, GraphRAG) consistently outperform purely chunk-based retrieval (NaiveRAG, HyDE, RQRAG), and the gap widens as dataset size increases. In the largest dataset (Legal), baselines achieve only about 20% win rates against LightRAG's dominance. This underscores the advantage of graph-enhanced RAG in capturing complex semantic dependencies within large-scale corpora, which leads to improved generalization performance.

**2. Enhancing Response Diversity with LightRAG.** LightRAG shows a significant advantage on the **Diversity** metric, particularly in the larger Legal dataset (win rates 86.4% vs. RQ-RAG and 80.0% vs. HyDE). This is attributed to the **dual-level retrieval paradigm**, which retrieves comprehensively from both low-level and high-level dimensions and leverages graph-based text indexing to capture full context in response to queries.

**3. LightRAG's Superiority over GraphRAG.** Both use graph-based retrieval, but LightRAG consistently outperforms GraphRAG, particularly in larger datasets with complex language contexts. In the **Agriculture, CS, and Legal** datasets (each containing millions of tokens), LightRAG shows a clear advantage, surpassing GraphRAG and highlighting its strength in comprehensive information understanding across diverse environments.
- *Enhanced Response Variety:* integrating low-level retrieval of specific entities with high-level retrieval of broader topics boosts diversity, addressing both detailed and abstract queries.
- *Complex Query Handling:* by accessing both specific details and overarching themes, LightRAG responds adeptly to complex queries involving interconnected topics, providing contextually relevant answers — especially valuable where diverse perspectives are required.

**Covers:** Section 4 intro, 4.1 experimental settings, 4.2 comparison with existing RAG methods (RQ1)
