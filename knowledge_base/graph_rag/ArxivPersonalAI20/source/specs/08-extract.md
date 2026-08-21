# Task: Extract wiki page 08 — Appendix: Memory Graph Stats, Clue-Query Ablations, MINE-1, and Human Evaluation

You are a worker extracting ONE section of an academic paper (PersonalAI 2.0 / PAI-2, a GraphRAG paper) into ONE wiki page. This is a mechanical extraction/summarization task, not a creative one.

**Context is tight on this model — read ONLY the two files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

1. Read this file in full:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/source/chunks/08.txt`

It contains Appendix G (characteristics of constructed memory graphs, Tables 26–28), Appendix H (non-aggregated results for the clue-queries-number ablation study, Tables 29–32), Appendix I (PAI-2 evaluation on the MINE-1 benchmark, including Figure 2 and Tables 33–34), and Appendix J (human evaluation, Tables 35–37).

2. Read this file — a pre-written description of Figure 2 (the MINE-1 score distribution chart) referenced in the chunk:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/images/08-figure2-description.md`

## Output

Write your result to:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/08-appendix-graph-stats-ablations-mine1-humaneval.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Memory Graph Stats, Clue-Query Ablations, MINE-1, and Human Evaluation

**In one sentence:** <what this appendix collectively documents, in one sentence>

## Key points

- <complete claim 1 — with exact numbers, e.g. the MINE-1 89% information-retention score>
- <complete claim 2>
- <complete claim 3>
- <complete claim 4>
- <complete claim 5>
- <complete claim 6>
(6-8 bullets total; these must stand alone at medium depth)

---

## Appendix G: Memory Graph Characteristics

<full detail, reproduce Tables 26, 27, 28 as markdown tables with exact values>

## Appendix H: Clue-Queries-Number Ablation (Non-Aggregated)

<full detail, reproduce Tables 29–32 as markdown tables with exact values>

## Appendix I: PAI-2 Evaluation on MINE-1

![Distribution of MINE-1 scores across 100 articles for PAI-2, Wikontic and KGGen](images/figure2-mine1-distribution.png)

<a paragraph describing what Figure 2 shows, based on the description file — write it as flowing prose, not a copy-paste of the description file. Then full detail on the MINE-1 protocol and reproduce Tables 33–34>

## Appendix J: Human Evaluation

<full detail, reproduce Tables 35, 36, 37 as markdown tables with exact values — Krippendorff's alpha, Pearson correlation, and HumanEval vs LLM-as-a-Judge scores>

**Covers:** Appendices G, H, I, and J of the paper (Tables 26–37, Figure 2).
```

## Rules

- The page must cover the WHOLE chunk, all four appendix subsections, including material near the end (Appendix J) — do not truncate before it.
- The figure MUST be embedded exactly as `![Distribution of MINE-1 scores across 100 articles for PAI-2, Wikontic and KGGen](images/figure2-mine1-distribution.png)` — this path is relative to the wiki/ folder and is already correct, do not change it.
- Reproduce every table with exact values.
- No meta-commentary about your own extraction process. No "as an AI..." preambles. Output only the wiki page content.
- Scope: touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.

## DoD

1. Output file written at the path above, covering the full chunk including all tables and Figure 2, following the format contract.
2. `bd close <own-id> --reason "chunk 08 extracted"`
