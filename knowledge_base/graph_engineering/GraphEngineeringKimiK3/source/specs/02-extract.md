# Task: write wiki page 02 for GraphEngineeringKimiK3

You are a worker with a small context window. **Read ONLY the one input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not try to diagnose a prior failure by reading logs — just re-read the input and write directly.

## Input

Read this file in full (it is short, well under your context window):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/source/chunks/02.txt
```

It covers: why the article picks Kimi K3 (1M context window, Kimi Delta Attention, Attention
Residuals, and an honest caveat about K3 not being the strongest model overall), the finding
that graph quality beats model size across 26 compared models, and the three ways to combine
an LLM with a knowledge graph (KG-enhanced LLM / LLM-augmented KG / Synergized). It includes a
bracketed `[FIGURE: images/....jpg — description: ...]` marker — use it to write the embed and
caption, you do not need to view the image yourself.

One image already exists at this path (relative to the output file's directory):
- `images/04_HOU5pIVaQAA9Bo-.jpg`

## Output

Write the complete wiki page to this absolute path (if it already exists — a retry — overwrite it completely):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/wiki/02-why-kimi-k3-and-the-model-vs-graph-finding.md
```

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Why Kimi K3, and the Model-vs-Graph Finding

**In one sentence:** <the whole point of this chunk in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim carrying real content (numbers, mechanisms,
  conclusions) — not "discusses X". Include: the 1M/1,048,576 token context number, the 6.3x
  KDA decoding speedup, the AttnRes mechanism's practical effect, the honest caveat that K3
  trails Claude Fable 5 and GPT-5.6 Sol overall, the "bigger model + bad graph -> worse; smaller
  model + good graph -> better" finding, and the three integration modes with Mode 3 as the
  recommended one.>

---

## <## subsections mirroring the chunk's own structure, e.g.>
## Why Kimi K3 Specifically (1M context, KDA, AttnRes, the honest caveat)
## The Finding That Should Change How You Build (graph beats model size)
## Three Ways to Combine LLM and Graph — Pick the Third

<Full detail, hierarchical prose following the chunk's own headings. Embed the figure inline
next to the "why Kimi K3 / context window" discussion, using its bracketed description as the
caption content:>

![<short caption derived from the figure's description>](images/04_HOU5pIVaQAA9Bo-.jpg)

Note explicitly: the article name-checks "agent graphs" (Anthropic, LangGraph) as a parallel
trend showing the same "structure beats scale" principle — but that is the OTHER, agent-topology
sense of graph engineering, not what this article itself is about. Do not conflate the two.

**Covers:** "Why Kimi K3 Specifically" through "Three Ways to Combine LLM and Graph."
```

## Rules

- Touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.
- No git commands at all.
- Use exact numbers (1,048,576 tokens, 6.3x, 26 models) verbatim from the source chunk.
- When done, close this bead: `bd close <own-id> --reason "chunk 02 extracted"`.
