# April 2026 OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs

> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

**In one sentence:** OntoExtend is a retrieval-augmented, requirement-driven framework that retrieves ontology fragments relevant to a new competency question and prompts an LLM to generate grounded extension fragments for integration, evaluated on 39 CQs from Onto-DESIDE and Bosch with few structural issues and full functional test success.

## Key points
- Ontology extension is defined as systematic enrichment of an existing ontology to satisfy new functional requirements, and is described as resource-intensive and error-prone.
- OntoExtend takes new CQs plus the existing ontology as input and, per CQ, retrieves relevant named classes/properties with their axioms to avoid exceeding LLM context windows or misguiding the model with irrelevant details.
- The pipeline has three steps: (1) Ontology Retriever extracts relevant elements, (2) Ontology Extender prompts an LLM with CQ + retrieved fragment to generate missing fragments, (3) Ontology Integrator integrates fragments into extended ontologies.
- A generated/retrieved "fragment" is a self-contained set of RDF/Turtle axioms for one extension step associated with a single CQ.
- Evaluation used 39 CQs from two use cases: the public EU-project ontology Onto-DESIDE and an industrial Bosch ontology; generated fragments showed few structural issues, satisfied all functional evaluation tests, and engineers rated them as needing minor to moderate revision before integration.
- Four research questions drive the work: best embedding configuration for compact CQ-relevant retrieval; which LLMs most effectively model the CQ; which evaluation criteria assess fragment quality; strengths/weaknesses of the extended ontologies.
- Stated contributions are: the OntoExtend framework, retrieval/prompting experiments on two domain-specific real-world case studies, and an evaluation methodology covering structural validity, functional adequacy, and a user-based study.

---

## Abstract

**Covers:** Title, authors, arXiv:2607.17963v1 [cs.AI] 20 Jul 2026, Abstract, Keywords

Authors: Anna Sofia Lippolis (Bologna/ISTC-CNR), Mohammad Javad Saeedizade (Linköping), Stefan Schmid (Bosch), Simon Blattner (Bosch), Robin Keskisärkkä, Aldo Gangemi, Eva Blomqvist, Andrea Giovanni Nuzzolese; first two authors contributed equally.

Verbatim claim:

> "This paper introduces OntoExtend, a requirements-driven framework for ontology extension with LLMs. It uses retrieval-augmented generation (RAG) over relevant input ontologies and requirements in the form of competency questions to propose grounded extensions."

Reported results (abstract):

| Item | Value as stated |
|---|---|
| CQs evaluated | 39 CQs from two use cases (Onto-DESIDE, Bosch industrial ontology) |
| Structural issues | "few structural issues" |
| Functional tests | "satisfy all functional evaluation tests" |
| Engineer rating | "requiring minor to moderate revision before integration" |

Interpretation stated: "useful as a drafting assistant for requirement-driven ontology extension in real world scenarios, while remaining sensitive to CQ specificity and modelling profile."

Keywords: Ontology extension, Ontology generation, Ontology engineering, Large Language Models.

Code/data stated as available at `https://github.com/dersuchendee/OntoExtend`.

## 1. Introduction

**Covers:** Section 1, including Figure 1 description and research questions

Prior LLM roles noted: ontology generation from requirements, and ontology evaluation (whether an ontology correctly models requirements). Gap claimed: "to the best of our knowledge, no prior study has examined how LLMs can extend an existing (input) ontology by reusing ontology elements while modelling additional requirements provided in the form of" CQs.

CQs defined as "natural language questions outlining and constraining the scope of an ontology."

Challenges stated:
- Input ontologies often contain hundreds of classes and properties, exceeding LLM input context limitations.
- Even when the ontology fits, irrelevant details may misguide LLMs into "off-target or inconsistent outputs."

Figure 1 pipeline (verbatim roles):
1. "The Ontology Retriever extracts the relevant ontology elements of the input ontologies given a new competency question."
2. "The Ontology Extender uses the retrieved ontology elements together with the competency question to prompt an LLM to generate missing ontology fragments."
3. "The Ontology Integrator integrates the fragments into the extended ontologies."

Paper organisation as stated: Section 2 related work; Section 3 OntoExtend; Section 4 experimental setup; Section 5 evaluation; Section 6 results; Section 7 metrics/impact/benchmark extensibility; Section 8 conclusions and future work.

## 2. Related Work (beginning only)

**Covers:** Section 2 opening through Table 1 header (table body not in chunk)

Early/interactive approaches named: Soares et al. extending APTO with ChatGPT-4 for OWL taxonomic axioms; Matieu and Groza Protégé plugin with fine-tuned GPT-3 translating controlled natural language to OWL Functional Syntax; Phrase2Onto prototype "limited to toy ontologies" and not applying to larger ontologies.

Automated systems named: Taxoria (taxonomy enrichment proposing child terms, validated before integration with provenance tracking; concerns over hallucinated nodes and implicit requirement capture); Wu et al. online clustering with LLM agents for evolving medical ontology; Dong et al. enriching OWL ontologies as formal KBs, baseline LLM methods "yet to achieve satisfying performance."

Broader frameworks named: Kholmska et al. multi-LLM workflow (concept search, extraction, alignment, CQ/SPARQL generation; needs manual repair); Joachimiak et al. Artificial Intelligence Ontology via Ontology Development Kit workflow; Garcia Fernandez et al. found hallucinations about standards/reusable ontologies and shallower-than-manual extensions, with human review essential.

Table 1 (header only in chunk): comparison columns are OOPS! pitfall analysis, Syntax/well-formedness, Consistency validation, requirement verification, superfluous elements, user evaluation, expert assessment, multi-domain evidence, real-world ontology, scalability; symbols Y = yes, P = partial, N = not reported.

**Covers:** Abstract through Section 2 opening up to Table 1 header; Table 1 body, Sections 3–8, and references are not in this chunk.
