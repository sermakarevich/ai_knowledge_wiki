# Task: Extract wiki page 01 — Motivation and Related Work — GraphScout paper

You are writing ONE page of an LLM-wiki for the paper "GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning" (Ying et al., 2026).

**Context is tight on this model — read ONLY the two files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input files (read exactly these, in full)

1. `/Users/sergii/.kb/papers/ArxivGraphScout/source/chunks/01.txt` — the source text for this page (covers the paper's title/authors/abstract, Introduction, and Section 2 Related Work — LLM for Graph Reasoning, Augmenting LLMs with Knowledge Graphs).
2. `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/images/descriptions.md` — read only the entry titled `fig1-motivation-comparison.png (Figure 1)`; ignore the other entries in that file.

## Output file

Write to: `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/01-motivation-and-related-work.md`

**If this file already exists (a retry), overwrite it completely.**

## Required page format (fill this in from the chunk text — do not invent facts not in the chunk)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Motivation and Related Work

**In one sentence:** <one sentence capturing the paper's core motivation: why existing GraphRAG methods are limited and what GraphScout proposes instead>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers, mechanisms, named methods) — not "discusses related work">

---

## The problem with existing GraphRAG

<hierarchical detail from the Introduction: the RAG background, the two classes of prior GraphRAG methods (passive retrieval-driven vs active traversal-based), their specific limitations (manually-designed/limited tool sets, LLMs lacking intrinsic priors for graph exploration), and the named examples/results (GraphCoT, PolyG) that illustrate the limitation>

## GraphScout's proposed shift

<the paper's claimed contribution at a high level: training-centric framework, Agentic Graph Exploration Tools (Code Interpreter + Node Retriever), Graph Quizzer, Graph Solver — as introduced in the Introduction, before the Method section goes deeper>

## Related Work

### LLM for Graph Reasoning
<summarize the two paradigms: LLMs as feature extractors (LLM-GNN cascade) vs LLMs as final predictors, citing what the chunk says>

### Augmenting LLMs with Knowledge Graphs
<summarize passive retrieval-driven vs active traversal-based GraphRAG, and the named prior methods mentioned (GraphCoT, PolyG, GraphCounselor, etc.) and how GraphScout positions itself against them>

![Figure 1: Qwen3-4B-Instruct with GraphScout vs leading-LLM GraphRAG baselines on Healthcare](images/fig1-motivation-comparison.png)

<one or two sentences captioning what Figure 1 shows, using the description file — GraphScout-4B scores, initial vs trained, and the baseline comparison numbers>

**Covers:** Title/Abstract, Section 1 Introduction, Section 2 Related Work (2.1, 2.2)
```

## Rules

- Use exact numbers, names, and citations as they appear in the chunk text (e.g. "16.7%", "Qwen3-4B", "GraphCoT [24]", "PolyG [34]") — do not round or paraphrase away specifics.
- The `## Key points` block must stand alone as the chapter at medium depth — write real claims, not topic labels.
- Do not fabricate content beyond what's in the chunk text and the one figure description you read.
- No git commands. No fleet commands other than the close command below.
- Touch ONLY the one output file listed above.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 01 extracted"`
