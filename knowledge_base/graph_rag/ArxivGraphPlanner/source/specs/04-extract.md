# Task: Write wiki page 04 — Related Work & Implementation Details

You are extracting ONE section of a paper into ONE wiki page. Context is tight on this model — **read ONLY the file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/source/chunks/04.txt`

This chunk covers four appendix sections of the paper "GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs" (Feng et al., ICLR 2026):
- Appendix A: Additional Related Work
- Appendix B: GraphPlanner Training Details
- Appendix C: Implementation Details
- Appendix D: Dataset and LLM Backbone Details

There are no figures in this chunk.

## Output

Write the wiki page to:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/04-related-work-and-implementation.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Related Work & Implementation Details

**In one sentence:** <how this paper positions itself against prior work and what it takes to reproduce it, in one sentence>

## Key points

- <5-8 bullets: the key related-work threads and how this paper differs, plus concrete implementation facts (hyperparameters, hardware, datasets) — not "discusses X">

---

## Additional Related Work

<summarize the prior-work threads (e.g. LLM-agents/multi-agent systems, LLM routing methods) and how GraphPlanner differs from each, citing named prior methods where given>

## Training Details

<the RL training procedure specifics: episodes, early stopping criterion, evaluation/decoding, hardware, as given>

## Implementation Details

<architecture/hyperparameter specifics as given>

## Dataset and LLM Backbone Details

<the datasets/domains/tasks used and the LLM backbones evaluated, with any table content transcribed as a markdown table>

**Covers:** Appendix A (Additional Related Work), Appendix B (Training Details), Appendix C (Implementation Details), Appendix D (Dataset and LLM Backbone Details)
```

Requirements:
- Cover the WHOLE chunk, including Appendix D at the end — do not stop after Appendix A.
- Preserve exact hyperparameters, dataset names, and numbers from the source text; transcribe tables as markdown tables.
- Name specific prior works mentioned (do not just say "prior work").
- No meta-commentary about your own extraction process in the output file.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When done: `bd close <own-id> --reason "chunk 04 extracted"`
