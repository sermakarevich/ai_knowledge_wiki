# When Does Combining Language Models Help? A Co-Failure Ceiling on Routing, Voting, and Mixture-of-Agents Across 67 Frontier Models

**Paper:** [When Does Combining Language Models Help? (Chen, 2026)](https://arxiv.org/abs/2606.27288)

## Human Readable TL;DR

Imagine hiring several experts to double-check each other's work, hoping their combined answer beats any one expert alone. That only pays off if the experts tend to make *different* mistakes. This paper shows that on hard, open-ended tasks, today's best AI models increasingly get the exact same questions wrong -- so no amount of voting, routing between them, or mixing their answers can rescue those shared blind spots. Worse, the simple "how correlated are their mistakes" number everyone uses to judge this is misleading -- it looks fine even when the models fail together far more often than it predicts, and that blind spot gets worse the more models you throw into the pool.

## TL;DR

For any policy that outputs one member model's answer (router, vote, cascade), accuracy is capped at 1 - β, where β is the rate at which every model in the pool is wrong on the same query. The commonly reported average pairwise error correlation ρ cannot identify β -- distributions with identical marginals and pairwise correlations can have very different β (proved via a Fréchet-class counterexample). Across 67 frontier models from 21 providers (GPT-5.5, Claude Opus 4.8, Gemini 3.1 Pro, Grok-4.3, DeepSeek V4, Qwen3.7-Max, Kimi K2.7, etc.), a correctly tetrachoric-calibrated single-factor copula still underprices the all-wrong tail by ~2.5x on open-ended math (β=0.052 vs. predicted 0.023) and by similar margins on execution-graded code (β=0.079), with the underpricing ratio growing with pool size. At matched quality, a diverse low-ρ ensemble beats a high-ρ Self-MoA (mixture-of-agents on one model's own samples) ensemble. Re-asking GPQA-Diamond in free-response instead of multiple-choice form reopens a large co-failure tail (β=0.127), showing the effect is driven by task format, not subject matter. Bottom line: on their verifiable-task pool, combining models rarely beats the single best model without a strong query-level routing signal -- gains come from models failing on *different* questions, not from adding more models.

---

## Problem & Motivation

Multi-model LLM systems -- routing, voting, cascades, fusion, mixture-of-agents (MoA) -- are widely used on the assumption that combining models pushes accuracy past any single model. Practitioners typically justify or size this expected gain using average pairwise error correlation ρ. The paper's core claim is that ρ is the wrong quantity: it says nothing about how often *all* models in the pool fail on the same query (the co-failure rate β), and β -- not ρ -- is what actually bounds the achievable gain from any selection-based combination method. Prior work lacked both a theoretical ceiling tied to the right statistic and large-scale empirical evidence of how badly ρ misprices that ceiling as pools scale to dozens of frontier models.

---

## Main Original Ideas

1. **The co-failure ceiling.** Any selection policy (router, weighted vote, cascade) whose output is always one of the pool's own answers cannot exceed accuracy 1 - β, where β = Pr[all m models wrong on the same query]. The maximum possible gain over the single best model is exactly (1 - β) - a_sb, attained only by a per-query oracle.

2. **Gain localization.** The achievable gain over single-best decomposes cleanly: it comes entirely from queries where the single-best model is wrong but the pool is not unanimous. The co-failure tail β contributes zero to this gain -- it is dead weight no combination method can recover.

3. **Pairwise correlation ρ systematically underprices β, worse as pools grow.** Under a common-shock mixture model (each query is "co-hard" with probability π, causing simultaneous failure across the whole pool), the true co-failure rate β(m) converges to π > 0 as pool size m grows, while a single-factor Gaussian copula calibrated to the same marginal error rate and pairwise ρ predicts β_sf(m) → 0. The ratio β(m)/β_sf(m) diverges to infinity as m increases -- ρ becomes an increasingly bad proxy exactly when pools get large.

4. **Non-identification of β from pairwise statistics (Fréchet-class result).** For m ≥ 3 models, β is not a function of the pairwise error law at all: there exist joint failure distributions with identical 1D/2D marginals and identical Pearson/tetrachoric pairwise correlations but different β (concrete 3-model counterexample given: β = 0 in one construction vs. β = 1/4 in another, same pairwise statistics). No statistic derived only from pairwise correlations -- including a single-factor copula fit -- can ever recover β.

5. **A $0 realizability certificate.** A Clopper-Pearson lower confidence bound on β, computed from one held-out graded query set, upper-bounds the best possible gain any selection policy could ever deliver -- before training a router or paying for orchestration. If the certified ceiling is below the orchestration overhead, no policy in that class can pay for itself.

6. **Matched-quality diversification result.** Naive unweighted majority voting across models of differing quality tends to *hurt* (regressing vote-gain-over-best-member on ρ gives a negative slope in the paper's pools). But once quality is matched (a 6-model accuracy-matched band), a diverse low-ρ heterogeneous ensemble reliably beats a high-ρ Self-MoA ensemble sampled repeatedly from one strong model -- isolating diversity, not raw model count, as the actual lever.

7. **Format, not subject matter, drives co-failure tails.** Re-grading the same GPQA-Diamond questions as free-response instead of multiple-choice reopens a large co-failure tail (β jumps from ~0 to 0.127), showing that answer format -- not the underlying scientific content -- determines whether models fail in correlated lockstep.

---

## Key Findings

| Domain | Models / queries | Single-best acc. | Oracle acc. | Oracle gain G | Co-failure β | ρ-implied underpricing |
|---|---|---|---|---|---|---|
| MATH-500 (open-ended math) | 67 / 330 | 0.836 | 0.948 | 0.112 | **0.052** (k=17) | **~2.5x** (90% CI 1.7-3.4x) |
| MATH-Hard (Level-5) | 67 / 298 | -- | -- | -- | 0.044 (k=13) | ~8.3x (90% CI 4.5-16x) |
| code_contests (Codeforces, execution-graded) | 18 / 63 | 0.825 | 0.921 | 0.096 | **0.079** (k=5) | 3.1x tetrachoric (CI [1.5, 6.2]) |
| GPQA-Diamond, multiple-choice | 52 / 130 | 0.846 | 1.000 | 0.154 | ~0 (0/130) | -- (realizability-bound, not ceiling-bound) |
| GPQA-Diamond, free-response (same questions) | 18 models, 5-judge panel | 0.51 (mean fell from 0.66) | -- | -- | **0.127** (k=10) | -- |

- Pillar A (15-model frontier pool): on a saturated multi-domain mix, single-best = 0.923, oracle = 0.967, gain G = 0.044; on hard MMLU-Pro, single-best = 0.850, oracle = 0.970, gain G = 0.120. Mean pairwise ρ was 0.464 and 0.382 respectively, yet naive-Pearson-calibrated predicted β (0.0011 and 0.0050) was 6-30x smaller than the true measured β (0.033 and 0.030).
- A held-out learned router (TF-IDF + domain logistic regression) captured only 9% of the oracle gain G (95% CI spans zero); a gradient-boosted per-model correctness predictor captured -9% (worse than doing nothing); a direct multiclass best-model predictor captured -127% (actively harmful); a deployment-realistic LLM-as-router (GPT-5-mini given a capsule of every model's strengths) routed to the single best model 100% of the time, capturing exactly 0% of G.
- Naive unweighted majority voting across quality-mismatched models produced negative average gain over the best individual member (-0.10 hard regime, -0.02 saturated regime) across all 455 three-model triplets tested.
- At matched quality, a diverse low-ρ ensemble (ρ=0.42) beat a high-ρ Self-MoA ensemble (ρ=0.80) by +0.027 average accuracy across 60 resampling partitions (positive in all 60); the gain shrank to +0.020 (not significant) on the higher-correlation MATH-500 regime.
- Cascades (cheap model L=GPT-5-nano, expensive H=Claude Opus 4.8, self-consistency verifier AUC=0.899): cascade beat random mixing at matched budget by +0.114 accuracy on a held-out fold; the theoretical volume ceiling for this pair was 1 - a_L/a_H = 0.188.
- Pool-size resampling: the tetrachoric underpricing ratio rose monotonically from 1.0x at pool size k=2 to a median 2.5x at k=67 -- confirming the underpricing is a genuine pool-scaling effect, not an artifact of which models happen to be included.
- Frontier cost-per-correct-answer fell ~14-15x over an 18-model, 2024-2026 generational pool; the "option value" of staying flexible across model releases was worth +0.33 accuracy by 2026 on hard MMLU-Pro, but only +0.01 on saturated GSM8K.

---

## Suggestions & Future Directions

1. Run a tight-ratio code-domain replication with ≥3 seeds and held-out model selection to sharpen the current k=5-event estimate on an 18-model pool.
2. Extend the matched-quality diversification experiment across multiple ρ levels to empirically fit the sensitivity parameter λ and predict the diversification limit k* out of sample (currently rests on one provider-matched band).
3. Benchmark against the theoretically optimal cascade-routing policy (per Dekoninck et al.) rather than only a naive confidence-based cascade, and construct a deferral rule conditioning on both the cheap and expensive model's signals (the current verifier scores only the cheap model, which is provably dominated).
4. Run a price-controlled tail-edge experiment to disentangle cost from co-failure effects.
5. Test whether the co-failure ceiling and ρ-underpricing results extend to open-ended generative tasks beyond the paper's verifiable (programmatically or panel-graded) benchmark pool -- explicitly flagged as open.
6. The static-price routing analysis (Appendix A) is only valid within a release epoch; future work should integrate it with the churn/option-value model (Appendix E) rather than treating them separately.

---

## Authors & Institutions

Josef Chen, KAIKAKU.
