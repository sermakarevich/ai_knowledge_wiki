> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Challenges and Background: Privacy-Preserving Local LLMs, CTI Formats, and Limits of Indicator-Oriented Extraction
**In one sentence:** External CTI is most valuable when fused with sensitive internal data that cannot be sent to enterprise LLMs, so ANCHOR proposes schema-agnostic, ontology-grounded KG construction with locally deployed open-source LLMs, motivated by information loss in flat indicator formats and the failure of prompt-based schema inclusion to scale to large ontologies like UCO.
## Key points
- Challenge 3 frames the privacy constraint: internal alerts, logs, and incident reports are too sensitive to expose to enterprise LLMs, so ontology-grounded reasoning must run on locally deployed open-source LLMs with competitive typing performance.
- ANCHOR (Adaptive Navigation for Cybersecurity Hybrid Ontology Reasoning) decouples the extraction pipeline from any specific schema and supports arbitrary OWL/SHACL ontologies at runtime without manual reconfiguration.
- Hybrid ontology discovery combines embedding-based semantic search with LLM-guided recursive navigation to retrieve only task-relevant ontology fragments, integrated with closed-loop SHACL validation for schema-compliant graphs.
- Local open-source LLM deployment retains 99.2% (entity) and 97.8% (predicate) of the best enterprise LLM's performance.
- Indicator-oriented formats (STIX, MISP, TAXII) log discrete values but omit causality and rationale, fragmenting attack logic such as macro → payload download → scheduled-task persistence → C2 connection and TTP-overlap attribution to APT-X.
- Prompt-based full schema inclusion works at small scale (60–77 elements: MALOnt 60, STIX 77) but fails on large ontologies such as UCO (419 classes cited in scalability discussion; up to 997 in Table I), via context exhaustion/"Lost in the Middle", precision degradation, and maintenance burden.
- No existing baselines in the comparison verify assigned types against formal structural constraints, allowing invalid mappings into the KG; ANCHOR instead enforces SHACL checks with re-invocation on violation until conformant or retry budget exhausted.
---
## 1. Challenge 3: privacy-preserving CTI analysis with local LLMs
**Covers:** Challenge 3 statement and ANCHOR proposal paragraph

> "Challenge 3) How can we support privacy-preserving CTI analysis with local LLMs? External CTI provides greater operational value when integrated with internal alerts, logs, and incident reports, but such data is often too sensitive to expose to enterprise LLMs. The system must therefore enable ontology-grounded reasoning with locally deployed open-source LLMs while preserving competitive typing performance."

Proposed response in chunk:

> "To this end, we propose ANCHOR (Adaptive Navigation for Cybersecurity Hybrid Ontology Reasoning), a schema-agnostic system that builds a structured threat knowledge graph from unstructured CTI reports."

Mechanism as stated:
- Hybrid ontology discovery: LLMs dynamically explore relevant sub-graphs of complex ontologies; separates extraction pipeline from any specific schema.
- SHACL-based validation during ontology typing to ensure accurate and schema-compliant alignment.

## 2. Contributions
**Covers:** Contribution bullets, Section I tail

- Schema-agnostic CTI KG construction framework decoupling extraction from any ontology schema, supporting arbitrary OWL/SHACL ontologies at runtime without manual reconfiguration.
- Hybrid ontology discovery combining embedding-based semantic search with LLM-guided recursive navigation to retrieve only task-relevant ontologies, plus closed-loop SHACL validation.
- Privacy-preserving construction with locally deployed open-source LLMs, retaining 99.2% (entity) and 97.8% (predicate) of best enterprise LLM performance.
- Source code "will be publicly available in the near future."

## 3. Background: CTI data formats, ontologies, LLM extraction
**Covers:** Section II-A–II-B

CTI records adversary TTPs and IoCs as a shared resource against rapidly changing threats; open-source CTI (OSCTI) comes from security blogs, threat reports, and vulnerability databases.

Three widely adopted formats/protocols:
- STIX [2]: domain objects (threat actors, malware, vulnerabilities) and relationships in JSON.
- MISP [3]: collaborative IoC-sharing framework with predefined attribute taxonomy.
- TAXII [21]: transport protocol distributing STIX-formatted data.

Their limit: flat attribute-value pairs and predefined relationship types; Fig. 1 contrasts indicator-oriented flat data vs ontology-based KG where semantic relationships connect entities so analysts trace full attack flow.

Ontology language details in chunk:
- OWL defines class hierarchies plus object/datatype properties, often with SHACL constraints (required attributes, cardinality bounds).
- UCO [7] unifies CyBOK, NIST, MITRE ATT&CK into one hierarchical OWL/SHACL framework with hundreds of classes and properties.
- MALOnt [9]: lightweight malware ontology with only 75 classes, 10 relations, 12 properties.
- Open problems cited: inconsistencies/ambiguities in cybersecurity terminology [10]; no ontology fully aligns with major standards for seamless cross-platform integration.

LLM-based extraction:
- LLMs outperform rule/keyword systems that miss attacker intent and context; studies [5],[15]–[17] extract entities and semantic relationships with high performance, reducing manual analyst work.
- Traditional per-source integrations create tightly coupled pipelines; recent agent frameworks with standardized interfaces (aligned with model context protocol (MCP) [24]) ground outputs in verifiable references; ANCHOR adopts this to decouple extraction logic from schema (Section IV).

## 4. Motivating examples
**Covers:** Section III-A–III-B, Table I

### A. Information loss in indicator-oriented formats
Verbatim scenario passage:

> "In early March 2024, security analysts identified a spear-phishing campaign targeting Southeast Asian financial institutions. The attacker delivered a Microsoft Word document disguised as an invoice via email. When a user opens the document, a macro executes to download a secondary payload from hxxp://update-check[.]site/loader.exe. This payload maintained access by creating a scheduled task named "WindowsUpdateCheck" and afterward communicated with a command and control (C2) server at 45.77.23.91 via TCP port 443. Analysis revealed that these techniques align with the activities of APT-X, known for macro-based initial access and invoice-themed lures."

STIX-style mapping preserves only:
- Indicators: URL "update-check[.]site", IP "45[.]77[.]23[.]91", File "loader.exe"
- Objects: Scheduled Task "WindowsUpdateCheck", Identity Financial Sector
- Relationships: Attributed-to APT-X

Chunk's diagnosis: isolation loses semantic connectivity — the causal chain ((i) macro execution downloads secondary payload, (ii) C2 connection enables remote control) and attribution rationale (TTP overlap with APT-X) are omitted, leaving a fragmented snapshot with no attack logic; ontology-based KG explicitly models that connectivity.

### B. Limited scalability of prompt-based schema inclusion
Existing methods embed the entire class list in the prompt. Comparison (TABLE I):

| System | Method | Schema dependency | Schema size |
|---|---|---|---|
| TTPDrill [11] | Rule | Fixed (ATT&CK) | - |
| CTIKG [15] | LLM (prompt) | Open-ended | - |
| CTINexus [16] | LLM (prompt) | Fixed (MALOnt) | 60 |
| LLM4CTI [17] | LLM (prompt) | Fixed (STIX) | 77 |
| ANCHOR | LLM (hybrid) | Any OWL/SHACL | Up to 997 (UCO) |

Three limitations when applied to large ontologies such as UCO (419 classes):
- Context exhaustion: massive prompts trigger the "Lost in the Middle" phenomenon [25].
- Precision degradation: too many candidates confuse adjacent types (e.g., Process, Action, Event) or hallucinate non-existent classes.
- Maintenance burden: fixed class list needs manual reconfiguration on schema update.
- Plus no baseline verifies types against formal structural constraints, so invalid mappings enter undetected.

Stated requirements: dynamic exploration retrieving only task-relevant fragments on demand, plus formal constraint enforcement before commit — motivating ANCHOR's discovery + validation design in Section IV.

## 5. ANCHOR design overview (beginning)
**Covers:** Section IV-A system overview through Fig. 2 caption/start; Sections IV-B/IV-C detail belongs to chunk 04

Three principles:
1. Extraction decoupled from any ontology schema; arbitrary OWL/SHACL at runtime.
2. Ontology fragments discovered dynamically, keeping each query within context window.
3. Every type assignment verified against formal schema constraints before commitment.

Three components (Fig. 2: "(1) Schema-Agnostic Extraction / (2) Hybrid Ontology Discovery / (3) Knowledge Graph Construction"):
- Schema-agnostic extraction: entities, coreferences, relation triplets without binding to ontology; forwards output for type assignment.
- Hybrid ontology discovery: aligns each element to class/property URI via embedding search + LLM-guided hierarchical navigation over OWL/SHACL; falls back to recursive traversal when confidence < threshold τ.
- KG construction: SHACL-based closed-loop correction — check candidate, re-invoke mapper with violation report until conformant or retry budget exhausted; serialize as JSON and optionally Neo4j-importable Cypher for multi-hop attack-chain queries.

Input preprocessing note (pipeline start): recursive character-based splitting respecting paragraph/sentence/word boundaries with fixed-size overlap to preserve cross-boundary context; knowledge extraction follows as entity extraction → coreference resolution → triplet extraction (full detail in next page).

**Covers:** Challenge 3 statement through Section IV-A overview and Fig. 2 header (Sections I–III fully; Section IV only its overview principles and three-component architecture, not the full IV-B/IV-C pipeline).
