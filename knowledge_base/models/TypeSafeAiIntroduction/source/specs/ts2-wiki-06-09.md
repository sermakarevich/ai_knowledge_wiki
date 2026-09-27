# TS2 — wiki pages 06–09 (Choice, Score, Noul, Advanced structure)

## Problem

`/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction/` covers only the
introduction page. This bead writes the three primitives + advanced-structure
pages (depends on TS1 only for ordering on the shared tree, not for content).

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
Read ONLY these four topic files (your sole source of facts):

- `source/topics/primitives_choice.md` → write `wiki/06-choice.md`
- `source/topics/primitives_score.md` → write `wiki/07-score.md`
- `source/topics/primitives_noul.md` → write `wiki/08-noul.md`
- `source/topics/primitives_advanced.md` → write `wiki/09-advanced-structure.md`

Each page follows exactly this contract (mirror `wiki/01-documentation-index.md` style):

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# <Topic>
**In one sentence:** <the page's whole argument in one sentence>
## Key points
- 5–8 bullets, each a complete claim with numbers/mechanisms, not a topic label
---
## <subsections mirroring the source>  (tables, exact numbers, verbatim quotes)
**Covers:** <topic page URL, e.g. https://docs.typesafe.ai/primitives/choice>
```

Never invent content: only claims present in the topic file. Do not read any
other topic file, the original web, or other wiki pages (except 01 for style).

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction
for f in wiki/06-choice.md wiki/07-score.md wiki/08-noul.md wiki/09-advanced-structure.md; do test -s "$f" || echo "MISSING $f"; grep -c "In one sentence" "$f"; grep -c "## Key points" "$f"; done
```

Every file must exist, non-empty, with exactly one `In one sentence` line and one
`## Key points` section.

## DoD

1. All four wiki pages exist at the exact absolute paths above.
2. Tests above green.
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY the four `wiki/` files listed. Do not touch `summary.md`, `digest.md`,
  `index.md`, `questions.md`, `explainer.md`, `critical_thinking.md`, `source/`.
- cwd: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
