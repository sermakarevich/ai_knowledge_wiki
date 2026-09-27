# Task: chapter 08 impl — RAG evals: retrieval metrics vs gold sections, RAGAS and DeepEval via Ollama, agreement with our judge (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/src/evals_tutorial/{helpdesk,results,stats,llm}.py`
(signatures: `retrieve`/`load_traces`, `write_metrics`, `bootstrap_ci`, `chat`/`embed`), the chapter-05
overall predictions `project/runs/05_judge_overall/predictions.jsonl` (head), and
`research/SOURCES_tools.md` (entries for RAGAS and DeepEval — versions, Ollama wiring, verdicts) plus
`research/SOURCES_papers.md` (RAG evaluation section: RAGAS, ARES). Do not read chapter markdown
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The helpdesk `answer` task is RAG (retrieval-augmented generation): it retrieves handbook sections, then
writes. Failures can come from retrieval or generation. We have gold sections per ticket, so retrieval
can be scored with classic information-retrieval metrics; generation quality is what RAGAS and DeepEval
promise to score with an LLM judge. We want both, run locally, and we want to know whether the library
scores agree with our aligned chapter-05 judge.

## Fix

### `project/src/evals_tutorial/rag_evals.py` (Typer: `retrieval`, `ragas`, `deepeval`, `agreement`, `all`)
- `retrieval --run answer_v1 --split test` (and `answer_v2`, and a sweep of `k`): from the traces'
  `retrieved[]` vs `gold.sections`: hit@k for k ∈ {1,2,4}, recall@k, precision@k, MRR, nDCG@4 (implement
  in ≤ 60 lines; sanity-check nDCG against a hand example in tests). Also re-run retrieval **only** with
  top-k = 8 through `helpdesk.retrieve` (embeddings cached → cheap) to plot recall@k for k = 1..8 →
  `runs/08_retrieval_answer_v1/recall_at_k.png`. Experiment `08_retrieval_answer_v1` (primary `recall@2`,
  n = 60, CI via `stats.bootstrap_ci`). Retrieval-failure vs generation-failure split: among the tickets
  the chapter-05 overall judge failed, the share where the gold section was not retrieved → `details`.
- `ragas --split test --n 30`: install `ragas` (add to pyproject; **check the installed version and API**
  — the Ollama wiring: `langchain_ollama`/OpenAI-compatible LLM + `nomic-embed-text` embeddings; see
  SOURCES_tools). Score the first 30 `test` tickets (seeded) of `answer_v1` on `faithfulness`,
  `answer_relevancy`, `context_precision` (with `gold.answer_points` joined as reference where a metric
  needs one). RAGAS makes several LLM calls per metric per item — count them (wrap the client or read
  the usage log) and stay ≤ ~300; if it exceeds, cut to 20 items and record. Experiment `08_ragas_answer_v1`
  (primary `faithfulness`, n as run, metrics = the three means, `llm_calls` recorded, `seconds`).
  Save per-item scores to `predictions.jsonl`. Record every rough edge (timeouts, NaN scores, parse
  failures) in the findings.
- `deepeval --split test --n 30`: install `deepeval`; custom `DeepEvalBaseLLM` subclass over the
  OpenAI-compatible endpoint (check the installed version's API); `FaithfulnessMetric`,
  `AnswerRelevancyMetric`, `ContextualPrecisionMetric` on the same 30 tickets; experiment
  `08_deepeval_answer_v1` (primary `faithfulness`); count calls; disable telemetry
  (`DEEPEVAL_TELEMETRY_OPT_OUT=YES`) and any login prompts.
- `agreement`: on the 30 common tickets: Spearman between RAGAS faithfulness, DeepEval faithfulness, the
  chapter-04 embedding similarity, and AUROC of each vs the chapter-03 `pass` label and vs the
  chapter-05 overall judge verdict; Markdown table → `runs/08_agreement.md`; experiment
  `08_agreement_metrics` (primary `auroc_ragas_faithfulness_vs_label`).

### `project/justfile`
`rag-retrieval`, `rag-ragas`, `rag-deepeval`, `rag-all`.

### Tests `project/tests/test_08_rag_evals.py`
hit@k / recall@k / MRR / nDCG on a hand-computed example; retrieval-vs-generation split on synthetic
traces+verdicts; agreement table on canned scores; RAGAS/DeepEval wiring functions are import-guarded
and the live paths are `@pytest.mark.slow`. No network.

### Findings note `project/runs/08_findings.md` (REQUIRED)
Retrieval table (all metrics, v1 and v2, with CI on recall@2), the recall@k curve numbers, the
retrieval-vs-generation split; RAGAS and DeepEval means, per-item ranges, number of LLM calls and
seconds per item, every rough edge; the agreement table with a one-line reading; two concrete tickets
(one where RAGAS faithfulness is high but the label is fail, one the reverse) with the scores and one
quoted sentence; versions of ragas / deepeval installed; what was skipped.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/rag_evals.py`, `project/pyproject.toml`, `project/uv.lock`,
`project/runs/08_*/**`, `project/runs/08_agreement.md`, `project/runs/results.md`, `project/data/cache/**`,
`project/justfile`, `project/tests/test_08_rag_evals.py`, `project/runs/08_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "08_retrieval_answer_v1"` ≥ 1.

## Scope & constraints
Do not change the retriever or prompts. Sample sizes are fixed (30 items for the libraries). ≤ ~600
library LLM calls in total (gpu-check first, background, log the counts). Context budget ≈ 55k tokens.
Do not run `fleet serve restart` or `fleet run`.
