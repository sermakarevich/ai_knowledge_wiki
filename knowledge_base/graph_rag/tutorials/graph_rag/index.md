# Graph RAG tutorial — from an unknown document to a queryable knowledge graph

A from-zero, hands-on tutorial on **Graph RAG** (Retrieval-Augmented Generation on a knowledge graph). Plain RAG cuts documents into chunks, embeds them as vectors and hands the most similar chunks to an LLM (Large Language Model). Graph RAG additionally asks an LLM to *read* the documents and extract **entities** (people, products, methods, …) and the **relationships** between them, stores them as a graph in **Neo4j**, and retrieves by walking that graph. The central problem this tutorial solves: *you are given documents you have never seen, and you want them inserted into a graph with sensible labels, relationship types and properties — automatically, repeatably, and without a hand-written schema.*

Everything runs locally: Neo4j 5 in Docker, `uv` (Python package manager), Python 3.12, a `justfile` (command runner like `make`), and open-weight models served by **Ollama** (a local LLM server).

Retrieve chapters with `ai show research_topics/graph_rag/tutorials/graph_rag/<chapter>`.

## Verified on
- Neo4j Kernel **5.26.29** (community edition, Docker image `neo4j:5`), plugins APOC and GDS (Graph Data Science) **2.13.12**.
- `neo4j` Python driver **6.3.0**.
- Ollama models: `qwen3.8:27b` (chat) and `nomic-embed-text` (embeddings), served at `http://127.0.0.1:11435`.
- Last verified: 2026-08-29.

## Quick start
```bash
cd project
just up && just sync      # start Neo4j, install Python deps
just pipeline              # ingest -> schema -> extract -> write-graph -> resolve -> embed -> communities
just ask q="how does GraphRAG differ from vector RAG?"
just ask-global q="what are the main open problems the survey identifies?"
```
`just pipeline` is cache-first: after the first real run (which makes hundreds of LLM calls and takes roughly two hours, see chapter 10), every stage's output is committed under `project/data/extracted/`, so re-running it costs almost nothing.

## Chapters (read in order)
- [00_setup.md](00_setup.md) — Neo4j (APOC + Graph Data Science) in Docker, `uv` project, Ollama models, `.env`, `justfile`, first LLM + embedding + Cypher call.
- [01_concepts.md](01_concepts.md) — what RAG is, why vector-only RAG fails on "connect-the-dots" questions, the Graph RAG pipeline end to end, the lexical graph vs the domain graph, the target schema of this tutorial, how the Microsoft GraphRAG paper fits.
- [02_documents_and_chunks.md](02_documents_and_chunks.md) — loading unknown files (Markdown, text, PDF), chunking strategies, `Document` and `Chunk` nodes with properties, `HAS_CHUNK` / `NEXT_CHUNK`, idempotent `MERGE`, constraints.
- [03_schema_discovery.md](03_schema_discovery.md) — "we don't know what is in the document": letting the LLM propose entity types, relationship types and properties from samples; reviewing and freezing the schema; open vs closed extraction.
- [04_extraction.md](04_extraction.md) — structured JSON extraction of entities and relationships per chunk (Pydantic schemas, Ollama JSON mode, prompts), validation, normalisation, caching results on disk.
- [05_writing_the_graph.md](05_writing_the_graph.md) — inserting extraction results into Neo4j: dynamic labels and relationship types, `MERGE` keys, properties and provenance (`MENTIONS` from chunks), batching with `UNWIND`, re-runs.
- [06_entity_resolution.md](06_entity_resolution.md) — the same thing under different names: normalisation, embedding similarity, LLM-as-judge, merging duplicate nodes with APOC, keeping aliases.
- [07_embeddings_and_vector_index.md](07_embeddings_and_vector_index.md) — embedding chunks and entities, Neo4j vector and full-text indexes, hybrid search.
- [08_retrieval_local_search.md](08_retrieval_local_search.md) — answering a question: vector hit → entities → graph neighbourhood → context assembly → LLM answer with citations; comparing against plain vector RAG.
- [09_communities_global_search.md](09_communities_global_search.md) — community detection (Leiden), community summaries, map-reduce answers to "what are the main themes?" questions.
- [10_updates_and_evaluation.md](10_updates_and_evaluation.md) — adding/changing/removing a document without rebuilding, a small evaluation set, cost/latency, pitfalls and a production checklist.

## Runnable project
`project/` — `docker-compose.yml`, `justfile`, `pyproject.toml`, `data/docs/*.pdf` (the input document), `data/extracted/` (cached LLM output so re-runs are instant), `src/graph_rag/` (one module per pipeline stage), `tests/`. Start with `cd project && just up && just check`.

## Local settings (shared by all chapters — never change these)
| setting | value |
|---|---|
| Docker image | `neo4j:5` with plugins `apoc` and `graph-data-science` |
| container name | `neo4j-graphrag` |
| browser UI | http://localhost:7477 (host **7477** → container 7474; 7474 + 7476 are used by other local Neo4j instances) |
| Bolt URI | `bolt://localhost:7690` (host **7690** → container 7687; 7687–7689 are used by other local Neo4j instances) |
| user / password | `neo4j` / `graphrag123` |
| Ollama URL | `http://127.0.0.1:11435` (a GPU box reached through an SSH tunnel; fallback `http://localhost:11434` = Ollama on this Mac) |
| chat / extraction model | `qwen3.8:27b` (set `think: false`, `temperature: 0`, JSON-schema `format`) |
| embedding model | `nomic-embed-text` (768 dimensions) |
| Python | 3.12 via `uv`, package `graph_rag` under `project/src/` |

All of these are read from `project/.env` (copy `project/.env.template`); `.env` is gitignored.

## The input document (the "unknown document")
`project/data/docs/graphrag_survey_2408.08921.pdf` — a real **41-page PDF**, the paper *"Graph Retrieval-Augmented Generation: A Survey"* (Peng et al., 2024, arXiv 2408.08921), copied from this knowledge base (`knowledge/research_topics/graph_rag/ArxivGraphRAGSurvey/source/`). It is long, unstructured, technical text that nobody has hand-labelled and that mentions dozens of methods, datasets, metrics and organisations — exactly the situation the tutorial is about: **one big document of unknown content goes in, a labelled graph comes out**. Every pipeline stage is run for real on this whole document, and the chapters show the real numbers (chunks, LLM calls, minutes, entities, duplicates). A second PDF (`project/data/docs_extra/graphrag_local_to_global_2404.16130.pdf`, 26 pages) is used in chapter 10 to demonstrate adding and removing a document. Any other `.pdf`, `.md` or `.txt` can be processed the same way: drop it into `project/data/docs/` and run `just pipeline`.

## Target graph schema (built up chapter by chapter)
Lexical layer (always the same, independent of content)
- `(:Document {id, path, title, sha256, ingested_at})-[:HAS_CHUNK]->(:Chunk {id, index, text, n_tokens, embedding})`
- `(:Chunk)-[:NEXT_CHUNK]->(:Chunk)`

Domain layer (labels and relationship types are *discovered* from the documents in chapter 03)
- `(:Entity:<Type> {name, normalized_name, description, aliases, embedding})` — every entity carries the generic `Entity` label plus a discovered type label such as `Method`, `Dataset`, `Organization`, `Metric`.
- `(:Entity)-[:<TYPE> {description, weight, chunk_ids}]->(:Entity)` — e.g. `IMPROVES_ON`, `EVALUATED_ON`, `PROPOSED_BY`.
- `(:Chunk)-[:MENTIONS]->(:Entity)` — provenance: which chunk an entity came from.
- `(:Community {id, level, summary, embedding})<-[:IN_COMMUNITY]-(:Entity)` — added in chapter 09.

Related reading in this knowledge base: `ai show research_topics/graph_rag/ArxivGraphRAGLocalToGlobal` (the Microsoft GraphRAG paper), `ai show research_topics/graph_rag/ArxivGraphRAGSurvey`.
