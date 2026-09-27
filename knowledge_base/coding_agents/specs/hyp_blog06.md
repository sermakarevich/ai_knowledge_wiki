# Spec fleet-blog06 — brief: aicoderscope (secondary tier)

## Problem
No KB brief exists for aicoderscope (https://aicoderscope.com/).
Triage tier: secondary journalism — cheap fleet brief.

## Fix
Fetch with `curl -sL --max-time 60` (network allowed ONLY to aicoderscope.com and
web.archive.org, Wayback fallback `https://web.archive.org/web/2026/<URL>`); strip tags
locally; validate the body mentions coding agents/tools.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog06_aicoderscope.md`:
```
# [Secondary] aicoderscope
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
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog06_aicoderscope.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog06_aicoderscope.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_blog06_aicoderscope.md` then `git commit -m "blog06: aicoderscope brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_blog06_aicoderscope.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-blog06 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to aicoderscope.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
