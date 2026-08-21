# Task: extract wiki page 01 — GRA agent design

## Input

Read ONLY this file: `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/source/chunks/01.txt`

This is plain text extracted from pages 1-4 of the paper "Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs" (Dragic, Rio, Ifrah — Oplit R&D, July 2026). It covers: the abstract/intro framing (code agents vs. graph agents), related work (ReAct, SWE-agent, GraphRAG survey, etc.), and the description of the three tested systems — GRA (Graph Reasoning Agent, 7 generic tools: ls, cat, grep, sems, query, think, answer), RSA (Retrieval SQL Agent, same loop with the graph removed), and SQA (SQL Agent, full-context baseline with ~17k tokens serialized up front).

There are no figures/images to embed for this chunk — the paper's diagrams are text/vector-based and already present as text in the chunk.

Do NOT read any other file. Do NOT read this task's own fleet artifacts, logs, events.jsonl, task.json, PLAN_AND_STATUS.md, or KNOWLEDGE.md. Do NOT read sibling wiki pages for style reference — the format contract below is the only convention you need. Context is tight on this model.

## Output

Write the result to: `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/wiki/01-gra-agent-design.md`

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
— organize with your own subheadings (###) as needed. Preserve specific facts: tool names, numbers,
citations by first author name (do not renumber references), and the exact distinctions the paper draws
(e.g. what differs between GRA, RSA, and SQA). Do not omit the tail of the chunk — cover material from
the end of the chunk (the RSA and SQA descriptions) with the same care as the opening (the intro/related work).>
```

Rules:
- Cover the WHOLE chunk end-to-end — the chunk's last major topic (RSA and SQA agent descriptions) matters as much as its first (intro framing).
- No meta-commentary about being an AI, no "as an extract worker" text, no placeholder text.
- Faithful to the source: do not invent numbers, citations, or claims not present in the chunk.
- Table 1 (the seven GRA tools: ls, cat, grep, sems, query, think, answer) must be reproduced as a proper Markdown table in the Detail section.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When the file is written:

```bash
bd close <own-id> --reason "chunk 01 extracted"
```
