[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Tool-Augmented Ontology Engineering
**In one sentence:** Open Ontologies is a Rust, MCP-exposed ontology engineering system whose stable 1-to-1 matching alignment reaches F1 = 0.832 (P = 0.963) on OAEI Anatomy and whose structured MCP tool access (F1 = 0.717) far beats an LLM reading raw OWL (F1 = 0.323) or nothing (F1 = 0.431).
## Key points
- Open Ontologies is implemented in Rust (~17,400 lines) and ships as a single binary with no JVM or Python dependency, exposing construction, reasoning, alignment, and lifecycle tools via MCP.
- Core engine combines an Oxigraph triple store (in-memory SPARQL 1.1), OWL-RL forward chaining plus partial SHIQ tableaux consistency checking, a SHACL validator, and a pattern enforcer with configurable rule packs.
- Alignment scores each candidate class pair with six weighted signals (label 0.25, property 0.20, parent 0.15, instance 0.15, restriction 0.15, neighbourhood 0.10); when signals 2–6 are all zero, confidence falls back to label similarity × 0.85.
- Stable 1-to-1 matching (sorted by confidence, keep only top target per source and vice versa) is the dominant factor: on Anatomy it lifts the initial 12,557-candidate run (P = 0.102, R = 0.846, F1 = 0.182) to 1,154 candidates at F1 = 0.832 with the highest reported precision (0.963).
- Ablation across five weight configurations varies F1 by less than 0.004 with stable matching applied, while removing stable matching drops F1 to 0.728.
- On OAEI Conference (7 ontologies, 21 pairs, 15 evaluated) the same method gives micro-averaged F1 = 0.438 (P = 0.693, R = 0.320); recall is low because heterogeneous modelling styles minimise label overlap.
- On the OntoAxiom tool-access ablation (9 ontologies, 3,042 ground-truth axioms, 5 types; Claude Opus 4, claude-opus-4-20250514), raw OWL file reading (F1 = 0.323) scores worse than no file at all (F1 = 0.431), while structured MCP tools reach F1 = 0.717.
---
## Abstract
The paper presents "Open Ontologies, an open-source ontology engineering system implemented in Rust that integrates LLM-driven construction with formal OWL reasoning and ontology alignment via the Model Context Protocol." Primary finding: "stable 1-to-1 matching is the dominant factor in ontology alignment quality: on the OAEI Anatomy track, it achieves F1 = 0.832 (P = 0.963, R = 0.733), competitive with state-of-the-art systems and exceeding all in precision." Ablation: "signal weights are irrelevant when stable matching is applied (F1 varies by less than 0.004), while removing stable matching drops F1 to 0.728." Conference track: F1 = 0.438. Tool-access result: "an LLM reading a raw OWL file (F1 = 0.323) performs worse than the same LLM with no file at all (F1 = 0.431), while structured MCP tool access achieves F1 = 0.717." Verbatim conclusion: "This demonstrates that tool structure provides a qualitatively different mode of access that the LLM cannot replicate by reading raw syntax." System "ships as a single binary under the MIT licence." Keywords: "Ontology engineering · Ontology alignment · Stable matching · Large language models · Model Context Protocol · OWL reasoning." Author: Fabio Rovai, The Tesseract Academy, London; arXiv:2605.09184v1 [cs.AI] 9 May 2026.
## 1. Introduction
LLMs "can generate syntactically valid OWL and orchestrate multi-step ontology engineering workflows" but "cannot, however, guarantee logical consistency or verify that generated axioms are mutually coherent." Alignment systems "achieve strong pairwise matching on standard benchmarks but operate as standalone pipelines, disconnected from construction workflows and lifecycle management." Open Ontologies addresses both gaps by exposing "ontology construction, reasoning, alignment, and lifecycle tools via the Model Context Protocol (MCP) [8], enabling integrated workflows where an LLM generates OWL, validates it against formal constraints, and refines based on symbolic feedback." Three contributions claimed: (1) stable matching alignment at F1 = 0.832 on Anatomy (P = 0.963), weights irrelevant under stable matching; Conference F1 = 0.438; (2) tool-access ablation (raw file 0.323 vs unaided 0.431 vs MCP tools 0.717), "disentangles the effect of tool structure from information availability"; (3) the open-source Rust system integrating "OWL-RL reasoning, alignment, and lifecycle management into an LLM-orchestrated workflow."
## 2. Related Work
Ontology matching: OAEI [3] benchmarks annually; "LogMap [4] combines lexical matching with structural repair and logical consistency checking. AML [5] uses background knowledge from BioPortal and UMLS. BERTMap [6] introduced transformer-based embedding matching. OLaLa [7] uses LLM world knowledge for candidate adjudication." Differentiator: "the matching constraint (1-to-1 assignment) dominates signal design." OWL reasoning: "HermiT [2] implements hypertableau calculus for OWL2-DL. Pellet [10] and FaCT++ [11] provide alternative implementations. ELK [12] achieves polynomial-time reasoning for the EL profile. All are Java-based." This system: "Rust-native OWL-RL forward chaining with a partial SHIQ tableaux for consistency checking." AI-assisted construction: "OntoGPT [13] extracts ontology terms from text. OntoChat [14] provides conversational construction. LLMs4OL [15] evaluates LLMs for ontology learning. OntoAxiom [1] benchmarks axiom identification across 9 ontologies, finding that even o1 achieves only F1 = 0.197 from name lists." Gap: "None integrate formal validation into the construction loop or evaluate the effect of tool access modality on extraction quality." Programmatic engineering: "The OWL API [19] provides the Java foundation for most ontology tools. ROBOT [20] offers command-line management for the OBO community. Owlready2 [21] provides Python-based manipulation. SSSOM [22] standardises mapping formats. These target expert users; our system targets LLM-orchestrated workflows."
## 3. System Architecture
Implemented in Rust (~17,400 lines), single binary, no JVM/Python dependency; exposes construction, reasoning, alignment, lifecycle tools via MCP [8].
### 3.1 Core Engine
Four parts: "(1) an Oxigraph triple store [9] providing in-memory SPARQL 1.1 query and update; (2) a native reasoner with two modes: OWL-RL forward-chaining rules [23] for triple materialisation, and a partial SHIQ tableaux for consistency checking; (3) a SHACL validator for shape constraints; and (4) a pattern enforcer with configurable rule packs."
### 3.2 Alignment Module
Score per candidate class pair: score(cs,ct) = sum of wi · si over i=1..6. Six signals: "(1) label similarity (Jaro-Winkler + token Jaccard, w1 = 0.25); (2) property overlap (Jaccard, w2 = 0.20); (3) parent overlap (w3 = 0.15); (4) instance overlap (w4 = 0.15); (5) restriction similarity (w5 = 0.15); (6) neighbourhood similarity (w6 = 0.10)." Fallback: "When all structural signals (2–6) are zero, confidence falls back to label similarity with a 15% penalty (label sim × 0.85), preventing structurally unsupported matches from passing the threshold." Then: "stable 1-to-1 matching is applied: candidates are sorted by confidence, and for each source class only the top-scoring target is retained (and vice versa). This eliminates many-to-many spurious matches."
### 3.3 Lifecycle Management
"Inspired by infrastructure-as-code [18]: plan (diff with blast-radius scoring), enforce (design pattern compliance), apply (safe reload or migration), monitor (SPARQL watchers with alerts), drift (version comparison). All operations recorded in an append-only lineage trail."
## 4. Evaluation (reproducibility; Anatomy; Conference; tool access — partial)
Reproducibility: "LLM benchmarks use Claude Opus 4 (Anthropic, model ID claude-opus-4-20250514), default temperature. Single-run results. Non-LLM benchmarks (LUBM, OAEI alignment, marketplace loading) are deterministic. All scripts and data are in the repository under benchmark/."
### 4.1 OAEI Alignment: Anatomy Track
Track size: 2,737 mouse classes, 3,304 human classes, 1,516 reference mappings [3]; system "achieves the highest precision of any reported system."

| System | P | R | F1 |
|---|---|---|---|
| AML [5] | 0.950 | 0.922 | 0.936 |
| BERTMap [6] | 0.940 | 0.910 | 0.924 |
| LogMap [4] | 0.930 | 0.890 | 0.912 |
| OLaLa [7] | 0.900 | 0.880 | 0.890 |
| Open Ontologies | 0.963 | 0.733 | 0.832 |

Table 1 caption (verbatim): "OAEI Anatomy results. Our system achieves the highest precision, with a recall gap due to the conservative label penalty." Trajectory: "The initial system (before stable matching) produced 12,557 candidates with P = 0.102, R = 0.846, F1 = 0.182. Three changes lifted performance: (a) stable 1-to-1 matching, eliminating many-to-many spurious candidates; (b) a label penalty (label sim × 0.85) when structural signals are zero; and (c) raising the label pre-filter from 0.70 to 0.75. Together these reduced candidates from 12,557 to 1,154." Recall gap cause: "true matches with low label similarity are penalised. Integrating domain-specific background knowledge (UMLS, as LogMap and AML use) would allow accepting these matches when supported by external evidence." Module "accepts pluggable similarity functions and can load domain-specific ONNX embedding models."
### 4.2 OAEI Alignment: Conference Track
"On the Conference track (7 ontologies, 21 pairwise alignments, 15 evaluated with available data), the same method achieves micro-averaged F1 = 0.438 (P = 0.693, R = 0.320)." Cause: "Precision remains reasonable (0.693), but recall is low (0.320) because conference ontologies use heterogeneous modelling styles where label overlap is minimal." Table 2 caption: "OAEI Conference track: per-pair results (selected). Published SOTA: LogMap 0.67, BERTMap 0.71."

| Pair | Ref | Cands | F1 |
|---|---|---|---|
| cmt-iasted | 4 | 5 | 0.667 |
| ekaw-iasted | 10 | 7 | 0.588 |
| ekaw-sigkdd | 11 | 4 | 0.533 |
| iasted-sigkdd | 15 | 9 | 0.500 |
| conference-edas | 17 | 8 | 0.480 |
| cmt-sigkdd | 12 | 5 | 0.471 |
| edas-sigkdd | 15 | 4 | 0.211 |
| Micro-average | | | 0.438 |

### 4.3 Tool-Augmented Ontology Interaction (chunk truncates mid-table)
Setup: "We use the OntoAxiom benchmark [1] (9 ontologies, 3,042 ground truth axioms, 5 types) to evaluate three access modalities. The original benchmark tests LLM inference from name lists. We add two conditions: reading the raw OWL file, and using MCP tools." Table 3 caption (verbatim, values from abstract/§1 since table body is cut off in this chunk): "Tool access modalities on OntoAxiom. Condition D (raw file) performs worse than Condition B (no file), demonstrating that raw syntax is not just unhelpful but actively harmful." Known values from this chunk: raw file F1 = 0.323, no file F1 = 0.431, MCP tools F1 = 0.717. Full Table 3 rows are not present in this chunk.
**Covers:** Abstract through §4.3 (Table 3 caption only; table body truncated in chunk) — system overview, MCP tooling, stable matching alignment approach.
