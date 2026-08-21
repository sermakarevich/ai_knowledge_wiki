# Task: Extract wiki page 01 — Motivation and Related Work (AgentGL paper)

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this
task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention
reference" — the format contract below is the only convention you need.

## Input

Read this file in full: `/Users/sergii/.kb/papers/ArxivAgentGL/source/chunks/01.txt`

It contains the Abstract, Introduction, and Related Work sections of the paper "AgentGL: Towards
Agentic Graph Learning with LLMs via Reinforcement Learning" (Sun et al., 2026).

## Output

Write the result to: `/Users/sergii/.kb/papers/ArxivAgentGL/wiki/01-motivation-and-related-work.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Motivation and Related Work

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <complete claim>
- ... (5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

## <subsection mirroring the source, e.g. "The Problem">

<full detail prose, hierarchical, covering the WHOLE chunk — including the ending, not just
the opening>

## <next subsection, e.g. "Why Existing Approaches Fall Short">

...

## <next subsection, e.g. "Related Work">

...

**Covers:** Abstract, Introduction, Related Work (source pages 1-3)
```

Requirements:
- The "Key points" bullets must stand alone: someone reading only them should get the chapter's
  substance. Include the paper's central question, the two challenges (C1 topology-aware navigation,
  C2 long-horizon policy optimization), and how AgentGL is positioned against GraphLLMs and GraphRAG.
- Cover the two related-work contrasts explicitly: GraphLLMs (GraphGPT, GraphICL) rely on static graph
  context; GraphRAG systems build costly reconstructed knowledge graphs that don't preserve native TAG
  topology. Name the specific baselines mentioned (GraphCoT, GraphSearch) and how AgentGL differs.
  This chunk has NO figures — do not fabricate any `![...]` image references.
- No meta-commentary about being an AI or about this task. Output ONLY the markdown page content.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the close command below.

## Done

After writing the file, close your own bead:

```
bd close <own-bead-id> --reason "chunk 01 extracted"
```
