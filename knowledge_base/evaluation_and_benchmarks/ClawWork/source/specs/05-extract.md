# ClawWork component 05 extract

## Problem
Write wiki page `wiki/05-economics-scripts.md` for the `ClawWork` codebase entry. The worker sees only this spec + the listed repo paths — never the whole repo.

## Fix
1. Read ONLY these repo paths (absolute, cloned read-only): /tmp/clawwork/scripts/validate_economic_system.py,/tmp/clawwork/scripts/recalculate_agent_economics.py,/tmp/clawwork/scripts/calculate_task_values.py,/tmp/clawwork/scripts/estimate_task_hours.py. Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else. Skip bulk data dirs (livebench/data, sandboxes) — read code and small configs only.
2. Write `/Users/sergii/.ai/knowledge/research/ClawWork/wiki/05-economics-scripts.md` COMPLETELY (overwrite on retry) with the wiki-page format contract: backlink line `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`, `# Economics pipeline scripts`, `**In one sentence:**`, `## Key points` (5-8 complete claims with file:line cites), `---`, full detail in `##` subsections, key signatures/configs quoted verbatim, footer `**Covers:** component 05`. Codebase rule: every structural claim cites `file:line`. No meta-junk.
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/research/ClawWork/wiki/05-economics-scripts.md && wc -l /Users/sergii/.ai/knowledge/research/ClawWork/wiki/05-economics-scripts.md` >= 40; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/research/ClawWork/wiki/05-economics-scripts.md` == 1.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "component 05 extracted"` (own task only).

## Scope & constraints
- No `fleet` commands except `bd close`. No network (read local clone only). No secrets. NEVER write into the repo clone.
