**Figure 3 — "The overview of graph-based indexing" (schematic flow diagram)**

**What it shows:** A left‑to‑right pipeline diagram (not a quantitative plot) illustrating the components of graph‑based indexing. There are **no axes, no curves, and no numerical trends**; it is a structural/conceptual schematic.

**Structure (left → right):**
1. **Data Source** (input box): three input types — *Wikipedia*, *Text Corpus*, and *Tables*.
2. **§ 5.1 Graph Data** (middle box): the knowledge‑graph layer, split into *Self‑constructed Knowledge Graphs* and *Open Knowledge Graphs*, with the open category further divided into *General* and *Domain Knowledge Graphs*.
3. **Graph Database** (right, with a database icon): the stored, indexable graph store.
4. **§ 5.2 Indexing** (top‑right box): the indexing strategies that operate over the graph, listed as *Graph Indexing, Text Indexing, Vector Indexing,* and *Hybrid Indexing*, feeding into the graph database.

**Takeaway:** Graph‑based indexing is organized as a staged pipeline — raw heterogeneous sources (Wikipedia, text, tables) are transformed into knowledge graphs, persisted in a graph database, and made retrievable through four complementary indexing schemes (graph, text, vector, and their hybrid). The diagram's purpose is to map the paper's §5.1/§5.2 structure rather than to report measured results.