> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph Engineering Defined

**In one sentence:** Graph engineering is simply a new name for what multi-agent frameworks like LangGraph, Google ADK, and Microsoft AutoGen have done for years — orchestrating multiple "self-prompting" loop-engineering solutions (each pairing an agent with an evaluator) as coordinated nodes to achieve a goal.

## Key points

- The agentic-AI technique stack has five layers: prompt engineering, context engineering, harness engineering, loop engineering, and graph engineering — in increasing scope.
- Prompt, context, and harness engineering are applied on the *input side inside* an AI agent; loop engineering is applied *outside* the agent.
- Loop engineering is a technique where multiple agents work together so the solution as a whole "self-prompts itself."
- A single agent cannot self-prompt itself in a loop — that is an incorrect technique that cannot work; instead, agent two evaluates agent one's response and re-prompts agent one.
- That two-agent arrangement (producer + evaluator) is called a "self-prompting solution."
- Graph engineering is what emerges when multiple self-prompting solutions (e.g., solution one as a "viewer agent," solution two, solution three) are arranged in a coordinated manner.
- In a graph, each node can be an agent, a self-prompting (loop-engineering) solution, or a direct LLM call; nodes are orchestrated so that together they achieve the goal.
- The presenter stresses this is *not* a new technique — LangGraph, Google ADK, and Microsoft AutoGen have used it for many years; anyone who implemented those frameworks has already done graph engineering, and only the name is new.

---

## The agentic-technique stack

The presenter frames agentic AI as a stack of prompting/technique layers ordered by scope:

1. **Prompt engineering** — crafting the prompt itself.
2. **Context engineering** — shaping what context accompanies the prompt.
3. **Harness engineering** — building the harness (tooling, scaffolding) around the model.
4. **Loop engineering** — running agents in evaluation loops.
5. **Graph engineering** — coordinating all of the above at the system level.

Where each applies relative to a single AI agent:

- **Inside the agent, on the input side:** prompt engineering, context engineering, and harness engineering. Whatever you apply to the input side of an individual agent belongs to this inner group.
- **Outside the agent:** loop engineering — it wraps an agent (or agents) in a run/evaluate/re-prompt cycle.
- **The whole thing together:** graph engineering. When you talk not about a single part but about multiple parts of this stack working together — multiple loop-engineering pieces combined — that composite is what graph engineering is. In the presenter's words, graph engineering is "like a multiple loop engineering together."

## Loop engineering recap: self-prompting via evaluation, not self-reference

Loop engineering is a technique where multiple agents work together so the *solution as a whole* tries to self-prompt itself. A critical constraint: **a single agent cannot self-prompt itself** — if one agent tries to prompt its own loop directly, that is the incorrect technique and it cannot work.

The working pattern is a two-agent arrangement:

1. **Agent one** produces a response.
2. **Agent two** evaluates that response.
3. Agent two then re-prompts agent one based on the evaluation.

Viewed as a whole, this producer-and-evaluator team is a **self-prompting solution**: the loop closes not through self-reference but through a second agent's evaluation feeding back into the first agent's prompt.

## From loop to graph: nodes and orchestration

If you take several self-prompting solutions and arrange them in a coordinated manner, the result is what belongs to graph engineering. The presenter's example: name the arrangements **solution one** (a "viewer agent"), **solution two**, and **solution three** — when these solutions are coordinated with each other rather than running in isolation, they form a graph.

In graph engineering you generally create **nodes**. Each node can be one of:

- an **agent**,
- a **self-prompting (loop-engineering) solution**, or
- a **direct LLM call**.

Nodes are **orchestrated** — wired together in a coordinated structure — such that the combined system achieves the overall goal.

Finally, the presenter's framing: this is **not a new technique**. LangGraph, Google ADK, and Microsoft AutoGen have been using this graph-based orchestration for many years, and anyone who implemented LangGraph or AutoGen has already implemented exactly this. Graph engineering is just a new name for a well-established practice — useful to be able to explain at a job or in an interview, but nothing underneath it is new.

---

**Covers:** 00:00-04:15
