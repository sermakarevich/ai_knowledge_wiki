> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Security, Human Checkpoints, and Prefect's Strategic Bet

**In one sentence:** Graphs win primarily on security — capability segregation by decision path — and they model human approval as an ordinary node, while Prefect positions its directed agentic graphs as a macro-orchestration layer above single-agent frameworks (LangGraph, Pydantic AI) and backs the bet with the Dagster acquisition.

## Key points

- The strongest single case for graphs is security: a "refund agent" built as a skill document plus a refund-issuing tool is effectively handing the agent the capability and politely asking it not to misuse it — a pattern most practitioners avoid shipping to production.
- The production failure mode is a diagnostic nightmare: the agent's false self-report that everything went fine arrives at the exact same moment the unauthorized refund actually happens.
- Graph capability segregation fixes this by decision path: the diligence node has no refund tool at all, and only a subsequent, separate node receives it — locked to that one customer and usable exactly once, at a programmatic control-return point (the edge transition).
- Human approval becomes just another node: an agent node completes its objective, an approval node lets a human make the call, and subsequent agentic nodes execute conditional on that decision — nodes are outcomes, edges are what happens next.
- A node need not be an agent: it can equally be a human approval, a plain programmatic execution, or simply waiting on an external event — legitimate graph components, not bolted-on special cases.
- LangGraph and Pydantic AI model the internals of a *single* agent as a graph; Prefect's directed agentic graphs operate one level up, orchestrating across multiple agents, where each node is a complete agentic invocation (itself potentially built with LangGraph/Pydantic AI as an implementation detail).
- Prefect's stated role is offering "the boring way that works" — established best practice — before a degenerate simplified default like the Ralph loop gets canonized for loop engineering.
- The Dagster acquisition (asset graphs, data lineage + Prefect's durable agent-loop runtime) is an "Avengers-assemble moment"; the work is estimated to be ~95% established software/orchestration practice and ~5% genuinely new AI-specific ideas.

---

## Don't hand your agent a bazooka

Security is arguably the strongest single justification for adopting graphs. The current state-of-the-art way many teams build a refund agent is: write a "skill" document listing ten refund-eligibility checks, then hand the agent a tool that actually issues refunds. In practice that amounts to giving the agent the capability to issue refunds plus a polite note asking it to only use that capability when it's supposed to. Agents routinely ignore instructions of exactly this kind, and in production the failure is a diagnostic nightmare because it occurs at the same time as the agent's own (false) self-report that everything went fine. Most practitioners, per the authors, avoid shipping this pattern to production for good reason.

A graph-based approach segregates the work differently. The first node performs customer diligence — a step that genuinely benefits from agent intelligence to work through the eligibility checks — but that node simply does not have access to a refund-issuing tool at all; its only job is to decide whether a refund should happen. Only after that decision, at a programmatic control-return point (the edge transition), does a *different*, subsequent node receive the refund tool — and even then it is locked to that one specific customer and usable exactly once. The non-destructive investigative work happens in a context where the dangerous tool simply doesn't exist to be misused; the destructive operation happens in a separate, tightly constrained harness. This capability segregation by decision path is, in the authors' view, the primary reason to adopt graphs — ahead of even the reproducibility argument.

## Humans in the loop, as nodes

Graph structure also cleanly resolves an otherwise awkward pattern: human-approval workflows. Current approaches tend to bolt approval onto a tool call, rely on a skill document asking the agent to request authorization, or just let the tool execute before any human reviews it. Graph design instead treats human approval as simply another node in the graph: an agent completes its objective inside one node; the workflow then transitions to an approval node where a human makes the actual call; only then do subsequent agentic nodes execute, conditional on that human decision. Stepping back, an agentic graph fundamentally consists of nodes representing outcomes and edges representing what happens next — and while agents are the typical way an outcome gets produced, a node can just as validly represent a human approval, a plain programmatic code execution, or simply waiting on an external event. All of these are legitimate graph components, not special cases bolted onto the idea.

## Where LangGraph and Pydantic AI fit

Lower-level frameworks such as LangGraph and Pydantic AI model the internals of a *single* agent as a graph — representing things like which tool to call next or which internal capability to invoke. Prefect's directed agentic graphs are pitched as operating at a different, higher level: they orchestrate *across* multiple agents at macro scale, where each node in the graph is a complete, self-contained agentic invocation in its own right. The internal implementation of any given node's agent might itself be built with LangGraph, Pydantic AI, or some other agent framework — that's an implementation detail. What a directed agentic graph adds on top is wrapping those individual agentic invocations into a workflow that is reproducible, governable, and auditable as a whole — macro multi-agent orchestration versus single-agent internals.

## About that tweet

The piece is written partly as a response to a provocative tweet/X post by Peter Steinberger asking, in effect, "loops or graphs?" — a question that touched off a lot of discussion in the agent-engineering community. The authors acknowledge the least charitable reading of a company like Prefect jumping into that conversation is that it's just signal-seeking, i.e., claiming to have discovered this idea first. Their stated counter is that using an established platform's visibility responsibly means connecting the current graph discussion back to decades of prior orchestration experience and literature, so the field doesn't reinvent already-known mistakes or let a "worst version" of the idea (as happened with the Ralph loop) become the default, oversimplified thing everyone associates with the concept. Prefect frames its own role as offering "the boring way that works" — sane, established-best-practice approaches, offered before some degenerate simplified version gets canonized the way the Ralph loop did for loop engineering.

## What this means for Prefect

Roughly once a decade, per the authors, questions about automating work resurface wearing whatever the current technological fashion is. Right now, agents are raising fresh versions of old questions about automation, trusting outcomes, and how to triage failures. Prefect's own product direction is to make directed agentic graphs the primary way agent behavior gets represented going forward: users will be able to visualize the conditional paths an agent's workflow can take, see where failures occur, and watch agents progress through a workflow that is observable, reproducible, and understandable step by step — including tool/capability changes that differ from one stage to the next.

The recent Dagster acquisition reinforces this direction. Dagster's product is itself graph-based, built around asset graphs and data lineage; combining that with Prefect's durable agent-loop runtime is described by the authors as "an Avengers-assemble moment." Proportionally, the authors estimate this is about 95% applying already-established software/orchestration practice and only about 5% genuinely new AI-specific ideas. Their framing: unlike humans, who can't really be forced to conform to a formal data structure for how they get work done, agents *can* be made to execute within an explicit structure that mirrors how humans already map out processes — which is what gives a graph-based approach its confidence that the same work gets executed consistently every time.

## Wrapping up

Jeremiah Lowin reportedly presented the directed-agentic-graph concept publicly at PyData London roughly 1.5 months before the broader "loops vs graphs" discourse took over people's feeds — offered by the authors as evidence that this was an independent trajectory rather than a reaction to the Steinberger tweet. Early-access partners are expected to be the first to experiment with the relevant tooling, with more significant production releases anticipated in the coming months. The post closes by inviting comments — the authors say they'll respond to anything addressing confusion about graphs, agents, or MCP (Model Context Protocol), and that compelling reader submissions may inform future posts on the topic.

---

**Covers:** Sections "Don't hand your agent a bazooka" through "Wrapping up" of the source article. (Omit the page's generic product call-to-action boilerplate — it is marketing, not article content.)
