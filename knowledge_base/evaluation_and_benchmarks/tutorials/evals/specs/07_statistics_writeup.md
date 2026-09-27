# Task: chapter 07 writeup — statistics for evals (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/07_findings.md`, `project/runs/07_power_table.md`,
`project/runs/results.md`, `project/src/evals_tutorial/stats.py` (excerpts), `research/SOURCES_papers.md`
(Miller 2024 section only), and — for style only — `06_judges_under_the_microscope.md`. Nothing else
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The stats module, the CI retrofit and the v1-vs-v2 A/B exist (previous task); the chapter does not.

## Fix
Create `07_statistics.md` (`# 07 — Statistics: error bars for every number`, "## What you will learn"):
why 0.72 vs 0.78 on 60 tickets is noise until proven otherwise; the bootstrap explained in plain words
with a 10-line code excerpt; Wilson vs bootstrap; the retrofitted results table and how wide the CIs are
at n = 60 (Miller 2024, arXiv 2411.00640 — the "eval questions are a sample" framing); paired vs
unpaired comparison and why pairing per ticket shrinks the error (the A/B table, discordant pairs,
McNemar); clustered standard errors — tickets sharing a topic are not independent (show plain vs
clustered CI); how many tickets you need — the power table read out loud; multiple comparisons — the
per-check p-values raw / Bonferroni / BH; a short "how to report a number" checklist (n, split, CI,
paired?, seed). Mermaid: predictions.jsonl → bootstrap → ci → results.md. "What landed in the results
table". Troubleshooting (CI wider than the effect → more items or pairing; bootstrap on kappa unstable;
p-hacking by re-running the judge); Exercises (recompute the CI with n_boot=200 vs 20000; cluster by
persona instead of topic); `Next:` → chapter 08.

## Tests
`test -s 07_statistics.md && grep -c "What you will learn" 07_statistics.md && grep -ci "bootstrap" 07_statistics.md && grep -ci troubleshooting 07_statistics.md`

## DoD
As in COMMON.md. Commit: `07_statistics.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/07_statistics.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
