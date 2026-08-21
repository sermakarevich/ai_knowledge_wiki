# Task: Write wiki page 05 — Additional Ablations & Generalization

You are extracting ONE section of a paper into ONE wiki page. Context is tight on this model — **read ONLY the files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/source/chunks/05.txt`

This chunk covers appendix sections of the paper "GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs" (Feng et al., ICLR 2026):
- Appendix E: Experiments on New Agentic Roles
- Appendix F: Additional Ablations on Other Graph Encoders
- Appendix G: Additional Ablations on Historical Information Processing
- Appendix H: Additional Experiments on New Dataset
- Appendix I: Comparison on Time Cost
- Appendix J: Illustrative Examples of GraphPlanner (introductory text before the worked examples, which continue in the next chunk)

Also read this figure description (a vision-model transcription of Figure 6, which appears near the end of this chunk):
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig6-illustrative-workflow-examples-description.md`

The actual image file already exists at `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig6-illustrative-workflow-examples.png` — you do not need to view it, just embed it at the right point using the markdown syntax below.

## Output

Write the wiki page to:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/05-additional-ablations-and-generalization.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Additional Ablations & Generalization

**In one sentence:** <the overall takeaway of this battery of extra experiments, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real numbers from the ablations/generalization results — not "discusses X">

---

## New Agentic Roles

<findings from Appendix E: how GraphPlanner generalizes to roles beyond Planner/Executor/Summarizer>

## Alternative Graph Encoders

<findings from Appendix F: which encoders were compared against GARNet and the result>

## Historical Information Processing

<findings from Appendix G>

## New Dataset

<findings from Appendix H>

## Time Cost Comparison

<findings from Appendix I, with numbers/table if given>

## Illustrative Examples (overview)

![Illustrative examples of GraphPlanner's workflow generation](images/fig6-illustrative-workflow-examples.png)

<description informed by the figure description file; note that the detailed worked examples continue in wiki page 06>

**Covers:** Appendix E (New Agentic Roles), F (Other Graph Encoders), G (Historical Information Processing), H (New Dataset), I (Time Cost Comparison), J (Illustrative Examples intro)
```

Requirements:
- Cover the WHOLE chunk, including Appendix I and the start of J — do not stop after Appendix E.
- Preserve exact numbers and comparisons from the source text; transcribe tables as markdown tables.
- Embed the figure using the exact path shown above.
- No meta-commentary about your own extraction process in the output file.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When done: `bd close <own-id> --reason "chunk 05 extracted"`
