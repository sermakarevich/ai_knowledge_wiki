# Task: Extract wiki page 03 — Experimental Setup and Evaluation Design

You are a worker extracting ONE section of an academic paper (PersonalAI 2.0 / PAI-2, a GraphRAG paper) into ONE wiki page. This is a mechanical extraction/summarization task, not a creative one.

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file in full:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/source/chunks/03.txt`

It contains the paper's Experiment Set-up and Evaluation sections (Sections IV and V), including benchmark datasets (Natural Questions, TriviaQA, HotpotQA, 2WikiMultihopQA, MuSiQue, DiaASQ), baselines (LightRAG, RAPTOR, HippoRAG 2), and evaluation metrics.

## Output

Write your result to:
`/Users/sergii/.kb/papers/ArxivPersonalAI20/wiki/03-experimental-setup-and-evaluation.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup and Evaluation Design

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete claim 1 — with numbers/mechanisms/conclusions, not "discusses X">
- <complete claim 2>
- <complete claim 3>
- <complete claim 4>
- <complete claim 5>
(5-8 bullets total; these must stand alone as the section at medium depth)

---

## <subsection heading, e.g. "Benchmarks">

<full detail: list every benchmark dataset by name with its characteristics as given in the text (e.g. any table values)>

## <subsection heading, e.g. "Baselines">

<full detail on LightRAG, RAPTOR, HippoRAG 2 and any other compared methods>

## <subsection heading, e.g. "Evaluation metrics and protocol">

<full detail: LLM-as-a-Judge protocol, Context Relevance / Faithfulness metrics, any tables reproduced as markdown tables>

**Covers:** Sections IV (Experiment Set-up) and V (Evaluation) of the paper.
```

## Rules

- The page must cover the WHOLE chunk, including material near the end of the file.
- Reproduce any tables found in the chunk as markdown tables with exact values.
- Use exact numbers, dataset names, and metric names verbatim from the text.
- No meta-commentary about your own extraction process. No "as an AI..." preambles. Output only the wiki page content.
- This chunk has no figures to embed.
- Scope: touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.

## DoD

1. Output file written at the path above, covering the full chunk, following the format contract.
2. `bd close <own-id> --reason "chunk 03 extracted"`
