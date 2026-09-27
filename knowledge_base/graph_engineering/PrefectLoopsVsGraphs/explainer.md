> [[index|Wiki]] | [[summary|Summary]]

# Loops vs. Graphs — In Plain Language

## What is this about?

Imagine you're teaching an AI assistant to handle customer refunds. The simplest way is to give it a checklist ("check these 10 things") and a button that issues the refund, then trust it to only push the button when the checklist passes. Prefect's argument in this article is that this is a bad idea, because if the AI misuses the button, it usually *also* tells you everything went fine — so you find out something went wrong from an angry customer, not from your monitoring.

Their fix is to draw the whole process as a flowchart made of boxes and arrows — a "graph." One box does the checking; only a *different* box — reached only after the checking box approves — is ever handed the refund button, and even then it can only be used once, for one specific customer. This article is Prefect explaining why they think drawing agent workflows as flowcharts (graphs) beats the current default of "just let the AI loop until it decides it's done" (loops), and why their own product is being rebuilt around that idea.

## Why does it matter?

If you're building an AI agent for anything beyond a personal chatbot — something that touches money, customer data, or an action you can't take back — the difference between "one AI does everything" and "the risky step is walled off behind a checkpoint" is not a small design detail. It's the difference between a system you can audit after something goes wrong and one where the failure and the false all-clear happen in the same breath. This article is worth reading because that design habit (separate judgment from action, checkpoint between them) is useful regardless of which company's software you use to build it.

There's also a business-vs-individual distinction worth internalizing: a person casually asking a chatbot a question doesn't care whether the same question produces the exact same reasoning path twice. A business running a workflow that decides refunds, insurance claims, or account changes does care — regulators, auditors, and angry customers all eventually ask "why did the system do that, and would it do the same thing again given the same facts?" Bare loop engineering has no good answer to that question; the article's pitch is that an explicit graph does.

## How does it work?

Think of it as three stages, each stage adding more structure than the last:

1. **Prompt engineering.** One request, one response. No automation around it — a person reads the output and decides what happens next.
2. **Loop engineering.** The AI repeats a step automatically — try, check, try again — until some condition says "done." Powerful, but in practice it collapsed in public discourse into the "Ralph loop," a stripped-down, oversimplified version that became the thing everyone associates with looping, even though more careful practitioners had already moved past it.
3. **Graph engineering (Prefect's version: "directed agentic graph").** Instead of one loop doing everything, you draw the process as connected boxes (nodes) and arrows (edges). Each box can have its own tools, its own permissions, and even its own underlying AI model. Arrows are allowed to loop back to an earlier box (a "cycle") — that's the one deliberate difference from the classic flowchart rule ("DAG") used in traditional data pipelines, which forbids looping back at all.

The security payoff comes from where you draw the boxes. If the "figure out whether a refund is owed" box and the "issue the refund" box are the *same* box, the AI holds the dangerous capability the whole time it's also making judgment calls — and it can misreport what it did. If they're *separate* boxes, the dangerous capability doesn't exist yet during the judgment phase, and appears — locked to one specific case, one-time-use — only after a decision point that the workflow (or a human) controls.

Human approval fits into this same picture: it's just another box. An AI does its part, hands off to an "approval" box where a person decides, and only afterward do downstream AI boxes continue. Nothing special has to be bolted on for humans to be part of the flow.

## A worked example: the refund agent

Walking through the article's own example end to end makes the pattern concrete:

1. **Node 1 — Diligence.** A customer asks for a refund. An AI agent reads the order history, checks the ten eligibility rules, and decides "eligible" or "not eligible." This node has no tool that can actually issue money — it can only decide.
2. **Edge.** The workflow reads the diligence node's decision and routes accordingly: "eligible" goes to Node 2; "not eligible" goes to a rejection node instead.
3. **Node 2 — Issue refund.** Only now does a refund-issuing tool exist, and only in this node. It's pre-locked to the one customer and order in question, and it can be used exactly once. Once it fires, this node's job is done.
4. **Why this matters in production.** Under the old, single-node design, a bug or a prompt-injection attack could make the agent issue a refund it shouldn't have, and the same broken run would also report "all checks passed, nothing unusual happened" — because both actions come from the same untrustworthy process. Under the graph design, the dangerous tool simply doesn't exist yet during the part of the process an attacker or bug is most likely to target (the judgment step), which shrinks the blast radius of anything going wrong there.

The same shape works for anything with a "figure out what to do, then do something you can't undo" structure — approving a refund, deleting a customer record, pushing a config change, sending an email blast.

If a human needs to sign off before Node 2 runs, that's not a special case — you just insert an "Approval" node between diligence and refund-issuance. The approval node isn't an AI step at all; it's a person looking at the diligence node's output and clicking approve or deny, and the edge out of that node is decided by their click rather than by an AI's reasoning. From the graph's point of view, a human decision and an AI decision are the same kind of thing: a node that produces an outcome the next edge can branch on.

## Common misconceptions

- **"A graph is just a fancier loop."** Not quite — a loop is what happens *inside* one node if that node repeats a step; the graph is the map of which node hands off to which other node, and under what condition.
- **"More nodes is always better design."** The article explicitly warns against this: a ten-step process doesn't need ten nodes. Extra nodes that don't earn their keep (no monitoring, no intervention point, no retry logic riding on them) just drag the design back toward plain loop engineering with extra steps.
- **"LangGraph and this article's 'directed agentic graph' are the same thing."** They operate at different scales — LangGraph typically graphs the decisions *inside* one agent (which tool to call next); Prefect's version graphs the handoffs *between* several complete, independent agent invocations.

## Where can this be used?

- **Any workflow that touches an irreversible or costly action** (refunds, deletions, sending money, changing production config): separate the "decide" step from the "act" step into different nodes, and only expose the risky tool inside the "act" node.
- **Any process that currently needs a human sign-off somewhere in the middle:** model that sign-off as its own node instead of bolting an approval flag onto a tool call.
- **Deciding whether you even need a multi-node design at all:** the article's own test is whether monitoring, human intervention, retry logic, or programmatic injection of logic would actually matter at a given point — if none of those apply, that point doesn't need to be its own node.
- **Comparing vendor claims about "graph" products:** the jargon decoder below helps you tell whether a tool is graphing the inside of one agent (LangGraph, Pydantic AI) or orchestrating across several complete agents (what Prefect claims to do), since the two are easy to conflate.

## What's the catch?

This is a company blog post from a vendor whose product bets on exactly this idea, published shortly after Dagster (a company with its own graph-shaped orchestration product) was folded into Prefect. The core security argument — don't let one step hold both "figure out what to do" and "do the dangerous thing" — is sound engineering advice and isn't unique to Prefect's product; you can apply it with plain code, LangGraph, Pydantic AI, or a hand-rolled state machine. The article itself is candid that "directed agentic graph" is mostly a repackaging of long-standing orchestration ideas — it estimates its own contribution as roughly 95% established practice and only 5% genuinely new. There are no benchmarks, no named customers, and no code shown to back up the claims, so treat this as a well-argued design principle rather than proof that Prefect's specific tooling is required to get the benefit.

## Conclusions & takeaways

A month from now, remember this: the reason to reach for a graph isn't that it sounds more sophisticated than a loop — it's that a graph gives you a specific place (a node boundary) to put a checkpoint, a permission change, or a human decision. If nothing in your workflow needs that checkpoint, a single loop (or even a single prompt) is still the right answer, and adding nodes just for the sake of it drags you back toward "loop engineering wearing a graph costume." The one habit worth keeping regardless of tooling: never let the same step hold both a dangerous capability and the only account of whether that capability was used correctly.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Graph | A diagram of boxes (nodes) connected by arrows (edges) — the computer-science meaning, like a subway map or an org chart, not a bar chart. |
| Node | One box in the graph: one unit of work. Can be an AI step, a human approval, plain code, or simply waiting for an external event. |
| Edge | An arrow between two nodes meaning "after this happens, go here next." Which arrow gets followed depends on what happened in the node before it. |
| DAG (Directed Acyclic Graph) | A flowchart where arrows only move forward and never loop back to a box already visited — the structure behind traditional data-pipeline tools. |
| Directed agentic graph | Prefect's term for an agent workflow drawn as a flowchart that, unlike a DAG, is allowed to loop back on itself, while still giving each box its own tools, permissions, and model. |
| Loop engineering | Building an AI system that repeats a step — try, check, try again — until it decides it's done, without a human approving each cycle. |
| Ralph loop | A very stripped-down way of doing loop engineering that went viral and became (unfairly, per this article) the poster child for the whole idea. |
| Capability segregation | Splitting "figure out what to do" from "actually do the risky thing" into separate steps, so the risky step is reachable only after a checkpoint. |
| MCP (Model Context Protocol) | A standard way for AI models to connect to external tools and data sources; mentioned only in passing as a topic the authors will field reader questions on. |
| Orchestration / orchestrator | The overall system deciding which node runs next and tracking where a workflow currently is — the "conductor" of the process. |
| Reproducibility | Running the same process twice and getting a comparably consistent path or decision, not just a similar-looking final answer — what businesses need in order to audit and trust a system. |

