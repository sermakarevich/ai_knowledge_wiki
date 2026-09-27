# Task: chapter 05b — LLM-as-judge: test-split runs, likert and no-context ablations, scorecard, disagreement review, findings (runs only, NO chapter writing, code changes only to fix bugs)

Read ONLY `specs/COMMON.md`, `index.md` ("Results table columns"), `project/runs/05a_findings.md`,
`project/runs/05_align_dev.md`, `project/src/evals_tutorial/judge.py` (only `--help` output and
`grep -n "^def \|^@app" …`; open a function body only when it fails), and `project/justfile` (judge
recipes). Do NOT read research notes or chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Task 05a made the judge module work and chose v1 or v2 per failure mode on `dev`. Now the frozen judges
must be measured on `test` (60 tickets) and the two classic mistakes demonstrated (a single 1–5 Likert
score; a judge without the retrieved context). Everything ends in `results.md` rows and the findings
note the chapter writer needs.

## Fix (run in this order, `just gpu-check` first, in the background with a log)
1. `judge run --mode all --version best --split test` → per tracked mode, experiment `05_judge_<mode>`
   (primary `kappa`, n = 60, `tpr`, `tnr`, `accuracy` in metrics, `ci` = {} — chapter 07 adds CIs).
   ≤ 6 × 60 = 360 calls. If after 4 modes the wall clock exceeds 2.5 h, stop at the 4 most frequent modes
   and record it.
2. `judge overall --split test` → experiment `05_judge_overall` (overall pass = no mode fails vs the
   chapter-03 `pass` label; primary `kappa`). Zero new calls (reuses step 1).
3. `judge likert --split test` on the **first 30 test tickets** (seeded order) → experiment
   `05_likert_overall` (primary `auroc` of the 1–5 score vs `pass`; details: score histogram). 30 calls.
4. `judge nocontext --mode missing_required_fact --split test` on the same 30 tickets → experiment
   `05_judge_missing_required_fact_nocontext` (primary `kappa`), and in `details` the with-context kappa
   on the same 30 for a fair comparison. 30 calls.
5. `judge scorecard` → `project/runs/05_judge_scorecard.md`: modes × {v1, v2} on dev (from 05a) and the
   chosen version on test; then `just results`.
6. **Disagreement review**: for the mode with the most test failures, list judge-vs-label disagreements in
   `project/runs/05_judge_disagreements.md` (ticket id, label note, judge critique). Read 10 of them and
   add one line each: `judge wrong` / `label wrong` / `ambiguous`. Do not change the chapter-03 labels.
7. `project/runs/05_findings.md` (REQUIRED, merge in the 05a note): the full scorecard; which version
   won per mode and by how much; the new `results.md` rows (copy the lines); Likert histogram and AUROC vs
   the binary judge's kappa; nocontext vs with-context; disagreement counts with 2 quoted critiques; LLM
   calls and seconds; what was skipped.

If a step fails because of a bug in `judge.py`, fix the bug minimally, re-run the tests, and note it.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/runs/05_*/**`, `project/runs/05_judge_scorecard.md`, `project/runs/05_judge_disagreements.md`,
`project/runs/05_findings.md`, `project/runs/results.md`, `project/data/cache/**`, plus `project/src/evals_tutorial/judge.py`
only if you fixed a bug.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "05_judge_overall"` ≥ 1.

## Scope & constraints
No new prompts, no redesign, no CIs. ≤ 450 LLM calls. Context budget ≈ 40k tokens: never `cat` a
predictions file — use `head -3` and `wc -l`. Do not run `fleet serve restart` or `fleet run`.
