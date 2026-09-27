[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Schema-Agnostic Knowledge Graph Construction via Hybrid Ontology Discovery for Cyber Threat Intelligence
**In one sentence:** The paper presents ANCHOR, a schema-agnostic CTI knowledge graph construction system whose hybrid ontology discovery (search-and-navigate) plus SHACL-based validation extracts ontology-aligned knowledge without schema-specific reconfiguration, outperforming baselines on UCO, STIX, and MALOnt while letting a local LLM match enterprise-LLM typing performance.
## Key points
- CTI reports capture adversary tactics, techniques, and procedures, but traditional platforms reduce them to isolated indicators via fixed schemas such as STIX, discarding causal dependencies between attack steps.
- Ontology-based representations (UCO [7], STUCCO [8], MALOnt [9], typically formalized in OWL with optional SHACL constraints) preserve semantic relationships, yet no single schema has achieved widespread adoption in practice [10].
- Existing extraction faces three stated problems: (i) schema-specific pipelines needing manual reconfiguration on schema change, (ii) prompt-based schema inclusion that fails to scale on large ontologies such as UCO, and (iii) reliance on enterprise LLM APIs conflicting with privacy constraints for sensitive internal incident data.
- ANCHOR's core is hybrid ontology discovery, described as a search-and-navigate mechanism that dynamically explores large-scale ontology schemas, combined with SHACL-based validation to enforce schema-compliant type assignments.
- Reported results on UCO, STIX, and MALOnt show ANCHOR outperforms existing baselines in ontology typing and schema compliance, and ANCHOR with a local LLM closely matches enterprise LLM typing performance.
- Conventional rule-based pipelines [11], [12] and classification models [13], [14] depend on hand-crafted rules or fixed type inventories requiring complete redesign on schema change; LLM-based methods [15]–[17] interpret class descriptions directly but were validated only on small custom schemas and fail on large real-world ontologies [18].
- Prompt-based inclusion of large-scale ontologies such as UCO fails because hundreds of hierarchical classes exhaust the context window and degrade the model's ability to distinguish semantically similar types.
---
## Title, authors, and abstract
**Covers:** Title block, author list, arXiv header, Abstract, Index Terms

Paper: "Schema-Agnostic Knowledge Graph Construction via Hybrid Ontology Discovery for Cyber Threat Intelligence" by Seonwoo Kim (Ministry of National Defense), Jinwoo Kim (Incheon International Airport Corporation), Daegyu Kang (Financial Security Institute), Daeseong Kim (Korean National Police Agency), and Insup Lee* (Korea University, corresponding author: islee94@korea.ac.kr). Header: "arXiv:2606.01208v1 [cs.CR] 31 May 2026".

Verbatim abstract claim:

> "In this paper, we present ANCHOR, a schema-agnostic CTI knowledge graph construction system that bridges LLMs and formal ontology schemas. At the core of ANCHOR is hybrid ontology discovery, a search-and-navigate mechanism that dynamically explores large-scale ontology schemas, combined with SHACL-based validation to enforce schema-compliant type assignments."

Abstract reports experimental results on the UCO, STIX, and MALOnt schemas showing ANCHOR "outperforms existing baselines in ontology typing and schema compliance", and that "ANCHOR with a local LLM closely matches enterprise LLM typing performance, enabling privacy-preserving CTI analysis with high fidelity."

Index Terms: "Cyber threat intelligence, ontology, knowledge graph, large language models".

## Introduction: indicator-oriented formats vs ontology-based graphs
**Covers:** Section I. Introduction (opening through ontology background)

The introduction argues comprehensive campaign analysis requires more than isolated indicators of compromise (IoC) [1]: CTI reports record threat actors, attack sequences, and technical evidence with explicit causal relationships between attack steps. Standardized formats STIX [2] and MISP [3] are widely adopted for automated sharing, but as indicator-oriented formats they "primarily capture low-level, isolated data points such as IP addresses and file names, discarding the causal dependencies between attack steps and the analytical reasoning that links them [4]–[6]."

Ontology-based representations address this by defining "a formal vocabulary of ontology classes, their properties (object and datatype), and structural constraints", with UCO [7], STUCCO [8], and MALOnt [9] as notable efforts, "typically formalized in the web ontology language (OWL) for class hierarchies and properties, supplemented by optional shapes constraint language (SHACL) constraints for structural validation." Despite many security ontologies, "no single schema has achieved widespread adoption in practice [10]."

The chunk's figure contrasts the two paradigms on one example sentence — "Buckeye APT used Trojan.Bemstour to install DoublePulsar by exploiting CVE-2019-0703": indicator-oriented extraction yields isolated attribute-value pairs (File name=Trojan.Bemstour, Vuln. name=CVE-2019-0703, Malware name=DoublePulsar) "without causal context", while the ontology-based knowledge graph preserves attack logic (Buckeye APT —uses→ Adversary/Exploit Tool relations, Trojan.Bemstour —delivers→ DoublePulsar, DoublePulsar —exploits→ CVE-2019-0703).

## Limitations of prior automated extraction
**Covers:** Section I, literature review (rule-based, classification, and LLM-based methods)

Conventional approaches rely on rule-based pipelines [11], [12] and classification models [13], [14], but "depend on hand-crafted rules or fixed type inventories, requiring a complete redesign whenever the target schema changes." LLM-based methods [15]–[17] suit schema-agnostic extraction better "because they can interpret ontology class descriptions directly without schema-specific engineering", but "existing LLM-based approaches have been validated only on small custom schemas and exhibit critical limitations when applied to large-scale, real-world ontologies [18]."

Three limitations are identified: first, conventional methods [11], [15]–[17] "either define their own custom schemas or hard-code a specific ontology into the extraction pipeline (schema dependency)", requiring "a complete redesign whenever the underlying schema changes"; second, prompt-based schema inclusion fails on large-scale ontologies such as UCO where "hundreds of hierarchical classes exhaust the context window and degrade the model's ability to distinguish semantically similar types"; third, "an inherent reliance on enterprise LLMs complicates the integration of external CTI with sensitive internal incident data due to privacy and data-sovereignty concerns."

## Challenges 1 and 2 (Challenge 3 is in the next chunk)
**Covers:** Section I, Challenge 1 and Challenge 2 statements (chunk ends mid-Challenge 2)

- Challenge 1) "How can we extract ontology-aligned knowledge without being tied to a specific schema?" To support diverse and evolving security standards [19], "the system must decouple extraction logic from schema definitions", allowing "different OWL/SHACL ontologies to be loaded without manually reconfiguring the pipeline."
- Challenge 2) "How can we handle large-scale ontologies that exceed the capacity of prompt-based schema inclusion? Rather than including the entire schema in the LLM prompt, the system must dynamically discover and retrieve only task-relevant ontology fragments." The chunk ends mid-sentence on the rationale: "This dynamic retrieval enables schema-aware reasoning within large and hierarchical ontologies while keeping each query within the context window."

**Covers:** Title block through Section I Introduction up to Challenge 2 (chunk 01/8, truncated mid-sentence); Challenge 3, system design, and evaluation are in later chunks.
