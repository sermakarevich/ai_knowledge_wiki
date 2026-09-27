# Graph RAG project

A runnable Graph RAG (Retrieval-Augmented Generation on a knowledge graph) pipeline: turn an
unknown PDF into a labelled Neo4j graph, then answer questions from it. Built step by step in
`knowledge/research_topics/graph_rag/tutorials/graph_rag/00_setup.md` through `10_updates_and_evaluation.md` (read those for
the full explanation of every design decision below).

## Quick start

```bash
just up          # start Neo4j (Docker) and wait until healthy
just sync        # uv sync
just pipeline     # ingest -> schema-propose -> extract -> write-graph -> resolve -> embed -> communities
just ask q="how does GraphRAG differ from vector RAG?"
just ask-global q="what are the main open problems the survey identifies?"
```

`just pipeline` is cache-first end to end: after the first real run (which makes hundreds of LLM
calls against the two Ollama models and takes tens of minutes), every stage's output is cached under
`data/extracted/` and committed, so re-running `just pipeline` again costs almost nothing.

## Everyday commands

| command | what it does |
|---|---|
| `just ask q="..." mode=graph\|vector\|both` | answer a question via graph-grounded local search (chapter 08), a plain-RAG baseline, or both side by side |
| `just ask-global q="..."` | answer a whole-corpus question via community map-reduce (chapter 09) |
| `just add path="data/docs_extra/foo.pdf"` | add one new document without rebuilding anything else (chapter 10) |
| `just remove path="..."` / `just update path="..."` | remove or re-sync one document (chapter 10) |
| `just evaluate` | LLM-as-judge evaluation over `data/questions.json` (chapter 10) |
| `just stats` | node/relationship/community counts for the graph currently in Neo4j |
| `just test` | run the pytest suite against the running Neo4j |
| `just down` | stop Neo4j, keep its data |

## Layout

- `docker-compose.yml`, `justfile` — infrastructure and every command above.
- `data/docs/` — the input PDF; `data/docs_extra/` — a second PDF used only in chapter 10's demo.
- `data/extracted/` — every cached LLM (Large Language Model) output: schema, per-chunk extractions,
  resolution judgements, community reports, evaluation runs. Committed to git on purpose.
- `src/graph_rag/` — one module per pipeline stage; see the chapters for why each exists.
- `tests/` — one file per chapter, run against the live Docker Neo4j.

Chapters: [`knowledge/research_topics/graph_rag/tutorials/graph_rag/index.md`](../index.md).
