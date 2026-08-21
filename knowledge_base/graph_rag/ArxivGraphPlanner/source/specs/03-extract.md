# Task: Write wiki page 03 — Experiments, Results & Conclusion

You are extracting ONE section of a paper into ONE wiki page. Context is tight on this model — **read ONLY the files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/source/chunks/03.txt`

This chunk covers Section 4 (Experiments), Section 5 (Conclusion), and the Ethics Statement of the paper "GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs" (Feng et al., ICLR 2026). It includes the experimental setup, baselines, main results across 14 tasks/6 domains, ablations, and the paper's conclusion.

Also read these three figure descriptions (vision-model transcriptions of figures that appear in this chunk's section):
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig3-phase1-evaluation-description.md`
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig4-pareto-frontier-description.md`
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig5-generalization-ablation-description.md`

The actual image files already exist at `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig3-phase1-evaluation.png`, `fig4-pareto-frontier.png`, and `fig5-generalization-ablation.png` — you do not need to view them, just embed them at the right points using the markdown syntax below.

## Output

Write the wiki page to:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/03-experiments-and-results.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments, Results & Conclusion

**In one sentence:** <the experimental headline claim, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real numbers — main result magnitudes, ablation deltas, generalization findings — not "discusses X">

---

## <subsection, e.g. "Experimental Setup">

<tasks, domains, baselines, LLM backbones, training/test splits as described>

## <subsection, e.g. "Phase 1 Evaluation">

![Detailed illustration of Phase 1 Evaluation](images/fig3-phase1-evaluation.png)

<description informed by the figure description file>

## <subsection, e.g. "Main Results">

Include a results table if the chunk provides comparable numbers.

![GraphPlanner vs. baselines: accuracy/cost Pareto frontier](images/fig4-pareto-frontier.png)

<description informed by the figure description file>

## <subsection, e.g. "Generalization and Ablations">

![Generalization to unseen LLMs, history ablation, transductive vs. inductive](images/fig5-generalization-ablation.png)

<description informed by the figure description file>

## Conclusion

<the paper's own conclusion, in its own terms, plus the Ethics Statement content if substantive>

**Covers:** Section 4 (Experiments), Section 5 (Conclusion), Ethics Statement
```

Requirements:
- Cover the WHOLE chunk, including the Conclusion at the end — do not stop after the experimental setup.
- Preserve exact numbers, percentages, and result magnitudes from the source text.
- Embed all three figures using the exact paths shown above, near the text that discusses each.
- No meta-commentary about your own extraction process in the output file.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When done: `bd close <own-id> --reason "chunk 03 extracted"`
