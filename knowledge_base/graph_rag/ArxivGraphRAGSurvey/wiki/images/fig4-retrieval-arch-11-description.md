**Figure 4 — "The general architectures of graph-based retrieval": a schematic pipeline (not a quantitative chart)**

**What it shows.** This is a left‑to‑right block/flow diagram (a conceptual architecture, not a data plot), so it has *no numeric axes and no trends*; the "x‑axis" equivalent is the sequence of processing stages, and the "y‑dimension" is the set of sub‑topics each stage covers. The pipeline begins with an **Input Query** and a **Graph Database**, passes through four annotated stage boxes (cross‑referenced to survey sections §6.1–§6.4), and ends at a post‑retrieval enhancement stage.

**Stage flow (the diagram's structure).**
1. **Query Enhancement (§6.4.1):** query expansion and query decomposition applied to the input before retrieval.
2. **Retrieval Granularity (§6.3):** the unit of retrieval — nodes, triplets, paths, subgraphs, or a hybrid.
3. **Retriever + Paradigm (§6.1 / §6.2):** the retrieval engine (non‑parametric, LM‑based, or GNN‑based retriever) operating under a retrieval paradigm (once, iterative, or multi‑stage retrieval), shown as a stacked/overlapping box to indicate they are coupled choices.
4. **Knowledge Enhancement (§6.4.2):** post‑retrieval knowledge merging and pruning.

**Trends.** None — the figure is qualitative; arrows denote data/control flow rather than magnitude or direction of a measured variable.

**Takeaway.** Graph‑based (GraphRAG) retrieval is best understood as a modular pipeline with four independent design dimensions — *how the query is enhanced*, *what granularity is retrieved*, *which retriever and retrieval paradigm are used*, and *how retrieved knowledge is enhanced* — each mapping to a dedicated survey section. The figure's purpose is to provide a unifying taxonomy/roadmap for the retrieval discussion in §6, not to report experimental results. (Section numbers such as "§6.1" are structural references, not data values.)