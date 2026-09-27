# Task: chapter 09b — SelfCheckGPT, the LLM judge on RAGTruth, the comparison table, detectors applied to our helpdesk replies, findings (runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/09_hallucination_detectors_impl.md` (full design — this task is its
SECOND HALF: `selfcheck`, `judge`, `compare`, `apply`), `project/runs/09a_findings.md`, `--help` and
`grep -n "^def \|^@app"` of `evals_tutorial.halluc`, `project/data/labels/taxonomy.yaml` (mode ids).
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `selfcheck` on 60 rows (3 sampled responses each at temperature 0.7 = 180 calls; NLI consistency
   scorer from 09a) → `09_selfcheck_ragtruth`.
2. `judge` with `prompts/halluc_judge_v1.txt` on the first 100 test rows (100 calls) → `09_llm_judge_ragtruth`
   (primary `f1`).
3. `compare` → `runs/09_compare.md` (all methods on the shared 100 rows: AUROC/F1/P/R, s/item, pairwise
   agreement, per task type).
4. `apply --run answer_v1`: HHEM and the best detector over the 60 test replies with retrieved sections as
   source, AUROC vs the chapter-03 `unsupported_claim` mode, 3 most-flagged replies → `09_detector_helpdesk_v1`.
   `just results`.
5. Tests: selfcheck aggregation on canned NLI scores; compare table builder on canned rows.
6. `project/runs/09_findings.md` (REQUIRED; merge 09a): everything in the original spec's findings list.

Files to commit: `project/src/evals_tutorial/halluc.py`, `project/src/evals_tutorial/prompts/halluc_judge_v1.txt`,
`project/runs/09_selfcheck_ragtruth/**`, `project/runs/09_llm_judge_ragtruth/**`, `project/runs/09_detector_helpdesk_v1/**`,
`project/runs/09_compare.md`, `project/runs/results.md`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_09_halluc.py`, `project/runs/09_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/09_compare.md | grep -c "AUROC"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 300 calls. Do not run `fleet serve restart` or `fleet run`.
