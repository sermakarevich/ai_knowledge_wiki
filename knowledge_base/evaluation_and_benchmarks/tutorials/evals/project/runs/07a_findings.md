# Chapter 07a — Statistics: confidence intervals, paired tests, and how thin our samples really are

## What this is

Every previous chapter reported a single point estimate — a pass rate, a
kappa, a rho — and called it a day. This chapter does two things and *nothing
else* (no LLM calls, no new experiments):

1. **Adds a confidence interval (CI) to every one of the 18 existing
   experiments.** A CI says "the true value could plausibly be anywhere in
   this band, not exactly at this number." It is computed by **bootstrapping**
   (re-sampling the same data thousands of times, seed 0, so it's
   reproducible with no model at all).
2. **Quantifies how big a sample we would actually need** to *trust* a
   difference we claim between two versions — the **power / sample-size**
   calculation.

The uncomfortable punchline is already visible: with the ~60 tickets / ~100
pairs every chapter used, most of our "results" are too uncertain to act on,
and the differences we are tempted to celebrate are mostly noise.

## Method

- **Unpaired bootstrap CI** — `bootstrap_ci(values, stat, n_boot=2000)`: sample
  indices *with replacement*, recompute the statistic, take the 2.5 / 97.5
  percentiles. Used for per-ticket statistics (the 04_* and 05_* experiments,
  and the *point* CIs in 06_*).
- **Wilson CI** — `wilson_ci(k, n)`: the proportion-accurate interval used as a
  sanity check that our pass-rate CIs are not off.
- **Clustered bootstrap CI** — `clustered_bootstrap_ci(values, clusters)`:
  re-samples *whole clusters* instead of items. In this tutorial each ticket
  belongs to a **topic** (from `load_tickets()`); a topic's items share
  context, so treating them as independent under-counts the true uncertainty.
  Ticket-based runs therefore also report a *clustered* CI, which is always
  **wider** than the naive one.
- **Paired bootstrap** — `paired_bootstrap(a, b)`: resamples the *same* pair
  positions so a vs b are compared on identical items; reports the mean
  difference, its CI, and a two-sided p.
- **McNemar** — `mcnemar(a, b)`: the exact two-sided test for *binary* paired
  outcomes (the discordant pairs are what carries all the signal).
- **Power** — `power_binary` / `power_paired`: how many items, at a target
  effect size and power, would we need for an unpaired or a paired test.
- All of the above is `numpy` + the standard library. No `scipy`, no network.

## Headline: the 95 % CI on every primary metric

Width is `hi − lo`. **The width, not the point, is the story.**

| experiment | metric | point | CI (95 %) | width |
|---|---|---|---|---|
| `04_checks_answer_v1` | all_checks_pass | 0.125 | [0.05, 0.20] | **0.150** |
| `04_similarity_answer_v1` | auroc_embed_vs_label | 0.822 | [0.719, 0.926] | **0.206** |
| `04_triage_v1` | f1_macro | 0.670 | [0.548, 0.792] | **0.243** |
| `05_judge_did_not_answer` | kappa | 0.131 | [−0.125, 0.386] | **0.511** |
| `05_judge_missing_required_fact` | kappa | 0.056 | [−0.174, 0.286] | **0.459** |
| `05_judge_missing_required_fact_nocontext` | kappa | −0.137 | [−0.275, 0.000] | **0.274** |
| `05_judge_overall` | kappa | 0.163 | [−0.088, 0.414] | **0.502** |
| `05_judge_unsupported_claim` | kappa | −0.110 | [−0.189, −0.031] | **0.158** |
| `05_judge_wrong_section_retrieved` | kappa | 0.000 | [0.000, 0.000] | **0.000** |
| `05_likert_overall` | auroc | 0.374 | [0.164, 0.585] | **0.421** |
| `06_agreement_atla/selene-mini` | agreement_with_humans | 0.615 | [0.520, 0.710] | 0.190 |
| `06_agreement_gemma4` | agreement_with_humans | 0.615 | [0.520, 0.710] | 0.190 |
| `06_agreement_qwen3.8:27b` | agreement_with_humans | 0.613 | [0.533, 0.693] | 0.160 |
| `06_bias_atla/selene-mini` | position_flip_rate | 0.210 | [0.130, 0.290] | 0.160 |
| `06_bias_gemma4` | position_flip_rate | 0.215 | [0.140, 0.290] | 0.150 |
| `06_bias_qwen3.8:27b` | position_flip_rate | 0.210 | [0.147, 0.273] | 0.127 |
| `06_bradley_terry` | spearman_rho | 0.386 | [−0.229, 1.000] | **1.229** |
| `06_panel` | panel_agreement | 0.700 | [0.610, 0.790] | 0.180 |

## Observations

### 1. The point estimates everyone quoted were too confident
Almost every metric has a CI of width 0.15–0.5. The two most dramatic:

- **`05_judge_overall` kappa = 0.16** had a CI of **[−0.09, 0.41]**. A kappa of
  0.16 reads as "barely above chance"; a 95 % CI that *crosses zero* means the
  judge's agreement with the reference is **statistically indistinguishable
  from chance**. The chapter-05 conclusion ("the judge disagrees with the
  rubric") is the honest one, but the headline 0.16 was doing more talking
  than the data supports.
- **`06_bradley_terry` rho = 0.39** has a CI of **[−0.23, 1.00]** — so wide the
  upper bound is clipped at 1. On six models a single Spearman value is
  over-determined by one flipped ranking; "the judges reconstruct the
  leaderboard at 0.71" (chapter 06's GPT-4 reference) and "0.39 on this
  subset" are the *same phenomenon* reported on different data, not a
  contradiction, but neither number is trustworthy on its own.

### 2. Clustering matters — and is exactly the right correction
For every ticket-based run the **clustered-by-topic CI is wider** than the
naive one, because a topic is the true unit of variation:

| run | naive CI | clustered CI |
|---|---|---|
| `04_triage_v1` (f1_macro) | [0.548, 0.792] | [0.423, 0.716] |
| `05_judge_overall` (kappa) | [−0.088, 0.414] | [−0.100, 0.406] |
| `04_checks_answer_v1` (pass) | [0.05, 0.20] | [0.033, 0.20] |

The direction is consistent (clustered ≥ naive) and the magnitudes are small
because most topics carry 1–2 tickets, but the *method* is the right one: any
per-item analysis whose items are grouped by topic is, strictly speaking,
under-stating its own uncertainty.

### 3. One clean *negative* result survived the interval
`05_judge_unsupported_claim` kappa = **−0.11** with CI **[−0.19, −0.03]** —
the interval *excludes zero* and sits entirely on the wrong side. That is the
one place in the whole tutorial where the CI does the job of a "significant"
badge: **the judge measurably disagrees about unsupported claims, in the
opposite direction from the rubric.** Every other 05_judge_* row crosses zero
except the degenerate `wrong_section_retrieved` (0 vs 0, width 0).

### 4. Pairing the same items is the single biggest sample-size saver
The power table (`runs/07_power_table.md`) shows why this tutorial's
100–150 *pairs* are far more honest than their 60 *tickets* would be:

| target pass-rate delta | unpaired n/arm | paired n/pairs (q = 0.30) |
|---|---|---|
| 5 pts | **1565** | 942 |
| 10 pts | **388** | 236 |
| 20 pts | 93 | 59 |

Pairing the same items cuts the required 10-point sample from **388 to 236**
(~39 % fewer), because the shared-item variance cancels out of the comparison.
That is the *only* reason chapter 06's pairwise setup is statistically
defensible at n ≈ 100–150; the unpaired per-ticket numbers in chapters 04/05
are not.

### 5. n = 60 can detect only a ~25-point change at 80 % power
Inverting `power_binary` at alpha = .05 / power = .80:

- delta 0.15 → need **170** items/arm (over 2× what we have)
- delta 0.18 → need **117** items/arm
- delta 0.25 → need **58** items/arm
- delta 0.30 → need **39** items/arm

So with our n = 60 tickets, the **smallest honest pass-rate change we could
have detected is ~24–25 points**. A "5-point improvement" is not a
finding on this data — it is below the noise floor. The same logic applies to
every 05_judge_* kappa comparison: most of them are within a coin-toss of each
other once the CI is drawn.

## Bottom line

- **No LLM calls, no new data — only the math.** Bootstrap (n_boot = 2000,
  seed 0) gives every metric an honest 95 % band.
- **Most point estimates were over-confident.** CIs on the 05_judge_* kappas
  all cross zero except one (unsupported_claim, which excludes zero in the
  wrong direction — the tutorial's only genuinely *negative* judge result).
- **Cluster-by-topic CIs are wider than item-level CIs.** Same data, same
  estimate, *more honest* uncertainty. Use the clustered numbers anywhere a
  metric is computed over topic-grouped items.
- **Pairing is the cheapest free lunch available.** 100–150 paired items
  carries roughly as much information as ~400 unpaired. Chapter 06's design is
  statistically defensible; chapters 04/05's are not.
- **n = 60 detects only ~25-point changes.** Every "small improvement" claimed
  earlier in the tutorial should be re-read as "inconclusive."
- **To make a claim with confidence we need ~10–20× more data** per the
  sample-size table, or a *pairwise* design that squeezes the same information
  out of fewer items.

## Reproducing

```
cd project
just stats-retrofit                       # recompute every CI -> runs/*/metrics.json + runs/results.md
just stats-power                          # sample-size table (stdout)
just stats-test                           # pytest tests/test_07_stats.py
# individual probes:
uv run python -m evals_tutorial.stats ci --experiment 05_judge_overall --n-boot 4000
uv run python -m evals_tutorial.stats paired \
    --a "0.62,0.55,0.60,0.48,0.58" --b "0.55,0.50,0.52,0.40,0.51"
uv run python -m evals_tutorial.stats power --p0 0.5
```

Artifacts:

- `src/evals_tutorial/stats.py` — every function used above (no new deps).
- `tests/test_07_stats.py` — 20 fast tests, all deterministic.
- `runs/*/metrics.json` — each primary metric now has a `ci` entry.
- `runs/results.md` — rebuilt by `retrofit`, `CI` column populated.
- `runs/07_power_table.md` — sample-size table.
