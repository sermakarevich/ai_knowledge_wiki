> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# EvoOntology: A Self-Evolving Ontology Layer for Data Agents — In Plain Language

## What is this about?
Data agents answer plain-English questions over messy, scattered data:
spreadsheets, CSV files, documents, charts, logs, and databases.
EvoOntology adds a helper layer between that raw data and the agent.
Think of it as a living glossary plus map: it records what business
concepts mean, where they live in the data, and what rules apply.
The key idea is that this glossary builds itself and keeps improving
by watching how the agent actually works, instead of relying on
experts to write and maintain it by hand.
The paper tests this on three benchmarks covering multi-source
research, business analytics, and text-to-SQL questions.

## Why does it matter?
Today's agents struggle with what the paper calls the agent–data gap.
The data sits outside the agent, reachable only through generic tools
like SQL queries and file readers, and the agent starts out knowing
almost nothing about where things are or what they mean.
Two current fixes both fall short.
Letting the agent poke at raw data works for small cases but turns
into slow, repetitive guessing on large, mixed-up sources.
Hand-built dictionaries of metrics and schemas help, but they are
expensive to create, hard to keep current, and too big to fit into
the agent's limited working memory.
A static cheat sheet pasted into every prompt can even hurt accuracy.
EvoOntology matters because it offers a middle path: a compact,
searchable memory that adapts itself to new data and new agents.

## How does it work?
Picture three connected parts: a knowledge store, a rulebook for what
the store can hold, and a pair of lookup tools.
The knowledge store holds four kinds of notes: Terms (concepts like
"profit" or "legality status"), Mappings (which columns and tables
each concept points to), Constraints (rules like "profit equals
revenue minus cost" or "revenue excludes cancelled orders"), and
Evidence (examples and value samples backing each claim).
The rulebook, called the Schema Layer, defines what those notes look
like and how they can link together.
The tools are simple: browse finds relevant concepts for a question,
and resolve pulls up full details plus linked rules and evidence.
Only a short menu goes into the agent's prompt; details load on demand.

Building happens in two phases.
First, a builder agent scans typical past questions, proposes likely
concepts, and probes the real data to check types, values, and links.
Only claims that check out get saved, with their supporting evidence.
Second, the system learns from experience.
It reviews saved runs of the agent, spots repeating failures, and
decides whether the problem is missing knowledge, a hard-to-use tool,
or a gap in the rulebook.
It then makes one small fix at a time and keeps it only if side-by-side
testing on held-out questions shows a clear improvement.
Rejected fixes are logged so the same bad idea is not tried again.
One example: the system learned that "banned card" needs both a status
of Banned and a specific game format, and added that rule without
rewriting anything else.

## Where can this be used?
Anywhere an assistant must answer questions over many connected data
sources without constant expert babysitting.
Business intelligence is a natural fit: recurring metrics such as cost,
revenue, and profit that appear in different tables with different
currency or time-grain quirks.
Data research over filings, tables, and documents is another, since the
agent otherwise wastes turns hunting for the right file or column.
Text-to-SQL products benefit too: grounding a question to the right
fields and filters before writing the query cuts errors.
Because each agent model develops its own version of the layer, teams
running several models would maintain one shared starting glossary
plus small per-model tuned copies.
The token savings also matter for cost-sensitive deployments.

## Conclusions & takeaways
The headline result is that the evolving layer beats doing nothing,
beats pasting in a static dictionary, and beats simple memory of past
runs across six different agent models.
On multi-source research questions, full-task accuracy rose by about
18 points on average; on database questions, correct answers rose by
about 7 points alongside more efficient queries.
Roughly two-thirds of the gain came from the initial auto-built
glossary and one-third from the later self-improvement loop.
Safety checks mattered: removing the test-before-keeping step was the
most damaging change in ablations, and field mappings plus supporting
evidence were the most load-bearing pieces of knowledge.
Growth leveled off after about three rounds, and total tokens per task
fell by roughly 20% because shorter, better-aimed runs outweighed the
slightly longer prompts.
The bottom line: a small, tested, self-updating map beats both blind
exploration and a giant static manual.

## Jargon decoder
| Term | Plain meaning |
|---|---|
| Ontology layer | A shared glossary-plus-map linking business ideas to actual data fields |
| Agent–data gap | The agent can query data but starts out not knowing where anything means what |
| Term | One named concept, e.g. "legality status" or "total cost" |
| Mapping | The pointer from a concept to real columns, tables, and join paths |
| Constraint | A rule for correct use, e.g. which filters must go together |
| Evidence | Saved samples and observations proving a concept really matches the data |
| browse / resolve | Look up relevant concepts, then fetch full details on demand |
| Paired validation | Keep a fix only if it beats the old version on the same test questions |
| Trajectory | The saved step-by-step record of one agent run, used as learning material |
