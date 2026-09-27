# ART-DELOS — plain-words article: Delos (AI workers company)

## Problem

`/Users/sergii/.ai/knowledge/research/WorkersDelos/` holds 35 wiki pages of dense
material. Nobody outside the field will read it. We need a single article that
explains in simple words what Delos is, how it works, and what is inside.

## Fix

Work dir: `/Users/sergii/.ai/knowledge/research/WorkersDelos`.
Read `summary.md`, `digest.md`, and skim `wiki/` pages as needed (never
`source/topics/`, never the web).

Write `/Users/sergii/.ai/knowledge/articles/delos-ai-workers-explained.md`:

- Audience: a smart non-engineer. Every piece of jargon (AI worker, memory,
  integrations, GDPR, confidence) gets a one-line plain explanation on first use.
- Sections: what Delos is and what problem it solves → how you use it (hire a
  worker, connect tools, give it work — concrete flow) → the product pieces
  (office suite plans and pricing, integrations, security) → internals (what a
  "worker" is made of: role, skills, memory, tools; meet 3–4 example workers by
  name with what each does) → where it fits and where it does not (one honest
  paragraph, no sales pitch).
- 80–150 lines. Flowing prose, concrete numbers from the source (prices, tool
  counts, worker count) where they exist. Never invent facts.
- Human voice, no AI tells: no em dashes, no "delve/landscape/crucial/tapestry/
  game-changer/deep dive", no "it's not just X, it's Y", no rule-of-three
  lists, no bold-led bullet lists, no generic upbeat ending. Vary sentence
  rhythm. Plain `is/are` over fancy constructions.

## Tests

```bash
f=/Users/sergii/.ai/knowledge/articles/delos-ai-workers-explained.md
test -s "$f"; wc -l "$f"; grep -ciE "delve|tapestry|crucial|game-changer|deep dive|evolving landscape|not just" "$f"
```

File exists, 80–150 lines, banned-phrase count is 0.

## DoD

1. Article exists at the exact absolute path above.
2. Tests above green.
3. Exit 0. Do NOT run git commands. Do NOT close the bead yourself.

## Scope & constraints

- WRITE ONLY the article file. Read-only everywhere else. Do not touch the
  WorkersDelos folder at all.
- cwd: `/Users/sergii/.ai`.
- Do not run `fleet serve restart` / `fleet run`. No network access needed.
