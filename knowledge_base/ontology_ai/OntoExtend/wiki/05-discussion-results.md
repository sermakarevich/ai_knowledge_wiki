> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Discussion, limitations and conclusion
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
---
## CQ style and why scores differ
**Covers:** open vs. tightly scoped CQs; EU-project vs. industry evaluation outcome

The chunk states EU-project CQs "were defined in a more open manner. I.e., the authors, mostly domain experts, left many of the modelling decisions to the tool," so "the tool in this case has to make the open modelling decisions when generating the ontology fragments." For these CQs, "the LLMs often produced reasonably structured extensions, but ontology engineers judged some outputs as less complete because additional manual refinement was needed to align the results with modelling choices implied by the full specification." The authors conclude: "lower correctness and completeness scores in this setting reflect rather the limitations of the CQ definition (i.e., missing clarity on the expectations and contextual detail), not necessarily a weakness of the OntoExtend framework." In the industry setting, "the tool mainly needed to render valid axioms according to an input ontology and hence achieved much higher scores for completeness and correctness."

## LLM behaviour as an implicit quality measure
**Covers:** same framework on two qualitatively different CQ sets; tool-centric quality dimension

The chunk contrasts "one in which CQs are tightly scoped, and another in which CQs lack clear expectations and context, leaving many modelling decisions open." Finding: "OntoExtend tends to perform better in terms of correctness and completeness, alignment with expert expectations, and reduced need for post-editing when the CQs and background ontologies are well structured, precise, and internally coherent." Interpretation: "if a given set of CQs and input ontologies systematically yields higher quality extensions with fewer modelling errors, then this combination is in a pragmatic sense 'better' for downstream ontology engineering with LLMs (and probably also humans). Conversely, when the same solution struggles, this most likely is a result of ambiguity, under-specification, or hidden modelling assumptions in the input." Verbatim: results "support the interpretation of LLM behaviour as a novel, tool-centric dimension of ontology and requirement quality."

## Practical impact: compact retrieval vs. large fragments
**Covers:** latency and API-cost scaling

"Sending very large ontology fragments (e.g., ∼75k-token) directly to an LLM resulted in substantially longer end-to-end response times and higher API costs in our experiments. By contrast, OntoExtend retrieves a compact subset of the ontology and provides only that subset to the LLM; this greatly reduces the typical LLM turnaround and lowers the amount of data transmitted and the associated cost."

## Limitations and future work
**Covers:** scope, model coverage, data leakage, CQ quality

- Restricted to two domain-specific use cases; broader domains and modelling scenarios needed for general conclusions.
- Only a small number of LLM configurations tested; systematic comparison across models/providers could reveal performance differences.
- Data leakage threat: LLMs may have seen similar ontologies/CQs in pre-training; EU-project ontologies are public (but CQ coverage material is not), while the industry ontology "was not disseminated in public code or data repositories, which reduces the risk."
- Planned safeguards: "on-the-fly benchmark generation, experiments with open-weight models trained on controlled corpora, and dedicated checks for overlap between evaluation data and known pre-training sources."
- CQ formulation strongly affects outcomes; future work should analyse/improve CQ quality, e.g. "(semi-)automatically generating CQs, or mapping them to existing CQ templates (see the work by Keet et al. [11])."

## Conclusion: framework and RQ findings
**Covers:** Section 8 conclusion — method, RQ1–RQ4, strengths and weaknesses

OntoExtend is "a scalable requirement-driven framework that extends one or more input ontologies according to the requirements specified in a set of CQs," processing "each CQ individually and extracts, for each CQ, the relevant existing ontology elements as context for an LLM to generate the missing ontological structures necessary to fully answer the CQ in a coherent manner." Reported findings: "using text-embedding-ada-002 as an embedder produced the most effective retrieval subsets (RQ1)"; "both GPT-5 and o1-preview yielded comparable performance (RQ2): the generated fragments contained almost no Turtle syntax errors, did not introduce any new critical or important OOPS! pitfalls, only a negligible amount of minor pitfalls, and exhibited only a small fraction of superfluous elements." Evaluation (RQ3) combined "syntactic checks, OOPS! analysis, CQ verification, measurement of unnecessary classes/properties (superfluous), and an analysis of the generated outputs by six ontology engineers." Outcome (RQ4): "structurally and syntactically correct, accurately model all evaluated CQs, and add fewer than 2% superfluous elements, with engineers often needing only minor edits in the industry use case." Weaknesses: "occasional missing domain/range declarations, suboptimal or overly specific names, and some unconnected elements" plus degraded performance on "open-ended or underspecified" CQs.
