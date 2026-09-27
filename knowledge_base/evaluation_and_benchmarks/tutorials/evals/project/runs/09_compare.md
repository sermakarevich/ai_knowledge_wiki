Cross-method comparison for ch-09.

Per-method headline metric from `runs/<experiment>/metrics.json`:

| Method | Headline AUROC (or primary) | n (rows) |
|---|---|---|
| HHEM (vectara) | AUROC=0.7581  (400 rows, 0.071s/item) | 400 |
| LettuceDetect | AUROC=0.7681  (400 rows, 0.139s/item) | 400 |
| NLI cross-encoder | AUROC=0.4835  (400 rows, 0.942s/item) | 400 |
| SelfCheckGPT | AUROC=0.412  (42 rows, 3.14s/item) | 42 |
| qwen3.8:27b judge | f1=0.7692  (70 rows, 1.765s/item) | 70 |

Pairwise binary agreement at 0.5 score threshold (all methods share the RAGTruth test rows):

| | HHEM (vectara) | LettuceDetect | NLI cross-encoder | SelfCheckGPT | qwen3.8:27b judge |
|---|---|---|---|---|---|
| HHEM (vectara) | — | 0.730 | 0.385 | 0.357 | 0.586 |
| LettuceDetect | 0.730 | — | 0.255 | 0.238 | 0.829 |
| NLI cross-encoder | 0.385 | 0.255 | — | 0.976 | 0.300 |
| SelfCheckGPT | 0.357 | 0.238 | 0.976 | — | 0.400 |
| qwen3.8:27b judge | 0.586 | 0.829 | 0.300 | 0.400 | — |

Shared rows across all 5 methods: 400 (RAGTruth test set: 240 QA + 160 Summary).  The SelfCheckGPT and LLM-judge methods only cover a subset (windows within these 400), so their pairwise cells above use the smaller overlap.

Notes on score scale: HHEM / Lettuce / NLI / SelfCheckGPT are continuous [0,1] (higher = more hallucinated).  The LLM judge is discrete {0, 1}.  Pairwise agreement is therefore computed at the 0.5 threshold for the continuous methods, which is a fair midpoint.

