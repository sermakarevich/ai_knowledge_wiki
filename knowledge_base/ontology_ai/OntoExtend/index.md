---
type: index
title: "OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs"
description: "Folder index for the OntoExtend paper: requirement-driven, retrieval-grounded ontology extension evaluated on 39 CQs from Onto-DESIDE and Bosch, with 100% CQ verification and under 2% superfluous elements."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T13:19:54Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.17963v1
  - id: local-copy
    resource: source/source.md
tags: [ontology-extension, large-language-models, retrieval-augmented-generation, competency-questions, ontology-evaluation]
---

# OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs

OntoExtend extends a mature ontology one competency question at a time: a Retriever pulls the top-k relevant elements from the input ontology, an Extender prompts an LLM with the CQ plus retrieved Turtle to draft a grounded fragment, and an Integrator merges it back. Tested on 39 CQs from the Onto-DESIDE network and an industrial Bosch ontology, it hit 100% CQ verification with under 2% superfluous elements — but engineer ratings split between minor edits (industry) and moderate revision (EU project). Use this folder as a drafting-assistant briefing, not a drop-in automation case.

## How to work through this

Start with the summary (~2 min) for the TL;DR, problem, ideas, and findings. Then read the digest (~10 min) for the five-move argument across all six wiki chunks. Then go deep into the wiki pages in order, using the explainer for plain-language intuition, critical_thinking for claims-vs-evidence scrutiny, and questions for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, original ideas, key findings, future directions.
- [Digest](digest.md) — ten-minute guided tour: one-sentence take plus key points per wiki chunk, then the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the framework and results.
- [Critical thinking](critical_thinking.md) — claims vs. evidence and what the evaluation does and does not show.
- [Questions](questions.md) — twelve retrieval-practice Q&As covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01-framework-overview](wiki/01-framework-overview.md) | Abstract, introduction, and research questions: what OntoExtend is, the Retriever/Extender/Integrator pipeline, and stated contributions |
| [02-related-work-comparison](wiki/02-related-work-comparison.md) | Related-work comparison table and synthesis, plus framework internals: FAISS Retriever, constrained Extender prompting, and Integrator |
| [03-experimental-setup](wiki/03-experimental-setup.md) | Experimental setup: 39-CQ dataset construction, retrieval tuning (text-embedding-ada-002, pipe, comments), LLM/prompt choice, and evaluation criteria |
| [04-evaluation-methodology](wiki/04-evaluation-methodology.md) | Evaluation methodology and results: RDFLib/OOPS!/Pellet structural checks, CQ verification and superfluous elements, six-engineer survey (Tables 4–5) |
| [05-discussion-results](wiki/05-discussion-results.md) | Discussion, limitations, and conclusion: CQ-specificity effects, LLM-as-quality-proxy, retrieval cost savings, and future work |
| [06-references](wiki/06-references.md) | Bibliography: references [1]–[29] on LLM-assisted ontology generation, enrichment, and evaluation |

## Original Source

- arXiv: [OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs](https://arxiv.org/abs/2607.17963v1)
- Local copy: [source/source.md](source/source.md)
