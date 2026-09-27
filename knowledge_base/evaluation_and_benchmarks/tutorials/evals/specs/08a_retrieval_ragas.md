# Task: chapter 08a — RAG evals: retrieval metrics against gold sections and RAGAS via Ollama (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/08_rag_evals_impl.md` (full design — this task is its FIRST HALF:
`retrieval` and `ragas`), `research/SOURCES_tools.md` (RAGAS entry only), `--help` of
`evals_tutorial.helpdesk` and the signatures of `results.write_metrics`, `stats.bootstrap_ci`.
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `project/src/evals_tutorial/rag_evals.py` with `retrieval` fully implemented (hit@k, recall@k,
   precision@k, MRR, nDCG@4; recall@k curve for k = 1..8 via `helpdesk.retrieve` → PNG;
   retrieval-vs-generation split using `runs/05_judge_overall/predictions.jsonl`) for `answer_v1` and
   `answer_v2` → experiments `08_retrieval_answer_v1` / `_v2` (primary `recall@2`, CI).
2. `ragas --split test --n 30` exactly as in the original spec (install, check API, count calls, ≤ 300;
   cut to 20 items if needed) → `08_ragas_answer_v1` (primary `faithfulness`). `just results`.
3. Stubs for `deepeval`, `agreement`, `all` (08b fills them).
4. `project/tests/test_08_rag_evals.py`: hand-computed hit@k/recall@k/MRR/nDCG; retrieval-vs-generation split
   on synthetic data; RAGAS wiring import-guarded, live path `@pytest.mark.slow`. No network.
5. `project/runs/08a_findings.md`: retrieval tables and curve numbers, the split, RAGAS means/ranges/
   calls/seconds/rough edges, installed ragas version.

Files to commit: `project/src/evals_tutorial/rag_evals.py`, `project/pyproject.toml`, `project/uv.lock`,
`project/runs/08_retrieval_*/**`, `project/runs/08_ragas_answer_v1/**`, `project/runs/results.md`, `project/data/cache/**`,
`project/justfile`, `project/tests/test_08_rag_evals.py`, `project/runs/08a_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "08_retrieval_answer_v1"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 350 calls (RAGAS + embeddings). Do not run `fleet serve restart` or `fleet run`.
