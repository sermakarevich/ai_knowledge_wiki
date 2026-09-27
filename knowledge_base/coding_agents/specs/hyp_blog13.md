# Spec fleet-blog13 — brief: rework coding tools 2026 (secondary tier)

## Problem
No KB brief exists for the rework roundup (https://resources.rework.com/tools/ai-tools/best-ai-coding-tools-2026).
Triage tier: secondary journalism — cheap fleet brief.

## Fix
Fetch with `curl -sL --max-time 60` (network allowed ONLY to resources.rework.com and
web.archive.org, Wayback fallback `https://web.archive.org/web/2026/<URL>`); strip tags
locally; validate the body mentions coding tools.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog13_rework.md`:
```
# [Secondary] rework — best AI coding tools 2026
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
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog13_rework.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog13_rework.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog13_rework.md` then `git commit -m "blog13: rework brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_blog13_rework.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-blog13 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to resources.rework.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
