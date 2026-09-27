# RecursiveSelfImprovement chunk 04 extract

## Problem
Write wiki page `wiki/04-applications.md` for the `RecursiveSelfImprovement` entry from exactly one source chunk. The worker sees only this spec + the chunk — never the full paper.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/research/RecursiveSelfImprovement/source/chunks/04.txt` (plain text, ~38927 chars). If figures are listed below, read those image files too. Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else.
2. Write `/Users/sergii/.ai/knowledge/research/RecursiveSelfImprovement/wiki/04-applications.md` COMPLETELY (overwrite if it exists — retries reuse this spec) following this format contract exactly:
   - Backlink line: `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`
   - `# RSI across applications`
   - `**In one sentence:** <the section's whole argument in one sentence>`
   - `## Key points` — 5-8 bullets, each a complete claim with numbers/mechanisms/conclusions, never bare topic labels. This block feeds digest.md verbatim — make it carry the substance.
   - `---` then full detail in `##` subsections mirroring the chunk's structure. Tables, exact numbers, verbatim definitions where present. No meta-junk ("As an AI…"), no echoed spec text.
   - Footer: `**Covers:** section 4`
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/research/RecursiveSelfImprovement/wiki/04-applications.md && wc -l /Users/sergii/.ai/knowledge/research/RecursiveSelfImprovement/wiki/04-applications.md` >= 40 lines; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/research/RecursiveSelfImprovement/wiki/04-applications.md` == 1; `grep -c "^- " /Users/sergii/.ai/knowledge/research/RecursiveSelfImprovement/wiki/04-applications.md` >= 5.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "chunk 04 extracted"` — never exit rc=0 without closing; close ONLY your own task.

## Scope & constraints
- No `fleet` commands except `bd close`. No network. No secrets.
