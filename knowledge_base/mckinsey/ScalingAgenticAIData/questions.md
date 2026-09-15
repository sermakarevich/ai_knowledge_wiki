# Questions — Scaling agentic AI with data transformations

Retrieval practice keyed to the six digest sections. Answers are hidden in collapsed blocks.

## 1. The scaling gap

**Q1 (recall):** What three headline statistics does the article use to frame the agentic AI scaling problem?

<details>
<summary>Answer</summary>

Nearly two-thirds of enterprises have experimented with agents, fewer than 10 percent have scaled them to tangible value, and eight in ten cite data limitations as the roadblock (Exhibit 1).

</details>

**Q2 (why / breaks):** Why do data workarounds that sufficed for human analysts collapse once agents run the workflow?

<details>
<summary>Answer</summary>

Humans patched fragmented data with judgment and manual reconciliation; agents coordinate multiple models and sources continuously without human intervention, so inconsistency compounds into breakdowns instead of being absorbed.

</details>

## 2. Two agentic archetypes

**Q3 (recall):** Name the two agentic archetypes and the distinct data each relies on.

<details>
<summary>Answer</summary>

Single-agent workflows, where one agent uses multiple tools and data sources sequentially; and multi-agent workflows, where specialized agents collaborate through shared knowledge graphs and fine-grained data access.

</details>

**Q4 (why / breaks):** What happens to each archetype when interoperable data is missing, and why do the failure modes differ?

<details>
<summary>Answer</summary>

The single agent makes inconsistent decisions because one reasoning thread sees conflicting versions of reality across sequential tool calls; the multi-agent system loses coordination and propagates errors because one agent's misread context becomes the next agent's input.

</details>

## 3. Seven data architecture principles

**Q5 (recall):** List four of the seven sidebar principles verbatim or near-verbatim.

<details>
<summary>Answer</summary>

Any four of: treat data ingestion like a product; share meaning, not just data; use one data foundation for analytics and AI; build trust into the platform by default; expose capabilities through stable interfaces; make behavior visible and measurable; provide a controlled way to run AI agents and applications.

</details>

**Q6 (transfer):** A bank's risk dashboard and its loan-approval agent disagree about a borrower's exposure. Which principle is violated, and what fix does it prescribe?

<details>
<summary>Answer</summary>

One data foundation for analytics and AI: build data once and use it everywhere so reports, models, and agents consume the same pipeline instead of drifting parallel copies.

</details>

## 4. Four steps to prepare data

**Q7 (recall):** State the four steps and the three criteria Step 1 uses to prioritize workflows.

<details>
<summary>Answer</summary>

Identify high-impact workflows to agentify; modernize each architecture layer; ensure continuous data quality; build the operating and governance model. Step 1 prioritizes by value potential, feasibility, and strategic fit.

</details>

**Q8 (why / breaks):** Why does the article warn against using AI advances to shortcut architecture best practices?

<details>
<summary>Answer</summary>

Because retrieval tricks and capable models only mask structural debt temporarily; the strongest organizations keep modular evolutionary architectures with replaceable components so each layer can be upgraded without rebuilding the system.

</details>

## 5. Modernizing the data stack

**Q9 (recall):** What are the medallion architecture and the AI gateway, and what does each do?

<details>
<summary>Answer</summary>

The medallion architecture progressively curates data from raw to agent-ready form while preserving lineage and auditability; the AI gateway governs model access to unstructured data, enforces usage policies, and records how data is retrieved and used in prompts and responses.

</details>

**Q10 (transfer):** An agent must answer questions from contracts, emails, and tickets. Which two platform-layer components make that unstructured content retrievable, and which layer gives it business meaning?

<details>
<summary>Answer</summary>

Vector stores and embedding services make unstructured content searchable by meaning; the semantic layer — ontologies plus knowledge graphs — codifies the business meaning.

</details>

## 6. Quality, cost, and the federated model

**Q11 (recall):** How does curated data reduce AI costs, and which three data classes must meet identical quality standards?

<details>
<summary>Answer</summary>

Well-structured internal data lets firms fine-tune smaller domain-specific models instead of paying full foundation-model inference, tuning, infrastructure, and governance costs; the smaller models are also more resilient and compliant. Identical standards apply to structured data, unstructured data, and agent-generated outputs.

</details>

**Q12 (why / breaks):** Who owns what in the federated accountability model, and what breaks if the split is ignored?

<details>
<summary>Answer</summary>

Business domains own day-to-day governance of agent workflows including domain models and ontologies; central data and AI teams own shared platforms, guardrails, and oversight. Without the split, either domains improvise incompatible controls or the center becomes a bottleneck that stalls every deployment.

</details>
