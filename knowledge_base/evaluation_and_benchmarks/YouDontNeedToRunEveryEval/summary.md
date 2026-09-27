# You Don't Need to Run Every Eval

**Paper:** [You Don't Need to Run Every Eval (Yuchen Zeng, Dimitris Papailiopoulos, 2026)](https://arxiv.org/abs/2606.24020)

## Human Readable TL;DR

Imagine you're a teacher who wants to know how a student is doing in all 133 subjects, but you only test them on 5. Turns out, because students tend to be "broadly smart" or "broadly weak," those 5 subjects can predict the other 128 with surprising accuracy. AI model benchmarking works the same way -- this paper shows you only need to run 5 carefully chosen tests to predict a model's score on all the rest, cutting evaluation costs by ~70-80% while staying accurate within 4 points.

## TL;DR

The authors analyze a matrix of 84 frontier LLMs evaluated across 133 benchmarks and discover it is approximately rank-2 -- just two latent factors explain >90% of variance. They build **BenchPress**, a logit-space bias-decomposed alternating least squares completion method, that predicts held-out scores with 4.6-point median absolute error. Selecting just 5 probe benchmarks (GPQA-D, HLE, Codeforces, MMLU-Pro, ARC-AGI-1) recovers full scorecards to 3.93 points error.

---

## Problem & Motivation

LLM development requires running 40+ benchmarks repeatedly during training, for checkpoint selection and release reporting. This is expensive and redundant if benchmark scores are highly correlated. The authors ask: is exhaustive evaluation necessary, or can a strategic subset predict the rest? They find the answer is largely no -- the benchmark landscape is highly redundant due to an underlying low-rank structure in model capabilities.

---

## Main Original Ideas

1. **Rank-2 Score Matrix Discovery.** The 84×133 model-benchmark score matrix is approximately rank-2 in both raw and logit-transformed spaces. Two singular components explain >90% of variance across complete submatrices (stable rank consistently ≈1.1-1.3). This is an empirical finding, not an assumption.

2. **BenchPress: Logit-Space Bias-Decomposed ALS.** The prediction model decomposes each score into four additive terms: global level + model offset + benchmark offset + rank-2 residual. Operating in logit space (mapping [0,100] percentages to unbounded scale) outperforms 7 other transforms. Among 12 candidate methods evaluated across 84 transform-method combinations, Logit Bias ALS at rank 2 with λ=0.1 achieves near-best accuracy with full prediction coverage (4.63 median absolute error).

3. **Greedy Probe Set Selection.** Rather than random benchmark selection, greedy probe picking minimizes prediction error over the remaining matrix. Five probes recover full scorecards at 3.93 points error (cost-unrestricted: GPQA-D, HLE, MMLU-Pro, ARC-AGI-1, Codeforces; budget-constrained: GPQA-D, MMLU-Pro, Aider Polyglot, MATH-500, AIME 2026 → 4.55 points).

4. **Reliability Analysis via Hypothesis Testing.** Systematic testing of 16 hypotheses (Spearman + paired Wilcoxon, p<0.01) identifies which factors predict per-benchmark and per-model error: score spread (H3), target coverage (H4), and strong-neighbor availability (H5) matter most at the benchmark level; reasoning model type (H2), capability level (H3), and peer correlation (H5) matter at the model level.

5. **Confidence Layer.** Ensemble spread, matrix-support features (coverage, peer availability, recency), and conformal calibration combine into 90% prediction intervals -- users can detect when BenchPress extrapolations are unreliable before trusting them.

---

## Key Findings

| Scenario | Probe Count | MedAE (pts) |
|---|---|---|
| Full matrix (all benchmarks observed) | All | 4.63 |
| 5 greedy probes (cost-unrestricted) | 5 | 3.93 |
| 5 greedy probes (budget-constrained) | 5 | 4.55 |
| Temporal holdout (27 post-DeepSeek-R1 models, 5 seeds) | 5 | 4.83 |
| Temporal holdout (10 seeds) | 10 | 2.57 |
| GPT-5.5 LLM baseline (names visible) | All | 3.50 |
| GPT-5.5 LLM baseline (anonymized) | All | 4.70 |

- Two SVD components explain >90% variance in every tested complete submatrix (4 to 13 benchmarks × 6 to 42 models).
- For model pairs separated by ≥5 points, BenchPress preserves correct ranking 92.1% of the time (454,090 comparable pairs).
- Cost-aware greedy probe selection tracks cost-unrestricted greedy closely -- the most informative benchmarks are already low-cost.
- Model size and provider identity do not significantly affect prediction quality; reasoning model type does (easier to predict).

---

## Suggestions & Future Directions

1. Combine with item-level benchmark compression (fewer questions per benchmark) for end-to-end cost reduction beyond probe selection alone.
2. Investigate the geometric reason rank-2 structure emerges from model capability space -- what do the two factors represent?
3. Re-derive probe sets dynamically as the matrix evolves with new models and benchmarks (current sets are snapshot-specific).
4. Extend to other AI evaluation domains: robotics, biology, chemistry benchmarks.
5. Integration with active learning -- adaptively pick the next benchmark to run based on remaining uncertainty.
6. Acknowledge: BenchPress identifies which scores are mutually predictable, not which benchmarks are redundant for other purposes (failure-mode discovery, contamination monitoring, incentive shaping).

---

## Authors & Institutions

Yuchen Zeng, Dimitris Papailiopoulos -- University of Wisconsin-Madison

## Artifacts Released

- Public score matrix (84 models × 133 benchmarks) on Hugging Face
- BenchPress code on GitHub
- Interactive score prediction tool
- Versioned audit pool: 188 models × 316 benchmarks for extensibility
