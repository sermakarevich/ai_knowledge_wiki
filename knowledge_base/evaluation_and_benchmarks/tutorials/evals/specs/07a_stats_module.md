# Task: chapter 07a — statistics module: bootstrap/Wilson/clustered CIs, paired tests, power, multiple comparisons; retrofit CIs onto every existing metrics.json (code only, ZERO LLM calls, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/07_statistics_impl.md` (full design — this task is its FIRST HALF: the
`stats.py` module and the `retrofit`), `index.md` ("Data contracts": metrics.json), the signature of
`results.write_metrics`/`results.build`, and `head -3` of two `project/runs/*/predictions.jsonl` files.
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `project/src/evals_tutorial/stats.py` exactly as designed in the original spec (`bootstrap_ci`,
   `wilson_ci`, `clustered_bootstrap_ci`, `paired_bootstrap`, `mcnemar`, `permutation_test`,
   `power_binary`, `power_paired`, `bonferroni`, `benjamini_hochberg`, `retrofit`; Typer commands `ci`,
   `paired`, `power`, `retrofit`).
2. `retrofit`: add a 95 % CI to every existing `runs/*/metrics.json` (chapters 04–06) by bootstrapping the
   per-item field of its `predictions.jsonl` (kappa/AUROC/F1 by resampling rows), clustered-by-topic CI
   into `details` where a ticket id can be joined; `just results`.
3. `power` → `project/runs/07_power_table.md`.
4. `project/tests/test_07_stats.py` as in the original spec. No network.
5. `project/justfile`: `stats-retrofit`, `stats-power`.
6. `project/runs/07a_findings.md`: the retrofitted table (copy `results.md`), CI widths at n = 60, the
   power table, observations.

## Not your part (07b)
`answer_v2` prompt, its traces, judging v2, the paired A/B, the multiple-comparisons demo on real
p-values, the final `07_findings.md`.

Files to commit: `project/src/evals_tutorial/stats.py`, every updated `project/runs/*/metrics.json`, `project/runs/results.md`,
`project/runs/07_power_table.md`, `project/justfile`, `project/tests/test_07_stats.py`, `project/runs/07a_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/07_power_table.md | grep -c "delta"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: 0 calls. Do not run `fleet serve restart` or `fleet run`.
