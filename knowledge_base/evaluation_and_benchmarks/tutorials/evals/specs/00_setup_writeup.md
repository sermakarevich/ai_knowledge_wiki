# Task: chapter 00 writeup — Setup chapter (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/00_findings.md`, `project/justfile`,
`project/src/evals_tutorial/llm.py` (skim for the cache design), and — for style only — the first 120
lines of `../rag/00_setup.md`. Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Chapter 00's code exists (previous task); the chapter that explains it does not.

## Fix
Create `00_setup.md`: `# 00 — Setup: project skeleton, cached Ollama client, GPU check`, "## What you
will learn"; explain every tool (uv, just, Docker — used only in chapter 13, Ollama, the SSH tunnel and
why the LLM is on another machine); the `project/` tree with one line per file; the cache design (why
caching makes the tutorial reproducible and free to re-run, what the key contains, how to invalidate,
`chat_json` and why structured output matters for evals); the GPU-sharing rule; the three public dataset
files and their licences (from `project/data/public/README.md`); the real `just check` output; a
**"Verified on"** table (Ollama version, model digests, Python and package versions — all from the
findings note); one mermaid diagram (Mac ↔ tunnel ↔ rtx). Troubleshooting (tunnel down; model being
loaded so first call is slow; GPU busy; `uv sync` behind a proxy). Exercises. `Next:` line → chapter 01.

## Tests
`test -s 00_setup.md && grep -c "What you will learn" 00_setup.md && grep -ci troubleshooting 00_setup.md && grep -ci exercises 00_setup.md`

## DoD
As in COMMON.md. Commit: `00_setup.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/00_setup.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code changes, no experiments. Every number/version comes from the findings note. Do not edit
`index.md`. Context budget ≈ 35k tokens. Do not run `fleet serve restart` or `fleet run`.
