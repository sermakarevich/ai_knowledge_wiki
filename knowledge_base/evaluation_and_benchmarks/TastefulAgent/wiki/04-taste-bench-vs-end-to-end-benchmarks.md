> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Taste-Bench Average vs End-to-End Benchmarks
**In one sentence:** Taste-Bench Average is useful only when it is not a restatement of end-to-end ability, and the chunk argues it passes this test because it is only partly correlated with SWE-bench Verified while separating top models that SWE-bench compresses, then shows taste can be distilled into Qwen3.6-27B to improve unseen-task judgment and end-to-end success.
## Key points
- Comparison uses each model's Taste-Bench Average against its public SWE-bench Verified score from the Vals AI leaderboard under one shared harness, with 11 models remaining after excluding 3 models unparsable on more than 9% of presentations.
- Pearson correlation between Average and SWE-bench Verified is r = +0.63, so SWE-bench Verified explains R² = 0.39 of variance between models; on the engineering subset mined from SWE-bench Pro tasks the correlation is only r = +0.37.
- The four highest models on SWE-bench Verified sit within 4.0 points of each other there but 10.7 points apart on Taste-Bench Average, showing Taste-Bench separates models at the top of SWE-bench.
- Distillation uses Qwen3.6-27B as base with LoRA-adapter updates, training on 390 engineering questions split into two task-disjoint folds so no student sees the source task of any evaluation question.
- Recipe distills reasoning rather than fitting binary labels: a privileged teacher seeing question plus supported-candidate description generates reasoning, and the student seeing only task, trajectory prefix, and two shuffled candidates is aligned via SDPO-style token-level distillation with forward KL over reasoning tokens and final choice, computed on teacher-sampled continuations.
- On the held-out fold the student reaches 47.9% accuracy vs 30.0% for the base model under the Section 3.4 protocol, with mean accuracy over two orders rising from 42.7% to 62.4% (+17.9 percentage points); on the training fold single-order accuracy rises from 48.6% to 92.9%.
- On 41 held-out SWE-bench Pro tasks with a fixed Qwen3.6-27B executor, success rises from 14.6% (no advice) to 39.0% (correct advice, +24.4 pp upper bound) and to 33.7% with student advice (+19.1 pp).
---
## Taste-Bench Average against SWE-bench Verified
**Covers:** comparison of Taste-Bench rankings with end-to-end benchmarks (Figure 5)

The chunk states the Average "is useful only when it is not a restatement of end-to-end ability" and tests this by comparing each model's Average with its public SWE-bench Verified score [10, 29] taken from the Vals AI leaderboard [30], which "reports every model of Figure 3 under one shared harness."

Three models whose responses are unparsable on more than 9% of presentations are excluded, leaving 11 models. Figure 5 plots Taste-Bench against SWE-bench Verified with one point per model and a least-squares dashed fit; red points deviate most and a band marks the four highest SWE-bench Verified scores.

| Measure | Value |
|---|---|
| Models in comparison | 11 (after excluding 3 with >9% unparsable) |
| Pearson r, Average vs SWE-bench Verified | +0.63 |
| Variance explained (R²) | 0.39 |
| Pearson r on engineering subset (mined from SWE-bench Pro, closest comparison) | +0.37 |
| Spread of top-4 SWE-bench models on SWE-bench Verified | within 4.0 points |
| Spread of same four models on Taste-Bench Average | 10.7 points apart (Appendix D.2) |

## Generalizing taste through distillation
**Covers:** Section 5 opening and Figure 6 overview

> "The results above show that current models judge these forks poorly. We therefore ask whether we can also train taste from the trajectories that measure it."

Each Section 3 question already contains supervision: two candidate directions plus the outcome determining the supported candidate. The section distills this judgment into model weights and tests transfer to unseen tasks and end-to-end success (Figure 6). Base model throughout is Qwen3.6-27B with LoRA adapters [31].

Figure 6 contrasts distilling an advisor (privileged teacher context vs query-plus-options student, fine-tune via distillation) with advisor-guided execution (student judgment written as advice into task context; fixed executor agent completes task independently toward solution, with gold action/observe labels).

## Distillation recipe
**Covers:** Section 5.1

- Task-disjoint folds: 390 engineering questions split into two task-disjoint folds; each student trains on one fold and is evaluated on the other.
- Distilling reasoning instead of fitting labels: a single binary label per question would lead to memorization, so the recipe distills complete reasoning sequences from a privileged teacher.
- Teacher and student are the same frozen base model with different contexts: teacher sees question plus demonstration/short description of supported candidate and reliably selects it; student sees only what the benchmark shows (task, trajectory prefix, two shuffled candidates).
- Loss is SDPO-style token-level distillation with forward KL [32] over reasoning tokens and final choice, computed on teacher-sampled continuations; Appendix G.1 explains the choice and leakage control.

## Transfer to unseen tasks
**Covers:** Section 5.2 and Figure 7 (left)

Training-fold single-order accuracy rises from 48.6% to 92.9%, but task-disjoint evaluation separates learning from memorization. On the held-out fold under Section 3.4 protocol:

| Setting | Accuracy |
|---|---|
| Base model | 30.0% |
| Distilled student | 47.9% |
| Mean over two orders, base | 42.7% |
| Mean over two orders, student | 62.4% |
| Gain | +17.9 percentage points |
| Reference: GPT-5.6 Sol on same questions | 56.9% |

Figure 7 whiskers are 95% item-bootstrap intervals; dashed line marks GPT-5.6 Sol accuracy. Appendix G.3 places the student in the Figure 3 engineering ranking and gives the two-order combination rule used in Section 5.3.

## End-to-end evaluation
**Covers:** Section 5.3 and Figure 7 (right)

For each held-out task, the judgment at each fork is written as one advice note (situation, candidate to avoid, candidate to take); forks were mined from earlier runs so advice is available before the new run, and a fixed Qwen3.6-27B executor completes the task independently. Three settings on the same 41 held-out SWE-bench Pro tasks:

| Setting | Executor success rate |
|---|---|
| No advice | 14.6% |
| Correct advice (every fork correct; upper bound) | 39.0% (+24.4 pp) |
| Student advice | 33.7% (+19.1 pp over no advice) |

Success is measured with the official SWE-bench Pro evaluation; Appendix H gives executor configuration and advice format. The 41 tasks are unseen during training.

> Finding 4
>
> "Taste can be distilled, and better judgment produces gains in task success. The student makes better judgments on unseen tasks, and its advice raises the executor's success rate from 14.6% to 33.7%."
