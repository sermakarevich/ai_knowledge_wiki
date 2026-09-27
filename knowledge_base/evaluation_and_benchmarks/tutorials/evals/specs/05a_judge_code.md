# Task: chapter 05a — LLM-as-judge: make the judge module run, tests, dev-split alignment (code + dev runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md` ("Data contracts"), `project/data/labels/taxonomy.yaml`,
`project/src/evals_tutorial/judge.py` (EXISTS — 670 lines, written by a previous worker, currently has a
**SyntaxError around line 233**), the prompt files `project/src/evals_tutorial/prompts/judge_*.txt` (exist:
v1 and v2 for `missing_required_fact`, `unsupported_claim`, `wrong_section_retrieved`, `did_not_answer`,
plus `judge_likert_v1.txt`, `judge_missing_required_fact_nocontext_v1.txt`), and the signatures of
`results.write_metrics`, `llm.chat_json`, `helpdesk.load_traces`. Do NOT read research notes or chapter
markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
A previous attempt wrote the judge module and all prompts but ran out of context before it ever ran:
`uv run python -m evals_tutorial.judge --help` fails with a SyntaxError, there are no tests, and no judge
results exist. Your job is the **code half only**: make the module work, test it, run the alignment on the
`dev` split (20 tickets), commit. A second task (05b) will run the `test` split, likert, scorecard and
the findings note — do NOT do those.

## Design (already implemented in judge.py — keep it, fix it)
- One binary judge per failure mode with ≥ 4 failing tickets in `taxonomy.yaml` ("tracked modes"); output
  schema `{critique: str, verdict: "pass"|"fail"}`, critique first. `v1` zero-shot, `v2` with 4 dev
  few-shot examples (already in the prompt files; ticket ids in the first comment line — verify they are
  all `dev` tickets, fix if not).
- `grade_split(mode, version, split)` → predictions; `align_mode`/`align_all` → TPR, TNR, accuracy,
  Cohen's kappa vs the chapter-03 labels; `chosen_version(mode)` picks v2 vs v1 **on dev only**.

## Fix
1. Fix the SyntaxError (line ~233 is a garbled comprehension — `load_traces("answer_v1")` keyed by
   `ticket_id` is what it should be) and any further import/runtime errors until `--help` works and
   `align --split dev` runs. Keep changes minimal; do not redesign. Delete the stray helper
   `project/_gen_v2_prompts.py` if the prompts already contain its output (they do), or move it under
   `src/evals_tutorial/` if it is still needed.
2. `project/tests/test_05_judge.py`: `FakeLLM` returning canned `{critique, verdict}` → predictions and
   alignment metrics with hand-computed TPR/TNR/kappa on a 10-row synthetic set; `cohen_kappa` and
   `auroc` on known inputs; every prompt file loads and contains its placeholders; the v2 prompt
   example ids are `dev` tickets (read `project/data/tickets/tickets.jsonl`). No network.
3. Run `align --split dev` for every tracked mode, v1 and v2 (≤ 6 × 2 × 20 = 240 calls; ~120 are already
   in the cache). `just gpu-check` first; background with a log. Save the dev scorecard as
   `project/runs/05_align_dev.md` (mode | version | TPR | TNR | acc | kappa | chosen) and the per-mode
   dev predictions under `project/runs/05_dev/<mode>_<version>.jsonl`.
4. `project/justfile`: `judge-dev` (= align on dev), `judge-test`, `judge-scorecard` (the last two call
   the existing commands; 05b will run them).
5. `project/runs/05a_findings.md` (short): what was broken and fixed, the dev scorecard, which version
   was chosen per mode and why, LLM calls made, anything odd in the critiques (2 quoted examples).

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/judge.py`, `project/src/evals_tutorial/prompts/judge_*.txt`
(if edited), `project/runs/05_align_dev.md`, `project/runs/05_dev/**`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_05_judge.py`, `project/runs/05a_findings.md` (and the removal of `project/_gen_v2_prompts.py`
via `git rm` if you deleted it).
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/05_align_dev.md | grep -c "kappa"` ≥ 1.

## Scope & constraints
`dev` split only. No `test` runs, no likert, no nocontext, no metrics.json, no `results.md` changes, no
findings beyond `05a_findings.md`. ≤ 250 LLM calls. Context budget ≈ 45k tokens: do not print whole
files, use `grep -n`/`sed -n` ranges. Do not run `fleet serve restart` or `fleet run`.
