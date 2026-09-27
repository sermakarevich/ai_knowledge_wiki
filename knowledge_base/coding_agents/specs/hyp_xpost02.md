# Spec fleet-xpost02 — brief: Alex Finn "Finn Loop" (hypothesis tier)

## Problem
No KB brief exists for Alex Finn's "Finn Loop" (/spec → /build → /review)
(https://x.com/AlexFinn/status/2076752798532931758). Triage tier: hypothesis / solo
production — process it cheaply as a fleet brief, not a full summarise run.

## Fix
Fetch the post (network allowed ONLY to x.com and web.archive.org):
1. `curl -sL --max-time 40 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://x.com/AlexFinn/status/2076752798532931758"`
2. Fallback: `https://web.archive.org/web/2026/https://x.com/AlexFinn/status/2076752798532931758`
3. Validate: body must contain "AlexFinn" — else it is a challenge/login page, try the next method.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_finn_loop.md`:
```
# [Hypothesis] Alex Finn — "Finn Loop" (/spec → /build → /review)
- Source: https://x.com/AlexFinn/status/2076752798532931758
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: the loop phases and any concrete tactics (or an honest retrieval note if inaccessible).
## Why it was kept
- Solo founder loop; high engagement is not team production — technique checklist only.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
```
Style: tight bullets; expand abbreviations on first use only.

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_finn_loop.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_finn_loop.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_finn_loop.md` then `git commit -m "xpost02: finn loop brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_finn_loop.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-xpost02 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to x.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
