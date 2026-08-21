> [[index|Wiki]] | [[summary|Summary]]

# PersonalAI 2.0 — Digest

The whole paper at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-related-work|Introduction and Related Work]]

**In one sentence:** PAI-2 is a GraphRAG framework that adds an LLM-planned, dynamic, multistage query-processing pipeline to knowledge-graph-backed LLM agents, and — by enabling adaptive iterative search guided by entities, matched vertices and clue-queries — beats LightRAG, RAPTOR and HippoRAG 2 on QA benchmarks (avg +4%), with the planning mechanism alone contributing +18% and graph traversal algorithms +6% over a flat retriever.

- PAI-2 introduces a dynamic, multistage query-processing pipeline for GraphRAG: adaptive, iterative information search guided by extracted entities, matched graph vertices and generated clue-queries, systematically decomposing complex queries into subqueries to retrieve only relevant KG segments.
- Evaluated on six benchmarks — Natural Questions, TriviaQA, HotpotQA, 2WikiMultihopQA, MuSiQue and DiaASQ — PAI-2 outperforms LightRAG, RAPTOR and HippoRAG 2, achieving superior results on 4 of 6 benchmarks with an average +4% LLM-as-a-Judge gain, reducing hallucination and increasing precision.
- Ablation: the search-plan enhancement mechanism yields a +18% LLM-as-a-Judge boost across all six datasets versus disabled; graph traversal algorithms (BeamSearch, WaterCircles) gain +6% on average over a standard flat retriever.
- On the MINE-1 benchmark PAI-2 reaches SOTA with 89% information-retention score; its memory construction is more stable (fewer LLM parsing errors) than KGGen and Wikontic in the 7–14B LLM tier.
- The five stated contributions are: (1) a GraphRAG method fusing graph-based external memory for unstructured text with LLM-planned search/traversal; (2) the six-benchmark evaluation vs LightRAG/RAPTOR/HippoRAG 2; (3) demonstration of the +18% plan-enhancement effect; (4) demonstration of the +6% graph-traversal advantage; (5) the MINE-1 SOTA result and memory-construction stability.
- Related work surveyed: PersonalAI 1.0 (PAI-1), Think-on-Graph (ToG), Reasoning on Graphs (RoG), Debate on Graph (DoG), Pyramid-Driven Alignment (PDA), and Pseudo-Graph Generation & Atomic Knowledge Verification (PG&AKV) — each pairing LLMs with KGs but with distinct trade-offs (scalability, faithfulness, latency, computational overhead).
- Core motivation: traditional GraphRAG relies on node-level retrievals with static ontology and inefficient traversal, struggling with multi-hop reasoning where the search strategy must adapt to intermediate discoveries.

## 2. [[wiki/02-methods-pai2-pipeline|Methods: PAI-2 Pipeline]]

**In one sentence:** PAI-2 answers questions over a memory (knowledge) graph by decomposing the question into sub-questions and then, for each, iteratively generating, validating, and enhancing natural-language search plans whose steps drive entity-grounded graph traversal, triplet relevance filtering, and progressive summarization until either a sufficient answer is produced or a "No Answer" stub is emitted.

- The QA pipeline has thirteen stages, most of which can be executed in parallel across sub-questions and clue-queries; it draws from PAI-1 but introduces a dynamic planning mechanism instead of relying on direct node-level retrievals and static pre-defined ontologies.
- Stage 1, `Preprocess(q) = Decompose(Enhance(Denoise(q)))`, denoises, enhances, and decomposes a composite question into independently answerable sub-questions {q_1…q_N}.
- For each sub-question, `InitialPlanGen(q)` produces an initial exploration plan P = [s_1…s_M] of natural-language search steps; entities E_j are extracted from each step via NER and matched to object vertices V with a per-entity cap V_m using dense and sparse retrieval models (BM25, DRMs, dual-tower and single-tower).
- A `LinearCombination` over the matched vertices selects the first C_m vertex groups, from which LLM-generated clue-queries CQ_j reformulate the search step with respect to each vertex group.
- Each clue-query drives independent graph traversal, `KGraphTraverse(cq_l, V[l])`, accumulating raw triples, which are then pruned by `FilterByRelevance(s, T_raw)` to keep the F_m closest triples.
- Evidence is aggregated in two steps: per-clue `ClueAnswerGen` followed by `SummarizeClueAnswers` to yield step knowledge sa_j.
- A decision loop checks accumulated knowledge SA: if sufficient, a sub-answer is generated; if not, the plan is enhanced and the pipeline loops back to entity extraction, until the search limit is exceeded and a "No Answer" stub is returned.
- Stage 13 aggregates all sub-answers into the final response via `AggregateSubAnswers`.

## 3. [[wiki/03-experimental-setup-and-evaluation|Experimental Setup and Evaluation]]

**In one sentence:** PAI-2 is evaluated against four baselines on six QA benchmarks (100 QA pairs each, 90 configurations total) using a validated LLM-as-a-Judge framework (Qwen2.5 7B) plus RAGAS Context Relevance, Faithfulness and Groundedness, with the LLM backbone chosen by a few-shot ablation on HotpotQA that favored Qwen2.5 7B.

- Three research questions drive the evaluation: RQ1 — whether PAI-2 achieves superior results compared to baselines; RQ2 — whether graph traversal algorithms improve PAI efficiency compared to PAI with a naive flattened retriever; RQ3 — how PAI-2 efficiency varies with the number of generating clue-queries per step of the search plan.
- LLM backbone selection used few-shot evaluation on HotpotQA over four 7–9B models (Qwen2.5 7B, Llama3.1 8B, Granite3.3 8B, Gemma2 9B); Qwen2.5 7B was the best across all four metrics and is used in the main experiments, with the same LLM used for both response generation and memory graph construction.
- Vector representations combine dense and sparse embeddings (`intfloat/multilingual-e5-large` + BM25); graph traversal uses two algorithm combinations from PAI-1 — "BS + WC" (BeamSearch + WaterCircles) and "BS + NR" (BeamSearch + NaiveRetriever).
- Each PAI-2 configuration was evaluated on 100 QA pairs from each of the six benchmarks, yielding 15 distinct QA configurations per dataset and 90 QA configurations in total, plus 44 configurations for the LLM few-shot ablation; six memory graphs were constructed, at ≈1.63 documents/minute average ingestion speed.
- Evaluation rejects BLEU/ROUGE/Meteor/BERTScore, adopting LLM-as-a-Judge (Qwen2.5 7B) plus RAGAS Context Relevance, Faithfulness and Groundedness.
- Judge reliability was validated against human annotation with Overlap-3, giving Krippendorff's α = 0.935 and Pearson r = 0.86 vs majority-vote human annotations.
- Baselines are LightRAG, RAPTOR, HippoRAG 2, and PAI-1, each with its own recommended embedder; infrastructure is Neo4j + Qdrant + OpenSearch + Redis/MongoDB in Docker, LLMs served via local Ollama on a single NVIDIA TITAN RTX 24GB GPU.

## 4. [[wiki/04-experiments-and-results|Experiments and Results]]

**In one sentence:** PAI-2 outperforms LightRAG, RAPTOR, and HippoRAG 2 by a 4% average LLM-as-a-Judge gain on three of six benchmarks (TriviaQA, 2WikiMultihopQA, MuSiQue) and improves on PAI-1 by 27%/26%/10% on Context Relevance/Faithfulness/LLM-as-a-Judge, with ablations showing the search-plan enhancement mechanism contributes 18%, graph traversal a 5–6% edge over flat retrieval, more clue-queries (1→8) a 4% gain, and episodic-triple exclusion mitigating "Lost in the Middle."

- PAI-2 achieves a 4% average gain by LLM-as-a-Judge on 3 out of 6 benchmarks; on HotpotQA and DiaASQ it is only comparable to HippoRAG 2 and PAI-1.
- PAI-2's best setup reaches 0.82 mean LLM-as-a-Judge, vs 0.57 for HippoRAG 2, 0.42 for RAPTOR, and 0.16 for LightRAG.
- Disabling the search plan enhancement mechanism degrades answer accuracy by 18% by LLM-as-a-Judge.
- Compared to PAI-1, PAI-2's QA pipeline improves answers by 27% (Context Relevance), 26% (Faithfulness), and 10% (LLM-as-a-Judge).
- Graph traversal algorithms show an average 5% increase over the standard flattened retriever in both PAI-1 and PAI-2.
- Increasing the maximum number of clue-queries from 1 to 8 yields an average 4% gain.
- TriviaQA is the easiest benchmark and MuSiQue the most difficult (0.68 vs 0.20 average LLM-as-a-Judge across methods' best setups).
- The Memorize pipeline achieves SOTA 89% information-retention score on the MINE benchmark.

## 5. [[wiki/05-conclusions-limitations-future-work|Conclusions, Limitations, Future Work]]

**In one sentence:** PAI-2 combines LLM capabilities with graph-based external memory to outperform LightRAG, RAPTOR, and HippoRAG 2 on six QA benchmarks and achieve SOTA information retention on MINE-1, while acknowledging four concrete memory-design limitations that the authors propose to fix via thesis vertex labeling, time interval specification, and fixed predicate fields.

- PAI-2 integrates LLMs with graph-based external memory for knowledge retrieval and reasoning, addressing GraphRAG's inefficiencies in traversing complex knowledge graphs.
- Across six benchmarks, PAI-2 achieved an average 4% LLM-as-a-Judge improvement on 4 out of 6 benchmarks.
- Ablations: search plan enhancement gave an 18% boost, advanced graph traversal algorithms gave a 6% boost in retrieval precision.
- The memory construction algorithm was more stable than KGGen and Wikontic in the 7–14B tier, and SOTA on MINE-1 (89% information retention).
- Limitations: (1) implicit temporal representation risking "Lost in the Middle" data loss; (2) simplified ontology with limited indexing/filtering; (3) ambiguous entity definitions forcing extensive traversals; (4) lack of semantic deduplication (only exact string matching).
- Future work: dual labeling of thesis vertices (Episode: FACT/OPINION/PREDICTION; Temporal: STATIC/DYNAMIC/ATEMPORAL), explicit timestamp fields per vertex, and fixed predicate fields from a verified glossary.
- The authors position PAI-2 as a substantial step toward next-generation intelligent agents with reliable factual outputs.
- Ethics: GigaChat Max was used to improve manuscript language; authors took full responsibility after review.

## 6. [[wiki/06-appendix-prompts-pipeline-stages|Appendix: Prompts for Pipeline Stages]]

**In one sentence:** This appendix gives the exact prompt templates (System/User/Assistant) used at every LLM stage of the PAI-2 QA pipeline — 7 query-preprocessing prompts (Appendix A, Tables 7–13) and 10 memory-graph exploration/answer-aggregation prompts (Appendix B, Tables 14–23).

- The 17 prompt tables split into two appendices: Appendix A — query preprocessing (Tables 7–13, 7 stages); Appendix B — memory-graph exploration and answer aggregation (Tables 14–23, 10 stages).
- Appendix A stages: grammar correction, noise removal, grammatical editing, rephrasing with precise terminology, rephrasing/expanding for search-clarity, decomposability detection, and question decomposition.
- Appendix B stages: search-plan generation, NER from a plan step, clue-question generation, clue-answer generation from triplets, clue-answer summarization, sufficiency check, final answer generation, plan-enhancement check, plan-step enhancement, and sub-answer aggregation.
- All System prompts share a common discipline: no external knowledge, preserve key entities/numbers/units/dates, preserve original language/style, output only the specified block(s).
- Decision-style stages force a strict True/False verdict with a Chain-of-thoughts justification; evidence-dependent stages fall back to sentinel tokens `<|NoRelevantInfo|>` and `<|NotEnoughtInfo|>`.
- User messages are thin payload wrappers using runtime placeholders (`{query}`, `{matched_entities}`, `{search_info}`, etc.); the Assistant row names the expected output block.
- Every prompt table is self-contained with 1–2 few-shot examples over banking/telecom/consumer entities.
- Search-plan prompts encode the independence requirement: plan steps must be answerable without knowing other steps' contents, and fully dependent plans collapse to a single step.

## 7. [[wiki/07-appendix-pseudocode-datasets-hyperparams-judge|Appendix: Pseudocode, Datasets, Hyperparameters, Judge]]

**In one sentence:** This appendix documents the PAI-2 QA pipeline algorithm (pseudocode), the exact preprocessing operations and resulting statistics for the six evaluation datasets, the retrieval hyperparameters of the three baseline systems, and the full LLM-as-a-Judge prompt set and decoding config used for answer scoring.

- The PAI-2 pipeline (Algorithm 1) is an iterative search-plan loop: generate a plan, then per step extract entities, match graph vertices, generate clue-queries, traverse, filter triples, generate clue answers, and either stop, enhance the plan, or emit a finalized sub-answer/no-answer stub, with sub-answers aggregated into the final answer.
- The four main complexity/depth bounds are S_m (max search-plan steps), C_m (max clue-queries per step), V_m (max matched vertices per entity), and F_m (max filtered triples per clue-query).
- All six datasets were reduced to evaluation subsets via a 64–1024 character length filter plus first-N selection; TriviaQA additionally required chunking with a coherence-drop rule.
- DiaASQ needed no additional preprocessing; it has the longest questions and shortest answers among the suites.
- Baseline retrieval hyperparameters differ across BeamSearch, WaterCircles, and NaiveRetriever (rerankers, fetch_n, triplet quotas).
- The LLM-as-a-Judge used Qwen2.5 7B with deterministic decoding (temperature 0.0, seed 42) and a 4-example few-shot prompt for binary 0/1 scoring, with interrogative-word-awareness.

## 8. [[wiki/08-appendix-graph-stats-ablations-mine1-humaneval|Appendix: Graph Stats, Ablations, MINE-1, Human Evaluation]]

**In one sentence:** This appendix documents the structural and cost characteristics of PAI-2's constructed memory graphs, the non-aggregated clue-queries-number ablation results, PAI-2's MINE-1 information-retention evaluation (89% vs 86% best baseline), and human-evaluation agreement metrics for PAI-2 and HippoRAG 2.

- Six memory graphs were constructed with Qwen2.5 7B over QA datasets; on average one graph holds 4,181 episodic, 36,151 thesis, 72,618 object and 147,523 hyper vertices plus 124,815 simple object-object edges.
- Constructing a ~4,182-document memory graph requires ≈7.5M LLM tokens, ≈46.25 hours and ≈2.01GB of disk space.
- LLM parsing errors during construction are minimal (0.02%–0.08% lost documents; 0% for three of the six datasets).
- In the clue-queries-number ablation, allowing up to 6–8 clue queries per search-plan step yields the best LLM-as-a-Judge scores.
- On MINE-1, PAI-2 retains 89% of factual information, beating Wikontic's 86%, GraphRAG's 44%, and all KGGen configurations.
- The MINE-1 vertex-type ablation shows best retention (95% mean) when object, thesis, and episodic vertex triples are all accepted; restricting to object+thesis degrades it by ~10%.
- Human evaluation agrees strongly with LLM-as-a-Judge: Krippendorff's alpha 0.93 (PAI-2) and 0.94 (HippoRAG 2), Pearson correlation 0.88 vs 0.84.

## The argument in five moves

1. Flat, node-level GraphRAG retrieval can't adapt mid-search, so it struggles on multi-hop questions that need iterative discovery.
2. PAI-2 fixes this by having the LLM write, check, and revise a natural-language search plan as it traverses the graph, generating clue-queries at each step.
3. Tested on six QA benchmarks against LightRAG, RAPTOR, HippoRAG 2, and predecessor PAI-1, PAI-2 wins on average (+4% LLM-as-a-Judge), with the planning mechanism alone worth +18% and better traversal algorithms worth +6%.
4. On a separate information-retention benchmark (MINE-1), PAI-2's graph-construction step also beats prior methods (89% vs 86%), with fewer parsing errors.
5. The authors are candid about four remaining weaknesses in their memory design — temporal representation, ontology structure, entity disambiguation, and deduplication — and propose concrete fixes as future work.
