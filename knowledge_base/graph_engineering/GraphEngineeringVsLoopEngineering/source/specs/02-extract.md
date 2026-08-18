# Extract wiki page 02 -- Anatomy of a Graph: What Makes It Different

## Context

This is one worker task in a larger pipeline that turns a YouTube video transcript into an
English-language knowledge-base wiki entry. The source video is a Chinese-language tech
commentary titled "什么是图工程 | Graph Engineering | 循环工程 | Loop Engineering | ..." (English:
"What Is Graph Engineering? From Loop Engineering to Multi-Agent Orchestration"), published by
the channel 最佳拍档 (host: 大飞). It argues that "Graph Engineering" is the latest layer in a
five-layer evolution of AI agent engineering (prompt -> context -> harness -> loop -> graph
engineering), explains what a graph actually is, when to use which topology, and when NOT to
bother.

**IMPORTANT -- context is tight on this model. Read ONLY the one input file listed below. Do
NOT read this task's own fleet artifacts/log/event files, do NOT read sibling wiki pages "for
style reference", and do NOT read the other chunk files. The format contract below is the only
convention you need. If this is a retry, do not try to diagnose the previous failure by reading
logs -- just re-read the input chunk and write the output directly.**

## Input

Read exactly this one file (a timestamped, Chinese-language transcript segment,
`[MM:SS] <text>` per line):

```
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/source/chunks/02.txt
```

## What this chunk covers

This chunk covers (in Chinese, with [MM:SS] timestamps):
- The key distinction: the "graph" here is NOT the flowchart people draw in slides (boxes and
  arrows meant for humans to read, describing how we WANT things to go). This graph is meant to
  be executed BY MACHINES: tasks, dependencies, state, permissions, budget, failure recovery,
  human approval -- all of it must be something the system actually enforces, not just depicts.
- The formal anatomy, stripped of jargon, has four parts:
  - **V (nodes)** -- the units of work. One input, one output, does exactly one thing. Can be a
    specialized agent or a deterministic step.
  - **E (edges)** -- routing between nodes: answers "where does it go next". Can be a straight
    pass-through, a conditional branch, a fan-out, a fan-in, or a loop-back.
  - **S (state)** -- the object that flows along edges and is read/written by everyone: records
    tasks, evidence, budget, artifacts, checkpoints. This is what welds a pile of independently
    acting agents into one system.
  - **P (policy)** -- constraints on who can create nodes, call tools, modify the graph, etc.
  - The "small self-running company" analogy: a company doesn't let the same person research,
    write the proposal, AND review it in one unbroken stretch -- it splits the work across
    roles, lets work flow between roles, and rolls results up. A graph is the same idea: an
    agent graduates from a single while-loop into an org chart.
- Two common confusions to clarify explicitly:
  1. This is NOT a knowledge graph. A knowledge graph organizes what the system KNOWS; this
     graph organizes WHO the system is made of and HOW work flows.
  2. This is NOT just drawing an existing process as a flowchart. It only counts as a real
     system structure when nodes can execute independently, edges carry explicit state, AND the
     process can be inspected, paused, and resumed/tracked.

## Output

Write the wiki page to:

```
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/wiki/02-anatomy-of-a-graph.md
```

## Wiki page format contract (follow exactly)

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# <Topic Title>

**In one sentence:** <the page's whole argument, one sentence>

## Key points

- <5-8 bullets, each a COMPLETE, standalone claim with real content -- numbers,
  mechanisms, named concepts, conclusions. NOT topic labels like "discusses X".
  Someone who reads only these bullets must have the substance of this page.>

---

## <First subsection mirroring the source's own structure>

<full detail: hierarchical ## subsections, exact numbers/terms/named concepts,
tables where useful, quotes attributed to the people named in the chunk (e.g.
Peter Steinberger, David Khourshid, Boris Cherny, Anthropic). Cite timestamps
like [03:24] next to major points so a reader can jump to that moment in the
source video.>

## <More subsections as needed>

...

**Covers:** [<start MM:SS>-<end MM:SS>] of the source video transcript
```

Rules:
- Output MUST be written in English, even though the source chunk is in Chinese --
  translate and synthesize, do not leave any Chinese text in the output file.
- Every named concept, framework, number, or person in the chunk must appear in the
  page (e.g. "90.2%", "15x tokens", "2000 vs 8000 tokens", "Boris Cherny", "Peter
  Steinberger", "LangGraph", "AutoGen", "CrewAI", "Google ADK", "Anthropic").
- No line limit. Be thorough -- this is the deep rung of the wiki, not a summary.
- If this file already exists (a retry), overwrite it completely.


## Scope & constraints

- Touch ONLY the one output file listed above. Do not edit or create any other file.
- Do not run any git commands -- this KB directory auto-syncs on its own.
- Do not run `fleet serve restart` / `fleet run` or any other fleet supervisor command.

## Definition of Done

1. The output file above exists and is written in English, following the format contract.
2. `bd close <own-task-id> --reason "wiki page 02 extracted"`
