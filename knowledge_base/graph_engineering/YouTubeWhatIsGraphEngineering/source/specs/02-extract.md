# Task: write wiki page 02 — Graph Engineering vs GraphRAG

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

**Input (read this exact file, nothing else):**
`/Users/sergii/.kb/papers/YouTubeWhatIsGraphEngineering/source/chunks/02.txt`

This is a transcript segment (timestamps `[04:15-06:23]`) from the YouTube video "What Is Graph Engineering?" by KGP Talkie. It explains why graph engineering and GraphRAG (retrieval-augmented generation over a knowledge graph) are NOT the same thing, despite both using the words "node" and "edge/relationship": in GraphRAG, nodes represent static things (entities/facts) that take no action, and edges are relationships only — no data flows along them. In graph engineering, nodes take action (they can be agents, parts of a loop, or direct LLM calls), and data actively flows from node to node along the edges/relationships.

**Output (write exactly this file; if it already exists — a retry — overwrite it completely):**
`/Users/sergii/.kb/papers/YouTubeWhatIsGraphEngineering/wiki/02-graph-engineering-vs-graphrag.md`

**Write the page using exactly this structure:**

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph Engineering vs GraphRAG

**In one sentence:** <one sentence stating the core distinction between graph engineering and GraphRAG>

## Key points

- <5-8 bullets, each a complete standalone claim — cover: superficial similarity (both use "node" and "edge/relationship" vocabulary), GraphRAG nodes represent static things and take no action, graph-engineering nodes take action and can be agents/loop-parts/direct LLM calls, GraphRAG edges denote relationship only with no data flow, graph-engineering edges carry data flowing from node to node, and the conclusion that GraphRAG cannot be equated with graph engineering>

---

## Surface-level similarity

<both frameworks use "node" and "edge"/"relationship" terminology, which invites confusion>

## The actual distinction

### Nodes: passive things vs action-taking components

<GraphRAG nodes represent entities/things and take no action; graph-engineering nodes can act — they may be agents, parts of a loop-engineering solution, or a direct LLM call>

### Edges: relationship-only vs data-carrying

<GraphRAG edges express relationship with no data flowing between nodes; graph-engineering edges carry data that actively moves from one node to the next>

## Why this matters

<the practical implication: graph engineering is an execution/orchestration structure, while GraphRAG is a knowledge-representation/retrieval structure — conflating them misdescribes what each is for>

---

**Covers:** 04:15-06:23
```

**Scope:** touch ONLY the one output file listed above. Do not run any fleet commands other than `bd close`.

**DoD:** output file written → `bd close <own-id> --reason "chunk 02 extracted"`. No git commands — `.kb` auto-syncs.
