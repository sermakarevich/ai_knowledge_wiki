**What the figure shows.** Figure 1 (SIGIR '24) is a schematic of a *retrieval‑augmented generation (RAG) pipeline built on a knowledge graph (KG) of customer‑service issue tickets*. It is a two‑panel process diagram, not a data plot, so it has **no axes, no quantitative trends, and no plotted numbers**; the only numerals are the step indices 1–6 and ticket IDs (e.g., ENT‑22970, PORT‑133061), which are identifiers rather than data values.

**Left panel — Knowledge Graph Construction.** Raw issue‑tracking tickets are turned into a graph database (Graph DB) plus a vector store:
- *Step 1 (intra‑ticket tree parsing):* each ticket node is expanded into child nodes for its Summary, Description, Fields (Priority, Root Cause, Impact Area), Comments, and Steps‑to‑reproduce, forming a per‑ticket tree.
- *Step 2 (inter‑ticket connections):* tickets are linked across the corpus via explicit `CLONE_FROM`/`CLONE_TO` edges and implicit `SIMILAR_TO` edges (derived from embedding similarity, "implicit EBR").
- *Step 3:* text embeddings of node values are written to a **Vector Database** for later retrieval.

**Right panel — Retrieval and Question Answering.** A natural‑language query is processed as:
- *Step 4 (LLM):* entity detection + intent classification, decomposing the query into key–value fields (Summary, Priority, Root Cause) and an intent (e.g., "Steps to Reproduce").
- *Step 5:* embedding‑based retrieval of candidate tickets followed by intent‑ and field‑based **filtering** to select the relevant sub‑graph.
- *Step 6 (LLM):* answer generation over the retrieved sub‑graph, producing the final answer (here, the reproduction steps for the cloned ticket).

**Takeaway.** The diagram's purpose is to show a *unified architecture* in which tickets are modeled as a structured knowledge graph (trees + clone/similarity edges) and stored both as graph nodes and as text embeddings; at query time, LLM‑driven parsing and filtering combine with embedding retrieval to ground the final LLM answer in a precise ticket sub‑graph. The intended benefit is more targeted, structure‑aware retrieval and explainable answers for customer‑service QA than flat vector search alone. (No performance numbers or trends are conveyed in this figure itself.)