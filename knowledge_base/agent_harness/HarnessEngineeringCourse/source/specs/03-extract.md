# HarnessEngineeringCourse component 03 extract

## Problem
Write wiki page `wiki/03-memory-skills.md` for the `HarnessEngineeringCourse` codebase entry. The worker sees only this spec + the listed repo paths — never the whole repo.

## Fix
1. Read ONLY these repo paths (absolute, cloned read-only): /tmp/harnessengineering/harness/memory.py,/tmp/harnessengineering/harness/compaction.py,/tmp/harnessengineering/harness/limits.py,/tmp/harnessengineering/harness/skills.py. Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else.
2. Write `/Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/wiki/03-memory-skills.md` COMPLETELY (overwrite on retry) with the wiki-page format contract: backlink line `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`, `# Memory, compaction, limits, skills`, `**In one sentence:**`, `## Key points` (5-8 complete claims with file:line cites), `---`, full detail in `##` subsections, key signatures/configs quoted verbatim, footer `**Covers:** component 03`. Codebase rule: every structural claim cites `file:line`. No meta-junk.
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/wiki/03-memory-skills.md && wc -l /Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/wiki/03-memory-skills.md` >= 40; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/wiki/03-memory-skills.md` == 1.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "component 03 extracted"` (own task only).

## Scope & constraints
- No `fleet` commands except `bd close`. No network (read local clone only). No secrets. NEVER write into the repo clone.
