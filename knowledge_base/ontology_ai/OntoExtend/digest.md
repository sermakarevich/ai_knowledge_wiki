> [[index|Wiki]] | [[summary|Summary]]

# OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs — Digest

## 1. [[wiki/01-framework-overview|April 2026 OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs]]

**In one sentence:** OntoExtend is a retrieval-augmented, requirement-driven framework that retrieves ontology fragments relevant to a new competency question and prompts an LLM to generate grounded extension fragments for integration, evaluated on 39 CQs from Onto-DESIDE and Bosch with few structural issues and full functional test success.

## Key points
- Ontology extension is defined as systematic enrichment of an existing ontology to satisfy new functional requirements, and is described as resource-intensive and error-prone.
- OntoExtend takes new CQs plus the existing ontology as input and, per CQ, retrieves relevant named classes/properties with their axioms to avoid exceeding LLM context windows or misguiding the model with irrelevant details.
- The pipeline has three steps: (1) Ontology Retriever extracts relevant elements, (2) Ontology Extender prompts an LLM with CQ + retrieved fragment to generate missing fragments, (3) Ontology Integrator integrates fragments into extended ontologies.
- A generated/retrieved "fragment" is a self-contained set of RDF/Turtle axioms for one extension step associated with a single CQ.
- Evaluation used 39 CQs from two use cases: the public EU-project ontology Onto-DESIDE and an industrial Bosch ontology; generated fragments showed few structural issues, satisfied all functional evaluation tests, and engineers rated them as needing minor to moderate revision before integration.
- Four research questions drive the work: best embedding configuration for compact CQ-relevant retrieval; which LLMs most effectively model the CQ; which evaluation criteria assess fragment quality; strengths/weaknesses of the extended ontologies.
- Stated contributions are: the OntoExtend framework, retrieval/prompting experiments on two domain-specific real-world case studies, and an evaluation methodology covering structural validity, functional adequacy, and a user-based study.

## 2. [[wiki/02-related-work-comparison|Related-Work Comparison and the OntoExtend Framework]]

**In one sentence:** Prior LLM-based ontology extension is mostly semi-automatic, taxonomy-biased enrichment with little formal evaluation and no retrieval of existing baseline elements, so OntoExtend adds a retrieval-grounded pipeline (Retriever, Extender, Integrator) that anchors LLM-generated TBox fragments in the input ontologies.

## Key points
- The comparison table scores OntoExtend as Y on all ten criteria while the closest prior row, [16] Ontology engineering assistant, scores Y on seven (Y Y N Y Y Y N Y Y N).
- The synthesis claims current work is predominantly semi-automatic enrichment of existing inputs with a bias toward taxonomic growth, constrained by reproducibility, reliance on interactive tools, limited support for complex axioms, and continued need for human judgment in requirement elicitation and validation.
- No surveyed method focuses on retrieval of existing ontology elements from baseline ontologies, whereas OntoExtend integrates retrieval directly into extension; most surveyed works use minimal to no formal evaluation.
- The Retriever builds a FAISS [5] inner-product index over OntologyElement records (IRI, labels/comments, domain/range, super-/sub-relations, verbatim Turtle snippet) embedded as pipe-delimited strings, returning top-k (default 20) elements per competency question (CQ).
- The Extender injects retrieved Turtle snippets as read-only context plus a merged namespace prefix block, enforces reuse-without-redeclaration, and gates fragments through a two-stage validator (Turtle parser plus domain/range constraint checker, configurable per use case).
- Two deployment prompt templates are used: a SHACL-based template for the industrial ontology (NodeShape/PropertyShape, naming conventions, sh:name labels) and a generic restrictions plus reuse-of-classes template for the EU ontology (mandatory rdfs:label and rdfs:comment on every new class/property).
- The Integrator only deduplicates (repeated axioms, classes, properties, prefixes) and concatenates the cleaned fragment, and its re-indexing of generated fragments for later CQs was disabled in the evaluation so each CQ fragment could be assessed independently.

## 3. [[wiki/03-experimental-setup|Experimental Setup: Datasets, Retrieval Tuning, and Evaluation Criteria]]

**In one sentence:** The evaluation uses 39 competency questions (20 from four Onto-DESIDE modules, 19 from an internal Bosch ontology) created by removing classes and referencing properties, with retrieval fixed to text-embedding-ada-002 (pipe separator, with comments, Mw 0.63) and LLMs o1-preview and GPT-5, assessed by structural, functional (CQ verification plus refined superfluous-element count), and human Correctness/Completeness ratings.

## Key points
- Dataset covers two settings jointly evaluated: four Onto-DESIDE ontology-network modules (circular-economy interoperability, 20 CQs) and an internal Bosch manufacturing ontology (19 CQs).
- CQs were created by selecting random classes C, removing each class c plus properties whose domain/range references c, iteratively adding subclasses and their referencing properties, then writing one CQ per removed class/properties asking what it was intended to represent.
- Input ontologies were converted to Turtle with compact prefixes; token counts use the GPT-4o tokeniser, with EU-project part 1 largest at 75,000 tokens / 2920 axioms / 405 classes+properties and part 4 smallest at 6,000 tokens / 228 axioms / 54 classes+properties.
- Retrieval tuning compared 3 OpenAI embedding models (text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002) × separator (| vs newline) × comments in/out on 5 held-out CQs, judged manually by two cross-checking ontology engineers with P@3 and P@20.
- Best retrieval was text-embedding-ada-002 with pipe-separated axioms plus comments (Mprod 0.23, Mw 0.63 where Mw = 0.7·P3 + 0.3·P20), selected for the main experiment; both Mw and Mprod = P3·P20 agreed per model.
- Extender LLMs are o1-preview (best in prior work [16]) and GPT-5 (latest OpenAI model); no other families were tested, and the prompt (general template + retriever elements + CQ placeholder + formalism directive) was iteratively refined on a disjoint dev set to remove typical axiom errors.
- Expressivity differs by setting by design: EU-project requests OWL restrictions in generated fragments, industry disallows OWL restrictions and requires only SHACL shapes, so the two settings are not comparable on OWL expressivity.
- Evaluation is multidimensional: OOPS! + Pellet + RDFLib syntax check (structural), CQ verification via writable SPARQL plus superfluous-element count where only named classes/properties absent from the query AND unconnected by subClassOf/subPropertyOf count (functional), and six-engineer Likert survey on Correctness (fragment alone) and Completeness (fragment + input ontology, effort to make usable).

## 4. [[wiki/04-evaluation-methodology|Evaluation methodology and results: structural, functional, and engineer survey]]

**In one sentence:** OntoExtend's extensions are validated by RDFLib syntax checks, before/after OOPS! pitfall comparison plus Pellet consistency checks, two-engineer CQ verification and superfluous-element counts, and a six-engineer survey, with results showing almost no syntax errors, only minor new OOPS! pitfalls, 100% CQ correctness with <2% superfluous elements, and high engineer ratings for the industry ontology but moderate-revision judgments for the EU-project fragments.

## Key points
- Each generated module is checked for correct Turtle syntax with the RDFLib Python library, OOPS! pitfalls are compared before vs after integration to document newly introduced issues, and the Pellet reasoner checks consistency after integration.
- Functional CQ verification is done per extension after adding it to the input ontology, with two ontology engineers independently verifying and cross-checking annotations and resolving disagreements by discussion.
- Superfluous elements are counted by the same engineer pair comparing counts before and after adding the extension, reporting elements generated but deemed unnecessary by the OntoExtend framework.
- Six engineers (industry and academia) evaluated fragments after a briefing, answering correctness and completeness survey questions per extension with free-text comments and a debriefing, using any visualisation tools (e.g. Protégé, TopBraid EDG, VSCode); means and Fleiss weighted observed agreement Po were computed.
- Structural results: almost no Turtle syntax issues, no new critical or important OOPS! pitfalls, only minor issues — EU-project: P02 (synonyms as classes, one instance per extension in a single project) and P04 (unconnected elements, at most one added instance in two of four use cases); industry: P08 missing annotations averaging ~3.7 per CQ-based extension for both LLMs, attributed to replicating the input's annotation-free style.
- Functional results (Table 4): CQ verification 100% (100% o1-preview, 100% GPT-5) on both EU-Project and Industry; syntax errors 0% EU-Project and 2.5% Industry (5% o1-preview, 0% GPT-5); superfluous elements 2% EU-Project (3.8% o1-preview, 0% GPT-5) and 0% Industry, versus ~30% (35% under original definition) reported in prior work [16].
- Survey results (Table 5, 1–5 scale): Industry means ~4.91–4.96 correctness and ~4.54–4.56 completeness with Po 0.87–0.98, versus EU-Project means 3.66–3.69 correctness and 2.94–3.11 completeness with Po 0.80–0.87; EU fragments need moderate revision (unconnected elements, over-specific names, GPT-5 missing domain/range and wrong restrictions, o1-preview redefining classes and wrong domains), while industry fragments need minor or no changes (occasional SHACL-only additions, missing sh:datatype, missing rdfs:subClassOf, missing comments).

## 5. [[wiki/05-discussion-results|Discussion, limitations and conclusion]]

**In one sentence:** Open-ended CQs lower correctness/completeness scores because modelling decisions are left to the tool, so OntoExtend performs best on precise CQs, LLM behaviour doubles as a proxy for requirement quality, compact retrieval cuts cost/latency versus ~75k-token prompts, and the evaluated fragments are syntactically correct with fewer than 2% superfluous elements but sensitive to CQ quality.

## Key points
- EU-project CQs were defined in a more open manner with many modelling decisions left to the tool, while industry CQs were tightly scoped to rendering valid axioms from an input ontology.
- Lower correctness and completeness scores in the EU-project setting reflect CQ under-specification and task complexity, not necessarily a weakness of the OntoExtend framework.
- OntoExtend performs better on correctness, completeness, expert-expectation alignment, and reduced post-editing when CQs and background ontologies are well structured, precise, and internally coherent.
- LLM performance is proposed as a proxy indicator of requirements/ontology quality: high-quality extensions with few modelling errors signal "better" inputs, while struggles signal ambiguity or hidden assumptions.
- Sending ~75k-token ontology fragments directly to an LLM caused substantially longer end-to-end response times and higher API costs; OntoExtend retrieves only a compact subset as LLM context.
- Using text-embedding-ada-002 produced the most effective retrieval subsets (RQ1); GPT-5 and o1-preview performed comparably with almost no Turtle syntax errors and no new critical/important OOPS! pitfalls (RQ2).
- Six ontology engineers judged the extensions correct and complete with fewer than 2% superfluous elements, though weaknesses remain: missing domain/range declarations, suboptimal names, unconnected elements (RQ3/RQ4).
- Evaluation is limited to two domain-specific use cases with few LLM configurations, plus a data-leakage threat; future work targets broader domains, systematic model comparison, leakage safeguards, and CQ-quality improvement.

## 6. [[wiki/06-references|References [1]–[29]: Bibliography Starting with Aggarwal/Salatino]]

**In one sentence:** This chunk contains only the paper's bibliography, listing references [1] through [29] on LLM-assisted ontology generation, enrichment, and evaluation, beginning with Aggarwal, Salatino, Osborne, and Motta (2025).

## Key points
- The chunk lists 29 numbered bibliography entries, [1] through [29], with no prose, figures, or findings beyond citation details.
- Entry [1] is Aggarwal, T., Salatino, A., Osborne, F., Motta, E.: Leveraging large language models for generating research topic ontologies: A multi-disciplinary study, arXiv preprint arXiv:2508.20693 (2025).
- Entries span 2012–2025 venues including ESWC, ISWC, ECAI, ACM CIKM, SYNASC, Applied Sciences, Applied Ontology, IEEE Access, Frontiers in Big Data, and arXiv preprints.
- Ontology-generation and enrichment works cited include Neon-GPT [6], Ontogenia [13], Phrase2Onto [22], and LLM-driven clustering agents [29].
- Evaluation and methodology works cited include ontology testing [2], OOPS! pitfall scanner [23], CQ verification via SPARQL, LLM-generated-ontology benchmarks [21], and rater-agreement generalisation of Fleiss' kappa [20].
- Infrastructure cited includes the FAISS library [5], the Pellet-adjacent tooling context, and competency-question authoring with Claro [11].
- The chunk tail carries only the footer line "July 2026" after entry [21], with entries [22]–[29] following it in the extracted text.

## The argument in five moves

1. Ontology extension — enriching an existing ontology to satisfy new functional requirements — is resource-intensive and error-prone, and no prior LLM work grounds generation in retrieved elements of the input ontology while modelling new CQs.
2. OntoExtend fills that gap with a three-stage retrieval-grounded pipeline (Retriever over a FAISS index of OntologyElement records, Extender prompting an LLM with CQ plus read-only retrieved Turtle under reuse constraints and a two-stage validator, Integrator deduplicating and concatenating fragments).
3. The framework is tested on 39 CQs from two real settings (20 from Onto-DESIDE modules, 19 from a Bosch manufacturing ontology, built by removing classes/properties and asking CQs about them), with retrieval tuned to text-embedding-ada-002 (pipe separator, with comments) and generation by o1-preview and GPT-5 under a structural + functional + engineer-survey evaluation.
4. Results show near-perfect structural/functional behaviour — almost no syntax errors, no new critical/important OOPS! pitfalls, 100% CQ verification, under 2% superfluous elements — but a split in human judgment: industry fragments need minor or no edits while EU-project fragments need moderate revision.
5. The split is attributed to CQ formulation rather than the framework: open-ended EU-project CQs leave modelling decisions to the tool while tightly scoped industry CQs render valid axioms, so OntoExtend works best as a drafting assistant on precise, well-structured CQs — with LLM behaviour doubling as a proxy for requirement quality — within the limits of two domains, few model configurations, and a data-leakage threat left to future work.
