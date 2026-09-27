# DS2 — wiki pages 11–18 (solutions, tech, use-cases, workers)

## Problem

`/Users/sergii/.ai/knowledge/research/WorkersDelos/` covers only the homepage.
This bead writes pages 11–18 (depends on DS1 only for ordering on the shared
tree, not for content).

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
Read ONLY these eight topic files (your sole source of facts):

- `source/topics/solutions_design.md` → write `wiki/11-solutions-design.md`
- `source/topics/solutions_developpement.md` → write `wiki/12-solutions-developpement.md`
- `source/topics/solutions_finance.md` → write `wiki/13-solutions-finance.md`
- `source/topics/solutions_marketing.md` → write `wiki/14-solutions-marketing.md`
- `source/topics/solutions_rh.md` → write `wiki/15-solutions-rh.md`
- `source/topics/tech.md` → write `wiki/16-tech.md`
- `source/topics/use-cases.md` → write `wiki/17-use-cases.md`
- `source/topics/workers.md` → write `wiki/18-workers.md`

Each page follows exactly this contract:

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# <Topic>
**In one sentence:** <the page's whole argument in one sentence>
## Key points
- 5–8 bullets, each a complete claim with numbers/mechanisms, not a topic label
---
## <subsections mirroring the source>  (tables, exact numbers, verbatim quotes)
**Covers:** <page URL, e.g. https://delos.so/solutions/marketing>
```

Never invent content: only claims present in the topic file. Do not read the
web or other wiki pages.

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/WorkersDelos
for f in wiki/11-solutions-design.md wiki/12-solutions-developpement.md wiki/13-solutions-finance.md wiki/14-solutions-marketing.md wiki/15-solutions-rh.md wiki/16-tech.md wiki/17-use-cases.md wiki/18-workers.md; do test -s "$f" || echo "MISSING $f"; grep -c "In one sentence" "$f"; done
```

## DoD

1. All eight wiki pages exist at the exact absolute paths above.
2. Tests above green.
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY the eight `wiki/` files listed. Do not touch `summary.md`, `digest.md`,
  `index.md`, `questions.md`, `explainer.md`, `critical_thinking.md`, `source/`.
- cwd: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
