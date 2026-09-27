# Spec fleet-xpost01 — brief: Prajwal Tomar 11-step loop (hypothesis tier)

## Problem
No KB brief exists for Prajwal Tomar's 11-step Cursor/Claude Code loop
(https://x.com/PrajwalTomar_/status/1947272871967174720). Triage tier: hypothesis / solo
production — process it cheaply as a fleet brief, not a full summarise run.

## Fix
Fetch the post (network allowed ONLY to x.com and web.archive.org):
1. `curl -sL --max-time 40 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://x.com/PrajwalTomar_/status/1947272871967174720"`
2. Fallback: `https://web.archive.org/web/2026/https://x.com/PrajwalTomar_/status/1947272871967174720`
3. Validate: body must contain "PrajwalTomar" — else it is a challenge/login page, try the next method.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_ptomar_11step.md`:
```
# [Hypothesis] Prajwal Tomar — 11-step Cursor/Claude Code loop
- Source: https://x.com/PrajwalTomar_/status/1947272871967174720
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: the loop steps and any concrete tactics (or an honest retrieval note if inaccessible).
## Why it was kept
- Solo operator loop ("I build products"); useful as a technique checklist, not team evidence.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
```
Style: tight bullets; expand abbreviations on first use only.

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_ptomar_11step.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_ptomar_11step.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_ptomar_11step.md` then `git commit -m "xpost01: ptomar loop brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_ptomar_11step.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-xpost01 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to x.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
