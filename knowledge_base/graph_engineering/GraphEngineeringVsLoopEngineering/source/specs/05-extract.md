# Extract wiki page 05 -- Worked Example: Daily Research Brief, Loop vs. Graph

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
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/source/chunks/05.txt
```

## What this chunk covers

This chunk covers (in Chinese, with [MM:SS] timestamps):
- A concrete task (borrowed from Anthropic/community examples for being small yet typical): a
  daily research brief -- every morning, read the latest content on a topic from a few sources,
  write a one-page summary, and check it for accuracy before it lands in the user's inbox.
- **Built as a single loop**: one agent does everything in one context -- dumps raw search
  results from all sources into context, drafts the brief, then reviews its own draft. The
  failure mode: by review time the context is already a mess (raw scraped pages, half-written
  sentences, the agent's own earlier reasoning all mixed together); it is reviewing its own
  draft in the SAME context it was written in, which is effectively the author grading their own
  exam -- it will almost always stamp "pass". Because a loop is inherently sequential, it also
  reads sources one at a time, so it's slower too.
- **Built as a graph**: a small three-node graph with state flowing cleanly between nodes.
  - A researcher node fans out to multiple sources, gathering in parallel, and returns only
    structured notes (not raw pages).
  - A writer node receives only the clean notes (never sees the messy raw web pages) and
    produces the brief.
  - A reviewer node checks the brief in a FRESH context, seeing only the brief and the
    acceptance criteria -- not disqualified, it sends it back to the writer node if it fails.
  - Benefits observed: contexts stay separate and clean; the writer is never drowned in search
    noise; the review is a genuine independent check rather than self-certification; parallel
    gathering makes it faster; and the whole thing is a clear, readable path rather than
    something you have to reverse-engineer from a long transcript.
- Honest costs of the graph approach: you now maintain three prompts instead of one, you must
  design the state structure between nodes, and you take on a new set of failure modes.
- The verdict on when it's worth it: for a brief that runs every single day, the extra overhead
  buys real, repeated quality improvement -- worth it. For a task that only runs once, the same
  overhead is pure tax with no repeated payoff. This tradeoff -- repeated value versus one-off
  cost -- is presented as the entire decision of whether to upgrade from a loop to a graph.

## Output

Write the wiki page to:

```
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/wiki/05-worked-example-loop-vs-graph.md
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
2. `bd close <own-task-id> --reason "wiki page 05 extracted"`
