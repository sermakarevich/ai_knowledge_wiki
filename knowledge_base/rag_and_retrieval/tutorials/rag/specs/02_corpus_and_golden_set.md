# Task: chapter 02 — Corpus and golden set: parsers compared, chunk schema, golden questions, metrics, scoreboard

Read `specs/COMMON.md`, `index.md`, chapters 00–01 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).

## Problem
Every later chapter is an experiment that must be scored the same way. This chapter fixes the
evaluation contract: the parsed corpus (best parser), the chunk schema, the golden question set with
evidence, the metrics module and the scoreboard generator. Nothing here may change afterwards.

## Fix

### `project/src/rag_tutorial/parsers.py` + `just parse-compare`
Run three parsers on the same two papers (pick one with tables, e.g. RAPTOR or Best-Practices) and
compare: `pypdf` (already used), `pymupdf4llm` (Markdown with headings), Docling (`docling` package,
CPU; it downloads layout models on first run — allowed here, note the time). Table in the chapter:
seconds per paper, characters, number of `#` headings detected, whether a known table survived
(quote 5 lines of the same table from each). Note that `pymupdf4llm`/PyMuPDF are **AGPL-licensed** (copyleft — fine for a tutorial, a
consideration for commercial products; say so). Pick the winner for the corpus (expected: pymupdf4llm or
Docling); re-parse all 12 papers to `data/corpus/md/` with it; keep `<!-- page N -->` markers. Update
`corpus.parse` to use the winner (keep `--parser` option).

### `project/src/rag_tutorial/schema.py`
`Chunk(id, paper, section, text, start, end, meta)` and `Document(paper, title, text, sections)`
Pydantic models; `chunk_id(paper, start, end)` = first 16 hex of sha1. `Section` detection from `#`
headings (heading path like `"3 Method > 3.2 Retrieval"`).

### `project/src/rag_tutorial/golden.py` (Typer CLI: `generate`, `review`, `stats`) + `data/golden/qa.jsonl`
- `generate`: for each of the five types create candidate questions with `qwen3.8:27b` using
  structured output (JSON schema): single_hop (12; from one random ~800-token passage each, question
  must be answerable from that passage alone and *specific* to the paper), multi_hop (10; from two
  passages of two different papers; the question must need both), comparative (6; "how does X in
  paper A differ from Y in paper B"), global (6; from the list of paper titles + abstracts: "which
  papers address…", "what are the common themes…"), unanswerable (6; plausible but not in the corpus
  — e.g. about a 2027 result, or a different field). Each item: `id, type, split, question, answer,
  evidence: [{paper, quote}]` where `quote` is a verbatim ≤ 300-character span from the source
  passage (verify with exact substring match after whitespace normalisation; drop candidates that
  fail). Assign `split`: every 4th item `dev`, others `test`.
- `review`: prints each item with its evidence for a human pass. **You are the reviewer**: read all
  ~40, delete or edit bad ones (trivial, ambiguous, wrong answer, evidence not supporting), and write
  a short paragraph in the chapter about what you removed and why (with two examples). Final size:
  36–44 questions.
- `stats`: counts per type/split, mean question length, papers covered.

### `project/src/rag_tutorial/evaluate.py` (the shared evaluator)
- `retrieval_metrics(retrieved_chunks: list[Chunk], evidence: list[Evidence], ks=(5,10))`: a chunk is
  relevant if it contains ≥ 80 % of an evidence quote's tokens (fuzzy containment after normalisation;
  implement with token sets and also exact normalised-substring; document the choice). Returns
  hit@k, recall@k (fraction of evidence quotes covered), MRR, nDCG@10.
- `judge_correctness(question, reference, answer) -> {score: 0|0.5|1, reason}` and
  `judge_faithfulness(answer, contexts) -> {supported, total, score, unsupported_claims}` (split the
  answer into atomic claims with the LLM, then check each claim against the contexts; RAGAS-style),
  both via `Ollama.chat` with JSON schema, temperature 0. For `unanswerable` questions correctness is
  replaced by **abstain**: 1 if the answer says it cannot be answered from the documents.
- `evaluate_run(name, chapter, answer_fn, retrieve_fn, split="test") -> metrics.json` writes the
  files described in COMMON.md; the `answer_fn` receives the question and returns
  `(answer, contexts, n_llm_calls)`; time each question. Also `--limit` for smoke runs.
- `scoreboard.py`: collect all `runs/*/metrics.json` → `runs/scoreboard.md` (Markdown table with the
  columns from `index.md`, sorted by chapter then name; anchors highlighted with **bold**) + `just scoreboard`.

### Anchors (run now, so chapter 03 can compare)
- `02_no_retrieval`: answer with the LLM only (prompt: answer briefly; if you don't know say so).
- `02_oracle`: give the LLM the evidence quotes (with paper names) as context.
Both on the test split. These two rows and their interpretation go in the chapter.

### Tests `project/tests/test_02_golden.py`
`chunk_id` deterministic; section path detection on a small Markdown; `retrieval_metrics` on a
hand-built case (known hit@k/MRR/nDCG values); the judge functions with `FakeLLM` returning canned
JSON; scoreboard renders from two synthetic `metrics.json`. No network.

### `02_corpus_and_golden_set.md` (chapter)
Parser comparison with real numbers and quoted table excerpts; why headings matter for chunking; the
chunk schema and why ids must be deterministic; how the questions were generated (prompts shown), the
review pass (what was removed), the final stats table and three example questions per type; the
metric definitions with the worked example on one real question; the judge prompts and their
limitations; the two anchor rows with interpretation (the no-retrieval model will answer some
questions from memory — discuss what that means for the benchmark). Troubleshooting; Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{parsers,schema,golden,evaluate,scoreboard,corpus}.py`,
`project/pyproject.toml`, `project/uv.lock`, `project/justfile`, `project/data/corpus/md/*.md`,
`project/data/golden/qa.jsonl`, `project/data/cache/**`, `project/runs/{02_no_retrieval,02_oracle}/**`,
`project/runs/scoreboard.md`, `project/tests/test_02_golden.py`, `02_corpus_and_golden_set.md`.
Verify token `"What you will learn"`.

## Scope & constraints
No chunker/retriever beyond what `golden.py` needs internally (a simple ~800-token window sampler).
After this task `data/golden/qa.jsonl` and `evaluate.py` metric definitions are frozen for all later
chapters (bug fixes allowed, must be mentioned in the chapter that makes them and the anchors re-run).
