# DS1 — wiki pages 02–10 (site pages batch 1)

## Problem

`/Users/sergii/.ai/knowledge/research/WorkersDelos/` covers only the homepage
(`wiki/01`). This bead writes site pages 02–10 from local topic files.

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
Read ONLY these nine topic files (your sole source of facts):

- `source/topics/about.md` → write `wiki/02-about.md`
- `source/topics/blog.md` → write `wiki/03-blog.md`
- `source/topics/build-a-team.md` → write `wiki/04-build-a-team.md`
- `source/topics/clone-yourself.md` → write `wiki/05-clone-yourself.md`
- `source/topics/compagnon.md` → write `wiki/06-compagnon.md`
- `source/topics/integrations.md` → write `wiki/07-integrations.md`
- `source/topics/personality.md` → write `wiki/08-personality.md`
- `source/topics/pricing.md` → write `wiki/09-pricing.md`
- `source/topics/security.md` → write `wiki/10-security.md`

Each page follows exactly this contract:

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# <Topic>
**In one sentence:** <the page's whole argument in one sentence>
## Key points
- 5–8 bullets, each a complete claim with numbers/mechanisms, not a topic label
---
## <subsections mirroring the source>  (tables, exact numbers, verbatim quotes)
**Covers:** <page URL, e.g. https://delos.so/pricing>
```

Never invent content: only claims present in the topic file. Thin marketing pages
still get full pages; say what the page covers and cross-reference the richer
neighbour (e.g. pricing → workers). Do not read the web or other wiki pages.

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/WorkersDelos
for f in wiki/02-about.md wiki/03-blog.md wiki/04-build-a-team.md wiki/05-clone-yourself.md wiki/06-compagnon.md wiki/07-integrations.md wiki/08-personality.md wiki/09-pricing.md wiki/10-security.md; do test -s "$f" || echo "MISSING $f"; grep -c "In one sentence" "$f"; done
```

## DoD

1. All nine wiki pages exist at the exact absolute paths above.
2. Tests above green.
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY the nine `wiki/` files listed. Do not touch `summary.md`, `digest.md`,
  `index.md`, `questions.md`, `explainer.md`, `critical_thinking.md`, `source/`.
- cwd: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
