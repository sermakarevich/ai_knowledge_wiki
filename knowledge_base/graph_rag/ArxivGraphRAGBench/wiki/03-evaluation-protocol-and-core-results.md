> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation Protocol, Metrics & Core Results

**In one sentence:** GraphRAG-Bench decomposes GraphRAG into graph construction, retrieval, and generation stages and scores each — plus a gold-rationale reasoning score — against nine methods (RAPTOR, LightRAG, GraphRAG, G-Retriever, HippoRAG, GFM-RAG, DALK, KGP, ToG) under a shared GPT-4o-mini setup, finding that RAPTOR and HippoRAG lead on both generation accuracy and reasoning while DALK and G-Retriever actually degrade the LLM.

## Key points

- Evaluation covers four metric families: (1) graph construction — efficiency (build time), cost (tokens), organization (non-isolated node ratio); (2) knowledge retrieval — indexing time, average per-query retrieval time, and retrieval operators used; (3) generation — a new LLM-judged Accuracy metric (semantic scoring for OE/FB, exact for MC/TF, partial credit for MS); and (4) rationale — an R reasoning-consistency score against the gold rationale plus an AR metric separating genuine reasoning from lucky guesses.
- Nine state-of-the-art GraphRAG methods are compared: RAPTOR, LightRAG, GraphRAG, G-Retriever, HippoRAG, GFM-RAG, DALK, KGP, and ToG, all run with the same GPT-4o-mini base LLM, no max-token cap, top-k=5, and 1200-token chunks; other hyperparameters are set to original-paper optima.
- Graph construction splits into four structure classes: Tree (RAPTOR, lowest token cost but slowest due to iterative clustering), Passage Graph (KGP, second-longest time, worst organization at 46.03%), Knowledge Graph (G-Retriever/HippoRAG/GFM-RAG/DALK, shortest time and best organization at ~90%), and Rich Knowledge Graph (GraphRAG/LightRAG, highest token cost because of added node/edge descriptions).
- Retrieval extremes: GFM-RAG indexes fastest (93.55s, no traditional vector DB) while HippoRAG indexes slowest (4695.29s, extra entity↔relationship and relationship↔chunk mappings); RAPTOR retrieves fastest (0.02s average) thanks to tree-based localization, while DALK/ToG/KGP are slow at retrieval because they invoke the LLM per query.
- Generation accuracy (average, vs GPT-4o-mini baseline of 70.68): RAPTOR is the top performer at 73.58, followed by HippoRAG 72.64 and GraphRAG 72.50; every GraphRAG method beats the TF-IDF (71.71) and BM-25 (71.66) baselines.
- DALK (69.30) and G-Retriever (69.84) are the only methods that degrade the LLM vs baseline: their over-reliance on structural information at the expense of semantic content introduces excessive generation noise that impairs LLM judgment.
- On reasoning, GPT-4o-mini drops sharply in R/AR scores even though its generation accuracy is high — it often answers by conjecture/pattern matching — while all GraphRAG methods significantly enhance reasoning by retrieving multi-hop dependent corpus as evidential support; HippoRAG and RAPTOR remain the top reasoning performers, mirroring their generation ranking.
- The paper's broader claim: graph-based architectures help most when they integrate structure with chunk-level semantics (GraphRAG's communities, HippoRAG's PageRank, GFM-RAG's pretrained model) or match the data's natural hierarchy (RAPTOR's tree), rather than when they lean on structure alone.

---

## Metrics

- **Graph construction** — three aspects: 1) *Efficiency*: time required to build the complete graph. 2) *Cost*: number of tokens consumed during construction. 3) *Organization*: proportion of non-isolated nodes in the constructed graph (inapplicable to the Tree structure, which contains no isolated nodes).
- **Knowledge retrieval** — two dimensions: 1) *indexing time*: duration to construct the vector database used for retrieval; 2) *average retrieval time*: mean per-query retrieval cost. Additionally, the *retrieval operators* each method employs are summarized to assess retrieval-mechanism complexity.
- **Generation** — a new **Accuracy** metric, motivated by the argument that exact match (word-by-word correspondence) is inappropriate for open answers: 1) **OE and FB** questions: both the generated output and the ground truth are fed to an LLM via a designed prompt, which scores based on semantic alignment and correctness; 2) **MC and TF**: 1 point for a correct answer, 0 otherwise; 3) **MS**: 1 point for a fully correct answer, 0.5 for a subset, 0 for incorrect.
- **Rationale / reasoning** — an **R score**: the method's generated rationale and the gold rationale are both fed to an LLM, which assigns a reasoning score R for their semantic correspondence and reasoning consistency. An additional **AR metric** determines whether the model provides correct reasoning when it answers correctly — distinguishing models that merely guessed the right answer from those that actually engaged proper logical reasoning to reach it.

## Experiment setup

- **Nine compared methods:** 1) RAPTOR, 2) LightRAG, 3) GraphRAG, 4) G-Retriever, 5) HippoRAG, 6) GFM-RAG, 7) DALK, 8) KGP, 9) ToG.
- **Shared configuration for fair comparison:** GPT-4o-mini as the default base LLM for all methods; no max-token length imposed (so individual methods are not artificially limited); top-k = 5 uniformly for methods requiring k-selection; text chunking at 1200 tokens consistently.
- **Other hyperparameters** were set to the optimal values reported in each method's original paper, rather than tuned for this benchmark.

## Graph construction results (Table 2)

| Method | Token cost of graph construction | Time cost of graph construction | Organization (non-isolated nodes) |
|---|---|---|---|
| RAPTOR (2024) | 10,142,221 | 20,396.49s | — (not applicable to Tree) |
| KGP (2024) | 15,271,633 | 17,318.07s | 46.03% |
| LightRAG (2024) | 83,909,073 | 12,976.22s | 69.71% |
| GraphRAG (2025) | 79,929,698 | 11,181.24s | 72.51% |
| G-Retriever (2024) | 32,948,161 | 5,315.27s | 89.95% |
| HippoRAG (2024) | 33,006,198 | 5,051.41s | 89.58% |
| DALK (2024) | 33,007,324 | **4,674.30s** | 89.49% |
| ToG (2024) | 33,008,230 | 5,235.30s | 89.95% |
| GFM-RAG (2025) | 32,766,094 | 5,631.10s | **89.97%** |

**Four graph-structure classes and their cost/quality tradeoffs:**

1. **Tree (RAPTOR):** each leaf node is a chunk; LLM-generated summaries plus clustering iteratively create parent nodes into a hierarchical tree. Lowest token cost (LLM invoked only for summary generation) but the longest build time (iterative clustering). No isolated nodes exist, so the organization metric does not apply.
2. **Passage Graph (KGP):** each chunk is a node; edges come from entity-linking tools. Token cost is modest (LLM only for summarizing entities/relationships), time is the second-longest (entity linking is time-intensive), and organization is worst (46.03%) — entity linking fails to establish edges between most entity pairs.
3. **Knowledge Graph (G-Retriever, HippoRAG, GFM-RAG, DALK):** entities and relationships extracted from chunks via open information extraction (OpenIE). Moderate token usage (LLM needed for both entity extraction and triple generation) but the shortest build times (4,674–5,631s), and the best organization at ~90% non-isolated nodes.
4. **Rich Knowledge Graph (GraphRAG, LightRAG):** standard knowledge graphs enriched with LLM-generated descriptions for nodes/edges. Highest token cost (~80M–84M tokens) and second-tier time (11–13k s); organization suboptimal (69.71–72.51%) — the added information inevitably introduces more noise.

## Knowledge retrieval results (Table 3)

| Method | Retrieval operators | Indexing time | Average retrieval time |
|---|---|---|---|
| KGP | Node | 204.10s | 89.38s |
| ToG | Node+Relationship | 1,080.43s | 70.53s |
| GraphRAG | Node+Relationship+Chunk+Community | 1,796.65s | 44.87s |
| DALK | Node+Subgraph | 407.10s | 26.80s |
| G-Retriever | Node+Relationship+Subgraph | 920.39s | 23.77s |
| LightRAG | Node+Relationship+Chunk | 1,430.32s | 13.95s |
| HippoRAG | Node+Relationship+Chunk | 4,695.29s | 2.44s |
| GFM-RAG | Node | **93.55s** | 1.96s |
| RAPTOR | Node | 451.03s | **0.02s** |

**Why the extremes differ:**

- **GFM-RAG indexes fastest (93.55s)** because it does not build a traditional vector database at all — it stores question-corresponding entities exclusively during graph construction.
- **RAPTOR retrieves fastest (0.02s average)** because its tree structure enables rapid information localization. GFM-RAG (1.96s) and HippoRAG (2.44s) follow, leveraging GNNs and PageRank respectively.
- **HippoRAG indexes slowest (4,695.29s)** due to its extra construction of entity↔relationship and relationship↔chunk mappings. GraphRAG is also slow (1,796.65s) because it additionally stores community reports; ToG/G-Retriever/LightRAG are moderate because storing relationships is inherently time-consuming; KGP/RAPTOR/DALK index cheaply with minimal stored information.
- On the retrieval side, G-Retriever (prize-collecting Steiner forest) and LightRAG (relationship-based retrieval) add latency, GraphRAG is slowed by using community information, and KGP/ToG/DALK incur substantial per-query time (26.80–89.38s) because they depend on LLM invocations during retrieval.

## Generation accuracy results (Table 4)

Accuracy by question type (FB = fill-in-blank, MC = multi-choice, MS = multi-select, TF = true-or-false, OE = open-ended) vs GPT-4o-mini baseline (74.29 / 81.11 / 76.68 / 75.95 / 52.23, avg 70.68):

| Method | FB | MC | MS | TF | OE | Average | Δ vs GPT-4o-mini |
|---|---|---|---|---|---|---|---|
| GPT-4o-mini (baseline) | 74.29 | 81.11 | 76.68 | 75.95 | 52.23 | 70.68 | — |
| TF-IDF (RAG baseline) | 75.71 | 77.88 | 72.52 | 84.17 | 50.18 | 71.71 | ↑ |
| BM-25 (RAG baseline) | 74.28 | 78.80 | 71.17 | **84.49** | 50.00 | 71.66 | ↑ |
| DALK | 70.00 | 78.34 | 71.62 | 77.22 | 51.49 | 69.30 | ↓ |
| G-Retriever | 70.95 | 77.42 | 71.62 | 78.80 | 52.04 | 69.84 | ↓ |
| LightRAG | 65.24 | 78.80 | 73.42 | 82.59 | 53.16 | 71.22 | ↑ |
| ToG | 70.48 | 78.80 | **78.38** | 79.75 | 54.28 | 71.71 | ↑ |
| KGP | 74.29 | 79.26 | 74.77 | 82.28 | 51.49 | 71.86 | ↑ |
| GFM-RAG | 72.38 | 80.65 | 72.07 | 82.59 | 52.79 | 72.10 | ↑ |
| GraphRAG | 75.24 | **81.57** | 77.48 | 80.70 | 52.42 | 72.50 | ↑ |
| HippoRAG | 70.48 | 80.18 | 74.32 | 81.65 | **56.13** | 72.64 | ↑ |
| RAPTOR | **76.67** | 80.65 | 77.48 | 82.28 | 54.83 | **73.58** | ↑ |

**Read-out:**

- **RAPTOR is the top performer** (73.58 average; also best on FB at 76.67). Its iteratively clustered tree matches the natural hierarchical organization of textbook data, enabling efficient retrieval of relevant information. HippoRAG (72.64, best on OE at 56.13) and GraphRAG (72.50, best on MC at 81.57) round out the top — all three integrate graph structure with chunk-level semantics (HippoRAG via PageRank, GraphRAG via community-based retrieval, GFM-RAG via its pretrained foundation model).
- **DALK and G-Retriever degrade the LLM** (69.30 / 69.84, below the 70.68 baseline): their over-reliance on structural information at the expense of semantic content introduces excessive noise in generation, impairing LLM judgment.
- **LightRAG, ToG, and KGP** give only slight gains — their retrieved content provides mere marginal assistance on generation tasks.
- Most GraphRAG methods outperform the traditional RAG baselines (BM-25, TF-IDF), supporting the utility of graph-based architectures for generation accuracy — consistent with the paper's argument that GPT-4o-mini is already strong at QA, so not every GraphRAG method nets a benefit.

## Reasoning capability results (Table 5)

R = reasoning-consistency score against the gold rationale; AR = "answer-and-reasoning" score, crediting a method only when a correct answer is paired with correct reasoning (rather than a lucky guess), by question type:

| Method | FB R | FB AR | MC R | MC AR | MS R | MS AR | TF R | TF AR | OE R | OE AR | Avg R | Avg AR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GPT-4o-mini (baseline) | 64.76 | 53.33 | 55.07 | 50.92 | 54.50 | 39.19 | 58.23 | 53.40 | 49.26 | 9.76 | 55.45 | 39.78 |
| TF-IDF (RAG baseline) | 68.09 | 52.61 | 52.76 | 49.19 | 56.30 | 43.02 | 64.08 | 61.23 | 50.37 | 10.50 | 57.61 | 42.38 |
| BM-25 (RAG baseline) | 69.04 | 56.42 | 57.14 | 53.11 | 57.20 | 42.79 | 65.18 | 62.18 | 50.74 | 11.52 | 59.18 | 44.15 |
| DALK | 70.95 | 55.24 | 54.15 | 50.35 | 59.01 | 46.40 | 62.18 | 58.23 | 54.09 | 9.67 | 58.89 | 42.12 |
| KGP | 64.29 | 49.29 | 56.45 | 52.07 | 58.11 | 44.37 | 64.08 | 60.68 | 52.42 | 8.92 | 58.74 | 42.22 |
| GraphRAG | **71.43** | 55.24 | 56.22 | 52.42 | 57.66 | 45.72 | 63.61 | 60.13 | 53.16 | 10.50 | 59.43 | 43.30 |
| G-Retriever | 70.00 | 55.00 | **57.60** | **53.46** | 60.81 | 48.20 | 64.24 | 60.21 | 53.35 | 10.04 | 60.17 | 43.66 |
| LightRAG | 66.19 | 47.86 | 57.14 | 52.30 | **61.71** | **49.10** | 66.61 | 63.45 | 53.16 | 10.13 | 60.46 | 43.81 |
| ToG | 70.00 | 53.10 | 56.00 | 51.73 | 57.21 | 45.72 | 65.66 | 62.26 | 54.46 | 12.08 | 60.17 | 44.01 |
| GFM-RAG | 70.00 | 54.76 | 56.22 | 52.07 | 58.11 | 45.50 | 66.46 | **63.69** | 53.72 | 10.69 | 60.36 | 44.30 |
| HippoRAG | 66.67 | 50.48 | 56.68 | 52.30 | 59.91 | 47.52 | **67.25** | 63.61 | **55.02** | 12.36 | **60.90** | 44.55 |
| RAPTOR | **71.43** | **57.86** | 56.45 | 52.07 | 60.36 | **49.10** | 66.30 | 62.90 | 53.90 | **13.57** | 60.81 | **45.53** |

**Read-out:**

- **GPT-4o-mini's reasoning drops even though its generation accuracy is high.** The R-score decline indicates LLMs often fail to perform correct reasoning, instead selecting answers via conjecture or pattern matching. The AR-score drop indicates that even when LLMs answer correctly, their reasoning process is often flawed (or they generate correct reasoning yet choose incorrect answers) — i.e., many "correct" answers are lucky guesses.
- **All GraphRAG methods significantly enhance the LLM's reasoning capabilities.** Through their distinct algorithmic designs they retrieve not only semantically relevant corpus but also multi-hop dependent corpus from the knowledge base, giving the LLM evidential support to reason over external information instead of relying solely on internal knowledge and conjecture.
- **HippoRAG and RAPTOR remain the top performers on reasoning**, mirroring the generation ranking — intuitive, since retrieving useful information is inherently correlated with enabling correct reasoning.
- **Most GraphRAG methods still outperform the traditional RAG baselines (BM-25, TF-IDF)** on the reasoning dimension as well.

**Covers:** Section 4 intro, Metrics, Experiment setups, 4.1-4.4 of GraphRAG-Bench (arXiv:2506.02404)
