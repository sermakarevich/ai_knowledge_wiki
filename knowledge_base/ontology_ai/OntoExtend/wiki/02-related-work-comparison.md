> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related-Work Comparison and the OntoExtend Framework
**In one sentence:** Prior LLM-based ontology extension is mostly semi-automatic, taxonomy-biased enrichment with little formal evaluation and no retrieval of existing baseline elements, so OntoExtend adds a retrieval-grounded pipeline (Retriever, Extender, Integrator) that anchors LLM-generated TBox fragments in the input ontologies.
## Key points
- The comparison table scores OntoExtend as Y on all ten criteria while the closest prior row, [16] Ontology engineering assistant, scores Y on seven (Y Y N Y Y Y N Y Y N).
- The synthesis claims current work is predominantly semi-automatic enrichment of existing inputs with a bias toward taxonomic growth, constrained by reproducibility, reliance on interactive tools, limited support for complex axioms, and continued need for human judgment in requirement elicitation and validation.
- No surveyed method focuses on retrieval of existing ontology elements from baseline ontologies, whereas OntoExtend integrates retrieval directly into extension; most surveyed works use minimal to no formal evaluation.
- The Retriever builds a FAISS [5] inner-product index over OntologyElement records (IRI, labels/comments, domain/range, super-/sub-relations, verbatim Turtle snippet) embedded as pipe-delimited strings, returning top-k (default 20) elements per competency question (CQ).
- The Extender injects retrieved Turtle snippets as read-only context plus a merged namespace prefix block, enforces reuse-without-redeclaration, and gates fragments through a two-stage validator (Turtle parser plus domain/range constraint checker, configurable per use case).
- Two deployment prompt templates are used: a SHACL-based template for the industrial ontology (NodeShape/PropertyShape, naming conventions, sh:name labels) and a generic restrictions plus reuse-of-classes template for the EU ontology (mandatory rdfs:label and rdfs:comment on every new class/property).
- The Integrator only deduplicates (repeated axioms, classes, properties, prefixes) and concatenates the cleaned fragment, and its re-indexing of generated fragments for later CQs was disabled in the evaluation so each CQ fragment could be assessed independently.
---
## Related-work table tail and synthesis
The chunk preserves the bottom rows of a comparison table whose columns are N/Y/P flags (headers not present in the chunk):

| Work | Flags (10 columns, as printed) |
|---|---|
| [26] Interactive taxonomy extension | N N N N N Y Y Y Y N |
| [18] Protégé plugin / CNL to OWL | N N P N N N N N N N |
| [22] Prototype ontology extension | N N N N N Y Y Y Y N |
| [8] Taxonomy enrichment (Taxoria) | N N N N N N N N Y P |
| [29] Online clustering framework | N N N N N N N N Y Y |
| [3] Biomedical enrichment benchmark | N N N N N N N N Y P |
| [12] Multi-LLM extension workflow | N P P N N N N N Y P |
| [10] AI Ontology curation support | N P Y N N N N N Y P |
| [7] Human-reviewed ontology extension | N Y N Y N N N Y Y N |
| [9] RAG ontology construction | N N N N N N N N N Y |
| [1] Research ontology construction | N N N N N N N N Y Y |
| [17] Ontology generation | N N N N N N N N Y N |
| [21] Ontology-Toolkit | N N N N N N N N N N |
| [4] Ontology generation from seeds/corpora | N N Y N N N N N N N |
| [27] Ontology transformation support | N N N Y N N Y N Y N |
| [25] Ontology engineering assistant | N Y N Y N N N Y N N |
| [16] Ontology engineering assistant | Y Y N Y Y Y N Y Y N |
| Ours OntoExtend | Y Y Y Y Y Y Y Y Y Y |

Verbatim synthesis (line breaks normalised):

> "These works reveal that current LLM-based ontology extension is predominantly semi-automatic enrichment of existing inputs with a bias toward taxonomic growth, facing recurring constraints around reproducibility, reliance on interactive tools, limited support for complex axioms, and continued necessity of human judgment for requirement elicitation and validation. However, none of these methods focuses on the retrieval of existing ontology elements from baseline ontologies, while our approach integrates retrieval mechanisms directly into the extension process. Furthermore, most of the works use minimal to no formal evaluation."

Nearby-but-distinct lines of work:

> "Several related works sit nearby but are less about extending a mature input ontology and more about generating or reconstructing ontologies from scratch [1,4,9,17,21] A parallel line of work looks at ontology transformation and general LLM-based assistance for ontology engineering [16,24,25,27]. These works reinforce the usefulness of LLM support throughout the ontology lifecycle, but they do not yet address retrieval-aware, requirement-driven extension of a mature input ontology."

## 3. The OntoExtend framework
Retrieval-based pipeline organised into three principal subsystems — Ontology Retriever, Ontology Extender, and Ontology Integrator (illustrated in Fig. 1). Input ontologies and reference ontologies are the same artefacts: the ontology (or ontologies) the user wants to extend, which are also indexed by the Retriever. The RAG component indexes the same ontology files that constitute the extension target so generated fragments are grounded in existing modelling choices; optionally, previously generated fragments can be re-indexed so later CQs build on earlier ones.

## 3.1. Ontology Retriever
Motivation: the whole set of input ontologies may not fit into current LLM context sizes, so the Retriever constructs and queries a semantic index over the input ontologies. At preprocessing time it parses each user-specified ontology file and iterates over all declared OWL entities, including classes, object properties, data properties, annotations, and their SHACL shapes if available. For each entity it constructs an OntologyElement record containing: entity IRI; human-readable labels and comments if present; domain and range declarations where applicable; super- and sub-class (or sub-property) relations; and a verbatim Turtle snippet of the canonical declaration. Each element is serialised as a pipe-delimited string combining URI local name, label, comment, element type, and domain/range before embedding with a configurable sentence embedding model, e.g. 'hasMaterialComponent | has material component | ... | Type: object property | Domain: Material | Range: MaterialComponent' (example also shown in Figure 2, "Example of the element to be embedded"). Vectors are normalized and stored in a FAISS index [5] configured for inner-product similarity, enabling efficient nearest-neighbour search with cosine-like semantics. At query time a user-supplied CQ is embedded into the same vector space and the retriever returns the top-k (default 20) most similar OntologyElement instances, anchoring generation in the reference ontologies' terminology and modelling patterns and promoting reuse of existing elements.

## 3.2. Ontology Extender
Assembles the final LLM prompt: retrieved elements are grouped by source ontology and rendered as Turtle snippets injected as read-only context, plus a unified prefix block merging namespace declarations of all input ontologies so every retrieved IRI resolves correctly and can be reused without namespace conflicts. Engineers can configure different prompt templates selectable at run-time. Before acceptance each fragment passes a two-stage validator: a Turtle parser for syntactic correctness and a constraint checker for the selected use case's modelling conventions — in the two evaluation profiles this includes explicit 'rdfs:domain' and 'rdfs:range' declarations, described as a configurable governance constraint, not a universal criterion; failing fragments are retried or flagged. The Extender calls the LLM service and extracts the returned Turtle code block as a candidate TBox fragment. Prompt templates are decoupled from the retrieval/generation/integration pipeline. Two templates were used (see Section 4): a SHACL-based template for the industrial ontology (SHACL NodeShape and PropertyShape definitions with specific naming conventions including sh:name labels for downstream compliance workflows; modelling guidance largely stops after requiring domain and range) versus a generic-restrictions plus reuse-of-classes template for the EU ontology (every newly introduced class and property annotated with both rdfs:label and rdfs:comment). Both impose strong reuse constraints (reuse existing elements without redeclaring them); externalised prompt configurations allow switching companies/use cases without changing system components.

## 3.3. Ontology Integrator
Incorporates the generated fragment into the input ontologies by deduplication (removing repeated axioms, named classes, properties, and prefixes) followed by concatenation of the cleaned fragment with the input ontologies. It additionally forwards each generated fragment to the Ontology Retriever for indexing, reducing the chance the Extender recreates similar elements for subsequent CQs and promoting cross-fragment consistency; this re-indexing was disabled in the evaluation so each CQ fragment could be assessed independently.

**Covers:** Related-work comparison-table tail ([26] through OntoExtend row) and synthesis paragraph, plus §3–§3.3 (Retriever, Extender, Integrator) up to the §4 Experimental setup heading
