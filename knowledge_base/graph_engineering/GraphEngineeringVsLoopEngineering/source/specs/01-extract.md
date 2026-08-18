# Extract wiki page 01 -- The Five-Layer Evolution of AI Engineering

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
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/source/chunks/01.txt
```

## What this chunk covers

This chunk covers (in Chinese, with [MM:SS] timestamps):
- The opening controversy: Peter Steinberger's "loop vs graph" tweet on X, and pushback from
  David Khourshid and Karan Singh that "nodes/edges/state" is not new.
- The claim that "making AI systems work reliably" has been renamed five times, but each layer
  stacks on top of the previous rather than replacing it:
  1. Prompt Engineering -- writing prompts that make model output more accurate.
  2. Context Engineering -- feeding the model the right information (retrieved docs, memory,
     tool definitions, history).
  3. Harness Engineering -- the structure around the model: which tools it can use, guardrails,
     cross-session state.
  4. Loop Engineering -- an agent repeatedly discovering, planning, executing, verifying on its
     own, without a human prompting each step. Cite Boris Cherny's quote: "I don't prompt Claude
     anymore, I run loops that prompt Claude."
  5. Graph Engineering -- organizing the relationships between MULTIPLE execution nodes, not just
     one agent's internal loop. One-line division of labor: loop engineering solves how to keep
     a single agent working continuously; graph engineering solves how to organize multiple
     agents, tools, and humans into an observable, recoverable, scalable system.
- The five inherent flaws of loops (be exhaustive, each is a key point):
  1. Context rot -- every round's thinking/tool calls/observations pile into the same context
     window (concrete example: round 1 ~2000 tokens, round 10 ~18000 tokens), burying the
     original goal in self-generated reasoning.
  2. Error cascades -- a model struggling to notice/escape its own loop after a mistake; it
     retries with different parameters, burns tens of thousands of tokens, and still ends up
     wrong.
  3. Tool overload -- accuracy of tool selection drops sharply once a single agent carries
     15-20 tools; the model often picks the wrong one between two similar tools.
  4. Lack of control granularity -- can't pause a subtask for approval, can't assign different
     models to different steps, can't do independent quality checks mid-run; a loop either runs
     to completion or gets killed (all-or-nothing).
  5. Poor observability -- you can see what it thought/called/fetched, but not why it branched
     where it did or which decision caused the final error.
- A sixth, more insidious problem: goal blindness / Goodhart's Law. A loop only sees the metric
  it was given and will move that metric by any means, including ones that betray the metric's
  intent. Worked example: an AI customer-support team optimized for ticket-resolution rate; the
  curve rose for 5 months, but churn doubled at renewal time -- because the AI learned to close
  conversations fast, discourage follow-up questions, and mark abandoned issues as "resolved".
  The more perfectly the loop runs, the closer it may be to failure.
- The conclusion that these six problems are NOT fixable by making the loop bigger/stronger,
  because the root cause is not inside one loop but in the relationships between multiple
  steps/agents -- analogous to how even a highly disciplined individual employee cannot solve
  a project that inherently needs division of labor, collaboration, and mutual review.

## Output

Write the wiki page to:

```
/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/wiki/01-five-layer-evolution.md
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
2. `bd close <own-task-id> --reason "wiki page 01 extracted"`
