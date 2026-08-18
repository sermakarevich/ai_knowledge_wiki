---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Graph Engineering Guide (2026)

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are the three parts that fully specify an agent graph, and what does each one do?

> [!tip]- Answer
> Nodes (specialized agents or deterministic steps, each with one job), edges (the routing between nodes — straight, conditional, fan-out, or fan-in), and shared state (the object every node reads from and writes to, such as the task, draft, notes, and verdict). See [[wiki/01-what-is-graph-engineering|What Is Graph Engineering?]].

### Q2. Why is a loop considered a special case of a graph rather than something different from it?

> [!tip]- Answer
> A loop is a single-node graph with an edge pointing back to itself — one worker repeating discover/plan/execute/verify. Graph engineering doesn't replace loop engineering; it's the layer above it that decides how several such loops hand off to each other, with the agent's freedom living inside each node rather than across the whole job. See [[wiki/01-what-is-graph-engineering|What Is Graph Engineering?]].

### Q3. Name the three things graph engineering is explicitly NOT, according to the guide.

> [!tip]- Answer
> (1) Knowledge graphs / GraphRAG — those model data as entities-and-relations for retrieval, not execution. (2) A new capability — nothing shipped in July 2026 that couldn't be built in 2025; LangGraph, AutoGen, and Google ADK predate the term. (3) A default — most tasks are a single loop, and reaching for a graph early buys a distributed-systems problem you didn't need. See [[wiki/01-what-is-graph-engineering|What Is Graph Engineering?]].

### Q4. Using the PDF-summarizer vs. market-brief examples, what is the actual test for whether a task needs a graph?

> [!tip]- Answer
> The test is whether the graph does work a single loop genuinely couldn't hold. The PDF summarizer's five nodes collapse into one loop with no loss, so it shouldn't be a graph. The market brief's nodes (parallel research across five sources, synthesis, drafting, an independent skeptical reviewer) each do something a single loop couldn't — so it earns the graph. See [[wiki/02-when-to-use-a-graph|When Should You Reach for a Graph?]].

### Q5. The guide claims LangGraph, AutoGen's GraphFlow, Google ADK, and A2A all predate the term "graph engineering." What, then, does the guide say is actually new in mid-2026?

> [!tip]- Answer
> Only the vocabulary and framing — a shared name for design decisions (what are the nodes, what are the edges, what's in the state) those frameworks already asked of builders, plus a growing sense that this is a distinct skill worth teaching on its own, not a new technical capability or paradigm. See [[wiki/02-when-to-use-a-graph|When Should You Reach for a Graph?]].

### Q6. In the 5-layer AI engineering stack (prompt, context, harness, loop, graph), why does the guide say the layers are "cumulative, not a ladder you climb away from"?

> [!tip]- Answer
> Because each outer layer depends on the one beneath it working: a graph is full of nodes, a good node is a well-designed loop, and a good loop needs a real harness. Skipping a lower layer — e.g. wiring weak agents into an org chart — just makes the failure show up one level further out, in a more elaborate form. See [[wiki/02-when-to-use-a-graph|When Should You Reach for a Graph?]].

### Q7. What specific critique does @NathanFlurry make about the timing of "graph engineering," and why does the guide accept it rather than argue back?

> [!tip]- Answer
> He points out that "graph engineering" posts rarely mention A2A, and that multi-agent delegation already had real enterprise history in 2025 (e.g. via LinkedIn and IBM) — meaning the July 2026 term is late to name something, not early. The guide concedes this outright as one of four fair critiques, rather than defending the term's novelty. See [[wiki/03-hype-check-and-checklist|Is Graph Engineering Just Slop?]].

### Q8. The guide is unusually self-skeptical — it quotes its own critics at length rather than only citing supporters. What does the three-question filter let it conclude that a simple "is this hype or not?" framing couldn't?

> [!tip]- Answer
> The filter separates the *word* from the *shift*: it lets the guide agree completely that the term is slop-prone and not new (question 3: no) while still affirming that teams really are moving from single loops to coordinated specialist nodes over shared state, and that this coordination is a distinct design skill (questions 1 and 2: yes). A binary hype/not-hype framing would have forced picking one side; the filter lets both be true at once — see the weakest-link discussion in [[critical_thinking|Critical Analysis]] and [[wiki/03-hype-check-and-checklist|Is Graph Engineering Just Slop?]].
