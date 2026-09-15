[[../index.md|Scaling agentic AI with data transformations]] · Page 5 — stack layers, retail exhibit, semantic layer

# Modernizing each layer of the data stack

**In one sentence:** Rather than rebuilding from scratch, companies modernize every layer of the stack — source ingestion with governance traveling alongside the data, a connected platform with vector stores and agent interoperability standards, a semantic layer of ontologies and knowledge graphs that turns data into knowledge, reusable data products with agent-use observability, and a consumption layer where orchestration and retrieval services assemble context dynamically under an AI (Artificial Intelligence) gateway and medallion-architecture controls.

## Key points

- Preparing the architecture means strengthening and adjusting each layer of the data stack to improve visibility and governance across workflows, evolving existing platforms instead of rebuilding systems from scratch.
- Data products turn curated data into reusable business-ready assets packaged with clear ownership, quality standards, semantics, and consumption interfaces, letting agents draw on trustworthy predictive and generative insights at scale.
- Observability of agent data use creates the traceability needed for oversight and enables feedback loops that improve upstream data and models over time.
- Agentic orchestration and retrieval services in the consumption layer let AI systems dynamically assemble context — often from unstructured data — deciding what to retrieve, how to refine it, and when to iterate, with retrieval kept secure, efficient, and governed at scale.
- A medallion architecture progressively curates and enriches data from raw to agent-ready form while preserving lineage and auditability, with access governed through Application Programming Interfaces (APIs), queries, and permissions.
- An AI gateway governs model access to unstructured data by enforcing usage policies and recording how data is retrieved and used in prompts and responses.
- The semantic layer sits between raw data and AI applications and codifies business meaning into machine-readable yet human-understandable form, implemented through ontologies that define how attributes and relationships combine into business reality and knowledge graphs that link real-world data across systems into connected entity networks.

---

## The retail exhibit: layers in action [unverified: exhibit details reconstructed from secondary extracts]

The article illustrates modernization with an omnichannel retail scenario. At the source layer, customer data such as browsing history, wishlists, purchase history, and support interactions enters from many systems; unstructured content undergoes continuous ingestion, transformation, and recombination, with quality checks, security controls, and lineage tracking automated inside the pipelines rather than handled as one-time reviews. At the platform layer, systems are connected through orchestrated access, synchronization, and real-time cross-system interaction, with vector stores and embedding services as key unstructured-data infrastructure and agent interoperability standards such as Model Context Protocol (MCP) and agent-to-agent (A2A) communication automating integration and access.

## Data products and the consumption layer

The product mindset treats data as a performance asset reusable across use cases and domains: ownership, standards, semantics, and interfaces travel with the asset. In consumption, orchestration replaces predefined queries — the system decides what to retrieve, refines it, and iterates — while retrieval services enforce the security, efficiency, and governance envelope at scale.

## Governance inside the stack

Control is layered, not perimeter-only: medallion curation from raw to agent-ready with lineage intact, access mediated by APIs, queries, and permissions, and the AI gateway standing between models and unstructured data to enforce policy and log every retrieval into prompts and responses. Governance travels with the data instead of sitting at system boundaries.

## The semantic layer up close

"Ontologies define how attributes and relationships add up to business reality. Knowledge graphs operationalize this vocabulary by linking real-world data across systems into a connected network of entities." Without this layer, agents act on data they can technically access but do not truly understand — the root cause of conflicting agent outputs over identical underlying records.

**Covers:** source section 4 (layer modernization; retail scenario; semantic layer; gateway and medallion controls).
