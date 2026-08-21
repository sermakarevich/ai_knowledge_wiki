# Task: Write wiki page 02 — GraphPlanner Method

You are extracting ONE section of a paper into ONE wiki page. Context is tight on this model — **read ONLY the files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/source/chunks/02.txt`

This chunk covers Section 3 ("GraphPlanner: Graph-Based Agentic LLM Routing") of the paper "GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs" (Feng et al., ICLR 2026). This is the paper's core method section: the heterogeneous graph GARNet, the MDP formulation of routing-as-workflow-generation, and the reinforcement-learning policy training.

Also read this figure description (a vision-model transcription of Figure 2, which appears in this chunk's section):
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig2-graphplanner-mdp-overview-description.md`

The actual image file already exists at `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig2-graphplanner-mdp-overview.png` — you do not need to view it, just embed it at the right point using the markdown syntax below.

## Output

Write the wiki page to:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/02-graphplanner-method.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# GraphPlanner Method

**In one sentence:** <the method's whole mechanism, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim — the graph structure, the MDP formulation, the reward, the training algorithm, key equations/numbers — not "discusses X">

---

## <subsection, e.g. "Routing as Workflow Generation (the MDP view)">

<state/action/reward/transition definitions exactly as given>

![Overview of GraphPlanner's MDP formulation and graph memory](images/fig2-graphplanner-mdp-overview.png)

<a sentence or two describing what the figure shows, informed by the figure description file>

## <subsection, e.g. "GARNet: the Heterogeneous Graph Memory">

<node/edge types, how historical and workflow memories are integrated>

## <subsection, e.g. "Policy Training">

<the RL algorithm, loss/objective, training procedure as described in this chunk>

**Covers:** Section 3 (GraphPlanner: Graph-Based Agentic LLM Routing)
```

Requirements:
- Cover the WHOLE chunk, including its final subsection — do not stop after the opening paragraphs.
- Preserve exact equations, notation, and numbers from the source text (reproduce math in plain text/LaTeX-in-markdown as it appears).
- Embed the figure using the exact path shown above, near the text that discusses the MDP overview.
- No meta-commentary about your own extraction process in the output file.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When done: `bd close <own-id> --reason "chunk 02 extracted"`
