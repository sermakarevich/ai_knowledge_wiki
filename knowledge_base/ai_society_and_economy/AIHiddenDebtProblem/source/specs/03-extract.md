# AIHiddenDebtProblem chunk 03 extract

## Problem
Write wiki page `wiki/03-verdict.md` for the `AIHiddenDebtProblem` video entry from exactly one transcript chunk (timestamps like [12:34] included). The worker sees only this spec + the chunk.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/source/chunks/03.txt` (timestamped transcript, ~29179 chars). Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else.
2. Write `/Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/03-verdict.md` COMPLETELY (overwrite on retry) with the wiki-page format contract: backlink line `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`, `# Verdict and outlook`, `**In one sentence:**`, `## Key points` (5-8 complete claims), `---`, full detail in `##` subsections, timestamp refs like [12:34] for key claims, footer `**Covers:** closing third`. No meta-junk.
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/03-verdict.md && wc -l /Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/03-verdict.md` >= 40; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/research/AIHiddenDebtProblem/wiki/03-verdict.md` == 1.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "chunk 03 extracted"` (own task only).

## Scope & constraints
- No `fleet` commands except `bd close`. No network. No secrets.
