# Task: extract wiki page 03 — results

## Input

Read ONLY this file: `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/source/chunks/03.txt`

This is plain text extracted from pages 6-7 of the paper "Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs" (Dragic, Rio, Ifrah — Oplit R&D, July 2026). It covers: accuracy across the seven model backbones (Table 3), the finding that tool reliability matters more than extended reasoning (Table 4), token usage patterns (Figure 1 description: GRA/RSA read ~29-33%/~24-29% of SQA's unique input tokens), the effect of the tool-call budget (Figure 2 description: accuracy vs. budget B, knee around B=30), and the "Further analysis" section synthesizing what drives GRA's advantage.

There are no images to embed — Figures 1 and 2 are described in the text as chart data (numbers/axes); render their key numbers as prose or a small table instead of an image reference. There is no PNG file for these figures.

Do NOT read any other file. Do NOT read this task's own fleet artifacts, logs, events.jsonl, task.json, PLAN_AND_STATUS.md, or KNOWLEDGE.md. Do NOT read sibling wiki pages for style reference — the format contract below is the only convention you need. Context is tight on this model.

## Output

Write the result to: `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/wiki/03-results.md`

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
— organize with your own subheadings (###) as needed. Preserve exact numbers (accuracy percentages,
confidence intervals, pp differences, failure rates, token-usage percentages, the B≈30 budget knee).
Do not omit the tail of the chunk (the "Further analysis" section) — cover it with the same care as
the opening (accuracy table).>
```

Rules:
- Cover the WHOLE chunk end-to-end — the "Further analysis" synthesis at the end matters as much as the accuracy tables at the start.
- No meta-commentary about being an AI, no "as an extract worker" text, no placeholder text.
- Faithful to the source: do not invent numbers or claims not present in the chunk.
- Reproduce Table 3 (accuracy by model/system) and Table 4 (tool-call reliability) as Markdown tables.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When the file is written:

```bash
bd close <own-id> --reason "chunk 03 extracted"
```
