**Figure 6 — Multi-dimensional assessment of graph quality (radar/spider chart).**

- **What it shows:** A radar chart comparing six GraphRAG frameworks (MS‑GraphRAG, LightRAG, HippoRAG, HippoRAG2, Fast‑GraphRAG, and the proposed **MemGraphRAG**) on the topological quality of their index graphs. Each method is drawn as a colored polygon; the larger the enclosed area, the stronger the graph's structural properties.

- **Axes (six spokes):** two metrics — **Average Degree** (entity‑level connectivity) and **Average Clustering Coefficient** (local semantic cohesion / clustering) — measured on two domain datasets (**G‑Medical** and **G‑Novel**) plus a **HotpotQA** axis pair, giving six dimensions in total.

- **Trends:** The **MemGraphRAG** polygon (orange) forms the outermost, most expansive shape, extending farthest on most spokes — particularly on the average‑degree (connectivity) axes, where it reaches roughly the high single/low double digits (≈14 on G‑Medical, ≈9–10 on G‑Novel), and also on the clustering axes. The five baselines form smaller, more tightly packed inner polygons of varying shape, with HippoRAG2 being the next largest but still well inside MemGraphRAG. No single baseline dominates across all dimensions; each is outperformed by MemGraphRAG on at least several axes.

- **Takeaway:** MemGraphRAG produces index graphs that are simultaneously more connected (higher average degree) and more locally clustered (higher clustering coefficient) across both medical and novel domains, indicating a denser, more coherent, and better‑structured knowledge graph than existing GraphRAG methods. In short, it integrates dispersed knowledge into a more unified, high‑connectivity structure rather than a sparse, loosely linked one.

*(Exact axis values are approximate, as read from the chart.)*