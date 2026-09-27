# Task: chapter 05 impl — LLM-as-judge: binary judges per failure mode, aligned on dev, measured on test (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md` ("Data contracts", "Results table columns"),
`project/data/labels/taxonomy.yaml`, `project/src/evals_tutorial/results.py` (`write_metrics` signature),
`project/src/evals_tutorial/llm.py` (`chat_json` signature), `project/src/evals_tutorial/helpdesk.py`
(`load_traces`, `run` signature) and `research/SOURCES_practitioner.md` (sections "LLM-as-judge" /
"binary pass-fail" / "judge alignment" only). Do not read chapter markdown
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Chapter 03 produced labels with a *reference-aware* grader that sees the gold answer. A production judge
must work **without** the gold answer (only ticket, retrieved sections, reply). The methodology (Husain /
Shankar; Eugene Yan) says: one binary judge per failure mode, with a critique, few-shot examples from
`dev`, aligned against the labels (true-positive rate TPR, true-negative rate TNR, Cohen's kappa) on `dev`,
then frozen and measured on `test`. We also want to show the two classic mistakes: a single 1–5 Likert
"overall quality" score and a judge without the retrieved context.

## Fix

### `project/src/evals_tutorial/judge.py` (Typer: `run`, `align`, `likert`, `all`)
- Prompts (plain text, `{ticket}`, `{context}`, `{reply}`, `{examples}` placeholders):
  `prompts/judge_<mode>_v1.txt` for each failure mode id in `taxonomy.yaml` that has ≥ 4 failing
  tickets (expect 4–6 modes; skip rarer ones and say so). Output schema
  `{critique: str, verdict: Literal["pass","fail"]}` — **critique before verdict** (chain-of-thought
  first). `v1` = zero-shot definition from the taxonomy; `v2` = same + 2 pass and 2 fail few-shot examples
  chosen from `dev` tickets (write them into the prompt file, ticket ids in a comment line at the top).
- `run --mode <id> --prompt v1|v2 --run answer_v1 --split dev|test`: judge every trace; `predictions.jsonl`
  with `ticket_id, verdict, critique, label` (label = the mode ∈ `failure_modes` of the chapter-03 labels).
- `align`: TPR, TNR, accuracy, Cohen's kappa of judge vs labels for one (mode, prompt, split); a
  **scorecard** table over all modes × {v1, v2} × {dev, test} printed as Markdown and saved to
  `runs/05_judge_scorecard.md`. Rule you must follow: choose `v2` vs `v1` per mode **on dev only**, then
  report the chosen prompt on `test` as experiment `05_judge_<mode>` (primary `kappa`, n = 60, also
  `tpr`, `tnr` in `metrics`). One extra experiment `05_judge_overall`: `pass` overall = no mode fails,
  vs the chapter-03 `pass` label (primary `kappa`).
- `likert`: `prompts/judge_likert_v1.txt` asks for a 1–5 overall score + one-sentence reason; compute
  AUROC of the score vs the `pass` label and the score distribution (expect a pile-up at 4); experiment
  `05_likert_overall` (primary `auroc`). Ablation `prompts/judge_<best_mode>_nocontext_v1.txt` (reply +
  ticket only, no retrieved sections) for the single mode with the most failures → experiment
  `05_judge_<mode>_nocontext` (primary `kappa`) — shows why the judge needs the context.
- Budget: modes(≤ 6) × prompts(2) × 80 tickets ≈ 960 calls is too many. Do: v1 and v2 on `dev` (20) for
  all modes (≤ 240 calls), then only the chosen prompt on `test` (60) per mode (≤ 360 calls), likert 60,
  nocontext 60. Total ≤ ~700 with cache; run `just gpu-check` first, in the background with a log, and
  if time runs out reduce to the 4 most frequent modes and record it.
- Also write a **judge-error review**: for the best mode, list the `test` disagreements (judge vs label)
  in `runs/05_judge_disagreements.md` with critique + label note; read 10 and write one line each: judge
  wrong / label wrong / genuinely ambiguous. Do not change the chapter-03 labels.

### `project/justfile`
`judge-dev`, `judge-test`, `judge-scorecard`.

### Tests `project/tests/test_05_judge.py`
`FakeLLM` returning canned `{critique, verdict}` → predictions and alignment metrics with hand-computed
TPR/TNR/kappa on a 10-row synthetic set; prompt files load and contain every placeholder; scorecard
renders; the `v2` prompt files reference only `dev` ticket ids (read the committed tickets file).

### Findings note `project/runs/05_findings.md` (REQUIRED)
The scorecard (dev and test); which prompt won per mode and by how much; the new `results.md` rows; the
Likert distribution and AUROC vs the binary judge's kappa; nocontext vs with-context; the disagreement
review counts (judge wrong / label wrong / ambiguous) with 2 quoted critiques; LLM calls and seconds;
what was skipped.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/judge.py`, `project/src/evals_tutorial/prompts/judge_*.txt`,
`project/runs/05_*/**`, `project/runs/05_judge_scorecard.md`, `project/runs/05_judge_disagreements.md`,
`project/runs/results.md`, `project/data/cache/**`, `project/justfile`, `project/tests/test_05_judge.py`,
`project/runs/05_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/05_judge_scorecard.md | grep -c "kappa"` ≥ 1.

## Scope & constraints
No pairwise judging or bias studies (06), no CIs (07), no answer_v2 prompt (07 introduces it for the
paired comparison). Do not change labels, SUT or traces. Context budget ≈ 55k tokens. Do not run
`fleet serve restart` or `fleet run`.
