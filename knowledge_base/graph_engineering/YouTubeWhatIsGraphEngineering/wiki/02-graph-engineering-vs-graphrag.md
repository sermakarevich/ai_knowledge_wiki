> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph Engineering vs GraphRAG

**In one sentence:** GraphRAG and graph engineering both use nodes and edges, but GraphRAG nodes are static things that represent entities and take no action while its edges carry no data, whereas graph-engineering nodes actively take action (agents, loop parts, direct LLM calls) and data flows along the edges from node to node.

## Key points

- Both graph engineering and GraphRAG use the vocabulary of "node" and "edge"/"relationship", which makes the two frameworks look superficially similar.
- In GraphRAG, nodes represent things/entities — they represent something static and take no action at all.
- In graph engineering, nodes take action: a node can be an agent, multiple agents forming part of a loop, or even a direct LLM call.
- In GraphRAG, edges (relationships) only tell about the relationship between nodes; there is no data flowing between them.
- In graph engineering, data actively flows from one node to another node along the relationships/edges.
- Together, the passive nodes and data-less edges of GraphRAG mean it fundamentally differs from the action-taking, data-carrying structure of graph engineering.
- Consequently, GraphRAG cannot be equated with graph engineering, despite the shared node/edge terminology.

---

## Surface-level similarity

Both frameworks use the same vocabulary: each has **nodes** and **edges** (relationships). GraphRAG has nodes and edges, and graph engineering also has nodes and relationships/edges. This shared terminology — same words for the same-shaped components — is what invites the confusion that the two are the same thing.

## The actual distinction

### Nodes: passive things vs action-taking components

In GraphRAG, the nodes are actually **things**: they represent something (entities, facts) and they are **not taking any action**. In graph engineering, by contrast, the nodes **take action**. A node can be an agent, can be part of the loop (multiple agents in a loop), or can be a direct LLM call. So where GraphRAG nodes are static representatives of things, graph-engineering nodes are active components that do work.

### Edges: relationship-only vs data-carrying

In GraphRAG, the relationships/edges are **just telling about the relationship** between nodes — no data flows between them at all. In graph engineering, **data is flowing**: it goes from one node to another node using these relationships. So GraphRAG edges are descriptive links, while graph-engineering edges are conduits over which data actively moves.

## Why this matters

Graph engineering is an **execution/orchestration structure**: nodes act and data moves through the graph. GraphRAG is a **knowledge-representation/retrieval structure**: it stores things and the relationships between them, with no execution and no data flow. Conflating them misdescribes what each is for — GraphRAG is not a way of executing or orchestrating, it is a way of representing and retrieving knowledge, which is precisely why "graph RAG" cannot be called graph engineering.

---

**Covers:** 04:15-06:23
