# Task: chapter 14 — Wrap-up: consistency pass, Q&A, README, tutorials index

Read `specs/COMMON.md`, `index.md`, ALL chapters 00–13, `project/runs/scoreboard.md` and
`project/runs/scoreboard_analysis.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).

## Problem
Fourteen chapters were written by different workers over several days. The tutorial needs one
consistency pass, a verified quick start, the "Verified on" table filled, a Q&A page, and an entry in
the tutorials index so `ai show research_topics/rag_and_retrieval/tutorials/rag` finds it.

## Fix
1. **Quick start really works**: from a clean clone state (`rm -rf project/.venv project/data/indexes`
   only — never delete caches or runs), run `cd project && just sync && just check && just scoreboard`
   and `uv run pytest tests/ -q -m "not slow"`; fix whatever breaks (minimal edits; list them in the
   commit message). Record the timings.
2. **Consistency pass over every chapter**: headings follow `# 0N — Title`; each has "What you will
   learn", "Troubleshooting", "Exercises", cross-links to previous/next; experiment names in the
   prose match `runs/`; every number quoted in a chapter exists in a `metrics.json`/`*.json` (spot-check
   at least 3 numbers per chapter and fix mismatches); abbreviations explained on first use per chapter;
   no leftover "TODO"/"UNVERIFIED" in chapters (research notes may keep theirs). Keep edits minimal —
   this is not a rewrite.
3. **`index.md`**: fill the "Verified on" pointer, make the chapter one-liners match what the
   chapters actually contain, add a short **"Results at a glance"** section: the final scoreboard's
   top 8 rows + the three anchors (copy from `runs/scoreboard.md`) and five one-line takeaways from
   `scoreboard_analysis.md`. Fix the corpus/golden set table with the real numbers (papers, pages,
   question counts per type).
4. **`Q&A.md`**: create it with 8–12 questions a reader is likely to ask (e.g. "Which framework
   should I start with?", "Why is my hybrid search worse than dense?", "How do I add my own
   documents?", "How much does it cost to re-run everything from scratch without the cache?") answered
   from the chapters, with links.
5. **`project/README.md`**: one page — what the project is, quick start, the `just` recipe list with
   one line each, the layout, how to add a new experiment (the `evaluate_run` contract), how the cache
   works, the Docker profiles and ports.
6. **`../index.md`** (tutorials index, `/Users/sergii/.ai/knowledge/tutorials/index.md`): add under
   "Machine learning & LLMs" a line:
   `- [rag/index.md](rag/index.md) — RAG from zero, hands-on: open-source frameworks (LangChain/LangGraph, LlamaIndex, Haystack, DSPy), systems (LightRAG, RAGFlow, Open WebUI), vector stores and rerankers compared on one corpus and one scoreboard; chunking/hybrid/reranking/query-rewriting tricks measured; evaluation with a local judge and RAGAS; production checklist.`
   Also confirm `ai show research_topics/rag_and_retrieval/tutorials/rag` and `ai show research_topics/rag_and_retrieval/tutorials/rag/13_evaluation_and_production` work.
7. Stop all Docker profiles (`just down qdrant`, etc.) at the end.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md, plus: commit `index.md`, `Q&A.md`, `project/README.md`, every chapter file you edited
(by path), `../index.md`, and any small code fixes (by path). Verify token for this task:
`git show HEAD:knowledge/tutorials/index.md | grep -c "rag/index.md"` ≥ 1. `bd close`.

## Scope & constraints
No new experiments, no new dependencies. Do not delete or rewrite chapters; do not touch
`../llm_training/**` or other tutorials.
