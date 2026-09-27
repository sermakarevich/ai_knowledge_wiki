# Task: chapter 01 — Concepts: what RAG is, the anatomy of a RAG system, the open-source landscape, how we measure

Read `specs/COMMON.md`, `index.md`, `00_setup.md` and all three files in `specs/research/` first
(cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).

## Problem
The reader needs the mental model before the experiments: why RAG exists, what its stages are, what
the open-source landscape looks like (this is the *overview* half of the tutorial's purpose), and
how this tutorial will judge everything. This is a mostly-prose chapter with two small runnable demos.

## Fix

### `project/src/rag_tutorial/demo_concepts.py` (Typer CLI, `just demo-concepts`)
1. **Why retrieval**: ask `qwen3.8:27b` three questions whose answers are in our corpus and are
   unlikely to be memorised precisely (e.g. "In the RAPTOR paper, what accuracy did GPT-4 reach on
   QuALITY with RAPTOR?"; "How many failure points does the 'Seven Failure Points' paper list and name
   two"; "What is the value of k in Reciprocal Rank Fusion used by …") — first without context, then
   with the one relevant paragraph pasted (find it by hand with grep in `data/corpus/md/`). Print
   both answers side by side; the chapter shows them verbatim.
2. **What an embedding is**: embed six short sentences (two pairs about the same thing in different
   words, two unrelated) with `nomic-embed-text`; print the cosine-similarity matrix with `rich`.
3. **Tokens and context**: print token counts of one paper, the whole corpus, and Ollama's
   configured context (`num_ctx` we use = 16,384; the server allows up to 98,304) — to motivate why
   "just paste everything" does not scale (and later chapter 13 revisits long-context vs RAG).

### `01_concepts.md` (chapter; the main deliverable, 350–500 lines)
Sections:
1. **The problem RAG solves** — knowledge cutoff, private data, hallucination, citations; the two
   demo outputs.
2. **Anatomy of a RAG system** — mermaid diagram: documents → parse → chunk → embed → index (vector +
   keyword) → [query → rewrite → retrieve → rerank → assemble context] → generate → cite → evaluate;
   one paragraph per stage naming the knobs that later chapters turn (chapter numbers as links).
3. **Retrieval basics in plain words** — sparse (BM25: term frequency, IDF) vs dense (embeddings,
   cosine), why both; approximate nearest neighbour (HNSW) in one paragraph; top-k and why "more
   context" is not free (lost in the middle, cite the paper in our corpus).
4. **The open-source landscape** — a table with four rows of *kinds* (orchestration libraries; RAG
   engines/frameworks with their own pipeline model; end-user apps with UI; retrieval infrastructure)
   and then one table per kind listing the concrete projects from the research notes (license, GitHub
   stars/date, what it is best at, main drawback, chapter where we try it or "survey only"). Include
   Microsoft GraphRAG with a pointer to `../graph_rag/index.md`. Be honest about what "free" means
   (open-source core + paid cloud: LangSmith, LlamaCloud, Qdrant Cloud, …).
5. **RAG vs long context vs fine-tuning** — when each wins; costs; link `../llm_training/index.md`.
6. **How this tutorial measures** — the golden set kinds, retrieval metrics (hit@k, recall@k, MRR,
   nDCG — each with a two-line definition and a tiny worked example), answer metrics (LLM-judge
   correctness and faithfulness — what the judge sees; its known biases), cost columns, the three
   anchors. Explain why every experiment must use the same chunk-id scheme.
7. **A first pros/cons view** — five bullets each for "RAG in general".
Troubleshooting (mostly conceptual misunderstandings: "the model still hallucinates", "retrieval
found the right chunk but the answer is wrong", …). Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"` (add `tests/test_01_concepts.py`: the cosine
matrix function is symmetric with ones on the diagonal, using `FakeEmbedder`).

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/demo_concepts.py`, `project/tests/test_01_concepts.py`,
`project/justfile`, `project/data/cache/**` (new entries), `01_concepts.md`. Verify token
`"What you will learn"`.

## Scope & constraints
No indexing code yet. Do not change `llm.py` except for bug fixes (say so in the chapter).
