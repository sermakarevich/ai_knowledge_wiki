# Extract wiki page 03: Hype Check and Starting Checklist

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/source/chunks/03.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/wiki/03-hype-check-and-checklist.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Is Graph Engineering Just Slop?

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the skeptics quoted and their specific critiques (@RhysSullivan on the content-farm
gold-rush, @DavidKPiano/XState creator on directed graphs and state machines being decades-old,
@PawelHuryn on naming the mechanism instead of the substance, @NathanFlurry on A2A/enterprise
prior art predating the term); the article's concession that all of it is true (mechanics are
old, much content is slop, the phrase is optional); the separating move (the escalation from one
loop to coordinated specialized nodes with shared state IS real and IS a distinct design skill,
whether or not you call it "graph engineering"); the three-question filter distinguishing the
real escalation from the hype around its name; the starting checklist (try to keep it a loop;
name nodes only if real specialties; draw edges before coding; design shared state explicitly
and decide who can write to it; give the reviewer node teeth — separate read-only verifier;
isolate failure so one node's failure doesn't corrupt shared state; pick a framework instead of
hand-rolling; set a spend cap); the win condition ("every node does work a loop couldn't, and
you could explain the whole graph in one breath"); the FAQ answers (what is graph engineering,
is it hype, what is an agent org chart); and the sources list (X posts and framework docs
cited).>

**Covers:** Skeptic critiques and the article's concession; the real-escalation-vs-hype filter;
the 8-item starting checklist; FAQ; cited sources (source chunk 03)
```

Key points must be complete standalone claims (not topic labels) — someone reading only the key
points should have the chunk's substance. Use precise wording for the skeptics' specific
critiques (attribute each to its named source) and the 8 checklist items, since those are the
chunk's most specific and citable content.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 03 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
