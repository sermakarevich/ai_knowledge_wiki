# Task: chapter 09a — hallucination detectors on RAGTruth: HHEM-2.1-Open, LettuceDetect, NLI cross-encoder (CPU code + runs, ZERO LLM calls, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/09_hallucination_detectors_impl.md` (full design — this task is its
FIRST HALF: the three CPU detectors), `project/data/public/README.md` (RAGTruth part),
`research/SOURCES_tools.md` (HHEM, LettuceDetect, NLI entries), signatures of `results.write_metrics`,
`stats.bootstrap_ci`. (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `project/src/evals_tutorial/halluc.py`: the common scorer interface (score in [0,1], threshold chosen on
   the first 80 rows to maximise F1, reported on the other 400, seconds/item on CPU), and `hhem`, `lettuce`,
   `nli` fully implemented → experiments `09_hhem_ragtruth`, `09_lettuce_ragtruth` (with span-level P/R in
   details), `09_nli_ragtruth` (primary `auroc`, n = 400, CI). Stubs for `selfcheck`, `judge`, `compare`,
   `apply`. `just results`.
2. Dependencies added to pyproject (`transformers`, CPU `torch`, `sentence-transformers`, `lettucedetect`);
   weights go to `~/.cache`, never git. If a package will not install, skip it and record why.
3. `project/tests/test_09_halluc.py`: threshold selection + metrics on canned scores; sentence splitting
   and chunking; span-level P/R on a hand example; the RAGTruth file has 480 rows with the contract fields;
   model paths `@pytest.mark.slow`. No downloads in tests.
4. `project/runs/09a_findings.md`: the three detectors' AUROC/F1/P/R, s/item, per-task-type breakdown,
   model sizes/load times, install problems.

Files to commit: `project/src/evals_tutorial/halluc.py`, `project/pyproject.toml`, `project/uv.lock`,
`project/runs/09_hhem_ragtruth/**`, `project/runs/09_lettuce_ragtruth/**`, `project/runs/09_nli_ragtruth/**`,
`project/runs/results.md`, `project/justfile`, `project/tests/test_09_halluc.py`, `project/runs/09a_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "09_hhem_ragtruth"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: 0 calls (CPU only). Do not run `fleet serve restart` or `fleet run`.
