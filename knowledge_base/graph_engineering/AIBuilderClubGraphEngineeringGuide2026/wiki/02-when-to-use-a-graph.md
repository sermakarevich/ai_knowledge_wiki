> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# When Should You Reach for a Graph?

**In one sentence:** The default answer to "when should you use a graph?" is "probably not" — a single well-scoped task with a clear verifier is a loop, and a graph only earns its keep when the work genuinely exceeds what a loop can hold.

## Key points

- The load-bearing default of the guide is that you probably do NOT need a graph: a single well-scoped task with a clear verifier is a loop, and reaching for a graph there is pure overhead.
- The decision table is a set of triggers, not a checklist to satisfy — you don't need all six — but if the honest answer to most of them is "yes," building a graph is how you turn a two-hour task into a two-day framework project.
- The over-engineered counter-example is "Summarize this PDF" built as a five-node graph (fetcher, chunker, summarizer, reviewer, formatter, with conditional edges and a shared state object) that is slower to build, harder to debug, and more expensive to run than the one thing it should have been: an agent in a loop that reads the file and writes a summary.
- The right-sized example is "Produce a researched, fact-checked market brief every morning": a researcher node fans out across five sources in parallel, a synthesizer joins their findings, a writer drafts, and a skeptical reviewer node (different model, read-only) scores it and loops back on a fail — each node has a job a single loop couldn't hold, and the hand-offs are the point.
- The tell for whether a graph earns its keep is whether the graph is doing work the loop couldn't: if you can collapse your five nodes back into one agent's loop and lose nothing, you should.
- Graph engineering is mostly prior art: LangGraph's StateGraph, Microsoft AutoGen's GraphFlow, Google ADK's graph-based architecture with sequential/parallel/loop workflow agents, and the A2A protocol for cross-team agent delegation all shipped before the term trended — what's new is a shared name for the design decisions those frameworks always asked of you, not a new paradigm.
- In the 5-layers-of-AI-engineering stack (prompt, context, harness, loop, graph), graph is the outermost layer and the one you reach for last; the stack is cumulative, not a ladder, so skipping a lower layer just makes the graph on top fail in a more elaborate way.

---

## The Default Answer: Probably Not

This question separates the useful builders from the people adding boxes to a diagram for fun. The load-bearing claim of the whole guide is that **you probably don't need a graph**:

- A single well-scoped task with a clear verifier is a **loop**.
- Reaching for a graph in that situation is pure overhead.

## The Decision Table as Triggers

The article presents an "honest decision table" of six signal questions. The key framing:

- Read the table as a **set of triggers, not a checklist** — you don't need all six.
- But if the honest answer to **most** of them is the "yes / build a graph" column, building a graph is how you turn a two-hour task into a two-day framework project.

## Over-Engineered vs. Right-Sized

### Over-engineered — a graph you didn't need

**"Summarize this PDF."** Built as a five-node graph:

- Nodes: a fetcher, a chunker, a summarizer, a reviewer, and a formatter — with conditional edges and a shared state object.
- Result: it works, but is slower to build, harder to debug, and more expensive to run than the one thing it should have been — an agent in a loop that reads the file and writes a summary.
- The verdict, in the article's words: "You engineered an org chart to answer an email."

### Right-sized — a graph that earns its keep

**"Produce a researched, fact-checked market brief every morning."**

- A **researcher node** fans out across five sources in parallel.
- A **synthesizer** joins their findings.
- A **writer** drafts.
- A **skeptical reviewer node** — different model, read-only — scores it and loops back on a fail.
- Why it works: each node has a job a single loop couldn't hold, and the hand-offs are the point.

### The Tell

The test is whether the graph is doing work the loop couldn't. If you can collapse your five nodes back into one agent's loop and lose nothing, you should. The article defers the exact call — borderline cases, cost math, and the migration path — to *Agent Graph vs Loop: When to Use Which*, and to how the disciplines relate in *Graph Engineering vs Loop Engineering*. The one-line version: master the loop first, and only split it into a graph when the work forces your hand.

## Isn't This Just LangGraph?

The sharpest reply in the timeline was some version of "congrats, you reinvented LangGraph." The honest answer: mostly right, and the prior art (described only at the level the official docs support, as of July 2026) ships in real tools well before the term "graph engineering" trended:

- **LangGraph (from LangChain)** — per its own docs, "a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents." In practice you define a **StateGraph**, add nodes, and add the edges between them — the exact nodes/edges/state model described above. If you've used LangGraph, you've been doing graph engineering under a different name.
- **Microsoft AutoGen — GraphFlow** — brings graph-based multi-agent orchestration to AutoGen: you describe how a team of agents connects and hands off, rather than running one agent in isolation. (The exact API was moving during 2026 — check the current AutoGen docs.)
- **Google ADK (Agent Development Kit)** — makes the graph model a headline feature. Its docs describe orchestrating "complex tasks through structured, graph-based architectures," and it ships named **sequential, parallel, and loop workflow agents**, plus agent routing — fan-out/fan-in and loops as first-class building blocks. (Its Go SDK hit 2.0 GA in 2026; the graph model spans the Python/TypeScript/Java/Kotlin SDKs too.)
- **A2A (Agent2Agent)** — an open protocol for agents to delegate to each other across systems: the "edges between graphs owned by different teams" layer. The clearest evidence the multi-agent idea has real, pre-buzzword history in the enterprise.

The verdict: is graph engineering just LangGraph? The technology, largely yes — LangGraph, GraphFlow, and ADK got there first. What's actually new in mid-2026 is narrower and softer: **a shared name for the design decisions those frameworks always asked of you** (what are the nodes, what are the edges, what's in the state) and a growing sense that this is a distinct skill worth teaching rather than a framework detail. That's a real thing — just a much smaller thing than "a new paradigm."

## The 5 Layers of AI Engineering

The cleanest way to place graph engineering without overselling it comes from @sairahul1, who framed the whole stack in one line: "Prompt, context, harness, loop & graph engineering... You can think of an AI application as five layers."

- The five layers, from closest to the model outward: **prompt → context → harness → loop → graph**.
- Each layer engineers the system one step further out from the model.
- The stack is **cumulative, not a ladder you climb away from**:
  - A graph is full of nodes.
  - A good node is a well-designed loop.
  - A good loop needs a real harness — the six components (context, tools, orchestration, state, evaluation, recovery) that make an agent able to act at all.
- Skip a lower layer and the graph on top just fails in a more elaborate way: if your nodes are weak agents, wiring them into an org chart gives you a weak org.
- Graph engineering is the outermost layer — which also makes it the one you should reach for last.

**Covers:** Decision framework for graphs vs. loops; over-engineered vs. right-sized examples; LangGraph/AutoGen/ADK/A2A prior art; the 5-layer AI engineering stack (source chunk 02)
