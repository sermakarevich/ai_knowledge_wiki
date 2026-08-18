> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Stack, Week-One Plan, and Troubleshooting

**In one sentence:** This closing chunk lays out the concrete stack (Neo4j + Kimi K3 API + Kimi Code CLI + DSPy), a realistic day-by-day week-one build plan, the failure modes and their fixes once the system is running, and cautions that the widely quoted "85% lower cost, 18% better accuracy" figures are not a universal guarantee — build the graph, the model is the easy part.

## Key points

- The recommended stack has four moving parts: **Neo4j** as the graph database (best docs, best visualization, genuinely readable Cypher), **Kimi K3** via API as the model (OpenAI-SDK compatible, so integration is a base-URL change), **Kimi Code CLI** as the agent/execution layer (reads and edits files, runs shell commands, supports MCP), and **DSPy** for orchestration if you'd rather program the pipeline than hand-tune prompts.
- Week one is a deliberate, day-by-day ramp: install Neo4j and get Cypher comfortable (Day 1), run extraction on one real document set and inspect what it extracted (Day 2), load the triples and build the simplest retrieval — entity lookup plus one-hop traversal (Day 3), add path search (Day 4), close the loop by letting Kimi Code query the graph and write a fact back over MCP (Day 5), and measure accuracy, token cost, and latency on your own data (Day 6–7).
- The single most common failure is **duplicate entities** — "OpenAI," "Open AI," and "OpenAI Inc." each becoming separate nodes so queries return fragments — and the fix is to run the entity-resolution step (Prompt 2) as a batch job over new entities *before* insertion, not after, because retrofitting resolution onto an already-polluted graph is significantly harder.
- Every other failure has a concrete, prompt-anchored fix: make the Prompt 1 evidence field mandatory (an exact quote or the relationship doesn't go in) to kill invented relationships, pass the *literal* schema into Prompt 3 and validate generated Cypher to stop "everything or nothing" queries, forbid inferring causation from co-occurrence and require the model to cite the specific relationship type it relies on, cap traversal depth to two or three hops to control cost, and run a scheduled maintenance pass (Prompt 5) so entropy doesn't quietly accumulate.
- The "85% lower cost, 18% better accuracy" number floating around is not a universal guarantee — it comes from specific research on specific document sets, and the baseline matters ("cheaper than loading structured files directly into context" is a very different claim than "cheaper than your current RAG"); the *direction* is well-supported, but the *magnitude* is something you measure yourself in week one.
- Standard RAG is "a search engine that writes prose"; graph engineering instead answers *why* and *how are these connected*, gets structurally better with every document, can surface what it doesn't know because graph gaps are visible (vector-store gaps are not), and costs less per useful answer because you retrieve the relevant subgraph rather than stuffing twenty documents into context and hoping.
- The real tradeoff is a week of upfront work — you're building extraction, resolution, storage, retrieval, verification, and maintenance instead of just calling an embedding API — and that week is what separates a demo from a system.
- The conclusion inverts the "reach for a bigger model" instinct: the research consistently shows a smaller model with a well-built graph beats a larger model with poor retrieval, because the system around the model matters more than the model — so build the graph, the model is the easy part.

---

## The Stack

The article recommends a four-component stack:

- **Graph database — Neo4j**, to start. It has the best docs, the best visualization, and Cypher is genuinely readable.
- **Model — Kimi K3 via API.** kimi-k3 on platform.kimi.ai, OpenAI-SDK compatible, so integration is just a base-URL change.
- **Agent layer — Kimi Code CLI.** It reads and edits files, runs shell commands, and supports MCP. It's your execution layer: the graph tells it what's true, the CLI acts on it.
- **Orchestration — DSPy**, if you want to program the pipeline rather than hand-tune prompts. Worth reading even if you don't adopt it — it reframes the model as a component in a system rather than the system itself.

## Week One: A Realistic Plan

- **Day 1** — Install Neo4j locally. Run the tutorial. Write five Cypher queries by hand until the syntax stops feeling foreign.
- **Day 2** — Take one document set you actually care about. Run Prompt 1 through the K3 API. Look hard at what it extracted — this is where you find out whether your prompt is too loose.
- **Day 3** — Load the extracted triples into Neo4j. Build the simplest possible retrieval: entity lookup plus one-hop traversal. Test it against a question your current RAG answers badly.
- **Day 4** — Add path search. This is the moment the difference becomes obvious — ask a "why" question that requires three hops and watch it work.
- **Day 5** — Connect Kimi Code via MCP. Let the agent query the graph, find a gap, run a search, and write a new fact back. That's your first closed loop.
- **Day 6–7** — Measure. Accuracy versus your old RAG, token cost per query, latency. Real numbers on your own data, not benchmarks from a blog post.

## Troubleshooting

These are the failure modes the article calls out, each with why it happens and the fix.

### The graph fills up with duplicate entities

The single most common failure. "OpenAI," "Open AI," "OpenAI Inc." all become separate nodes and your queries return fragments.

**Fix:** don't skip the resolution layer. Run Prompt 2 as a batch job over new entities *before* insertion, not after. Retrofitting entity resolution onto a polluted graph is significantly harder than doing it upfront.

### Extraction invents relationships that aren't in the source

The model reads "Microsoft and OpenAI" in the same sentence and creates Microsoft → partnered_with → OpenAI when the text said no such thing.

**Fix:** the evidence field in Prompt 1 is not optional. Require an exact quote for every relationship. If the model can't produce one, the relationship doesn't go in. This single constraint eliminates most extraction hallucination.

### Queries return everything or nothing

Usually a schema problem. The model generates Cypher against labels that don't exist, or writes a query so broad it returns the entire graph.

**Fix:** pass the actual schema in Prompt 3, every time. Not a description of it — the literal node labels, relationship types, and properties. And validate generated Cypher against the schema before executing it.

### The answer is confident and wrong

The model connected two nodes that are adjacent in the graph but not causally related, and presented it as a finding.

**Fix:** Prompt 4's "do not infer causation from co-occurrence" rule, plus the verification layer. Make the model cite the specific relationship type it's relying on. caused_by is a claim. mentioned_alongside is not.

### Costs are higher than expected

Graph engineering reduces cost per useful answer, but a badly built system can pass enormous subgraphs on every query.

**Fix:** limit traversal depth. Most questions need two or three hops, not six. Measure your average tokens per query — if it's climbing, your retrieval is too greedy, not your model too expensive.

### The graph slowly stops being trustworthy

Contradictions accumulate. Old facts sit alongside new ones with no indication which is current.

**Fix:** timestamps on everything, and a scheduled maintenance pass with Prompt 5. Same principle as linting a codebase — entropy is guaranteed, the only question is whether you have a process for it.

## About Those Numbers You'll See Quoted

You'll see "85% lower cost, 18% better accuracy" attached to graph engineering everywhere right now. Worth knowing where that comes from: it's from specific research on specific document sets, not a universal guarantee. The comparison baseline matters enormously — "85% cheaper than loading structured files directly into context" is a very different claim from "85% cheaper than your current RAG."

The direction of the finding is well-supported across multiple independent groups. The exact magnitude on your data is something you measure in week one, not something you assume. The same discipline applies here as anywhere: your own five test questions are worth more than anyone's published percentage.

## What You Actually Get, and Conclusion

Standard RAG gives you a search engine that writes prose. Graph engineering gives you a system that:

- Answers "why" and "how are these connected" instead of only "what documents mention this"
- Gets structurally better with every document you feed it
- Can tell you what it doesn't know, because gaps in a graph are visible in a way gaps in a vector store are not
- Costs less per useful answer, because you retrieve the relevant subgraph instead of stuffing twenty documents into context and hoping

The tradeoff is real: it's more work upfront. You're building extraction, resolution, storage, retrieval, verification, and maintenance instead of calling an embedding API. That's a week of work. And it's the week that separates a demo from a system.

**Conclusion.** The instinct when your AI system underperforms is to reach for a bigger model. The research consistently says the opposite: a smaller model with a well-built graph beats a larger model with poor retrieval. The system around the model matters more than the model. Kimi K3's 1M context and long-sequence economics make it the right engine for this architecture — not because it's the strongest model in absolute terms, but because graph engineering rewards exactly what K3 is built for.

**Build the graph. The model is the easy part.**

*(Educational content. All performance figures cited are from published research on specific datasets, not universal guarantees. Measure on your own data before committing to production architecture.)*

**Resources (from the article):**

- Kimi K3: https://www.kimi.com
- Kimi K3 on GitHub: https://github.com/MoonshotAI/Kimi-K3
- Kimi Code CLI: https://github.com/MoonshotAI/kimi-code
- Neo4j: https://neo4j.com
- Microsoft GraphRAG: https://github.com/microsoft/graphrag
- DSPy: https://github.com/stanfordnlp/dspy

**Covers:** "The Stack" through "Conclusion," plus the article's link list.
