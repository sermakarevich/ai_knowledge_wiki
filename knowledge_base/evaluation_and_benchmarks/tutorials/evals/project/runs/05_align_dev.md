# Chapter 05a — dev-split judge alignment scorecard

Aligned the v1 (zero-shot) and v2 (few-shot) binary judge of each tracked mode against the
chapter-03 human labels on the `dev` split (20 tickets). Chosen version per mode = higher
Cohen's kappa on dev. Predictions: `runs/05_dev/<mode>_<version>.jsonl`.

| mode | version | TPR | TNR | acc | kappa | chosen |
|---|---|---|---|---|---|---|
| did_not_answer | v1 <- | 1.000 | 0.947 | 0.950 | 0.643 | v1 |
| did_not_answer | v2 | 1.000 | 0.895 | 0.900 | 0.459 |  |
| missing_required_fact | v1 | 0.333 | 1.000 | 0.900 | 0.459 |  |
| missing_required_fact | v2 <- | 1.000 | 1.000 | 1.000 | 1.000 | v2 |
| unsupported_claim | v1 | 1.000 | 0.947 | 0.950 | 0.643 |  |
| unsupported_claim | v2 <- | 1.000 | 0.947 | 0.950 | 0.643 | v2 |
| wrong_section_retrieved | v1 | 0.000 | 1.000 | 1.000 | 1.000 |  |
| wrong_section_retrieved | v2 <- | 0.000 | 1.000 | 1.000 | 1.000 | v2 |
