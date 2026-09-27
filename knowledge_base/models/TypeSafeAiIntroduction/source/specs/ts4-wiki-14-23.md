# TS4 — wiki pages 14–23 (Patterns, Demos, SDKs, API, Agent skill)

## Problem

`/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction/` covers only the
introduction page. This bead writes the final batch, pages 14–23 (depends on
TS3 only for ordering on the shared tree, not for content).

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
Read ONLY these ten topic files (your sole source of facts):

- `source/topics/patterns.md` → write `wiki/14-patterns.md`
- `source/topics/patterns_fan-out.md` → write `wiki/15-speculative-fan-out.md`
- `source/topics/patterns_confidence-routing.md` → write `wiki/16-confidence-gated-routing.md`
- `source/topics/patterns_composite-scoring.md` → write `wiki/17-composite-scoring.md`
- `source/topics/patterns_intent-routing.md` → write `wiki/18-intent-routing.md`
- `source/topics/demos.md` → write `wiki/19-demos.md`
- `source/topics/demos_smart-home.md` → write `wiki/20-smart-home-demo.md`
- `source/topics/sdk.md` → write `wiki/21-client-sdks.md`
- `source/topics/api.md` → write `wiki/22-api-reference.md`
- `source/topics/agent-skill.md` → write `wiki/23-agent-skill.md`

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

Never invent content: only claims present in the topic file. Small topics
(demos.md, sdk.md) still get full pages; if a file is thin, say what it covers
and point to the richer neighbour page. Do not read the web or other wiki pages
(except 01 for style).

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction
for f in wiki/14-patterns.md wiki/15-speculative-fan-out.md wiki/16-confidence-gated-routing.md wiki/17-composite-scoring.md wiki/18-intent-routing.md wiki/19-demos.md wiki/20-smart-home-demo.md wiki/21-client-sdks.md wiki/22-api-reference.md wiki/23-agent-skill.md; do test -s "$f" || echo "MISSING $f"; grep -c "In one sentence" "$f"; done
ls wiki/*.md | wc -l
```

All ten files exist and non-empty; `wiki/` holds 24 `.md` files total
(01–23 plus nothing else).

## DoD

1. All ten wiki pages exist at the exact absolute paths above.
2. Tests above green.
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY the ten `wiki/` files listed. Do not touch `summary.md`, `digest.md`,
  `index.md`, `questions.md`, `explainer.md`, `critical_thinking.md`, `source/`.
- cwd: `/Users/sergii/.ai/knowledge/research/TypeSafeAiIntroduction`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
