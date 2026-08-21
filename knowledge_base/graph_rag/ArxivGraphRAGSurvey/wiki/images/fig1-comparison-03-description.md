**Figure 1 — Technical summary**

**What it shows.** A schematic side‑by‑side flow diagram comparing three answer‑generation pipelines for the same user query ("How did the artistic movements of the 19th century impact the development of modern art in the 20th century?"). Each panel is a vertical flow: *Query → (optional) Retriever → LLMs → Response*. A red "✗" or black "✓" under each response signals whether the output is deemed adequate.

**Axes / quantitative trends.** There are no plotted axes, scales, or numerical trends; this is a qualitative architecture diagram rather than a chart. The only "trend" is a left‑to‑right progression in retrieval structure and answer specificity:

- **Left — Direct LLM:** Query goes straight to the LLMs. The response is a generic, shallow summary. Marked ✗.
- **Middle — RAG:** A Retriever returns *retrieved text* (a short numbered fact list, ~4 items) that is fed to the LLMs. The response is more concrete but still blends relational claims into prose. Marked ✗.
- **Right — GraphRAG:** A Retriever returns *retrieved triplets* — explicit subject–predicate–object edges (e.g., (Claude Monet)–introduced→(new techniques); (Impressionist techniques)–influenced→(later art movements); (Pablo Picasso)–pioneered→(Cubism)) — which drive the LLMs to a precise, relation‑faithful answer. Marked ✓.

**Takeaway.** Direct LLM answers are shallow; RAG improves grounding but, because natural‑language text encodes entity relationships loosely and at variable length, it under‑emphasizes the relational ("influence") structure that is the core of the question. GraphRAG, by retrieving explicit entity–relation triples from a graph, preserves that relational structure and yields a more accurate, specific response — the only configuration endorsed with a checkmark.