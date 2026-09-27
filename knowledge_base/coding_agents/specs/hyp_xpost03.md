# Spec fleet-xpost03 — brief: Ben X TRD/epics/tickets (hypothesis tier)

## Problem
No KB brief exists for Ben X's TRD → epics → tickets → new-session-per-ticket method
(https://x.com/Benn_X1/status/2048468090342486417). Triage tier: hypothesis / individual
method — process it cheaply as a fleet brief, not a full summarise run.

## Fix
Fetch the post (network allowed ONLY to x.com and web.archive.org):
1. `curl -sL --max-time 40 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://x.com/Benn_X1/status/2048468090342486417"`
2. Fallback: `https://web.archive.org/web/2026/https://x.com/Benn_X1/status/2048468090342486417`
3. Validate: body must contain "Benn_X1" — else it is a challenge/login page, try the next method.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_benx_trd.md`:
```
# [Hypothesis] Ben X — TRD → epics → tickets → fresh session per ticket
- Source: https://x.com/Benn_X1/status/2048468090342486417
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: the method steps and any concrete tactics (or an honest retrieval note if inaccessible).
## Why it was kept
- Individual method, no team — session-hygiene idea (fresh context per ticket) worth stealing.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
```
Style: tight bullets; expand abbreviations on first use only (TRD (technical requirements document)).

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_benx_trd.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_benx_trd.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_benx_trd.md` then `git commit -m "xpost03: benx trd brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_benx_trd.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-xpost03 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to x.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
