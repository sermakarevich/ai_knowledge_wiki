# Task: Extract wiki page 06 — Appendix: LLM Prompts for the QA Pipeline

You are a worker extracting ONE section of an academic paper (PersonalAI 2.0 / PAI-2, a GraphRAG paper) into ONE wiki page. This is a mechanical extraction/summarization task, not a creative one.

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file in full:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/source/chunks/06.txt`

It contains Appendix A (LLM prompts used in query preprocessing: grammar checking, noise removal, editing, rephrasing) and Appendix B (LLM prompts used in memory-graph exploration and answer aggregation: search-plan generation, entity extraction, clue-question generation, clue-answer generation, answer summarization, plan-completeness checking, plan enhancement, final answer generation) — this is a large chunk of prompt tables (Tables 7–23).

## Output

Write your result to:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/06-appendix-prompts-pipeline-stages.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: LLM Prompts for the QA Pipeline

**In one sentence:** <what this appendix documents, in one sentence — that it gives the exact prompt templates used at each pipeline stage>

## Key points

- <complete claim 1 — e.g. what categories of prompts exist (preprocessing vs. graph exploration) and how many tables/stages each covers>
- <complete claim 2>
- <complete claim 3>
- <complete claim 4>
- <complete claim 5>
(5-8 bullets total; these must stand alone at medium depth)

---

## Appendix A: Query Preprocessing Prompts

<for EACH table (7–13), give: table number, its purpose/title (one line), and the prompt content — quote the System/User/Assistant prompt text verbatim in a markdown table or blockquote, since these are exact artifacts the reader may want to reuse>

## Appendix B: Memory Graph Exploration and Answer Aggregation Prompts

<for EACH table (14–23), give: table number, its purpose/title (one line), and the prompt content verbatim, same format>

**Covers:** Appendix A and Appendix B of the paper (Tables 7–23) — all LLM prompt templates used across the PAI-2 pipeline stages.
```

## Rules

- The page must cover the WHOLE chunk — every table from Table 7 through Table 23 must appear on the page. Do not skip any; this is the longest chunk but completeness matters more than brevity here.
- Quote prompt text verbatim (System/User/Assistant roles, rules, examples) — these are exact reusable artifacts, not something to paraphrase away.
- No meta-commentary about your own extraction process. No "as an AI..." preambles. Output only the wiki page content.
- This chunk has no figures to embed.
- Scope: touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.

## DoD

1. Output file written at the path above, covering ALL 17 tables (7 through 23) in the chunk, following the format contract.
2. `bd close <own-id> --reason "chunk 06 extracted"`
