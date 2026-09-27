# Chapter 07 — Statistics (CI + power) and a paired A/B of a better prompt

This chapter is two halves that share one theme: *a point estimate is a lie
until you show its band, and a difference is a finding only once you test it on
the same items.*

- **07a** adds a confidence interval (CI) to every existing experiment, with no
  new data and no model calls.
- **07b** writes a second prompt (`answer_v2`) that targets the two most common
  failure modes, runs it, and compares it to the baseline with the *same
  frozen judge* on the *same 60 test tickets* — a proper paired comparison with
  the stats 07a introduced.

---

# Part 1 — 07a: confidence intervals, paired tests, and how thin our samples really are

## What this is

Every previous chapter reported a single point estimate — a pass rate, a
kappa, a rho — and called it a day. This part does two things and *nothing
else* (no LLM calls, no new data):

1. **Adds a confidence interval to every one of the 18 existing experiments.**
   A CI says "the true value could plausibly be anywhere in this band, not
   exactly at this number." It is computed by **bootstrapping** (re-sampling
   the same data thousands of times, seed 0, so it's reproducible with no model
   at all).
2. **Quantifies how big a sample we would actually need** to *trust* a
   difference we claim between two versions — the **power / sample-size**
   calculation.

## Method

- **Unpaired bootstrap CI** — sample indices *with replacement*, recompute the
  statistic, take the 2.5 / 97.5 percentiles. Used for per-ticket statistics
  and the *point* CIs in the `06_*` pairwise runs.
- **Wilson CI** — proportion-accurate interval, used as a sanity check that
  pass-rate CIs are not off.
- **Clustered bootstrap CI** — re-samples *whole clusters* instead of items.
  Each ticket belongs to a **topic**; a topic's items share context, so treating
  them as independent under-counts the true uncertainty. Ticket-based runs
  therefore also report a *clustered* CI, which is always **wider** than the
  naive one.
- **Paired bootstrap** — resamples the *same* pair positions so a vs b are
  compared on identical items; reports the mean difference, its CI, and a
  two-sided p.
- **McNemar** — the exact two-sided test for *binary* paired outcomes (the
  discordant pairs carry all the signal).
- **Power** — `power_binary` / `power_paired`: how many items, at a target
  effect size and power, would we need.

All of it is `numpy` + the standard library. No `scipy`, no network.

## Headline: the 95 % CI on every primary metric

Width is `hi − lo`. **The width, not the point, is the story.** A selection:

| experiment | metric | point | CI (95 %) | width |
|---|---|---|---|---|
| `04_checks_answer_v1` | all_checks_pass | 0.125 | [0.05, 0.20] | **0.150** |
| `05_judge_overall` | kappa | 0.163 | [−0.088, 0.414] | **0.502** |
| `05_judge_did_not_answer` | kappa | 0.131 | [−0.125, 0.386] | **0.511** |
| `05_judge_unsupported_claim` | kappa | −0.110 | [−0.189, −0.031] | **0.158** |
| `05_likert_overall` | auroc | 0.374 | [0.164, 0.585] | **0.421** |
| `06_bradley_terry` | spearman_rho | 0.386 | [−0.229, 1.000] | **1.229** |

## Observations

### 1. The point estimates everyone quoted were too confident
Almost every metric has a CI of width 0.15–0.5. Two stand out:
- **`05_judge_overall` kappa = 0.16** had a CI of **[−0.09, 0.41]** — a CI that
  *crosses zero* means the judge's agreement with the reference is
  **statistically indistinguishable from chance**.
- **`06_bradley_terry` rho = 0.39** has a CI of **[−0.23, 1.00]** — "the judges
  reconstruct the leaderboard at 0.71" (chapter 06's GPT-4 reference) and
  "0.39 on this subset" are the *same phenomenon* on different data, and
  neither number is trustworthy on its own.

### 2. Clustering matters — and is exactly the right correction
For every ticket-based run the **clustered-by-topic CI is wider** than the
naive one:

| run (metric) | naive CI | clustered CI |
|---|---|---|
| `04_triage_v1` (f1_macro) | [0.548, 0.792] | [0.423, 0.716] |
| `05_judge_overall` (kappa) | [−0.088, 0.414] | [−0.100, 0.406] |

The direction is consistent (clustered ≥ naive); the *method* is the right one.

### 3. One clean *negative* result survived the interval
`05_judge_unsupported_claim` kappa = **−0.11**, CI **[−0.19, −0.03]** — the
interval *excludes zero* and sits entirely on the wrong side. That is the one
place in the whole tutorial where the CI does the job of a "significant"
badge: **the judge measurably disagrees about unsupported claims, in the
opposite direction from the rubric.** Every other `05_judge_*` row crosses zero.

### 4. Pairing the same items is the single biggest sample-size saver

| target pass-rate delta | unpaired n/arm | paired n/pairs (q = 0.30) |
|---|---|---|
| 5 pts | **1565** | 942 |
| 10 pts | **388** | 236 |
| 20 pts | 93 | 59 |

Pairing the same items cuts the required 10-point sample from **388 to 236**
(~39 % fewer). That is the *only* reason chapter 06's pairwise setup is
statistically defensible at n ≈ 100–150.

### 5. n = 60 can detect only a ~25-point change at 80 % power
- delta 0.15 → need **170** items/arm (over 2× what we have)
- delta 0.25 → need **58** items/arm

So with our n = 60 tickets the **smallest honest pass-rate change we could
detect is ~24–25 points**. A "5-point improvement" is not a finding on this
data — it is below the noise floor.

---

# Part 2 — 07b: A/B — does a prompt aimed at the two biggest failure modes actually help?

## What this is

This half *uses* the machinery of 07a on real, new data:

1. Write a second answer prompt, `answer_v2`, that explicitly targets the two
   most common failure modes in the v1 labels — `missing_required_fact` (18)
   and `unsupported_claim` (13).
2. Run it on all 80 tickets with the frozen RAG pipeline (no other change).
3. Judge it **with the exact same judges we already chose in chapter 05**
   (same prompt, same version, same `best` choice) so the *only* thing that
   moves between arms is the answer prompt.
4. Compare with the 07a statistics — paired bootstrap, McNemar, per-check rates
   with multiple-comparisons correction — on the same 60 test tickets.

This is the difference between "I think v2 is better" and "I can show it is."

## Result: no net improvement on overall pass — and the data *cannot* tell a 2-point swing from noise

Primary metric, judge-vs-judge, test split (n = 60 pairs):

| | value |
|---|---|
| v1 overall pass rate (frozen judge) | **0.70** (42/60) |
| v2 overall pass rate (frozen judge) | **0.70** (42/60) |
| paired delta (v2 − v1) | **0.0**, 95 % CI **[−0.117, +0.117]** |
| McNemar (v2 fixes / v2 breaks) | **7 / 7**, p = **1.0** |

The two arms land on the **same pass rate**. McNemar says 7 tickets that v2
*fixed* but v1 failed, and 7 that v2 *broke* but v1 passed — a perfectly
balanced, **statistically indistinguishable** swap. The 95 % CI on the delta
spans ±12 points, which is *wider than any real difference we are likely to
have produced* (07a told us the noise floor at n = 60 is ~25 points).

**This is the honest A/B result: "no difference," not "v2 is worse" and not
"v2 is better."** With this much data, a genuine 2–5-point gain would be
invisible.

## The interesting thing is *where* the failures move

Overall pass is the same, but the composition of failures changes in exactly
the directions the new prompt targeted — and pays for it elsewhere:

| failure mode (test) | v1 fails | v2 fails | delta |
|---|---|---|---|
| `missing_required_fact` *(target)* | 7 | 3 | **−4** ✓ |
| `unsupported_claim` *(target)* | 4 | 2 | **−2** ✓ |
| `did_not_answer` | 13 | 15 | **+2** ✗ |
| `wrong_section_retrieved` | 0 | 0 | 0 |

The prompt that told the model *to cite the specific facts* and *not to invent
claims* measurably reduced those two modes (11 → 5 total target-mode fails).
But a "cite more of the answer" steering nudged the model to answer slightly
less completely on a couple of tickets, adding 2 `did_not_answer` fails.
Net: the same 42/60 pass overall, **reallocated, not improved.**

Per-check rates (6 deterministic checks, none survives Bonferroni/BH at α = .05):

| check | v1 | v2 | delta |
|---|---|---|---|
| `no_forbidden_promises` | 0.917 | 0.950 | +0.033 |
| `mentions_section_name` | 0.900 | 0.867 | −0.033 |
| `mentions_all_answer_point_keywords` | 0.933 | 0.917 | −0.017 |
| `max_words_150` | 0.167 | 0.150 | −0.017 |
| `no_phone_or_email_invented` | 1.000 | 1.000 | 0 |
| `nonempty` | 1.000 | 1.000 | 0 |

No check clears the multiple-comparisons bar — another honest "no significant
difference" at per-check granularity.

## Bottom line (both halves)

- **07a — No LLM calls, just the math.** Bootstrap (n_boot = 2000, seed 0) puts
  an honest 95 % band on every metric. Most `05_judge_*` kappas cross zero;
  clustered CIs are wider and more correct.
- **07a — n = 60 detects only ~25-point changes.** Every small improvement
  claimed earlier in the tutorial should be re-read as *"inconclusive."*
- **07b — A targeted prompt moves failure *types* but not the *total*.** It cut
  the two modes it aimed at (11 → 5 fails) at the cost of +2 `did_not_answer`,
  so overall pass stays 0.70.
- **07b — "same" is a legitimate result, and the test is what proves it.**
  McNemar 7/7 (p = 1.0) and a delta CI of ±12 points mean we *cannot claim an
  improvement* on this data; nor can we claim a regression. The next step is
  not another tweak — it is **more data** (per 07a, ~10–20× more, or a paired
  design over more tickets) so that a real difference, if one exists, rises
  above the noise floor.
- **Design note (this is what makes the A/B fair):** the judge was *frozen* and
  the split was identical, so the comparison isolates the one variable we
  changed — the prompt. Swapping judges or splits would let us "cheat" the
  number; we did neither.

## Reproducing

```
cd project

# 07a: CIs + power (no LLM)
just stats-retrofit
just stats-power
uv run python -m evals_tutorial.stats ci --experiment 05_judge_overall --n-boot 4000

# 07b: the A/B
uv run python -m evals_tutorial.helpdesk run --task answer --version v2 --split all
uv run python -m evals_tutorial.judge run --mode all --version best --split test --run answer_v2
uv run python -m evals_tutorial.judge overall --split test --run answer_v2   # composes the 4 modes, 0 LLM
uv run python -m evals_tutorial.code_evals checks --run answer_v2 --split test
uv run python -m evals_tutorial.stats paired --a answer_v1 --b answer_v2      # -> 07_ab_answer_v2_vs_v1

uv run pytest tests/ -q -m "not slow"
```
