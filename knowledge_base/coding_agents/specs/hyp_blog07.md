# Spec fleet-blog07 — brief: pick-right harnesses (secondary tier)

## Problem
No KB brief exists for the pick-right roundup (https://pick-right.com/best/best-ai-harnesses-tools/).
Triage tier: secondary journalism — cheap fleet brief.

## Fix
Fetch with `curl -sL --max-time 60` (network allowed ONLY to pick-right.com and
web.archive.org, Wayback fallback `https://web.archive.org/web/2026/<URL>`); strip tags
locally; validate the body mentions coding harnesses/tools.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog07_pickright.md`:
```
# [Secondary] pick-right — best AI harnesses/tools
- Source: <URL>
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: comparison claims worth checking, if any (or retrieval note).
## Why it was kept
- Secondary roundup; keep only checkable claims, never conclusions.
## Tier
- Secondary journalism — do not cite as evidence.
```
Style: tight bullets; expand abbreviations on first use only.

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog07_pickright.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog07_pickright.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog07_pickright.md` then `git commit -m "blog07: pickright brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_blog07_pickright.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-blog07 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to pick-right.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
