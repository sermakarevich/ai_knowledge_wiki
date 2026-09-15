# Source reconstruction — Scaling agentic AI with data transformations (McKinsey)

> Route-4 reconstruction (direct fetch blocked on all routes; see `provenance.md`).
> Original: "Building the foundations for agentic AI at scale", McKinsey & Company, April 2, 2026.
> Canonical URL: https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/building-the-foundations-for-agentic-ai-at-scale
> Display title used by McKinsey listings: "Scaling agentic AI with data transformations".
> Byline (sourced from McKinsey page snippet and RamaOnHealthcare mirror): Asin Tavakoli, Brian Goodman,
> Henning Soller, and Kayvaun Rowshankish, with Akshat Kumar, Carlos Barreto, Satyajit Parekh, and
> Tancredi Bernard Litta Modignani, representing views from McKinsey Technology and QuantumBlack, AI by McKinsey.
> Dek (sourced): "Agentic AI scales on strong data. To capture value, tech leaders can agentify high-impact
> workflows, modernize data architectures, enforce data quality, and evolve operating models."
>
> Every passage below is drawn from search-result extracts of the McKinsey page and verbatim mirrors/summaries;
> contributing sources are tagged [S1]–[S8] at the end. Passages that appear in only one secondary source or
> whose wording could not be cross-checked are marked [unverified].

## 1. A house is only as strong as its foundation

A house is only as strong as its foundation. That's what companies are quickly coming to understand about
agentic AI as well. Nearly two-thirds of enterprises worldwide have experimented with agents, but fewer than
10 percent have scaled them to deliver tangible value. [S1][S2] Shaky data is often to blame; eight in ten
companies cite data limitations as a roadblock to scaling agentic AI (Exhibit 1). Addressing this issue is a
core element of building a solid capability foundation—and that's what distinguishes companies that create
value from AI from those that don't, according to our Rewired research. [S1][S2]

While companies have often muscled through issues of fragmented and siloed data, those issues are impossible
to manage at scale. Inconsistent governance has just increased the challenge of preserving data context while
enforcing access control, lineage, and auditability. [S1][S2]

## 2. Why agentic AI needs a different data architecture

Success with agentic AI depends on a data architecture that can support increasing levels of autonomy,
coordination, and real-time decision-making. This often looks like modular, interoperable frameworks that give
agents reliable access to the data they need to operate safely (see sidebar, "Seven data architecture
principles that enable scale"). While gen AI has already shown the need for data access control, lineage, and
traceability, agentic platforms place greater operational pressure on these foundations. Because agentic AI
coordinates multiple models and data sources continuously, often without human intervention, it requires
tighter, more automated governance to ensure reliability and control at scale. [S1][S2]

Two agentic archetypes are emerging: single-agent workflows, where one agent uses multiple tools and data
sources sequentially; and multi-agent workflows, where specialized agents collaborate through shared knowledge
graphs and fine-grained data access. Both require consistent, interoperable data, without which agents could
break down. [S2] Single agents could make inconsistent decisions from fragmented data, while multi-agent
systems could lose coordination and propagate errors. [S3]

## Sidebar. Seven data architecture principles that enable scale [S1][S3]

1. Treat data ingestion like a product. Make it easy and consistent for all data—batch, real-time, structured,
or unstructured—to enter the company once and be usable by everyone.
2. Share meaning, not just data. Ensure data comes with clear, common definitions so analytics, AI models, and
agents all understand it the same way.
3. Use one data foundation for analytics and AI. Build data once and use it everywhere—reports, machine
learning, and gen AI—rather than running separate pipelines and platforms.
4. Build trust into the platform by default. Security, access controls, privacy, and AI governance should be
automatic, not added later or managed manually.
5. Expose capabilities through stable interfaces. Provide clear APIs and model access points so teams can
reliably build applications and AI solutions without rework.
6. Make behavior visible and measurable. Continuously track data quality, model performance, speed, and cost so
issues are caught early and systems improve over time.
7. Provide a controlled way to run AI agents and applications. Coordinate AI agents and applications through a
shared execution layer that enforces enterprise rules and guardrails.

## 3. How to prepare data for agentic AI

To enable a scaled transformation into an agentic organization, companies can start by building foundational
data capabilities. This requires not just a technology reboot, but also an organizational one. That's because
a company's data strategy and operating model is just as important as its underlying data quality and
architecture. Success depends on taking four coordinated steps that link strategy, technology, and people:
[S1][S2]

Step 1: Identify high-impact workflows to "agentify." Organizations can identify a small number of high-value,
end-to-end workflows where increased autonomy could unlock impact. Building on established approaches to
building data products, leaders can prioritize agentic use cases based on value potential, feasibility, and
strategic fit before scaling more broadly. [S1][S2]

Step 2: Modernize each layer of the data architecture for agents. Rather than rebuilding everything from
scratch, leaders can modernize existing platforms to support interoperability and governance across systems.
While some may be tempted to lean on advancements in AI to shortcut data architecture best practices, the
strongest organizations build modular, evolutionary architectures with components that can be replaced as new
technologies emerge. [S1][S2]

Step 3: Ensure that data quality is in place. Organizations must move from periodic data cleanup to continuous,
real-time quality management. They can do this while ensuring that both structured and unstructured data, as
well as agent-generated outputs, meet consistent standards for accuracy, lineage, and governance. [S1][S2]

Step 4: Build an operating and governance model for agentic AI. Scaling agentic AI requires rethinking how work
gets done. Human roles are shifting from execution to supervision and orchestration of agent-driven workflows.
In a hybrid human–agent work environment, clear governance is essential to allow agents to operate
transparently and safely at scale. [S1][S2]

## 4. Modernizing each layer of the data stack [unverified: section organization reconstructed from extracts]

Preparing the data architecture for agentic AI requires strengthening and adjusting the layers of the data
stack. Rather than rebuilding systems from scratch, companies can modernize each layer to improve visibility
and governance across workflows. [S1] The article illustrates this with an omnichannel retail scenario [S4]
[unverified: retail scenario is the article's exhibit; details below are sourced]:

Data products turn curated data into reusable, business-ready assets. They package data with clear ownership,
quality standards, semantics, and interfaces for consumption. Through a product mindset, companies treat data
as a performance asset that can be reused across multiple use cases and domains. Reusable data products allow
agents to draw on trustworthy predictive and generative insights at scale, while observability records how
agents use data, creating the traceability needed for oversight and enabling feedback loops that improve
upstream data and models. [S1]

Agentic orchestration and retrieval services are embedded in the consumption layer [unverified: layer name].
AI systems dynamically assemble context—often from unstructured data—rather than relying on predefined
queries. Orchestration enables AI systems to decide what to retrieve, how to refine it, and when to iterate,
while retrieval services ensure this access is secure, efficient, and governed at scale. [S1]

Governance and access controls provide core components that control how agents interact with data, tools, and
models in a controlled way. A medallion architecture progressively curates and enriches data from raw to
agent-ready form, while preserving lineage and auditability. Data access is then governed through APIs,
queries, and permissions. As models retrieve and use unstructured data dynamically, an AI gateway is needed to
control access and usage. The gateway governs model access to unstructured data, enforces usage policies, and
records how data is retrieved and used in prompts and responses. [S1]

At the data source layer, customer data such as browsing history, wishlists, purchase history, and support
interactions enters from various systems; for unstructured data, continuous ingestion, transformation, and
recombination are needed, and governance must flow along with it, with quality checks, security controls, and
lineage tracking automated and embedded directly in pipelines rather than handled as one-time reviews. At the
data platform layer, data from different systems is connected for applications and models through orchestrated
access, synchronization, and real-time cross-system interaction; vector stores and embedding services are key
components for unstructured data, and agent-specific interoperability standards such as Model Context Protocol
(MCP) and agent-to-agent (A2A) communication can further automate integration and access. [S4][S5]
[unverified: exact exhibit wording; MCP/A2A also corroborated in S6.]

The semantic layer turns data into knowledge, sitting between raw data and AI applications and codifying
business meaning into machine-readable yet human-understandable form, most often implemented through
ontologies and knowledge graphs: ontologies define how attributes and relationships combine into business
reality, while knowledge graphs operationalize this vocabulary by linking real-world data across systems into
connected entity networks. [S4][S7]

## 5. Data quality as a continuous discipline

Curated, high-quality data becomes a strategic differentiator in the agentic AI era. Foundation models can be
costly to deploy, given the costs of large-scale inference, fine-tuning, infrastructure, and governance.
Organizations with well-structured internal data sets can reduce technology investment costs by fine-tuning
smaller, domain-specific models on their own data. These models are not just more cost- and resource-efficient,
but more resilient and compliant. [S1]

Making unstructured data usable requires improving its quality through tagging, classification, vector
embeddings, and graph-based structuring. This allows agents to reliably understand entities, relationships, and
context. Unstructured data must be held to the same standards as structured data. [S1]

Companies must also evolve how they manage structured data. Instead of periodic cleanups, organizations can
engage in continuous, real-time data quality monitoring. This process is supported by AI-enabled automated
validation, anomaly detection, and enrichment pipelines that prevent issues from propagating across workflows.
Metadata management provides lineage and business context so that agents can trace and justify decisions. [S1]

Finally, as agents generate new data, organizations must apply the same quality, lineage, and reconciliation
standards to their outputs. This includes data retrieved or written through agent-invoked tools and APIs, which
should operate through governed, reconcilable interfaces rather than bypassing enterprise quality control.
Shared fit-for-purpose definitions embedded into automated quality checks can ensure that agents act on reliable
information at scale. [S1]

## 6. The operating and governance model

As agentic systems scale, governance becomes the primary mechanism for control. Clear and explicit policies are
needed to define what agents can do, what data they can access, and when human approval is required, with
access checks evaluated automatically for each agent based on their role and scope. Importantly, agents should
not introduce new data quality or governance rules; they should follow the same standards as other systems,
applied automatically as autonomy increases. [S1]

Clear accountability for agent behavior—spanning business outcomes, risk management, and policy
compliance—is critical to scale. In practice, business domains own day-to-day governance of agent-enabled
workflows, including domain models and ontologies. Meanwhile, central data and AI teams maintain shared
platforms, guardrails, and oversight. This federated model balances domain autonomy with enterprise-wide
accountability. [S1]

## 7. Closing

In the agentic age, technology leaders are finding that their data foundations increasingly define competitive
positioning. Yet despite the promise of using data to generate real value from agentic AI, many organizations
still struggle to make data accessible and governable for digital agents. The time has come to drive data
transformations that pave the way for an agentic future. [S1]

---

## Contributing sources

- [S1] McKinsey page extracts via search provider (mckinsey.com and mckinsey.com.br URLs), deep-search
result 1, 2026-09-14: lede, architecture passage, four steps, layer passages, quality passages, governance
passages, closing.
- [S2] informedi.org republication of extractive summary (Arif Saleem, 2026-04-27): lede, architecture passage,
archetypes, four steps.
- [S3] LinkedIn post by Dr. Stephen B. Baruch quoting the article (2026-07-11): architecture passage, sidebar
reference, archetype failure modes.
- [S4] haxitag.ai deep analysis of the report (2026-06-13): seven-principles interpretation, omnichannel retail
layer walkthrough, semantic-layer definitions.
- [S5] agenticaiinstitute.org commentary (2026-04-22): four-step framing, vector stores/embedding services as
foundational, MCP/A2A standards.
- [S6] Stanford Tech Review article (2026-06-13): MCP/A2A and controlled execution layer corroboration.
- [S7] plastergroup.com insights article (2026-03-21): semantic-layer quotation ("turns data into knowledge",
ontologies/knowledge graphs), governance-travels-with-data, continuous monitoring, agent outputs held to same
standards, publication date and cost points.
- [S8] RamaOnHealthcare mirror page (2026-04-04) and RALI listing (2026-04-02): byline, date, dek, lede.
