> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments (Sec 5) and Conclusion

**In one sentence:** SAGE is evaluated across four research questions — open-domain/multi-hop QA, long-term agent memory, writer–reader self-evolution, and design ablations — and wins big in open-domain retrieval (82.5% R@2D on NQ zero-shot) and retrieval speed, while remaining competitive-but-not-leading on specialized long-term-memory benchmarks.

## Key points

- Evaluation is organized around four research questions: RQ1 (consistent gains on multi-hop QA and open-domain transfer), RQ2 (long-term conversation history, knowledge updates, memory hallucination), RQ3 (whether the writer–reader closed loop truly yields self-evolution), RQ4 (where and how the gains come from specific designs).
- Open-domain zero-shot transfer is the headline result: trained only on multi-hop data (MuSiQue, HotpotQA, 2WikiMultiHopQA), SAGE reaches **82.5% R@2D / 91.6% R@5D on NQ** — far above the next-best reported baselines (HippoRAG 2: 45.6/78.0; RAPTOR: 40.3/68.3) — and 41.5/52.3 on PopQA, where it is roughly on par with the strongest baselines (GTR 40.1/49.4, HippoRAG 2 43.9/51.7).
- On multi-hop QA (Table 3) the paper reports Exact Match and F1 on HotpotQA, MuSiQue, and 2WikiMultiHopQA; the only full baseline row printed in this chunk is BM25 (arXiv'24): 40.0/53.2 (HotpotQA), 19.5/23.6 (MuSiQue), 46.9/57.9 (2Wiki), avg. rank 15.5.
- On the e-commerce Review-Based QA task (AmazonQA, Table 10), SAGE outperforms the neural baseline R-Net across all metrics; training on AmazonQA yields substantial further gains, with interaction rounds steadily improving performance, while zero-shot results demonstrate transfer.
- On LongMemEval (Table 2, six categories: SS-U, SS-A, SSR, SS-P, KU, TR, MS) and HaluMem (Table 11), SAGE does not yet surpass the strongest system-level memory baselines — a hard setting, since competitors like Memobase, Supermemory, MemU are highly specialized — but SAGE +1 training round already outperforms Memobase on several metrics; the remaining gap is attributed to memory updating and high-coverage extraction.
- Retrieval efficiency (Table 4, seconds on HotpotQA/MuSiQue/2Wiki): SAGE achieves the fastest retrieval time among the compared single-step and iterative methods, which the authors read as strong potential for practical, large-scale deployment.
- Interpretability evidence: a visualized retrieved subgraph (Figure 3) shows the graph traversal resolving an entity disambiguation between two similar sci-fi authors (a near-miss author hub vs. the correctly resolved target), with a detailed case study in P.1.
- Full ablations of the Memory Writer and Memory Reader are deferred to Appendices H and G respectively; the writer–reader training loop itself is Algorithm 1 (writer RL update with the fixed GFM reader as reward environment, then reader update on improved graphs).
- The conclusion frames memory as a "dynamic substrate for writing, reading, and continual improvement," and claims that SAGE improves evidence recovery, grounding, and retrieval efficiency, making self-evolving graph memory a promising foundation for long-horizon language agents.

---

**Covers:** Section 5 (Experiments: dataset and RQ setup, 5.1 End-to-End Effectiveness, 5.2 Long-term Agent Memory Evaluation, 5.3 Further Analysis), Section 6 (Conclusion), the reference list, and Algorithm 1 (Writer–Reader Self-Evolution Training) — source lines 443–936 of the paper.

## Research questions and datasets

The experimental section is driven by four RQs:

- **RQ1:** whether SAGE brings consistent benefits in tasks such as multi-hop QA and open-domain transfer;
- **RQ2:** whether SAGE is an agent memory system capable of handling long-term conversation history, knowledge updates, and memory hallucination;
- **RQ3:** whether the writer–reader closed loop truly yields self-evolution benefits;
- **RQ4:** further analysis of where and how the performance gains come from specific designs.

Evaluation runs on five complementary scenarios:

| Category | Datasets | What they test |
| --- | --- | --- |
| General + multi-hop QA | NQ, PopQA, HotpotQA, 2WikiMultiHopQA, MuSiQue | recovering bridge entities across documents; combining evidence and reasoning paths |
| E-commerce (practical) | AmazonQA (Review-Based QA) | value in real e-commerce with real noisy reviews |
| Long-term agent memory | LongMemEval, HaluMem | extraction from long interaction histories, multi-session reasoning, temporal reasoning, knowledge updating, abstention, operation-level hallucination |

Table 13 (Appendix) summarizes dataset details; baseline and metric details are in Appendix R.

## 5.1 End-to-End Effectiveness

### Open-domain retrieval (NQ, PopQA) — Table 1

Passage-/document-level Recall (%) at top-2/top-5 (R@2D / R@5D). Baseline numbers are taken from the original papers or later reproductions that cite them; **only the SAGE row is a zero-shot transfer result** — SAGE was *not* trained on NQ or PopQA — while baseline rows used their own training setups.

| Method | NQ R@2D | NQ R@5D | PopQA R@2D | PopQA R@5D |
| --- | --- | --- | --- | --- |
| BM25 (SIGIR'94) | 28.2 | 56.1 | 24.0 | 35.7 |
| Contriever (TMLR'22) | 29.1 | 54.6 | 27.0 | 43.2 |
| GTR (EMNLP'22) | 35.0 | 63.4 | 40.1 | 49.4 |
| ColBERTv2 (NAACL'22) | 36.8 | 64.3 | – | – |
| RAPTOR (ICLR'24) | 40.3 | 68.3 | 40.2 | 48.7 |
| Proposition (EMNLP'24) | 33.1 | 62.2 | – | – |
| HippoRAG (NeurIPS'24) | 21.3 | 44.4 | 40.0 | 53.8 |
| HippoRAG 2 (ICML'25) | 45.6 | 78.0 | 43.9 | 51.7 |
| PropRAG (EMNLP'25) | – | 77.9 | – | 56.2 |
| **SAGE (ours) [0-shot]** | **82.5** | **91.6** | 41.5 | 52.3 |

Footnotes in the source: some baseline values come from reproduced passage-level Recall@2/5 evaluations; PropRAG's numbers come from a Recall@5 table (no Recall@2 reported); ColBERTv2's come from a reproduced single-step retrieval table (no PopQA).

The authors emphasize the transfer result: even when directly tested on NQ and PopQA, with a model trained **only on MuSiQue, HotpotQA, and 2WikiMultiHopQA**, SAGE still achieves very strong performance, especially on NQ — an 82.5% R@2D that beats the closest reported baseline (HippoRAG 2, 45.6%) by over 37 points in top-2 document recall.

### Multi-hop QA — Table 3

Main multi-hop results report Exact Match (EM) and F1 (%) on HotpotQA, MuSiQue, and 2WikiMultiHopQA, plus an average rank; Table 9 reports the corresponding retrieval performance on these benchmarks. The baseline row reproduced in this chunk:

| Method | HotpotQA EM / F1 | MuSiQue EM / F1 | 2Wiki EM / F1 | Avg. rank |
| --- | --- | --- | --- | --- |
| BM25 (arXiv'24) | 40.0 / 53.2 | 19.5 / 23.6 | 46.9 / 57.9 | 15.5 |

### Domain-specific memory — AmazonQA (Table 10)

On the review-based QA task, SAGE consistently outperforms the neural baseline R-Net across all metrics, indicating strong cross-task generalization. After training on AmazonQA, "Ours" achieves substantial gains; interaction rounds steadily enhance performance, while the zero-shot results demonstrate promising transfer ability.

## 5.2 Long-term Agent Memory Evaluation

| Benchmark | Results table | Outcome |
| --- | --- | --- |
| LongMemEval | Table 2 | Competitive but not leading vs. specialized systems |
| HaluMem | Table 11 | Same setting |

LongMemEval accuracy is reported over six task categories: single-session user (SS-U), single-session assistant (SS-A), merged single-session recall (SSR, the weighted average of SS-U/SS-A when both are available), single-session preference (SS-P), knowledge update (KU), temporal reasoning (TR), and multi-session reasoning (MS). Results are grouped by reporting protocol (Unified protocol in TiMem with GPT-4o-mini LLJ accuracy; MemOS evaluation suite with short-answer prompt; and the authors' own method) and explicitly "should not be treated as a single strict leaderboard." Again, only the "Ours" rows marked **[0-shot]** are zero-shot transfer results; baseline rows and trained variants are not.

The comparison is against highly specialized long-term memory systems — Memobase, Supermemory, MemU, and similar — making this a challenging setting. SAGE does not yet surpass the strongest system-level baselines, but **SAGE + 1 training round already outperforms Memobase on several metrics**, suggesting it is competitive despite being less system-engineered. The authors attribute the remaining gap mainly to memory updating and high-coverage extraction, indicating clear potential for further gains with stronger memory-management and update mechanisms.

## 5.3 Further Analysis

**Retrieval efficiency — Table 4.** Retrieval time (seconds, lower is better) on HotpotQA, MuSiQue, and 2Wiki, comparing single-step and iterative retrieval methods. SAGE demonstrates a strong speed advantage and achieves the fastest retrieval time, indicating strong potential for practical and large-scale deployment.

**Interpretability.** To analyze interpretability, the authors visualize the retrieved subgraph for a representative case (Figure 3); a detailed case study is in Appendix P.1, and ablation study design, analysis, and results for the Memory Writer and Reader are in Appendices H and G respectively.

![Figure 3 — Visualization of the retrieved results: the left (red ✗) panel shows a near-miss author hub (Alan Dean Foster) connected via typed edges to overlapping sci-fi works, series, and era dates; the right (green ✓) panel is the tightly resolved correct target (Samuel R. Delany, with alias "Samuel Ray Delany Jr."), with a dashed edge bridging the two — i.e., graph traversal over typed relationships and alias/identity cues disambiguates candidate entities that flat surface-attribute matching would confuse.](images/03-fig3-retrieval.png)

The figure illustrates the disambiguation mechanism: when candidate entities are highly similar (two sci-fi authors sharing themes and era dates), a flat retrieval would land on the wrong, densely connected author hub (left, ✗); the graph representation lets SAGE follow typed edges (wrote / written by / contains / topic) and alias/identity cues (e.g., "Samuel Ray Delany Jr.", "Gay African American") to reach the correct node (right, ✓).

## 6 Conclusion

"We presented SAGE, a self-evolving agentic graph-memory engine that treats memory as a dynamic substrate for writing, reading, and continual improvement. Experiments show that SAGE improves evidence recovery, grounding, and retrieval efficiency, suggesting that self-evolving graph memory is a promising foundation for long-horizon language agents."

## Reference list (scope)

The chunk's reference section spans the paper's full bibliography (~40 entries), including the datasets and baselines used in Sec 5 (HotpotQA, MuSiQue, NQ-style DART/RAG line via Lewis et al., AmazonQA, LongMemEval, HaluMem), prior memory systems (MemGPT, Mem0, MemOS, Zep, SGMEM, HyperMem, AssoMem, G-Memory, SgMem, LightRAG, HippoRAG 1/2, PropRAG, NodeRAG, E²GraphRAG, GFM-RAG), and the retrieval/QA infrastructure (BM25, Contriever, GTR, ColBERTv2, RAPTOR, FLARE, Self-RAG, Adaptive-RAG, GraphRAG).

## Algorithm 1: Writer–Reader Self-Evolution Training for SAGE

Inputs: training set `D_train`, writer `π_θ0`, GFM reader `f_φ0`, self-evolution iterations `T`; outputs: trained writer `π_θT` and reader `f_φT`.

For `t = 0 … T−1`:

1. **Writer update** (fixed GFM reader as reward environment): for each sample `x = (q, D, D⁺, y) ∈ D_train`, sample `G` graph-construction trajectories `{τ_i}` from `π_θt`; for each `i`, obtain graph `G_i` and retrieve `P_k(q, G_i)` using `f_φt`; calculate return `R_i`; update writer `π_θt`.
2. **Reader update** (improved graphs as memory substrate): construct the set of graph memories `{G_x}` for the training corpus using the updated writer `π_θt+1`; update the GFM reader `f_φt` on `{G_x}`.

Informal implication: each round the writer is RL-trained against a frozen reader (the reader's retrieval quality is the reward signal for what kind of graph to write), then the reader is retrained on the improved graphs the new writer produces — a co-evolution loop rather than a one-shot distillation, which is the concrete mechanism behind RQ3.
