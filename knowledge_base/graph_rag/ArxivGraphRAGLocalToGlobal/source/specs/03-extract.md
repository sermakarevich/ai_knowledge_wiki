# Task: Extract wiki page 03 — Experimental Setup and Results

## Context is tight on this model

Read ONLY the two input files listed below. Nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

- Source text chunk: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/chunks/03.txt`
  (covers: Section 4 Analysis — 4.1 Experiment 1 datasets/conditions/configuration, 4.2 Experiment 2 claim-based validation via Claimify; Section 5 Results — 5.1 Experiment 1 results including Figure 2 win-rate percentages, 5.2 Experiment 2 results)
- Figure description (read and use when writing about Figure 2): `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/02-winrates-description.md`
- The figure image itself already exists at `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/02-winrates-figure2.png` — do not create or move it, just reference it by relative path `images/02-winrates-figure2.png` in your embed.

## Output

Write to: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/03-experimental-setup-and-results.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup and Results

**In one sentence:** <the whole finding in one sentence — GraphRAG's global approaches (C0-C3) win over vector RAG on comprehensiveness and diversity, validated two ways>

## Key points

- <5-8 bullets with exact numbers: dataset sizes (podcast ~1M tokens/1669 chunks, news ~1.7M tokens/3197 chunks), the 6 conditions (C0-C3, TS, SS), win-rate percentages and p-values, graph sizes (nodes/edges), claim counts from Experiment 2, indexing time>

---

## Experiment 1: Setup (Section 4.1)

### Datasets
<podcast transcripts and news articles datasets, exact chunk counts and token counts>

### Conditions
<the 6 conditions C0, C1, C2, C3, TS, SS with their exact definitions>

### Configuration
<context window size, indexing time, hardware, Leiden/graspologic library>

## Experiment 2: Claim-Based Validation (Section 4.2)

<Claimify method, comprehensiveness and diversity metric definitions, clustering approach>

## Results: Experiment 1 (Section 5.1)

<graph sizes (nodes/edges per dataset), global approaches vs vector RAG findings with exact win-rate percentages and p-values, empowerment mixed results, directness findings. Embed the figure:>

![Head-to-head win rate percentages across conditions](images/02-winrates-figure2.png)

<describe the figure's content and trends in prose, integrated — do not just paste the description file verbatim>

## Results: Experiment 2 (Section 5.2)

<claim-based comprehensiveness/diversity results, how they corroborate or complicate Experiment 1's findings>

---

**Covers:** Section 4 (Analysis: 4.1 Experiment 1, 4.2 Experiment 2), Section 5 (Results: 5.1, 5.2), Figure 2.
```

## Rules

- Cover the WHOLE chunk — verify Experiment 2 and its results near the end of the chunk got real coverage, not just Experiment 1 at the top.
- No meta-commentary about your own process. No "as an AI" disclaimers. Just the page content.
- Preserve EXACT numbers, percentages, p-values, node/edge counts as they appear in the source — this is a results page, precision matters most here.
- The figure must actually be embedded with the markdown image syntax shown above (relative path `images/02-winrates-figure2.png`), not just mentioned by name.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than closing your own bead.

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/03-experimental-setup-and-results.md` written per the format contract above, covering the entire chunk.
2. `bd close <own-id> --reason "chunk 03 extracted"`
