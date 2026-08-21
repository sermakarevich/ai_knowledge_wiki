# Task: write wiki page 02 — Experimental Design and the Three Ablation Studies

## Problem
We are building an LLM-wiki summary of an academic paper. This task covers one section of the paper: the Experimental Design, including its three ablation studies (Isolation, Cited Evidence Ablation, Visited-but-uncited entities Ablation), and two figures.

## Fix
1. Read ONLY these files (nothing else):
   - `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/source/chunks/02.txt` (the section text)
   - `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/images/01-description.md` (description of Figure 1)
   - `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/images/02-description.md` (description of Figure 2)
2. Write the wiki page to: `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/02-experimental-design-and-studies.md`
3. If that file already exists (this is a retry), overwrite it completely with fresh content.

The wiki page MUST follow this exact structure:

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Design and the Three Ablation Studies

**In one sentence:** <the section's whole argument in one sentence>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5, up to 8 total>

---

## The three agentic GraphRAG systems tested

<Describe the three systems (Agentic GraphRAG, Evidence-First Agentic GraphRAG, Visited-Only-First
Agentic GraphRAG) using the chunk text AND the Figure 1 description. Embed the figure here:>

![Representation of the three agentic graphRAG systems tested](images/fig1-agentic-graphrag-systems.png)

## Study 1 — Isolation of Evidence

<full detail from the chunk>

## Study 2 — Cited Evidence Ablation

<full detail from the chunk>

## Study 3 — Visited-but-uncited entities Ablation

<full detail from the chunk. Embed the figure here:>

![Example of the three graph ablations on a synthetic subgraph](images/fig2-graph-ablations.png)

---

**Covers:** Section 2 (Experimental Design) and Studies 1-3, source/full.txt lines 74-239
```

Rules:
- The `## Key points` bullets must be complete, standalone claims, not topic labels.
- Cover the ENTIRE chunk, including all three studies.
- Use the figure descriptions to write accurate captions/explanations, but the images themselves are already embedded via the markdown paths above — do not change those paths.
- Do not fabricate numbers or claims not present in the chunk text or the figure descriptions.
- Do not read any other file — not this task's own fleet artifacts/log/event files, not sibling wiki pages, not `PLAN_AND_STATUS.md`/`KNOWLEDGE.md`. Context is tight on this model; only the 3 files listed above are needed.

## Tests
- `test -s /Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/02-experimental-design-and-studies.md`
- The file contains `**In one sentence:**`, `## Key points`, and both image references `fig1-agentic-graphrag-systems.png` and `fig2-graph-ablations.png`

## DoD
1. `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/02-experimental-design-and-studies.md` written per the structure above.
2. No git commands — this repo auto-syncs.
3. `bd close <own-id> --reason "chunk 02 extracted"` — never exit rc=0 without closing.

## Scope & constraints
- Touch ONLY `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/02-experimental-design-and-studies.md`.
- Do not run fleet commands other than `bd close`.
- cwd: /Users/sergii/.kb
