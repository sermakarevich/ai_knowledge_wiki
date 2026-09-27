> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix: Training Setup (Hyperparameters and Optimization)
**In one sentence:** The curator is trained with GRPO for up to 100 steps on Qwen3-8B (non-thinking) using a constant-with-warmup learning rate of 1×10⁻⁶, group size 8, and low-variance KL loss (coef 1×10⁻³), with a Qwen3-8B executor served via vLLM retrieving k=3 memories per task.
## Key points
- Base curator policy is Qwen3-8B (non-thinking), trained with GRPO advantage estimator without std normalization.
- Optimization uses learning rate 1×10⁻⁶ with a constant schedule plus 5 warmup steps (0.05 ratio of 100 steps), max 100 RL steps, train batch 32 prompts and policy mini-batch 32.
- KL in reward is disabled; KL loss is enabled with low-variance KL at coefficient 1×10⁻³, clip range (0.2, 0.2), and token-mean loss aggregation.
- Curator rollout uses 8 samples per prompt (group size), max prompt length 32768, and max response length 8192 (ALFWorld) / 4096 (WebShop) at sampling temperature 1.0.
- Executor is Qwen3-8B (non-thinking) served via vLLM at temperature 1.0 / top-p 0.95 / top-k 20, max 4096 new tokens, max 30 env steps per game, 3 retrieved memories per task.
- Retrieval count is insensitive: on WebShop, k=3 vs k=5 changes success rate by <2 points (Qwen3-8B 32.8 vs 32.8, Gemini-2.5-Pro 50.5 vs 48.6, GPT-5.4 45.4 vs 45.3), so k=3 is used for efficiency.
- Consolidated ablations show removing retrieved trajectories from RL-trained JITMEM causes the largest drop (up to −14.8 SR ALFWorld, −15.2 SR WebShop), and removing raw trajectories costs up to −8.2 SR on WebShop.
---
## Optimization hyperparameters
| Hyperparameter | Value |
|---|---|
| Base policy (curator) | Qwen3-8B (non-thinking) |
| Advantage estimator | GRPO (no std. normalization) |
| Learning rate | 1 × 10⁻⁶ |
| LR schedule | constant with warmup |
| Warmup steps | 5 (ratio 0.05 of 100 steps) |
| Train batch size (prompts) | 32 |
| Policy mini-batch size | 32 |
| Max RL steps | 100 |
| KL in reward | disabled |
| KL loss | enabled, low-variance KL, coef. 1 × 10⁻³ |
| Clip range (low, high) | (0.2, 0.2) |
| Loss aggregation | token-mean |

**Covers:** optimization table (curator base policy through loss aggregation)

## Rollout / generation (curator)
| Hyperparameter | Value |
|---|---|
| Samples per prompt (group size) | 8 |
| Max prompt length | 32768 |
| Max response length | 8192 (ALFWorld) / 4096 (WebShop) |
| Sampling temperature (train) | 1.0 |

**Covers:** rollout/generation settings

## Executor / environment
| Hyperparameter | Value |
|---|---|
| Executor model | Qwen3-8B (non-thinking), served via vLLM |
| Executor temperature / top-p / top-k | 1.0 / 0.95 / 20 |
| Executor max new tokens | 4096 |
| Max env. steps per game | 30 |
| Retrieved memories per task | 3 |

**Covers:** executor and environment settings

## Additional results: sensitivity to retrieval count k
Table 8 compares k=3 and k=5 retrieved trajectories on WebShop across all three executors. "Performance is stable across both settings: SR varies by less than 2 points in all cases, and the differences remain within standard deviation for Qwen3-8B and GPT-5.4."

| Executor | k | Score | SR |
|---|---|---|---|
| Qwen3-8B | k=3 | 61.1 ± 0.9 | 32.8 ± 1.7 |
| Qwen3-8B | k=5 | 60.5 ± 0.4 | 32.8 ± 0.3 |
| Gemini-2.5-Pro | k=3 | 61.0 ± 0.8 | 50.5 ± 0.8 |
| Gemini-2.5-Pro | k=5 | 59.2 ± 0.4 | 48.6 ± 0.7 |
| GPT-5.4 | k=3 | 53.8 ± 0.3 | 45.4 ± 0.0 |
| GPT-5.4 | k=5 | 53.4 ± 0.7 | 45.3 ± 0.8 |

"This indicates that JITMEM is not sensitive to the retrieval count, and we use k=3 for all main results for efficiency."

**Covers:** Appendix B, retrieval-count sensitivity (Table 8)

## Additional results: consolidated ablations (Table 9)
"Table 9 collects all ablation and baseline results from the main text into a single table for easy comparison. For each executor, the table first lists baselines, then JITMEM-base ablations, and finally JITMEM ablations." Mean ± std over 3 runs.

JITMEM-base ablations (prompted curator) isolate individual design choices:
- "w/o task adaptivity: removes current task description xt from the curator's input, reducing it to a query-independent summarizer."
- "w/o successful traj. filtering: stores all trajectories with correctness labels instead of filtering to successful ones."
- "w/o raw traj.: applies ReasoningBank-style distillation at write time and stores only the distilled items."

JITMEM ablations (RL-trained curator) probe what RL training learns:
- "w/o retrieved traj.: forces the retriever to return an empty set, isolating parametric knowledge from episodic retrieval."
- "w/o task adaptivity: removes current task description xt from the RL-trained curator."
- "w/ staged bank refresh: rebuilds the training bank with curator-augmented trajectories after 100 GRPO steps and continues training for 50 more."
- "w/ test bank warm-starting: pre-populates the test bank with 100 training-set trajectories to mitigate the cold-start effect."

Key findings (verbatim):
1. "Every design choice contributes. Every JITMEM-base ablation degrades performance, confirming that task-adaptive conditioning, quality-filtered storage, and raw trajectory retention each contribute independently. The largest drop comes from removing raw trajectories on WebShop (up to −8.2 SR), underscoring that write-time distillation discards information the curator needs."
2. "RL learns to distill retrieved experience. Removing retrieved trajectories from the RL-trained JITMEM causes the largest degradation (up to −14.8 SR on ALFWorld and −15.2 SR on WebShop). Removing task adaptivity also degrades substantially, with the gap widening compared to the untrained variant."
3. "Default training and evaluation settings are sufficient. Staged bank refresh provides modest gains (+2.8 SR at best), and test bank warm-starting has negligible effect, suggesting the static training bank and empty-start evaluation already work well."

Selected Table 9 values (Qwen3-8B executor; ALFWorld SR / WebShop Score / WebShop SR):
- No Memory: 47.9 ± 1.2 / 33.3 ± 0.7 / 9.8 ± 0.5; JITMEM-base: 60.5 ± 2.6 / 32.5 ± 3.2 / 11.7 ± 0.5; JITMEM: 77.4 ± 2.9 / 61.1 ± 0.9 / 32.8 ± 1.7
- JITMEM w/o retrieved traj.: 62.6 ± 1.2 / 47.9 ± 1.6 / 17.6 ± 1.1; w/o task adaptivity: 66.0 ± 4.7 / 49.6 ± 1.4 / 22.4 ± 0.4
- JITMEM w/ staged bank refresh: – / 61.7 ± 0.9 / 35.6 ± 0.3; w/ test bank warm-starting: – / 60.9 ± 1.0 / 32.5 ± 1.5

**Covers:** Appendix B, consolidated ablations (Table 9, pp. 20–21)
