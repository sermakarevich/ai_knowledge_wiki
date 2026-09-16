# LangChainCustomHarness chunk 02 extract

## Problem
Write wiki page `wiki/02-capabilities-fit.md` for the `LangChainCustomHarness` entry from exactly one source chunk. The worker sees only this spec + the chunk — never the full article.

## Fix
1. Read ONLY `/Users/sergii/.ai/knowledge/papers/LangChainCustomHarness/source/chunks/02.txt` (plain text, ~4444 chars). Do NOT read fleet artifacts/logs, sibling wiki pages, or anything else.
2. Write `/Users/sergii/.ai/knowledge/papers/LangChainCustomHarness/wiki/02-capabilities-fit.md` COMPLETELY (overwrite if it exists — retries reuse this spec) following this format contract exactly:
   - Backlink line: `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`
   - `# Harness capabilities and task-harness fit`
   - `**In one sentence:** <the section's whole argument in one sentence>`
   - `## Key points` — 5-8 bullets, each a complete claim with mechanisms/trade-offs, never bare topic labels. This block feeds digest.md verbatim — make it carry the substance.
   - `---` then full detail in `##` subsections mirroring the chunk's structure. Verbatim definitions and code/config where present. No meta-junk ("As an AI…"), no echoed spec text.
   - Footer: `**Covers:** capabilities + fit`
3. No git commands (repo auto-syncs). Touch ONLY the one output file.

## Tests
- `test -f /Users/sergii/.ai/knowledge/papers/LangChainCustomHarness/wiki/02-capabilities-fit.md && wc -l /Users/sergii/.ai/knowledge/papers/LangChainCustomHarness/wiki/02-capabilities-fit.md` >= 40 lines; `grep -c "^**In one sentence:**" /Users/sergii/.ai/knowledge/papers/LangChainCustomHarness/wiki/02-capabilities-fit.md` == 1; `grep -c "^- " /Users/sergii/.ai/knowledge/papers/LangChainCustomHarness/wiki/02-capabilities-fit.md` >= 5.

## DoD
1. Tests green.
2. `bd close <own-id> --reason "chunk 02 extracted"` — never exit rc=0 without closing; close ONLY your own task.

## Scope & constraints
- No `fleet` commands except `bd close`. No network. No secrets.
