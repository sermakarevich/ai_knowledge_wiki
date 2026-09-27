[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation methodology and results: structural, functional, and engineer survey
**In one sentence:** OntoExtend's extensions are validated by RDFLib syntax checks, before/after OOPS! pitfall comparison plus Pellet consistency checks, two-engineer CQ verification and superfluous-element counts, and a six-engineer survey, with results showing almost no syntax errors, only minor new OOPS! pitfalls, 100% CQ correctness with <2% superfluous elements, and high engineer ratings for the industry ontology but moderate-revision judgments for the EU-project fragments.
## Key points
- Each generated module is checked for correct Turtle syntax with the RDFLib Python library, OOPS! pitfalls are compared before vs after integration to document newly introduced issues, and the Pellet reasoner checks consistency after integration.
- Functional CQ verification is done per extension after adding it to the input ontology, with two ontology engineers independently verifying and cross-checking annotations and resolving disagreements by discussion.
- Superfluous elements are counted by the same engineer pair comparing counts before and after adding the extension, reporting elements generated but deemed unnecessary by the OntoExtend framework.
- Six engineers (industry and academia) evaluated fragments after a briefing, answering correctness and completeness survey questions per extension with free-text comments and a debriefing, using any visualisation tools (e.g. Protégé, TopBraid EDG, VSCode); means and Fleiss weighted observed agreement Po were computed.
- Structural results: almost no Turtle syntax issues, no new critical or important OOPS! pitfalls, only minor issues — EU-project: P02 (synonyms as classes, one instance per extension in a single project) and P04 (unconnected elements, at most one added instance in two of four use cases); industry: P08 missing annotations averaging ~3.7 per CQ-based extension for both LLMs, attributed to replicating the input's annotation-free style.
- Functional results (Table 4): CQ verification 100% (100% o1-preview, 100% GPT-5) on both EU-Project and Industry; syntax errors 0% EU-Project and 2.5% Industry (5% o1-preview, 0% GPT-5); superfluous elements 2% EU-Project (3.8% o1-preview, 0% GPT-5) and 0% Industry, versus ~30% (35% under original definition) reported in prior work [16].
- Survey results (Table 5, 1–5 scale): Industry means ~4.91–4.96 correctness and ~4.54–4.56 completeness with Po 0.87–0.98, versus EU-Project means 3.66–3.69 correctness and 2.94–3.11 completeness with Po 0.80–0.87; EU fragments need moderate revision (unconnected elements, over-specific names, GPT-5 missing domain/range and wrong restrictions, o1-preview redefining classes and wrong domains), while industry fragments need minor or no changes (occasional SHACL-only additions, missing sh:datatype, missing rdfs:subClassOf, missing comments).
---
## Structural validation workflow
> "As shown on the right side of Fig. 3, each generated extension module is validated for correct Turtle syntax via the RDFLib Python library. To assess common modelling pitfalls, we run OOPS! on the input ontology both before and after integrating the generated extension, compare the reported pitfalls, and document any new issues introduced by the extension. In addition, we execute the Pellet reasoner to perform a consistency check on the input ontology after the generated extension has been integrated."

**Covers:** Fig. 3 right-side validation pipeline (Sections 5.1–5.2 boundary)

## Functional evaluation: CQ verification and superfluous elements
Functional adequacy (CQ verification) is performed "on each generated extension after it is added to the input ontology to ensure that each CQ is correctly modelled (see Figure 3)"; "[t]wo ontology engineers independently verify the CQ modelling decisions and then cross-check each other's annotations; any disagreement is resolved through discussion."

After CQ verification, "the same pair of engineers inspects the integrated file to identify and count superfluous elements introduced by the generated extension by comparing the number of superfluous elements before and after adding the extension."

**Covers:** Section 5.2 Functional Evaluation

## Engineer survey design
Six ontology engineers from industry and academia evaluated generated modules after "a short briefing that explained the task and the survey form"; each received "a set of CQs, the input ontologies, and the generated ontology fragments for each CQ", answered "the two survey questions regarding correctness and completeness", added free-text comments, joined a debriefing, and could use any visualisation tools (e.g., Protégé, TopBraid EDG, VSCode). Means and "Fleiss weighted observed agreement Po [20]" were computed.

**Covers:** Section 5.3 Evaluation by Ontology Engineers

## Structural results and Tables 4–5
Generated fragments "almost did not exhibit any syntax issues in Turtle"; OOPS! showed "no new critical or important modelling pitfalls", only minor ones; versus prior generation work [6,13,16] with "a considerable number of important and critical OOPS! pitfalls", OntoExtend "exhibits only a few minor pitfalls".

| Use case | OOPS! P2,P4&P8 (o1-prev,GPT-5) | CQ-verification (o1-prev,GPT-5) | Syntax errors (o1-prev,GPT-5) | Superfluous elements (o1,GPT-5) |
|---|---|---|---|---|
| EU-Project | 13 (7,6) | 100% (100%, 100%) | 0% (0%,0%) | 2% (3.8%,0%) |
| Industry | 141 (70,71) | 100% (100%,100%) | 2.5% (5%,0%) | 0% (0%,0%) |

Table 4 caption in chunk: "Summary of structural (syntax and OOPS!) and functional (CQ-verification and percentage of superfluous elements) evaluation for the EU-Project and the Industry ontologies, all LLMs combined and separated."

| Model | Metric | Industry Mean | Industry Fleiss Po | EU-Project Mean | EU-Project Fleiss Po |
|---|---|---|---|---|---|
| o1-preview | Correctness | 4.91 | 0.97 | 3.69 | 0.80 |
| o1-preview | Completeness | 4.56 | 0.89 | 3.11 | 0.85 |
| GPT-5 | Correctness | 4.96 | 0.98 | 3.66 | 0.87 |
| GPT-5 | Completeness | 4.54 | 0.87 | 2.94 | 0.87 |

Table 5 caption in chunk: "Survey results on evaluating ontology extension fragments for the EU-Project and industry ontologies. The ratings are between 1 and 5 (see section 4.1)".

**Covers:** Section 6.1 Results of Structural Evaluation (Tables 4–5)

## Functional and survey results
CQ verification: "all CQs in both use cases are correctly modelled, with no minor issues of the type identified by Saeedizade and Blomqvist [25]"; both GPT-5 and o1-preview yield "only negligible amounts of superfluous elements" — "fewer than 2% unnecessary elements, whereas [16] reported around 30% superfluous elements (35% with [16]'s original definition)".

EU-project survey (three engineers): systematic unconnected elements needing subClassOf links, suboptimal over-specific class names; GPT-5 omitted domain/range, wrong allValuesFrom/complementOf restrictions, over-simplified names; o1-preview redefined existing classes, syntactically incorrect axioms "not shown by the tools used for the Structural evaluation", wrong domains, over-specific object properties; verdict: "require moderate revision before they can be safely integrated".

Industry survey (three engineers): main errors were SHACL property shapes without matching object property plus rdfs:domain/range, missing sh:datatype, omitted rdfs:subClassOf axioms, missing comment annotations (both models); o1-preview-only: many unneeded Property shapes/object properties; two comments flagged ungrounded anticipatory extensions; overall "high degree of user satisfaction (minor or no changes needed)" with strong agreement.

**Covers:** Sections 6.2–6.3 Results of Functional and Engineers' Evaluation

## Discussion: overall results and CQ formulation
"OntoExtend can reliably produce high-quality ontology extensions across both domains": "almost always syntactically valid", "only a small number of minor OOPS! pitfalls", "correctly model all evaluated CQs", "fewer than 2% superfluous components", engineers judged "syntactically and semantically adequate and requiring at most minor to moderate edits" — functioning as "a drafting assistant" shifting effort "from manual axiom authoring to quick validation and targeted refinement", lowering "the barrier to entry for domain experts".

Two usage scenarios: "(i) extending an ontology from highly specific, pre-determined CQs" versus "(ii) constructing or extending ontologies from more general, open CQs"; industry CQs were "deliberately very focused and targeted... authored jointly by domain experts and ontology engineers", while EU-project CQs "differ qualitatively".

**Covers:** Section 7 Discussion (opening, truncated in chunk)
