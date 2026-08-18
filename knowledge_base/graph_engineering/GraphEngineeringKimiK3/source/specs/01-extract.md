# Task: write wiki page 01 for GraphEngineeringKimiK3

You are a worker with a small context window. **Read ONLY the one input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not try to diagnose a prior failure by reading logs — just re-read the input and write directly.

## Input

Read this file in full (it is short, well under your context window):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/source/chunks/01.txt
```

It contains the article's opening section: the problem with standard RAG, and what "graph engineering" (the knowledge-graph / GraphRAG sense) actually is. It includes bracketed `[FIGURE: images/....jpg — description: ...]` markers giving you a text description of each figure — use these to write the embed and caption, you do not need to view the images yourself.

Three images already exist at these paths (relative to the output file's directory, i.e. `images/<file>`):
- `images/01_HPhTmdJWkAAVhUF.jpg`
- `images/02_HPd4u13XUAAMNII.jpg`
- `images/03_HPd2I-8W4AAmwdF.jpg`

## Output

Write the complete wiki page to this absolute path (if it already exists — a retry — overwrite it completely):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/wiki/01-the-problem-and-what-graph-engineering-is.md
```

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Problem, and What Graph Engineering Actually Is

**In one sentence:** <the whole point of this chunk in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim carrying real content (numbers, mechanisms,
  conclusions) — not "discusses X". A reader who reads only these bullets should have the
  chunk's substance.>

---

## <## subsections mirroring the chunk's own structure, e.g.>
## The Problem with Standard RAG
## What Graph Engineering Actually Is (triples, local vs. global search)

<Full detail: hierarchical prose/subsections following the chunk's own headings. Include the
concrete triple examples verbatim (Kimi K3 -> developed by -> Moonshot AI, etc.) and the
"why did sales drop in March" walkthrough. Embed each figure inline, right next to the text it
illustrates, using its description from the bracketed marker as the caption content:>

![<short caption derived from the figure's description>](images/01_HPhTmdJWkAAVhUF.jpg)

![<short caption>](images/02_HPd4u13XUAAMNII.jpg)

![<short caption>](images/03_HPd2I-8W4AAmwdF.jpg)

**Covers:** Article intro through "What Graph Engineering Actually Is" (local/global search framing).
```

## IMPORTANT — terminology note

Near the top of the page (right after the one-sentence summary or in the key points), explicitly
note: this article uses "graph engineering" in the KNOWLEDGE-GRAPH / GraphRAG sense — storing
facts as triples and querying relationships — which is DIFFERENT from the agent-topology sense
of "graph engineering" (wiring multi-agent loops/pipelines into a graph), used elsewhere in
related research. This is a real distinction the reader must not miss.

## Rules

- Touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.
- No git commands at all.
- Use exact numbers, causal-chain examples, and triple notation verbatim from the source chunk.
- When done, close this bead: `bd close <own-id> --reason "chunk 01 extracted"`.
