# Spec fleet-blog08 — brief: inspiredbyfrustration assistant 2026 (secondary tier)

## Problem
No KB brief exists for the inspiredbyfrustration roundup (https://inspiredbyfrustration.com/blog/best-ai-coding-assistant-2026).
Triage tier: secondary journalism — cheap fleet brief.

## Fix
Fetch with `curl -sL --max-time 60` (network allowed ONLY to inspiredbyfrustration.com and
web.archive.org, Wayback fallback `https://web.archive.org/web/2026/<URL>`); strip tags
locally; validate the body mentions at least two coding assistants by name.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog08_frustration.md`:
```
# [Secondary] inspiredbyfrustration — best AI coding assistant 2026
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
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog08_frustration.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog08_frustration.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog08_frustration.md` then `git commit -m "blog08: frustration brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_blog08_frustration.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-blog08 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to inspiredbyfrustration.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
