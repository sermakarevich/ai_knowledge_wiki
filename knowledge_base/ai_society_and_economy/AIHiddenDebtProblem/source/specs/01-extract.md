# AIHiddenDebtProblem chunk 01 extract

## Problem
Write wiki page `wiki/01-thesis.md` for the `AIHiddenDebtProblem` video entry from exactly one transcript chunk (timestamps like [12:34] included). The worker sees only this spec + the chunk.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/source/chunks/01.txt` (timestamped transcript, ~29314 chars). Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else.
2. Write `/Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/01-thesis.md` COMPLETELY (overwrite on retry) with the wiki-page format contract: backlink line `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`, `# Thesis: AI's hidden debt`, `**In one sentence:**`, `## Key points` (5-8 complete claims), `---`, full detail in `##` subsections, timestamp refs like [12:34] for key claims, footer `**Covers:** opening third`. No meta-junk.
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/01-thesis.md && wc -l /Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/01-thesis.md` >= 40; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/01-thesis.md` == 1.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "chunk 01 extracted"` (own task only).

## Scope & constraints
- No `fleet` commands except `bd close`. No network. No secrets.
