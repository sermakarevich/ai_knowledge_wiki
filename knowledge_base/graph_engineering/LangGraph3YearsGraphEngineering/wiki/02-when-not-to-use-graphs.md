> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# When Not to Use Graphs

**In one sentence:** Some tasks are inherently agentic, and forcing them into a deterministic graph is the wrong move — for those, an agent harness (like Deep Agents) is the right substrate.

## Key points

- Some tasks are more agentic by nature; forcing them into deterministic (graph) paths is the wrong move.
- For such tasks you should not represent the system as a graph at all, but use an agent harness like Deep Agents instead.
- Generic deep research is a good example: a research agent must plan, delegate, search, read, and synthesize in ways that are hard to pin down ahead of time.
- LangChain built early deep research on predefined LangGraph workflows, then moved to a more agentic core loop.
- GPT Researcher, a popular deep research implementation, made the same move: it swapped its graph-shaped multi-agent pipeline for Deep Agents so that planning, delegation, and context management emerge in the harness rather than being hardcoded in the graph.

---

## When not to use graphs

The article draws a clear line: not every LLM system should be modeled as a graph. Some tasks are more agentic by nature, and the act of forcing them into deterministic paths is itself the wrong move — the structure fights the behavior. In these cases the right representation is not a graph at all. Instead of hand-drawing the control flow, you let an agent harness (the article names Deep Agents) own the loop, and the capabilities you need — planning, delegation, search, read, synthesis, context management — emerge at run time instead of being baked into edges and nodes.

Generic deep research is the article's example of this boundary. A research agent needs to plan, delegate, search, read, and synthesize in ways that are hard to pin down ahead of time: the number of steps, their order, and the branching cannot be known before the research begins, so a predefined graph is an approximation of a process that is fundamentally open-ended.

Both sides of the ecosystem moved the same direction. The authors note they built early deep research on predefined LangGraph workflows, then moved to a more agentic core loop. GPT Researcher, a popular deep research implementation, made the same move: it swapped its graph-shaped multi-agent pipeline for Deep Agents, so that planning, delegation, and context management emerge in the harness rather than being hardcoded in the graph.

**Covers:** When not to use graphs
