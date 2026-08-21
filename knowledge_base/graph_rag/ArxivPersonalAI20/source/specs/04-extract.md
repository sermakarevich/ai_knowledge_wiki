# Task: Extract wiki page 04 — Experiments and Results

You are a worker extracting ONE section of an academic paper (PersonalAI 2.0 / PAI-2, a GraphRAG paper) into ONE wiki page. This is a mechanical extraction/summarization task, not a creative one.

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file in full:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/source/chunks/04.txt`

It contains the paper's Experiments and Results section (Section VI), including the headline comparison against LightRAG/RAPTOR/HippoRAG 2, the ablation on graph traversal algorithms (BeamSearch, WaterCircles) vs. flat retrieval, the search-plan-enhancement ablation (18% boost claim), triple-type ablation, clue-query-count ablation, and latency results.

## Output

Write your result to:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/04-experiments-and-results.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments and Results

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete claim 1 — with the EXACT numbers from the text, e.g. "PAI-2 achieves a 4% average gain by LLM-as-a-Judge across four benchmarks">
- <complete claim 2 — with exact numbers>
- <complete claim 3 — with exact numbers>
- <complete claim 4 — with exact numbers>
- <complete claim 5 — with exact numbers>
- <complete claim 6 — with exact numbers>
(6-8 bullets total; these must stand alone as the section at medium depth — this is the results section, numbers matter most here)

---

## <subsection heading, e.g. "Main comparison against baselines">

<full detail, reproduce relevant tables as markdown tables with exact values, e.g. Table 3>

## <subsection heading, e.g. "Graph traversal algorithm ablation">

<full detail on BeamSearch, WaterCircles vs flat retriever, with the 6% figure and any table values>

## <subsection heading, e.g. "Search-plan enhancement ablation">

<full detail on the 18% boost claim>

## <subsection heading, e.g. "Triple-type and clue-query-count ablations">

<full detail, reproduce Tables 4 and 5>

## <subsection heading, e.g. "Latency">

<full detail, reproduce Table 6 (latency in minutes for PAI-1 vs PAI-2 with Qwen2.5 7B across 6 datasets)>

**Covers:** Section VI (Experiments and Results) of the paper, including Tables 1–6.
```

## Rules

- The page must cover the WHOLE chunk, including material near the end of the file (latency results are usually near the end — do not truncate before them).
- Reproduce every table found in the chunk as a markdown table with exact values — this is the results section, precision matters.
- Use exact numbers, percentages, and method names verbatim from the text.
- No meta-commentary about your own extraction process. No "as an AI..." preambles. Output only the wiki page content.
- This chunk has no figures to embed.
- Scope: touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.

## DoD

1. Output file written at the path above, covering the full chunk including all tables, following the format contract.
2. `bd close <own-id> --reason "chunk 04 extracted"`
