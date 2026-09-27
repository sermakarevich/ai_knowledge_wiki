> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Large Language Models for Ontology Engineering: A Systematic Literature Review | www.semantic-web-journal.net — In Plain Language

## What is this about?

This is a survey article, not a new tool or experiment.

The authors — Jiayi Li, Maria Poveda, and Daniel Garijo — read and compared
30 published papers about using Large Language Models (LLMs) to help build
ontologies, which are formal maps of concepts and relationships in a subject area.

It was submitted to the Semantic Web Journal in April 2025 as a Survey Article
(Tracking #3864-5078, editor Guilin Qi) and currently stands at Major Revision,
meaning reviewers asked for substantial improvements before acceptance.

The review started from 11,985 search results covering 2018–2024 and narrowed
them down to 30 core papers, from which the authors extracted 41 distinct studies.

In short: it asks "what has everyone tried so far when pointing LLMs at
ontology work, and what patterns emerge?"

## Why does it matter?

Building an ontology is slow, skilled work.

Normally you need domain experts who know the subject deeply, plus ontology
engineers who know how to express that knowledge precisely and keep it
logically consistent.

Mistakes or vague definitions ripple through every system that reuses the ontology.

LLMs look tempting here because they can read large amounts of text, suggest
terms and definitions, draft documentation, and even propose formal statements.

But the field is moving fast and chaotically: everybody defines the task
differently, tests on different data, and reports different scores.

Without a review like this, it is hard to tell what actually works, what is
just a demo, and what is missing.

The reviewers agreed on this point: both called the coverage comprehensive
and valuable for the community.

## How does it work?

The paper itself does not propose a new method. It organises existing work.

Think of it as sorting 41 experiments into a shared grid:

1. **Stages of the lifecycle.** The review follows four phases of ontology work:
   requirements specification (deciding what the ontology should cover),
   implementation (writing the actual concepts and relationships),
   publication (making it available and documented), and maintenance (fixing
   and updating it over time).

2. **Three jobs for the LLM.** Across the studies, the model plays one of three
   roles: ontology engineer (drafting or editing the ontology itself),
   domain expert (supplying subject knowledge such as definitions or examples),
   or evaluator (checking or scoring someone else's output).

3. **Familiar models, varied inputs and outputs.** The studies mostly use GPT,
   LLaMA, and T5 family models. Inputs are heterogeneous: existing OWL
   ontologies, plain text, competency questions (test questions the ontology
   should answer), and similar artefacts. Outputs are task-specific: examples,
   axioms (formal statements), documentation, and more.

4. **Four research questions.** The authors map four objectives to four research
   questions covering development activities, input-output characteristics,
   evaluation methods, and application domains.

5. **Open science.** Data files are shared via GitHub and Zenodo, though one
   reviewer notes the repository lacks a clarifying README.

The reviewers also describe what needs fixing: de-duplicate overlapping sections,
align section titles with their contents, flatten an awkward figure layout,
and above all add a unifying taxonomy diagram so readers can see the whole
landscape at a glance.

## Where can this be used?

Anywhere a team maintains a shared vocabulary or knowledge graph:

- **Requirements gathering.** Turning interviews, documents, or competency
  questions into a first draft of what the ontology should contain.
- **Drafting and enrichment.** Suggesting new classes, relationships, definitions,
  or examples during implementation.
- **Documentation and publishing.** Generating human-readable descriptions of
  ontology elements so others can reuse them.
- **Quality checking.** Using an LLM as a second pair of eyes to spot missing
  coverage, inconsistent statements, or weak definitions.
- **Maintenance.** Help with updating an ontology when the domain changes.

A caveat from the review: only four of the extracted studies involved human
participants in a serious way, so claims about "human in the loop" workflows
are still thin. One reviewer explicitly asked for deeper analysis of domains
and of the human role.

Another caveat is coverage: the search terms ("Language Model" / "LM" / "LLM*")
may have missed some 2018–2021 BERT- and T5-era work, and the novelty over an
earlier 2024 review by Garijo and colleagues needs clearer justification.

## Conclusions & takeaways

- LLMs are already being tried at every stage of ontology engineering, most
  often as drafters, knowledge sources, or checkers.
- The headline finding is fragmentation: no shared task definitions, no shared
  datasets, no shared metrics, no shared workflows.
- Reproducibility is weak because some papers omit full evaluation protocols
  or code, so results are hard to verify or compare.
- The authors' prescription: build standardized benchmarks and design hybrid
  workflows where LLM automation is paired with human expertise.
- Peer review broadly endorses the direction but demands a tighter structure,
  less repetition, deeper domain and human-role analysis, and a clear taxonomy
  figure before the survey is ready.
- Practical takeaway: treat current LLM assistance as a useful but uneven
  drafting aid — keep an expert in charge and insist on transparent evaluation.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Ontology | A formal map of the important concepts in a subject and how they relate. |
| Ontology engineering (OE) | The disciplined process of designing, writing, publishing, and maintaining such a map. |
| Large Language Model (LLM) | An AI model trained on vast text that can read, summarise, and generate language. |
| Competency question | A test question an ontology should be able to answer, used to check coverage. |
| Axiom | A formal statement in the ontology, e.g. "every student is a person". |
| OWL | Web Ontology Language: the standard format for writing machine-readable ontologies. |
| Systematic literature review | A study that collects papers by explicit search rules and compares them fairly. |
| Benchmark | A shared dataset plus scoring rules so different methods can be compared. |
| Reproducibility | Whether someone else can rerun your experiment and get the same result. |
| Major Revision | A journal decision meaning the paper needs substantial changes and re-review. |
