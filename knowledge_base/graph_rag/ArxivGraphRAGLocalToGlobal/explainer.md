> [[index|Wiki]] | [[summary|Summary]]

# From Local to Global — In Plain Language

## What is this about?

Imagine you have a librarian who is extremely good at one specific task: if you ask "which page mentions the word 'photosynthesis'?", they can find it in seconds. That's how most AI chatbots-over-your-documents (called **RAG**, retrieval-augmented generation) work today — they turn your question into a search, fetch a few matching paragraphs, and have an AI write an answer from just those paragraphs.

But now ask that librarian: "What are the big recurring themes across this entire 500-book library?" They can't just fetch a few pages for that — they'd need to have actually read and connected ideas across the whole library. This paper, from Microsoft Research, is about building an AI system that can do that second kind of question well. They call it **GraphRAG**.

The trick: instead of only indexing documents by their words, GraphRAG has an AI read through the whole corpus once and build a **map of who/what relates to whom** — a knowledge graph, like a mind-map with people, places, and organizations as dots and their relationships as lines connecting them. It then groups tightly-connected clusters of dots into neighborhoods (called **communities** — think "everything related to the tech industry" vs. "everything related to health policy"), and has the AI write a short summary of each neighborhood in advance. When you ask a big-picture question later, instead of searching for matching paragraphs, the system pulls together the relevant neighborhood summaries and stitches them into one answer.

## Why does it matter?

Most RAG systems fail silently on "sensemaking" questions — the kind where you're trying to understand a whole situation, not look up one fact. Examples: "What are the main risks across all our customer contracts?", "What themes show up across this year's incident reports?", "What does this 200-podcast-episode archive collectively say about a topic?" A standard RAG chatbot will confidently answer these by grabbing a random handful of matching snippets and generalizing from them — which produces answers that sound plausible but miss most of the picture. GraphRAG is built specifically so the AI has actually "seen" a compressed version of the whole corpus before answering, not just a few matching fragments.

## How does it work?

Think of it as building a library's index card system, but smarter, then answering questions in two stages:

1. **Read and extract.** The corpus is split into chunks (like pages). An AI reads each chunk and pulls out the important entities (people, places, organizations) and the relationships between them — plus any solid factual claims. Duplicate mentions of "NeoChip" across many chunks get merged into one entity card.
2. **Build the map.** All those entities and relationships become a graph — dots and connecting lines. The system then automatically groups the graph into nested neighborhoods of closely related dots, using an algorithm called **Leiden** — first broad neighborhoods, then sub-neighborhoods within those, like continents → countries → cities.
3. **Pre-write neighborhood summaries.** Starting from the smallest neighborhoods and working up, an AI writes a short report for each one — "here's what this cluster is about." Bigger neighborhoods' summaries are built by combining the summaries of their sub-neighborhoods, so the system never has to re-read the raw text at query time.
4. **Answer questions with map-reduce.** When you ask a global question, every relevant neighborhood summary is asked, in parallel, "does this help answer the question, and how helpful is your partial answer (0-100)?" (the **map** step). The most helpful partial answers are then combined by another AI pass into one final, coherent answer (the **reduce** step) — the same map-reduce idea used in big-data processing, just applied to AI-generated summaries instead of numbers.

## Where can this be used?

- **Internal knowledge bases** where people ask "what are the recurring issues/themes/risks across X?" rather than "find me the one document about Y."
- **Long-running document collections** (contracts, research archives, support tickets, meeting transcripts) that get queried repeatedly with different big-picture questions — the summaries are built once and reused for every future query.
- **Intelligence/investigative analysis**, where the value is in connections between many separate pieces of information, not any single document.
- Less suited to one-off fact lookups ("what's the phone number on page 12?") — for that, plain vector RAG is cheaper and just as good, and actually wins on giving short, direct answers.

## Conclusions & takeaways

- GraphRAG isn't a universal replacement for standard RAG — it specifically targets whole-corpus sensemaking questions, and standard vector RAG remains the more direct, cheaper choice for fact lookup.
- The one-time cost is real: building the graph and all the community summaries requires many LLM calls, before any question is even asked (indexing took ~4.5 hours on one ~1M-token corpus in this paper's setup).
- Once built, the cheapest tier of summaries (the broadest, top-level communities) already captures most of the benefit at a fraction of the cost of feeding the whole corpus through map-reduce every time — a good default for repeated big-picture queries over the same data.
- A month from now, remember the core reframe: some questions need "have you read the whole thing and connected the dots" rather than "can you find the one matching paragraph" — and that's a structural difference, not something fixable by fetching a few more chunks.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| RAG (retrieval-augmented generation) | Feeding an AI a question plus a handful of relevant retrieved documents, so it answers from those instead of just its trained memory. |
| Vector RAG | The standard flavor of RAG: finds relevant text by comparing "meaning fingerprints" (embeddings) of the question and the documents. |
| Sensemaking | Questions that require understanding an entire body of information and how its parts connect, not just looking up one fact. |
| Knowledge graph | A map of entities (people, places, things) as dots and their relationships as connecting lines, usually built by an AI reading text. |
| Community detection | An algorithm that finds tightly-connected clusters ("neighborhoods") within a graph. |
| Leiden algorithm | A specific, high-quality community-detection algorithm used here to build the neighborhood hierarchy. |
| Community summary | A short AI-written report describing what one graph neighborhood is about. |
| Map-reduce summarization | Answer generation in two stages: many independent partial answers generated in parallel (map), then merged into one final answer (reduce). |
| LLM-as-judge | Using a second AI model to score or compare the quality of two AI-generated answers, instead of a human grader. |
| Comprehensiveness / Diversity / Empowerment / Directness | The paper's four scoring criteria for answer quality: how much ground it covers, how many distinct perspectives it offers, how well it helps the reader form their own judgment, and how concise/to-the-point it is. |
| Context window | The maximum amount of text an AI model can look at in one go when generating a response. |
