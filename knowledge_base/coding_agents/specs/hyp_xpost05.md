# Spec fleet-xpost05 — brief: Cory House Spec Kit run (hypothesis tier)

## Problem
No KB brief exists for Cory House's personal Spec Kit + Claude Code run
(https://x.com/housecor/status/1970666878797258990). Triage tier: real use but one person
on a personal/app codebase — process it cheaply as a fleet brief.

## Fix
Fetch the post (network allowed ONLY to x.com and web.archive.org):
1. `curl -sL --max-time 40 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://x.com/housecor/status/1970666878797258990"`
2. Fallback: `https://web.archive.org/web/2026/https://x.com/housecor/status/1970666878797258990`
3. Validate: body must contain "housecor" — else it is a challenge/login page, try the next method.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_coryhouse_speckit.md`:
```
# [Hypothesis] Cory House — personal Spec Kit + Claude Code run
- Source: https://x.com/housecor/status/1970666878797258990
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: what he ran, what worked, friction points (or an honest retrieval note if inaccessible).
## Why it was kept
- Real hands-on run, but n=1 on a personal codebase — practitioner datapoint, not team evidence.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
```
Style: tight bullets; expand abbreviations on first use only.

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_coryhouse_speckit.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_coryhouse_speckit.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_coryhouse_speckit.md` then `git commit -m "xpost05: coryhouse brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_coryhouse_speckit.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-xpost05 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to x.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
