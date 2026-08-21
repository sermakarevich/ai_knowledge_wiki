# Extract task — SAGE paper, chunk 01

Topic: Introduction, Related Work, Preliminary
Source paper: SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware
Associative Memory (Wang et al., 2026), https://arxiv.org/abs/2605.12061

## Input

Read exactly this file — it is a plain-text excerpt of the paper (source lines 1-235):

`/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/source/chunks/01.txt`

## Figure description file(s) for this chunk

- Image: `/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/wiki/images/01-fig1-challenges.png` (embed as `![...](images/01-fig1-challenges.png)`)
- Vision description (read this to write the caption/discussion): `/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/wiki/images/01-fig1-challenges-description.md`

## Output

Write the wiki page to:

`/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/wiki/01-challenges-and-related-work.md`

## Wiki page format contract (follow exactly)

The output file is one page of an LLM-wiki. Structure it exactly like this:

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# <Topic Title>

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete-claim bullet 1, with real numbers/mechanisms/conclusions>
- <complete-claim bullet 2>
- ... (5-8 bullets total, each a standalone claim, not a topic label)

---

<Full detail below, mirroring the source's internal structure with ## subsections.
Use tables for numeric results. Quote exact numbers, prompts, or equations where
the source gives them. Embed any named figure exactly where it is discussed:
![<caption>](images/<file>.png) using the image file(s) listed below, if any.>

**Covers:** <line/section range given below>
```

Rules:
- The page must cover the WHOLE chunk given to you, including the last topic near the end of the chunk — do not stop after the opening subsection.
- Write for a technical reader already familiar with RAG / knowledge graphs / RL — no need to re-explain basics, but do explain this paper's own notation and mechanisms.
- Do not invent numbers, citations, or claims not present in the chunk text.
- If the chunk is mostly proofs/derivations, summarize the setup, the key lemma/proposition statements, and their informal implication — do not transcribe full equation derivations line by line, but do keep the final stated bounds/results verbatim.


## If this is a retry

If the output file already exists (a retry), overwrite it completely — do not
try to merge with the previous attempt.

Context is tight on this worker model: read ONLY the chunk file (and the figure
description file(s), if listed) referenced below — nothing else. Do NOT read this
task's own fleet artifacts/log/event files, and do NOT read sibling wiki pages for
style reference; the format contract above is the only convention you need. On a
retry, do not try to diagnose the prior failure by reading logs — just re-read the
chunk and write the page directly.


## Definition of done

1. Write the full page to the output path below.
2. `bd close <own-id> --reason "chunk 01 extracted"`

Scope: touch ONLY the one output file listed below. Do not run any fleet/bd
commands other than the final `bd close`. No git commands — this repo auto-syncs.

