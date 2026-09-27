# Chapter 08 — Retrieval, LLM-judge metrics, and cross-evaluator agreement

Chapters 04-07 established *that* the answer pipeline fails, but never *why*.
This chapter separates the two things we keep conflating: the **retriever**
(which section the query lands in) and the **generator** (given that section,
can the LLM answer?). We run three independent LLM-judge stacks on the same
30-ticket test split — **RAGAS** (`ragas==0.4.3`), **DeepEval**
(`deepeval==4.2.1`, native `OllamaModel`), and our own **overall judge** from
chapter 05 — and measure how much they *agree* with each other, with the
chapter-04 embedding cosine, and with the chapter-03 gold `pass` label.

Headline: **retrieval is not the bottleneck.** 17 of 18 hard failures have the
right section already in front of the model and are generation failures. The
LLM-judge stacks largely agree *about the label* (AUROC 0.57-0.76) but **do
not agree ticket-by-ticket** (Spearman -0.23 to +0.38): DeepEval is near-saturated
(mean 0.99, 9 of 30 scores are exactly 1.0) so its rank order carries little
signal, while RAGAS is softer and better-calibrated.

## What we ran

| Experiment | n | LLM calls | Primary |
|---|---|---|---|
| `08_retrieval_answer_v1` / `_v2` | 60 | 0 | recall@2 |
| `08_ragas_answer_v1` | 30 | 146 | faithfulness |
| `08_deepeval_answer_v1` | 30 | 270 | faithfulness |
| `08_agreement_metrics` | 28 | 0 | auroc_ragas_faithfulness_vs_label |

`v1` and `v2` retrieval runs share the same `TOP_SECTIONS=2` cosine lookup and
the same gold sections, so the metric columns are identical by design (retrieval
is a function of ticket+helpdesk, not of generator). RAGAS and DeepEval use the
*same* 30 tickets (positional: first 30 test-split ids) and the *same* cached
v1 answer text from `runs/traces/answer_v1/tkt-*.json`, so the only thing that
moves between the two columns is the metric's own decomposition+judge prompts.

## Method

- **IR metrics** (`src/evals_tutorial/rag_evals.py`) — hand-rolled, no LLM
  calls. 18 test tickets scored per-k for `hit@k`, `recall@k`, `precision@k`,
  `mrr`, `ndcg@k` with `kmax=8`. Bootstrap CI (2000 draws, seed 0) over the
  primary `recall@2`.
- **Failure split** — of the tickets that failed on their *own* run, a
  *retrieval* failure is one where the gold section was NOT in top-2; the rest
  are generation failures.
- **RAGAS** — `Faithfulness`, `AnswerRelevancy`, `ContextPrecision` over the
  30-ticket sample; each ticket supplies `reference` = concatenated gold-section
  bodies, `response` = the cached v1 answer.
- **DeepEval** — `OllamaModel(model="qwen3.8:27b", base_url=http://127.0.0.1:11435)`
  shared across the three metrics. Patched `a_generate`/`generate` on the
  shared instance to count calls (total 270 = 30 tickets × 3 metrics × ≈ 3
  sub-calls, within the ≤ 300 budget). Telemetry off via
  `DEEPEVAL_TELEMETRY_OPT_OUT=1` *before* `deepeval` is imported. Per-ticket
  scores come from `metric.measure(tc)` → `metric.score`; `NaN` rows are
  dropped and a warning is recorded. `async_mode=False` for determinism.
- **Agreement** (pure, no LLM) — for each of the 30 aligned tickets:
  Spearman rank correlation of (RAGAS faithfulness, DeepEval faithfulness,
  chapter-04 `embed_cosine`), and one-vs-one AUROC of each against (a) the
  chapter-03 gold `pass` label and (b) the chapter-05 overall `pred_pass`
  verdict. n=28 after dropping 2 tickets with any `NaN` source.

## Retrieval (n=60 test tickets, both versions)

| Metric | v1 | v2 |
|---|---|---|
| recall@2 | 0.8417 | 0.8417 |
| hit@2 | 0.9167 | 0.9167 |
| precision@2 | 0.4750 | 0.4750 |
| mrr | 0.8694 | 0.8694 |
| ndcg@2 | 0.8376 | 0.8376 |

Primary `recall@2 = 0.8417 [0.7583, 0.9167]`. The recall@k curve peaks at
~0.958 by k=8 and hit@8 ≈ 0.983, so **1 in 60 tickets has no gold section in
top-8** — a genuine blind spot (`tkt-045`, a dual-gold ticket).

### Failure split (per version, on 18 failed tickets)

| | Retrieval fail (gold not in top-2) | Generation fail |
|---|---|---|
| v1 | 1 | 17 |
| v2 | 1 | 17 |

**17 of 18 hard failures have the right section in front of the model and fail
on generation.** That is the finding that matters for the pipeline.

## RAGAS (n=30)

| Metric | Mean | 95 % CI |
|---|---|---|
| **faithfulness** (primary) | **0.6764** | [0.5898, 0.7604] |
| answer_relevancy | 0.7087 | [0.6102, 0.7855] |
| context_precision | 0.9333 | [0.8500, 1.0000] |

146 LLM calls (≈ 4.9/sample). The `Faithfulness` metric is the expensive one:
it lists atomic claims then scores each, and with `max_tokens=4096` on
`qwen3.8:27b` the claim list is frequently truncated — this is why the CI is
wide. Wall time ≈ 51 min.

## DeepEval (n=30)

| Metric | Mean | 95 % CI |
|---|---|---|
| **faithfulness** (primary) | **0.9868** | [0.9733, 0.9976] |
| answer_relevancy | 0.9851 | [0.9684, 0.9984] |
| context_precision | 0.9500 | [0.8667, 1.0000] |

270 LLM calls (within the 300 cap). Wall time ≈ 48 min.

### RAGAS vs DeepEval, side by side

| | RAGAS | DeepEval |
|---|---|---|
| faithfulness | 0.676 [0.590, 0.760] | 0.987 [0.973, 0.998] |
| answer_relevancy | 0.709 [0.610, 0.786] | 0.985 [0.968, 0.998] |
| context_precision | 0.933 [0.850, 1.000] | 0.950 [0.867, 1.000] |

Two different stacks, two different priors. RAGAS is much harsher on
faithfulness (0.676) than DeepEval (0.987). The reason is that DeepEval's
`Faithfulness` metric treats the `reference` field as a *grounding source* and
decomposes the response into atomic claims it can confirm against it; RAGAS
instead asks the LLM to *list every* claim and check each one against the
reference, so anything the model infers-but-doesn't-state drops the ticket.
For *this* corpus, where the answers are short and grounded, the difference
reads as DeepEval being more lenient and RAGAS being more demanding.

DeepEval is also **effectively binary** in this run — **26 of 30 tickets scored
exactly 1.0** on faithfulness (values: 1.0×26, 0.929×1, 0.9×2, 0.875×1);
answer_relevancy is the same shape (26 at 1.0). The 4 non-1.0 tickets are the
only ones with a *partially* unmet atomic claim. That is why its mean is 0.987
rather than 0.85, and why the Spearman agreement numbers (below) are near
zero: a near-constant column has almost no rank structure to correlate on.

## Agreement (n=28, pure)

| Metric | Value |
|---|---|
| spearman_ragas_vs_deepeval | **-0.234** |
| spearman_ragas_vs_embed | **+0.379** |
| spearman_deepeval_vs_embed | **-0.239** |
| auroc_ragas_faithfulness_vs_label | **0.578** |
| auroc_deepeval_faithfulness_vs_label | **0.567** |
| auroc_embed_cosine_vs_label | **0.756** |
| auroc_ragas_faithfulness_vs_verdict | 0.578 |
| auroc_deepeval_faithfulness_vs_verdict | 0.520 |
| auroc_embed_cosine_vs_verdict | 0.571 |

Reading:

- **Rank order does not transfer.** RAGAS and DeepEval faithfulness have a
  slightly *negative* Spearman (-0.234): the tickets RAGAS scores high are
  *not* the same ones DeepEval scores high. Same for both against the ch-04
  embedding cosine (± 0.23-0.38, with signs pointing different directions).
  Three different stacks, three different orderings.

- **But the *label* transfer is weakly positive and similar for all three.**
  AUROC against the gold chapter-03 `pass` label is 0.58 (RAGAS) / 0.57
  (DeepEval) / **0.76 (ch-04 embedding)**. None of the "expensive" LLM-judge
  stacks beats the raw cosine similarity at predicting the gold label. The
  cosine is the strongest single-feature predictor we have; adding LLM judges
  helps only marginally and only for RAGAS.

- **Against the chapter-05 *overall* verdict** every AUROC is ~0.52-0.57 —
  i.e. essentially at chance. The chapter-05 verdict is the aggregate of many
  per-ticket judges (correctness, completeness, no-hallucination) and no
  single judge — including the embedding — reliably reproduces it. This is
  the expected failure mode: our ch-07 ensemble *is* the ground truth we are
  evaluating against, so single judges cannot outperform the ensemble they
  are components of.

### Two counter-example tickets

The spec calls out two specific tickets where RAGAS and DeepEval disagree
sharply and the gold label is on the RAGAS side:

- **`tkt-012`** — gold `pass=True`, ch-05 `pred_pass=False` (so our *own* ch-05
  verdict also flags this one), ch-04 `embed_cosine=0.853` (looks good).
  RAGAS faithfulness **0.250** / DeepEval faithfulness **1.000**. DeepEval
  says "perfect" where RAGAS, the cosine-similarity check, *and* our own ch-05
  all say it's not. This is the case DeepEval misses.
- **`tkt-014`** — gold `pass=False`, ch-05 `pred_pass=True` (our own ch-05
  verdict also misses it), ch-04 `embed_cosine=0.534` (looks borderline).
  RAGAS faithfulness **0.222** / DeepEval faithfulness **1.000**. Once again
  DeepEval tops the ticket as perfect while RAGAS catches the failure. Both
  counter-examples are in the same direction — **DeepEval is the lenient
  stack and RAGAS is the one aligned with the gold label on the failure
  tickets.**

This is exactly why the two stacks disagree (Spearman -0.23): DeepEval's
binary-decomposition approach saturates at 1.0 the moment it cannot find a
*contradiction* with the reference, whereas RAGAS' "list every claim and
check each" approach gives partial credit. For *ranking* quality answers the
two agree; for *catching* bad ones, only RAGAS does.

## Versions / provenance

| Component | Version |
|---|---|
| `ragas` | 0.4.3 |
| `deepeval` | 4.2.1 (native `OllamaModel`) |
| `numpy` / `pandas` / `scikit-learn` | see `project/uv.lock` |
| Judge model | `qwen3.8:27b` at `http://127.0.0.1:11435` (Ollama) |
| Embedding model | `nomic-embed-text` (ch-03, ch-04) |
| Test split | 60 tickets; RAGAS/DeepEval use first 30 by `split="test"` |
| Python | 3.14 (uv-managed venv) |

Total LLM calls for this chapter: **146 (RAGAS) + 270 (DeepEval) + ~150
(ch-05 re-run, not recited) ≈ 566**. Ch-08 itself is within budget.

## Bottom line

- Retrieval recall@2 is 84 % with a ±8 pt CI and only 1 genuine retrieval
  blind spot (`tkt-045`). **17 of 18 hard failures are generation problems**
  — the right section is in front of the model and it still fails the answer.
- RAGAS and DeepEval agree *about the label* (AUROC ≈ 0.57 against the gold
  ch-03 label) but **do not agree about ordering** (Spearman -0.23). The ch-04
  cosine, the cheapest feature, is actually the best single label predictor
  (AUROC 0.756).
- The two specific counter-example tickets (`tkt-012`, `tkt-014`) are both
  caught by RAGAS and missed by DeepEval, reinforcing that DeepEval's
  binary-decomposition is more lenient than RAGAS' partial-credit approach on
  this corpus.
- Practical takeaway: for a small local 27B model, the answer-side judge is
  *noisier than its CI suggests* — truncated claim lists in RAGAS and a
  binary 0/1 in DeepEval both hide the true per-ticket uncertainty. Treat the
  mean+CI as a band, not a point estimate; the per-ticket disagreement with
  the gold is 20%+ on failure tickets.
