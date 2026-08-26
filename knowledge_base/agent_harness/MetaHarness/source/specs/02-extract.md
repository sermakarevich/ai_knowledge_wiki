# Task: write wiki page 02 for the Meta-Harness paper

Context is tight on this model — read ONLY the one input file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files, and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full: `/Users/sergii/.kb/papers/MetaHarness/source/chunks/02.txt`

It contains Section 3 ("Meta-Harness: A Harness for Optimizing Harnesses") of the paper "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv 2603.28052). This section describes the method itself: the objective, the search loop (agentic proposer with filesystem access to all prior candidates' code/scores/traces), Algorithm 1 (the outer loop pseudocode), and the practical implementation (each harness as a single-file Python program).

There are no figures assigned to this chunk.

## Output

Write the file: `/Users/sergii/.kb/papers/MetaHarness/wiki/02-method.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Meta-Harness Method

**In one sentence:** <the whole method in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers, mechanisms, design choices) — not "discusses X">

---

## Objective

<what a "harness" is formally: a stateful program wrapping an LLM controlling what to store/retrieve/present>

## The Meta-Harness search loop

<how the agentic proposer works: reads filesystem of all prior candidates' source code, scores, execution traces; what it writes; how this differs from typical text-optimizer feedback compression>

## Algorithm 1 (outer loop)

<transcribe the pseudocode/steps of Algorithm 1 as a numbered list or code block, verbatim as closely as possible>

## Advantages of code-space search

<why searching in code space beats other representations, per the source>

## Practical implementation

<concrete details: single-file Python program per harness, and any other implementation specifics given>

**Covers:** Section 3 (Meta-Harness: A Harness for Optimizing Harnesses)
```

Rules:
- The page must be self-contained (readable without other wiki pages).
- No line limit — be thorough. Include exact numbers, any hyperparameters or design constants mentioned, and citation markers (e.g. "[47]") as they appear.
- Use Obsidian `[[wikilink]]` syntax only for the backlink line shown above.

## Done

Write the output file, then run: `bd close <own-id> --reason "chunk 02 extracted"`

Scope: touch ONLY the one output file listed above. Do not run any fleet commands other than the `bd close` above.
