# Task: chapter 08b — RAG evals: DeepEval via Ollama, agreement between RAGAS / DeepEval / similarity / our judge / labels, findings (runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/08_rag_evals_impl.md` (full design — this task is its SECOND HALF:
`deepeval` and `agreement`), `project/runs/08a_findings.md`, `research/SOURCES_tools.md` (DeepEval entry
only), `--help` of `evals_tutorial.rag_evals` and `grep -n "^def \|^@app"` of it.
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `deepeval --split test --n 30` on the same 30 tickets RAGAS used (read their ids from
   `runs/08_ragas_answer_v1/predictions.jsonl`): custom `DeepEvalBaseLLM` over the OpenAI-compatible
   endpoint, Faithfulness / AnswerRelevancy / ContextualPrecision, telemetry off, count calls (≤ 300) →
   `08_deepeval_answer_v1` (primary `faithfulness`).
2. `agreement`: Spearman between RAGAS faithfulness, DeepEval faithfulness and the chapter-04 embedding
   similarity; AUROC of each vs the chapter-03 `pass` label and vs the chapter-05 overall verdict →
   `runs/08_agreement.md`, experiment `08_agreement_metrics`. `all` command; `just results`.
3. Tests: agreement table on canned scores; DeepEval wiring import-guarded, live path slow.
4. `project/runs/08_findings.md` (REQUIRED; merge 08a): everything in the original spec's findings list
   including the two counter-example tickets and installed versions.

Files to commit: `project/src/evals_tutorial/rag_evals.py`, `project/pyproject.toml`, `project/uv.lock`,
`project/runs/08_deepeval_answer_v1/**`, `project/runs/08_agreement_metrics/**`, `project/runs/08_agreement.md`,
`project/runs/results.md`, `project/data/cache/**`, `project/justfile`, `project/tests/test_08_rag_evals.py`,
`project/runs/08_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "08_deepeval_answer_v1"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 300 calls. Do not run `fleet serve restart` or `fleet run`.
