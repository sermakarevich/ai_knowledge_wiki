# Task: write wiki page 01 for ArxivGoAgentTopologyGeneration

Context is tight on this model — read ONLY the two files listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

**Input (read exactly these):**
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/source/chunks/01.txt` — extracted paper text: title/authors/abstract, Section 1 Introduction, Section 2 Preliminaries (2.1 Problem Formulation, 2.2 Information Bottleneck)
- `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/images/01-description.md` — a vision-model description of Figure 1 (node-centric vs. group-centric paradigm comparison)

**Output:** `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/01-problem-and-motivation.md`

If this file already exists (a retry), overwrite it completely.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Problem and Motivation

**In one sentence:** <the whole argument of this section, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers, mechanisms, definitions) — not "discusses X". A reader who reads only these bullets should have the substance of this section.>

---

## <## subsections mirroring the source's own structure, e.g.:>
## Node-centric vs. group-centric paradigms
## Contributions
## Problem formulation
## Information bottleneck background

<Full detail under each subsection: exact definitions, notation, numbers, the paper's stated contributions as a list, and how the information bottleneck concept is used. Preserve technical precision — this is an ML paper, keep math notation as written in the source (e.g. z_Q, X, K, IB terms).>

Embed the figure inline at the point where it is discussed:
![Node-centric vs. group-centric graph generation paradigms](images/fig1-node-vs-group-paradigm.png)

<Then a paragraph describing what the figure shows, based on the description file — do not just repeat the description verbatim, integrate it into the prose.>

**Covers:** Title, Abstract, Section 1 (Introduction), Section 2 (Preliminaries: 2.1 Problem Formulation, 2.2 Information Bottleneck)
```

## Rules
- Cover the WHOLE chunk, including the end (Section 2.2 Information Bottleneck) — do not stop after the introduction.
- No meta-commentary, no "as an AI", no repeating these instructions in the output.
- Scope: touch ONLY the one output file `wiki/01-problem-and-motivation.md`. Do not run any fleet commands other than the final `bd close`.
- No git commands — this repo auto-syncs.

## DoD
1. `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/wiki/01-problem-and-motivation.md` written per the contract above.
2. `bd close <own-id> --reason "chunk 01 extracted"`
