**Figure 5 — "The overview of graph-enhanced generation."**

**What it shows.** A conceptual (schematic) pipeline, not a quantitative plot. It maps the *generation* stage of a Graph‑Retrieval‑Augmented Generation (GraphRAG) system, organized under section §7.3 "Generation Enhancement." The diagram is a left‑to‑right flow with three "enhancement" hooks mounted above it.

**Axes / trends.** There are no numeric axes, scales, or time series to read — the only "trend" is the directional data flow. Reading left to right:

1. **Input:** *Retrieval Results* (a small node‑edge graph icon) — the retrieved graph data that feeds generation.
2. **§7.2 Graph Formats:** the retrieved data is rendered into a generator‑compatible form via *Graph Languages* or *Graph Embeddings*.
3. **§7.1 Generators:** the formatted graph is consumed by a model class — *GNNs*, *LMs*, or *Hybrid Models*.
4. **Output:** *Response* (light‑bulb icon) — the final generated answer.

Overlaid on this main path are three purple "enhancement" stages that intervene at different points: *Pre‑Generation Enhancement* (before/at the format step), *Mid‑Generation Enhancement* (during generation), and *Post‑Generation Enhancement* (refining the response), each shown with a downward arrow into the pipeline.

**Takeaway.** Graph‑enhanced generation is a modular pipeline in which retrieved graph data is first *formatted* (graph languages/embeddings), then *decoded* by a suitable generator (GNN, LLM, or hybrid), with optional *generation‑enhancement* techniques applied before, during, or after decoding to lift response quality. The selection of generator and enhancement depends on the downstream task (discriminative vs. generative), per the accompanying §7.1 text.

*(No exact numeric values are present in the figure; the §‑numbers above are the only labels and are reproduced as shown.)*