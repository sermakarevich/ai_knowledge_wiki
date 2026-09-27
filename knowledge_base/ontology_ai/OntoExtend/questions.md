---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs

### Q1. What problem does OntoExtend solve, and what are its three pipeline stages?

> [!tip]- Answer
> > OntoExtend tackles requirement-driven ontology extension: enriching an existing ontology to satisfy new competency questions without overwhelming the LLM with hundreds of irrelevant classes. Its pipeline is (1) Ontology Retriever, which extracts CQ-relevant elements, (2) Ontology Extender, which prompts an LLM with the CQ plus retrieved fragments to generate missing axioms, and (3) Ontology Integrator, which merges fragments into extended ontologies. See [[wiki/01-framework-overview|Framework Overview]].

### Q2. What is a "fragment" in OntoExtend, and what are the paper's four research questions and contributions?

> [!tip]- Answer
> > A fragment is a self-contained set of RDF/Turtle axioms for one extension step tied to a single CQ. The four research questions ask for the best retrieval embedding setup, the most effective LLMs, the right evaluation criteria, and the strengths/weaknesses of the extensions. Stated contributions are the framework itself, retrieval/prompting experiments on two real-world case studies, and an evaluation methodology spanning structural validity, functional adequacy, and a user study. See [[wiki/01-framework-overview|Framework Overview]].

### Q3. How does OntoExtend differ from prior LLM-based ontology extension work?

> [!tip]- Answer
> > Prior work is mostly semi-automatic, taxonomy-biased enrichment with little formal evaluation and no retrieval of baseline ontology elements, while OntoExtend grounds generation in retrieved input-ontology elements via RAG. Its comparison table scores OntoExtend Y on all ten criteria versus seven for the closest prior row. The synthesis also flags reproducibility limits, interactive-tool dependence, weak complex-axiom support, and continued need for human judgment in prior methods. See [[wiki/02-related-work-comparison|Related-Work Comparison]].

### Q4. How do the Retriever, Extender, and Integrator work technically?

> [!tip]- Answer
> > The Retriever embeds OntologyElement records (IRI, labels/comments, domain/range, super/sub-relations, Turtle snippet) as pipe-delimited strings in a FAISS inner-product index and returns top-k (default 20) elements per CQ. The Extender injects retrieved Turtle as read-only context with merged prefixes, enforces reuse-without-redeclaration, and gates output through a Turtle-parser plus domain/range validator, using a SHACL template for industry and an OWL-restriction template for the EU ontology. The Integrator only deduplicates and concatenates fragments, and its re-indexing of generated fragments was disabled during evaluation for independent per-CQ assessment. See [[wiki/02-related-work-comparison|Related-Work Comparison]].

### Q5. How were the 39 evaluation CQs and datasets constructed?

> [!tip]- Answer
> > CQs were built by removing random classes plus properties referencing them (expanding through subclasses), then writing one CQ per removed class/properties asking what it was meant to represent. The dataset spans four Onto-DESIDE circular-economy modules (20 CQs) and an internal Bosch manufacturing ontology (19 CQs). Converted to Turtle, sizes range from EU part 1 at 75,000 tokens / 2920 axioms / 405 classes+properties down to part 4 at 6,000 tokens / 228 axioms / 54 classes+properties. See [[wiki/03-experimental-setup|Experimental Setup]].

### Q6. Which retrieval configuration won tuning, and which LLMs and prompts were used?

> [!tip]- Answer
> > Tuning over 3 embedding models × separator × comments on 5 held-out CQs (judged by two cross-checking engineers with P@3/P@20) selected text-embedding-ada-002 with pipe separators plus comments (Mw 0.63). Generation used o1-preview (best in prior work) and GPT-5, with a prompt refined on a disjoint dev set combining a general template, retrieved elements, a CQ placeholder, and a formalism directive. By design the EU setting requests OWL restrictions while industry disallows them in favour of SHACL shapes, so the two are not comparable on OWL expressivity. See [[wiki/03-experimental-setup|Experimental Setup]].

### Q7. What evaluation criteria and Correctness/Completeness scales does the paper use?

> [!tip]- Answer
> > Evaluation is threefold: structural (RDFLib syntax check, OOPS! before/after comparison, Pellet consistency), functional (CQ verification via writable SPARQL plus a refined superfluous-element count excluding query-mentioned or hierarchically linked elements), and a six-engineer Likert survey. Correctness (1–5) rates the fragment in isolation from generation failure to full CQ alignment, while Completeness (1–5) rates fragment plus input ontology from needing full rework to complete and correct. See [[wiki/03-experimental-setup|Experimental Setup]].

### Q8. What were the structural and functional results, with key numbers?

> [!tip]- Answer
> > Structurally there were almost no Turtle syntax errors and no new critical/important OOPS! pitfalls — only minor P02/P04 issues in the EU setting and P08 missing annotations (~3.7 per extension) in industry. Functionally, CQ verification hit 100% for both LLMs in both settings with under 2% superfluous elements, versus ~30% reported in prior work. Syntax errors were 0% EU-project and 2.5% industry, with superfluous elements at 2% EU and 0% industry. See [[wiki/04-evaluation-methodology|Evaluation Methodology]].

### Q9. What did the six-engineer survey find, and how did industry vs EU-project judgments differ?

> [!tip]- Answer
> > Industry fragments scored ~4.9 correctness and ~4.5 completeness with high agreement, needing only minor or no edits (occasional SHACL-only additions, missing datatypes or comments). EU-project fragments scored ~3.7 correctness and ~3.0 completeness, needing moderate revision for unconnected elements, over-specific names, GPT-5's missing domain/range and wrong restrictions, and o1-preview's redefined classes and wrong domains. Means and Fleiss weighted observed agreement Po were computed from briefed engineers using tools like Protégé. See [[wiki/04-evaluation-methodology|Evaluation Methodology]].

### Q10. Why did scores differ between settings, and what are the limitations and future work?

> [!tip]- Answer
> > Open-ended EU-project CQs left many modelling decisions to the tool, while tightly scoped industry CQs only required rendering valid axioms, so the gap reflects CQ under-specification rather than framework weakness. The authors propose LLM behaviour as a proxy for requirement quality and note compact retrieval cuts cost/latency versus ~75k-token prompts. Limits are two domains, few LLM configurations, and data-leakage risk, with future work on broader domains, systematic model comparison, leakage safeguards, and CQ-quality improvement. See [[wiki/05-discussion-results|Discussion and Conclusion]].

### Q11. What does the bibliography ([1]–[29]) reveal about the paper's foundations?

> [!tip]- Answer
> > The reference list spans 2012–2025 across ESWC, ISWC, ECAI, CIKM, and arXiv, covering generation works like Neon-GPT, Ontogenia, and Phrase2Onto alongside evaluation infrastructure. Method anchors include the OOPS! pitfall scanner, CQ-verification ontology testing, the FAISS library, and Fleiss-kappa rater agreement. It is a pure bibliography with no prose or findings beyond citation details. See [[wiki/06-references|References]].

### Q12. Should your team adopt OntoExtend as a drafting assistant for ontology extension, and under what conditions?

> [!tip]- Answer
> > Yes, but only where CQs are precise and the background ontology is coherent, since industry-style scoped requirements needed minor edits while open-ended EU CQs needed moderate revision. Treat it as a drafting assistant with mandatory engineer validation, compact retrieval to control cost, and structural plus CQ-verification checks before integration. Decline fully automatic deployment given sensitivity to CQ quality, missing domain/range and naming weaknesses, and the two-domain, few-model evidence base. See [[wiki/05-discussion-results|Discussion and Conclusion]].
