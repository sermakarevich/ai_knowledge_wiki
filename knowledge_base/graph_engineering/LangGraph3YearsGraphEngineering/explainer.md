> [[index|Wiki]] | [[summary|Summary]]

# 3 Years of Graph Engineering with LangGraph — In Plain Language

## What is this about?

Imagine you're designing a factory floor rather than hiring one super-smart-but-occasionally-unreliable employee to do everything by themselves. A factory floor has fixed stations — one worker always tightens the same bolt the same way — and a few decision points where a supervisor looks at the piece and decides which station it goes to next. This article, written by two people who built LangGraph (a popular tool for building AI agents), argues that this is exactly how you should think about building an AI agent: some parts of the job should always happen the same way (fixed "stations"), and only the genuinely judgment-heavy parts should be handed to the AI model.

They call this "graph engineering" because the factory floor, drawn as a diagram, looks like a graph in the mathematical sense: circles (called "nodes") connected by arrows (called "edges"). A node is a station — it could be a plain computer program, a single call to an AI model, or even a full AI agent doing its own multi-step job. An edge is an arrow saying "after this station, go here next" — sometimes that's always the same next station, sometimes it depends on what happened at the last one.

After three years of running LangGraph in the real world, the authors also share three hard lessons and one big-picture claim: none of this — graphs, loops, "harnesses" — is actually a new idea. It is the same old engineering principle of "figure out what has to be reliable and lock that down, then let judgment handle the rest," just wearing a new name.

## Why does it matter?

If you let an AI model decide every single step of a task from scratch, you get something that's unpredictable, slow, and expensive — like asking a new employee to reinvent the company's shipping process from first principles every single day. If you hardcode every single step instead, you lose the AI's ability to actually think through the parts of the job that genuinely require judgment, like reading a confusing customer message and figuring out what they actually want. Graph engineering matters because it gives you a concrete way to draw the line: this part is a fixed process (a node with deterministic code), this part needs a quick judgment call (a node that's one AI call), and this part is complicated enough to deserve its own mini-agent (a node that's a full agent). Getting that split right is often the difference between an AI system that works reliably in production and one that's a fun demo.

## How does it work?

Think of building an agent as answering four questions in order:

1. **Does this task have predictable structure?** If a support ticket always needs to be classified before it's answered or escalated, that's predictable structure — draw it as a graph: classify node → answer node OR escalate node.
2. **Is any part of this task open-ended instead?** Some jobs — like "go do generic research on this topic" — can't be planned out step by step in advance: you don't know how many sources you'll need, or in what order you'll need to read them. For those, don't force a graph; hand the whole job to an "agent harness" (a more flexible AI runtime, like LangChain's Deep Agents) and let it figure out its own plan as it goes.
3. **Does the graph need to loop?** Real work rarely goes in a straight line. An agent might retry a failed step, ask a follow-up question, or wait for a human to approve something before continuing. The authors' key insight: a loop is not a different thing from a graph — it's just a graph with an arrow pointing back to an earlier station. So "loop engineering" (designing systems that repeat themselves intelligently) is really a special case of graph engineering, not a competing idea.
4. **Does the graph need to grow branches at runtime?** Sometimes you don't know in advance how many parallel workers you'll need — like a factory that has to split a big order into an unknown number of smaller boxes depending on how big the order actually is. LangGraph has a feature called `Send` for exactly this: a node can say "spin up however many downstream stations this particular piece of work needs," decided on the fly rather than drawn ahead of time.

Once you've drawn your graph, you can mix and match how "smart" each station is: some stations are plain code (cheap and fast), some are a single quick AI judgment call, and some — increasingly, now that AI agents have gotten good enough to trust — are entire AI agents doing a multi-step job on their own, like a full coding agent that goes off and fixes a bug.

## Where can this be used?

- **Customer support systems** — classify the issue, then route to an answer path, an escalation path, or a human, with loops for follow-up questions.
- **Coding and DevOps agents** — inspect the repository (fixed step), decide what needs fixing (judgment step), then hand the actual fix to a full coding agent (agent step), all inside one graph.
- **Internal knowledge assistants** — a fixed classify → search (across GitHub, Notion, Slack, etc.) → synthesize pipeline, with the model only reasoning at the parts that genuinely need it.
- **Any workflow with a "for each item, do X" step where the number of items isn't known ahead of time** — document processing, multi-source research summarization, batch data enrichment — these are natural fits for the `Send`/map-reduce pattern.
- **Deliberately NOT for** highly open-ended tasks like unconstrained research or exploratory brainstorming — those are better served by a flexible agent harness than by a graph you tried to pre-draw.

## Conclusions & takeaways

A month from now, the one thing worth remembering is the *decision rule*, not the vocabulary: figure out which parts of your agent's job are predictable enough to lock down, put those in fixed or lightly-model-assisted "nodes," reserve full agent autonomy for the genuinely open-ended parts, and don't be afraid of loops — a well-designed cycle (retry, ask, revise, pause-for-human) is a normal, expected shape for a working agent, not a design flaw. The honest limitation to keep in mind: this is one team's (LangChain's) framing of their own product's philosophy, written to make the case for LangGraph — it's a genuinely useful mental model, but it's not a neutral, evidence-backed evaluation of graphs versus other approaches.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Graph | A diagram of circles (nodes) connected by arrows (edges), used here to represent an agent's workflow. |
| Node | One "station" in the graph — can be plain code, one AI model call, or a full AI agent doing its own multi-step job. |
| Edge | An arrow between nodes saying what happens next; either always the same (deterministic) or dependent on what just happened (conditional). |
| DAG (Directed Acyclic Graph) | A graph where the arrows only ever move forward, never loop back — like a one-way assembly line with no rework station. |
| Cycle / loop | An arrow that points back to an earlier station, so work can repeat — e.g., "try again," "ask a follow-up question." |
| State machine | A system that moves between defined situations ("states") based on rules — a graph is one concrete way to build one. |
| `Send` | A LangGraph feature letting one station dynamically spin up however many downstream stations a given piece of work needs, decided at runtime rather than drawn in advance. |
| Map-reduce | Split a big job into many small pieces ("map"), process each separately, then combine the results ("reduce") — the classic case where you don't know the piece count in advance. |
| Agent harness | A more flexible AI runtime (the article names "Deep Agents") that lets an agent plan and improvise its own steps, used instead of a graph when the task is too open-ended to pre-draw. |
| Cognitive architecture | A fancy term for "the structure that encodes how this system is supposed to think and act" — here, the graph itself plays that role. |
| Loop engineering | Deliberately designing the repeating, self-checking parts of an agent system — the article argues this is really just graph engineering applied to a cycle. |
| Harness engineering | Designing the surrounding scaffolding (tools, context, guardrails) that lets an AI model act reliably — grouped here with graph and loop engineering as the same underlying discipline. |
