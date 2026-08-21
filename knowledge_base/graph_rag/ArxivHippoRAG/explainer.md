> [[index|Wiki]] | [[summary|Summary]]

# HippoRAG — In Plain Language

## What is this about?

Imagine an LLM (large language model — the AI that powers ChatGPT-style assistants) as someone with an excellent memory for anything they read *during* a conversation, but total amnesia the moment the conversation ends. To help it "remember" facts, we give it a stack of index cards (documents) it can flip through before answering — that's retrieval-augmented generation, or RAG. The problem: the AI reads each card by itself. If the answer to your question requires combining two cards — one that says "Alhandra was born in Vila Franca de Xira" and another that says "Vila Franca de Xira is in the Lisbon District" — a system that only matches cards to your question by word-overlap struggles, because neither card alone mentions "Lisbon" and your question together.

HippoRAG's answer borrows from neuroscience. Your brain doesn't re-file every memory into one page either — it stores raw experiences in the neocortex (think: the "content" library) and keeps a much smaller index in the hippocampus that says which memories are related to which. When you get a partial clue, the hippocampus's associative index helps you "complete the pattern" and recall the full memory. HippoRAG builds an artificial version of that index: instead of index cards, it builds a knowledge graph (KG — a network of "things" connected by labeled links, e.g. Alhandra → born-in → Vila Franca de Xira) out of every document, using an LLM to read each passage and extract these connections automatically.

## Why does it matter?

Lots of real tasks require connecting dots across many separate documents: a lawyer briefing a case needs facts from a dozen filings; a doctor needs symptoms cross-referenced against multiple lab reports; a researcher needs to connect a gene from one paper to a disease from another. Plain RAG treats every document as its own island; more advanced RAG that tries several rounds of "search, read, search again" (like the method IRCoT) can bridge some gaps but is slow and expensive because it re-runs the LLM at every round. HippoRAG does the same job in one shot, and cheaply, because the expensive LLM work (building the graph) happens once, offline, not every time someone asks a question.

## How does it work?

Think of it as a two-phase process, like preparing a filing cabinet and then searching it:

1. **Build the index (offline, once).** For every document, an LLM plays detective and extracts short facts in "subject – relationship – object" form (this technique is called OpenIE, open information extraction) — e.g., "Alhandra – born in – Vila Franca de Xira." All these facts, from every document, get merged into one giant knowledge graph. Entities that show up in multiple documents (like a person's name) become shared connection points, so the graph naturally links documents to each other even if no single document mentions both facts.
2. **Add "these mean the same thing" shortcuts.** A separate tool measures how similar two entity names are (embeddings — numeric fingerprints of meaning) and draws extra links between near-duplicates, so slightly different phrasings of the same entity still connect.
3. **Search the index (online, per question).** When a question arrives, the system extracts the key names/entities in the question (e.g., "Stanford," "Alzheimer's") and finds where they land in the graph.
4. **Spread the search outward.** A graph-walking algorithm called Personalized PageRank starts at those entity nodes and spreads a "probability of relevance" outward along the graph's connections, the way ripples spread from a stone dropped in water — nodes closer to and more connected with the seed entities get more probability. Whichever documents contain the highest-scoring nodes get retrieved.
5. **Weight rare entities more.** A trick called node specificity gives more weight to entities that appear in fewer documents (similar to how "Stanford" is more distinctive than "the," "researcher," or other common words) — so the search doesn't get diluted by very common concepts.

## Where can this be used?

Anywhere multi-document reasoning matters: enterprise search over internal wikis and tickets, legal discovery, scientific literature review, customer-support knowledge bases that span many articles, and any chatbot memory system that needs to recall facts a user mentioned across many separate past conversations rather than just the current one.

## Conclusions & takeaways

- Building an explicit knowledge graph as a retrieval index, rather than relying purely on vector similarity between passages, measurably helps when answers require connecting facts across documents.
- The approach is unusually cheap and fast at answer time because the expensive LLM step happens only once, during indexing — not once per question.
- It is not a finished product: the graph-building and search steps are all "off-the-shelf" (not specially trained for this task), the graph search ignores what the connecting relationships actually say (it just follows links), and nobody has yet tested whether this approach still works well on a knowledge graph 100x larger than the paper's benchmarks.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| RAG (retrieval-augmented generation) | Giving an LLM extra documents to read before it answers, instead of relying only on what it memorized during training |
| Multi-hop QA | Questions whose answer requires chaining together facts from two or more separate sources, not just one |
| Knowledge graph (KG) | A network of "things" (nodes) connected by labeled relationships (edges), like a family tree but for any facts |
| OpenIE (open information extraction) | Automatically pulling out "subject – relationship – object" facts from plain text, without a pre-defined list of relationship types |
| Personalized PageRank | A graph-walk algorithm (a variant of the algorithm that originally ranked Google search results) that spreads "importance" outward from a chosen starting set of nodes rather than from everywhere equally |
| Node specificity | A weighting trick that treats rare, distinctive entities as more informative than common ones — similar in spirit to "inverse document frequency" in search engines |
| Hippocampal indexing theory | A neuroscience theory that the brain's hippocampus doesn't store memories itself but keeps an index of associations pointing to where memories are stored in the neocortex |
| Path-finding question | A question whose two clue-facts never appear together in any single document, so the answer can only be found by combining separate documents through a shared entity |
| Path-following question | A question whose answer can be reached by following one chain of documents step by step (A mentions B, B mentions C) — easier than path-finding |
| Embeddings | Numeric representations of text that let a computer measure how similar two pieces of meaning are |
| IRCoT | An iterative multi-hop retrieval baseline that alternates retrieval and LLM reasoning steps several times per question |
