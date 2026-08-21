# Task: Extract wiki page 02 — Methods: the PAI-2 Pipeline

You are a worker extracting ONE section of an academic paper (PersonalAI 2.0 / PAI-2, a GraphRAG paper) into ONE wiki page. This is a mechanical extraction/summarization task, not a creative one.

**Context is tight on this model — read ONLY the two files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

1. Read this file in full — the paper's Methods section (Section III):
`/Users/sergii/.kb/papers/ArxivPersonalAI20/source/chunks/02.txt`

2. Read this file — a pre-written description of Figure 1 (the pipeline diagram) referenced in the chunk:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/images/02-figure1-description.md`

## Output

Write your result to:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/02-methods-pai2-pipeline.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Methods: The PAI-2 Pipeline

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete claim 1 — with numbers/mechanisms/conclusions, not "discusses X">
- <complete claim 2>
- <complete claim 3>
- <complete claim 4>
- <complete claim 5>
(5-8 bullets total; these must stand alone as the section at medium depth)

---

![PAI-2's QA pipeline for information search in memory graph](images/figure1-qa-pipeline.png)

<a paragraph describing what Figure 1 shows, based on the description file — write it as flowing prose, not a copy-paste of the description file>

## <subsection heading, e.g. "Question preprocessing">

<full detail: walk through each of the pipeline's numbered stages as described in the chunk (question preprocessing, initial plan generation, entity extraction, entity-to-vertex matching, clue-query generation, graph traversal e.g. BeamSearch/WaterCircles, path filtering, knowledge summarizing, plan validation, plan enhancement, sub-answer generation, "no answer" handling, answer aggregation). Use exact algorithm/mechanism names verbatim.>

## <another subsection heading>

...

**Covers:** Section III (Methods) of the paper, including Figure 1.
```

## Rules

- The page must cover the WHOLE chunk, including material near the end of the file.
- The figure MUST be embedded exactly as `![PAI-2's QA pipeline for information search in memory graph](images/figure1-qa-pipeline.png)` — this path is relative to the wiki/ folder and is already correct, do not change it.
- Use exact numbers, algorithm names, and mechanism names verbatim from the text where present.
- No meta-commentary about your own extraction process. No "as an AI..." preambles. Output only the wiki page content.
- Scope: touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.

## DoD

1. Output file written at the path above, covering the full chunk, following the format contract, with Figure 1 embedded.
2. `bd close <own-id> --reason "chunk 02 extracted"`
