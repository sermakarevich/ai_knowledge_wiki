> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# When to Use Graph Engineering

**In one sentence:** Graph engineering is powerful but should be reserved for genuinely complex, multi-part problems rather than simple tasks where a plain LLM call is enough.

## Key points

- Graph engineering can technically be applied to anything, but you should not use it for everything.
- Decomposing a simple task — like summarizing a single PDF — into a multi-node graph is "overdoing it": unnecessary overhead for a problem that doesn't need it.
- If a plain LLM call solves a task using X tokens, using a single agent costs roughly 4X the tokens (i.e., ~4x the overall base cost).
- Using a graph of agents (graph engineering) wastes roughly 15X more tokens than the plain LLM call baseline — ~15x the cost.
- The decision framework: choose between a simple LLM call, an agent, harness engineering, loop engineering, or graph engineering based on the task's actual complexity.
- The rule of thumb is to pick the cheapest technique that fits the problem, not to default to the most sophisticated one.
- "Can you use graph engineering everywhere?" is framed as a common interview question — the expected answer is that you *can*, but you *shouldn't* for simple problems, precisely because of these cost multipliers.

---

## The overdoing-it problem

A simple, single-task problem — for example, summarizing a particular PDF — needs neither agents nor a graph. If you try to break it down into multiple parts and route it through a multi-node graph, that is "overdoing" it: the structure you add brings no benefit, only overhead. The presenter's point is that graph engineering exists for genuinely multi-part problems; forcing it onto a one-shot task is misapplying the tool.

## Cost multipliers vs a plain LLM call

| Technique | Cost vs plain LLM call |
|---|---|
| Plain LLM call (baseline) | X tokens |
| Single agent | ~4X tokens / ~4x cost |
| Graph of agents (graph engineering) | ~15X tokens / ~15x cost |

The multipliers are approximate, from the presenter: a single agent costs about 4x the base task, and a graph of agents about 15x. So every extra layer of sophistication should be justified by the task, not assumed.

## Decision framework

The practical rule: match the technique to the actual complexity of the task. Ladder from cheapest to most sophisticated — simple LLM call → agent → harness engineering → loop engineering → graph engineering — and pick the one that genuinely fits. Do not default to the most sophisticated option. The presenter frames this as a common interview question: "Can you use graph engineering everywhere?" Yes, you can; but because of the 4x/15x cost multipliers, you should not.

---

**Covers:** 06:23-08:26
