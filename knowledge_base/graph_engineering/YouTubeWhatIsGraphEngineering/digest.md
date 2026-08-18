> [[index|Wiki]] | [[summary|Summary]]

# What Is Graph Engineering? — Digest

The whole video at medium depth: every page's headline claim and key points, in order. ~3 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-graph-engineering-defined|Graph Engineering Defined]]

**In one sentence:** Graph engineering is simply a new name for what multi-agent frameworks like LangGraph, Google ADK, and Microsoft AutoGen have done for years — orchestrating multiple "self-prompting" loop-engineering solutions (each pairing an agent with an evaluator) as coordinated nodes to achieve a goal.

- The agentic-AI technique stack has five layers: prompt engineering, context engineering, harness engineering, loop engineering, and graph engineering — in increasing scope.
- Prompt, context, and harness engineering are applied on the *input side inside* an AI agent; loop engineering is applied *outside* the agent.
- Loop engineering is a technique where multiple agents work together so the solution as a whole "self-prompts itself."
- A single agent cannot self-prompt itself in a loop — that is an incorrect technique that cannot work; instead, agent two evaluates agent one's response and re-prompts agent one.
- That two-agent arrangement (producer + evaluator) is called a "self-prompting solution."
- Graph engineering is what emerges when multiple self-prompting solutions (e.g., solution one as a "viewer agent," solution two, solution three) are arranged in a coordinated manner.
- In a graph, each node can be an agent, a self-prompting (loop-engineering) solution, or a direct LLM call; nodes are orchestrated so that together they achieve the goal.
- The presenter stresses this is *not* a new technique — LangGraph, Google ADK, and Microsoft AutoGen have used it for many years; anyone who implemented those frameworks has already done graph engineering, and only the name is new.

## 2. [[wiki/02-graph-engineering-vs-graphrag|Graph Engineering vs GraphRAG]]

**In one sentence:** GraphRAG and graph engineering both use nodes and edges, but GraphRAG nodes are static things that represent entities and take no action while its edges carry no data, whereas graph-engineering nodes actively take action (agents, loop parts, direct LLM calls) and data flows along the edges from node to node.

- Both graph engineering and GraphRAG use the vocabulary of "node" and "edge"/"relationship", which makes the two frameworks look superficially similar.
- In GraphRAG, nodes represent things/entities — they represent something static and take no action at all.
- In graph engineering, nodes take action: a node can be an agent, multiple agents forming part of a loop, or even a direct LLM call.
- In GraphRAG, edges (relationships) only tell about the relationship between nodes; there is no data flowing between them.
- In graph engineering, data actively flows from one node to another node along the relationships/edges.
- Together, the passive nodes and data-less edges of GraphRAG mean it fundamentally differs from the action-taking, data-carrying structure of graph engineering.
- Consequently, GraphRAG cannot be equated with graph engineering, despite the shared node/edge terminology.

## 3. [[wiki/03-when-to-use-graph-engineering|When to Use Graph Engineering]]

**In one sentence:** Graph engineering is powerful but should be reserved for genuinely complex, multi-part problems rather than simple tasks where a plain LLM call is enough.

- Graph engineering can technically be applied to anything, but you should not use it for everything.
- Decomposing a simple task — like summarizing a single PDF — into a multi-node graph is "overdoing it": unnecessary overhead for a problem that doesn't need it.
- If a plain LLM call solves a task using X tokens, using a single agent costs roughly 4X the tokens (i.e., ~4x the overall base cost).
- Using a graph of agents (graph engineering) wastes roughly 15X more tokens than the plain LLM call baseline — ~15x the cost.
- The decision framework: choose between a simple LLM call, an agent, harness engineering, loop engineering, or graph engineering based on the task's actual complexity.
- The rule of thumb is to pick the cheapest technique that fits the problem, not to default to the most sophisticated one.
- "Can you use graph engineering everywhere?" is framed as a common interview question — the expected answer is that you *can*, but you *shouldn't* for simple problems, precisely because of these cost multipliers.

## The argument in five moves

1. Agentic-AI techniques form a stack — prompt, context, and harness engineering inside the agent, loop engineering outside it.
2. Loop engineering composes into graph engineering when multiple self-prompting (producer + evaluator) solutions are coordinated together.
3. A node in that graph can be an agent, a loop-engineering solution, or a direct LLM call — and none of this is new, just renamed.
4. Graph engineering is distinct from GraphRAG: its nodes act and its edges carry data, unlike GraphRAG's static nodes and data-less edges.
5. Because a single agent already costs ~4x and a graph of agents ~15x a plain LLM call, apply the cheapest technique that fits the task's actual complexity.
