# TS3 — wiki pages 10–13 (AI primer, Confidence, How-to-build, Use-case map)

## Problem

`/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction/` covers only the
introduction page. This bead writes pages 10–13 (depends on TS2 only for
ordering on the shared tree, not for content).

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
Read ONLY these four topic files (your sole source of facts):

- `source/topics/introduction_machine-learning-primer.md` → write `wiki/10-ai-primer.md`
- `source/topics/confidence.md` → write `wiki/11-confidence.md`
- `source/topics/concepts_how-to-build-with-system-one.md` → write `wiki/12-how-to-build-with-system-one.md`
- `source/topics/concepts_use-case-map.md` → write `wiki/13-use-case-map.md`

Each page follows exactly this contract (mirror `wiki/01-documentation-index.md` style):

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# <Topic>
**In one sentence:** <the page's whole argument in one sentence>
## Key points
- 5–8 bullets, each a complete claim with numbers/mechanisms, not a topic label
---
## <subsections mirroring the source>  (tables, exact numbers, verbatim quotes)
**Covers:** <topic page URL>
```

Never invent content: only claims present in the topic file. Do not read any
other topic file, the original web, or other wiki pages (except 01 for style).

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction
for f in wiki/10-ai-primer.md wiki/11-confidence.md wiki/12-how-to-build-with-system-one.md wiki/13-use-case-map.md; do test -s "$f" || echo "MISSING $f"; grep -c "In one sentence" "$f"; grep -c "## Key points" "$f"; done
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
