**Figure 2 — "Prime Agent state hierarchy"** is not a quantitative chart; it has no numeric axes or plotted trends. It is a schematic, four‑row hierarchy table that organizes the agent's state by *level of persistence and model visibility*, from the most fixed (bottom) to the most externally managed (top).

**What it shows (the vertical "axis"):** a stack of four levels, L0 → L3, each annotated with (a) the state it represents, (b) concrete examples of what lives there, and (c) the mechanism that updates it (right‑hand column).

- **L0 – Model Weights:** learned computation and prior knowledge → changed by **fine‑tuning**.
- **L1 – Active Context:** token‑visible working state for a single model invocation → changed by **compaction**.
- **L2 – REPL and Subagents:** code, tools, retained values, recursive session state → changed by **agentic garbage collection**.
- **L3 – Disk‑Backed State:** history, artifacts, memories, skills, prompts, subagent specs → changed by **refinement**.

**The dividing line:** a red dashed line labeled **MODEL‑CONTEXT BOUNDARY** sits between L1 and L2, separating token‑visible model state (L1 and below) from explicitly managed computation and retained state (L2 and above).

**Takeaway:** the figure's point is that each state layer is mutated by a *different, single* mechanism (fine‑tuning, compaction, agentic GC, refinement), and the model‑context boundary cleanly splits what the model sees as tokens from what the harness manages explicitly. There are no trends or approximate numeric values to report — the "structure" is the level ordering and the level‑to‑mechanism mapping itself.