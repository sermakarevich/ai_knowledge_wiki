# Spec fleet-xpost04 — brief: kloss DESIGN.md repo OS (hypothesis tier)

## Problem
No KB brief exists for kloss's "DESIGN.md or hallucination" post (DESIGN.md / AGENTS.md /
SKILL.md as required repo OS) (https://x.com/kloss_xyz/status/2048530452877873390). Triage
tier: hypothesis / individual manifesto — process it cheaply as a fleet brief.

## Fix
Fetch the post (network allowed ONLY to x.com and web.archive.org):
1. `curl -sL --max-time 40 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://x.com/kloss_xyz/status/2048530452877873390"`
2. Fallback: `https://web.archive.org/web/2026/https://x.com/kloss_xyz/status/2048530452877873390`
3. Validate: body must contain "kloss_xyz" — else it is a challenge/login page, try the next method.
Write `/Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_kloss_design.md`:
```
# [Hypothesis] kloss — DESIGN.md / AGENTS.md / SKILL.md as required repo OS
- Source: https://x.com/kloss_xyz/status/2048530452877873390
- Status: fetched <date> | inaccessible (methods tried: ...)
## Content
- 5–10 bullets: the manifesto claims and any concrete file-convention tactics (or an honest retrieval note if inaccessible).
## Why it was kept
- Individual manifesto, but the repo-OS convention (design + agent instructions + skills checked into the repo) matches real team practice elsewhere — compare, don't adopt blindly.
## Tier
- E5 hypothesis / solo production — do not cite as team evidence.
```
Style: tight bullets; expand abbreviations on first use only.

## Tests
`test -s /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_kloss_design.md && grep -c "## Tier" /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_kloss_design.md`

## DoD
1. Test above green.
2. `git add /Users/sergii/.ai/knowledge/research_topics/coding_agents/hypothesis_kloss_design.md` then `git commit -m "xpost04: kloss design brief"`.
3. Verify: `git show HEAD:knowledge/research_topics/coding_agents/hypothesis_kloss_design.md | grep -c "## Tier"` prints >= 1.
4. `bd close fleet-xpost04 --reason "brief landed"` — close ONLY your own task. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai (shared tree, git repo in isolation_exclude).
- Touch ONLY your one output file. NEVER touch interviews/, other topics, specs/, index files.
- Network ONLY to x.com / web.archive.org via curl. NEVER `git add -A` / `.` / `-a`; NEVER reset/checkout/stash/restore; NEVER run `fleet serve` / `fleet run`.
