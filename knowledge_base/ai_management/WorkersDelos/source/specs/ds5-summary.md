# DS5 — rewrite summary.md for the full 36-page site

## Problem

`summary.md` in `/Users/sergii/.ai/knowledge/research/WorkersDelos/` summarizes
only the homepage. After DS1–DS4 the folder covers the whole Delos site
(36 wiki pages + fresh digest). This bead rewrites the summary from the wiki pages.

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
Read ONLY `wiki/01-*.md` … `wiki/35-*.md`
(never `source/`, the topic files, or the web).

Rewrite `summary.md`:

- Keep the `#` title heading; adjust only if it says homepage-only.
- Metadata line: `**Article:** [Delos site](https://delos.so/) — Delos company +
  product + worker-profile pages (35 pages, fetched 2026-09-16)`.
- Sections in order: `## Human Readable TL;DR` (3–5 plain sentences with
  analogies), `## TL;DR`, then `---`, then `## Problem & Motivation`,
  `## Main Original Ideas` (numbered, with bold names), `## Key Findings`,
  `## Suggestions & Future Directions`, `## Authors & Institutions`.
- Flowing paragraphs throughout, never one-sentence-per-line. Keep under
  300 lines. Cover product (AI workers, office suite), pricing, integrations,
  security/GDPR, use cases/solutions, and the worker roster — not just the homepage.

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/WorkersDelos
test -s summary.md; wc -l summary.md; grep -c "^## " summary.md
```

File non-empty, under 300 lines, with all 7 `##` sections present.

## DoD

1. `summary.md` rewritten as above.
2. Tests above green.
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY `summary.md`. Do not touch `wiki/`, `digest.md`, `index.md`,
  `questions.md`, `explainer.md`, `critical_thinking.md`, `source/`.
- cwd: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
