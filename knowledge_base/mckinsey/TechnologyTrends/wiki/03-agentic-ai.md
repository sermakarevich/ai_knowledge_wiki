> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Agentic AI
**In one sentence:** Agentic AI has moved from experimentation to major enterprise investment as systems that plan and execute multistep workflows, but measurable EBIT impact remains elusive while costs, integration, governance, and new token/identity economics decide whether it becomes enterprise connective tissue.
## Key points
- Agentic AI means systems that plan and execute multistep workflows with limited human direction, reasoning, using enterprise systems, coordinating with other agents, and adjusting as context evolves.
- Adoption is broad but value is thin: 89 percent of organizations regularly use AI with majority at least experimenting with agents, yet only 37 percent attribute any positive EBIT impact from AI programs.
- Agents are compute-intensive and costly: a single agentic workflow can consume five to 30 times more tokens than a standard chatbot query via repeated reasoning loops, tool calls, retrieval, and orchestration; 93 percent of respondents report exceeding AI budgets.
- Capability is improving: agent-building tools from Anthropic and OpenAI improved tool use and computer interaction, LangChain's LangGraph adds orchestration and human-in-the-loop controls; METR estimates Claude Opus 4.6 had a 50 percent time horizon of roughly 12 hours on software engineering tasks by May 2026.
- The direction is from point agents to orchestrated end-to-end workflows where multiple agents coordinate across systems, with biggest gains from redesigning workflows around human-agent collaboration plus new governance, security, and infrastructure.
- Scoring signals conviction off a small base: equity investment reached $9.9 billion in 2025 and already $6.7 billion by mid-2026; job postings rose +952% in 2024-25.
- Talent demand is R&D-heavy and orchestration-scarce: hiring leans 78% R&D, led by software engineers, ML engineers, data scientists, solution architects; cloud computing required in roughly four in five postings, while orchestration supply is only 0.2x demand.
- Adoption score is 3 — Piloting: North America leads, China integrates agents into industrial/consumer platforms, Europe is more cautious on regulation/privacy, and digitally mature sectors with cloud-native data infrastructure progress fastest.
---
## What agentic AI is
Agentic AI refers to AI systems that can plan and execute multistep workflows with limited human direction. They reason, interact with enterprise systems, coordinate with other agents, and autonomously adjust their actions as context evolves.
**Covers:** pp. 18–19, definition

## The trend — and why it matters
Over the past 12 months, agentic AI moved beyond experimentation to become a major focus of enterprise technology investment. Research finds 89 percent of organizations regularly use AI, majority at least experimenting with agents, yet only 37 percent attribute any positive EBIT impact from AI programs, let alone newer agentic deployments. Agents add complexity and cost: they require tech-stack upgrades and consume many compute tokens because agentic workflows rely on repeated reasoning loops, tool calls, retrieval steps, and cross-system orchestration — in some environments a single agentic workflow consumes five to 30 times more tokens than a standard chatbot query. With agents central, 93 percent of respondents to a McKinsey survey report exceeding AI budgets. Value should expand as technology becomes more capable and embedded; recent tools from Anthropic and OpenAI improved tool use and computer interaction, while LangGraph adds orchestration and human-in-the-loop controls for longer workflows. Software development emerged as early adoption area; broader experimentation is underway across business functions. Agents raise buy-versus-build, hiring/training/labor-distribution, and human-agent operating-model questions, and are growing into a connective layer / agentic mesh between fragmented legacy systems that can reduce tech debt and extract more ROI from enterprise spend.
**Covers:** pp. 18–19, trend and why it matters

## Longer horizons and orchestrated workflows
Clearest progress indicator is handling longer, more complex tasks end to end. METR benchmarks "time horizons" — maximum time an AI can work independently before likely failing or needing help. Best models now complete tasks taking a skilled human many hours; e.g. METR estimates Claude Opus 4.6 had a 50 percent time horizon (predicted to succeed half the time) of roughly 12 hours on software engineering tasks by May 2026. Many companies have point agents for specific workflows; a smaller set of digitally mature organizations moves toward orchestrated end-to-end workflows where multiple agents coordinate across systems and tasks, visible in software development life cycle. Implications go beyond productivity: biggest gains come not from layering agents onto existing processes but redesigning workflows and operating models around humans plus agents, requiring new governance/security because agents interact across systems, plus reimagined infrastructure for and with agentic AI.
**Covers:** pp. 19–20, time horizons and agentic organization

> 'Today's challenge is operationalizing judgment. The defining question of the agentic era is not how autonomous agents can become but how much autonomy the enterprise can safely absorb.'
> — Oana Cheta, partner, Chicago

## Scoring the trend
Agentic AI emerged as distinct field when systems gained autonomous-action capability, advancing rapidly 2022–2025. Google searches and news mentions rose meaningfully; equity investment rose quickly off a small base, reaching $9.9 billion in 2025 and already $6.7 billion by mid-2026. Score-by-vector chart (0–1, relative to trends studied) covers News, Searches, Research, Patents, Equity investment, Talent demand.

| Indicator | Value |
|---|---|
| Equity investment, 2025 | $9.9 billion (+ $6.7 billion by mid-2026) |
| Job postings, 2024–25 change | +952% |

**Covers:** pp. 20–21, scoring the trend

## Latest developments
- Enterprise AI focuses on process orchestration: capturing value requires system-level integration; companies invest in agentic orchestration layers spanning ERP, CRM, supply chain. Visible in products: Salesforce expanded Agentforce for sales/CRM orchestration; Microsoft expanded Copilot Studio and orchestration tooling for custom agents across productivity and enterprise apps. Gartner forecasts supply-chain management software with agentic AI grows to $53 billion spend by 2030.
- Multiagent orchestration frameworks are the new enterprise middleware: organizations use coordinated "teams" of specialized agents rather than one monolithic model. LangGraph and CrewAI matured to enterprise-grade, with a "manager" agent routing to domain agents; LangGraph v1.0 signaled production-ready execution; CrewAI added OpenTelemetry support, better planning/observation handling, Snowflake/Databricks integrations.
- Integration with legacy systems is an emerging bottleneck: harder problem is safely turning model outputs into action in regulated environments via APIs and legacy ERP; companies adopt Model Context Protocol (MCP) and rearchitect around machine-readable interfaces.
- New compute and token economics: agentic systems require far more compute than chatbots, making token costs a key constraint; large companies cap internal AI use as costs spiral; Linux Foundation moves to formalize "tokenomics"; vendors prioritize token throughput, cost per token, inference efficiency.
- New cybersecurity frameworks: agents as read/write operators introduce nonhuman identities (NHIs) — API keys, service accounts, machine credentials — now vastly outnumbering human identities; need agentic governance; Okta launched blueprint for "secure agentic enterprise" around registration and access standardization.
- Enterprise workflows as embedding place: e.g. Morgan Stanley opening wealth-management funnel to corporate-client AI agents connecting directly to Shareworks and Equity Edge without human-oriented interfaces, early access to handful of clients expanding next year.
- Autonomy for complex multistep actions: Microsoft computer-using agents in Copilot Studio; OpenAI embedded Operator capabilities into ChatGPT to go to web, interact with interfaces, execute browser actions, coordinate multistep workflows — pointing to cross-application work without custom integrations.
- Agentic commerce as global opportunity: by 2030 global retail could see as much as $5 trillion in orchestrated revenue from agentic commerce; Alibaba rolling out Qwen-powered digital workforce for millions of Taobao/Tmall merchants (customer service, real-time price adjustments) and into consumer ecosystem (ordering milk tea, booking flights) — intent-based purchasing; Mastercard recorded first agentic transaction in 2025, Amex introduced agentic commerce developer kit April 2026; Google Agent Payments Protocol (AP2, Sept 2025) cryptographically verifies purchase against user authorization.
- Open-source agents move from cloud to local machines: e.g. OpenClaw surge reportedly drove demand for Mac minis as power-efficient local machines for on-device agents, improving latency, privacy, autonomy, offline reliability across desktop apps/OS; e.g. AgentServe co-design for efficient serving on consumer-grade GPU.

> 'The key to unlocking the value of agentic AI is evaluations. You have to invest in creating evals that align with your business objectives. Then you can create the improvement loops that accelerate business performance.'
> — Stephen Xu, partner, Chicago

**Covers:** pp. 21–23, latest developments

## Talent and labor markets — demand
Demand grew dramatically, postings rising roughly tenfold 2024–2025 off a small base, among fastest-growing trends. Led by technical/research roles — software engineers, machine learning engineers, data scientists, solution architects — plus product managers and early commercial roles like account executives signaling move from research toward productization. Functional mix is R&D-heavy with smaller share for sales, operations, general roles.

| Business function share, 2025 | % |
|---|---|
| R&D | 78 |
| Sales and marketing | 8 |
| Operations | 4 |
| General and administrative | 3 |
| Other | 7 |

Top titles include software engineer, machine learning engineer, solution architect, data scientist, product manager, software developer, full-stack developer, data engineer, scientist, account executive.
**Covers:** pp. 23–24, demand

## Talent and labor markets — skills availability
Cloud computing is most widely required (roughly four in five postings), supply broadly keeping pace. Shortage is orchestration, the coordination layer tying models, tools, workflows into functioning systems. Established capabilities like JavaScript, Python, even machine learning show broad pool formed while newer coordination skills remain scarce.

| Skill | % postings requiring | Availability ratio (talent to demand) |
|---|---|---|
| Cloud computing | ~80 / 71* | 1.0x |
| Machine learning | 51* | 4.3x |
| Python | 38* | 1.8x |
| Amazon Web Services | 36* | 0.9x |
| Azure | 22* | 1.4x |
| Orchestration | 19* | 0.2x |
| JavaScript | — | 5.9x |

\* Chart labels in chunk list values 80, 71, 51, 38, 36, 22, 19 against Cloud computing, Machine learning, Python, Amazon Web Services, Azure, Orchestration, JavaScript; availability ratios listed as 1.0x, 4.3x, 1.8x, 0.9x, 1.4x, 0.2x, 5.9x in same order.
**Covers:** p. 24, skills availability

## Adoption around the globe
Adoption score: 3 — Piloting. Many organizations test functionality with small prototypes and targeted deployments; enthusiasm and investment up sharply, few have fully scaled agentic operating models. North America is center of experimentation (hyperscalers, frontier developers, AI-native start-ups, large tech orgs); earliest scaled deployments in software engineering, customer operations, enterprise productivity. China increasingly integrates agentic capabilities into industrial automation, enterprise software, consumer ecosystems — e.g. Moonshot AI July 2026 release of Kimi K3, a 2.8-trillion-parameter open-weight model said to approach Anthropic's frontier Fable model. Europe adopts more cautiously on regulatory scrutiny, governance, labor, accountability, data privacy. Digitally mature sectors with strong data infrastructure and cloud-native environments (technology, software, financial services, telecommunications) progress fastest; many large non-tech enterprises remain in experimentation due to legacy integration complexity, fragmented data, governance constraints.
**Covers:** pp. 24–25, adoption developments

## Underlying technologies
| Technology | Role per source |
|---|---|
| AI-enabled user interfaces | Conversational/multimodal interfaces to manage workflows via natural language |
| AI orchestration frameworks | Coordinate multiple agents, tools, workflows, enterprise integrations |
| API integration layers | Enable agents to interact with enterprise software, databases, external services |
| Foundation models | Large-scale models for reasoning, generation, planning |
| Memory and context management | Retain context and continuity across workflows |
| Reasoning models | Optimize multistep planning, sequencing, workflow execution |
| Retrieval-augmented generation | Combine language models with enterprise knowledge retrieval |
| Workflow management systems | Task routing, approvals, execution, operational monitoring |

**Covers:** p. 25, underlying technologies

## Key uncertainties
- Reliability and trust: ensuring consistent accurate safe execution.
- Governance and accountability: responsibility, oversight, escalation, operational control for autonomous workflows.
- Cybersecurity risks: cross-system interaction creates new attack surfaces and vulnerabilities.
- Workforce transformation: long-term implications for structures, management layers, role design, labor demand uncertain.
- Infrastructure economics: compute requirements and operational costs may constrain adoption.
- Enterprise integration complexity: legacy systems, fragmented data, silos.
- Regulatory evolution: frameworks for autonomous systems, liability, accountability still developing.
- Human–machine collaboration models: how best to structure workflows around humans plus autonomous systems.
**Covers:** pp. 25–26, key uncertainties

## Big questions about the future
- Which enterprise workflows are best suited for agentic orchestration, and how can enterprises ensure transparency, reliability, accountability in multistep autonomous workflows?
- How should organizations rethink infrastructure, operating models, governance, workforce strategies around agentic systems?
- What new roles and skill sets emerge as agentic systems integrate deeper?
- Which industries realize greatest productivity/operational gains over next five years?
- How will agentic AI reshape software interfaces, enterprise applications, structure of digital work?
**Covers:** p. 26, big questions
