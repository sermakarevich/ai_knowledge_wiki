# RoPoLL: Robust Panel of LLM Judges

**Paper:** [RoPoLL: Robust Panel of LLM Judges (Acharya, Pan, Verkhovsky, 2026)](https://arxiv.org/abs/2606.30931)

## Human Readable TL;DR

Imagine a panel of three judges scoring a talent show and reporting the average score. That works fine if judges disagree only a little, randomly, around the true value. But what if one judge falls asleep and scores everything zero, or is a pushover and rates everything a perfect 10? A simple average gets dragged badly off course by that one bad judge -- and adding more good judges to the panel doesn't fix it, because the average is still poisoned by the one broken vote. This paper shows that "juries" of AI models used to grade other AI models' answers have exactly this problem: a single AI judge that chokes (spits out garbage, is a suck-up, or panics and refuses to answer) can throw off the whole panel's verdict no matter how big the panel is. The fix is to stop averaging and instead find the panel's "geometric median" -- the single point that is closest, in total, to all the judges' scores at once. It's a bit like finding the most central meeting spot for a group of people scattered across a city: one person standing off in the middle of nowhere barely moves that spot, whereas it would badly skew a plain average of everyone's coordinates. Using this trick, a panel of three cheap AI judges can beat one giant, expensive judge model at spotting quality differences, even when a third of the panel's votes are unreliable.

## TL;DR

The paper formalizes "LLM Jury" evaluation (Panel of LLM judges, PoLL, which averages judge scores) under the Huber ε-contamination model and proves the arithmetic-mean aggregator has unbounded bias under any positive contamination rate, regardless of jury size, whenever a single judge fails in an LLM-typical biased way (mode collapse/parser failure, sycophancy, refusal). It reframes jury aggregation as classical robust mean estimation and proposes RoPoLL, which keeps the PoLL panel structure but swaps the mean for the geometric median (GM) -- tuning-free, joint-distance-preserving, with the optimal finite-sample breakdown point of 1/2. A finite-sample upper bound (Theorem 1) and a matching minimax lower bound (Theorem 2) agree on the parametric rate σ√(d/N) but differ by a factor of √d on the breakdown floor -- a statistical-computational gap that GM's polynomial-time tractability pays relative to the NP-hard Tukey halfspace median. Across 13 open-weight judges (4B-675B), three reward-model benchmarks (HelpSteer2, HelpSteer3, UltraFeedback), and four corruption regimes up to 50%, RoPoLL beats PoLL on every biased corruption type -- by about 19% on cross-dimensional attacks at matched compute, and by orders of magnitude under heavy-tailed Byzantine corruption -- while paying at most a 6.4% "insurance premium" in RMSE when no corruption is present.

---

## Problem & Motivation

Reliable evaluation is the bottleneck for aligning LLMs: human evaluation doesn't scale, so the field relies on LLM-as-a-Judge, where another model scores outputs. A single judge is a single point of statistical failure -- its backbone's biases (position, verbosity, self-enhancement, sycophancy, refusal artifacts) propagate uncorrected into every score. The natural fix is the LLM Jury / Panel of LLM Evaluators (PoLL, Verga et al. 2024): ensemble several smaller, diverse, cheaper judges and report the arithmetic mean as consensus. Averaging is statistically optimal precisely when judge errors are light-tailed and centered on the truth (variance shrinks at the parametric rate 1/N).

The catch: real LLM judges don't fail like Gaussian noise. A judge that emits malformed JSON triggers a parser fallback to an all-zeros score. A sycophantic judge rates everything near the maximum, flattening real quality differences. A judge that handles one attribute well may catastrophically mis-score another, producing a score vector that looks plausible per-coordinate but is jointly anomalous. A hallucinating parser can emit values entirely outside the valid score range. These four failure modes -- mode collapse, sycophancy, cross-attribute confusion, heavy-tailed hallucination -- are all biased point masses far from the truth, not symmetric perturbations of it, and they occur at non-trivial real rates (parser failure alone reaches 33% for the smallest judge tested, Gemma-4B, on multilingual HelpSteer3 prompts). Under the classical Huber ε-contamination model this is exactly the regime where mean-based aggregation is known to break: the paper's Proposition 2 proves PoLL's conditional bias grows linearly with the corruption shift and is unbounded over the contamination class for any jury size N -- the 1/N variance reduction that motivates juries cannot rescue an aggregator whose bias is itself unbounded.

---

## Main Original Ideas

1. **Formalizing the LLM Jury under Huber contamination** -- Mapping the real, observed judge failure modes (parser-failure/mode-collapse, sycophancy, cross-attribute confusion, heavy-tailed hallucination) onto four canonical contamination distributions used in the experiments: zeros, inverted, bimodal-random, and cauchy-far.
2. **Proposition 2: unbounded bias of PoLL** -- A direct proof that the arithmetic mean's bias grows linearly with the corruption shift and is unbounded over the contamination class regardless of jury size N, formally establishing why simply adding more judges to a PoLL-style jury cannot fix a biased failure.
3. **RoPoLL -- geometric median as the aggregator** -- Among robust-estimator candidates (coordinate-wise median, trimmed mean, geometric median), the paper selects the geometric median (GM) because it is tuning-free (no contamination-rate hyperparameter, unlike the trimmed mean), joint-distance-preserving (operates on the full Euclidean score vector, capturing cross-attribute structure that coordinate-wise methods miss), and attains the optimal finite-sample breakdown point of 1/2. GM is computed via a modified Weiszfeld iteration (Algorithm 1) at O(N·d·log(1/ε)) per query.
4. **Matching finite-sample upper and minimax lower bounds** -- Theorem 1 (upper bound) and Theorem 2 (minimax lower bound) agree exactly on the parametric rate σ√(d/N), but differ by a factor of √d on the breakdown floor. This is a genuine statistical-computational gap: the intractable (NP-hard for d≥3) Tukey halfspace median hits the optimal breakdown floor, while RoPoLL's geometric median pays a √d penalty in exchange for polynomial-time tractability. Since the score dimension d is small (1-5) in the benchmarks tested, this overhead is at most ~2.2x and is dominated by the variance term at the jury sizes used.
5. **Equicorrelated jury extension and effective-jury-size saturation** -- Lemma 3 relaxes the i.i.d. judge assumption to allow inter-judge correlation γ. The effective jury size N_eff = N/(1+(N-1)γ) saturates at 1/γ as N→∞, explaining empirically why 3-judge committees capture most of the achievable benefit given the γ ≈ 0.3-0.7 correlations measured among real open-weight judges.

---

## Key Findings

| Corruption regime | Comparison | PoLL (mean) | RoPoLL (geometric median) | Result |
|---|---|---|---|---|
| Heavy-tailed (cauchy-far), r=40% | Medium jury (~89B), HelpSteer2 | RMSE ≈ 4,951 | RMSE ≈ 9.2 | RoPoLL wins by ≈540x |
| Cross-dimensional (bimodal-random), r=30% | Small jury (38B) vs. Mistral-Large-3 (675B), HelpSteer2 | 1.55 (Mistral-Large-3) | **1.18** (Small jury) | 1.31x more accurate at 18x fewer parameters |
| Cross-dimensional (bimodal-random), r=30%, compute-matched | Small jury (38B), same 3 judges, HelpSteer2 | RMSE ≈ 1.45 | **RMSE 1.18** | ≈19% RMSE reduction at identical inference cost |
| Cross-dimensional (bimodal-random), r=30% | Medium jury (89B) vs. DeepSeek-V3.1 (671B), HelpSteer3 | 1.85 (DeepSeek-V3.1) | **1.85** (Medium jury) | Matches a 671B judge at 89B |
| Bounded mean-preserving (zeros/inverted), r=30% | Medium jury, all benchmarks | baseline | gap ≤ 0.3 RMSE | Smallest RoPoLL advantage -- these are the regimes hardest to separate |
| Clean baseline, r=0% | All 4 juries, all benchmarks | baseline | +0.9% median, ≤6.4% max relative RMSE | Small "insurance premium" for using RoPoLL when no corruption is present |
| Noisy-GT control (unbiased Gaussian noise, not bias) | All juries | slightly better | slightly worse | Confirms the RoPoLL premium is paid against biased contamination, not benign imprecision (PoLL is optimal there) |

- Experiments span 13 open-weight judges from 4B to 675B parameters (Mistral-Large-3, DeepSeek-V3.1, Qwen3-235B/32B, Nemotron-30B/12B/9B, Gemma-27B/12B/4B, Magistral-Small-24B, Ministral-14B/8B) and four 3-judge committees (Medium ~89B, Mixed ~53B, Small ~38B, Tiny ~21B).
- Naturally-occurring parser-failure rates (not synthetic corruption) average 3.4% on HelpSteer3 and 0.6% on HelpSteer2 across the 13-judge panel, reaching 33% on the smallest judge for multilingual prompts.
- The choice of jury size N=3 is corroborated empirically: the diminishing-returns knee in accuracy vs. jury size sits at N≈3, matching the saturation law's prediction from measured inter-judge correlations (γ̄ = 0.49 on HelpSteer2/3, 0.71 on UltraFeedback).
- The authors release a corpus of ~28K scored (judge, sample) cells across the 13-judge x 3-benchmark panel for reproducibility.

---

## Suggestions & Future Directions

1. Extend the theory beyond the i.i.d. baseline to per-judge heterogeneity -- different noise levels and contamination rates across the 4B-675B parameter range.
2. Tighten the √d gap between the finite-sample upper bound (Theorem 1) and the minimax lower bound (Theorem 2) at finite contamination rate α.
3. Run a large-scale evaluation against naturally-occurring judge failures on a downstream alignment task -- the current corruption sweep is synthetic injection at a single rubric format and temperature 0, so it doesn't probe prompt-format sensitivity.
4. Systematically compare against the broader robust-aggregation toolbox: median-of-means, smoothed Tukey depth, and learned calibration.
5. Study explicit-dependence jury designs (peer-rank discussion, multi-agent debate, judge networks) rather than the i.i.d. panels analyzed here.
6. Outlook: the corruption-class diagnosis (biased, low-rate point-mass failures) is argued to transfer to any pipeline with heterogeneous workers producing similar errors -- reward-model ensembles for RLHF, synthetic-data filtering juries, and crowd annotation -- suggesting the geometric median as a candidate default aggregator beyond LLM juries.

---

## Authors & Institutions

Anish Acharya (Amazon Web Services), Kris W. Pan (Amazon Web Services), Brian Verkhovsky (Amazon Web Services).
