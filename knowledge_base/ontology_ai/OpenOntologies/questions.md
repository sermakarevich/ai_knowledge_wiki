---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment

### Q1. What is Open Ontologies and what are the four components of its core engine?
> [!tip]- Answer
> Open Ontologies is a Rust (~17,400 lines) single-binary ontology engineering system with no JVM or Python dependency that exposes construction, reasoning, alignment, and lifecycle tools via MCP. Its core engine combines an Oxigraph triple store with in-memory SPARQL 1.1, a native reasoner (OWL-RL forward chaining plus partial SHIQ tableaux consistency checking), a SHACL validator, and a pattern enforcer with configurable rule packs. Lifecycle management follows infrastructure-as-code: plan, enforce, apply, monitor, and drift, all recorded in an append-only lineage trail. See [[wiki/01-tool-augmented-ontology-engineering|Tool-Augmented Ontology Engineering]].

### Q2. How does the alignment module score candidate class pairs, and what happens when structural signals are all zero?
> [!tip]- Answer
> Each candidate class pair is scored as a weighted sum over six signals: label similarity (Jaro-Winkler + token Jaccard, 0.25), property overlap (0.20), parent overlap (0.15), instance overlap (0.15), restriction similarity (0.15), and neighbourhood similarity (0.10). When signals 2–6 are all zero, confidence falls back to label similarity with a 15% penalty (label sim × 0.85) so structurally unsupported matches cannot pass the threshold easily. Stable 1-to-1 matching then sorts candidates by confidence and keeps only the top target per source and vice versa, eliminating many-to-many spurious matches. See [[wiki/01-tool-augmented-ontology-engineering|Tool-Augmented Ontology Engineering]].

### Q3. What trajectory took OAEI Anatomy from F1 0.182 to 0.832, and why does the same method reach only F1 0.438 on Conference?
> [!tip]- Answer
> The initial Anatomy run produced 12,557 candidates (P 0.102, R 0.846, F1 0.182); adding stable 1-to-1 matching, the label × 0.85 penalty, and raising the label pre-filter from 0.70 to 0.75 cut candidates to 1,154 at F1 0.832 with record precision 0.963. The recall gap (0.733 vs AML's 0.922) comes from penalising true matches with low label similarity, fixable with domain background knowledge such as UMLS. On Conference (7 ontologies, 21 pairs, 15 evaluated) the same method gives micro-averaged F1 0.438 (P 0.693, R 0.320) because heterogeneous modelling styles minimise label overlap, versus SOTA LogMap 0.67 and BERTMap 0.71. See [[wiki/01-tool-augmented-ontology-engineering|Tool-Augmented Ontology Engineering]].

### Q4. Compare Conditions B, C, and D on the OntoAxiom benchmark and explain why reading the raw OWL file hurts.
> [!tip]- Answer
> On 9 ontologies with 3,042 ground-truth axioms of 5 types (Claude Opus 4), Condition B (LLM, name lists, no tools) scores F1 0.431, Condition D (LLM + raw OWL file in context) drops to 0.323, and Condition C (LLM + MCP tools, file via SPARQL) reaches 0.717. Raw Turtle reading is 25% worse than the unaided LLM because of systematic extraction errors, especially domain/range triples (F1 0.0 on 4 of 9 ontologies), plus confusion of property and class IRIs, language-tag mismatches, and missed multi-line axiom blocks. Condition D also varies by Turtle complexity: NordStream 0.692 and FOAF 0.647 versus Time 0.087, Pizza 0.154, and ERA 0.058. See [[wiki/02-evaluation-results|Condition Input F1: LLM Alone vs Raw File vs MCP Tools]].

### Q5. What does the alignment ablation show about signal weights versus stable matching, and how does the confidence threshold trade off precision and recall?
> [!tip]- Answer
> All five weight configurations with stable matching score F1 0.830–0.834, while all three without it score an identical F1 0.728, so weights move F1 by less than 0.004 and the 1-to-1 assignment constraint does the work. The reason is that most Anatomy class pairs have no structural data, so changing weights on zero-valued signals has no effect and stable matching selects a clean assignment regardless of scoring details. Threshold sensitivity with stable matching runs from 0.70 (P 0.643, R 0.811, F1 0.717) to 0.80 (P 0.961, R 0.732, F1 0.831) to 0.85 (P 0.977, R 0.689, F1 0.808). See [[wiki/02-evaluation-results|Condition Input F1: LLM Alone vs Raw File vs MCP Tools]].

### Q6. Which five references (19–23) does the paper cite, and what claim does each support?
> [!tip]- Answer
> Horridge and Bechhofer (2011) is cited for the OWL API as the Java foundation of most ontology tools, and Jackson et al. (2019) for ROBOT command-line management for the OBO community. Lamy (2017) is cited for Owlready Python-based ontology manipulation, and Matentzoglu et al. (2022) for SSSOM as the mapping exchange standard. Motik, Grau, Horrocks, et al. (2012) is cited for the OWL 2 Profiles W3C Recommendation, which underpins the system's OWL-RL reasoning choice. See [[wiki/03-references|References]].

### Q7. Should a team building LLM-driven ontology workflows adopt stable 1-to-1 matching plus MCP tool access, and with what caveats?
> [!tip]- Answer
> Yes: stable matching is the highest-leverage change (Anatomy F1 0.182 → 0.832 with record precision) while signal engineering buys under 0.004, and MCP tools (+122% over raw file, +66% over unaided LLM) are a qualitatively different access modality since raw OWL in context actively harms extraction. Caveats are that Conference heterogeneity still caps label-centric matching at F1 0.438, the Anatomy recall gap needs background knowledge such as UMLS, results are single-run Claude-only and not yet independently OAEI-evaluated, and OWL-RL is incomplete for OWL-DL so HermiT-class completeness is traded for interactive speed. See [[wiki/02-evaluation-results|Condition Input F1: LLM Alone vs Raw File vs MCP Tools]].
