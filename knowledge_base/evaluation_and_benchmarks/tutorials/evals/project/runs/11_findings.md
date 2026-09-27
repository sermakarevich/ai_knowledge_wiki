# Chapter 11 findings — model benchmarks via lm-evaluation-harness (Ollama)

All numbers below are `n=50` items, `seed=0`, `temperature=0`, through
`lm_eval` `local-chat-completions` against Ollama (`http://127.0.0.1:11435`).
CIs are our bootstrap 95% (10k resamples, `evals_tutorial.stats`) over the
per-sample 0/1 correctness from the harness `samples_*.jsonl`;
"harness stderr" is the harness's own normal-approx SE for comparison.

**lm-evaluation-harness version: 0.4.13** (installed via `lm-eval[api,ifeval]>=0.4.11`).

## 1. Main score table — 3 models × 2 tasks

| model (params) | task | primary metric | score | our bootstrap 95% CI | harness stderr | seconds |
|---|---|---|---|---|---|---|
| **qwen3.8:27b** (27.3B) | gsm8k (5-shot) | exact_match (flexible-extract) | **0.46** | [0.32, 0.60] | 0.0712 | 368.8 |
| qwen3.8:27b | ifeval | prompt_level_strict_acc | **0.82** | [0.72, 0.92] | 0.0549 | 429.1 |
| **gemma4:latest** (8.0B) | gsm8k (5-shot) | exact_match (flexible-extract) | **0.06** | [0.00, 0.14] | 0.0339 | 110.4 |
| gemma4:latest | ifeval | prompt_level_strict_acc | **0.74** | [0.62, 0.86] | 0.0627 | 258.8 |
| **tiny-qwen35-110m-sft** (108.6M) | gsm8k (5-shot) | exact_match (flexible-extract) | **0.00** | [0.00, 0.00] | 0.0 | 23.2 |
| tiny-qwen35-110m-sft | ifeval | prompt_level_strict_acc | **0.14** | [0.06, 0.24] | 0.0496 | 38.6 |

Reading:
- **The tiny 110M model is ≈0 on both tasks — that is the point.** It has
  essentially no multi-step arithmetic and weak instruction-following. It
  still gets some IFEval credit because "answer in 1 sentence / all-caps / no
  bullet points" style constraints are trivial for a small LM to satisfy even
  without understanding the content.
- **qwen3.8:27b** is the only model that solves ~half of the GSM8K problems
  (0.46 on 5-shot) and clears IFEval (0.82). Its gsm8k 95% CI ([0.32,0.60])
  is wide — n=50 is small, so treat 0.46 as "roughly 0.3–0.6", not a precise
  46%.
- **gemma4:latest (8B)** is the interesting contrast: **IFEval 0.74 vs GSM8K
  0.06**. It follows *format* instructions well but barely does *arithmetic*.
  IFEval is a formatting/verifiability task; GSM8K is a reasoning task. The
  same model scores 12× higher on the task that leans more on following
  surface form. This is the concrete "the task, not just the model, drives
  the number" message for the chapter.

**Caveat on n.** `--limit 50` caps the *questions* to 50; the harness's
gsm8k logs one sample row **per question per filter** (it reports both
`strict-match` and `flexible-extract`). We score exactly the
`flexible-extract` rows (the task's primary metric), so every reported
`n=50` is 50 distinct questions — not 100 rows. The collector filters by
the primary filter before bootstrapping; otherwise the CI would be
contaminated by the second-filter duplicates.

## 2. Prompt-sensitivity table — qwen3.8:27b only, gsm8k, same 50 questions

| variant | score | our bootstrap 95% CI | scored by | note |
|---|---|---|---|---|
| 0-shot (harness template, 0 fewshot) | **0.46** | [0.32, 0.60] | lm-eval flexible-extract | `--num_fewshot 0` |
| 5-shot (harness template, default 5) | **0.46** | [0.32, 0.60] | lm-eval flexible-extract | same 5 fewshots as §1 |
| CoT (`gsm8k_cot`, chain-of-thought template) | **0.52** | [0.38, 0.66] | lm-eval flexible-extract | different Q:/A: template + CoT fewshots |
| **plain** (our `gsm8k_plain_v1.txt`, lenient regex, cached client) | **0.96** | [0.90, 1.00] | our extractor | single-shot custom prompt |

**score_range = 0.96 − 0.46 = 0.50** (max − min across variants).

### Paired bootstrap deltas (same questions, `stats.paired_bootstrap`)

| pair | mean_a | mean_b | diff (a−b) | 95% CI on diff | p |
|---|---|---|---|---|---|
| 0-shot vs 5-shot | 0.46 | 0.46 | 0.00 | [−0.08, +0.08] | 1.00 |
| 0-shot vs CoT | 0.46 | 0.52 | −0.06 | [−0.18, +0.06] | 0.37 |
| 0-shot vs plain | 0.46 | 0.96 | −0.50 | [−0.64, −0.36] | **0.001** |
| 5-shot vs CoT | 0.46 | 0.52 | −0.06 | [−0.18, +0.04] | 0.37 |
| 5-shot vs plain | 0.46 | 0.96 | −0.50 | [−0.64, −0.36] | **0.001** |
| CoT vs plain | 0.52 | 0.96 | −0.44 | [−0.56, −0.30] | **0.001** |

### Flips between variants

- **0-shot vs 5-shot:** 4/50 flip
- **0-shot vs CoT:** 9/50 flip
- **0-shot vs plain:** 25/50 flip
- **5-shot vs CoT:** 9/50 flip
- **5-shot vs plain:** 25/50 flip
- **CoT vs plain:** 22/50 flip
- **n_flips any variant:** **29** of 50 questions get a different 0/1 verdict
  depending on which prompt/extractor is used.

### One question that flips (house-flipping arithmetic)

> "Josh decides to try flipping a house. He buys a house for $80,000 and then
> puts in $50,000 in repairs. This increased the value of the house by 150%.
> How much profit did he make?"  (gold = **70000**)

| variant | verdict | extracted value |
|---|---|---|
| 0-shot | ✗ | `80000` (repeats the buy price, not the profit) |
| 5-shot | ✗ | `null` (no number the extractor accepted) |
| CoT | ✗ | `800` (arithmetic slip) |
| plain | ✓ | `70000` (correct) |

The same model gives a correct *and* three different wrong answers on the
same question depending on the prompt — a clean illustration that the
**scoring surface** (template + extractor), not just the weights, determines
the reported score. The plain prompt + lenient regex is what lets the model's
intended final number survive extraction.

## 3. Thinking tokens & extraction failures

- **No `<thinking>`/reasoning-token blocks** were emitted by any model in a
  way that broke the harness's `flexible-extract` regex. Qwen internally
  shows scratch arithmetic (`<<5*0.60=3>>3`-style) inside its chain, but the
  harness still isolates the final `#### <number>` answer line. This is the
  known "thinking-token extraction" fragility; here the harness's
  `#### <answer>` convention absorbed it.
- **Extraction failures (5-shot qwen):** 6/50 rows had no parseable final
  number (`extracted=None`) — the model answered in prose without a clean
  terminal number. 0-shot: 5/50. These count as incorrect, which is why the
  0-shot and 5-shot scores are *lower bounds* (extraction drops hide
  some-correct-in-prose answers). The **plain** variant had **0** extraction
  failures — its lenient "last number in the reply" regex always found
  something, which is a large part of why it scores 0.96.
- **CoT 5-shot** had a couple of arithmetic slips (e.g. the Josh example
  above) where the model reasoned but mis-computed, not an extraction issue.

## 4. What was skipped / not run (per spec)

- **GSM1k / LiveCodeBench / LiveBench / HLE / GPQA Diamond / τ²-bench /
  SWE-bench Verified** — contamination-resistant & frontier benchmarks
  (see `11_notes.md` §1–§2). Literature only; not executed.
- **No more than 3 models, no more than 2 tasks, `--limit 50` fixed** — per
  the spec's scope & call budget (≤ ~550 calls). We used 300 (6 harness runs
  × 50) + 50 plain + 100 sensitivity-variant ≈ 450 LLM calls (harness runs
  plus the plain/sensitivity variants), within the budget.
- **No Inspect AI** — that is chapter 12.
- **GSM1k contamination run** — cited in `11_notes.md`, not computed here.

## 5. Bottom line for the chapter

1. **Model size dominates** on reasoning tasks (gsm8k): 110M→0.00, 8B→0.06,
   27B→0.46. On a *format*-heavy task (IFEval) even the 8B model scores
   respectably (0.74), and the 110M one gets partial credit (0.14) — task
   and model interact.
2. **Prompt / few-shot / extractor move the score by half a point** for the
   *same* model on the *same* 50 questions (0shot/5shot/CoT cluster at
   0.46–0.52; a plain custom prompt + lenient regex hits 0.96). 29/50
   questions flip verdict across variants.
3. **Every number needs an error bar** (Miller 2024): with n=50 the CIs are
   wide — that is the statistical lesson, and exactly why we report
   bootstrap CIs + paired bootstrap rather than point estimates.
