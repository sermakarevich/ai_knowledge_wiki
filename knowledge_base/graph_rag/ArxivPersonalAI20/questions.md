> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# PersonalAI 2.0 — Retrieval Practice

Answer from memory first, then expand to check. Covers all 8 wiki pages.

1. What is the single biggest lever behind PAI-2's accuracy gains — is it the graph-traversal algorithm or something else, and by how much?

<details><summary>Answer</summary>
The search-plan enhancement (planning) mechanism, not the traversal algorithm. Disabling it costs an average 18% LLM-as-a-Judge score across all six benchmarks, versus a 6% gain from better graph-traversal algorithms (BeamSearch/WaterCircles) over a flat retriever. See [[wiki/01-introduction-and-related-work|Introduction & Related Work]] and [[wiki/04-experiments-and-results|Experiments & Results]].
</details>

2. Walk through the 13-stage PAI-2 pipeline: what happens between a plan step being written and a sub-answer being produced?

<details><summary>Answer</summary>
Entities are extracted from the plan step (NER) and matched to graph vertices; a `LinearCombination` selects the top vertex groups; clue-queries are generated per vertex group; each clue-query drives independent graph traversal (`KGraphTraverse`), producing raw triples that get filtered for relevance; per-clue answers are generated then summarized into step knowledge; a decision loop checks sufficiency — if sufficient, a sub-answer is generated; if not, the plan is enhanced and the loop repeats (up to a step limit), else a "No Answer" stub is emitted. See [[wiki/02-methods-pai2-pipeline|Methods: PAI-2 Pipeline]].
</details>

3. Which four baseline systems is PAI-2 compared against, and which embedding model does each use?

<details><summary>Answer</summary>
LightRAG (`BAAI/bge-m3`), RAPTOR (`sentence-transformers/multi-qa-mpnet-base-cos-v1`), HippoRAG 2 (`facebook/contriever`), and PAI-1 (fusion of `intfloat/multilingual-e5-large` and BM25). See [[wiki/03-experimental-setup-and-evaluation|Experimental Setup & Evaluation]].
</details>

4. How did the authors validate that their LLM-as-a-Judge scoring was trustworthy?

<details><summary>Answer</summary>
They ran human annotation with Overlap-3 (three overlapping annotators) on the best PAI-2 and HippoRAG 2 setups, obtaining Krippendorff's α = 0.935 and a Pearson correlation r = 0.86 between judge scores and majority-vote human annotations. See [[wiki/03-experimental-setup-and-evaluation|Experimental Setup & Evaluation]].
</details>

5. On which benchmarks does PAI-2 actually win, and where is it merely comparable to baselines?

<details><summary>Answer</summary>
PAI-2 wins with a ~4% average LLM-as-a-Judge gain on TriviaQA, 2WikiMultihopQA, and MuSiQue. On HotpotQA and DiaASQ it's only comparable to HippoRAG 2 and PAI-1 (6% and 1% differences respectively). See [[wiki/04-experiments-and-results|Experiments & Results]].
</details>

6. What is PAI-2's improvement over its own predecessor, PAI-1, and on which metrics?

<details><summary>Answer</summary>
An average 27% improvement in Context Relevance, 26% in Faithfulness, and 10% in LLM-as-a-Judge score. See [[wiki/04-experiments-and-results|Experiments & Results]].
</details>

7. Name the four concrete limitations the authors admit in their memory design, and what fix is proposed for each.

<details><summary>Answer</summary>
(1) Implicit temporal representation (timestamps as plain text, risking "Lost in the Middle" loss) → explicit timestamp fields per vertex (t_created, t_valid, t_expired, t_invalid, invalidated_by). (2) Simplified ontology with limited indexing/filtering → no direct fix stated beyond noting it. (3) Ambiguous entity definitions causing extensive traversal → dual vertex labeling (Episode: FACT/OPINION/PREDICTION; Temporal: STATIC/DYNAMIC/ATEMPORAL) and entity metadata. (4) Lack of semantic deduplication (only exact string match) → fixed predicate fields drawn from a verified, periodically updated glossary. See [[wiki/05-conclusions-limitations-future-work|Conclusions, Limitations & Future Work]].
</details>

8. What sentinel tokens does the pipeline use when a stage can't find relevant information or has insufficient information, and in which prompt stages do they appear?

<details><summary>Answer</summary>
`<|NoRelevantInfo|>` (no relevant fact found) and `<|NotEnoughtInfo|>` (insufficient information to answer confidently — note the original spelling). These appear in evidence-dependent stages such as clue-answer generation (Table 17) and summarization (Table 18). See [[wiki/06-appendix-prompts-pipeline-stages|Appendix: Prompts for Pipeline Stages]].
</details>

9. What are S_m, C_m, V_m, and F_m in the PAI-2 algorithm, and what do they each bound?

<details><summary>Answer</summary>
S_m = max search-plan steps, C_m = max clue-queries per step, V_m = max matched vertices per entity, F_m = max filtered triples per clue-query. Together they bound the depth/breadth of the iterative search. See [[wiki/07-appendix-pseudocode-datasets-hyperparams-judge|Appendix: Pseudocode, Datasets, Hyperparameters, Judge]].
</details>

10. Roughly how expensive is it to build one memory graph (tokens, time, disk), and how error-prone is the process?

<details><summary>Answer</summary>
Constructing a graph from ~4,182 documents takes ≈7.5M LLM tokens, ≈46.25 hours, and ≈2.01GB of disk space; LLM parsing errors are minimal (0.02%–0.08% of documents lost, 0% on three of the six datasets). See [[wiki/08-appendix-graph-stats-ablations-mine1-humaneval|Appendix: Graph Stats, Ablations, MINE-1, Human Eval]].
</details>

11. On the MINE-1 benchmark, how does PAI-2's information-retention score compare to the best baseline, and what vertex-type configuration gets the best result?

<details><summary>Answer</summary>
PAI-2 with Qwen2.5 7B retains 89% of factual information, beating Wikontic's best of 86%; the best configuration (95% mean retention) accepts triples incident to object, thesis, AND episodic vertices — restricting to just object+thesis triples degrades retention by ~10%. See [[wiki/08-appendix-graph-stats-ablations-mine1-humaneval|Appendix: Graph Stats, Ablations, MINE-1, Human Eval]].
</details>

12. Which prior LLM+KG methods does the paper survey as related work, and what's each one's core limitation according to the authors?

<details><summary>Answer</summary>
PAI-1 (memory-representation focus, limited scalability/open-domain applicability), Think-on-Graph/ToG (depends on KG integrity, limited adaptability), Reasoning on Graphs/RoG (relies on manual annotations), Debate on Graph/DoG (computational overhead), Pyramid-Driven Alignment/PDA (depends on precise hierarchical organization), and PG&AKV (extra LLM computation adds latency). See [[wiki/01-introduction-and-related-work|Introduction & Related Work]].
</details>
