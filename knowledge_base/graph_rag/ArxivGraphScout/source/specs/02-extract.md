# Task: Extract wiki page 02 — The GraphScout Method — GraphScout paper

You are writing ONE page of an LLM-wiki for the paper "GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning" (Ying et al., 2026).

**Context is tight on this model — read ONLY the two files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input files (read exactly these, in full)

1. `/Users/sergii/.kb/papers/ArxivGraphScout/source/chunks/02.txt` — the source text for this page (covers Section 3.1 Preliminary, and Section 3 "GraphScout" — Agentic Graph Exploration Tools, Graph Quizzer, Graph Solver, and the GRPO-based training objective).
2. `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/images/descriptions.md` — read only the entry titled `fig2-graphscout-architecture.png (Figure 2)`; ignore the other entries in that file.

## Output file

Write to: `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/02-graphscout-method.md`

**If this file already exists (a retry), overwrite it completely.**

## Required page format (fill this in from the chunk text — do not invent facts not in the chunk)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The GraphScout Method

**In one sentence:** <the chapter's whole argument: how GraphScout's three components — Agentic Graph Exploration Tools, Graph Quizzer, Graph Solver — combine to give LLMs intrinsic graph-exploration ability via post-training>

## Key points

- <5-8 bullets, each a complete standalone claim with real content — e.g. the exact tool set, what the Graph Quizzer produces, how the Graph Solver is trained, the reward components, the RL algorithm used>

---

## Preliminaries

<knowledge-graph formalism from Section 3.1: how a KG is defined (entities/relations/triples), and any task formalization given before the method itself>

## Agentic Graph Exploration Tools

<the Code Interpreter and Node Retriever tools: what each does, how they let the model interact with the knowledge graph more flexibly than fixed primitives>

## Graph Quizzer

<how the "senior scout" explores the graph environment to synthesize question-answer pairs and their evidence/clue-node traversal path; task specification, exploration initialization, exploration process, stopping condition — as described in the chunk>

## Graph Solver

<how the "junior scout" (small-parameter LLM) is post-trained as a multi-turn decision policy for agentic graph interaction; the reward design (answer correctness reward + auxiliary clue-based/evidence reward) and why sparse feedback motivates the auxiliary reward>

## Training objective (GRPO)

<the reinforcement-learning setup: Group Relative Policy Optimization, the group-relative advantage formulation, the clipped surrogate objective, KL regularization to the reference policy — with exact terms/variable names as they appear (do not attempt to re-typeset every equation verbatim if formatting breaks, but preserve the named quantities and their role)>

![Figure 2: Overview of the GraphScout framework](images/fig2-graphscout-architecture.png)

<2-3 sentences captioning what Figure 2 shows using the description file — the three panels (a) tools, (b) Graph Quizzer, (c) Graph Solver, and how they connect>

**Covers:** Section 3.1 Preliminary, Section 3 GraphScout (method design and training objective)
```

## Rules

- Use exact terminology from the chunk (e.g. "Agentic Graph Exploration Tools", "Graph Quizzer", "Graph Solver", "GRPO", "clue-based reward") — these are the paper's own named components, keep them exact.
- The `## Key points` block must stand alone as the chapter at medium depth — write real claims, not topic labels.
- Do not fabricate content beyond what's in the chunk text and the one figure description you read.
- No git commands. No fleet commands other than the close command below.
- Touch ONLY the one output file listed above.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 02 extracted"`
