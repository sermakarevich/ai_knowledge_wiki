# DS3 — wiki pages 19–35 (17 worker profiles)

## Problem

`/Users/sergii/.ai/knowledge/research/WorkersDelos/` covers only the homepage.
This bead writes one page per AI worker profile, pages 19–35 (depends on DS2
only for ordering on the shared tree, not for content).

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
Read ONLY these topic files (your sole source of facts) and write the mapped page:

- `source/topics/worker_laura.md` → `wiki/19-worker-laura.md`
- `source/topics/worker_james.md` → `wiki/20-worker-james.md`
- `source/topics/worker_nova.md` → `wiki/21-worker-nova.md`
- `source/topics/worker_sophie.md` → `wiki/22-worker-sophie.md`
- `source/topics/worker_henry.md` → `wiki/23-worker-henry.md`
- `source/topics/worker_atif.md` → `wiki/24-worker-atif.md`
- `source/topics/worker_karen.md` → `wiki/25-worker-karen.md`
- `source/topics/worker_sun.md` → `wiki/26-worker-sun.md`
- `source/topics/worker_ivan.md` → `wiki/27-worker-ivan.md`
- `source/topics/worker_victoria.md` → `wiki/28-worker-victoria.md`
- `source/topics/worker_mateo.md` → `wiki/29-worker-mateo.md`
- `source/topics/worker_rosa.md` → `wiki/30-worker-rosa.md`
- `source/topics/worker_jeanne.md` → `wiki/31-worker-jeanne.md`
- `source/topics/worker_alexa.md` → `wiki/32-worker-alexa.md`
- `source/topics/worker_alex.md` → `wiki/33-worker-alex.md`
- `source/topics/worker_camille.md` → `wiki/34-worker-camille.md`
- `source/topics/worker_arjun.md` → `wiki/35-worker-arjun.md`

Each page follows exactly this contract:

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# <Worker name> — <role>
**In one sentence:** <who this worker is and what it does, one sentence>
## Key points
- 5–8 bullets: role, key skills, tool integrations, personality notes, example behavior — each a complete claim, not a topic label
---
## <subsections mirroring the source>  (skills, tools, verbatim quotes)
**Covers:** <profile URL, e.g. https://delos.so/worker/laura>
```

Never invent content: only claims present in the topic file. Profiles share a
template — capture what is DISTINCT per worker (role, skills, tools, voice).
Do not read the web or other wiki pages.

## Tests

```bash
cd /Users/sergii/.ai/knowledge/research/WorkersDelos
for f in wiki/19-worker-laura.md wiki/20-worker-james.md wiki/21-worker-nova.md wiki/22-worker-sophie.md wiki/23-worker-henry.md wiki/24-worker-atif.md wiki/25-worker-karen.md wiki/26-worker-sun.md wiki/27-worker-ivan.md wiki/28-worker-victoria.md wiki/29-worker-mateo.md wiki/30-worker-rosa.md wiki/31-worker-jeanne.md wiki/32-worker-alexa.md wiki/33-worker-alex.md wiki/34-worker-camille.md wiki/35-worker-arjun.md; do test -s "$f" || echo "MISSING $f"; done
ls wiki/*.md | wc -l
```

All 17 files exist and non-empty; `wiki/` holds 36 `.md` files total (01–35 + images dir ignored).

## DoD

1. All 17 wiki pages exist at the exact absolute paths above.
2. Tests above green.
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- Touch ONLY the 17 `wiki/` files listed. Do not touch `summary.md`, `digest.md`,
  `index.md`, `questions.md`, `explainer.md`, `critical_thinking.md`, `source/`.
- cwd: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
