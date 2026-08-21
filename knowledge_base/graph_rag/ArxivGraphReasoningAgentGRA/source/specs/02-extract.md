# Task: extract wiki page 02 — UFK-M benchmark & experimental setup

## Input

Read ONLY this file: `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/source/chunks/02.txt`

This is plain text extracted from page 5 of the paper "Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs" (Dragic, Rio, Ifrah — Oplit R&D, July 2026). It covers: the UFK-M benchmark (a synthetic bicycle-assembly factory with a "large" and "xlarge" tier — table sizes, row counts, KG nodes/edges, question counts), the answer-first question-generation methodology, deterministic scoring, and the experimental setup (seven backbone LLM configurations across four providers, turn budgets, bootstrap uncertainty quantification).

There are no figures/images to embed for this chunk. Table 2 (the two nested tiers of UFK-M) must be reproduced as a proper Markdown table.

Do NOT read any other file. Do NOT read this task's own fleet artifacts, logs, events.jsonl, task.json, PLAN_AND_STATUS.md, or KNOWLEDGE.md. Do NOT read sibling wiki pages for style reference — the format contract below is the only convention you need. Context is tight on this model.

## Output

Write the result to: `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/wiki/02-ufkm-benchmark.md`

If this file already exists (a retry), overwrite it completely with a fresh, complete page — do not append or patch.

## Format contract (wiki page)

Write a single Markdown file with exactly this structure:

```markdown
[[../index|Wiki]] | [[../summary|Summary]]

# <short descriptive title for this section of the paper>

**In one sentence:** <one sentence headline capturing the core idea of this chunk>

## Key points

- <bullet>
- <bullet>
- ... (5-10 bullets covering the whole chunk, not just the opening)

## Detail

<full detailed walkthrough of everything in the chunk, in your own words but faithful to the source
— organize with your own subheadings (###) as needed. Preserve specific numbers exactly (table/row/node/edge
counts, question counts and their breakdown by type, model names, turn budgets, bootstrap parameters).
Do not omit the tail of the chunk (experimental setup: models, turn budgets, decoding parameters) —
cover it with the same care as the opening (benchmark description).>
```

Rules:
- Cover the WHOLE chunk end-to-end — the experimental-setup material at the end matters as much as the benchmark description at the start.
- No meta-commentary about being an AI, no "as an extract worker" text, no placeholder text.
- Faithful to the source: do not invent numbers, model names, or claims not present in the chunk.
- Reproduce Table 2 (large vs. xlarge tiers) as a Markdown table.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When the file is written:

```bash
bd close <own-id> --reason "chunk 02 extracted"
```
