> [[index|Wiki]] | [[summary|Summary]]

# SAGE — In Plain Language

## What is this about?

Imagine you're a detective building a case file over months. Every new witness statement, document, or clue gets pinned to a corkboard, with string connecting related names, places, and events. When a new question comes in — "who was at the warehouse on the night of the 12th?" — you don't reread every file; you trace the strings on the corkboard from whatever names the question gives you, following bridges to the answer.

AI agents that need to remember things over long stretches of time (chats, research sessions, customer-support histories) face the same problem, and a popular solution is to build exactly this kind of corkboard: a "graph memory" where facts and entities are nodes and their relationships are the connecting strings. This general approach is called GraphRAG (Graph Retrieval-Augmented Generation).

SAGE's insight is that most existing systems build the corkboard once, with fixed rules, and never improve it. SAGE instead trains *two* things together: a "writer" that decides how to pin new information onto the board, and a "reader" that decides which strings to follow when answering a question. Crucially, the writer is graded on whether the reader can actually find the answer using what the writer wrote — so a bad writer that clutters the board with useless pins gets penalized, and a good writer that leaves clean, traceable trails gets rewarded. The two are trained back and forth, round after round, so the corkboard-builder and the corkboard-reader keep improving each other.

## Why does it matter?

Most graph-memory systems have a blind spot: they treat graph construction as a solved, static preprocessing step (an LLM reads a document, spits out some triples, done) and pour all their engineering into cleverer ways to search the resulting graph. But if the graph itself is badly built — missing a crucial connecting fact, or so cluttered with trivial pins that the real path is buried — no amount of clever searching fixes that.

SAGE argues you should optimize the *writing* of the memory graph too, using the same kind of feedback signal search engines have used for decades (did the retrieval actually work?), just applied to how the graph gets built in the first place. If this generalizes, it means agent memory systems stop being "build once, hope it's good" and become something that keeps calibrating itself against how well it's actually being used.

## How does it work?

1. **The corkboard-builder (writer).** Given a batch of documents and a question, the writer reads through them and decides, piece by piece, which entities and relationships to pin onto the graph — this is like a detective jotting "Alice knew Bob," "Bob visited the warehouse," and cross-referencing aliases ("Bob" = "Robert Smith"). It's trained with reinforcement learning: try several ways of building the graph, see which version lets the reader find the right answer, and nudge the writer toward the versions that work.

2. **The corkboard-reader (reader).** Given a question, the reader doesn't just grab pins that literally match keywords in the question — it first plans out what it's *actually* looking for (direct entity mentions, likely aliases, "the thing related to X," a guess at what type of answer is expected — like a detective saying "I need someone who was at the warehouse, might go by a nickname, probably male given witness accounts"). Then it "lights up" the graph starting from those clues and lets the activation spread along the strings, using a smart gate at each connection that dampens over-popular hubs (don't follow every string out of "the city of London") while preserving rare but important bridging connections (do follow the one string that links two otherwise-unrelated clusters).

3. **The context/schema trick.** Because the graph keeps changing as the writer updates it, the reader needs some things to stay stable even as details shift — like a detective who's built dozens of cases and has learned general patterns ("the person the story keeps circling back to without being named is often the key suspect") on top of the specifics of this one case. SAGE splits the reader's judgment into a part that's specific to the current graph and a part that's a stable, cross-case "schema" — a mixture of learned patterns for structural roles like hubs, bridges, and boundaries.

4. **The back-and-forth (self-evolution).** Freeze the reader, retrain the writer against it (writer gets better at writing graphs the current reader can use well). Then freeze the writer, retrain the reader on the newly improved graphs (reader adapts to the writer's new style). Repeat. Neither side improves in isolation forever — the paper proves mathematically that a reader-only fix or a writer-only fix each hits a hard ceiling the other side is needed to break through.

## Where can this be used?

- **Long-running AI assistants** that need to remember a user's preferences, past conversations, and facts across weeks or months without re-reading everything each time.
- **Customer-support and knowledge-base systems** where support tickets, documents, and past resolutions form a growing body of interlinked information that needs targeted retrieval, not brute-force search.
- **Multi-hop research assistants** that need to chain together clues across multiple documents ("this technique builds on that paper, which cites this older idea") rather than answer from a single retrieved passage.
- Outside its own domain: any system that maintains an evolving structured index of information (a codebase dependency graph, a fraud-investigation case graph, a scientific-literature citation graph) where both "how the index gets built" and "how it gets queried" could benefit from being trained together instead of hand-designed separately.

## Conclusions & takeaways

- The framing worth remembering: memory quality is a *joint* property of how it's written and how it's read, not a property of the graph alone — and you can operationalize this by rewarding the writer with the reader's actual success.
- SAGE's biggest, cleanest win is generalization: trained only on multi-hop QA data, it transfers to open-domain QA (NQ) far better than prior graph-memory systems, suggesting the writer/reader co-training teaches transferable *retrieval skill*, not just dataset-specific tricks.
- Honest limitation to remember: on specialized long-term-memory benchmarks (tracking what a user said weeks ago, catching contradictions, avoiding hallucinated memories) SAGE is competitive but not yet best-in-class — the co-evolution loop helps general retrieval more than it currently helps memory *updating and hallucination control*, which purpose-built systems still do better.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Graph memory | A corkboard-and-string structure where facts are nodes and relationships are connecting edges, used instead of (or alongside) a flat pile of text chunks. |
| GraphRAG | The general family of systems that retrieve from a graph memory instead of plain text passages, to better handle questions requiring multi-step reasoning. |
| GFM (Graph Foundation Model) reader | A neural network pretrained to work on *many different graphs* in general (not just this one), then fine-tuned to read the specific memory graph and figure out which nodes/documents answer a question. |
| RL writer (reinforcement-learning writer) | The graph-building component, trained not by copying human-labeled examples but by trial-and-error: build several candidate graphs, see which one lets the reader succeed, and adjust toward the successful style. |
| Structural gating | A learned "volume knob" on each connection in the graph that turns down over-popular, generic connections (hubs) and turns up rare-but-important bridging connections, so the reader doesn't get flooded with noise or miss the one crucial link. |
| Associative retrieval | Finding the answer not by exact keyword match but by following a chain of related concepts — the way remembering "Cornu Ammonis" might lead you to "hippocampus" then to a specific memory-related paper, without the paper ever mentioning "Cornu Ammonis" directly. |
| Context–schema split | Separating "what's true about *this specific* graph right now" (context) from "general patterns that hold across many graphs" (schema, e.g. "hubs are usually less informative than bridges") so the reader stays stable even as the graph keeps changing. |
| Self-evolution loop | Alternately freezing one component and training the other, back and forth, so the graph-writer and graph-reader keep adapting to each other's latest version rather than being trained once and left fixed. |
| Signal-to-noise ratio (SNR) bound | A mathematical guarantee about how much useful "signal" (real evidence) survives versus "noise" (irrelevant clutter) as information spreads through the graph, used to justify why the design choices (gating, soft addressing) should work. |
| Retrieval budget | How many top-ranked documents/entities (top-k) the reader needs to return to have a good chance of covering the true evidence — the paper derives a formula bounding this budget in terms of the SNR. |
| Deducible / Deducibility | Whether the retrieved evidence is actually sufficient for a judge (human or LLM) to derive the correct answer — a stricter, more meaningful bar than just "matches the gold documents." |
