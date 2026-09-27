# Task: chapter 07 impl — statistics: bootstrap CIs, paired comparison v1 vs v2, clustered errors, power, multiple comparisons; retrofit CIs to every metrics.json (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/src/evals_tutorial/{results,judge,helpdesk}.py`
(signatures: `write_metrics`, `judge.run`, `helpdesk.run`, `load_traces`), `project/runs/results.md`,
`project/src/evals_tutorial/prompts/answer_v1.txt`, and `research/SOURCES_papers.md` (section on
Miller 2024 "Adding Error Bars to Evals", arXiv 2411.00640, and on statistical testing for evals).
Do not read chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Every number in `results.md` is a point estimate on 60 tickets. A pass rate of 0.72 vs 0.78 means nothing
without error bars. This chapter builds the shared `stats` module, **retrofits a 95 % CI onto every
existing experiment** by re-reading its `predictions.jsonl`, and performs the tutorial's first proper
A/B: prompt `answer_v2` vs `answer_v1`, paired per ticket.

## Fix

### `project/src/evals_tutorial/stats.py` (Typer: `ci`, `paired`, `power`, `retrofit`)
Pure functions, numpy only, seed argument everywhere:
- `bootstrap_ci(values, stat=np.mean, n_boot=2000, alpha=0.05, seed=0)` → `(lo, hi)`; also
  `wilson_ci(k, n)` for proportions and `clustered_bootstrap_ci(values, clusters, …)` (resample clusters
  — tickets share a `topic`, 12 clusters).
- `paired_bootstrap(a, b, …)` → mean difference, CI, and one-sided/two-sided p-value; plus
  `mcnemar(a, b)` for binary outcomes and `permutation_test`.
- `power_binary(p0, delta, alpha=0.05, power=0.8)` → n per arm for an unpaired comparison, and
  `power_paired(p_discordant, delta, …)`; print a small table for delta ∈ {0.05, 0.10, 0.20}.
- `bonferroni(pvals)` and `benjamini_hochberg(pvals)`.
- `retrofit`: for every `runs/*/metrics.json` whose `predictions.jsonl` has a binary or numeric
  per-item field (name the field per experiment in a small dict — `pass`, `correct`, `agree`, …),
  compute the 95 % bootstrap CI of the primary metric and write it into `ci` (and `clustered` CI into
  `details` when a `topic` can be joined via the tickets file); re-run `results.build()`.
  Experiments whose primary metric is not a mean (kappa, AUROC, F1, Spearman) get a bootstrap over items
  recomputing that statistic — implement kappa/AUROC/f1 bootstrap by resampling rows of predictions.

### The A/B: `answer_v2`
- Write `prompts/answer_v2.txt`: same as v1 plus explicit instructions targeting the top-2 failure modes
  of chapter 03 (e.g. "quote the exact figure from the section", "never promise refunds outside the
  policy"). Run `helpdesk run --task answer --version v2` on all 80 tickets (80 calls) → traces
  `runs/traces/answer_v2/`.
- Grade v2 with the chapter-05 overall judge (frozen prompts, `judge.run` per mode on `test`, ≈ 60 ×
  modes calls ≤ 360) → `05_judge_*` style predictions under `runs/07_answer_v2_judged/`; also run the
  chapter-04 `checks` on v2 (free).
- `paired --a answer_v1 --b answer_v2`: per-ticket pass (judge overall) paired difference with CI and
  p-values (bootstrap + McNemar), the unpaired comparison for contrast, clustered by topic; per-topic
  win/loss table. Experiment `07_ab_answer_v2_vs_v1` (primary `pass_rate_delta`, `ci` on the delta,
  n = 60, details: p-values, discordant pairs, per-topic table). Also `07_answer_v2_pass_rate` (primary
  `pass_rate`, with CI) so v2 has its own row.
- Multiple comparisons demo: the per-check p-values from the chapter-04 check table for v1 vs v2,
  raw vs Bonferroni vs BH → `details` of the A/B experiment.
- Power table → `runs/07_power_table.md`.

### `project/justfile`
`stats-retrofit`, `ab-answer-v2`.

### Tests `project/tests/test_07_stats.py`
Bootstrap CI contains the true mean on a synthetic sample and narrows with n; Wilson vs bootstrap
agree roughly; paired bootstrap detects a known shift and does not on identical arrays; McNemar
hand-computed on a 2×2; power monotonic in delta; BH ≥ Bonferroni rejections; `retrofit` on a
`tmp_path` runs dir writes `ci`. No network.

### Findings note `project/runs/07_findings.md` (REQUIRED)
The retrofitted table (copy `results.md` — every row now has a CI); widths of the CIs at n = 60 and what
that implies; the A/B result (delta, CI, p-values, discordant pairs, per-topic table, clustered vs
plain CI); the multiple-comparisons demo; the power table; 3–5 observations; LLM calls and seconds.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/stats.py`, `project/src/evals_tutorial/prompts/answer_v2.txt`,
`project/runs/traces/answer_v2/**`, `project/runs/07_*/**`, `project/runs/07_power_table.md`, every updated
`project/runs/*/metrics.json`, `project/runs/results.md`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_07_stats.py`, `project/runs/07_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "07_ab_answer_v2_vs_v1"` ≥ 1.

## Scope & constraints
Do not edit chapter-05 prompts or chapter-03 labels; do not touch `answer_v1` traces. ≤ ~450 LLM calls
(gpu-check first, background run). Context budget ≈ 55k tokens. Do not run `fleet serve restart` or
`fleet run`.
