# Chapter 05 — LLM-as-judge: test-split results, ablations, and findings

Task `fleet-msccr`. This is the **test half** (05b); the **dev half** (05a) chose the
prompt version per mode on 20 dev tickets. Together they cover the full chapter.

---

## 1. Per-mode results on test (chosen version, n = 60)

| mode | version | true fails | pred fails | TPR | TNR | accuracy | kappa | FN | FP |
|---|---|---|---|---|---|---|---|---|---|
| did_not_answer | v1 | 5 | 13 | 0.400 | 0.800 | 0.767 | 0.116 | 3 | 11 |
| missing_required_fact | v2 | 15 | 7 | 0.133 | 0.889 | 0.700 | 0.027 | 13 | 5 |
| unsupported_claim | v2 | 12 | 4 | 0.000 | 0.917 | 0.733 | -0.111 | 12 | 0 |
| wrong_section_retrieved | v2 | 8 | 0 | 0.000 | 1.000 | 0.867 | 0.000 | 8 | 0 |

**Version chosen per mode** (from 05a dev alignment, primary = higher dev kappa):

| mode | v1 kappa | v2 kappa | chosen | margin |
|---|---|---|---|---|
| did_not_answer | 0.643 | 0.459 | **v1** | +0.184 |
| missing_required_fact | 0.459 | 1.000 | **v2** | +0.541 |
| unsupported_claim | 0.643 | 0.643 | **v2** | tie (tie-break) |
| wrong_section_retrieved | 1.000 | 1.000 | **v2** | tie (tie-break) |

The margin for `missing_required_fact` is the clearest: v1 catches 1 of 3 dev fails
(TPR 0.333) while v2 catches all 3 (TPR 1.000, kappa 1.000). On test that advantage
does not hold — even v2 achieves TPR 0.133 (2 of 15). The other modes are worse:
`unsupported_claim` v2 produces zero positive predictions (all 12 true-fails become
false negatives) and `wrong_section_retrieved` v2 does the same.

**Overall pass** (ticket passes iff no tracked mode fails): kappa 0.155, TPR 0.385,
TNR 0.765. The overall judge inherits the per-mode weaknesses; because 3 out of 4
modes are effectively non-discriminative on test, the overall kappa is dragged down.

---

## 2. Likert (1–5) ablation — first 30 test tickets

| metric | value |
|---|---|
| AUC (score vs pass) | **0.360** |
| mean score | 4.27 / 5 |
| score histogram | 1:0, 2:0, 3:5, 4:12, 5:13 |
| n | 30 |

AUC 0.36 is *below chance* (0.50) — the Likert scores are **weakly inversely
correlated** with the pass label. In plain terms: the LLM tended to give pass replies
slightly *higher* scores than fail replies (mean 4.27), but the scale was too compressed
to separate the two classes. The five points on the scale did not map to the two
failure regimes. All 5 scores of 3 were on failing tickets; all 25 scores of 4–5
were a mix of pass and fail. This is the textbook case of "a single fuzzy number
that blurs out the reason why" — the binary per-mode judges avoid this by
separating the failure axis, even though individual judges are also weak here.

**Comparison**: the best binary judge's test kappa is 0.116 (`did_not_answer` v1);
the Likert AUC of 0.360 is a different metric class and not directly comparable,
but both are far below the 0.64–1.0 kappas observed on dev. The lesson: dev
agreement does not transfer to test under this rubric.

---

## 3. No-context ablation — `missing_required_fact`, first 30 tickets

| condition | n | kappa | TPR | TNR | accuracy |
|---|---|---|---|---|---|
| with context (chosen v2, same 30) | 30 | -0.111 | 0.000 | 0.917 | 0.733 |
| **no context** (handbook text withheld) | 30 | -0.154 | 0.000 | 0.875 | 0.700 |

Delta: kappa drops by 0.043; TPR unchanged at 0.000 (the judge still says "pass"
for every fail). The no-context ablation does not meaningfully change this mode's
performance — the `missing_required_fact` judge relies primarily on the customer's
question and the reply text, not on cross-referencing the retrieved context, so
withholding the hand-back text has minimal effect. This is useful to know: the
judge is NOT verifying that the cited policy is actually in the retrieved section,
which is precisely what a no-context test would expose.

---

## 4. Disagreement review

Full table: `05_judge_disagreements.md`. For `missing_required_fact` (most test
failures, 15 true-fails, 18 disagreements): the dominant error is **false negatives**
(13 of 18) — the judge says pass when the label says a specific fact is missing.
Review of 18 cases: 8 judge wrong, 3 label wrong, 7 ambiguous.

Two representative critiques:

> **tkt-047** (FN, judge wrong) — Label: "The reply omits the required key fact
> that the minimum purchase amount is $25.00 per card." Judge: "The reply correctly
> conveys the required facts that digital gift cards are delivered within 15 minutes
> and can be re-sent." — *The judge evaluated a different aspect of the reply
> (delivery speed) and never checked whether the $25 minimum was stated.*

> **tkt-074** (FP, label wrong) — Label: "reply matches the reference standard."
> Judge: "The customer explicitly asked the assistant to review their account
> history. The assistant failed to perform this review." — *The label explicitly
> marks this as a pass; the judge is hallucinating a missing-fact failure that the
> annotator did not recognise.*

---

## 5. LLM calls and wall time

| step | calls | seconds | notes |
|---|---|---|---|
| step 1 (4 modes × 60) | 240 | ~5,800 (4 modes parallel, ~10 min wall) | fresh calls, 240/450 budget used |
| step 2 (overall) | 0 | 0 | cache hits, zero fresh calls |
| step 3 (likert, 30) | 30 | 72 s | fresh calls |
| step 4 (nocontext, 30) | 30 | 81 s | fresh calls |
| **total fresh** | **300** | **~10 min** | within 450 budget |

Note: per-mode `seconds` in `metrics.json` (~580 s each) are the shared wall clock —
the four modes run in parallel threads within one client process, so they share the
same timer. `llm_calls` in each mode's file shows 235–240 because it records the
total calls made by the shared client, not mode-specific calls.

---

## 6. What was skipped

- **Confidence intervals** — deferred to chapter 07 per spec (`ci = {}`).
- **`answer_v2` trace evaluation** — the task spec (step 1) only requires `answer_v1`
  traces on test; `answer_v2` will be covered when that split is ready.
- **Per-mode `ci` fields** in `metrics.json` — empty dicts, to be filled in ch. 07.
- **Full Likert on all 60 test tickets** — spec requires only first 30 (seeded order).
- **`fleet serve restart` / `fleet run`** — explicitly forbidden; not executed.

---

## 7. New `results.md` rows (all 7, copied verbatim from `runs/results.md`)

| experiment | chapter | n | metric | secondary | llm_calls | seconds | notes |
|---|---|---|---|---|---|---|---|
| 05_judge_did_not_answer | 05 | 60 | 0.1158 | — | 238 | 9.645 | did_not_answer v1 (best=v1) |
| 05_judge_missing_required_fact | 05 | 60 | 0.0270 | — | 240 | 9.726 | missing_required_fact v2 (best=v2) |
| 05_judge_missing_required_fact_nocontext | 05 | 30 | -0.1538 | — | 30 | 2.686 | |
| 05_judge_overall | 05 | 60 | 0.1549 | — | 0 | 0.0 | |
| 05_judge_unsupported_claim | 05 | 60 | -0.1111 | — | 235 | 9.535 | unsupported_claim v2 (best=v2) |
| 05_judge_wrong_section_retrieved | 05 | 60 | 0.0000 | — | 239 | 9.683 | wrong_section_retrieved v2 (best=v2) |
| 05_likert_overall | 05 | 30 | 0.3600 | — | 30 | 2.386 | |

---

## 8. Key takeaways for the chapter writer

1. **Dev → test generalization failure.** `missing_required_fact` v2 was perfect on dev
   (kappa 1.000) but the second-worst on test (kappa 0.027, TPR 0.133). The 3 dev
   failures were easier than the 15 test failures. This is the single most important
   finding to explain in the chapter.
2. **TPR collapse pattern.** Three of the four modes achieve TPR = 0 on test
   (`unsupported_claim`, `wrong_section_retrieved`, and effectively
   `missing_required_fact`). The judge says "pass" for every true-fail. This is a
   systematic under-calling bias, not random noise — the judge is over-conservative
   when deciding to flag a failure.
3. **Likert AUC below chance.** AUC 0.36 is not just weak — it is *inversely*
   correlated. This should be presented as "the single-score rubric fails in the
   expected way: it cannot separate pass/fail and is weakly misleading."
4. **No-context ablation is a null result.** For `missing_required_fact` the judge
   does not depend on the retrieved text; it relies on the customer question +
   reply text. This is consistent with the judge's failure mode (under-calling)
   — it never cross-references the cited section.
5. **Disagreement direction is asymmetric.** 13 false-negatives vs 5 false-positives
   on `missing_required_fact`. The judges systematically fail to catch omissions,
   which is the most consequential failure type for an RAG answer.

---

## 9. Reproducing

```bash
cd project
# Step 1 — per-mode on test (240 fresh calls)
uv run python -m evals_tutorial.judge run --mode all --version best --split test

# Step 2 — overall (0 fresh, cache hits)
uv run python -m evals_tutorial.judge overall --split test

# Step 3 — likert, first 30 (30 fresh)
uv run python -m evals_tutorial.judge likert --split test --limit 30

# Step 4 — nocontext, same 30 (30 fresh)
uv run python -m evals_tutorial.judge nocontext --mode missing_required_fact --split test --limit 30

# Step 5 — scorecard + results table
uv run python -m evals_tutorial.judge scorecard
uv run python -m evals_tutorial.results build

# Tests
uv run pytest tests/ -q -m "not slow"
```
