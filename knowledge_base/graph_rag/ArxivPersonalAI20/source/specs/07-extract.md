# Task: Extract wiki page 07 — Appendix: Pseudocode, Dataset Prep, Hyperparameters, and Judge Instructions

You are a worker extracting ONE section of an academic paper (PersonalAI 2.0 / PAI-2, a GraphRAG paper) into ONE wiki page. This is a mechanical extraction/summarization task, not a creative one.

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file in full:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/source/chunks/07.txt`

It contains Appendix C (pseudocode for the PAI-2 algorithm), Appendix D (dataset preprocessing operations for evaluation, including Table 24), Appendix E (retrieval hyperparameters), and Appendix F (LLM-as-a-Judge instructions, including Table 25).

## Output

Write your result to:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/07-appendix-pseudocode-datasets-hyperparams-judge.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Pseudocode, Dataset Preparation, Hyperparameters, and Judge Instructions

**In one sentence:** <what this appendix collectively documents, in one sentence>

## Key points

- <complete claim 1>
- <complete claim 2>
- <complete claim 3>
- <complete claim 4>
- <complete claim 5>
(5-8 bullets total; these must stand alone at medium depth)

---

## Appendix C: Pseudocode

<reproduce the algorithm's pseudocode as a code block, preserving structure/indentation as closely as possible>

## Appendix D: Dataset Preprocessing Operations

<full detail on how each of the six benchmark datasets was preprocessed; reproduce Table 24 as a markdown table with exact values>

## Appendix E: Retrieval Hyperparameters

<full detail — every hyperparameter and its value>

## Appendix F: LLM-as-a-Judge Instructions

<full detail on the judge protocol; reproduce Table 25's prompt content verbatim>

**Covers:** Appendices C, D, E, and F of the paper (including Tables 24 and 25).
```

## Rules

- The page must cover the WHOLE chunk, all four appendix subsections.
- Reproduce the pseudocode and tables faithfully (exact values, exact prompt wording).
- No meta-commentary about your own extraction process. No "as an AI..." preambles. Output only the wiki page content.
- This chunk has no figures to embed.
- Scope: touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.

## DoD

1. Output file written at the path above, covering the full chunk, following the format contract.
2. `bd close <own-id> --reason "chunk 07 extracted"`
