# Task: 14b — consistency pass over chapters 00–06 (markdown fixes only)

Read: `index.md`, `specs/COMMON.md`, `project/runs/results.md`, then the chapters `00_setup.md` …
`06_judges_under_the_microscope.md` **one at a time** (read, fix, commit, move on — never hold two in
context). (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Problem
Chapters were written by different workers from findings notes. Numbers may have drifted from
`results.md`, abbreviations may be unexplained, structure sections may be missing, links may be wrong.

## Fix
For each chapter, check and fix in place:
- every number that names an experiment matches `project/runs/results.md` (primary metric, CI, n) —
  when a chapter predates chapter 07, add the CI from `results.md` in a short sentence rather than
  rewriting; if a number cannot be traced to a committed file, replace it with the committed one or mark
  it "(not measured)";
- structure: `# 0N — …`, `## What you will learn`, `## Troubleshooting` table, `## Exercises`, `Next:`
  line pointing to the actual next file; experiment chapters have "What landed in the results table",
  library chapters have "Advantages and disadvantages";
- every abbreviation explained at first use in that chapter (LLM, RAG, CI, TPR, TNR, MRR, nDCG, AUROC,
  F1, BT, …); simple language;
- code excerpts refer to functions that exist (`grep -n "def <name>" project/src/evals_tutorial/*.py`);
  commands refer to existing just recipes; file paths exist;
- one citation line per method; mermaid blocks parse (no `=`-leading labels, no unquoted `:` in node
  text); no leftover TODO/placeholder text; length 300–500 lines (trim or note if far outside).
Keep a running log `runs/14b_consistency_log.md`: per chapter, the list of fixes (one line each).

## Tests
`for f in 0[0-6]_*.md; do grep -q "What you will learn" "$f" && grep -qi troubleshooting "$f" && grep -q "^Next:" "$f" || echo "FAIL $f"; done`

## DoD
As in COMMON.md. Commit after each chapter (`evals: 14b consistency <chapter>`), and finally
`runs/14b_consistency_log.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/14b_consistency_log.md | grep -c "^- "` ≥ 7.

## Scope & constraints
Markdown only — no code, no runs, no `index.md` edits (record needed index changes in the log for 14d).
Never change a number to something not in a committed file. Context budget ≈ 50k tokens (one chapter at
a time). Do not run `fleet serve restart` or `fleet run`.
