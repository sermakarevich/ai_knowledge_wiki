# Extract wiki page 03 -- Graph Topologies and When to Use Them

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
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/source/chunks/03.txt
```

## What this chunk covers

This chunk covers (in Chinese, with [MM:SS] timestamps):
- The claim that recognizing a handful of proven topologies is more useful than memorizing
  vocabulary. Three core shapes plus two more from Anthropic:
  1. **Diamond / fan-out-fan-in** -- the highest-frequency shape: split work into parallel
     branches, then merge. Worked example from the video's own production: one agent reads the
     original X post, one translates the official docs, one reviews community discussion --
     three branches run in parallel with no one waiting on another (fan-out); results come back
     and are deduplicated/classified by code before going to a final drafting agent (fan-in).
  2. **Orchestrator-Workers** -- a supervisor agent dispatches tasks to specialized workers
     (research, coding, review, etc.) and handles planning + aggregation itself. This is the
     core pattern behind Anthropic's research system: the lead agent analyzes the problem, sets
     strategy, and spawns subagents that act like intelligent filters gathering information in
     parallel, then reports back for the lead agent to synthesize into a final answer.
  3. **Pipeline** -- task broken into a fixed sequence of steps, each processing the previous
     step's output, with optional programmatic checkpoints in between to keep the process on
     track. Good for tasks that decompose cleanly into fixed subtasks; trades latency for higher
     accuracy because each call becomes a simpler task.
  - These three are not mutually exclusive framework choices -- they are composable, nestable
    building blocks. Real production systems often nest a diamond inside an orchestrator
    pattern, and a pipeline inside the diamond.
  - Two more shapes from Anthropic's "Building Effective Agents": **Routing** (classify the
    input first, then direct it to specialized downstream handling -- good when input types
    vary enough that one prompt optimized for one type would hurt another) and
    **Evaluator-Optimizer** (one node generates, another evaluates/scores, loop until it meets
    the bar -- good when there's a clear evaluation standard and iteration demonstrably
    improves quality).
  - Anthropic's simplicity-first stance: find the simplest solution first, only add complexity
    when truly needed. Many applications just need a single call plus retrieval -- no agent, let
    alone a graph, required.
  - A pointed caveat about frameworks like LangGraph, Bedrock, and Rivet: they simplify calling
    conventions, tool parsing, and chaining calls, which helps you start fast -- but they also
    add a layer of abstraction that can hide the underlying prompts and responses, making
    debugging harder, and can tempt you to over-complicate a system that a simple solution would
    have solved. Recommendation: start directly with the raw model API (many patterns are a few
    lines of code), and if you do use a framework, make sure you understand the code underneath
    it.
  - Closing point for this section: a graph's real leverage is NOT how many agents it packs in,
    but how much certainty/determinism you can build around the result.

## Output

Write the wiki page to:

```
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/wiki/03-graph-topologies.md
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
2. `bd close <own-task-id> --reason "wiki page 03 extracted"`
