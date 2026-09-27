# Chapter 12 — Inspect-AI re-run of chapters 05 and 11

Both run in Inspect-AI on the **cached Ollama client** (0 fresh LLM calls),
with the **same** prompt files, labels and scorer composition as the chapter
baselines — so the only variable is the harness around the model.

## 1) helpdesk (chapter 05)

| metric | chapter 05 | Inspect | agree? |
|---|---|---|---|
| pass_rate (primary) | — | **0.7000** | — |
| accuracy | 0.6000 | **0.6000** | yes |
| kappa (positive=fail) | **0.1549** | **0.1549** | yes |
| code_checks mean | — | 0.8194 | — |
| includes hit rate | — | 0.0000 | — |

Per-item (chapter 05 `pred_pass` vs Inspect `judge_grade` verdict):

| ticket | ch-05 pred | Inspect pred | agree? | ch-05 failed | Inspect failed |
|---|---|---|---|---|---|
| tkt-003 | yes | yes | yes | — | — |
| tkt-004 | yes | yes | yes | — | — |
| tkt-005 | yes | yes | yes | — | — |
| tkt-006 | yes | yes | yes | — | — |
| tkt-007 | yes | yes | yes | — | — |
| tkt-010 | no | no | yes | did_not_answer, missing_required_fact | did_not_answer, missing_required_fact |
| tkt-011 | no | no | yes | did_not_answer, missing_required_fact | did_not_answer, missing_required_fact |
| tkt-012 | no | no | yes | did_not_answer | did_not_answer |
| tkt-013 | no | no | yes | did_not_answer | did_not_answer |
| tkt-014 | yes | yes | yes | — | — |
| tkt-017 | yes | yes | yes | — | — |
| tkt-018 | yes | yes | yes | — | — |
| tkt-019 | yes | yes | yes | — | — |
| tkt-020 | yes | yes | yes | — | — |
| tkt-021 | yes | yes | yes | — | — |
| tkt-024 | no | no | yes | unsupported_claim | unsupported_claim |
| tkt-025 | yes | yes | yes | — | — |
| tkt-026 | yes | yes | yes | — | — |
| tkt-027 | yes | yes | yes | — | — |
| tkt-028 | yes | yes | yes | — | — |
| tkt-031 | yes | yes | yes | — | — |
| tkt-032 | yes | yes | yes | — | — |
| tkt-033 | yes | yes | yes | — | — |
| tkt-034 | yes | yes | yes | — | — |
| tkt-035 | yes | yes | yes | — | — |
| tkt-038 | no | no | yes | did_not_answer | did_not_answer |
| tkt-039 | yes | yes | yes | — | — |
| tkt-040 | no | no | yes | did_not_answer | did_not_answer |
| tkt-041 | yes | yes | yes | — | — |
| tkt-042 | no | no | yes | unsupported_claim | unsupported_claim |
| tkt-045 | no | no | yes | missing_required_fact | missing_required_fact |
| tkt-046 | yes | yes | yes | — | — |
| tkt-047 | yes | yes | yes | — | — |
| tkt-048 | yes | yes | yes | — | — |
| tkt-049 | yes | yes | yes | — | — |
| tkt-052 | yes | yes | yes | — | — |
| tkt-053 | yes | yes | yes | — | — |
| tkt-054 | no | no | yes | did_not_answer, missing_required_fact | did_not_answer, missing_required_fact |
| tkt-055 | no | no | yes | did_not_answer | did_not_answer |
| tkt-056 | yes | yes | yes | — | — |
| tkt-058 | yes | yes | yes | — | — |
| tkt-059 | no | no | yes | did_not_answer | did_not_answer |
| tkt-060 | yes | yes | yes | — | — |
| tkt-061 | yes | yes | yes | — | — |
| tkt-062 | yes | yes | yes | — | — |
| tkt-064 | no | no | yes | unsupported_claim | unsupported_claim |
| tkt-065 | yes | yes | yes | — | — |
| tkt-066 | no | no | yes | did_not_answer, missing_required_fact | did_not_answer, missing_required_fact |
| tkt-067 | no | no | yes | did_not_answer, missing_required_fact | did_not_answer, missing_required_fact |
| tkt-068 | yes | yes | yes | — | — |
| tkt-070 | no | no | yes | did_not_answer | did_not_answer |
| tkt-071 | yes | yes | yes | — | — |
| tkt-072 | yes | yes | yes | — | — |
| tkt-073 | yes | yes | yes | — | — |
| tkt-074 | no | no | yes | did_not_answer, missing_required_fact | did_not_answer, missing_required_fact |
| tkt-076 | yes | yes | yes | — | — |
| tkt-077 | no | no | yes | unsupported_claim | unsupported_claim |
| tkt-078 | yes | yes | yes | — | — |
| tkt-079 | yes | yes | yes | — | — |
| tkt-080 | yes | yes | yes | — | — |

Disagreements: **0** / 60.

### 1.1) Interpretation

- Inspect's primary `pass_rate` = `0.7000` (mean of per-ticket judge pass verdicts; ch-05 recorded accuracy/kappa instead).
- Inspect's `judge_grade` accuracy = `0.6000` vs ch-05 accuracy = `0.6000`.
- Inspect kappa (positive=fail) = `0.1549` vs ch-05 kappa = `0.1549`.
- `code_checks_mean` = mean of ch-10's 6 deterministic checks (auxiliary).
- `includes_hit_rate` = fraction where any ch-05 gold answer point appears (expected to be low: replies paraphrase).

## 2) gsm8k (chapter 11)

| metric | chapter 11 | Inspect | agree? |
|---|---|---|---|
| accuracy | 0.9600 | **0.9600** | yes |

Per-item (chapter 11 `correct` vs Inspect `match(location='end')`):

| doc_id | ch-11 | gold | Inspect | agree? |
|---|---|---|---|---|
| 0 | yes | 18 | yes | yes |
| 1 | yes | 3 | yes | yes |
| 10 | yes | 366 | yes | yes |
| 11 | yes | 694 | yes | yes |
| 12 | no | 13 | no | yes |
| 13 | yes | 18 | yes | yes |
| 14 | yes | 60 | yes | yes |
| 15 | yes | 125 | yes | yes |
| 16 | yes | 230 | yes | yes |
| 17 | yes | 57500 | yes | yes |
| 18 | yes | 7 | yes | yes |
| 19 | yes | 6 | yes | yes |
| 2 | yes | 70000 | yes | yes |
| 20 | yes | 15 | yes | yes |
| 21 | yes | 14 | yes | yes |
| 22 | yes | 7 | yes | yes |
| 23 | yes | 8 | yes | yes |
| 24 | yes | 26 | yes | yes |
| 25 | yes | 2 | yes | yes |
| 26 | yes | 243 | yes | yes |
| 27 | yes | 16 | yes | yes |
| 28 | yes | 25 | yes | yes |
| 29 | yes | 104 | yes | yes |
| 3 | yes | 540 | yes | yes |
| 30 | yes | 109 | yes | yes |
| 31 | yes | 80 | yes | yes |
| 32 | yes | 35 | yes | yes |
| 33 | yes | 70 | yes | yes |
| 34 | yes | 23 | yes | yes |
| 35 | yes | 9 | yes | yes |
| 36 | yes | 75 | yes | yes |
| 37 | yes | 2 | yes | yes |
| 38 | yes | 10 | yes | yes |
| 39 | yes | 18 | yes | yes |
| 4 | yes | 20 | yes | yes |
| 40 | yes | 8 | yes | yes |
| 41 | yes | 200 | yes | yes |
| 42 | yes | 26 | yes | yes |
| 43 | yes | 48 | yes | yes |
| 44 | yes | 20 | yes | yes |
| 45 | no | 104 | no | yes |
| 46 | yes | 163 | yes | yes |
| 47 | yes | 800 | yes | yes |
| 48 | yes | 8 | yes | yes |
| 49 | yes | 30 | yes | yes |
| 5 | yes | 64 | yes | yes |
| 6 | yes | 260 | yes | yes |
| 7 | yes | 160 | yes | yes |
| 8 | yes | 45 | yes | yes |
| 9 | yes | 460 | yes | yes |

Disagreements: **0** / 50.

### 2.1) Interpretation

- Both use the **same plain-prompt file** and the **same 50 questions**.
- Scorer difference: ch-11's harness extracts the last `#### N` line; Inspect's `match(location='end', numeric=True)` pulls the last parseable number.
