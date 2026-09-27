> [[../../index|Research]] | [[../../overview|Overview]] | [[../../digest|Digest]]

# ontology foundations in AI

**In one sentence:** A systematic review of 30 papers (41 studies) finds LLMs can assist across the full ontology-engineering lifecycle but the evidence is fragmented by non-standard tasks, datasets, metrics, and workflows, pointing to shared benchmarks and hybrid LLM-human workflows as the way forward.

## Key points
- Ontology engineering spans four lifecycle stages — requirements specification, implementation, publication, and maintenance — and LLMs have been tried at every stage, not just axiom generation ([[../../../../LargeLanguageModelsForOntologyEngineering/summary|SLR]])
- LLMs play three distinct roles in the literature: ontology engineer drafting structures, domain expert supplying or interpreting meaning, and evaluator judging outputs ([[../../../../LargeLanguageModelsForOntologyEngineering/summary|SLR]])
- The dominant model families studied are GPT, LLaMA, and T5, operating over heterogeneous inputs (OWL ontologies, free text, competency questions) to produce task-specific outputs (examples, axioms, documentation) ([[../../../../LargeLanguageModelsForOntologyEngineering/summary|SLR]])
- The central finding is a lack of homogenization: task definitions, datasets, metrics, and experimental workflows differ study to study, making comparison across the 41 extracted studies difficult ([[../../../../LargeLanguageModelsForOntologyEngineering/summary|SLR]])
- Reproducibility is weak because several studies omit complete evaluation protocols or release no code, despite open screening data via the oeg-upm/llm4oe-slr GitHub and Zenodo deposits ([[../../../../LargeLanguageModelsForOntologyEngineering/summary|SLR]])
- Human involvement is thin — only a small subset of studies (four per the second review) include human participants — so claims about practical usability rest on limited evidence ([[../../../../LargeLanguageModelsForOntologyEngineering/summary|SLR]])
- The prescribed direction is standardized benchmarks plus hybrid LLM-human workflows that preserve logical consistency and domain fidelity while gaining automation speed ([[../../../../LargeLanguageModelsForOntologyEngineering/summary|SLR]])

---
## What the sources agree on
With a single source, there is no cross-source agreement to report; the review's abstract and both solicited peer reviews converge internally that the coverage is comprehensive and valuable and that fragmentation of tasks, datasets, metrics, and workflows is the key problem.

## Where they differ
With a single source, there is no cross-source disagreement; the only internal tension is between the two reviewers' emphases — Review #1 stresses structural tightening (redundancy, section-title mismatch, figure layout) while Review #2 stresses evidence-scope risks (search-term under-coverage of BERT/T5-era work, novelty over Garijo et al. 2024, thin human-role and domain analysis, missing taxonomy diagram).

## Evidence quality
Systematic literature review: 11,985 initial results (2018–2024) screened to 30 papers / 41 extracted studies, with published screening data — strong breadth, but weakened by heterogeneous primary-study methods, incomplete evaluation protocols and unreleased code in primaries, possible search-term coverage gaps for pre-LLM-era models, and thin human-participant evidence. Article status at snapshot: Major Revision (Semantic Web Journal, Tracking #3864-5078).

## Sources in this sub-topic
| source | kind | what it contributes |
|---|---|---|
| [[../../../../LargeLanguageModelsForOntologyEngineering/summary|LargeLanguageModelsForOntologyEngineering]] | fresh systematic review | Lifecycle-wide mapping of LLM roles, inputs/outputs, evaluation gaps, and the benchmark-plus-hybrid-workflow agenda |
