# ByoCodingAgent component 06 extract

## Problem
Write wiki page `wiki/06-course-map.md` for the `ByoCodingAgent` codebase entry. The worker sees only this spec + the listed repo paths — never the whole repo.

## Fix
1. Read ONLY these repo paths (absolute, cloned read-only): /tmp/byo-coding-agent/follow_along/,/tmp/byo-coding-agent/how-to/,/tmp/byo-coding-agent/exercises/,/tmp/byo-coding-agent/README.md. Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else.
2. Write `/Users/sergii/.ai/knowledge/research/ByoCodingAgent/wiki/06-course-map.md` COMPLETELY (overwrite on retry) with the wiki-page format contract: backlink line `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`, `# Course structure: lessons, exercises, how-tos`, `**In one sentence:**`, `## Key points` (5-8 complete claims with file:line cites), `---`, full detail in `##` subsections, key signatures/configs quoted verbatim, footer `**Covers:** component 06`. Codebase rule: every structural claim cites `file:line`. No meta-junk.
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/research/ByoCodingAgent/wiki/06-course-map.md && wc -l /Users/sergii/.ai/knowledge/research/ByoCodingAgent/wiki/06-course-map.md` >= 40; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/research/ByoCodingAgent/wiki/06-course-map.md` == 1.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "component 06 extracted"` (own task only).

## Scope & constraints
- No `fleet` commands except `bd close`. No network (read local clone only). No secrets. NEVER write into the repo clone.
