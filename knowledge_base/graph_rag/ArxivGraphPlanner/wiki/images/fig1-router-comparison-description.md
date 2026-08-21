**Figure 1 — Comparison of three LLM routing architectures (schematic, no quantitative axes).**

The figure is a conceptual diagram, not a data plot; it has no axes or numerical trends. It contrasts three routing strategies as flowcharts of how a query is turned into a response.

- **Single‑round router (top‑left):** A query *q* is passed to a router *R_single*, which selects one model from a backbone pool; that model directly emits the final response *oₜ*. The decision depends only on the current query, with no history or collaboration.

- **Multi‑round router (top‑right):** The query is processed in a sequence of rounds. Each round selects a model and produces an intermediate output (*o₁*, …), and the accumulated context is fed back so that *R_multi* makes the next selection, ultimately yielding *oₜ*. It is contextual but still a flat, sequential chain.

- **Agentic router (bottom, ℱ_workflow):** A *Planner* first decomposes the query into a workflow graph of sub‑tasks (colored nodes *o₁*… *oₜ₋₁*). Each sub‑task is assigned to an *Executor* (some performing specialized or iterative work, indicated by the sparkle and loop icons). At step *t*, *R_agentic* jointly chooses both the **agent role** and the **model**, and a *Summarizer* integrates the branch outputs into the final response. This layer adds explicit role assignment and task decomposition on top of model selection.

**Takeaway:** The three designs differ in the information used to route. Single‑round routing is query‑only and fast but cannot decompose or coordinate; multi‑round routing adds historical context but remains a sequential, single‑track decision; the agentic router introduces a workflow memory graph so that the system jointly selects *which role* and *which model* at each step, enabling explicit multi‑LLM collaboration and task decomposition that the other two lack.