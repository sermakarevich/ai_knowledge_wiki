**Figure 1 — "Poisoning attacks on GraphRAG" (technical description)**

**What it shows:** A schematic of a retrieval‑augmented generation (GraphRAG) pipeline being subjected to a data‑poisoning attack, depicting both the legitimate user→model query flow and the adversary's injection path into the knowledge base.

**Components (left‑to‑right):**
- **User** (icon at left) issuing a *Query x*.
- **GraphRAG** (two gears) — the orchestration/agent layer that coordinates search, retrieval, and prompting.
- **Retriever p_η(z|x)** — the retrieval function.
- **(Polluted) Knowledge Base** — a small graph with nodes (entities) and edges (relations), some nodes highlighted red to indicate poisoned/corrupted content.
- **Text Corpus** — a stack of document icons on the right, with an "Adversary" (devil) mascot signifying malicious injection.
- **LLM / Generator p_θ(y|x,z)** (OpenAI‑style logo) — the language model that produces the output.

**Flow / architecture (numbered arrows, approximate):**
1. User → GraphRAG: *Query x* (1).
2. GraphRAG → Retriever: *Semantic Search* (2, downward blue arrow).
3. Retriever → GraphRAG: *Context z* (3, upward red arrow), drawn from the polluted knowledge‑base graph.
4. GraphRAG → LLM: composed *Prompt x, z* (4, orange).
5. LLM → GraphRAG: *Generation* (5, orange).
6. GraphRAG → User: *Response y* (6, red).
- Attack path: Adversary → Text Corpus → *Indexing* → Knowledge Base (red arrow, circled 0), i.e., malicious text is ingested and indexed into the graph before any query is made.

**Takeaway:** The diagram's central message is that in GraphRAG the poisoning surface is the **indexing/knowledge‑base construction stage**: the adversary plants false or malicious text in the corpus, which becomes part of the structured knowledge graph and is later surfaced as retrieved context *z*. Because that context is fed directly into the LLM prompt, the poisoned knowledge propagates through retrieval into the final response, illustrating the attack vector the paper studies (rather than attacking the LLM weights directly).