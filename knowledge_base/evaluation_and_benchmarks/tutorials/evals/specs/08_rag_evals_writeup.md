# Task: chapter 08 writeup — RAG evals (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/08_findings.md`, `project/runs/08_agreement.md`,
`project/runs/results.md`, `project/src/evals_tutorial/rag_evals.py` (excerpts), `research/SOURCES_tools.md`
(RAGAS and DeepEval entries only), and — for style only — `07_statistics.md`. Nothing else
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Retrieval metrics, RAGAS and DeepEval ran (previous task); the chapter does not exist.

## Fix
Create `08_rag_evals.md` (`# 08 — RAG evals: …`, "## What you will learn"): RAG in one paragraph and the
two places it fails; retrieval metrics explained with a worked example on one ticket (hit@k, recall@k,
precision@k, MRR, nDCG — each with a one-sentence definition), the table with CIs and the recall@k curve;
the retrieval-vs-generation split and what it says about where to work next; the RAGAS triad (Es et al.
2023, arXiv 2309.15217) — what each metric asks the judge, the Ollama wiring code excerpt, the results,
cost per item and every rough edge you hit; the same in DeepEval with its wiring excerpt; the agreement
table: do RAGAS, DeepEval, embedding similarity and our aligned judge agree with the labels, with the
two counter-example tickets; the honest conclusion (library metrics are unaligned judges — chapter 05's
alignment loop applies to them too). Mermaid: ticket → retrieve → gold sections check / generate →
faithfulness. "What landed in the results table". Two "Advantages and disadvantages" tables (RAGAS,
DeepEval). Troubleshooting (NaN faithfulness → statement extraction failed; DeepEval login/telemetry;
slow → too many calls per item); Exercises (add a context-recall metric; score answer_v2 with RAGAS
on the same 30); `Next:` → chapter 09.

## Tests
`test -s 08_rag_evals.md && grep -c "What you will learn" 08_rag_evals.md && grep -ci "ragas" 08_rag_evals.md && grep -ci "advantages and disadvantages" 08_rag_evals.md`

## DoD
As in COMMON.md. Commit: `08_rag_evals.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/08_rag_evals.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
