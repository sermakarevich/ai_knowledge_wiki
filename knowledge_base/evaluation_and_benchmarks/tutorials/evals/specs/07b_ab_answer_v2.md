# Task: chapter 07b — the A/B: prompt answer_v2, traces, judged, paired comparison v1 vs v2, multiple comparisons, findings (runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/07_statistics_impl.md` (full design — this task is its SECOND HALF: "The
A/B: answer_v2"), `project/runs/07a_findings.md`, `project/src/evals_tutorial/prompts/answer_v1.txt`,
`project/data/labels/taxonomy.yaml` (mode counts), `--help` of `evals_tutorial.helpdesk`,
`evals_tutorial.judge`, `evals_tutorial.code_evals`, `evals_tutorial.stats`. (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `prompts/answer_v2.txt` targeting the top-2 failure modes; `helpdesk run --task answer --version v2` on
   all 80 tickets (80 calls; gpu-check first, background + log).
2. Judge v2 on `test` with the frozen chapter-05 judges (`judge run --mode all --version best --split test`
   pointed at run `answer_v2` — add a `--run` option if missing; ≤ 360 calls) and `judge overall`; write
   under `runs/07_answer_v2_judged/`; `code_evals checks` on v2 (free).
3. `stats paired --a answer_v1 --b answer_v2` → experiment `07_ab_answer_v2_vs_v1` (primary
   `pass_rate_delta` with CI, p-values bootstrap + McNemar, discordant pairs, per-topic table, plain vs
   clustered CI) and `07_answer_v2_pass_rate` (primary `pass_rate`, CI). Multiple-comparisons demo on the
   per-check p-values v1 vs v2 (raw / Bonferroni / BH) into `details`. `just results`.
4. Tests: add a `paired` end-to-end test on synthetic predictions to `project/tests/test_07_stats.py`.
5. `project/runs/07_findings.md` (REQUIRED; merge 07a): everything in the original spec's findings list.

Files to commit: `project/src/evals_tutorial/prompts/answer_v2.txt`, `project/src/evals_tutorial/{stats,judge}.py` (if edited),
`project/runs/traces/answer_v2/**`, `project/runs/07_*/**`, `project/runs/results.md`, `project/data/cache/**`,
`project/justfile`, `project/tests/test_07_stats.py`, `project/runs/07_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "07_ab_answer_v2_vs_v1"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 450 calls. Do not run `fleet serve restart` or `fleet run`.
