# Task: Extract wiki page 02 — Knowledge Graph Method

## Context is tight on this model

Read ONLY this spec and the two input files listed below. Nothing else. Do NOT read this
task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`,
`task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read any sibling wiki page
"for style/reference" — the format contract below is the only convention you need.

If this is a retry: do not try to diagnose the previous failure by reading logs. Just
re-read the input files and write the output directly.

## Input

1. Read this file in full (the main text — pages 3-4 through Section 3.2.3):
   `/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/source/chunks/02.txt`

   It covers: Section 3 (Methods) overview, 3.1 Knowledge Graph Construction (graph structure
   definition — intra-issue tree + inter-issue graph with explicit/implicit edges; the
   two-phase construction algorithm with formulas; embedding generation), and 3.2 Retrieval
   and Question Answering (query entity/intent extraction, embedding-based sub-graph
   retrieval with the scoring formula, LLM-driven Cypher query generation, answer generation).

2. Read this vision-model description of Figure 1 (the paper's main architecture diagram),
   already generated for you — do not try to view the image yourself:
   `/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/wiki/images/01-description.md`

## Output

Write the full page to:
`/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/wiki/02-knowledge-graph-method.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Knowledge Graph Method

**In one sentence:** <the whole mechanism of this chunk in one sentence>

## Key points

- <complete-claim bullet with real content — e.g. name the two-level graph structure,
  the explicit vs implicit edge types, the retrieval scoring approach, the Cypher
  translation step>
- <5-8 bullets total>

---

## Knowledge Graph Construction

<hierarchical summary of 3.1.1 Graph Structure Definition (intra-issue tree T_i, inter-issue
graph G, explicit Eexp vs implicit Eimp edges, the ENT-22970 worked example), 3.1.2 Knowledge
Graph Construction (rule-based + LLM-based hybrid parsing, the formulas for T_i / Eexp / Eimp),
and 3.1.3 Embedding Generation (BERT/E5 embeddings, QDrant vector DB, chunking within a section)>

![Figure 1: overview of the RAG + knowledge graph framework](images/01-figure1-overview.png)

<a paragraph describing what Figure 1 shows, based on the vision description file — explain
both panels: knowledge graph construction (left) and retrieval/QA (right)>

## Retrieval and Question Answering

<hierarchical summary of 3.2.1 Query Entity Identification and Intent Detection (the P/I
extraction, the login-issue worked example), 3.2.2 Embedding-based Retrieval of Sub-graphs
(EBR-based ticket identification with the scoring formula, LLM-driven subgraph extraction
and the Cypher query example), and 3.2.3 Answer Generation (LLM as decoder, the fallback
mechanism)>

**Covers:** pages 3-4 (Section 3 Methods, through Section 3.2.3; Figure 1)
```

Rules:
- The `## Key points` bullets must be complete, standalone claims with real content
  (name the formulas/mechanisms, not "explains the method").
- The figure MUST be embedded exactly where shown above (right after the Knowledge Graph
  Construction subsection) using the path `images/01-figure1-overview.png` — this is a
  required figure reference; do not omit it or describe it without embedding.
- Preserve the two worked examples from the text (ENT-22970 ticket family; the login-issue
  query example) — they are the clearest illustrations of the mechanism.
- Be thorough; no line-count limit.

## Definition of done

1. Output file written at the path above, non-trivial (well over 40 lines), following the
   format contract, covering BOTH subsections 3.1 and 3.2 with the figure embedded.
2. Close this task: `bd close <own-id> --reason "chunk 02 extracted"`

## Scope

Touch ONLY the one output file listed above. Do not run any fleet command other than
`bd close` on your own task id. No git commands.
