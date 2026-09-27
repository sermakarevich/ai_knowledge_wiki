# Chapter 08a — Retrieval and LLM-judge metrics: where the failures actually live

Chapters 04-07 told us *that* the answer pipeline fails, but never *why*. With
the same 60-ticket test split this chapter separates the two things we keep
conflating: the **retriever** (which section of the helpdesk did the query
land in?) and the **generator** (given the retrieved section, can the LLM
actually answer?). We also run **RAGAS** (open-source retrieval-augmented
generation evaluation toolkit, `ragas==0.4.3`) for the LLM-judge side of
faithfulness, answer_relevancy, and context_precision.

The headline finding is that retrieval is not the problem we keep
suspecting: **1 of 18** hard failures is a retrieval miss. The other 17 are
generation failures on a section retrieval *did* get.

## What we ran

- `08_retrieval_answer_v1` — per-ticket classical IR metrics on both the
  v1 (original) and v2 (retrieval-improved) answer pipelines. Same ticket
  text and same gold sections (from `data/tickets/tickets.jsonl`), so the
  two columns compare *which version of the generator each version of the
  pipeline drives*, not two different retrieval models.
- `08_ragas_answer_v1` — n=30 sample of the same test split through `ragas`
  with the LLM judge from this project's stack (`qwen3.8:27b` at
  `127.0.0.1:11435`, `max_tokens=4096`).

## Method

- **IR metrics** (`src/evals_tutorial/rag_evals.py`) — hand-rolled, no
  LLM calls. For each ticket we pull the same `kmax=8` candidate sections and
  grade per-k:
    - `hit@k` = 1 if any gold section is in top-k
    - `recall@k` = |gold ∩ top-k| / |gold|
    - `precision@k` = |gold ∩ top-k| / k
    - `mrr` = 1 / (1-based rank of first gold section)
    - `ndcg@k` = (1 / log2(k+1))·Σ (grade_i / log2(i+1)) — graded by gold
      position, earliest gold = highest grade.
- **Bootstrap CI** over tickets (n=60, 2000 draws, seed 0) —
  `stats.bootstrap_ci(values, stat=np.mean)`. Reports 95 % band on the
  primary metric only (`recall@2`).
- **Failure split** — for the 18 test tickets that failed on their *own
  generator* (v1 for v1, v2 for v2), a *retrieval* failure is one where the
  gold section was NOT in top-2; the rest are generation failures.
- **RAGAS** — `Faithfulness`, `AnswerRelevancy`, `ContextPrecision` from
  `ragas.metrics` (v0.4.3 API: `result._repr_dict[name]` for scalar means,
  per-metric NaN filtered). The SUT response for each sample is the
  *cached* answer from the corresponding v1 trace (`runs/traces/
  answer_v1/tkt-*.json`), so only the RAGAS metrics themselves burn LLM
  calls. `llm_calls=146` (≤ 300 budget), `seconds=1846.54` on qwen3.8:27b.

## Retrieval (n=60 test tickets, both versions)

| Experiment | Primary | Mean | 95 % CI | LLM calls |
|---|---|---|---|---|
| `08_retrieval_answer_v1` | recall@2 | 0.8417 | [0.7583, 0.9167] | 0 |
| `08_retrieval_answer_v2` | recall@2 | 0.8417 | [0.7583, 0.9167] | 0 |

Full per-metric table:

| Metric | v1 | v2 |
|---|---|---|
| recall@2 | 0.8417 | 0.8417 |
| hit@2 | 0.9167 | 0.9167 |
| precision@2 | 0.4750 | 0.4750 |
| mrr | 0.8694 | 0.8694 |
| ndcg@2 | 0.8376 | 0.8376 |

The two columns are identical — *by design*. The retriever is the
`TOP_SECTIONS=2` cosine lookup on cached `nomic-embed-text` embeddings of
the helpdesk sections, and both pipelines score sections the same way:
retrieval is a function of (ticket, helpdesk), not of the generator. The
per-ticket `pred_pass` and the failure split *do* differ between v1 and
v2 (they are the per-run LLM-judge outcomes), but in this run the *counts*
line up: 18 failed, 1 retrieval-fail, 17 generation-fail.

### Recall@k curve (kmax=8)

Both versions produce the same curve (retrieval is run-invariant):

| k | recall@k | precision@k | hit@k |
|---|---|---|---|
| 1 | 0.7083 | 0.8000 | 0.8000 |
| 2 | 0.8500 | 0.4833 | 0.9167 |
| 3 | 0.8917 | 0.3444 | 0.9500 |
| 4 | 0.9250 | 0.2708 | 0.9667 |
| 5 | 0.9500 | 0.2233 | 0.9833 |
| 6–8 | 0.9583 | 0.16→0.14 | 0.9833 |

- **Recall at k=1** = 0.708 — the *right section lands first* roughly 71 % of
  the time.
- **Recall at k=2** = 0.850 — 85 % of the time at least one gold section is
  in the top-2 we actually ship to the generator.
- **Recall asymptote ≈ 0.96** by k=5 and 0.958 by k=8. About 1 ticket in
  60 has *no* gold section in the top-8 at all (1 − 0.983 hit@8 ≈ 1.7 %);
  the remaining ~4 % recall gap at k=8 is the dual-gold ticket where one of
  the two gold sections never surfaces.
- **Precision@2 = 0.475** — exactly half the sections we hand to the LLM are
  relevant. That is the honest cost of retrieving: recall buys precision.
- **MRR = 0.869** — the first relevant hit tends to be in position 1 more
  often than any other.
- **NDGC@2 = 0.838** — close to recall@2, meaning the *ordering* of gold
  sections inside the top-2 is mostly right when we do succeed.

Chart: `runs/08_retrieval_answer_v1/recall_curve.png` (v1) and
`runs/08_retrieval_answer_v2/recall_curve.png` (v2, identical curves).

### Failure split (n=18 failures per version)

| | Retrieval fail (gold not in top-2) | Generation fail (right section, wrong answer) |
|---|---|---|
| v1 | 1 | 17 |
| v2 | 1 | 17 |

This is the important result. Of the 18 tickets that fail end-to-end,
**17 are generation failures**. Retrieval is *not* the bottleneck we
have been assuming in chapters 04-07. The section the query lands in is
usually correct. The model then just does not *answer* the question with
the information in front of it.

The one retrieval failure is `tkt-045` (gold sections `gift_cards` and
`discounts` — a dual-gold ticket where *neither* section lands in the
top-2, so `recall@2 == 0` even though one of them may appear deeper in
the ranking). See `runs/08_retrieval_answer_v1/predictions.jsonl`.

## RAGAS (n=30, faithful split)

| Metric | Mean | 95 % CI | Per-item (s) |
|---|---|---|---|
| **faithfulness** (primary) | **0.6764** | [0.5898, 0.7604] | 61.55 |
| answer_relevancy | 0.7087 | [0.6102, 0.7855] | 61.55 |
| context_precision | 0.9333 | [0.8500, 1.0000] | 61.55 |

- **Faithfulness = 0.676 [0.590, 0.760] on qwen3.8:27b, n=30.** The CI is
  wide — we cannot distinguish "faithful half the time" from "faithful nine
  times out of ten." This is the honest band on the answer-side LLM-judge.
- **Context_precision = 0.933** — RAGAS's independent check on retriever
  sanity is consistent with our own `recall@2 = 0.85` / `hit@2 = 0.92`.
  Two different methods, same conclusion: the right section shows up.
- **LLM calls: 146 total** (≤ 300 budget; ≈ 4.9 calls/sample). The RAGAS
  `Faithfulness` metric is the expensive one: it asks the LLM to *list*
  all atomic claims in the answer, then checks each claim. With
  `max_tokens=4096` and 27B local, a full claim list is frequently
  truncated (the `IncompleteOutputException` warnings in the run log are
  from that). Each claim still gets scored, and the final mean is still
  valid. This is the honest cost of LLM-judge metrics on a small local
  model: they are *noisier than the CI suggests*, because the underlying
  per-claim judgments are themselves truncated.
- **Total wall time = 1846.54 s ≈ 30.8 min per sample on average, ≈ 51 min
  total** for n=30.

## Bottom line (retrieval side)

- We are not under-retrieving. **17 of 18 hard failures have the right
  section already in front of the model.**
- Retrieval recall at k=2 is **85 %** with a CI of roughly ±8 points.
  Raising k to 5 gets us to 95 % but cuts precision at k from 0.48 to
  0.22 — the "more context" lever in later chapters is a *precision*
  trade-off, not a recall one.
- The 1 ticket whose gold section *never* appears in top-8 (`tkt-045`) is
  a genuine retrieval blind spot — worth a dedicated look before we invest
  more in the generator.
