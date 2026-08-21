> [[index|Wiki]] | [[summary|Summary]]

# Why Neighborhoods Matter — In Plain Language

## What is this about?

Imagine asking a very well-read assistant a question, and it goes off to a giant web of interconnected facts — a knowledge graph — to find the answer. It doesn't just look at one fact; it hops from fact to fact, following connections, until it's confident it has an answer. At the end, it tells you: "here are the two or three facts I used." That's a citation.

This paper asks a simple but important question: is that short list of "facts I used" the *whole story*? Or did the assistant also lean on things it saw along the way but never explicitly mentioned — the neighborhood of facts surrounding the ones it cited? The authors call this "Agentic GraphRAG" (an AI agent doing Graph-based Retrieval-Augmented Generation), and they run careful experiments to find out whether the cited facts alone explain the answer, or whether the unmentioned neighbors matter too.

## Why does it matter?

If you're building an AI system that cites its sources so people can trust and verify its answers, you want those citations to be honest and complete. If an assistant secretly relies on information it never lists as a source, then the citation is misleading — it looks fully verifiable, but it isn't. This matters a lot for anything high-stakes: legal research, medical Q&A, financial analysis — anywhere someone might check the citations and assume that's everything the AI used.

## How does it work?

Think of it like a detective walking through a city, visiting a dozen buildings (entities) while investigating a case, but only listing two buildings as "evidence" in the final report.

1. **Set up the city.** The authors build a small, controlled "city" (knowledge graph) from a well-known multi-hop question-answering dataset, with about 1,800 buildings (entities) and 1,700 streets connecting them (relationships).
2. **Let six different detectives investigate.** They test a plain LLM (no city map at all), classic RAG (grabs nearby documents), classic non-agentic GraphRAG (walks the city once), and three "agentic" versions that autonomously decide where to go and when to stop, differing in how strict they are about only citing places they actually visited.
3. **Bulldoze buildings and see what breaks.** To find out which buildings actually mattered, they run three controlled experiments:
   - **Remove the cited buildings** — does the detective's answer collapse? (Tests: are citations *necessary*?)
   - **Only allow access to the cited buildings** — can the detective still get the right answer with nothing else? (Tests: are citations *sufficient*?)
   - **Remove or hide the buildings the detective visited but didn't list as evidence** — does that also break the answer? (Tests: does unlisted context matter?)
4. **Compare against a fair control.** To make sure removing buildings isn't just generally disruptive, they also bulldoze the same number of *random*, uncited buildings and compare the damage.

The finding: removing cited buildings hurts a lot — confirming citations matter. But restricting the detective to *only* the cited buildings also hurts — meaning the cited buildings alone don't contain everything needed. And removing the unlisted-but-visited buildings hurts too. The unlisted neighborhood was doing real work.

## Where can this be used?

- **Any GraphRAG or agentic RAG product that shows citations to end users** — this paper is a warning that "here's my source" may not equal "here's everything I used."
- **AI audit and compliance tooling** — if regulators or auditors want to verify an AI's evidence trail, a citation list alone may be an incomplete audit surface; the full traversal log matters.
- **Provenance and explainability research** — motivates building interfaces that show the whole traversal path, not just the final citations, when transparency really matters.
- **Benchmark design for agentic retrieval systems** — the paper's ablation methodology (remove-cited vs remove-random vs isolate-to-cited) is a reusable recipe for stress-testing any citation mechanism, not just this specific system.

## Conclusions & takeaways

A month from now, remember this: **in agentic graph retrieval, "what I cited" and "what actually shaped my answer" are not the same set** — the second is bigger, and it includes places the agent walked through but never named. Citations are necessary evidence, but they're not the complete evidence. If you're designing citation or provenance systems for agentic RAG, you need to expose (or at least log) the traversal trajectory, not just the final source list. The main honest limitation: this was shown on a small, synthetic 30-question benchmark built from one dataset, not a large real-world deployment — so the effect sizes, while clear directionally, may not transfer exactly to bigger, messier graphs.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Agentic GraphRAG | An AI agent that autonomously decides how to explore a knowledge graph (rather than doing one fixed lookup) before answering |
| GraphRAG | Retrieval-Augmented Generation that pulls evidence from a knowledge graph (facts + connections) instead of plain documents |
| RAG | Retrieval-Augmented Generation — grounding an LLM's answer in retrieved external text |
| Provenance | The record of where an answer's evidence actually came from |
| Citation faithfulness | Whether the sources an AI cites genuinely and completely explain its answer |
| Ablation | Deliberately removing or disabling a part of a system to see how much that part mattered |
| Multi-hop QA | Questions that require chaining together facts from more than one document/fact to answer |
| Entity | A node in the knowledge graph — a person, place, or concept |
| Text unit (TU) | A chunk of source text linked to one or more graph entities |
| Isolation (in this paper) | Restricting a system's access to only a specific subset of entities, to test if that subset alone is enough |
| Leiden communities | Clusters of tightly connected entities found automatically in the graph, used to organize it into "neighborhoods" |
| Visited-but-uncited entity | A graph node the agent looked at during its search but did not include in its final citation list |
