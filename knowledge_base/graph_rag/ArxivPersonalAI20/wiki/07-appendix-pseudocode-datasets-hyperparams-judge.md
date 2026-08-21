> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Pseudocode, Dataset Preparation, Hyperparameters, and Judge Instructions

**In one sentence:** This appendix documents the PAI-2 QA pipeline algorithm (pseudocode), the exact preprocessing operations and resulting statistics for the six evaluation datasets, the retrieval hyperparameters of the three baseline systems, and the full LLM-as-a-Judge prompt set and decoding config used for answer scoring.

## Key points

- The PAI-2 pipeline (Algorithm 1) is a iterative search-plan loop: for each sub-question it generates a search plan, then per step extracts entities, matches them to graph vertices, generates clue-queries, traverses the knowledge graph, filters triples by relevance, generates clue answers, and either stops (if `Sufficient`), enhances the search plan and continues up to `S_m` steps, or finally emits a finalized sub-answer or a no-answer stub, with all sub-answers aggregated into the final answer `A`.
- The four main complexity/depth bounds are `S_m` (max search-plan steps), `C_m` (max clue-queries per step), `V_m` (max matched vertices per entity), and `F_m` (max filtered triples per clue-query).
- All six datasets (Natural Questions, TriviaQA, HotpotQA, 2WikiMultihopQA, MuSiQue, DiaASQ) were reduced to evaluation subsets of a few hundred to a few thousand QA pairs and 3,400–4,900 relevant documents by applying a 64–1024 character length filter on answers/documents plus first-N selection; TriviaQA additionally required LangChain `RecursiveCharacterTextSplitter` chunking (1024 chars, 64 overlap, double-newline separators) and a coherence rule discarding all remaining chunks of any document whose one chunk was dropped.
- DiaASQ used a pre-modified version requiring no additional preprocessing; it has the longest questions (mean 109 chars) and shortest answers (mean 8 chars) among the suites.
- Baseline retrieval hyperparameters differ across BeamSearch, WaterCircles, and NaiveRetriever; BeamSearch and NaiveRetriever share a `single_step` reranker over the `dense_triplets` vector DB with threshold 0.5, but differ in `fetch_n` (25 vs 50), while WaterCircles uses no reranker and fixed triplet quotas (hyper 15, episodic 15, chain 25, other 6).
- The LLM-as-a-Judge used Qwen2.5 7B (Ollama) with deterministic decoding — `num_predict` 2048, `seed` 42, `temperature` 0.0, `top_k` 1 — and a 4-example few-shot prompt instructing binary 0/1 scoring of a generated answer against a ground-truth answer, with interrogative-word-awareness (e.g., "who" requires a person/animal, "how many" requires a number).

---

## Appendix C: Pseudocode

```text
Algorithm 1  PAI-2 QA pipeline

1:  Input: Q - user question; S_m - maximum number of search plan steps;
         C_m - maximum number of clue-queries per search step;
         V_m - maximum number of matched vertices to one entity;
         F_m - maximum number of triples after filtering per clue-query.
2:  Output: A - answer to user question.
3:  SubQuestions <- Preprocess(Q)                     ▷ {q1, q2, ..., qN}
4:  SubAnswers   <- NewList()
5:  for all qi ∈ SubQuestions do
6:      SearchPlan    <- InitialPlanGen(qi)           ▷ [s1, s2, ..., sM], where 0 ≤ M ≤ S_m
7:      StepsAnswers  <- NewList()
8:      SubAnswerFound <- False
9:      StepNum       <- 1
10:     while StepNum ≤ S_m do
11:         StepEntities        <- NER(SearchPlan[StepNum])
12:                                     ▷ [e1, e2, ..., eU]
13:         MatchedVertices     <- Entities2VerticesMatching(StepEntities, V_m)
14:                                     ▷ [[v11, v12, ..., v1Vm], ..., [vU1, vU2, ..., vUUVm]]  U×Vm
15:         AcceptedVerticesLists <- LinearCombination(MatchedVertices, C_m)
16:                                     ▷ V C_m×U
17:         ClueQueries   <- ClueQueriesGen(SearchPlan[StepNum], AcceptedVerticesLists)
18:                                 ▷ [cq1, cq2, ..., cqC_m]
19:         ClueAnswers   <- NewList()
20:         for all cqcj ∈ ClueQueries do
21:             RetrievedTriples <- KGraphTraverse(cqcj, AcceptedVerticesLists[j])
22:                                        ▷ {t1, t2, ..., tY}
23:             FilteredTriples  <- FilterByRelevance(RetrievedTriples)
24:                                        ▷ {t1, t2, ..., tF_m}
25:             caj <- ClueAnswerGen(cqcj, FilteredTriples)
26:             ClueAnswers <- ClueAnswers + caj
27:         end for
28:         saStepNum   <- SummarizeClueAnswers(SearchPlan[StepNum], ClueQueries, ClueAnswers)
29:         StepsAnswers <- StepsAnswers + saStepNum
30:         if Sufficient(qi, SearchPlan, StepsAnswers) then
31:             SubAnswerFound <- True
32:             break
33:         else
34:             SearchPlan <- SearchPlanEnhance(qi, SearchPlan, StepsAnswers)
35:                                     ▷ [s1, s2, ..., sK], where 0 ≤ M ≤ K ≤ S_m
36:             StepNum    <- StepNum + 1
37:             if StepNum - K then
38:                 break
39:             end if
40:         end if
41:     end while
42:     if SubAnswerFound then
43:         ai <- FinalizeSubAnswer(qi, SearchPlan, StepsAnswers)
44:     else
45:         ai <- NoAnswerStubGeneration(qi)
46:     end if
47:     SubAnswers <- SubAnswers + ai
48: end for
49: A <- AggregateSubAnswers(Q, SubQuestions, SubAnswers)
```

## Appendix D: Dataset Preprocessing Operations

| Dataset | Source | Original size | Preprocessing steps | Final subset |
|---|---|---|---|---|
| Natural Questions | HuggingFace `sentence-transformers/natural-questions`, "train" subset | 100,231 QA pairs (no documents, so `answer` column used as the related text) | (1) Filter QA pairs whose answer length is outside **64–1024 characters** → 67,174 remain; (2) take the **first 2,000** QA pairs; (3) expand with **2,000 randomly-selected answers** | **4,000** unique documents for graph construction |
| TriviaQA | HuggingFace `mandarjoshi/trivia_qa`, "rc.wikipedia/validation" subset | 7,993 QA pairs | (1) Chunk documents with LangChain `RecursiveCharacterTextSplitter` using: chunk size **1,024 chars**, separators `"\n\n"`, chunk overlap **64 chars**, `len` function, `is_separator_regex=False` → 278,384 unique chunks; (2) discard chunks with length outside **64–1024 chars** → 13,291 chunks remain; (3) coherence filter — if any chunk of a document was discarded, remove all remaining chunks of that document → 9,975 unique chunks; (4) select the **first 500** QA pairs | **4,925** unique chunks for graph construction |
| HotpotQA | HuggingFace `hotpotqa/hotpot_qa`, "distractor/validation" subset | 7,405 QA pairs, 13,781 unique documents | (1) Filter QA pairs whose associated document length is outside **64–1024 chars** → 13,291 documents remain; (2) take the **first 2,000** QA pairs | **3,933** unique documents for graph construction |
| 2WikiMultihopQA | GitHub `Alab-NII/2wikimultihop`, "dev" subset | 12,576 QA pairs, 56,687 unique documents | (1) Filter QA pairs whose document length is outside **64–1024 chars** → 49,299 documents remain; (2) take the **first 2,000** QA pairs | **4,596** unique documents for graph construction |
| MuSiQue | HuggingFace `dgslibisey/MuSiQue`, "validation" subset | 2,417 QA pairs, 21,100 unique documents | (1) Filter QA pairs whose context length is outside **64–1024 chars** → 19,867 documents remain; (2) take the **first 2,000** QA pairs; (3) expand with **2,000 randomly-selected documents** | **4,185** unique documents for graph construction |
| DiaASQ | GitHub `On-Point-RND/DiaASQ-2-QA` (modified version) | 5,698 QA pairs, 3,483 unique documents | No additional preprocessing/filtering applied | **3,483** documents used as-is |

**Table 24 (reproduced): Extended characteristics of datasets used for PAI-2 and baselines evaluation**

| Dataset | QA-pairs Amount | Questions length (chars) — median | Questions length — mean | Questions length — std | Answers length (chars) — median | Answers length — mean | Answers length — std | Relevant documents Amount | Docs length (chars) — median | Docs length — mean | Docs length — std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Natural Questions | 2000 | 44 | 47 | 11 | 515 | 534 | 218 | 3970 | 522 | 536 | 220 |
| TriviaQA | 500 | 66 | 76 | 39 | 9 | 10 | 6 | 4925 | 807 | 765 | 196 |
| HotpotQA | 2000 | 87 | 93 | 33 | 13 | 15 | 12 | 3933 | 384 | 414 | 201 |
| 2WikiMultihopQA | 2000 | 69 | 70 | 17 | 13 | 14 | 9 | 4596 | 300 | 362 | 227 |
| MuSiQue | 1931 | 89 | 96 | 37 | 14 | 17 | 13 | 4185 | 384 | 426 | 216 |
| DiaASQ | 5698 | 114 | 109 | 19 | 8 | 8 | 2 | 3483 | 556 | 613 | 324 |
| **Mean** | 2355 | 78 | 82 | 26 | 95 | 100 | 43 | 4182 | 492 | 519 | 231 |

**Interpretation (from the paper):**
- Longest- and shortest-average questions: **DiaASQ** (109 chars) and **Natural Questions** (47 chars), respectively.
- Shortest- and longest-average answers: **DiaASQ** (8 chars) and **Natural Questions** (534 chars), respectively.
- Longest- and shortest-average relevant documents: **TriviaQA** (765 chars) and **2WikiMultihopQA** (362 chars), respectively.
- Most- and least-relevant documents: **TriviaQA** (4,925) and **DiaASQ** (3,483), respectively.

## Appendix E: Retrieval Hyperparameters

**BeamSearch**

- `main_hyperparams`: `max_depth=5`, `max_paths=10`, `same_path_intersection_by_node=False`, `diff_paths_intersection_by_node=False`, `diff_paths_intersection_by_rel=False`, `mean_alpha=0.75`, `final_sorting_mode="mixed"`.
- `reranker_method="single_step"`.
- `reranker_config`: `vdb_name="dense_triplets"`, `threshold=0.5`, `fetch_n=25`.

**WaterCircles**

- `main_hyperparams`: `strict_filter=True`, `hyper_num=15`, `episodic_num=15`, `chain_triplets_num=25`, `other_triplets_num=6`, `do_text_pruning=False`.

**NaiveRetriever**

- `main_hyperparams`: `max_k=50`.
- `reranker_method="single_step"`.
- `reranker_config`: `vdb_name="dense_triplets"`, `threshold=0.5`, `fetch_n=50`.

## Appendix F: LLM-as-a-Judge Instructions

LLM inference was conducted with a **deterministic generation strategy** to ensure reproducibility. Applied hyperparameters: `num_predict=2048`, `seed=42`, `temperature=0.0`, `top_k=1`. The model is **Qwen2.5 7B** (from the Ollama repository). The judge is asked to evaluate whether the responses of the proposed method correctly answered the given questions, comparing a generated answer against a ground-truth answer using a 4-example few-shot prompt.

**Table 25 (reproduced): LLM prompts for LLM-as-a-Judge framework**

| Type | Prompt |
|---|---|
| **System** | You are an expert that evaluating the quality of the answer to the question. You are given: a [Question], a [Ground Truth Answer] that is definitely correct, and a [Generated Answer] that you must score as 0 or 1. A score of 1 means that the [Generated Answer] is correct, a score of 0 means that the [Generated Answer] is incorrect. You need to compare the [Generated Answer] with the [Ground Truth Answer], taking into account the [Question] itself. The [Ground Truth Answer] and the [Generated Answer] can be of different lengths and contain different amounts of information, so consider whether the answer is given to the interrogative word from the question: if in the [Question] asking "who", then the [Generated Answer] must name a person, character, or animal; if in the [Question] asking "how many", then the answer must contain a number.<br><br>Examples of [Questions], [Ground Truth Answer], [Generated Answer] and its corresponding [Score] are listed below:<br><br>**Example 1**<br>[Question]: Where does Everybody rank on the Hot Dance Club Songs chart?<br>[Ground Truth Answer]: Everybody climbs to number 3 on the Hot Dance Club Songs chart.<br>[Generated Answer]: 3rd place.<br>[Score]: 1<br><br>**Example 2**<br>[Question]: Which area has many populous villages?<br>[Ground truth answer]: In the area of the lands of Colchis.<br>[Generated answer]: There are many populous villages in this area.<br>[Score]: 0<br><br>**Example 3**<br>[Question]: How many volumes is the History of Rome published in?<br>[Ground Truth Answer]: The history of Rome is published in four volumes.<br>[Generated Answer]: Answer: In three volumes.<br>[Score]: 0<br><br>**Example 4**<br>[Question]: What kind of head did Michelangelo have?<br>[Ground Truth Answer]: Michelangelo had a round head.<br>[Generated Answer]: Michelangelo's head was round, his forehead was square, furrowed, and with pronounced brow ridges.<br>[Score]: 1 |
| **User** | [Question]: {q}<br>[Ground Truth Answer]: {gold_answer}<br>[Generated Answer]: {gen_answer} |
| **Assistant** | [Score]: |

**Covers:** Appendices C, D, E, and F of the paper (including Algorithms 1, Tables 24 and 25).
