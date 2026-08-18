> [[index|Wiki]] | [[summary|Summary]]

# Graph Engineering for Multi-Agent Systems — In Plain Language

## What is this about?

Imagine you've built a small team of AI helpers instead of one AI assistant: one drafts something, another checks it, a router decides which specialist handles a request, and occasionally a human has to sign off before something risky happens. "Graph engineering" is the name for treating that team's org chart — who talks to whom, in what order, under what rules — as a real, explicit thing you design and can look at, rather than something that just emerges from a pile of code.

This article is not about the diagram itself so much as what it takes to run that org chart at a company, safely and affordably. It's written by a vendor (TrueFoundry) that sells a "gateway" (a checkpoint all the AI traffic flows through) and a managed runtime for AI agents, so a lot of the article is also implicitly explaining why you'd want their product.

## Why does it matter?

A single AI assistant is easy to reason about: one thing happens at a time, and if it misbehaves, you can look at the one conversation. A team of AI agents is much harder — one agent's output becomes another's input, agents can call tools and spend money on your behalf, and a bug or malicious instruction can hop from one agent to another. Without deliberate design, you end up with a system where nobody can answer basic questions after an incident: who did this, what did it cost, was it supposed to be allowed, and did a human ever actually see it before it happened?

## How does it work?

The article's structure, walked through step by step:

1. **Draw a boundary.** First, it separates "graph engineering" (designing the team) from "knowledge-graph engineering" (a completely different, older field about databases shaped like graphs of facts). Same word, unrelated meaning — don't confuse them.
2. **Stack it on what came before.** It places graph design on top of three lower layers that already existed: writing a good instruction for one AI call (prompt engineering), controlling what information the AI can see (context engineering), and controlling one AI agent's repeat-until-done cycle (loop engineering). None of these go away when you add a graph — a team of unreliable individual workers is still unreliable, no matter how well-organized the org chart is.
3. **Give everyone an ID badge.** In an enterprise, every AI agent, tool call, and team needs to be traceable to who's responsible — like an ID badge that gets checked at a shared front desk (the "gateway") rather than everyone deciding for themselves who's allowed to do what.
4. **Track spending like a shared credit card system.** Because an AI team can spawn many calls (one request triggering ten sub-tasks, or retries after failures), the article proposes attaching a label to every single call — which graph, which run, which specific worker — so spending limits and rate limits can be set per team without one team's usage blowing another team's budget.
5. **Keep two logbooks and cross-check them.** One logbook (the orchestrator) records which workers actually did what, in what order. A separate logbook (the gateway) records what each call to the AI model or a tool actually cost and whether it was allowed. Neither logbook alone tells the whole story — you need both, matched up.
6. **Put a human at the dangerous doorway.** Before an AI agent does something consequential (like deleting data or sending an email), a human approval step can be inserted right at that doorway, turning "the AI decided to do X" into "the AI proposed X, and a human said yes."
7. **Use the tracking data to make it cheaper.** Once you know exactly which worker is expensive, you can swap that one worker for a cheaper model, cache answers for repeated questions, or add a backup plan for flaky workers — all without touching the rest of the team.

## Where can this be used?

- Any organization running more than one AI agent in production — customer support bots that hand off to specialists, code-review pipelines with a drafting agent and a checking agent, or research pipelines with a search agent feeding a writing agent.
- Security and compliance teams needing to answer "who did this and was it approved" after an AI-driven incident.
- Finance/platform teams needing to attribute AI spending to the right cost center instead of one shared, unexplained bill.
- Teams evaluating whether to adopt a gateway product (TrueFoundry's, or a competitor's) — the checklist works as a vendor-neutral requirements list even if you never buy TrueFoundry.

## Conclusions & takeaways

A month from now, the one thing worth remembering: a multi-agent system needs the same operational disciplines as any other production system running with real permissions and a real budget — identity, spending controls, approval gates, and two matching records of what happened — and none of that is optional just because the workers are AI instead of people. The honest limitation: this is a vendor's blog post, so treat the specific "our gateway measures 3-4ms latency and 350+ RPS" claims, and the assumption that you need a product like this at all, with the same skepticism you'd apply to any vendor pitch — the checklist is useful even if you build the plumbing yourself.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Graph engineering | Designing a multi-agent AI system's org chart — who talks to whom, in what order — as an explicit, inspectable thing. |
| Node | One worker in the graph: could be an AI agent, a plain piece of code, a router, or a human approval step. |
| Edge | A connection between two nodes — who can send work or information to whom. |
| Org graph | The slow-changing chart of who exists and who's responsible — updated rarely, like a company's org chart. |
| Work graph | The fast-changing record of what's actually happening right now on one specific task — like today's to-do list, not the company handbook. |
| Gateway | A shared checkpoint all AI/tool traffic passes through, where identity, spending limits, and rules get enforced in one place instead of scattered across every agent's code. |
| Virtual account | A labeled sub-budget (like a company credit card assigned to one team) used to track and cap spending per team or per worker. |
| Guardrail hook | An automatic check inserted right before or after an AI call or tool use — checking the question going in, the answer coming out, or the tool call itself. |
