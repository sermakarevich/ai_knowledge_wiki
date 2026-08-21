# Extract wiki page 04 — Related Work and Appendix Details

## Problem
We are building an LLM-wiki knowledge-base entry for the paper "MemGraphRAG: Memory-based
Multi-Agent System for Graph Retrieval-Augmented Generation" (arXiv 2606.00610). Your job is
to write ONE wiki page covering one chunk of the paper's text.

## Input (read ONLY these files — nothing else)
- Chunk text: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/source/chunks/04.txt`
  (covers: Appendix B Related Work, and Appendices C-F — additional methodology details on
  conflict detection/resolution agents and graph propagation/initialization, dataset details,
  implementation details, and the two agent prompt figures)
- Figure description 1: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/images/page18_fig7-description.md`
  (for Figure 7: the prompt used for the Conflict Detection Agent)
- Figure description 2: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/images/page19_fig8-description.md`
  (for Figure 8: the prompt used for the Conflict Resolution Agent)

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling
wiki pages "for style/convention reference" — the format contract below is the only
convention needed. Context is tight on this model — read ONLY the files listed above.

## Fix — write the output file

Output path: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/04-related-work-and-appendix.md`

If this file already exists (a retry), overwrite it completely with a fresh write covering
the whole chunk.

Write the page following this EXACT structure (a page is itself a ladder — shallow at the
top, deep below):

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Related Work and Appendix Details

**In one sentence:** <the chapter's whole argument, in one sentence — how MemGraphRAG
relates to prior GraphRAG/RAG work, and what the appendix reveals about the mechanics of the
conflict-handling agents and experimental setup>

## Key points

- <5-8 bullets, each a COMPLETE claim with real content (numbers, mechanisms, conclusions) —
  not "discusses X". These must stand alone as the chapter at medium depth.>

---

## Related Work
<summarize how the paper positions itself vs. prior RAG and GraphRAG methods>

## Appendix: Conflict Detection and Resolution Agents
### Detection Agent
### Resolution Agent

## Appendix: Graph Propagation and Node Initialization
### Entity Node Initialization via Facts
### Type Node Initialization via Schemas
### Passage Initialization with Information Density

## Appendix: Datasets and Implementation Details

<Full detail: hierarchical summary of the chunk's content, not flat prose. Use tables and
exact numbers/settings where the source gives them. Embed the two prompt figures inline,
right next to the passage that discusses each agent:>

![Figure 7: The prompt used for Conflict Detection Agent](images/page18_fig7.png)

<one or two sentences paraphrasing the figure description file content, placed near the
"Detection Agent" discussion>

![Figure 8: The prompt used for Conflict Resolution Agent](images/page19_fig8.png)

<one or two sentences paraphrasing the figure description file content, placed near the
"Resolution Agent" discussion>

**Covers:** Appendix B, C, D, E, F of arXiv 2606.00610
```

Notes:
- The image markdown paths above are correct as written — do not change them.
- Cover the WHOLE chunk, including the dataset/implementation details near the end — do not
  stop after the Related Work section.
- No meta-commentary about being an AI or about this task. Write only the wiki page content.

## Tests
- File exists at the output path and is non-trivial (> 40 lines).
- Both `![...]( images/...)` figure embeds are present verbatim as written above.

## DoD
1. Output file written.
2. `bd close <own-id> --reason "chunk 04 extracted"` — never exit rc=0 without closing.

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run any fleet commands other than `bd close`.
- On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and
  write directly.
