**Figure 1 — Technical summary**

**What it shows:** A system-architecture (block/connectivity) diagram of the *Prime Agent* harness, not a data plot. It depicts five nodes and the links between them: a **Human** operator feeding an **Agents View** panel; a **Root session** (a REPL/`>_` node) that is the central hub; a **Subagents** node (a group of three REPL sessions); and an **Environment** node. Beneath these sit two dashed-state components, a **Daemon** (database store) and a **Continual Harness** (loop/refresh icon).

**Axes / trends:** None — this is a schematic, so there are no coordinate axes, scales, or plotted trends. The "structure" is instead the topology of connections, with a two-way (solid) path Human → Agents View ↔ Root session ↔ Subagents ↔ Environment, and a persistent-state layer (Daemon ↔ Continual Harness) tied in via dashed arrows from the Root session and to the Subagents.

**Encoding convention:** Per the caption, **solid arrows** carry execution and messages (e.g., the `rlm()` call and `message` return between Root session and Subagents), while **dashed arrows** carry persistent state (session ↔ Daemon ↔ Continual Harness).

**Takeaway:** The figure's point is *separation of concerns* in the runtime: a single persistent **root session** orchestrates work and spawns parallel **subagent** sessions to act on the environment, while all durable state is offloaded to a **daemon + continual harness** so that context can be compacted, detached, or restarted without losing it. In short, it illustrates Prime Agent's split between live execution/message flow (solid) and durable state (dashed), with the root session as the coordination hub.

*(Note: the diagram contains no quantitative values, so no approximate figures are involved.)*