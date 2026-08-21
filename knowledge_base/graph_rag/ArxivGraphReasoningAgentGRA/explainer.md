> [[index|Wiki]] | [[summary|Summary]]

# Schema-Agnostic Graph Reasoning Agent — In Plain Language

## What is this about?

Imagine dropping a new engineer into a company's codebase they've never seen, with no documentation. A good engineer doesn't try to read every file first — they run `ls` to see what's there, `grep` to search for a keyword, and open (`cat`) just the files that look relevant. They build understanding by poking around, not by memorizing everything up front.

This paper asks: can an AI agent do the same thing with a company's *data*, not just its code? Specifically, with a "knowledge graph" — a web of connected facts that mixes plain-English descriptions ("Rule R7: station 1 only welds carbon frames") with structured tables (spreadsheets of orders, customers, shipments). The authors build such an agent, called GRA (Graph Reasoning Agent), give it seven simple looking-around tools, and test whether it can answer real business questions about a factory without ever being told in advance what the data looks like.

## Why does it matter?

The obvious alternative is to just paste the entire company handbook and every table's structure into the AI's prompt and let it figure things out from there — the "read everything first" approach. That works, but it gets expensive and unwieldy as the amount of data grows, and it forces the model to wade through mostly-irrelevant information for every single question. If an agent can instead look up only what a given question actually needs — the way the engineer greps for one keyword instead of reading the whole codebase — it can be both cheaper and, this paper shows, more accurate.

## How does it work?

1. **The agent starts cold.** It's given seven generic commands — think of a very small, safe subset of Unix commands adapted for a graph instead of a filesystem: `ls` (list what's nearby), `cat` (read one item fully), `grep` (search for an exact word), `sems` (search by *meaning*, not just exact words), `query` (run a safe, read-only database lookup), `think` (scratch space to reason), and `answer` (submit the final answer).
2. **It's asked a question**, e.g. "How many orders were late for each customer segment last quarter?" It has no idea what tables or labels exist yet.
3. **It explores step by step**: list what kinds of things exist → search for "orders" → search for "customer segment" → open the specific table and node it finds → run a small database query to compute the actual number → double check its reasoning → answer.
4. **Two controls test what's really doing the work.** One agent (RSA) uses the exact same explore-then-answer loop but the graph is replaced with plain document chunks — so if it does just as well, the graph itself isn't the secret sauce, the *habit of looking things up selectively* is. Another (SQA) skips exploration entirely and gets everything shoved into its prompt at once, then just writes one database query.
5. **All three are tested on the same set of 258 factory questions**, and it turns out GRA (the graph explorer) wins by about 5 points of accuracy over SQA (the read-everything agent) — while reading less than a third as much text per question — but only edges out RSA by a hair. That tells the authors the big win is "look only at what you need," and the graph structure is a smaller, secondary bonus.

## Where can this be used?

- Enterprise data that's a messy mix of documents, rules, and databases — support ticket systems, ERP/scheduling data, compliance rule books — anywhere a full dump into a prompt would be too large or too stale to maintain.
- The paper's own example: a factory floor manager states a scheduling rule in plain English ("no more than three colour changes per shift"), and the agent checks it against real historical data before it's accepted, catching problems (or confirming feasibility with a quantified risk) that no single spreadsheet would reveal on its own.
- More broadly, any setting where a "junior analyst" AI needs to answer ad-hoc questions over a knowledge base that changes too often, or is too large, to keep rewriting into one giant prompt.

## Conclusions & takeaways

- Giving an AI a small toolbox and letting it explore beats stuffing everything into its context — but only when the model is good at reliably using tools; a model that fumbles tool calls does better with the "give it everything" approach instead.
- Most of the benefit came from *selectively fetching relevant information*, not from the graph's specific shape — a useful reality check against assuming graph structure is inherently magic.
- This is still an early-stage demonstration: the company's data in the test was small enough to fit in a single prompt anyway, so the scenario where "read everything" becomes truly impossible — which is where this approach should matter most — hasn't been tested yet.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Knowledge graph | A network of facts and their relationships — like a mind map made of "this connects to that" links, instead of a table or plain paragraph. |
| Hybrid knowledge graph | A knowledge graph where some parts are plain-English descriptions and some parts are structured database tables, mixed together. |
| Agent | An AI that doesn't just answer in one shot — it takes a sequence of actions (like running tools) to gather information before answering. |
| Tool-calling / tool use | The AI's ability to invoke external functions (like a search or a database query) as part of answering a question, rather than relying only on what it already "knows". |
| Schema-agnostic | Works without being told in advance what the data's structure/vocabulary/table names are — it discovers them itself. |
| ReAct | An earlier technique for AI agents: alternate between "reasoning" (thinking) and "acting" (using a tool), repeating until done. |
| SQL / query | A way of asking a structured database precise questions, like "sum up all late orders for segment X". |
| Token | Roughly a chunk of a word; how much text an AI model has read or written is measured in tokens, and it costs money and time proportional to that count. |
| Full-context / serialize-everything approach | Pasting the entirety of the available documentation and data structure into the AI's prompt up front, instead of letting it fetch pieces as needed. |
| Bootstrap / confidence interval | A statistics technique for saying "we're fairly sure the true accuracy is within this range," accounting for the fact the test set is a limited sample. |
