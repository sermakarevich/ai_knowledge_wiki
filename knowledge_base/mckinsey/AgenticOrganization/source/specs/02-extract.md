# AgenticOrganization chunk 02 extract

## Problem
Write wiki page `wiki/02-pillars-close.md` for the `AgenticOrganization` entry from exactly one transcript chunk (McKinsey podcast, Krivkovich + Rahilly). The worker sees only this spec + the chunk.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/structured_papers/mckinsey/AgenticOrganization/source/chunks/02.txt` (plain text, ~9323 chars). Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else.
2. Write `/Users/sergii/.ai/knowledge/structured_papers/mckinsey/AgenticOrganization/wiki/02-pillars-close.md` COMPLETELY (overwrite on retry) with the wiki-page format contract: backlink line `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`, `# Remaining pillars and close`, `**In one sentence:**`, `## Key points` (5-8 complete claims with the podcast's numbers/examples), `---`, full detail in `##` subsections, attribute claims to speaker where it matters, footer `**Covers:** closing half`. No meta-junk.
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/structured_papers/mckinsey/AgenticOrganization/wiki/02-pillars-close.md && wc -l /Users/sergii/.ai/knowledge/structured_papers/mckinsey/AgenticOrganization/wiki/02-pillars-close.md` >= 40; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/structured_papers/mckinsey/AgenticOrganization/wiki/02-pillars-close.md` == 1.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "chunk 02 extracted"` (own task only).

## Scope & constraints
- No `fleet` commands except `bd close`. No network. No secrets.
