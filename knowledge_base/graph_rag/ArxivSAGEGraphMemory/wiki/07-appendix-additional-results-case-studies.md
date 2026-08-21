> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix P–R: Additional Results, Case Studies, Datasets, Baselines, and Paper Backmatter

**In one sentence:** This tail of the paper adds the full retrieval-perf tables for multi-hop QA, AmazonQA, and HaluMem (with SAGE's zero-shot rows marked), a concrete HotpotQA path-interpretation case study showing how SAGE aligns entity aliases to satisfy both question constraints, then closes with the dataset statistics, baseline families and metrics of the evaluation suite, plus the limitations, broader impact, compute (8× A100), licenses, and NeurIPS checklist.

## Key points

- SAGE's document-level retrieval results on the three multi-hop QA benchmarks (Table 9): HotpotQA R@2 = 65.1 / R@5 = 77.6, MuSiQue R@2 = 43.2 / R@5 = 53.1, 2WikiMultiHopQA R@2 = 83.6 / R@5 = 88.6, with average rank 7.0 across compared methods.
- On AmazonQA (Table 10, original full-test protocol; BLEU1/2/3/4 and ROUGE), the only numeric row present in the excerpt is the original protocol's neural baseline R-Net (IJCAI'19) at B-1 47.04, B-2 40.32, B-3 31.48, B-4 23.92, R 40.22; SAGE's rows are the only zero-shot ones and are marked **[0-shot]**.
- The HaluMem-Medium results (Table 11) span three metric groups — Memory Extraction (R, W-R, T-P, Acc., FMR, F1), Memory Updating (C, H, O), and Memory QA (C, H, O) — where C/H/O are Correct Rate, Hallucination Rate, and Omission Rate (lower better for H and O).
- Path interpretation is defined as path-importance scoring: the importance of each path to the final prediction is measured by the partial derivative of the prediction score with respect to the triples at each reasoning layer, and top-k paths are obtained by selecting the top-k longest paths with beam search.
- The HotpotQA case study ("Which man who presented the Australia 2022 FIFA World Cup bid was born on October 22 1930?" → Frank Lowy) yields two 3-step paths: one via inverse relation "was one of the representatives of"⁻¹ to Frank Lowy, then an "equivalent" link to "Sir Frank P. Lowy" whose birth date is 22 October 1930; the second runs the same chain in reverse starting from the birth date.
- The evaluation suite deliberately spans three categories (Table 13): general/multi-hop QA (NQ-Open 79,168/8,757/3,610; PopQA 14,267 pairs; HotpotQA 90,447/7,405/7,405 with 10-paragraph distractors; 2WikiMultiHopQA 167,454/12,576/12,576 with 10 passages per instance; MuSiQue 19,938/2,417/2,459, 24,814 total), e-commerce review QA (AmazonQA: 923K questions, 3.6M answers, 14M reviews, 156K products), and long-term agent memory (LongMemEval: ~115K tokens/30–40 sessions (S), ~1.5M tokens/~500 sessions (M), Oracle; HaluMem: Medium 20 users, 30,073 rounds, ~160K tokens/user, 14,948 memory points, 3,467 QA pairs; Long 53,516 rounds, ~1M tokens/user).
- Baselines are grouped into four families: Base LLM (GPT-4o-mini), Single-step RAGs (BM25, Contriever, GTR, ColBERTv2, RAPTOR, Proposition), Graph-enhanced RAGs (GraphRAG, G-Retriever, LightRAG, HippoRAG, HippoRAG 2, SubgraphRAG, PropRAG, GFM-RAG), and Multi-step RAGs (IRCoT, FLARE, Adaptive-RAG); metrics are document/entity Recall@2/5 plus EM, F1, P, R.
- The paper's declared limitations and mitigations: effectiveness depends on entity extraction, relation writing, source anchoring, and reader feedback quality, with theoretical guarantees resting on bounded graph drift, aggregate signal propagation, and local Lipschitz stability — assumptions noted as potentially not covering all large-scale, continuously evolving failure modes.

---

## P · Additional Detailed Experimental Results

The appendix reports three result tables.

### Table 9 — Retrieval performance on multi-hop QA benchmarks

Document-level Recall (%) at top-2 and top-5 across HotpotQA, MuSiQue, and 2WikiMultiHopQA; average rank is also reported. Only SAGE's row is legible in the extracted text:

| Method | HotpotQA R@2 | HotpotQA R@5 | MuSiQue R@2 | MuSiQue R@5 | 2WikiMultiHopQA R@2 | 2WikiMultiHopQA R@5 | Avg. Rank |
|---|---|---|---|---|---|---|---|
| **SAGE (ours)** | 65.1 | 77.6 | 43.2 | 53.1 | 83.6 | 88.6 | 7.0 |

### Table 10 — AmazonQA (original full-test protocol)

BLEU1/2/3/4 (B-1…B-4) and ROUGE (R). Only SAGE rows marked **[0-shot]** are zero-shot transfer results; baseline rows and trained variants are not. Visible numeric row from the excerpt:

| Method | B-1 | B-2 | B-3 | B-4 | R |
|---|---|---|---|---|---|
| R-Net (IJCAI'19) — neural baseline from original AmazonQA protocol | 47.04 | 40.32 | 31.48 | 23.92 | 40.22 |

### Table 11 — HaluMem-Medium

Three metric groups with direction: Memory Extraction (R↑, W-R↑, T-P↑, Acc.↑, FMR↑, F1↑), Memory Updating (C↑, H↓, O↓), Memory QA (C↑, H↓, O↓), where W-R = Weighted Recall, T-P = Target Memory Precision, FMR = False Memory Resistance, C = Correct Rate, H = Hallucination Rate, O = Omission Rate. SAGE rows marked **[0-shot]** are the zero-shot ones; systems reporting only a subset of metrics use "–". (Metric values for the rows were not legible in the excerpt.)

## P.1 · Path Interpretations

Path importance to the final prediction is measured by the **partial derivative of the prediction score with respect to the triples at each reasoning layer**; top-k path interpretations are then obtained by selecting the top-k longest paths with **beam search**.

Table 12 gives a HotpotQA case study (SAGE's multi-hop path interpretations, where r⁻¹ denotes the inverse of an original relation):

| Question | Answer |
|---|---|
| Which man who presented the Australia 2022 FIFA World Cup bid was born on October 22 1930? | Frank Lowy |
| **Sup. Doc.** | ["Frank Lowy", "Australia 2022 FIFA World Cup bid"] |
| **Path 1** | (the bid for the 2022 ffa world cup, was one of the representatives of⁻¹, frank lowy) → (frank lowy, equivalent, sir frank p lowy) → (sir frank p lowy, was born on, 22 october 1930) |
| **Path 2** | (22 october 1930, was born on⁻¹, sir frank p lowy) → (sir frank p lowy, equivalent, frank lowy) → (frank lowy, was one of the representatives of, the bid for the 2022 ffa world cup) |

SAGE thereby connects the two key constraints of the question — the presenter of the 2022 FIFA World Cup bid and the person born on October 22, 1930. Path 1 starts from "the bid for the 2022 FIFA World Cup", follows the inverse relation of "was one of the representatives of" to "Frank Lowy", then links via an entity-equivalence relation to "Sir Frank P. Lowy" whose birth date is 22 October 1930. Path 2 verifies the chain in reverse, starting from the birth date. The takeaway: SAGE can align different surface forms of the same entity (Frank Lowy = Sir Frank P. Lowy) and integrate multiple question constraints within a single-step retrieval process, i.e. interpretable multi-hop reasoning.

## Q · Dataset Details

Table 13 summarizes the datasets across three complementary categories. The paper's rationale for each:

**General and Multi-hop QA.** `NQ-Open` (Natural Questions-derived) tests whether a system can retrieve and ground factual short answers in a Wikipedia-scale corpus. `PopQA` focuses on entity-centric factual questions spanning popularity levels, stress-testing recovery of **long-tail** factual knowledge vs. parametric memorization. `HotpotQA` provides Wikipedia multi-hop questions with sentence-level supporting facts, so evaluation covers answer correctness plus recovery of bridge evidence and interpretable reasoning chains. `2WikiMultiHopQA` combines Wikipedia text with Wikidata-derived relations and evidence paths for 2–4 hop questions. `MuSiQue` composes connected single-hop questions into 2–4 hop questions to reduce shortcut reasoning, testing genuinely compositional evidence integration.

**E-commerce Review-based QA.** `AmazonQA` is a practical, noisy, user-generated setting: real product questions, community answers, product reviews, and product metadata, with **answerability annotations** marking whether a question is answerable from available reviews. For a self-evolving memory system it is valuable because the system must decide *which* review facts, product attributes, and user opinions are worth indexing for future retrieval — rather than matching a question to a clean encyclopedic passage.

**Long-term Agent Memory.** `LongMemEval` assesses long-term chat-assistant memory over extended multi-session histories, covering five core abilities: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. `HaluMem` is complementary: it decomposes memory evaluation into **memory extraction, memory updating, and memory QA**, revealing at which operational stage hallucinations, omissions, or conflicts arise — important because errors introduced during graph construction or memory updating propagate to graph-guided retrieval and final answer generation.

**Evaluation Rationale.** Together the datasets form a progressively broader suite: NQ/PopQA test factual open-domain retrieval; HotpotQA/2WikiMultiHopQA/MuSiQue test multi-hop evidence composition; AmazonQA tests noisy real-world review memory; LongMemEval tests long-horizon interactive memory; HaluMem diagnoses operation-level hallucinations. This frames SAGE not merely as a RAG QA pipeline but as a self-evolving memory system that decides what to store, how to organize it, how to retrieve under different query conditions, and how to update or suppress unreliable memories over time.

Table 13 details:

| Category | Dataset | Scale / Split | Evidence source | Task type | Main metrics |
|---|---|---|---|---|---|
| General / Multi-hop QA | NQ-Open | 79,168 / 8,757 / 3,610 | English Wikipedia | Open-domain short-answer | EM / F1 / Acc.; Recall@k |
| General / Multi-hop QA | PopQA | 14,267 QA pairs | Wikidata triples + Wikipedia page-view popularity | Entity-centric open-domain QA | Acc. / EM; long-tail breakdown |
| General / Multi-hop QA | HotpotQA | 90,447 / 7,405 / 7,405 | Wikipedia paragraphs; 10-paragraph distractor setting | Explainable 2-hop QA | Answer EM/F1; Support EM/F1; Joint EM/F1 |
| General / Multi-hop QA | 2WikiMultiHopQA | 167,454 / 12,576 / 12,576 | Wikipedia + Wikidata; 2–4 hop; 10 passages per instance | Multi-hop QA (comparison, bridge, bridge-comparison) | Answer EM/F1; Evidence / path recall |
| General / Multi-hop QA | MuSiQue | 19,938 / 2,417 / 2,459 (24,814 total) | Composed single-hop QA over textual passages | 2–4 hop connected multi-hop QA (shortcut-resistant) | Answer EM/F1; Support / evidence recall |
| E-commerce Review QA | AmazonQA | 923K questions; 3.6M answers; 14M reviews; 156K products | Amazon reviews, Q&A, product metadata | Review-based QA with answerability annotation | BLEU / ROUGE; answerability Acc./F1; groundedness |
| Long-term Agent Memory | LongMemEval | 500 eval. instances per file; S: ~115K tokens / 30–40 sessions; M: ~1.5M tokens / ~500 sessions; Oracle: evidence sessions only | Long multi-session human–AI chat histories | Long-term interactive memory QA | Overall Acc.; category-wise Acc.; context tokens; latency |
| Long-term Agent Memory | HaluMem | Medium: 20 users, 30,073 dialogue rounds, ~160K tokens/user, 14,948 memory points, 3,467 QA pairs; Long: 53,516 rounds, ~1M tokens/user | Synthetic long-term human–AI interaction with memory points and multi-type questions | Operation-level memory / hallucination benchmark | Extraction R/P/F1; Updating C/H/O; QA C/H/O |

## R · Baselines and Metrics

**Baselines** — four categories:

- **Base LLM:** GPT-4o-mini.
- **Single-step RAGs:** BM25, Contriever, GTR, ColBERTv2, RAPTOR, Proposition.
- **Graph-enhanced RAGs:** GraphRAG, G-Retriever, LightRAG, HippoRAG, HippoRAG 2, SubgraphRAG, PropRAG, and the closely related GFM-RAG.
- **Multi-step RAGs:** IRCoT, FLARE, Adaptive-RAG.

`IRCoT` is highlighted as a general multi-step reasoning framework that integrates with non-iterative retrievers, letting both single-step RAG and graph-based methods do multi-hop reasoning through interleaved retrieval and generation.

**Metrics** — retrieval quality: Recall@2 and Recall@5 for both retrieved **entities** and **documents**, denoted R@2/5_E and R@2/5_D. End-to-end QA: Exact Match (EM), F1, Precision (P), Recall (R).

## Limitations

SAGE treats graph memory as a dynamic substrate for writing, reading, and self-evolution, but its effectiveness still depends on the quality of entity extraction, relation writing, source anchoring, and reader feedback. Errors introduced during graph construction may propagate to retrieval and final answer generation, especially in long-term memory settings involving temporal updates, conflicting user preferences, or sparse evidence. Promising results across multi-hop QA, open-domain retrieval, review-based QA, and long-term agent-memory benchmarks coexist with acknowledged room for improvement on memory updating, high-coverage extraction, and hallucination control. The theoretical analysis relies on assumptions such as **bounded graph drift, aggregate signal propagation, and local Lipschitz stability** — useful intuition, but may not capture all failure modes of large-scale, noisy, continuously evolving memory graphs.

## Broader Impact

Positive: structure-aware self-evolving memory can help long-horizon agents recover evidence chains from fragmented cues, keep long-term interactions more consistent, and reduce unsupported answers (knowledge/research/customer support, review-based QA). Risks: on personal or sensitive histories such systems may store private information, infer preferences, retain outdated or incorrect memories, or enable profiling/surveillance; wrong graph writes or retrieval failures can produce confidently grounded but wrong answers. Recommended practices: consent-based data collection, data minimization, access control, deletion/forgetting, provenance tracking, auditing, and human oversight for high-stakes use cases.

## Compute Resources

All experiments ran on a server with **8 NVIDIA A100 GPUs**. Main cost: graph-memory construction, GFM-based graph propagation, selector regularization, and entity-to-document projection; training/inference complexity in terms of nodes *n*, edges *m*, hidden dim *d*, propagation layers *L*, batch size *B*, pseudo-queries *M*, and entity–document links is analyzed in Appendix J. Structural features and entity–document indices are precomputed/cached; edge-level gates are computed in chunks, reducing peak GPU memory from O(|E|d) to O(C_e·d) for chunk size C_e. Dominant inference cost is one (or a small number of) query-conditioned graph propagations plus sparse document projection — making the reader suitable for repeated evaluation inside the self-evolving writer–reader loop.

## Licenses and Existing Assets

The paper uses existing public benchmarks and baselines (NQ-Open, PopQA, HotpotQA, 2WikiMultiHopQA, MuSiQue, AmazonQA, LongMemEval, HaluMem, and the RAG baselines above), cites their original papers/repos, uses them only for research evaluation under their stated licenses, and does not redistribute modified datasets beyond preprocessing scripts. Released code is research-only and includes setup, data-preparation, training, and evaluation documentation.

## NeurIPS Paper Checklist (back matter)

All 16 checklist questions except Safeguards (Q11: N/A — no high-risk assets released), New assets (Q13: N/A — no new dataset/benchmark/model released), Crowdsourcing (Q14: N/A), and IRB (Q15: N/A — no human subjects) are answered **Yes**. Notable justifications: theoretical results include complete assumptions, theorem statements, lemmas, and proofs in the appendix (SNR, retrieval budget, target-graph calibration, stability, self-evolution); Q8 confirms 8× A100 compute; Q16 (LLM usage declaration) is **Yes** — LLMs are used in the memory writer, structured query-planning prompts, and answer generation, i.e. part of the proposed method, not just writing assistance.

**Covers:** source lines 5067–6108 (Appendix P "Additional Detailed Experimental Results" incl. Tables 9–11, P.1 Path Interpretations with Table 12 case study, Q Dataset Details with Table 13, R Baselines and Metrics, Limitations, Broader Impact, Compute Resources, Licenses, NeurIPS Paper Checklist)
