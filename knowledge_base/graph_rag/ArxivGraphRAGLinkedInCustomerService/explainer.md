> [[index|Wiki]] | [[summary|Summary]]

# Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering — In Plain Language

## What is this about?

Picture a big company's customer-support team. Over the years they've built up a huge pile of past support tickets — each one a record of a problem a customer had and (hopefully) how it was solved. When a new problem comes in, the fastest way to solve it is often to find a similar past ticket and reuse its solution.

The standard way AI tools do this "find a similar past case" job is called RAG (Retrieval-Augmented Generation): chop every document into small text snippets, turn each snippet into a list of numbers (an embedding) that captures its meaning, and when a new question arrives, find the snippets whose numbers are closest to the question's numbers. It's like a librarian who's shredded every book into paragraphs and can only search paragraph by paragraph — fast, but she's lost the table of contents and any sense of which paragraphs belong together.

This paper, from a team at LinkedIn, points out that support tickets aren't just flat text — they have structure (a summary, a description, a priority, a thread of comments, steps to fix it) and they relate to each other (ticket #22970 might be a near-duplicate of ticket #1744). Chopping tickets into equal-sized snippets throws all of that away. So instead of shredding, the authors build a map — a knowledge graph — that keeps each ticket's parts connected to each other and draws lines between related tickets. Then, when a question comes in, the system doesn't blindly grep for similar text; it reads the map, jumps to the right ticket, walks to the right part of it, and hands that exact piece to an AI to write the answer.

## Why does it matter?

Slow or wrong answers to support tickets cost real money and real customer trust. If a support tool gives an incomplete answer because it accidentally split a ticket's "here's the fix" sentence away from the "here's the problem" sentence, the person asking has to dig further or wait for a human. If the tool doesn't realize a brand-new-looking issue is actually a duplicate of one solved last month, it may miss the fastest path to a fix. This paper isn't just an academic exercise — it's a system LinkedIn put in front of real customer-service staff and measured with a real experiment, and it shows that fixing "the AI doesn't understand structure" produces a measurable business win: issues got resolved almost twice as fast for the group using the tool.

## How does it work?

Think of it as a two-stage process: building the map, then using the map.

**Stage 1 — Build the map (once, offline).**
1. For every support ticket, break it into its natural parts: summary, description, priority/root-cause/impact fields, comment thread, steps to reproduce. Connect these parts to the ticket with labeled arrows (like a small family tree per ticket).
2. Look for tickets that are near-duplicates. Some are explicit — the ticket text literally says "this is a clone of ticket X." Others are implicit — two tickets just read similarly, discovered by comparing their embeddings. Draw arrows between related tickets too.
3. A computer program handles the parts that are easy to spot mechanically (like "priority: Major"); an LLM (a large language model, the kind of AI behind ChatGPT) handles the messier parts, like pulling a clean summary out of a rambling comment thread.
4. Store the whole map in a graph database (a database built to store "things and the arrows between them," here using a tool called Neo4j) and also store number-versions (embeddings) of each part's text in a separate vector database, for quick similarity search later.

**Stage 2 — Use the map (every time someone asks a question).**
1. An LLM reads the question and picks out which "parts" it's asking about and what it wants (e.g., "they're asking about the login issue, and they want the fix").
2. The system compares those extracted parts against the map's tickets, using the number-versions from step 4 above, and picks the ticket that best matches — like a "which family tree looks most like what you described" check.
3. It then asks an LLM to write a precise, structured lookup command (a language called Cypher, which is to graph databases what SQL is to spreadsheets) that walks straight to the exact part of that ticket's family tree holding the answer — e.g., "go to ticket #22970, then to its description, then to its steps-to-reproduce."
4. Finally, an LLM reads that exact retrieved piece plus the original question and writes the answer in plain English.
5. If anything in the map-walking step breaks (a bad Cypher query, a system hiccup), the system doesn't just fail — it quietly falls back to the old-fashioned "search similar text snippets" method, so customers still get an answer.

## Where can this be used?

The obvious use is any large organization with a big archive of structured, interlinked records and a support/help-desk function — IT helpdesks, SaaS customer support, internal engineering bug trackers (Jira, GitHub Issues), even legal case files or medical records where a "case" has sub-parts and relates to other cases. Anywhere records have (a) internal structure worth preserving and (b) relationships to other records worth exploiting, this pattern — map first, then query the map — beats treating everything as interchangeable shredded text.

## Conclusions & takeaways

- Structure and relationships between documents are real signal that flat-chunk RAG throws away; modeling them explicitly as a graph can meaningfully improve both retrieval accuracy and answer completeness.
- The gains held up not just on an offline benchmark but in a live business experiment with a real operational metric (ticket resolution time) — a rarer and more convincing kind of evidence than a leaderboard number.
- A month from now, the thing worth remembering: "if my documents have internal sections and cross-references, and I'm using plain RAG, I'm probably throwing away exploitable structure" — worth checking before assuming a bigger LLM or better embeddings is the fix.
- Limitation to keep in mind: this is one company's internal ticket data and one internal A/B test, not a public, independently reproducible benchmark — see [[critical_thinking|Critical Analysis]].

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| RAG (Retrieval-Augmented Generation) | Look up relevant text first, then have an AI write an answer using that text, instead of relying only on what the AI memorized during training. |
| Knowledge graph (KG) | A map of "things" (nodes) and the labeled "arrows" (edges) connecting them, instead of plain text. |
| Embedding | A list of numbers that represents the meaning of a piece of text, so that similar meanings end up as similar number-lists. |
| EBR (Embedding-Based Retrieval) | Finding relevant text by comparing embeddings (number-lists) for closeness, rather than matching exact words. |
| MRR (Mean Reciprocal Rank) | A retrieval score: how close to the top of the results list the correct answer lands, averaged over many questions. Higher is better; 1.0 means it's always first. |
| Recall@K | Out of all questions, what fraction had the correct answer somewhere in the top K results. |
| NDCG@K | Like Recall@K, but also rewards putting the best result even higher (position matters, not just presence). |
| BLEU / ROUGE / METEOR | Automatic scores that compare an AI-generated answer's wording against a reference "correct" answer; higher means closer wording overlap. |
| Cypher | The "question language" for graph databases (like Neo4j) — you write a Cypher query to say "find this node, then follow this arrow, then follow that arrow." |
| Neo4j | A specific graph database product used here to store the knowledge graph. |
| P50 / P90 | Percentile measures of a distribution — P50 is the median (half of cases are faster, half slower); P90 means 90% of cases are faster than this value, capturing the "slow tail." |
| GPT-4 / E5 | GPT-4 is the large language model used for writing answers; E5 is the embedding model used to turn text into number-lists. Both were held identical between the control and experimental groups so the comparison is fair. |
