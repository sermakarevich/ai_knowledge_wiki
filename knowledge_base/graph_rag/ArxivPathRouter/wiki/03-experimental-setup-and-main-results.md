> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup and Main Results

**In one sentence:** PathRouter is evaluated on six QA benchmarks against GraphRAG, non-retrieval, chunk-based, and graph-based agentic baselines, and it delivers consistent gains over Graph-R1 at every model scale — largest on the multi-hop benchmarks where evidence-path faithfulness matters most.

## Key points

- **Research questions (§4):** RQ1 — does PATHROUTER improve answer accuracy and evidence quality over existing baselines (§4.2)? RQ2 — which components drive path faithfulness, and how does routing change trajectory-level behavior (§4.3, §4.4)? RQ3 — how does teacher KL interact with model capacity, and do the learned retrieval strategies transfer across datasets (§4.5, §4.6)?
- **Datasets (§4.1):** evaluation follows the protocol of Graph-R1 (Luo et al., 2025a) on six QA benchmarks: three multi-hop datasets with gold supporting facts enabling path-faithfulness evaluation — HotpotQA (Yang et al., 2018), 2WikiMultiHopQA (Ho et al., 2020), MuSiQue (Trivedi et al., 2022) — and three single-hop datasets for broader coverage — NQ (Kwiatkowski et al., 2019), PopQA (Mallen et al., 2023), TriviaQA (Joshi et al., 2017).
- **Baselines (§4.1), following Graph-R1:** GPT-4o-mini-based references (GraphRAG, LightRAG, PathRAG, HippoRAG2, HyperGraphRAG), non-retrieval approaches (NaiveGeneration, SFT, R1 = GRPO without retrieval), chunk-based retrieval (StandardRAG, Search-R1, R1-Searcher), and graph-based agentic retrieval (Graph-R1, the primary baseline).
- **Metrics (§4.1):** token-level F1, Exact Match (EM), and GPT-4o-mini evaluation (G-E) for answer quality; Supporting Fact F1 (SF-F1) and Unsupported Answer Rate (UAR, ↓) for path faithfulness; formal definitions are in Appendix A.
- **Main results (§4.2):** PATHROUTER consistently outperforms Graph-R1 across all model scales — 7B average F1 improves from 57.82 to 62.74, EM from 48.57 to 53.26, G-E from 76.23 to 78.72 — and also outperforms the `w/o TKL` ablation at every scale.
- **Gains are most pronounced on multi-hop benchmarks (§4.2):** at 7B, F1 rises by 7.4 points on HotpotQA and 8.2 on MuSiQue, where faithful evidence composition is essential; the pattern holds at smaller scales (average F1 +3.1 at 3B, +3.2 at 1.5B), confirming route-conditioned training mitigates answer-path reward aliasing regardless of model capacity.
- **Scaling behavior (§4.2):** route conditioning is scale-robust, while TKL is more capacity-sensitive — whether this reflects teacher mismatch or limited student capacity is discussed in Section 4.5.

---

## Experimental setup (§4.1)

**Datasets.** Following the evaluation protocol of Graph-R1 (Luo et al., 2025a), the paper uses six QA benchmarks: three multi-hop datasets — HotpotQA (Yang et al., 2018), 2WikiMultiHopQA (Ho et al., 2020), and MuSiQue (Trivedi et al., 2022) — that provide gold supporting facts enabling path-faithfulness evaluation, and three single-hop datasets — NQ (Kwiatkowski et al., 2019), PopQA (Mallen et al., 2023), and TriviaQA (Joshi et al., 2017) — for broader coverage.

**Baselines.** Following Graph-R1 (Luo et al., 2025a), the compared methods are:

- **GPT-4o-mini-based methods as references:** GraphRAG (Edge et al., 2025), LightRAG (Guo et al., 2025), PathRAG (Chen et al., 2025), HippoRAG2 (Gutiérrez et al., 2025), HyperGraphRAG (Luo et al., 2025b).
- **Non-retrieval approaches:** NaiveGeneration (direct LLM), SFT (Zheng et al., 2024, supervised fine-tuning), R1 (Shao et al., 2024, GRPO without retrieval).
- **Chunk-based retrieval:** StandardRAG (Lewis et al., 2020), Search-R1 (Jin et al., 2025), R1-Searcher (Song et al., 2025).
- **Graph-based agentic retrieval:** Graph-R1 (Luo et al., 2025a) — the primary baseline.

**Evaluation metrics.** Token-level F1, Exact Match (EM), and GPT-4o-mini evaluation (G-E) for answer quality, along with Supporting Fact F1 (SF-F1) and Unsupported Answer Rate (UAR, ↓) for path faithfulness. Formal definitions are in Appendix A.

## Main results (§4.2)

Table 1 reports results across six datasets and three model sizes (Qwen2.5 at 1.5B, 3B, 7B), revealing two consistent patterns (per the source text in this chunk):

**Consistent gains over Graph-R1.** PATHROUTER outperforms Graph-R1 across all model scales, improving the 7B average F1 from 57.82 to 62.74, EM from 48.57 to 53.26, and G-E from 76.23 to 78.72. The agreement across lexical, exact-match, and LLM-based metrics suggests the gains reflect more reliable answer production rather than surface-form effects. The `PATHROUTER w/o TKL` ablation (token-level KL removed) trails the full model at every scale (e.g., 7B: average F1 60.36 vs. 62.74).

| Method | HotpotQA F1 / G-E | 2Wiki F1 / G-E | MuSiQue F1 / G-E | NQ F1 / G-E | Avg. EM / F1 / G-E |
|---|---|---|---|---|---|
| **Qwen2.5-7B-Instruct** | | | | | |
| NaiveGeneration | 16.58 / 65.31 | 12.25 / 66.75 | 4.06 / 65.47 | 13.00 / 69.56 | 3.12 / 13.87 / 66.71 |
| StandardRAG | 21.00 / 66.13 | 12.75 / 60.06 | 4.53 / 59.84 | 15.97 / 70.49 | 5.34 / 15.89 / 65.18 |
| SFT | 27.59 / 65.65 | 20.28 / 63.85 | 10.02 / 63.50 | 19.93 / 68.19 | 15.57 / 24.01 / 64.63 |
| R1 | 37.06 / 60.12 | 30.99 / 59.19 | 14.53 / 49.39 | 28.45 / 57.11 | 25.91 / 33.12 / 57.74 |
| Search-R1 | 50.85 / 73.85 | 41.29 / 70.26 | 22.35 / 57.68 | 45.88 / 67.58 | 38.54 / 46.19 / 68.60 |
| R1-Searcher | 46.36 / 74.56 | 33.96 / 69.61 | 16.63 / 59.05 | 44.93 / 68.34 | 34.51 / 42.29 / 69.08 |
| Graph-R1 | 62.69 / 80.03 | 65.04 / 82.42 | 46.17 / 71.42 | 49.87 / 70.97 | 48.57 / 57.82 / 76.23 |
| **PATHROUTER** | **70.13 / 82.56** | **71.04 / 84.20** | **54.34 / 74.18** | **53.84 / 74.62** | **53.26 / 62.74 / 78.72** |
| PATHROUTER w/o TKL | 65.93 / 81.40 | 67.49 / 83.54 | 51.61 / 73.26 | 51.52 / 73.84 | 49.74 / 60.36 / 78.47 |

*(The full table in the source also includes PopQA and TriviaQA columns and the GPT-4o-mini† and Qwen2.5-1.5B/3B-Instruct rows; e.g., at 3B PATHROUTER reaches 62.20/79.58 F1/G-E on HotpotQA and average EM 54.32 vs. Graph-R1's 51.26, and at 1.5B average F1 43.31 vs. Graph-R1's 40.09.)*

**Multi-hop gains where evidence composition matters.** Improvements are most pronounced on multi-hop benchmarks where faithful evidence composition is essential, with 7B F1 rising by 7.4 points on HotpotQA and 8.2 on MuSiQue. The same pattern holds at smaller scales, with average F1 improving by 3.1 points at 3B and 3.2 at 1.5B, confirming that route-conditioned training mitigates answer-path reward aliasing regardless of model capacity. Route conditioning remains scale-robust, while TKL is more capacity-sensitive; Section 4.5 discusses whether this reflects teacher mismatch or limited student capacity.

**Covers:** Section 4.1 (Experimental Setup), Section 4.2 (Main Results)
