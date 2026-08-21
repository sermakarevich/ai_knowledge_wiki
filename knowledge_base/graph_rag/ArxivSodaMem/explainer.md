> [[index|Wiki]] | [[summary|Summary]]

# SodaMem — In Plain Language

## What is this about?

Imagine an AI assistant that chats with you every day for months. Somewhere along the way, you mentioned you love spicy food. A few weeks later you said you're cutting back on spice. Tonight you ask, "what should I cook?" A dumb assistant just keeps a running diary of everything you've ever said and grabs whichever line looks most relevant — it might quote your old "I love spicy food" line back at you, which is now wrong.

SodaMem is a paper about giving AI assistants a smarter kind of memory: not a diary, but something closer to a court case file. Every fact the assistant remembers about you is written down together with (a) the exact sentence you said it in, so it can always prove where the fact came from, (b) when you said it and when it happened, and (c) whether a newer fact has replaced it. When your preference changes, the old fact isn't deleted — it's marked "no longer current," with a link pointing to the fact that replaced it. That way the assistant can always answer "what's true now?" while still being able to explain "here's how your preference changed."

## Why does it matter?

Most memory systems for AI agents today are basically a big pile of saved sentences that get searched by "which sentences sound similar to the question." That works fine for finding a needle in a haystack, but it falls apart in four common situations: (1) you change your mind and the old and new statements both get retrieved as if they're equally true; (2) you ask something that depends on time ("what did I say most recently about X?") and the assistant has no sense of ordering; (3) you want to know *why* the assistant believes something, and it can't point to the actual sentence; (4) you ask something that requires connecting two separate facts, and a similarity search alone won't make that connection. If AI assistants are going to be useful over weeks and months — not just single conversations — these four problems have to be solved, not papered over.

## How does it work?

Think of it as a three-step assembly line:

1. **Filing (Ingest).** Every time you say something, an LLM reads it and pulls out structured "fact cards" — who, what, when, and (critically) the exact quote it came from. If the AI can't point to your exact words, the fact card gets thrown out. This is like a fact-checker who refuses to write anything down without a direct quote.
2. **Filing cabinet (Store).** These fact cards go into a searchable filing cabinet that's also a web of connections: cards link to newer cards that replaced them, to related people/things, and to the original conversation. The cabinet is indexed two ways — by keyword (like a library card catalog) and by meaning (so paraphrases still get found).
3. **Answering (Answer).** When you ask a question, a "planner" — think of it as a research assistant — goes searching through the cabinet using three different search strategies at once (keyword search, meaning-based search, and following connections in the web), then scores each fact by how many independent searches turned it up (the more corroboration, the more confident). If your question mentions a rough time ("a couple months ago"), that nudges the ranking rather than filtering things out entirely — so a fuzzy memory of "when" doesn't cause the right fact to be thrown away. Finally, a separate "writer" takes the best evidence and composes an answer, always citing which fact cards it used.

## Where can this be used?

- **Personal AI assistants** that need to remember your evolving preferences, plans, and facts about your life across weeks or months of conversation.
- **Customer support or CRM agents** that need an auditable trail — being able to show "here's the exact message where the customer said X" matters for trust and compliance.
- **Any long-running agent** (a coding agent tracking decisions across a multi-week project, an operations agent tracking configuration changes) where "what's the current state, and how did we get here" both matter.
- Less suited to short, one-off conversations where there's nothing to update or supersede — the machinery is overhead if there's no history to manage.

## Conclusions & takeaways

SodaMem's big idea is that "currency" (knowing what's true *now*) should be handled by the memory system's structure — explicit supersession edges — rather than left to the language model to figure out at answer time by reading a jumble of old and new statements. Combined with mandatory provenance (never store a fact you can't point to in the source text) and a cheap Flash-tier model, the paper reports getting 92.8% accuracy on a standard long-memory benchmark for about $0.0016 per question — competitive with far more expensive systems. The honest caveat: this is one run, graded by the same model that answered the questions, and cost comparisons with other systems were reconstructed from published numbers rather than run head-to-head under identical conditions.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| FactEvent | The paper's basic "fact card": a structured record of one thing learned about the user, with type, time, and the exact quote it came from |
| Provenance span | The exact snippet of the original conversation a fact is quoted from — the "receipt" that proves the fact wasn't made up |
| Supersession | Marking an old fact as replaced when a new, conflicting fact arrives — like crossing out an old address when you get a new one |
| SUPERSEDES / CONTRADICTS / UPDATES | The three kinds of "this fact relates to that older fact" links the system draws between facts |
| BM25 | A classic keyword-search scoring method (like a smarter version of Ctrl+F) used alongside meaning-based search |
| Connection-density fusion | Ranking a fact higher the more independent search methods (keyword, meaning, graph links) all point to it, instead of trusting one similarity score |
| Planner–reader loop | Splitting "go find evidence" (the planner, which can use tools) from "write the final answer" (the reader) into two separate steps/models |
| LongMemEval | A public benchmark of 500 questions testing whether an AI assistant can correctly answer questions about a long, multi-session chat history |
