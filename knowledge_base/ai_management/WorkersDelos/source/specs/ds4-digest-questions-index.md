# DS4 — rewrite digest.md, questions.md, index.md wiki table (all 36 pages)

## Problem

`digest.md`, `questions.md`, and `index.md` in
`/Users/sergii/.ai/knowledge/research/WorkersDelos/` cover only the homepage
(`wiki/01`). After DS1–DS3 the folder holds `wiki/01`–`wiki/35` and the derived
files are stale. This bead refreshes the three mechanical files (DS5 rewrites
`summary.md`, DS6 `explainer.md` + `critical_thinking.md`).

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
Read ONLY `wiki/01-*.md` … `wiki/35-*.md`
(never `source/`, the topic files, or the web).

1. Rewrite `digest.md`:
   - Backlink line: `> [[index|Wiki]] | [[summary|Summary]]`
   - Heading: keep the existing title line, extended to the whole site if needed.
   - One section per wiki page in order: `## N. [[wiki/NN-slug|Title]]` with that
     page's `**In one sentence:**` line and its `## Key points` bullets copied
     VERBATIM (no rewording, no merging).
   - End with `## The argument in five moves` (5–7 numbered clauses tracing what
     Delos offers across the pages: product, workers, pricing, integrations).
2. Rewrite `questions.md` (36 pages → 12–20 questions):
   - Front-matter: `type: Retrieval Prompts, last_reviewed: null, review_count: 0`
   - Backlink line: `> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]`
   - Heading: keep the existing title.
   - Cover the site's AREAS (product, pricing, integrations, security, workers —
     not every one of the 17 worker profiles needs its own question) with at
     least one question per area plus exactly one evaluation
     (judgment/recommendation) question.
   - One block per question: `### Qn. <question>` followed by `> [!tip]- Answer`
     and then `> <2–4 sentences>. See [[wiki/NN-slug|Topic]].`
   - Answers exist ONLY inside the collapsed callouts.
3. Update `index.md`: read it first, keep front-matter, orientation, ladder, and
   Read This Folder links untouched; extend the `## Wiki` table with one row per
   new page (`| [[wiki/NN-slug|<Topic>]] | <one line> |`) in numeric order.
4. Append rows to `source/plan.md` mapping each topic file to its wiki page
   (`NN-slug.md` + one-line "covers" note); do not alter existing rows.

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/WorkersDelos
grep -c "^## [0-9]*\. " digest.md
grep -c "^### Q" questions.md
grep -c "wiki/3" index.md
```

Digest must have 36 numbered page sections; questions 12–20 `### Q` blocks;
index table must reference pages 30–35 (spot check the tail).

## DoD

1. `digest.md`, `questions.md`, `index.md`, `source/plan.md` updated as above.
2. Tests above green (digest == 36, questions 12–20).
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY `digest.md`, `questions.md`, `index.md`, `source/plan.md`. Do not
  touch `summary.md`, `explainer.md`, `critical_thinking.md`, `wiki/`, or topics.
- cwd: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
