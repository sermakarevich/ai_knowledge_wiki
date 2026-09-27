# Spec fleet-xpost07 — brief: Maryam Miradi 9 production layers (hypothesis tier)

## Problem
No KB brief exists for Maryam Miradi's 9 production AI-agent layers
(https://x.com/MaryamMiradi/status/2102112004341154153). Triage tier: generic
agent-production checklist, not AI-coding team practice — process it cheaply as a fleet brief.

## Fix
Fetch the post (network allowed ONLY to x.com and web.archive.org):
1. `curl -sL --max-time 40 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://x.com/MaryamMiradi/status/2102112004341154153"`
2. Fallback: `https://web.archive.org/web/2026/https://x.com/MaryamMiradi/status/2102112004341154153`
3. Validate: body must contain "MaryamMiradi" — else it is a challenge/login page, try the next method.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_miradi_layers.md`:
```
# [Hypothesis] Maryam Miradi — 9 production AI-agent layers
- Source: https://x.com/MaryamMiradi/status/2102112004341154153
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: the 9 layers and any AI-coding-relevant points (or an honest retrieval note if inaccessible).
## Why it was kept
- Generic production checklist; keep only what maps to AI-coding team practice, note the rest as out of scope.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
```
Style: tight bullets; expand abbreviations on first use only.

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_miradi_layers.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_miradi_layers.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_miradi_layers.md` then `git commit -m "xpost07: miradi brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_miradi_layers.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-xpost07 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to x.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
