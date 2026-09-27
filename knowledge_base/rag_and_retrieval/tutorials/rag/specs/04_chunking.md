# Task: chapter 04 — Chunking strategies and the small-to-big / contextual tricks

Read `specs/COMMON.md`, `index.md`, chapters 00–03 (esp. the failure analysis in 03) first
(cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`). Research: `specs/research/models_eval_papers.md` Part 5,
`systems_and_infra.md` Part 3.

## Problem
Chunking decides what can be retrieved at all. Chapter 03 showed evidence cut at chunk boundaries and
context-less chunks. This chapter implements the common strategies and measures them with the
baseline retriever (dense top-5, same prompt) so only chunking changes.

## Fix

### `project/src/rag_tutorial/chunkers.py` — extend the registry
- `fixed` (exists), `recursive` (split on `\n\n`, `\n`, sentence, word — LangChain's recursive idea,
  implemented ourselves in ~40 lines), `sentence` (n sentences per chunk with `k`-sentence overlap,
  simple regex sentence splitter), `markdown` (split on heading boundaries first, then `fixed` inside
  long sections; every chunk text is prefixed with a **contextual header** line
  `"<paper title> — <section path>"`), `semantic` (embed sentences, break where cosine similarity to
  the previous window drops below a percentile threshold — the "semantic chunking" idea; uses the
  cached embedder), `parent_child` (children of 128–200 tokens for retrieval, parent of ~800 tokens
  returned as context — needs a `parent_id` in `meta` and a retriever that swaps child → parent and
  deduplicates), `sentence_window` (index single sentences, return the sentence ± 3 neighbours),
  `contextual` (Anthropic-style contextual retrieval: for every `markdown` chunk ask the LLM for a
  2–3 sentence context of where the chunk sits in the document — the prompt gets the paper abstract +
  section path + chunk — prepend it to the text before embedding; ≈ 600–900 LLM calls, run once
  behind `just gpu-check`, cached).
- For **late chunking** write a clear explanation in the chapter and a ≤ 30-line demo with
  `sentence-transformers` on CPU using a long-context model that exposes token embeddings
  (`jinaai/jina-embeddings-v2-small-en`, see research), applied to one paper; do not evaluate it on
  the scoreboard unless it fits in time — say what you did.
- Every chunker returns `list[Chunk]` with `meta` (`strategy`, `size`, `parent_id`, `window`, …).

### `project/src/rag_tutorial/retrievers.py` (introduced here, extended later)
`DenseRetriever(store, embedder, k)`, `ParentChildRetriever`, `SentenceWindowRetriever` — each with
`retrieve(question) -> list[Chunk]` (the chunks handed to the prompt) and `retrieved_ids()` for the
metrics. Note: retrieval metrics are computed on the chunks *handed to the prompt* (parents/windows),
so the evidence-containment rule from chapter 02 still applies.

### Experiments (`just chunking-eval`, all `test` split, dense top-5, baseline prompt)
`04_fixed_256`, `04_fixed_512` (= 03 baseline, reuse), `04_fixed_1024`, `04_fixed_512_ov128`,
`04_recursive_512`, `04_sentence_5`, `04_markdown_512`, `04_semantic`, `04_parent_child`,
`04_sentence_window`, `04_contextual_512`. Also write `runs/04_chunk_stats.json` (chunks per
strategy, mean/median tokens, index seconds).

### Tests `project/tests/test_04_chunking.py`
Each chunker covers the whole document text (concatenated children ⊇ original modulo whitespace and
headers); `markdown` chunks start with the header line; `parent_child` children point to existing
parents; `semantic` with `FakeEmbedder` returns ≥ 2 chunks on a two-topic text; `sentence_window`
returns the window. No network.

### `04_chunking.md` (chapter)
Why chunking matters (embedding one vector per chunk = one "meaning" per chunk); each strategy with
a small diagram or example on a real paragraph of one paper (show the actual chunk boundaries);
the trade-off triangle (precision of retrieval vs completeness of context vs cost); the chunk stats
table; "What changed on the scoreboard" (all rows, the anchors, interpretation: which failure classes
from 03 moved); the cost of contextual retrieval in LLM calls and minutes vs its gain; guidance
("start with markdown-aware 400–600 tokens + small-to-big; add contextual headers for free");
Troubleshooting; Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{chunkers,retrievers}.py`, the CLI you add
(`project/src/rag_tutorial/chunking_eval.py`), `project/pyproject.toml`, `project/uv.lock`,
`project/justfile`, `project/data/cache/**`, `project/runs/04_*/**`, `project/runs/scoreboard.md`,
`project/tests/test_04_chunking.py`, `04_chunking.md`. Verify token `"What you will learn"`.

## Scope & constraints
Only dense retrieval + the baseline prompt; no reranking/hybrid here. Do not modify `evaluate.py`
metric definitions or `prompts.py`.
