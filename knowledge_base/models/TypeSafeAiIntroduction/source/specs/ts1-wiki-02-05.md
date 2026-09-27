# TS1 — wiki pages 02–05 (quickstart → primitives overview)

## Problem

`/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction/` covers only the
introduction page (`wiki/01-documentation-index.md`). The other 22 docs topics
must become wiki pages in the same folder. This bead writes pages 02–05.

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
Read ONLY these four topic files (your sole source of facts):

- `source/topics/introduction_quickstart.md` → write `wiki/02-quick-start.md`
- `source/topics/concepts_system-one.md` → write `wiki/03-system-one.md`
- `source/topics/concepts_state.md` → write `wiki/04-state.md`
- `source/topics/primitives.md` → write `wiki/05-primitives-overview.md`

Each page follows exactly this contract (mirror `wiki/01-documentation-index.md` style):

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# <Topic>
**In one sentence:** <the page's whole argument in one sentence>
## Key points
- 5–8 bullets, each a complete claim with numbers/mechanisms, not a topic label
---
## <subsections mirroring the source>  (tables, exact numbers, verbatim quotes)
**Covers:** <topic page URL, e.g. https://docs.typesafe.ai/introduction/quickstart>
```

Never invent content: only claims present in the topic file. Do not read any
other topic file, the original web, or other wiki pages (except 01 for style).

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction
for f in wiki/02-quick-start.md wiki/03-system-one.md wiki/04-state.md wiki/05-primitives-overview.md; do test -s "$f" || echo "MISSING $f"; grep -c "In one sentence" "$f"; grep -c "## Key points" "$f"; done
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
