[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Agentic software development (Trend 01)
**In one sentence:** Agentic software development — LLM (Large Language Model) systems that autonomously plan, write, test, fix, and deploy code — could unlock almost $1 trillion in value, but only about one-quarter of adopters get meaningful acceleration because value requires rewiring the full product development life cycle (PDLC), change management, verification, and small human–agent teams rather than just more code.
## Key points
- Agentic software development means LLM-powered systems autonomously performing planning, coding, testing, bug-fixing, and deployment, shifting engineers from hands-on coders to agent supervisors/orchestrators.
- Potential value is almost $1 trillion when deployed successfully, but only one-quarter of companies using the tools achieved meaningful PDLC acceleration (defined as more than a quarter of their teams achieving twofold or greater productivity gains).
- Gains are highly skewed: 80 percent of engineers using AI tools see only ~3 percent acceleration while the top 20 percent see a 55 percent boost; in 30 percent of companies productivity fell after adopting agentic AI tools.
- More code does not equal more product: in one study AI tools raised coding activity by 180 percent but shipped releases rose by only 30 percent; 46 percent of developers distrust AI accuracy vs 33 percent who trust and only 3 percent who highly trust it.
- Capital and interest are converging: investment in agentic coding-tool companies was negligible through 2023, ~$5 billion in 2025, and crossed $61 billion in H1 2026 (mainly the $60 billion Cursor acquisition); job postings rose +221% with $4.9 billion equity investment in 2025.
- The operating model must shift from two-week sprints and synchronous assistance to asynchronous delegation, after-hours agents, the "agentic factory" across the full software development life cycle (SDLC), and human–agent pods of small human teams supervising agent fleets.
- Bottlenecks move "to the edges" (what to build, whether it works): top performers are 6–7x more likely to embed AI across 4+ life-cycle stages; developers spend only ~one-tenth of the workday writing code; AI agents can accelerate modernization by 40–50 percent and cut costs up to 40 percent, while AI now accounts for a third of companies' spending to introduce new capabilities.
---
## The trend — and why it matters
**Covers:** pp. 8–10, "01 Agentic software development"

Agentic software development refers to the use of large language model (LLM)–powered systems that autonomously perform software engineering tasks, including planning, writing code, running tests, fixing bugs, and deploying changes.

In the past year developers can instruct computers to create applications instead of typing lines; top engineers became "agent wranglers" spawning multiple agents that write, modify, and test code while they sleep. Companies adopt at breakneck pace; when deployed successfully it could unlock almost $1 trillion in value.

Making individual engineers productive is only part of the battle. Companies must rewire the full PDLC using AI; those most likely to capture value support developers with change management, embed AI tools into workflows, and verify/validate agentic outputs to high-quality standards.

Results so far (McKinsey, Aug 21 2026):
- Just one-quarter of companies using agentic tools achieved meaningful acceleration (more than a quarter of their teams with 2x+ gains).
- 80% of engineers see ~3% acceleration; top 20% see 55% boost — requires nurturing top performers and spreading winning practices.
- In 30% of companies productivity fell after agentic AI adoption.
- AI tools increased coding activity by 180% but shipped releases rose only 30% (Demirer, Musolff & Yang, CEPR, June 21 2026).
- Developer trust gap (Stack Overflow 2025 Developer Survey): 46% actively distrust AI tools' accuracy vs 33% who trust, only 3% highly trust. Near-term objective: human–agent systems that safely generate, test, and deploy code in controlled environments.

## Scoring the trend
**Covers:** p. 10, "Scoring the trend"

Clearest signals are capital and interest. Investment was negligible through 2023, rising in 2024, roughly $5 billion in 2025, crossing $61 billion in H1 2026 (mainly the $60 billion acquisition of Cursor; TechCrunch, June 16 2026). Search activity climbs in parallel. Software development is the first agentic AI application where capital and interest converge on tangible returns. Innovation/news scores look modest because activity leans to product work over patents/publications and remains niche in broad news.

| Metric | Value |
|---|---|
| Equity investment, 2025 | $4.9 billion |
| Job postings change, 2024–25 | +221% |

Score by vector (0=lower, 1=higher): News, Searches, Research, Patents, Equity investment, Talent demand — indexed 0–1 relative to trends studied (vectors defined as press reports, search queries, scientific publications, patent filings, capital raises, job postings).

## Latest developments
**Covers:** pp. 11–14

- Shift from synchronous assistance to asynchronous execution: earlier tools required interactive real-time prompting like extended code completion (predict/insert rest of word/line/block); now developers assign discrete tasks to autonomous agents, moving from two-week sprints to a continuous high-speed loop (e.g., Anthropic Claude Code, OpenAI Codex); after-hours/overnight/weekend workflows return completed code, tests, analysis, documentation; humans become orchestrators defining workflows and judgment while agents execute. Risk: frontier models like Anthropic's Claude Mythos can autonomously discover/exploit vulnerabilities at machine speed, compressing the vulnerability life cycle; requires multilayered controls (access control, isolation, monitoring, human oversight, containment, recovery).
- The "agentic factory" as engineering paradigm: Cursor exemplifies shift from integrated development environment to agent-centric orchestration — a visual environment for spawning, monitoring, coordinating agents (Cursor SDK, Apr 29 2026); Anthropic, Cognition, OpenAI invest in long-running agents; multiagent systems automate the surrounding SDLC since developers spend only ~one-tenth of the workday writing code (e.g., one agent drafts requirements, another designs architecture, third generates security tests, fourth manages release); top organizations are 6–7x more likely to embed AI across 4+ stages (McKinsey, Nov 3 2025). Bottlenecks shift "to the edges": deciding what to build, validating it works; embed AI across PDLC not just coding; knowledge graphs give shared definitions, lineage, permissions to interpret requirements and validate outputs.

> 'The real shift in software engineering is not that agents write code faster. To capture the value from these tools, the software development life cycle operating model has to shift, including moving toward smaller, highly leveraged teams that supervise agents through execution.'
> — Martin Harrysson, senior partner, Silicon Valley

- AI-native development: from coding-assistant experiments to AI-first workflows embedded in coding, testing, debugging, documentation, code review. In Oct 2025 GitHub reported >1.1 million public repositories using an LLM software development kit and nearly 80% of new developers used Copilot in their first week. Early access was a differentiator; now broad uptake means CTOs (Chief Technology Officers) can build organization-specific capabilities and custom enterprise-grade capabilities atop SaaS (Software-as-a-Service) platforms' native agentic tools.
- Enterprise context as core requirement: code generation is easy; hard part is codebase, policies, regulatory constraints, product history. Greenfield moves faster; brownfield must work inside existing code/decisions/dependencies; modernization bar highest (refactor/translate legacy while preserving operations) — AI agents can accelerate modernization 40–50% and cut costs up to 40%. Demand for knowledge graphs, repository indexing, enterprise context systems; well-documented workflows + searchable knowledge enable agentic development.
- Economics rewritten: token spend/inference costs from rounding error to material line item; token-based pricing makes consumption a governed budget item. AI now accounts for a third of companies' spending to introduce new capabilities plus adds to run costs; inference adds variable compute/infrastructure costs; token consumption treated as governed financial resource.
- Talent model to smaller, highly leveraged teams: leaner teams focused on product definition, architecture, prompt engineering, exception handling; shift from large pools to talent pods multiplying output; traditional agile "two pizza" pods vs human–agent pods (many agents under few humans; engineers define product/architecture/constraints, agents implement/test). Salesforce announced no additional software-engineer hires in 2025 after AI productivity gains, prioritizing leverage over headcount.

> 'Asynchronous agents—and workflows—change the cadence of software delivery. Work that once moved through two-week sprints can now become a continuous loop of drafting, testing, debugging, and documentation between human reviews. The leadership challenge is to increase speed without weakening maintainability, quality, or control.'
> — Prakhar Dixit, partner, Seattle

## Talent and labor markets: demand
**Covers:** pp. 14–15

Demand surged, postings more than tripling 2024→2025, among fastest-growing trends. Software engineers remain largest role; full-stack developers rose from negligible base to second largest; machine learning engineer postings fell sharply (shift from training models to wiring existing ones into software). Mix heavily R&D-weighted.

- Job postings by title 2022–25 (thousands): Software engineer, Full-stack developer, Software developer, Machine learning engineer, Web developer, Solution architect, Product manager, Site reliability engineer, Data engineer, Data scientist.
- Job postings by business function 2025: R&D 90%, Sales and marketing 2%, Operations 2%, General and administrative 2%, Other 4%.

## Talent and labor markets: skills availability
**Covers:** p. 15

Cloud computing required in most postings with supply just keeping pace. Sharpest shortage in CI/CD (Continuous Integration / Continuous Delivery) — delivery skills to move agentic software to production. JavaScript, Python, GitHub, machine learning widely available.

| Skill | % postings requiring | Talent-to-demand ratio |
|---|---|---|
| Cloud computing | 87 | 1.0x |
| CI/CD | 84 | 0.1x |
| JavaScript | 49 | 5.9x |
| Amazon Web Services | 47 | 0.9x |
| Python | 46 | 1.8x |
| GitHub | 43 | 3.3x |
| Machine learning | 36 | 4.3x |

## Adoption across the globe
**Covers:** pp. 15–16

Adoption score: 3 — Piloting. Most organizations piloting, more scaling; fast movers fully implemented as core workflow. Technology companies furthest; legacy industries still working through people/process/governance.

- North America center of activity: AI-native software firms, hyperscalers, tool providers, large tech; advanced deployments in engineering, testing, deployment, orchestration, internal productivity.
- Europe more cautious: governance, compliance, quality controls; select use cases, greater human oversight.
- Asia–Pacific growing where development ties to digital transformation, industrial workflows, large modernization.
- Sectors: software firms fastest (digital infrastructure, flexible workflows, experimentation tolerance); codified processes/structured docs/searchable knowledge move quickly; retail, manufacturing, oil and gas, mining slower on fragmented/less-mature infrastructure.

## Underlying technologies
**Covers:** p. 16

| Technology | What it is |
|---|---|
| Agent evaluations | Frameworks benchmarking/testing/monitoring agent performance across coding, review, debugging, security, deployment |
| Coding agents | Systems autonomously writing, reviewing, refactoring, debugging code |
| CI/CD integration layers | Infrastructure letting agents interact with testing, deployment, release pipelines |
| Enterprise context systems | Knowledge graphs, document stores, retrieval systems helping agents understand code, policy, product history |
| Foundation models | Large AI systems providing code generation, planning, reasoning |
| Harness and guardrail systems | Controls defining what agents can access, change, execute |
| Orchestration frameworks | Tools coordinating multiple agents across tasks/handoffs |
| Reinforcement-learning verifiable reward systems | Converting checkable outcomes (passing tests, satisfying specs) into feedback to improve agents |
| Token and workload management systems | Platforms monitoring inference usage, cost, run-time efficiency |

## Key uncertainties
**Covers:** pp. 16–17

- Trust and reliability: ensuring safe, correct, maintainable code.
- Governance and control: what agents may change, autonomy level, audit.
- Economic returns: developer-level gains shown, fewer sustained org-level financial impacts.
- Talent redesign: long-term roles, performance management, team structure unclear.
- Cost discipline: token spend, tool sprawl, orchestration overhead may limit returns.
- Legacy integration: older systems, compliance, fragmented enterprise context slow adoption.

## Big questions about the future
**Covers:** p. 17

- How balance speed, governance, maintainability as agents take on more SDLC?
- Which parts of SDLC genuinely delegated to agents at scale?
- How measure productivity when token spend enters development economics?
- What is right team structure for AI-first software organization?
- Which roles become more valuable as agents take implementation work?

Related reading (per source): Enterprise Software knowledge center; Insights on AI; The state of AI in 2026: On the road to ROI; AI-native development: Rethinking software from the ground up; Rewiring software delivery for the agentic era; Unlocking the value of AI in software development; The AI-centric imperative: Navigating the next software frontier.
**Covers:** Technology Trends Outlook 2026, Trend 01 Agentic software development, pp. 8–17 (chunk 02/15)
