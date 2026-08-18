# Task: write wiki page 04 for GraphEngineeringKimiK3

You are a worker with a small context window. **Read ONLY the one input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not try to diagnose a prior failure by reading logs — just re-read the input and write directly.

## Input

Read this file in full (it is short, well under your context window):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/source/chunks/04.txt
```

It covers: the recommended tech stack (Neo4j, Kimi K3 API, Kimi Code CLI, DSPy), a realistic
7-day build plan, five common failure modes with fixes, a caveat about the "85% lower cost, 18%
better accuracy" numbers floating around, and the article's conclusion. This chunk has no figures.

## Output

Write the complete wiki page to this absolute path (if it already exists — a retry — overwrite it completely):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/wiki/04-stack-week-one-plan-and-troubleshooting.md
```

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Stack, Week-One Plan, and Troubleshooting

**In one sentence:** <the whole point of this chunk in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim. Include: the recommended stack components,
  the shape of the week-one plan, the single most common failure (duplicate entities) and its
  fix, and the caveat about the "85%/18%" numbers not being a universal guarantee.>

---

## The Stack

<List the 4 stack components (graph database, model, agent layer, orchestration) with the
reasoning given for each.>

## Week One: A Realistic Plan

<The day-by-day plan, Day 1 through Day 6-7, as given.>

## Troubleshooting

<All 5 problems from the source, each as a subsection: the failure mode, why it happens, and
the fix — verbatim detail from the source, not paraphrased away.>

## About Those Numbers You'll See Quoted

<The caveat about "85% lower cost, 18% better accuracy" — what it's actually measuring, and why
the reader should measure their own data instead of trusting the published percentage.>

## What You Actually Get, and Conclusion

<The closing summary of what graph engineering delivers vs. standard RAG, the real tradeoff
(a week of upfront work), and the article's final point: build the graph, the model is the easy
part. Include the article's link list (Kimi K3, Kimi K3 GitHub, Kimi Code CLI, Neo4j, Microsoft
GraphRAG, DSPy) as a bullet list of resources.>

**Covers:** "The Stack" through "Conclusion," plus the article's link list.
```

## Rules

- Touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.
- No git commands at all.
- Preserve the day-by-day plan and troubleshooting fixes with their concrete detail, not generic paraphrase.
- When done, close this bead: `bd close <own-id> --reason "chunk 04 extracted"`.
