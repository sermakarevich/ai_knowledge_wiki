**Figure 1 — Technical summary (schematic, not a data plot)**

**What it shows.** A side‑by‑side conceptual comparison of two ways to build a multi‑agent communication topology over time, illustrating the paper's motivation (node‑centric, prior work) versus its proposed method (group‑centric, "GoAgent"). There are no quantitative value axes; the only axis is a discrete time axis (t₁ → t₂ → t₃ → …, indicated by a rightward arrow) on which the topology is generated step by step.

**Panel (a) – Node‑centric paradigm (existing methods).** Left: an "Agent Pool" of ~6 individual agent nodes. A "Construct/Prune" step expands them into a graph that grows across t₁–t₃, with edges added node‑by‑node. A red shaded region marks the failure mode: *redundant edges / noise propagation*—uncontrolled, dense inter‑agent connections that let task‑irrelevant signals accumulate.

**Panel (b) – Group‑centric paradigm (ours).** Left: a "Group Pool" in which the same agents are pre‑clustered into role‑coherent groups (e.g., Code / Reason / Eval). Generation is *autoregressive* over groups rather than nodes: at each time step a whole group is selected and wired in. Arrows labeled "Restrict information flow" plus a green "Efficient Edge / Restrict Propagation" legend indicate that inter‑group communication is deliberately bottlenecked, limiting redundant message passing.

**Trend (qualitative).** Moving from (a) to (b), the topology goes from a dense, node‑level mesh (more edges, more noise) to a sparse, group‑level structure (fewer, more purposeful edges, constrained propagation).

**Takeaway.** Treating cohesive *groups* as the atomic unit of construction—rather than individual agents—preserves intra‑group collaboration while explicitly curbing inter‑group noise, yielding a more efficient communication topology than node‑centric edge prediction. (Exact node/edge counts are illustrative, not measured values.)