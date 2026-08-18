> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Lessons from Three Years of Building LangGraph

**In one sentence:** Three years of building production agents taught three lessons — agent graphs are usually not DAGs, loops are simply a basic form of graphs, and dynamic transition is essential.

## Key points

- Agent graphs are usually not DAGs: production agents inherently require cycles.
- Cycles are needed for retrying failed tool calls, asking users for missing information, revising answers after validation, repeatedly calling tools until there is enough context, and pausing for human input before resuming — looping is one of the core parts of agentic systems.
- Loops are simple graphs: loop engineering is not an alternative to graphs, but a simple version of them. As David Khorshid put it, a loop is merely a directed, cyclic graph — in fact, the LangChain framework, built on top of a simple agentic loop, is constructed on top of LangGraph.
- Dynamic transitions matter: we should not always predefine all edges in advance, because at runtime a node may decide how much work to generate.
- The Send mechanism is precisely for this purpose: it allows a node to dynamically route work to one or more downstream nodes without statically defining every transition — the classic case being map-reduce, where the number of workers depends on the input and cannot be known in advance.
- This is important because useful agent systems combine known structure with runtime variability — for example, knowing that a research task first fans out and then integrates, but not knowing how many sources exist in advance; or knowing that a supervisor delegates to workers, but not knowing which worker until the task begins. Graphs still need runtime flexibility.

---

## First: agent graphs are usually not DAGs

After 3 years of building agents with graphs, we learned that production agents require cycles: they retry failed tool calls, ask users for missing information, revise answers after validation, repeatedly call tools until there is enough context, and pause for human input before resuming. Because looping is one of the core parts of agentic systems, we should expect agent graphs to generally not be DAGs.

## Second: loops are simple graphs

Loop engineering is not an alternative to graphs, but a simple version of graphs. As David Khorshid put it, a loop is merely a directed, cyclic graph. In fact, the LangChain framework, built on top of a simple agentic loop, is built on top of LangGraph.

## Third: dynamic transitions matter

We should not always predefine all edges. Sometimes, at runtime, a node may decide how much work to generate. The classic case is map-reduce: split the input into pieces, send each to a worker, then combine the results. The number of workers depends on the input, and we can't know it in advance. LangGraph handles this with Send: a node can dynamically route work to one or more downstream nodes without statically defining every transition.

This is important because useful agent systems combine known structure with runtime variability. We might know that a research task first fans out and then integrates, but not know how many sources will exist. We might know that a supervisor delegates to workers, but not know which specific workers to use until the task begins. Graphs still need runtime flexibility.

**Covers:** What building LangGraph taught us (three lessons: not DAGs, loops are simple graphs, dynamic transitions)
