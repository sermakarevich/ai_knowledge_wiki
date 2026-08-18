> [[index|Wiki]] | [[summary|Summary]]

# Graph Engineering with Kimi K3 — In Plain Language

## What is this about?

Imagine you ask a very well-read assistant, "why did our sales drop in March?" A normal AI search tool (called "RAG" — Retrieval-Augmented Generation) works like a librarian who finds pages that use similar words to your question and hands them to you. That works fine for "what is X," but it fails completely for "why did X happen," because the real answer might be scattered across five unrelated-looking documents: a shipment was late, because a supplier had a problem, because a warehouse flooded, which led to bad reviews, which cut sales. None of those documents mention "sales drop in March" — so the word-matching librarian never finds the chain.

This article proposes a different approach: instead of storing pages of text and searching by "sounds similar," you store *facts* as a web of dots connected by labeled lines — "Warehouse → caused → Supplier delay," "Supplier delay → caused → Release delay," and so on. This web is called a knowledge graph. Instead of asking "what text looks like my question," you ask the system to "walk the path from A to B and show me every link." That's the "graph engineering" this article means.

**Important mix-up to avoid:** there's a second, completely different thing people also call "graph engineering" — wiring several AI agents together in a flowchart (agent A hands off to agent B, which loops back to agent A, etc.). That's about *organizing AI workers*, not *storing facts*. This article is 100% about the facts-and-connections kind. If you've read other articles in this research batch about "graph engineering," check which of the two they mean — the word is the same, the idea is not.

## Why does it matter?

Because the questions that actually matter to a business — "why did this happen," "what's the recurring pattern," "how are these two things connected" — are exactly the questions a word-matching search tool cannot answer, no matter how good the underlying AI model gets. Better AI models don't fix a broken retrieval method; you need a structurally different way of storing information. This article claims (citing Microsoft, Stanford, and MIT research) that the knowledge-graph approach is proven to work, and gives a concrete recipe for building one.

## How does it work?

Think of it as an assembly line with 8 stations, and the belt loops back to station 2 once it reaches station 8:

1. **Bring in raw material** — PDFs, web pages, Slack messages, whatever your source documents are. No processing yet.
2. **Pull out facts** — an AI model reads each document and writes down entities ("Kimi K3," "Moonshot AI") and relationships between them ("developed by"), each with a confidence score and the exact quote it came from.
3. **Merge duplicate names** — "OpenAI," "Open AI," and "OpenAI Inc." need to be recognized as the same thing, or your web of dots turns into many disconnected mini-webs. This is the step most people skip, and the article says it's the step everyone later regrets skipping.
4. **Store it** — in a graph database (Neo4j is the recommended starting point), which is built specifically to store dots-and-lines instead of pages of text.
5. **Retrieve, five different ways** — look up a specific entity, search for similar text, trace a path between two dots, find recurring patterns across the whole web, or filter by "what was true at that point in time."
6. **Let the AI agent explore** — it plans its search, writes the graph-query language (Cypher), reads what comes back, and runs more searches if there are gaps.
7. **Check the work** — verify the AI's conclusion is actually backed by the paths it retrieved, and flag anything that contradicts something else in the graph. Skip this and you've built (in the article's words) "a very sophisticated hallucination machine."
8. **Update the graph** — new facts get added, contradictions get flagged (not silently overwritten), old facts get timestamped rather than deleted. Then the belt loops back to step 2 — every new answer can make the next answer better.

**Why Kimi K3 specifically?** Not because it's the smartest model — Moonshot's own blog admits it trails Claude Fable 5 and GPT-5.6 Sol on general benchmarks. It's chosen because a graph query, unlike a normal question, comes back as a *huge* pile of connected facts (subgraphs, evidence chains), and K3 can hold roughly 1 million tokens (about 750,000 words) of that in its "working memory" at once, versus the 128,000–200,000 most models offer. That means you don't have to chop up the web of facts before showing it to the model — which would defeat the whole point of building the web in the first place. A special engineering trick called Kimi Delta Attention also makes reading all those tokens roughly 6x cheaper/faster than it would otherwise be.

A separate, striking finding the article cites: when researchers compared 26 different AI models on knowledge-graph tasks, a *smaller* model paired with a *well-built* graph consistently beat a *bigger* model paired with a *badly-built* graph. In other words: the quality of your fact-web matters more than which AI model you use to read it.

## Where can this be used?

- **Customer support / root-cause analysis** — "why do customers in region X churn more?" needs a causal chain, not a document search.
- **Supply chain / operations** — tracing how one disruption (a flood, a strike, a shortage) rippled through to a business outcome.
- **Compliance / audit trails** — "show me every step that led to this decision" is a graph-path question by nature.
- **Any domain with a lot of interlinked internal documents** (engineering docs, Slack history, meeting notes) where the useful answers are about how things relate, not what any one document says.

## Conclusions & takeaways

- If your AI answers feel shallow or wrong on "why" questions, the fix the article recommends is not a bigger/better model — it's a better-structured retrieval system.
- Building this properly is roughly a week of upfront engineering work (extraction, deduplication, storage, retrieval, verification, upkeep) — it is not a drop-in replacement for calling an embeddings API.
- Treat the specific percentages you'll see quoted ("85% cheaper, 18% more accurate") as directionally credible but not something to bank on for your own data without measuring it yourself.
- Remember the terminology split: this article's "graph engineering" = knowledge graphs / facts. A different, equally common usage = wiring multiple AI agents into a flowchart. Same words, different tools.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| RAG (Retrieval-Augmented Generation) | Finding relevant text first, then having an AI model write an answer based on it. |
| Triple | A single fact written as Subject → Relation → Object, e.g. "Kimi K3 → developed by → Moonshot AI." |
| Knowledge graph | A database of triples, stored as a web of connected dots (entities) and labeled lines (relationships). |
| GraphRAG | Retrieval-augmented generation done over a knowledge graph instead of over plain text chunks. |
| Local search / global search | Local = look at one dot and its immediate neighbors; global = look for patterns across the whole web. |
| Context window | How much text an AI model can "hold in mind" at once, measured in tokens (roughly word-fragments). |
| Kimi Delta Attention (KDA) | An engineering trick that makes it much cheaper/faster for the model to process very long inputs. |
| Attention Residuals (AttnRes) | A mechanism that helps the model keep track of information from early in a long input without it fading by the end. |
| Cypher | The query language used to ask a graph database questions (like SQL, but for graphs). |
| Entity resolution | Recognizing that "OpenAI," "Open AI," and "OpenAI Inc." are the same thing, so they merge into one dot instead of three. |
| Agent-topology graph engineering | The *other* meaning of "graph engineering": wiring multiple AI agents into a flowchart of who hands off to whom — unrelated to knowledge graphs. |
