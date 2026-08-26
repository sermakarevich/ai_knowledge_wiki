# Task: write wiki page 01 for the Meta-Harness paper

Context is tight on this model — read ONLY the one input file listed below (plus the two figure-description files listed), nothing else. Do NOT read this task's own fleet artifacts/log/event files, and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full: `/Users/sergii/.kb/papers/MetaHarness/source/chunks/01.txt`

It contains the Abstract, Introduction, and Related Work sections of the paper "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv 2603.28052).

Also read these two figure-description files (vision-model descriptions of the actual figure images) and use them to write the parts of the page that discuss the figures:

- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig1-teaser-description.md` — describes `fig1-teaser.png`, the paper's headline results teaser (Figure 1)
- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig2-search-loop-description.md` — describes `fig2-search-loop.png`, the Meta-Harness search-loop schematic (Figure 2)

## Output

Write the file: `/Users/sergii/.kb/papers/MetaHarness/wiki/01-motivation-and-related-work.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Motivation and Related Work

**In one sentence:** <the whole argument of this section in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers, mechanisms, conclusions) — not "discusses X">

---

## <subsection mirroring the source, e.g. "The harness-engineering problem">

<full detail prose, hierarchical ## subsections mirroring the source's own structure (Introduction, then Related Work sub-topics: external memory / adaptive access, executable code search, text optimization methods). Include exact numbers, claims, and citations as they appear (e.g. "[47]"). Where the section discusses Figure 1 or Figure 2, embed the image and describe it using the figure-description file content, e.g.:>

![Meta-Harness search loop](images/fig2-search-loop.png)

<description of what the figure shows, drawn from the description file>

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work)
```

Rules:
- The page must be self-contained (readable without other wiki pages).
- No line limit — be thorough, include all relevant details, numbers, and citation markers.
- Embed both figures (`![...](images/fig1-teaser.png)` and `![...](images/fig2-search-loop.png)`) at the point in the text where they are discussed, using the vision descriptions to write the caption/description text.
- Use Obsidian `[[wikilink]]` syntax only for the backlink line shown above — no other wikilinks needed on this page.

## Done

Write the output file, then run: `bd close <own-id> --reason "chunk 01 extracted"`

Scope: touch ONLY the one output file listed above. Do not run any fleet commands other than the `bd close` above.
