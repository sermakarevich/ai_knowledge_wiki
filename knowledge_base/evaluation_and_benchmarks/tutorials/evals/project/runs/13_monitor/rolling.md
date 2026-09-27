# Online monitor — chapter 13b

run `answer_v1`: 80 traces pooled over 7 seeded days, sample=20%/day, HHEM threshold=0.3 + one cheap check (max 150 words).
Pooled sampled pass: **0.009** (95% CI [0.000, 0.026]).
Alert rule: day pass rate below the pooled 95% CI lower bound → flagged.

| day | n | pass | rate ±CI | alert |
|---|---|---|---|---|
| 1 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 2 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 3 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 4 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 5 | 16 | 1 | 0.062 [0.000,0.181] |  |
| 6 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 7 | 16 | 0 | 0.000 [0.000,0.000] |  |
