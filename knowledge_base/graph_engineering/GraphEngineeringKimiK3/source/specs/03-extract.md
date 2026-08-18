# Task: write wiki page 03 for GraphEngineeringKimiK3

You are a worker with a small context window. **Read ONLY the one input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not try to diagnose a prior failure by reading logs — just re-read the input and write directly.

## Input

Read this file in full (it is short, well under your context window):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/source/chunks/03.txt
```

It covers the 8-layer architecture (Ingestion, Extraction, Resolution, Storage, Retrieval,
Agent, Verification, Update — a closed loop) and the 5 pipeline prompts (Extraction, Entity
Resolution, Query Translation, Grounded Answer, Graph Maintenance) with their full verbatim
prompt text. It includes a bracketed `[FIGURE: images/....jpg — description: ...]` marker —
use it to write the embed and caption, you do not need to view the image yourself.

One image already exists at this path (relative to the output file's directory):
- `images/05_HPd2SF6WYAAQwmJ.jpg`

## Output

Write the complete wiki page to this absolute path (if it already exists — a retry — overwrite it completely):

```
/Users/sergii/.kb/papers/GraphEngineeringKimiK3/wiki/03-the-8-layer-architecture-and-5-prompts.md
```

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The 8-Layer Architecture and the 5 Pipeline Prompts

**In one sentence:** <the whole point of this chunk in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim. Name all 8 layers in order, note the loop
  closes at Update back to Extraction, and note each of the 5 prompts' narrow job.>

---

## The 8 Layers

<Numbered list or table of the 8 layers with their job, including the JSON extraction example
from the source verbatim in a code block. Embed the figure inline here, using its bracketed
description as the caption content:>

![<short caption derived from the figure's description>](images/05_HPd2SF6WYAAQwmJ.jpg)

## The 5 Prompts That Run the Pipeline

<For each of the 5 prompts: its name/purpose in one line, then the full verbatim prompt text in
a fenced code block exactly as given in the source — do not paraphrase or shorten the prompts.>

**Covers:** "The Architecture, Layer by Layer" and "5 Prompts That Run the Pipeline."
```

## Rules

- Touch ONLY the one output file above. Do not run any fleet commands other than the final `bd close`.
- No git commands at all.
- Reproduce the 5 prompts and the JSON extraction example VERBATIM in code blocks — these are
  reference material the reader will copy-paste, so do not summarize or truncate them.
- When done, close this bead: `bd close <own-id> --reason "chunk 03 extracted"`.
