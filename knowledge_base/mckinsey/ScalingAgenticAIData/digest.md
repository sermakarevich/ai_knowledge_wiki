# Digest — Scaling agentic AI with data transformations

Headlines and key points copied verbatim from the wiki pages.

## Page 1 — The scaling gap: shaky data blocks agentic value

# The scaling gap: shaky data blocks agentic value

- Nearly two-thirds of enterprises worldwide have experimented with agents, but fewer than 10 percent have scaled them to deliver tangible value, a gap the article attributes primarily to fragile data foundations rather than model immaturity.
- Eight in ten companies cite data limitations as a roadblock to scaling agentic AI, the article's Exhibit 1 quantification of the bottleneck.
- Addressing shaky data is a core element of building a solid capability foundation, and that foundation is what distinguishes companies that create value from AI from those that do not, according to McKinsey's Rewired research program.
- Fragmented and siloed data could previously be muscled through by human effort, but at agentic scale those workarounds collapse because agents operate continuously and without human intervention.
- Inconsistent governance compounds the problem by making it harder to preserve data context while simultaneously enforcing access control, lineage, and auditability.
- The article's thesis is that data strategy and operating model matter as much as data quality and architecture, so preparing for agentic AI requires a technology reboot and an organizational one together.
- The closing verdict is that data foundations increasingly define competitive positioning, and the time has come to drive data transformations that pave the way for an agentic future.

## Page 2 — Two agentic archetypes and what each demands of data

# Two agentic archetypes and what each demands of data

- Two agentic archetypes are emerging: single-agent workflows, where one agent uses multiple tools and data sources sequentially, and multi-agent workflows, where specialized agents collaborate through shared knowledge graphs and fine-grained data access.
- Both archetypes require consistent, interoperable data, without which agents could break down regardless of how capable the underlying models are.
- Single agents fail by making inconsistent decisions from fragmented data, because one reasoning thread sees a different version of reality at each tool call.
- Multi-agent systems fail by losing coordination and propagating errors, because one agent's misread context becomes the next agent's input.
- Success with agentic AI depends on a data architecture that supports increasing levels of autonomy, coordination, and real-time decision-making, typically as modular interoperable frameworks giving agents reliable, safe access to data.
- Generative AI (gen AI, models that produce text, images, or other content from prompts) already demonstrated the need for data access control, lineage, and traceability, but agentic platforms place greater operational pressure on those foundations through continuous multi-model, multi-source coordination.
- Because agentic AI coordinates multiple models and data sources continuously, often without human intervention, it requires tighter and more automated governance than gen AI to ensure reliability and control at scale.

## Page 3 — Seven data architecture principles that enable scale

# Seven data architecture principles that enable scale

- Treat data ingestion like a product by making it easy and consistent for all data — batch, real time, structured, or unstructured — to enter the company once and be usable by everyone.
- Share meaning, not just data, by ensuring data carries clear common definitions so analytics, AI models, and agents all understand it the same way.
- Use one data foundation for analytics and AI by building data once and using it everywhere — reports, machine learning, and generative AI — rather than running separate pipelines and platforms.
- Build trust into the platform by default so that security, access controls, privacy, and AI governance are automatic rather than added later or managed manually.
- Expose capabilities through stable interfaces that provide clear Application Programming Interfaces (APIs, contracts letting software components talk to each other) and model access points so teams can reliably build applications and AI solutions without rework.
- Make behavior visible and measurable by continuously tracking data quality, model performance, speed, and cost so issues are caught early and systems improve over time.
- Provide a controlled way to run AI agents and applications by coordinating them through a shared execution layer that enforces enterprise rules and guardrails.

## Page 4 — Four coordinated steps to prepare data for agentic AI

# Four coordinated steps to prepare data for agentic AI

- Enabling a scaled transformation into an agentic organization starts with foundational data capabilities and demands a technology reboot plus an organizational one, since data strategy and operating model are as important as data quality and architecture.
- Step 1 tells leaders to identify a small number of high-value end-to-end workflows to agentify, prioritizing agentic use cases by value potential, feasibility, and strategic fit before scaling broadly, building on established data-product approaches.
- Step 2 tells leaders to modernize each layer of the data architecture for agents rather than rebuilding from scratch, pursuing interoperability and governance with modular evolutionary architectures whose components can be replaced as technologies emerge.
- Step 2 explicitly warns against leaning on AI advances to shortcut architecture best practices, arguing the strongest organizations keep modular discipline instead of letting models paper over structural debt.
- Step 3 moves organizations from periodic data cleanup to continuous real-time quality management, holding structured data, unstructured data, and agent-generated outputs to consistent standards for accuracy, lineage, and governance.
- Step 4 rebuilds the operating and governance model because human roles shift from execution to supervision and orchestration of agent-driven workflows, requiring clear governance for transparent safe operation in hybrid human-agent environments.
- The four steps are designed to run as one coordinated program across strategy, technology, and people rather than as four sequential projects owned by four separate teams.

## Page 5 — Modernizing each layer of the data stack

# Modernizing each layer of the data stack

- Preparing the architecture means strengthening and adjusting each layer of the data stack to improve visibility and governance across workflows, evolving existing platforms instead of rebuilding systems from scratch.
- Data products turn curated data into reusable business-ready assets packaged with clear ownership, quality standards, semantics, and consumption interfaces, letting agents draw on trustworthy predictive and generative insights at scale.
- Observability of agent data use creates the traceability needed for oversight and enables feedback loops that improve upstream data and models over time.
- Agentic orchestration and retrieval services in the consumption layer let AI systems dynamically assemble context — often from unstructured data — deciding what to retrieve, how to refine it, and when to iterate, with retrieval kept secure, efficient, and governed at scale.
- A medallion architecture progressively curates and enriches data from raw to agent-ready form while preserving lineage and auditability, with access governed through Application Programming Interfaces (APIs), queries, and permissions.
- An AI gateway governs model access to unstructured data by enforcing usage policies and recording how data is retrieved and used in prompts and responses.
- The semantic layer sits between raw data and AI applications and codifies business meaning into machine-readable yet human-understandable form, implemented through ontologies that define how attributes and relationships combine into business reality and knowledge graphs that link real-world data across systems into connected entity networks.

## Page 6 — Quality, cost, and the federated operating model

# Quality, cost, and the federated operating model

- Curated high-quality data is a strategic differentiator because organizations with well-structured internal data sets can cut technology costs by fine-tuning smaller domain-specific models, which are more cost- and resource-efficient as well as more resilient and compliant.
- Foundation models are costly to deploy through large-scale inference, fine-tuning, infrastructure, and governance spend, so data quality directly reduces the AI bill rather than merely improving accuracy.
- Unstructured data becomes usable through tagging, classification, vector embeddings, and graph-based structuring that let agents reliably grasp entities, relationships, and context, and it must meet the same standards as structured data.
- Structured data management evolves from periodic cleanups to continuous real-time monitoring backed by AI-enabled automated validation, anomaly detection, and enrichment pipelines that stop defects from propagating across workflows.
- Metadata management supplies the lineage and business context agents need to trace and justify their decisions to supervisors and auditors.
- Agent-generated outputs — including data retrieved or written through agent-invoked tools and APIs — must meet the same quality, lineage, and reconciliation standards via governed reconcilable interfaces, with shared fit-for-purpose definitions embedded in automated checks.
- Accountability follows a federated model that balances domain autonomy with enterprise-wide accountability: business domains own day-to-day governance of agent-enabled workflows including domain models and ontologies, while central data and AI teams maintain shared platforms, guardrails, and oversight.

## The argument in five moves

1. Most firms experiment with agents but almost none scale them because shaky data breaks autonomous workflows.
2. Single-agent and multi-agent archetypes both demand consistent interoperable data with shared meaning.
3. Seven architecture principles convert fragmented pipelines into a modular governable platform.
4. Four coordinated steps turn principles into action across workflows, layers, quality, and operating model.
5. Continuous quality plus federated governance lets curated data cut model costs and carry agents to scale.
6. Data foundations therefore decide competitive position, so transformation starts now.
