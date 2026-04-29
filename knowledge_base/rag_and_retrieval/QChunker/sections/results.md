> **Paper:** [[summary]] | **Deep dive:** [[details]]

## Results

### 1. Main Results (Table 1)

QChunker is evaluated on four domain QA datasets: CRUD (news), OmniEval (finance), MultiFieldQA (multi-domain), and HChemSafety (hazardous chemical safety). The first two are in-domain (used for training QChunker-3B); MultiFieldQA and HChemSafety are out-of-domain benchmarks. All methods use standardized chunk length (avg 178 tokens) and identical RAG pipeline components (Milvus vector DB, bge-base-zh-v1.5 embeddings, top_k=8, Qwen2.5-7B generator).

| Chunking Method | CRUD BLEU | CRUD ROU. | CRUD MET. | OmniEval BLEU | OmniEval ROU. | OmniEval MET. | MultiFieldQA BLEU | MultiFieldQA ROU. | MultiFieldQA MET. | HChemSafety BLEU | HChemSafety ROU. | HChemSafety MET. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Original | 0.5022 | 0.5654 | 0.7324 | 0.1906 | 0.2254 | 0.3904 | 0.1707 | 0.2315 | 0.3650 | 0.2282 | 0.2054 | 0.3152 |
| Llama_index | 0.5312 | 0.5896 | 0.7449 | 0.1969 | 0.2350 | 0.4040 | 0.1732 | 0.2363 | 0.3726 | 0.2477 | 0.2234 | 0.3213 |
| Semantic Chunking | 0.5188 | 0.5823 | 0.7434 | 0.1913 | 0.2240 | 0.3821 | 0.1609 | 0.2191 | 0.3468 | 0.2037 | 0.1891 | 0.2964 |
| LumberChunker | 0.5061 | 0.5701 | 0.7399 | 0.1997 | 0.2375 | 0.4085 | 0.1841 | 0.2426 | 0.3809 | 0.2298 | 0.2124 | 0.3402 |
| MoC MetaChunker | 0.5456 | 0.6031 | 0.7546 | 0.2042 | 0.2457 | 0.4141 | 0.1707 | 0.2255 | 0.3512 | 0.2525 | 0.2307 | 0.3449 |
| Qwen2.5-14B | 0.5329 | 0.5920 | 0.7502 | 0.2048 | 0.2473 | 0.4160 | 0.1883 | 0.2497 | 0.3827 | 0.2550 | 0.2250 | 0.3237 |
| Qwen3-14B | 0.5382 | 0.5953 | 0.7531 | 0.1907 | 0.2329 | 0.4080 | 0.1800 | 0.2412 | 0.3759 | 0.2419 | 0.2195 | 0.3311 |
| **QChunker-3B** | **0.5552** | **0.6114** | **0.7640** | **0.2193** | **0.2673** | **0.4348** | **0.1970** | **0.2613** | **0.4010** | **0.2792** | **0.2457** | **0.3654** |
| QChunker w/o M_Ref | 0.5433 | 0.6014 | 0.7601 | 0.2139 | 0.2555 | 0.4198 | 0.1935 | 0.2549 | 0.3889 | 0.2719 | 0.2427 | 0.3607 |

QChunker-3B achieves the best result on all 12 metrics (bold). The second-best result is obtained by the ablation variant w/o M_Ref on 11 out of 12 metrics and by MoC MetaChunker on 1 out of 12 metrics.

---

### 2. Statistical Significance

Three independent repeated experiments were conducted. QChunker outperforms all baseline methods under a **t-test with p < 0.05** across all comparisons. This confirms that the improvements are statistically significant and not artifacts of random variation.

---

### 3. Ablation Study: Effect of Removing M_Ref (Knowledge Completion)

The ablation variant "QChunker w/o M_Ref" removes the knowledge completion module while retaining the question-aware segmentation. Comparison of the last two rows of Table 1:

| Dataset | Metric | QChunker-3B | w/o M_Ref | Degradation |
|---|---|---|---|---|
| CRUD | BLEU | 0.5552 | 0.5433 | -0.0119 |
| CRUD | ROUGE-L | 0.6114 | 0.6014 | -0.0100 |
| CRUD | METEOR | 0.7640 | 0.7601 | -0.0039 |
| OmniEval | BLEU | 0.2193 | 0.2139 | -0.0054 |
| OmniEval | ROUGE-L | 0.2673 | 0.2555 | -0.0118 |
| OmniEval | METEOR | 0.4348 | 0.4198 | -0.0150 |
| MultiFieldQA | BLEU | 0.1970 | 0.1935 | -0.0035 |
| MultiFieldQA | ROUGE-L | 0.2613 | 0.2549 | -0.0064 |
| MultiFieldQA | METEOR | 0.4010 | 0.3889 | -0.0121 |
| HChemSafety | BLEU | 0.2792 | 0.2719 | -0.0073 |
| HChemSafety | ROUGE-L | 0.2457 | 0.2427 | -0.0030 |
| HChemSafety | METEOR | 0.3654 | 0.3607 | -0.0047 |

Performance degrades on **all 12 metrics across all 4 datasets** when M_Ref is removed. The largest single drop is on OmniEval METEOR (-0.0150, from 0.4348 to 0.4198). Even without knowledge completion, w/o M_Ref still surpasses most baselines (second-best on 11/12 metrics), confirming that the question-aware segmentation itself is valuable -- but knowledge completion provides a consistent additional boost.

---

### 4. ChunkScore Validation

#### 4.1 Lambda Sweep (Hyperparameter Tuning)

The ChunkScore is defined as:

$$\Phi_{CS}(C) = \lambda \cdot \Phi_{LI}(C) + (1 - \lambda) \cdot \Phi_{SD}(C)$$

where LI = Logical Independence (micro-level boundary clarity) and SD = Semantic Dispersion (macro-level diversity).

A lambda sweep was conducted on the CRUD benchmark from **0.0 to 1.0 with step size 0.01**. For each lambda value, the Pearson correlation coefficient was calculated between ChunkScores (across multiple chunking strategies) and ROUGE-L performance on the downstream QA task.

The resulting correlation curve (Figure 2) shows:
- At **lambda = 0.3**, the Pearson correlation coefficient **approaches 1.0** -- the maximum observed.
- This optimal weighting assigns **30% weight to Logical Independence** and **70% weight to Semantic Dispersion**.

#### 4.2 Interpretation: Relative Importance of LI vs SD

The optimal lambda = 0.3 reveals that **semantic dispersion (SD) is more important than logical independence (LI)** for predicting downstream QA quality. Ensuring that text chunks cover diverse, non-redundant information (SD) matters more than merely guaranteeing clean boundaries (LI), provided that basic boundary clarity is maintained.

#### 4.3 Cross-Dataset Pearson Correlations

The lambda = 0.3 setting was further validated on three additional datasets (OmniEval, MultiFieldQA, HChemSafety) with analogous correlation analyses. The results show that **all Pearson correlation coefficients exceed 0.85** across all four datasets. This confirms that ChunkScore generalizes as a reliable proxy metric -- it is not overfit to a single domain or dataset.

---

### 5. Perplexity Analysis (Effectiveness of Knowledge Completion)

#### 5.1 Experimental Setup

On the CRUD benchmark, perplexity is used to directly measure the intrinsic coherence and comprehensibility of text chunks before and after knowledge completion. Lower perplexity indicates clearer logical structure and better comprehensibility for a language model.

#### 5.2 Results on 1.5B and 7B Models

The analysis (Figure 3) was conducted on models at **two parameter scales: 1.5B and 7B**. The key findings:

| Aspect | Original Chunks | Knowledge-Completed Chunks |
|---|---|---|
| Mean perplexity | Higher | **Lower** (consistently across both 1.5B and 7B) |
| Volatility | Higher (many spikes) | **Lower** (smoother distribution) |
| Perplexity peaks | Frequent (caused by context breaks) | **Reduced** (ambiguity points pre-eliminated) |

Regardless of model scale (1.5B or 7B):
- Text chunks that underwent knowledge completion have **consistently lower perplexity** than original chunks.
- Knowledge-completed chunks have a **lower overall mean value** of perplexity.
- Knowledge-completed chunks exhibit **less volatility** -- they avoid the perplexity spikes that appear in original chunks due to context breaks at chunk boundaries.

This demonstrates that the knowledge completion mechanism optimizes internal context consistency of text chunks, pre-eliminating ambiguity points and information gaps that would otherwise cause model comprehension obstacles.

---

### 6. Key Takeaways

#### Why knowledge completion matters (not just segmentation)

The ablation study definitively shows that text chunking is a **composite task of segmentation and knowledge completion** -- the paper's central thesis. Even with high-quality question-aware segmentation (w/o M_Ref still beats most baselines), removing knowledge completion causes degradation on all 12 metrics. The perplexity analysis provides mechanistic evidence: knowledge completion smooths out information gaps at chunk boundaries, reducing comprehension difficulty for downstream models. Segmentation alone leaves semantic fragments; knowledge completion reconstructs self-contained, information-rich units.

#### Why 3B outperforms 14B (specialized training vs general prompting)

QChunker-3B (a fine-tuned Qwen2.5-3B) outperforms both Qwen2.5-14B and Qwen3-14B on all 12 metrics, despite being nearly 5x smaller. The general-purpose 14B models are applied via prompting alone, while QChunker-3B is trained on 45K high-quality samples specifically constructed through the multi-agent debate framework. This demonstrates that **task-specific fine-tuning of a small model decisively outperforms general prompting of a much larger model** for specialized tasks like text chunking. The distillation from the multi-agent framework into the SLM preserves the advanced segmentation and completion capabilities at a fraction of the computational cost.

#### Domain-specific advantage (HChemSafety gains)

On HChemSafety -- a proprietary dataset featuring high term density and strong contextual dependencies in hazardous chemical safety -- QChunker's advantage is **particularly prominent**. QChunker-3B achieves BLEU 0.2792, ROUGE-L 0.2457, METEOR 0.3654, far surpassing all baselines including LLM-based methods (best baseline: Qwen2.5-14B at 0.2550/0.2250/0.3237). This is an out-of-domain benchmark (not used for training), demonstrating that the understanding-retrieval-augmentation paradigm generalizes to highly specialized domains where semantic fragmentation is most damaging.

#### ChunkScore as a reliable proxy metric

The lambda sweep and cross-dataset correlation analysis establish ChunkScore as a **direct, efficient evaluation metric** that can replace expensive downstream-task evaluation. With Pearson correlations exceeding 0.85 on all four datasets at lambda = 0.3, ChunkScore reliably discriminates chunking quality without requiring end-to-end RAG pipeline execution. The optimal lambda reveals a practical insight: semantic dispersion (70% weight) matters more than boundary clarity (30% weight), guiding practitioners to prioritize information coverage over clean cuts. ChunkScore also serves as the adjudicator in QChunker's multi-path sampling, enabling the segmentation agent to select optimal chunking schemes autonomously.
