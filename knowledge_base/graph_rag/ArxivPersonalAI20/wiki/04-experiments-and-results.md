> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments and Results

**In one sentence:** PAI-2 outperforms LightRAG, RAPTOR, and HippoRAG 2 by a 4% average LLM-as-a-Judge gain on three of six benchmarks (TriviaQA, 2WikiMultihopQA, MuSiQue) and improves on PAI-1 by 27%/26%/10% on Context Relevance/Faithfulness/LLM-as-a-Judge, with ablations showing the search-plan enhancement mechanism contributes 18%, graph traversal a 5–6% edge over flat retrieval, more clue-queries (1→8) a 4% gain, and episodic-triple exclusion mitigating "Lost in the Middle."

## Key points

- PAI-2 achieves a 4% average gain by LLM-as-a-Judge on 3 out of 6 benchmarks: TriviaQA, 2WikiMultihopQA, and MuSiQue; on HotpotQA and DiaASQ it is only comparable to HippoRAG 2 and PAI-1 (6% and 1% differences by LLM-as-a-Judge respectively).
- PAI-2's best setup reaches 0.82 mean LLM-as-a-Judge (combined retrieval + plan enhancement), vs 0.57 for HippoRAG 2, 0.42 for RAPTOR, and 0.16 for LightRAG — and a 11% LLM-as-a-Judge gap over HippoRAG 2 on Natural Questions.
- Disabling the search plan enhancement mechanism degrades answer accuracy by 18% by LLM-as-a-Judge versus PAI-2's best configurations.
- Compared to PAI-1, PAI-2's QA pipeline improves answers by an average of 27% (Context Relevance), 26% (Faithfulness), and 10% (LLM-as-a-Judge).
- Graph traversal algorithms (BeamSearch/WaterCircles) show an average 5% increase by LLM-as-a-Judge over the standard flattened (naive) retriever in both PAI-1 and PAI-2.
- Increasing the maximum number of clue-queries from 1 to 8 yields an average 4% gain by LLM-as-a-Judge (e.g., mean LLM-as-a-Judge 0.48 at 1 clue-query vs 0.52 at 6 and 8).
- TriviaQA is the easiest benchmark and MuSiQue the most difficult, with average LLM-as-a-Judge scores of 0.68 and 0.20 respectively across methods' best setups.
- The Memorize (plain-text-to-knowledge-graph extraction) pipeline achieves SOTA 89% information-retention score on the MINE benchmark.

---

## Main comparison against baselines

A comparative table summarizing the best-performing QA configurations by LLM-as-a-Judge metric was compiled (Table 3). PAI-2 achieves superior results with a 4% average gain by LLM-as-a-Judge on 3 out of 6 benchmarks: TriviaQA, 2WikiMultihopQA, and MuSiQue. Meanwhile, on HotpotQA and DiaASQ it achieves comparable results to HippoRAG 2 and PAI-1: with a 6% and 1% difference by LLM-as-a-Judge, respectively.

TriviaQA turned out to be the easiest benchmark (in terms of question difficulty), while MuSiQue was the most difficult, with average LLM-as-a-Judge scores of 0.68 and 0.20, respectively. There is a significant gap between PAI-2 and HippoRAG 2 on Natural Questions: a 11% difference by LLM-as-a-Judge. This may be attributed to characteristics of this benchmark: (1) the original questions are presented in lowercase, which increases the probability of missing critical named entities and consequently losing essential information required for relevant response generation; (2) some questions require general or insufficiently specific answers, for example "how are the American declaration of independence and the French declaration of the rights of man similar". Because PAI-2 does not have an explicit mechanism for detecting question type and expected answer format, at the decision-making stage it often returns a "No Answer" response due to uncertainty regarding the completeness of retrieved/summarized knowledge from memory.

PAI-2 vs PAI-1: the proposed QA pipeline significantly improves answer quality — average increases by Context Relevance, Faithfulness, and LLM-as-a-Judge metrics are 27%, 26%, and 10%, respectively. This means that integration of a planning stage with a search-steps enhancement mechanism and knowledge-graph traversal based on a set of detailed/adjusted clue-queries increases the probability of extracting relevant information from a structured document store and improves consistency of the final answer with the existing knowledge base.

Table 3. Best LLM-as-a-Judge scores for LightRAG, RAPTOR, HippoRAG 2 and Context Relevance / Faithfulness / LLM-as-a-Judge scores for PAI-1 and PAI-2 on six benchmarks. For PAI-1 and PAI-2 the cells also contain the retrieval algorithm and the type of restriction applied to the graph during traversal. Retrieval algorithm shortcuts: "BS+WC" — hybrid of BeamSearch and WaterCircles; "BS+NR" — hybrid of BeamSearch and NaiveRetriever. Graph restriction shortcuts: "all" — no restrictions applied; "E" — episodic vertices were excluded from traversal. PAI-1/PAI-2 cells are shown as Context Relevance / Faithfulness / LLM-as-a-Judge, with the best per-dataset value bolded.

| Method | LLM | Natural Questions | TriviaQA | HotpotQA | 2WikiMultihopQA | MuSiQue | DiaASQ | Mean |
|---|---|---|---|---|---|---|---|---|
| LightRAG | Qwen2.5 7B | 0.26 | 0.37 | 0.15 | 0.11 | 0.01 | 0.07 | 0.16 |
| RAPTOR | RAPTOR | 0.66 | 0.73 | 0.46 | 0.27 | 0.22 | 0.15 | 0.42 |
| HippoRAG 2 | HippoRAG 2 | **0.80** | 0.77 | **0.73** | 0.56 | 0.29 | 0.28 | **0.57** |
| PAI-1 (Ours) — only Naive Retriever | only Naive Retriever | 0.68 / 0.63 / 0.56 | 0.68 / 0.74 / 0.70 | 0.65 / 0.62 / 0.50 | - / - / 0.29 | 0.32 / 0.46 / 0.12 | - / - / 0.14 | 0.58 / 0.61 / 0.38 |
| PAI-1 (Ours) — only Traversal Algorithms | only Traversal Algorithms | 0.68 / 0.61 / 0.55 | - / - / 0.67 | 0.65 / 0.61 / 0.62 | 0.45 / 0.35 / 0.34 | 0.32 / 0.65 / 0.12 | 0.63 / 0.36 / **0.35** | 0.54 / 0.51 / 0.44 |
| PAI-1 (Ours) — Combined Retrieval (best) | Combined Retrieval (best) | - / - / 0.56 (BS+NR / E) | 0.66 / 0.82 / 0.73 (BS+NR / all) | 0.65 / 0.61 / 0.62 (BS+WC / all) | 0.46 / 0.50 / 0.40 (BS+NR / all) | 0.35 / 0.36 / 0.17 (BS+NR / all) | 0.63 / 0.36 / 0.35 (BS+WC / all) | 0.55 / 0.53 / 0.47 |
| PAI-2 (Ours) — only Traversal Algorithms + w/o plan enhancement | only Traversal Algorithms + w/o plan enhancement | - / - / 0.57 | 0.74 / 0.88 / 0.71 | 0.71 / 0.81 / 0.47 | 0.44 / **0.84** / 0.28 | 0.34 / 0.80 / 0.08 | **0.83** / 0.63 / 0.26 | 0.61 / 0.79 / 0.39 |
| PAI-2 (Ours) — only Naive Retriever + plan enhancement | only Naive Retriever + plan enhancement | 0.88 / 0.96 / 0.64 | 0.89 / 0.88 / 0.77 | 0.82 / 0.85 / 0.63 | 0.60 / 0.78 / 0.48 | **0.68** / 0.86 / 0.28 | 0.66 / 0.60 / 0.26 | 0.75 / **0.82** / 0.51 |
| PAI-2 (Ours) — only Traversal Algorithms + plan enhancement | only Traversal Algorithms + plan enhancement | 0.91 / 0.93 / 0.67 | **0.92** / **0.91** / 0.77 | **0.89** / **0.87** / 0.67 | **0.74** / 0.80 / 0.54 | 0.66 / **0.87** / 0.33 | **0.83** / 0.58 / 0.34 | **0.82** / **0.82** / 0.55 |
| PAI-2 (Ours) — Combined Retrieval (best) + plan enhancement | Combined Retrieval (best) + plan enhancement | **0.93** / 0.91 / 0.69 (BS+NR / E) | 0.89 / 0.83 / **0.8** (BS+NR / all) | **0.89** / **0.87** / 0.67 (BS+WC / all) | **0.74** / 0.74 / **0.58** (BS+NR / all) | 0.66 / **0.87** / **0.33** (BS+WC / all) | **0.83** / 0.57 / 0.34 (BS+WC / E) | **0.82** / 0.79 / **0.57** |
| Mean (by best setups) | Mean (by best setups) | 0.59 | 0.68 | 0.52 | 0.38 | 0.20 | 0.23 | 0.43 |

To prepare document stores and perform QA for every method, Qwen2.5 7B was used.

## Search-plan enhancement ablation

A series of experiments evaluated PAI-2 with the disabled search-plan enhancement mechanism. Table 3 shows that, compared to the best PAI-2 configurations, accuracy of generated answers is degraded by 18% by LLM-as-a-Judge. This can be attributed to the form/complexity of some questions, which requires a dynamic search strategy with intermediate grounding on available knowledge in the memory graph.

Example: the question "Do both films Payment On Demand and My Cousin From Warsaw have the directors from the same country?" yields the following initial plan: (1) "Who is the director of the film Payment On Demand?"; (2) "Who is the director of the film My Cousin From Warsaw?"; (3) "What country is the director of Payment On Demand from?"; (4) "What country is the director of My Cousin From Warsaw from?". The last two steps require clarification using information obtained from the first, more specific, steps. With plan enhancement disabled, the information available to generate the final answer is: (1) "Curtis Bernhardt"; (2) "Carl Boese is the director of the film My Cousin From Warsaw."; (3) "Germany"; (4) "<|NotEnoughtInfo|>" — not enough to generate a relevant answer. If subsequent search steps can be modified based on information obtained by previous steps, the enhanced plan becomes: (1) "Who is the director of the film Payment On Demand?"; (2) "Who is the director of the film My Cousin From Warsaw?"; (3) "What country is the director of Payment On Demand from?"; (4) "What country is Carl Boese from?"; (5) "What country is Curtis Bernhardt from?". With that enhanced plan, the available information for the final answer is: (1) "The director of the film Payment On Demand is Curtis Bernhardt."; (2) "The director of the film 'My Cousin from Warsaw' is Carl Boese."; (3) "Curtis Bernhardt, the director of Payment On Demand, was born in New York, New York."; (4) "Carl Boese was a German film director, screenwriter, and producer."; (5) "Curtis Bernhardt, born as Kurt Bernhardt in Worms, Germany, was from Germany." — crucial information successfully extracted from memory to generate an accurate answer.

## Graph traversal algorithm ablation

Both PAI-1 and PAI-2 demonstrate a trend toward the superiority of graph traversal algorithms (e.g., BeamSearch, WaterCircles in the BS+NR and BS+WC hybrid setups) over the standard flattened (NaiveRetriever) retriever: an average 5% increase by LLM-as-a-Judge.

- PAI-1: "only Traversal Algorithms" mean LLM-as-a-Judge 0.44 vs "only Naive Retriever" 0.38 (Table 3).
- PAI-2: "only Traversal Algorithms + plan enhancement" mean 0.55 vs "only Naive Retriever + plan enhancement" 0.51 (Table 3); e.g., on 2WikiMultihopQA, **0.74** / 0.80 / 0.54 (traversal) vs 0.60 / 0.78 / 0.48 (naive).

Graph restriction also matters: excluding episodic vertices ("E") during traversal improved best setups on Natural Questions (0.93 / 0.91 / 0.69, BS+NR / E) and DiaASQ (0.83 / 0.57 / 0.34, BS+WC / E).

## Triple-type and clue-query-count ablations

**Triple types (Table 4).** It is important to control the amount of noise in the triples the LLM uses for knowledge summarization and deciding the next search step. Using the NaiveRetriever algorithm, exclusion of episodic triples from the LLM context for both PAI-1 and PAI-2 mitigates the "Lost in the Middle" problem and improves accuracy and groundedness of answers. Table 4 shows PAI-1 and PAI-2 performance depending on accepted triple types (simple, hyper, simple+hyper, episodic) for final answer generation across the six datasets; for graph/triples traversal/retrieval the NaiveRetriever algorithm is used. Cells are Context Relevance / Faithfulness / LLM-as-a-Judge with the best per-dataset value bolded.

| Method | Accepted Triplet Types | LLM | Natural Questions | TriviaQA | HotpotQA | 2WikiMultihopQA | MuSiQue | DiaASQ | Mean |
|---|---|---|---|---|---|---|---|---|---|
| PAI-1 | simple | Qwen2.5 7B | 0.63 / 0.62 / 0.47 | 0.63 / 0.66 / 0.68 | 0.63 / 0.45 / 0.48 | - / - / 0.26 | 0.23 / 0.52 / **0.13** | - / - / 0.07 | 0.53 / 0.56 / 0.35 |
| PAI-1 | hyper | hyper | 0.60 / 0.57 / 0.45 | 0.63 / 0.69 / 0.64 | - / - / 0.35 | - / - / 0.23 | 0.21 / **0.68** / 0.06 | - / - / **0.15** | 0.48 / **0.65** / 0.31 |
| PAI-1 | simple, hyper | simple, hyper | **0.68** / **0.64** / **0.56** | **0.68** / **0.74** / **0.70** | **0.65** / **0.62** / **0.50** | - / - / **0.29** | **0.32** / 0.46 / 0.12 | - / - / 0.14 | **0.58** / 0.62 / **0.38** |
| PAI-1 | episodic | episodic | 0.48 / 0.61 / 0.37 | 0.65 / **0.74** / 0.44 | - / - / 0.21 | 0.41 / 0.51 / 0.13 | 0.16 / 0.56 / - | - / - / - | 0.42 / 0.60 / 0.29 |
| PAI-2 | simple | simple | 0.86 / **0.96** / 0.58 | 0.86 / 0.87 / 0.69 | **0.83** / **0.85** / 0.59 | 0.59 / 0.67 / **0.48** | **0.69** / **0.86** / 0.25 | 0.49 / 0.56 / 0.10 | 0.72 / 0.80 / 0.45 |
| PAI-2 | hyper | hyper | **0.90** / 0.92 / 0.59 | 0.88 / 0.86 / 0.72 | 0.73 / 0.79 / 0.50 | 0.52 / 0.74 / 0.34 | 0.59 / 0.73 / 0.27 | 0.62 / 0.61 / 0.25 | 0.71 / 0.78 / 0.44 |
| PAI-2 | simple, hyper | simple, hyper | 0.88 / **0.96** / **0.64** | **0.89** / **0.88** / **0.77** | 0.82 / **0.85** / **0.63** | **0.60** / **0.78** / **0.48** | 0.68 / **0.86** / 0.28 | **0.66** / 0.60 / **0.26** | **0.76** / **0.82** / **0.51** |
| PAI-2 | episodic | episodic | 0.75 / 0.93 / 0.60 | - / - / 0.66 | 0.73 / 0.81 / 0.55 | 0.48 / 0.75 / 0.33 | 0.62 / 0.82 / **0.32** | 0.32 / **0.62** / 0.06 | 0.58 / 0.79 / 0.42 |
| Mean (PAI-1) | — | — | 0.60 / 0.61 / 0.46 | 0.65 / 0.71 / 0.62 | 0.64 / 0.54 / 0.38 | 0.41 / 0.51 / 0.23 | 0.23 / 0.56 / 0.10 | - | 0.51 / 0.60 / 0.34 |
| Mean (PAI-2) | — | — | 0.85 / 0.94 / 0.60 | 0.88 / 0.87 / 0.71 | 0.78 / 0.82 / 0.57 | 0.55 / 0.74 / 0.41 | 0.64 / 0.82 / 0.28 | 0.52 / 0.60 / 0.17 | 0.70 / 0.79 / 0.46 |

**Clue-query count (Table 5).** To measure the impact of the number of clue-queries per search step on relevance of generated answers, a series of experiments was conducted (non-aggregated results are in Appendix H). With an increase in clue-query count (used to manage graph traversal from associated starting vertices), answer quality improves: an average 4% gain by LLM-as-a-Judge was achieved when changing the maximum number of clue-queries from 1 to 8 (mean LLM-as-a-Judge 0.48 → 0.52). This may be attributed to characteristics of PAI's memory-graph construction: when a new document is added, its extracted triplets are validated for duplicates against triplets in the existing memory graph using exact match on the triplet's text attributes. Because the same knowledge can be formulated in different ways, several subgraphs may appear in memory that contain and describe the same knowledge using different entities; such subgraphs may share no common vertices and may be incomplete, so information about a single object can be scattered across subgraphs. Using multiple vertices for a single entity from the search plan and generating clue questions from their linear combination allows traversing such subgraphs and aggregating the requested information to generate an accurate and complete answer.

| Max Clue Queries | LLM | Natural Questions | TriviaQA | HotpotQA | 2WikiMultihopQA | MuSiQue | DiaASQ | Mean |
|---|---|---|---|---|---|---|---|---|
| 1 | Qwen2.5 7B | 0.85 / **0.94** / 0.60 | 0.88 / **0.89** / 0.72 | 0.83 / **0.84** / 0.58 | 0.66 / 0.75 / 0.49 | 0.63 / 0.82 / 0.24 | 0.76 / **0.66** / 0.25 | 0.77 / **0.82** / 0.48 |
| 2 | 2 | 0.89 / 0.93 / **0.66** | 0.88 / 0.86 / 0.73 | 0.84 / **0.84** / 0.58 | 0.68 / 0.75 / 0.51 | 0.67 / **0.83** / **0.29** | 0.80 / 0.64 / 0.26 | 0.79 / 0.81 / 0.50 |
| 4 | 4 | **0.90** / 0.92 / 0.65 | 0.89 / 0.87 / 0.75 | 0.88 / **0.84** / 0.61 | 0.71 / 0.76 / 0.53 | 0.69 / 0.82 / 0.25 | 0.82 / 0.65 / 0.27 | **0.82** / 0.81 / 0.51 |
| 6 | 6 | **0.90** / 0.93 / 0.64 | 0.89 / 0.87 / **0.77** | 0.88 / **0.84** / **0.62** | **0.73** / **0.78** / **0.55** | 0.70 / 0.81 / 0.25 | **0.84** / 0.64 / 0.28 | **0.82** / 0.81 / **0.52** |
| 8 | 8 | **0.90** / 0.92 / 0.65 | **0.90** / 0.88 / **0.77** | **0.89** / 0.83 / **0.62** | 0.71 / 0.76 / 0.53 | **0.71** / 0.82 / 0.25 | **0.84** / 0.64 / **0.29** | **0.82** / 0.81 / **0.52** |
| Mean | — | 0.89 / 0.93 / 0.64 | 0.89 / 0.87 / 0.75 | 0.86 / 0.84 / 0.60 | 0.70 / 0.76 / 0.52 | 0.68 / 0.82 / 0.26 | 0.81 / 0.65 / 0.27 | 0.80 / 0.81 / 0.51 |

Table 5 cells contain Context Relevance, Faithfulness, and LLM-as-a-Judge scores, with the best per-dataset value bolded.

## Latency

Table 6 (referenced for time required to process a single user question; Qwen2.5 7B was used for document store preparation and QA) shows that PAI-2 requires approximately double the time to process one question and generate an answer compared to PAI-1. This is because PAI-1 performs only a single iteration of information retrieval, while in PAI-2 the number of iterations can vary depending on the complexity of the question.

Identified bottlenecks: (1) LLM inference; (2) vector search; (3) knowledge graph traversal. Recommended mitigation practices: (1) caching and reusing LLM inference results; (2) splitting large vector stores into smaller subsets by element types; (3) limiting the search space in the memory graph.

Additionally, the plain-text-to-knowledge-graph extraction algorithm (Memorize pipeline) was evaluated on the MINE benchmark to measure the factual completeness of constructing PAI's memory graphs: it demonstrates SOTA results with an 89% information-retention score (details in Appendix I).

**Covers:** Section VI (Experiments and Results) of the paper, including Tables 1–6.
