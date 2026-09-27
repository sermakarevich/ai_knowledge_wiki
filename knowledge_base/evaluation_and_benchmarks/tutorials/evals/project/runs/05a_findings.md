# Chapter 05 — LLM-as-judge alignment findings (dev half)

## What this is

Per-failure-mode binary judges (replaces the old Likert 1–5 scale). For each
tracked mode we grade the 20-ticket `dev` split by asking the LLM a
single yes/no question ("does this reply commit `<mode>`?"). We aligned the
v1 (zero-shot) and v2 (few-shot) prompts on dev and picked the winner by
Cohen's kappa. This is the **dev half** of task `fleet-5d8oh`; the **test
half** (05b) will run the dev-aligned winner per mode against the sealed set.

## Method details

- **Tracked modes** (≥4 fails in the chapter-03 labels):
  `missing_required_fact`, `unsupported_claim`, `wrong_section_retrieved`,
  `did_not_answer`. `wrong_tone_or_promise` is left untracked (few fails).
- **Ground truth**: chapter-03 human labels (`data/labels/answer_v1.jsonl`).
  `true_fail` = the mode is present in that ticket's `failure_modes`.
  `pred_fail` = the judged reply returned `{"verdict": "fail"}`.
- **Metrics**: TPR (recall), TNR (specificity), accuracy, Cohen's kappa,
  and AUC (ranked by how strongly the model leans fail). Chosen version per
  mode = higher dev kappa.
- **No-context run** (a separate `nocontext` flag, not part of this run):
  grades the *retrieved context itself* — see 05b.

## Results on dev (20 tickets)

| mode | version | TPR | TNR | acc | kappa | chosen |
|---|---|---|---|---|---|---|
| did_not_answer | v1 | 1.000 | 0.947 | 0.950 | 0.643 | **v1** |
| did_not_answer | v2 | 1.000 | 0.895 | 0.900 | 0.459 | |
| missing_required_fact | v1 | 0.333 | 1.000 | 0.900 | 0.459 | |
| missing_required_fact | v2 | 1.000 | 1.000 | 1.000 | 1.000 | **v2** |
| unsupported_claim | v1 | 1.000 | 0.947 | 0.950 | 0.643 | |
| unsupported_claim | v2 | 1.000 | 0.947 | 0.950 | 0.643 | **v2** |
| wrong_section_retrieved | v1 | (0/0) | 1.000 | 1.000 | 1.000 | |
| wrong_section_retrieved | v2 | (0/0) | 1.000 | 1.000 | 1.000 | **v2** |

Chosen per mode: **v1 for `did_not_answer`**, **v2 for the other three**.

## Observations

- **`missing_required_fact` v2 is perfect on dev** (kappa 1.000, zero
  disagreements). v1 badly under-calls (TPR 0.333 — it only catches 1 of the
  3 truly-failing replies), i.e. a zero-shot judge that leans "pass" misses
  omissions. The few-shot examples fix this. This is the clearest win for
  going v2.
- **`did_not_answer` regresses with v2** (kappa 0.459 vs 0.643): the
  few-shot version adds a false positive on a passing ticket (TNR 0.895 vs
  0.947). One dev ticket. v1 is the safer pick here — fewer fails to catch
  (1 dev fail) means the positives are noise-sensitive.
- **`unsupported_claim` v1 and v2 tie** on dev (kappa 0.643 both). We pick v2
  by the tie-break (it never disagrees more than v1), but treat this mode as
  "version-agnostic on dev" — the sealed test split is what will separate them.
- **`wrong_section_retrieved` has 0 dev fails.** TPR is a 0/0 (degenerate →
  reported 0.000) and both versions are kappa 1.000 because every dev ticket
  is a true-pass. **This mode is not actually validated on dev** — the whole
  judgment there is "no failures to find." It will only be testable on the
  sealed split. (The 8 total fails live in the test split.)
- **Overall**: the binary per-mode judges are clearly more discriminative
  than a single Likert scale would be — each runs a focused question and we
  can see per-mode TPR/TNR instead of one blurred score.

## What 05b (test half) still needs

- Run the **dev-aligned winner per mode** on the sealed `test` split for the
  two answer runs (`answer_v1`, `answer_v2`) → `runs/05_test/`.
- The **no-context** grading of the `answer_v2` retrieved-context quality on
  both splits → `runs/05_noc/`.
- Emit the final scorecard `runs/05_judge_scorecard.md` plus the
  `metrics.json` for `results.md`, then close task `fleet-5d8oh`.

## Reproducing

```
cd project
uv run python -m evals_tutorial.judge align --split dev      # writes 05_judge_align/<mode>.json
uv run python -m evals_tutorial.judge_dev_report             # writes 05_align_dev.md + 05_dev/*.jsonl
```

Artifacts: `runs/05_judge_align/<mode>.json` (full alignment record),
`runs/05_align_dev.md` (this scorecard), `runs/05_dev/<mode>_<version>.jsonl`
(per-ticket predictions, 20 rows each, dev split only).
