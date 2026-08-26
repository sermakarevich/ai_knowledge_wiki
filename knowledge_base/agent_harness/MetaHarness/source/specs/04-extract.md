# Task: write wiki page 04 for the Meta-Harness paper

Context is tight on this model — read ONLY the one input file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files, and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full: `/Users/sergii/.kb/papers/MetaHarness/source/chunks/04.txt`

It contains Section 4.3 ("Evaluating Agentic Coding Harnesses on TerminalBench-2") and Section 5 ("Discussion") of the paper "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv 2603.28052). This covers: the TerminalBench-2 benchmark, comparison against hand-engineered baselines (e.g. Terminus-KIRA, Claude Code, Mini-SWE-Agent, Goose), pass-rate results, a qualitative discussion of why the discovered harness works, and the paper's closing discussion of implications and limitations.

There are no figures assigned to this chunk.

## Output

Write the file: `/Users/sergii/.kb/papers/MetaHarness/wiki/04-coding-experiments-and-discussion.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Agentic Coding Experiments and Discussion

**In one sentence:** <the whole argument of this section in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with exact numbers/results — not "discusses X">

---

## TerminalBench-2 setup

<benchmark description, baseline harnesses compared against>

## Results

<exact pass-rate numbers per method/harness, in a markdown table if the source gives a table; where Meta-Harness ranks>

## Qualitative behavior of the proposer

<why the discovered harness works, per the source's own explanation>

## Discussion

<the paper's Section 5 discussion: implications, limitations, what this means for automated harness engineering going forward>

**Covers:** Section 4.3 (Evaluating Agentic Coding Harnesses on TerminalBench-2), Section 5 (Discussion)
```

Rules:
- The page must be self-contained (readable without other wiki pages).
- No line limit — be thorough. Preserve exact numbers (pass rates, rankings) as given in the chunk; use a markdown table for the results comparison if the source presents one.
- Use Obsidian `[[wikilink]]` syntax only for the backlink line shown above.

## Done

Write the output file, then run: `bd close <own-id> --reason "chunk 04 extracted"`

Scope: touch ONLY the one output file listed above. Do not run any fleet commands other than the `bd close` above.
