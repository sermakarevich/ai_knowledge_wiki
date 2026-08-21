# Task: Write wiki page 06 — Prompt Templates & Worked Examples

You are extracting ONE section of a paper into ONE wiki page. Context is tight on this model — **read ONLY the file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/source/chunks/06.txt`

This chunk covers Appendix K (Prompt Usage) of the paper "GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs" (Feng et al., ICLR 2026) — the actual prompt templates used by the Planner/Executor/Summarizer agents, plus worked step-by-step examples of GraphPlanner decomposing a task into sub-questions and synthesizing a final answer.

There are no new figures in this chunk (Figure 6 was already embedded in wiki page 05).

## Output

Write the wiki page to:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/06-prompt-templates-and-examples.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Prompt Templates & Worked Examples

**In one sentence:** <what this appendix shows about how GraphPlanner's agents are actually prompted, in one sentence>

## Key points

- <5-8 bullets: the distinct prompt roles/templates present, and what the worked examples demonstrate about workflow decomposition — not "discusses X">

---

## Prompt Templates

<transcribe the actual prompt templates verbatim, in fenced code blocks or blockquotes, one per agent role (Planner/Executor/Summarizer/Verifier as applicable), preserving placeholders exactly as written>

## Worked Example 1: <short label for the task type, e.g. "Multi-step arithmetic reasoning">

<walk through the example step by step exactly as given: original task, decomposed sub-questions Q1/Q2/..., intermediate answers, final synthesis>

## Worked Example 2: <short label for the second task type, if present>

<same treatment>

**Covers:** Appendix K (Prompt Usage)
```

Requirements:
- Cover the WHOLE chunk, including every worked example present — do not stop after the first prompt template.
- Transcribe prompts and examples verbatim (exact wording, quotes, placeholders) — this appendix's value is the literal text.
- No meta-commentary about your own extraction process in the output file.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When done: `bd close <own-id> --reason "chunk 06 extracted"`
