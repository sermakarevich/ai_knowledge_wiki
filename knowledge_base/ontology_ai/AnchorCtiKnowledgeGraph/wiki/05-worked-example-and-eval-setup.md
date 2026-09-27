> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Worked Example (Buckeye / DoublePulsar) and Evaluation Setup

**In one sentence:** ANCHOR's Buckeye APT example graph traces 10 typed entities across five classes from exploit tools through CVEs and backdoors to the Shadow Brokers leak, and its evaluation grounds this capability in a 149-report CTINexus benchmark with reconstructed UCO/STIX 2.1 labels, three baselines, and a hierarchical F1 metric.

## Key points

- The Fig. 3 Buckeye example knowledge graph contains 10 typed entities of five classes (ThreatActor, Identity, Malware, Software, and Vulnerability) linked by typed predicates such as uses, delivers, and exploits.
- The attack chain runs from the exploit tool through the vulnerabilities and the backdoor to the Shadow Brokers leak, with CVE-2019-0703 and CVE-2017-0143 both typed as Vulnerability.
- If a SHACL violation persists after maximum retries, the system retains the entity with its assigned class and flags it with a validation warning rather than silently discarding it.
- SHACL shapes also support facet discovery for compound-structure ontologies such as UCO via property domain inspection, inheritance traversal, and SHACL shape resolution, with output serialized as an ontology-aligned KG in JSON format.
- The benchmark reuses CTINexus [16] with 149 CTI reports plus manually annotated entities, triplets, and ontology labels, extended with reconstructed ground truth for the larger UCO and STIX 2.1 schemas beyond MALOnt.
- Ground truth used an ensemble of three LLMs (GPT-5.4, Claude-Sonnet-4-6, Gemini-3.1-flash) for candidates plus manual cross-examination and consensus resolution by three cybersecurity researchers.
- Baselines are TTPDrill [11], CTINexus [16], and LLM4CTI [17] on Qwen3.5-35B served locally via vLLM on an NVIDIA GB10 / 128 GB workstation, excluding CTIKG [15] because it does extraction without ontology typing.
- UCO typing uses hierarchical F1 (1.0 exact, 0.6 one-step parent/child mismatch, 0.3 two-step mismatch) over three schema scales: UCO (419 classes), STIX (109 classes), MALOnt (75 classes).

---

## Fig. 3 worked example: Buckeye APT campaign report

**Covers:** Fig. 3 caption and surrounding description

"Fig. 3. Example knowledge graph constructed by ANCHOR from a Buckeye APT campaign report."

"To provide an intuitive understanding of how ANCHOR reconstructs semantic connectivity from an unstructured CTI report, as shown in Fig. 3, we visualize an example knowledge graph constructed from a Buckeye APT campaign report."

"The resulting graph contains 10 typed entities of five classes (ThreatActor, Identity, Malware, Software, and Vulnerability), connected by typed predicates (e.g., uses, delivers, and exploits) that trace the attack chain from the exploit tool through the vulnerabilities and the backdoor to the Shadow Brokers leak."

"The two vulnerabilities (CVE-2019-0703 and CVE-2017-0143) are typed against the Vulnerability class, demonstrating accurate resolution of numerical CVE references."

Visible graph labels in the chunk include Trojan.Bemstour (Malware), Windows (Software) delivering backdoor, DoublePulsar (Malware) with alias, Backdoor.DoubleParser, EternalSynergy (Malware), EternalRomance (Malware), Shadow Brokers (Identity), plus ThreatActor / uses / exploits / targets edges.

## SHACL validation tail and serialization

**Covers:** Section D tail (validation persistence, facet discovery, serialization)

"To prevent unbounded execution. If the violation persists after the maximum attempts, the system retains the entity with its assigned class and flags it with a validation warning rather than silently discarding it."

"This approach minimizes unverified type assignments while preserving the extracted intelligence."

"Beyond constraint checking, these SHACL shapes facilitate facet discovery for ontologies that organize auxiliary properties into compound structures (e.g., UCO). The system performs this through a multi-strategy lookup combining property domain inspection, inheritance traversal, and SHACL shape resolution."

"Finally, ANCHOR serializes the validated type assignments as an ontology-aligned knowledge graph in JSON format."

## Evaluation setup: benchmark and ground truth

**Covers:** Section V opening (reproducibility, Table II reference, human-in-the-loop labeling)

"For reproducibility, we use a benchmark provided by CTINexus [16], consisting of 149 CTI reports with manually annotated entities, triplets, and ontology type labels."

"The original benchmark targets only the small-scale MALOnt schema, so we additionally reconstruct ground-truth type labels for two larger schemas, UCO and STIX 2.1, as summarized in Table II."

"Three cybersecurity researchers established the ground truth through a human-in-the-loop process. An ensemble of three LLMs (GPT-5.4, Claude-Sonnet-4-6, and Gemini-3.1-flash) produced the initial candidates, and the researchers manually cross-examined and resolved conflicting assignments by consensus."

## Baselines, hardware, and models

**Covers:** Section V baselines and deployment paragraph

"For our baselines, we compare the F1 scores of ANCHOR against three systems: TTPDrill [11], CTINexus [16], and LLM4CTI [17]. We exclude CTIKG [15], as it performs only knowledge extraction without ontology typing."

"Since CTINexus originally types only entities, we extend it to predicate typing by reusing its prompt-based entity ontology typing method on relation predicates."

"We deploy ANCHOR on a workstation equipped with an NVIDIA GB10 board and 128 GB of memory, where we serve Qwen3.5-35B locally via vLLM [26]. For a fair comparison, all baselines also use Qwen3.5-35B as their underlying model."

"In the comparison against enterprise LLMs (Section V-D), we additionally use GPT-5.4-mini and Claude Haiku-4.5."

## Ontology typing performance setup

**Covers:** Section V-A opening (schemas, hierarchical F1, task definitions)

"We examine the ontology typing performance on three schemas with different scales: UCO (large, 419 classes), STIX (medium, 109 classes), and MALOnt (small, 75 classes)."

"Ontology typing measures whether the extracted entities and relations can be aligned to formal ontology classes and properties."

"Since the UCO schema is deeply nested with multi-level class hierarchies, we adopt a hierarchical F1 score that assigns full credit (1.0) for an exact match and partial credit (0.6 for a one-step parent or child mismatch, 0.3 for a two-step mismatch) to capture semantic proximity."

"We evaluate two complementary tasks: entity ontology typing, where each extracted entity is mapped to an ontology class uniform resource identifier (URI)" [chunk truncates here].

## Tables present in this chunk

**Covers:** TABLE III and TABLE V fragments as they appear in the chunk body

TABLE III — Entity ontology typing performance on three schemas:

| System | UCO | STIX | MALOnt | Average |
|---|---|---|---|---|
| TTPDrill [11] | 0.0652 | 0.1042 | 0.2305 | 0.1333 |
| CTINexus [16] | 0.4439 | 0.5698 | 0.6370 | 0.5502 |
| LLM4CTI [17] | 0.4521 | 0.7886 | 0.6891 | 0.6432 |
| ANCHOR | 0.7347 | 0.8724 | 0.6942 | 0.7371 |

TABLE V — Ablation study on hybrid ontology discovery components:

| Configuration | Entity Ontology Typing | Predicate Ontology Typing |
|---|---|---|
| Search-Only | 0.9184 | 0.3142 |
| Recurse-Only | 0.7914 | 0.6416 |
| Hybrid (ours) | 0.9364 | 0.7843 |

**Covers:** chunk 05-malware-types-exploits-buckeye-threatactor-v-e (Fig. 3 Buckeye/DoublePulsar worked example through Section V evaluation setup and V-A ontology-typing metric definition, plus TABLE III / TABLE V fragments)
