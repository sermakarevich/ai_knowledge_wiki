# Introducing the Google Cloud Knowledge Catalog

**Source:** [Introducing the Google Cloud Knowledge Catalog (Pydimukkala & McVeety, 2026)](https://cloud.google.com/blog/products/data-analytics/introducing-the-google-cloud-knowledge-catalog)
**Type:** Google Cloud product announcement blog post (April 22, 2026)

## Human Readable TL;DR

Imagine your company's data is a giant library, but the books have no covers, no table of contents, and no librarian -- so when you ask an AI assistant a question, it grabs random pages and makes up the rest. Google is turning its data service (Dataplex) into a smart librarian called the Knowledge Catalog: it reads every book, labels it, learns how books relate to each other, and hands AI agents the exact page they need in under a second. The big promise is fewer AI hallucinations and agents that actually know your business rules instead of guessing.

## TL;DR

Google Cloud is rebranding and expanding Dataplex into the **Knowledge Catalog**, a context engine purpose-built for AI agents. It stands on three pillars -- Aggregation (unifying metadata across BigQuery, SAP, Salesforce, Collibra, etc.), Enrichment (Gemini-powered auto-tagging of structured and unstructured data, verified SQL patterns, semantic guardrails), and Search (sub-second hybrid semantic search with access-control awareness). The goal is to give agents high-precision, secure, and governed context so they can execute complex tasks reliably instead of hallucinating joins or inventing business logic.

---

## Problem & Motivation

Traditional data catalogs were built as manual inventories for human technical users and focus on table structure, not the business semantics and relationships AI agents need. Without that deeper context, agents hallucinate, run slowly, and return stale insights. As enterprises push agentic workflows into production, this gap becomes a blocker for trust and adoption.

---

## Main Original Ideas

1. **Context Engine, Not a Catalog.** Reframes the data catalog from a passive human-facing inventory into an active, always-on context engine whose primary consumer is AI agents, not analysts.

2. **Three-Pillar Architecture (Aggregate / Enrich / Search).** Organizes the product around the lifecycle of context: pulling metadata in, generating meaning on top of it, and serving it with precision.

3. **Broad Metadata Aggregation with Federation.** Harvests from native Google systems (BigQuery, AlloyDB, Spanner, Cloud SQL, Firestore, Looker) and federates semantic context from third parties (Atlan, Collibra, Datahub, Ab Initio, Anomalo) and enterprise apps (Palantir, Salesforce Data360, SAP, ServiceNow, Workday).

4. **LookML Agent.** An autonomous agent that reads strategy docs and generates business-ready semantics across the whole semantic layer lifecycle, delivered as a VS Code extension so agents and analysts share one source of truth.

5. **BigQuery Measures.** Embeds programmatic business logic directly into the SQL engine, making every calculation reusable and mathematically consistent; aggregated alongside LookML into one governed semantic foundation.

6. **Data Products (GA).** Self-contained units bundling intent, SLAs, and governance constraints -- the building blocks for scaling complex AI use cases.

7. **Smart Storage and Object Context API.** Native GCS integration that auto-tags, embeds, and enriches unstructured files on arrival, making them instantly discoverable by agents.

8. **Deep Multimodal Metadata Extraction.** Gemini-powered pipelines automatically extract entities and business relationships from complex unstructured data.

9. **Automated Context Curation.** Generates natural-language glossaries, infers hidden relationships, and produces verified SQL patterns -- turning context maintenance into a continuous, automated process.

10. **Verified Queries and Semantic Guardrails.** Directly targets hallucinated joins and guessed SQL (a leading failure mode for AI) by shipping verified query patterns and pre-generated natural-language questions.

11. **Access Control-Aware Semantic Search.** Hybrid search with sub-second latency that respects source-system permissions, so agents cannot retrieve or act on data they are not authorized to see.

12. **Measurable Context Evaluation.** Evaluation framework that turns context engineering into a measurable discipline with quantitative iteration on context-construction strategies.

---

## Key Findings

| Capability | Status | Notable Claim |
|-----------|--------|---------------|
| Broad metadata aggregation | **GA** | Harvests across BigQuery, AlloyDB, Spanner, Cloud SQL + partners |
| Data products | **GA** | Includes SLAs, intent, governance |
| High-precision semantic search | **GA** | **Sub-second latency**, hybrid search |
| Enterprise connectivity | Preview | Palantir, SAP, Salesforce, ServiceNow, Workday |
| BigQuery Measures | Preview | SQL-engine-embedded business logic |
| Smart Storage / Object Context API | Preview | Auto-enrichment on GCS write |
| Deep multimodal extraction | Preview | Gemini-powered |
| Automated context curation | Preview | Glossaries + verified SQL |
| Verified queries & semantic guardrails | Preview | Anti-hallucination layer |
| Deep Research Agent (Gemini Enterprise) | Preview | Tasks in minutes vs. weeks |

- **Customer evidence -- Bloomberg Media:** launched a Data Access AI Agent on Knowledge Catalog; stakeholders explore the data lake via natural language with trusted grounding (William Anderson, CTO, Bloomberg Media).
- **Deep Research Agent:** synthesizes live business data, internal docs, and web research with deep citations; reduces multi-week manual research to minutes.
- **Ecosystem:** 5+ enterprise app integrations and 5 third-party catalog partners at launch.

---

## Suggestions & Future Directions

1. **Adopt Data Products as primary building blocks** for AI use cases, bundling SLAs and governance up front.
2. **Unify semantics via LookML Agent + BigQuery Measures** so analysts and agents share one definition layer.
3. **Turn on Smart Storage / Object Context API** for unstructured buckets to make files agent-discoverable by default.
4. **Use verified queries and semantic guardrails** as the anti-hallucination mechanism before shipping agent workflows.
5. **Quantify context quality** using the evaluation framework rather than treating context construction as ad hoc.
6. **Entry points:** Knowledge Catalog via the Dataplex console; Deep Research via Gemini Enterprise Agent Platform.

---

## Authors & Institutions

Chai Pydimukkala (Product Lead, Google Cloud), Sam McVeety (Tech Lead, Google Cloud).
