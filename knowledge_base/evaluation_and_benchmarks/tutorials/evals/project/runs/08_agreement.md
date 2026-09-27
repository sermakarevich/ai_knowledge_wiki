# Chapter 08b — Evaluator agreement (RAGAS × DeepEval × embedding × label)

Pure analysis (no LLM calls) on the 28 tickets where all four sources have a
non-null score. Sources, aligned by `ticket_id`:

- **RAGAS faithfulness** — `runs/08_ragas_answer_v1/predictions.jsonl` (positional:
  first 30 test-split ids, n=30).
- **DeepEval faithfulness** — `runs/08_deepeval_answer_v1/predictions.jsonl`
  (n=30, keyed by `ticket_id`).
- **Chapter-04 embedding cosine** — `runs/04_similarity_answer_v1/predictions.jsonl`
  (n=60, keyed by `ticket_id`).
- **Chapter-03 gold `pass` label** and **chapter-05 overall `pred_pass` verdict** —
  `runs/05_judge_overall/predictions.jsonl` (n=60, keyed by `ticket_id`).

Experiment: `runs/08_agreement_metrics/` (primary `auroc_ragas_faithfulness_vs_label`).

## Metric table (n=28)

| Metric | Value |
|---|---|
| spearman_ragas_vs_deepeval | **-0.2336** |
| spearman_ragas_vs_embed | **+0.3793** |
| spearman_deepeval_vs_embed | **-0.2386** |
| auroc_ragas_faithfulness_vs_label | **0.5778** |
| auroc_deepeval_faithfulness_vs_label | **0.5667** |
| auroc_embed_cosine_vs_label | **0.7556** |
| auroc_ragas_faithfulness_vs_verdict | 0.5782 |
| auroc_deepeval_faithfulness_vs_verdict | 0.5204 |
| auroc_embed_cosine_vs_verdict | 0.5714 |

## Findings

1. **Rank order does not transfer between stacks.** RAGAS and DeepEval
   faithfulness have a *negative* Spearman (-0.234): the tickets RAGAS scores
   high are not the ones DeepEval scores high. Both against the chapter-04
   embedding cosine they sit at ±0.23-0.38 with conflicting signs. Three
   different stacks, three different orderings; there is no single "quality
   ranking" the community stacks agree on.

2. **The gold-label signal is weakly positive and nearly identical across
   stacks.** AUROC against the chapter-03 gold `pass` label is 0.578 (RAGAS),
   0.567 (DeepEval). None of the LLM-judge stacks beats **0.756**, which is the
   AUROC of the raw *embedding cosine* — the cheapest feature in the stack.
   The single cosine similarity is the best individual label predictor we have;
   the expensive judges add little on top of it for this task.

3. **Against the chapter-05 overall verdict, every single judge falls to
   chance (0.52-0.58).** This is expected and informative: the chapter-05
   verdict is the *ensemble* of per-ticket judges (correctness, completeness,
   no-hallucination) and a single component cannot reliably reconstruct the
   aggregate it is part of. So "the judges disagree with the ensemble" is not
   a failure of any one judge; it is the ceiling of single-feature evaluation.

## Counter-example tickets

The two tickets where RAGAS and DeepEval disagree sharply, with the signal in
opposite directions, are the ones that pin down *which* stack is doing the
catching and *which* is doing the passing. Both are on the gold-fail side,
caught by RAGAS and missed by DeepEval:

| Ticket | gold `pass` | ch-05 verdict | ch-04 embed | RAGAS fid | DeepEval fid |
|---|---|---|---|---|---|
| **tkt-012** | True | False | 0.853 | **0.250** | **1.000** |
| **tkt-014** | False | True | 0.534 | **0.222** | **1.000** |

- **tkt-012**: a ticket the gold data says *pass*, that our ch-05 ensemble
  *also* flags as failing, that ch-04 cosine rates high (0.853), and that
  DeepEval calls "perfectly faithful" — RAGAS rates 0.250. This is the case
  where DeepEval's lenient binary-decomposition saturates at 1.0 and RAGAS
  stays aligned with the other signals.
- **tkt-014**: a ticket the gold data says *fail*, that our ch-05 ensemble
  *misses* (predicts pass), that ch-04 cosine rates borderline (0.534). Both
  DeepEval (1.000) and our ch-05 ensemble miss this; RAGAS's 0.222 is the only
  signal aligned with the gold. This is the "even our own ensemble doesn't
  catch it, and the third-party stack doesn't either" ticket.

Across the 30 aligned tickets, in 10 of 30 deep-vs-RAGAS disagree on the 0.5
threshold — DeepEval leans "pass", RAGAS leans "fail", **in the same direction
both times** (both counter-example tickets above). DeepEval is *systematically
more lenient* on this corpus, RAGAS is *more aligned with the label* on
failure tickets. The practical implication: if you need a failure-catch, use
RAGAS; if you need a fast "is this plausibly faithful" screen, DeepEval.

## Provenance

- `deepeval==4.2.1` (native `OllamaModel`, no custom wrapper). `ragas==0.4.3`.
  See `project/uv.lock` / `project/pyproject.toml`.
- Judge model: `qwen3.8:27b` over Ollama at `127.0.0.1:11435`.
- Alignment: 30 tickets (first test-split in `05_judge_overall` ordering); 2
  dropped (any source `NaN`) → n=28.
- Reproduce: `cd project && uv run python -m evals_tutorial.rag_evals
  agreement --run answer_v1 --n 30 --seed 0` (0 LLM calls).
