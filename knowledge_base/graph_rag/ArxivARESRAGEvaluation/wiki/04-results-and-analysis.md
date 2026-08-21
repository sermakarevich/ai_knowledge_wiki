> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Results & Analysis

**In one sentence:** ARES ranks RAG systems more accurately than RAGAS (Kendall's τ 0.065 higher for context relevance, 0.132 higher for answer relevance) and more data-efficiently than sampled annotations (0.08 higher τ on average with 78% fewer annotations), reliably distinguishes faithful from hallucinated answers on AIS, and the paper concludes that ARES beats RAGAS while admitting limitations around small annotation sets, ~32GB GPU requirements, and an English-only evaluation scope.

## Key points

- ARES averages a Kendall's τ of 0.065 higher than RAGAS for context relevance and 0.132 higher for answer relevance across datasets from KILT and SuperGLUE, with DeBERTa-v3-Large as the pretrained basis for the judges.
- In triple-level scoring, ARES with the fine-tuned LLM judge is 59.9 percentage points higher than RAGAS on context relevance and 14.4 percentage points higher on answer relevance.
- Against a sampled-annotations benchmark (150 datapoints per mock RAG system, totaling 1,350 annotations), ARES achieves a Kendall's τ 0.08 higher on average across context and answer relevance while using 78% fewer annotations.
- Compared to a few-shot GPT-3.5 judge (gpt-3.5-turbo-16k) using the same 300-datapoint PPI validation set, ARES ranks RAG systems 0.06 Kendall's τ higher on average over both context and answer relevance.
- PPI improved the ranking prediction accuracy of the fine-tuned LLM judge on all datasets tested; ARES requires only 150 human annotations as the minimum (tested sets ranged 25–400).
- On the AIS attribution benchmark, ARES gets within 2.5 accuracy points of the correct scores (Split Prediction 0.478 WoW / 0.835 CNN/DM vs. Correct 0.458 / 0.859) using only 200 human-preference datapoints.
- On existing RAG systems (BM25, OpenAI Ada, ColBERTv2 retrievers with MPT-7b-Instruct, GPT-3.5-Turbo, GPT-4, plus Facebook RAG), ARES averages Kendall's τ 0.91 (context relevance) and 0.97 (answer relevance), beating RAGAS by 0.16 and 0.15 respectively; PPI confidence intervals captured ground truth over 95% of the time (7.4 points wide for context, 6.1 for answer relevance); best retriever was ColBERTv2 and best generative LLM was GPT-4.
- Cross-domain limits: the NQ-fine-tuned judge generalizes well across KILT/SuperGLUE shifts, but drastic shifts fail — 0.33 Kendall's τ on XGLUE (cross-lingual), 0.28 on CodeSearchNet (text-to-code), 0.38 on T-Rex (entity extraction) — while limitations include the 150–300 annotation minimum, ~32GB GPUs for DeBERTa-v3-Large (304M) and FLAN-T5-XXL (11.3B), and English-only datasets.

---

## Main Results (Table 1)

Table 1 reports Kendall's tau (ranking) and triple-level accuracy for context relevance (C.R.) and answer relevance (A.R.) across six datasets (NQ, HotpotQA, WoW, FEVER, MultiRC, ReCoRD) for five systems: Sampled Annotations, RAGAS, GPT-3.5 Judge, ARES LLM Judge (without PPI), and ARES (with PPI). Setup: ARES uses DeBERTa-v3-Large judges; the GPT-3.5 judge uses few-shot prompts (Appendices A.2–A.4); both ARES and the GPT-3.5 judge use PPI with a 300-datapoint human preference validation set; GPT-3.5 was chosen over GPT-4 for lower financial cost.

| System | NQ C.R. | NQ A.R. | HotpotQA C.R. | HotpotQA A.R. | WoW C.R. | WoW A.R. | FEVER C.R. | FEVER A.R. | MultiRC C.R. | MultiRC A.R. | ReCoRD C.R. | ReCoRD A.R. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kendall's Tau — Sampled Annotations | 0.83 | 0.89 | 0.78 | 0.78 | 0.78 | 0.83 | 0.89 | 0.89 | 0.83 | 0.83 | 0.72 | 0.94 |
| Kendall's Tau — RAGAS | 0.89 | 0.89 | 0.94 | 0.89 | 0.94 | 0.94 | 0.72 | 0.61 | 0.83 | 0.94 | 0.89 | 0.44 |
| Kendall's Tau — GPT-3.5 Judge | 0.89 | 0.94 | 0.67 | 0.94 | 0.94 | 0.89 | 0.78 | 0.78 | 0.83 | 0.89 | 0.83 | 0.94 |
| Kendall's Tau — ARES LLM Judge (no PPI) | 0.89 | 1.0 | 0.89 | 0.94 | 0.94 | 1.0 | 0.83 | 0.72 | 0.94 | 0.83 | 0.78 | 0.83 |
| Kendall's Tau — ARES | 0.94 | 1.0 | 0.94 | 0.94 | 1.0 | 1.0 | 0.89 | 0.78 | 0.94 | 0.89 | 0.83 | 0.89 |
| RAGAS Accuracy | 31.4% | 71.2% | 17.2% | 76.0% | 36.4% | 77.8% | 23.7% | 69.2% | 16.1% | 75.0% | 15.0% | 72.8% |
| GPT-3.5 Judge Accuracy | 73.8% | 95.5% | 75.3% | 71.6% | 84.3% | 85.2% | 60.4% | 59.6% | 72.4% | 60.3% | 81.0% | 65.8% |
| ARES Accuracy | 79.3% | 97.2% | 92.3% | 81.3% | 85.7% | 96.1% | 88.4% | 78.5% | 85.8% | 82.7% | 67.8% | 92.3% |

Headline numbers: ARES ranked RAG systems more accurately than RAGAS and the GPT-3.5 judge across all explored datasets; ARES's Kendall's tau was 0.065 higher on average for context relevance and 0.132 higher on average for answer relevance than RAGAS; PPI boosted the ranking accuracy of the ARES LLM judge across the board.

## AIS Attribution Results (Table 2)

| Metric | WoW | CNN / DM |
|---|---|---|
| ARES Split Prediction | 0.478 | 0.835 |
| Correct Positive/Negative Split | 0.458 | 0.859 |
| ARES Judge Accuracy | 62.5% | 84.0% |
| Evaluation Set Size | 707 | 510 |
| Human Preference Data Size | 200 | 200 |

To evaluate whether ARES can gauge answer faithfulness in real RAG systems, the authors tested ARES on the AIS attribution benchmark (Rashkin et al., 2022). They selected the Wizards of Wikipedia (WoW) and CNN/DM datasets, excluding ToTTo (table reasoning) and QRECC (passage summarization). Each evaluation example includes a query, a retrieved passage, and a generated answer that is either faithful or non-attributed to the retrieved passage. ARES effectively scores the AIS datasets, getting within 2.5 accuracy points of the correct scores, using only 200 annotated datapoints for the human preference validation set. These results demonstrate ARES's ability to reliably distinguish faithful and hallucinated answers in real-world RAG systems.

## Ranking accuracy and system comparison

For the few-shot GPT-3.5 judge, the authors provide few-shot examples guiding predictions (prompts in Appendices A.2, A.3, A.4), and for both ARES and the GPT-3.5 judge they augment the LLM with PPI using a 300-datapoint human preference validation set to rectify ML predictions and produce confidence intervals.

- ARES is more accurate than RAGAS in ranking across almost all KILT and SuperGLUE settings: +0.065 Kendall's τ on context relevance and +0.132 on answer relevance, averaging to a 59.9-point context-relevance and 14.4-point answer-relevance advantage over RAGAS in triple-level scoring.
- The LLM judge is substantially more accurate than RAGAS at predicting context relevance and answer relevance of a query-passage-answer triple.
- PPI improved the fine-tuned LLM judge's ranking prediction accuracy on all datasets tested (compared against ARES LLM Judge without PPI in Table 1).
- Sampled-annotations ablation: sampling 150 datapoints per mock RAG system (1,350 total annotations) still leaves ARES 0.08 higher in Kendall's τ on average across both context and answer relevance, despite using 78% fewer annotations. ARES is significantly more data-efficient with human annotations while scoring more accurately than standard sampled annotation methods.
- Vs. GPT-3.5 judge: ARES is 0.06 Kendall's τ higher on average over both metrics; the fine-tuned ARES judge distinguishes RAG systems more precisely and guides configuration decisions around document splitting, retriever selection, and generative LLM choice. The GPT-3.5 judge is more readily deployable (no fine-tuning) but carries variable querying costs based on date of querying and total tokens used.

### Human annotation requirements (Tables 3–4)

Two experiment sets quantify the role of human annotations: (1) ARES with human annotation sets ranging from 25 to 400 datapoints found 150 to be the minimum required (Table 3); (2) testing whether GPT-4 generations could replace human annotations entirely found GPT-4 worse than humans in this role, though the idea arguably has promise (Table 4).

### Ranking existing RAG systems (Section 5.3)

The authors evaluated whether ARES can score and rank existing RAG systems. Datasets: NQ, WoW, and FEVER from KILT; answer generations count as correct if they contain the KILT answer in their output. RAG systems: three retrievers — BM25, OpenAI Ada embeddings with cosine similarity search, and ColBERTv2 (Santhanam et al., 2022) — and three generative LLMs — MPT-7b-Instruct (Team, 2023), GPT-3.5-Turbo, and GPT-4 — plus the Facebook RAG model (Lewis et al., 2020) with a DPR retriever (Karpukhin et al., 2020) and a BART sequence-to-sequence model (Lewis et al., 2019). Each RAG system retrieves only one passage during retrieval.

Results (Table 5): ARES reliably scores and ranks real-world RAG systems, averaging Kendall's τ 0.91 for context relevance and 0.97 for answer relevance. Compared to RAGAS, ARES is 0.16 higher for context relevance and 0.15 higher for answer relevance on average. ARES provided accurate confidence bounds, capturing the ground-truth average outcomes for context relevance and answer relevance more than 95% of the time; PPI confidence intervals averaged 7.4 points wide for context relevance and 6.1 points wide for answer relevance (Figures 2 and 3 show ARES vs. RAGAS). Among models tested, the best performing retriever was ColBERTv2 and the best performing generative LLM was GPT-4.

### Strengths and limits of cross-domain applications (Section 5.4)

The generalizability of the ARES LLM judge is critical for deployment in specialized domains where in-domain queries, documents, and answers are difficult to gather. The authors tested three domain shifts: change in query type from training to test (e.g. NQ to FEVER), change in document type (e.g. NQ to MultiRC), and change in both query and document type (e.g. NQ to ReCoRD).

Findings (Table 6): the fine-tuned LLM judges proved successful in cross-domain applications. Across all settings, ARES judges had strong generalizability even with only 300 datapoints in the human preference validation set for PPI. Even when the judge's accuracy suffered in cross-domain applications, PPI helped mitigate the loss and kept ARES successful; additional PPI examples continued to boost cross-domain performance in subsequent tests.

Limits: LLM judges fail on more drastic domain shifts — switching languages (English to Spanish, German, etc.), text to code (questions + passages to coding functions + documentation), and text retrieval to extraction of entities, webpages, or citations. Quantified: an NQ-fine-tuned judge scored Kendall's τ 0.33 (XGLUE, cross-lingual; Liang et al., 2020), 0.28 (CodeSearchNet, text-to-code; Husain et al., 2019), and 0.38 (T-Rex from KILT, extraction; Elsahar et al., 2018; Petroni et al., 2021) over both context and answer relevance. Each cross-domain shift requires in-domain passages and few-shot query examples for reconfiguring ARES judges.

## Conclusion

In this work, the authors present ARES, a novel automated evaluation framework for retrieval-augmented generation (RAG). ARES offers a novel training pipeline for fine-tuning lightweight LLM judges on synthetically generated queries and answers. ARES can evaluate each component of a RAG system separately to help improve system understanding and create targeted solutions, and it requires only minimal human annotations. For the eight different datasets in KILT, SuperGLUE, and AIS requiring RAG-based solutions, ARES can accurately score and rank RAG systems based on context relevance, answer faithfulness, and answer relevance scores, beating the existing RAGAS automated evaluation framework.

ARES is a flexible framework, and there may be variants even more powerful than the ones explored. Avenues to explore include GPT-4 as a replacement for human labeling (Table 4), more robust techniques for the synthetic datasets used in fine-tuning LLM judges, utilizing logits in LLM judge prediction to improve PPI confidence intervals, and testing more sophisticated LLMs as fine-tuned judges for ARES.

## Limitations

ARES relies on a small set of annotations in the human preference validation set (roughly 150–300 datapoints, but more is better). These annotations often require an annotator familiar with the RAG system's domain application: while easy to generate for general-domain applications, more specialized domains such as law, medicine, and finance may require annotators with specialized expertise.

The LLMs used in ARES benefit substantially from GPU-based hardware with substantial storage. DeBERTa-v3-Large (304M) and FLAN-T5-XXL (11.3B) required GPUs with about 32GB of memory to run, taking several hours for fine-tuning and generation, respectively. While commercial GPUs are widely available, they are not easily accessible to all NLP researchers and practitioners due to their costs.

All datasets used in the evaluation of ARES are in English, a well-resourced language with abundant annotations. Future work should explore how ARES can be employed in other languages by utilizing different LLMs for the ARES judge and the synthetic data generation, which can help better understand the strengths and weaknesses of the current ARES framework.

**Covers:** Section 5 "Results & Analysis" (Tables 1-2), Section 6 "Conclusion", Section 7 "Limitations" — arXiv 2311.09476, pages 6-9
