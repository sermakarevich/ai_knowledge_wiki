> [[index|Wiki]] | [[summary|Summary]]

# Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment — Digest

## 1. [[wiki/01-tool-augmented-ontology-engineering|Tool-Augmented Ontology Engineering]]

**In one sentence:** Open Ontologies is a Rust, MCP-exposed ontology engineering system whose stable 1-to-1 matching alignment reaches F1 = 0.832 (P = 0.963) on OAEI Anatomy and whose structured MCP tool access (F1 = 0.717) far beats an LLM reading raw OWL (F1 = 0.323) or nothing (F1 = 0.431).

## Key points

- Open Ontologies is implemented in Rust (~17,400 lines) and ships as a single binary with no JVM or Python dependency, exposing construction, reasoning, alignment, and lifecycle tools via MCP.
- Core engine combines an Oxigraph triple store (in-memory SPARQL 1.1), OWL-RL forward chaining plus partial SHIQ tableaux consistency checking, a SHACL validator, and a pattern enforcer with configurable rule packs.
- Alignment scores each candidate class pair with six weighted signals (label 0.25, property 0.20, parent 0.15, instance 0.15, restriction 0.15, neighbourhood 0.10); when signals 2–6 are all zero, confidence falls back to label similarity × 0.85.
- Stable 1-to-1 matching (sorted by confidence, keep only top target per source and vice versa) is the dominant factor: on Anatomy it lifts the initial 12,557-candidate run (P = 0.102, R = 0.846, F1 = 0.182) to 1,154 candidates at F1 = 0.832 with the highest reported precision (0.963).
- Ablation across five weight configurations varies F1 by less than 0.004 with stable matching applied, while removing stable matching drops F1 to 0.728.
- On OAEI Conference (7 ontologies, 21 pairs, 15 evaluated) the same method gives micro-averaged F1 = 0.438 (P = 0.693, R = 0.320); recall is low because heterogeneous modelling styles minimise label overlap.
- On the OntoAxiom tool-access ablation (9 ontologies, 3,042 ground-truth axioms, 5 types; Claude Opus 4, claude-opus-4-20250514), raw OWL file reading (F1 = 0.323) scores worse than no file at all (F1 = 0.431), while structured MCP tools reach F1 = 0.717.

## 2. [[wiki/02-evaluation-results|Condition Input F1: LLM Alone vs Raw File vs MCP Tools]]

**In one sentence:** Giving the LLM a raw OWL file hurts extraction (F1 0.323 vs 0.431 unaided), while structured MCP/SPARQL tool access raises it to 0.717, and stable matching — not signal weights — dominates alignment.

## Key points

- Condition B (LLM, no tools, name lists) scores F1 0.431, Condition D (LLM + raw OWL file in context) scores 0.323, and Condition C (LLM + MCP tools, file via SPARQL) scores 0.717.
- Raw-file reading (D) is 25% worse than unaided LLM (B) because the LLM makes systematic extraction errors on raw Turtle, especially domain/range triples (F1 = 0.0 on 4 of 9 ontologies for domain extraction).
- Structured tools provide +122% over raw file access, while B-to-C improvement is +66% F1; richer input without tools hurts, so MCP tools are a qualitatively different access modality, not merely richer input.
- Condition D varies widely by Turtle complexity: NordStream 0.692, FOAF 0.647, GoodRelations 0.632 versus Time 0.087, Pizza 0.154, ERA 0.058.
- Alignment ablation on OAEI Anatomy (min confidence 0.80): all five stable-matching configurations score F1 0.830–0.834, while all three without stable matching score identical F1 0.728, so signal weights change F1 by less than 0.004.
- OWL-RL vs HermiT on LUBM gives different reasoning profiles/outputs: at 50,000 axioms OWL-RL takes 15 ms vs HermiT 24,490 ms (1,633× ratio); on Pizza (4,179 triples) HermiT computes 312 subsumptions in 213 ms while OWL-RL materialises inferred triples in 43 ms without the same subsumptions.
- LLM-driven Pizza construction via the MCP pipeline produces a 91-class ontology in under 5 minutes with 96% class coverage (95/99 classes), versus ~4 hours manual work; the 4 missing classes are teaching artifacts for OWL syntax variants.

## 3. [[wiki/03-references|References]]

**In one sentence:** This chunk is a bibliography fragment listing references 19–23 (OWL API, ROBOT, Owlready, SSSOM, OWL 2 Profiles) cited by the Open Ontologies paper.

## Key points

- Horridge and Bechhofer (2011) is cited for "The OWL API: A Java API for OWL Ontologies," published in Semantic Web 2(1), pages 11–21.
- Jackson et al. (2019) is cited for "ROBOT: A Tool for Automating Ontology Workflows," published in BMC Bioinformatics 20, article 407.
- Lamy (2017) is cited for "Owlready: Ontology-Oriented Programming in Python," published in Artificial Intelligence in Medicine 80, pages 11–28.
- Matentzoglu et al. (2022) is cited for "A Simple Standard for Sharing Ontological Mappings (SSSOM)," published in Database 2022, article baac035.
- Motik, Grau, Horrocks, et al. (2012) is cited for "OWL 2 Web Ontology Language Profiles (Second Edition)," a W3C Recommendation.

## The argument in five moves

1. Open Ontologies integrates LLM-driven construction with formal OWL reasoning and lifecycle management in a Rust single binary exposed via MCP tools.
2. On OAEI Anatomy, stable 1-to-1 matching turns a noisy 12,557-candidate run (F1 = 0.182) into a precise 1-to-1 alignment at F1 = 0.832 with record precision (0.963), while the same label-centric method manages only F1 = 0.438 on heterogeneous Conference pairs.
3. The ablation shows the assignment constraint, not signal engineering, does the work: weights move F1 by less than 0.004 under stable matching, and removing it drops F1 to 0.728.
4. The tool-access ablation shows structured MCP/SPARQL access (F1 = 0.717) is qualitatively different from information access, since raw OWL in context (F1 = 0.323) scores worse than the unaided LLM (F1 = 0.431), especially on domain/range triples and complex Turtle.
5. Fast OWL-RL engineering reasoning plus MCP tooling makes LLM construction practical (91-class Pizza ontology in under 5 minutes at 96% coverage), leaving Conference heterogeneity and the Anatomy recall gap (background knowledge) as the open challenges.
