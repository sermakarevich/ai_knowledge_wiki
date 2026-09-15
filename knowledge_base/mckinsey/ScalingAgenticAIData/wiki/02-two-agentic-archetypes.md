[[../index.md|Scaling agentic AI with data transformations]] · Page 2 — single-agent vs multi-agent archetypes, failure modes

# Two agentic archetypes and what each demands of data

**In one sentence:** Agentic AI (Artificial Intelligence systems that act autonomously toward goals) is converging on two archetypes — single-agent workflows in which one agent uses multiple tools and data sources sequentially, and multi-agent workflows in which specialized agents collaborate through shared knowledge graphs and fine-grained data access — and both depend on consistent interoperable data, without which single agents make inconsistent decisions from fragmented data while multi-agent systems lose coordination and propagate errors.

## Key points

- Two agentic archetypes are emerging: single-agent workflows, where one agent uses multiple tools and data sources sequentially, and multi-agent workflows, where specialized agents collaborate through shared knowledge graphs and fine-grained data access.
- Both archetypes require consistent, interoperable data, without which agents could break down regardless of how capable the underlying models are.
- Single agents fail by making inconsistent decisions from fragmented data, because one reasoning thread sees a different version of reality at each tool call.
- Multi-agent systems fail by losing coordination and propagating errors, because one agent's misread context becomes the next agent's input.
- Success with agentic AI depends on a data architecture that supports increasing levels of autonomy, coordination, and real-time decision-making, typically as modular interoperable frameworks giving agents reliable, safe access to data.
- Generative AI (gen AI, models that produce text, images, or other content from prompts) already demonstrated the need for data access control, lineage, and traceability, but agentic platforms place greater operational pressure on those foundations through continuous multi-model, multi-source coordination.
- Because agentic AI coordinates multiple models and data sources continuously, often without human intervention, it requires tighter and more automated governance than gen AI to ensure reliability and control at scale.

---

## The two archetypes

### Single-agent workflows

One agent uses multiple tools and data sources sequentially: it plans, calls a tool, reads the result, and continues. The data demand is consistency across sequential reads — the customer record, inventory figure, or policy text must mean the same thing at step one and step ten.

### Multi-agent workflows

Specialized agents collaborate through shared knowledge graphs and fine-grained data access: each agent owns a slice of the work and exchanges context with the others. The data demand is shared semantics plus scoped access — agents must interpret shared entities identically while only touching the data their role permits.

## How each breaks without interoperable data

A single agent fed by fragmented sources makes inconsistent decisions, committing to one version of a fact early and contradicting it later. A multi-agent system loses coordination as small interpretation differences compound across handoffs, and errors propagate because no human reviews the intermediate steps. The mechanism is the same in both cases — unreliable data context — but the blast radius grows with autonomy and agent count.

## From gen AI pressure to agentic pressure

Gen AI established the baseline needs of access control, lineage, and traceability. Agentic AI multiplies the operational pressure because coordination is continuous, multi-model, and unsupervised, which is why the article insists on tighter, more automated governance rather than merely more governance headcount.

**Covers:** source section 2 (architecture demands; the two archetypes).
