# Scaling agentic AI with data transformations

**Article:** [Scaling agentic AI with data transformations](https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/building-the-foundations-for-agentic-ai-at-scale)

## Human Readable TL;DR

Think of AI agents as brilliant new hires who work at lightning speed but believe everything they read and never ask questions. Companies have hired them by the thousand, yet almost none get real work out of them, because the company filing cabinets are a mess: conflicting records, missing labels, no locks on the doors. The article is a cleanup manual saying that tidy, well-labeled, well-guarded information — plus managers retrained as supervisors — is what turns clever software into reliable coworkers.

---

## TL;DR

The article argues that agentic AI fails to scale because of fragile data foundations rather than model limits, citing near-two-thirds experimentation against sub-10-percent scaled value with eight in ten firms blaming data. Its method is a practitioner framework: two agent archetypes with distinct data failure modes, seven data architecture principles, and four coordinated steps spanning workflow selection, layered architecture modernization, continuous quality management, and operating-model redesign. The key result is a reference design — modular interoperable stack, semantic layer, AI gateway, medallion curation, federated governance — under which curated data becomes a cost-saving differentiator enabling smaller fine-tuned models.

---

## Problem & Motivation

Enterprises face a paradox of heavy agentic AI investment with almost no scaled return, and the article locates the cause in data that humans could historically patch through judgment but agents cannot. Fragmented siloed sources, conflicting definitions, and inconsistent governance turn autonomous multi-step workflows into error cascades, while periodic cleanups and perimeter controls prove too slow and too coarse for continuous unsupervised coordination. The gap matters because data foundations increasingly define competitive positioning, so leaders need a combined technology and organization program rather than another model upgrade.

---

## Main Original Ideas

1. **Two archetypes with asymmetric failure modes.** Single-agent workflows use tools sequentially while multi-agent workflows collaborate through shared knowledge graphs, and each breaks differently — inconsistent decisions versus lost coordination with error propagation — which lets architects target data investments to the design they run.
2. **Seven principles as an agent-ready platform contract.** Productized ingestion, shared meaning, one foundation for analytics and AI, default trust, stable interfaces, measurable behavior, and a controlled execution layer together convert legacy pipelines into infrastructure agents can safely consume.
3. **Agent outputs as governed data.** Agent-generated content and tool-mediated writes must meet the same accuracy, lineage, and reconciliation standards as inputs through governed reconcilable interfaces, closing a blind spot most quality programs ignore.
4. **One rulebook enforced automatically.** Agents get no separate governance regime; they follow existing enterprise standards applied by machines with per-agent role-based access checks that tighten as autonomy rises, making governance the primary control mechanism.
5. **Federated accountability for hybrid work.** Business domains own daily governance of agent workflows including models and ontologies while central data and AI teams own platforms and guardrails, balancing local speed with enterprise accountability as humans shift to supervision.

---

## Key Findings

| Claim | Detail |
|---|---|
| Adoption gap | Nearly two-thirds of enterprises experimented with agents; fewer than 10 percent scaled to tangible value |
| Data bottleneck | Eight in ten companies cite data limitations as the scaling roadblock (Exhibit 1) |
| Foundation effect | Capability foundations distinguish AI value creators from the rest (Rewired research) |
| Cost lever | Well-structured data enables smaller domain fine-tunes that cut inference, tuning, infrastructure, and governance spend while improving resilience and compliance |

- Single-agent designs need cross-step consistency while multi-agent designs need shared semantics plus fine-grained scoped access, and both collapse without interoperable data.
- Modernization should evolve each stack layer — ingestion, platform, semantic, products, consumption — with modular replaceable components rather than rip-and-replace rebuilds or AI shortcuts over structural debt.
- The semantic layer of ontologies and knowledge graphs turns raw data into machine-readable business meaning, without which agents misunderstand records they can technically access.
- Continuous real-time quality with automated validation, anomaly detection, and enrichment must cover structured records, unstructured content, and agent outputs alike, supported by metadata carrying lineage and business context.
- The AI gateway plus medallion curation and API-mediated access embeds governance in the stack so retrieval stays secure, efficient, and fully logged in prompts and responses.

---

## Suggestions & Future Directions

1. Start with a small number of high-value end-to-end workflows chosen for value, feasibility, and strategic fit, proving the pattern before broadening scope.
2. Build reusable assets deliberately — data products, agent capability modules, governance rules — so each pilot accelerates the next wave of scaling.
3. Treat the semantic layer as production infrastructure from the outset rather than research overhead, prioritizing the domains the first workflows require.
4. Close the acknowledged gaps the article leaves open: publish the survey evidence behind the headline statistics, detail migration paths for legacy batch estates, and specify threat models and credentialing for agent access.
5. Run foundation-building and production pilots in parallel with clear outcome metrics instead of sequencing architecture first and agents later.

---

## Authors & Institutions

Asin Tavakoli, Brian Goodman, Henning Soller, Kayvaun Rowshankish, with Akshat Kumar, Carlos Barreto, Satyajit Parekh, Tancredi Bernard Litta Modignani, McKinsey Technology and QuantumBlack, AI by McKinsey.
