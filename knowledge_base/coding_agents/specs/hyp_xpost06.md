# Spec fleet-xpost06 — brief: Gaurav Sen 2500 agent repos (hypothesis tier)

## Problem
No KB brief exists for Gaurav Sen's "best practices from GitHub analysis of 2500 agent
repos" (https://x.com/gkcs_/status/1994157453366448570). Triage tier: recap — the
underlying analysis is not linked/checked — process it cheaply as a fleet brief.

## Fix
Fetch the post (network allowed ONLY to x.com and web.archive.org):
1. `curl -sL --max-time 40 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://x.com/gkcs_/status/1994157453366448570"`
2. Fallback: `https://web.archive.org/web/2026/https://x.com/gkcs_/status/1994157453366448570`
3. Validate: body must contain "gkcs_" — else it is a challenge/login page, try the next method.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_gauravsen_2500.md`:
```
# [Hypothesis] Gaurav Sen — "best practices from 2500 agent repos"
- Source: https://x.com/gkcs_/status/1994157453366448570
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: claimed findings (or an honest retrieval note if inaccessible). Flag prominently whether the underlying GitHub analysis is linked and checkable — if not, say so.
## Why it was kept
- Big-number claim without a checkable analysis — treat as recap/leads, not findings.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
```
Style: tight bullets; expand abbreviations on first use only.

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_gauravsen_2500.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_gauravsen_2500.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_gauravsen_2500.md` then `git commit -m "xpost06: gauravsen brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_gauravsen_2500.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-xpost06 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to x.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
