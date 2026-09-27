# Chapter 05 — judge scorecard

## Dev alignment (v1 vs v2, chosen = higher kappa) — from 05a
| mode | version | tpr | tnr | accuracy | kappa | chosen |
|---|---|---|---|---|---|---|
| did_not_answer | v1 | 1.000 | 0.947 | 0.950 | 0.643 | <- |
| did_not_answer | v2 | 1.000 | 0.895 | 0.900 | 0.459 |  |
| missing_required_fact | v1 | 0.333 | 1.000 | 0.900 | 0.459 |  |
| missing_required_fact | v2 | 1.000 | 1.000 | 1.000 | 1.000 | <- |
| unsupported_claim | v1 | 1.000 | 0.947 | 0.950 | 0.643 |  |
| unsupported_claim | v2 | 1.000 | 0.947 | 0.950 | 0.643 | <- |
| wrong_section_retrieved | v1 | 0.000 | 1.000 | 1.000 | 1.000 |  |
| wrong_section_retrieved | v2 | 0.000 | 1.000 | 1.000 | 1.000 | <- |

## Test (chosen version + ablations)
| experiment | mode | n | kappa | tpr | tnr | llm_calls | notes |
|---|---|---|---|---|---|---|---|
| 05_judge_did_not_answer | did_not_answer | 60 | 0.116 | 0.400 | 0.800 | 238 | did_not_answer v1 (best=v1) | 
| 05_judge_missing_required_fact | missing_required_fact | 60 | 0.027 | 0.133 | 0.889 | 240 | missing_required_fact v2 (best=v2) | 
| 05_judge_wrong_section_retrieved | wrong_section_retrieved | 60 | 0.000 | 0.000 | 1.000 | 239 | wrong_section_retrieved v2 (best=v2) | 
| 05_judge_unsupported_claim | unsupported_claim | 60 | -0.111 | 0.000 | 0.917 | 235 | unsupported_claim v2 (best=v2) | 
| 05_judge_overall | overall | 60 | 0.155 | 0.385 | 0.765 | 0 |  | 
| 05_likert_overall | overall | 30 | 0.360 | — | — | 30 |  | 
| 05_judge_missing_required_fact_nocontext | missing_required_fact | 30 | -0.154 | 0.000 | 0.875 | 30 |  | 
