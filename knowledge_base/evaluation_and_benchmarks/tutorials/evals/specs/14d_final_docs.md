# Task: 14d — wrap-up chapter, Q&A, index updates and the tutorials index entry (markdown only)

Read: `index.md`, `specs/COMMON.md`, `project/runs/results.md`, `project/runs/14a_quickstart_report.md`,
`project/runs/14b_consistency_log.md`, `project/runs/14c_consistency_log.md`, the "What landed in the
results table" section of each chapter 04–13 (`grep -n -A 12 "What landed" <chapter>` — excerpts only,
never a whole chapter), `research/SOURCES_practitioner.md` (its "Key ideas" and "Disagreements" sections),
`../index.md` (the tutorials index) and, for the entry format, its existing `rag`/`neo4j` lines.
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Problem
The chapters exist and are consistent; the tutorial has no ending, no Q&A file, and is not listed in the
tutorials index.

## Fix
1. `14_wrapup.md` (`# 14 — Wrap-up: the results table read as one story`, "## What you will learn"):
   the full `results.md` table reproduced, then read as a story in ~10 paragraphs (what code-graded evals
   caught, what the judges added, how well judges track humans, what the error bars allowed us to claim
   about v2 vs v1, retrieval vs generation, detectors vs judges, agent reliability, benchmark
   sensitivity, framework reconciliation, the production loop); a **decision guide** table (situation →
   which eval, which chapter, cost per item, when it lies); an **evals checklist for a new project** (15
   items, ordered, each one line with the chapter reference); the methodological disagreements between
   sources and where this tutorial landed; "what we would do with a real team" (human labels, more test
   items, online data); further reading (10 items with one line each from the research notes);
   Troubleshooting (a short table of the 6 most common mistakes across chapters); Exercises (apply the
   checklist to your own app); no `Next:` — end with a link back to `index.md`.
2. `Q&A.md`: `# Q&A — evals tutorial`; 12–15 questions a reader is likely to ask, each answered in 3–8
   lines with a chapter pointer, drawn from the troubleshooting tables and findings (e.g. "Can I use a
   smaller judge?", "How many test tickets do I need?", "Binary or 1–5?", "Do I need Langfuse?",
   "Why do RAGAS and my judge disagree?"). Append-friendly format.
3. `index.md`: update only what is stale (the "Verified on" pointer, any chapter one-liner the
   consistency logs flagged, the `Q&A.md` line). Data contracts, settings and the columns must not change.
4. `../index.md`: add the `evals` entry in the same format as the existing tutorial lines (title, one
   sentence, `ai show research_topics/evaluation_and_benchmarks/tutorials/evals/index` hint). Run `ai index` or the equivalent rebuild command if
   the knowledge base has one (check `ai --help`); otherwise leave it.

## Tests
`test -s 14_wrapup.md && test -s Q&A.md && grep -c "What you will learn" 14_wrapup.md && grep -ci "checklist" 14_wrapup.md && grep -c "evals" ../index.md`

## DoD
As in COMMON.md. Commit: `14_wrapup.md`, `Q&A.md`, `index.md`, `../index.md` (path
`knowledge/tutorials/index.md`). Verify:
`git show HEAD:knowledge/tutorials/index.md | grep -c "evals"` ≥ 1 and
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/14_wrapup.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
Markdown only; no code, runs or LLM calls; every number from `results.md`. Context budget ≈ 50k tokens.
Do not run `fleet serve restart` or `fleet run`.
