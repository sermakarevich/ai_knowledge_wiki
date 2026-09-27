# TS5 — rewrite digest.md, questions.md, index.md wiki table (all 24 pages)

## Problem

`digest.md`, `questions.md`, and `index.md` in
`/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction/` cover only the
introduction page (`wiki/01`). After TS1–TS4 the folder holds `wiki/01`–`wiki/23`
and the derived files are stale. This bead refreshes the three mechanical files
(TS6 rewrites `summary.md`, TS7 `explainer.md` + `critical_thinking.md`).

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
Read ONLY `wiki/01-documentation-index.md` … `wiki/23-agent-skill.md`
(never `source/`, the topic files, or the web).

1. Rewrite `digest.md`:
   - Backlink line: `> [[index|Wiki]] | [[summary|Summary]]`
   - Heading: `# Introduction - TypeSafe AI — Digest`
   - One section per wiki page in order: `## N. [[wiki/NN-slug|Title]]` with that
     page's `**In one sentence:**` line and its `## Key points` bullets copied
     VERBATIM (no rewording, no merging).
   - End with `## The argument in five moves` (5–7 numbered clauses tracing the
     whole docs' argument across the pages).
2. Rewrite `questions.md` (24 pages → 12–20 questions):
   - Front-matter: `type: Retrieval Prompts, last_reviewed: null, review_count: 0`
   - Backlink line: `> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]`
   - Heading: `# Retrieval Practice: Introduction - TypeSafe AI`
   - Cover every wiki page with at least one question plus exactly one evaluation
     (judgment/recommendation) question.
   - One block per question: `### Qn. <question>` followed by `> [!tip]- Answer`
     and then `> <2–4 sentences>. See [[wiki/NN-slug|Topic]].`
   - Answers exist ONLY inside the collapsed callouts.
3. Update `index.md`: read it first, keep front-matter, orientation, ladder, and
   Read This Folder links untouched; extend the `## Wiki` table with one row per
   new page (`| [[wiki/NN-slug|<Topic>]] | <one line> |`) in numeric order.
4. Append 22 rows to `source/plan.md` mapping each topic file to its wiki page
   (`NN-slug.md` + one-line "covers" note); do not alter existing rows.

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction
grep -c "^## [0-9]*\. " digest.md
grep -c "^### Q" questions.md
grep -c "wiki/2" index.md
```

Digest must have 24 numbered page sections; questions 12–20 `### Q` blocks;
index table must reference pages 20–23 (spot check the tail).

## DoD

1. `digest.md`, `questions.md`, `index.md`, `source/plan.md` updated as above.
2. Tests above green (digest == 24, questions 12–20).
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY `digest.md`, `questions.md`, `index.md`, `source/plan.md`. Do not
  touch `summary.md`, `explainer.md`, `critical_thinking.md`, `wiki/`, or topics.
- cwd: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
