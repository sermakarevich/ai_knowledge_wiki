# Spotify Portal article (ai:summary:get, full depth)

## Problem
Spotify Engineering (Sept 2026) reports "Portal" cut their Claude Code token usage by 90% — directly relevant to harness cost engineering. No KB entry exists.

## Fix
This is an `ai:summary:get` order for https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90 . BEFORE ANYTHING ELSE run `ai show summary/get` and read the whole recipe, then follow it exactly (full wiki pipeline — NOT --fast).
- Folder (cwd `/Users/sergii/.ai`, PascalCase, NO date prefix): `knowledge/research/SpotifyPortal/` (scaffold already exists with `source/specs/` — build the rest). If `knowledge/research/SpotifyPortal/summary.md` already exists when you start, STOP and close with reason "already exists".
- Capture: what Portal is, which mechanisms cut tokens (caching? compaction? routing? smaller models? — verify against the article, never invent), measured numbers, limits/caveats, transferability to other harnesses.
- `wiki/targeted.md` answering: (1) the 90% broken down by mechanism; (2) what generalizes beyond Spotify's setup; (3) failure modes and what got worse.
- Style: simple language, abbreviations first use. Claims vs evidence separated in critical_thinking.md.

## Tests
- `ls knowledge/research/SpotifyPortal/summary.md knowledge/research/SpotifyPortal/index.md knowledge/research/SpotifyPortal/wiki/targeted.md` all exist; `wc -l knowledge/research/SpotifyPortal/summary.md` >= 60; `ls knowledge/research/SpotifyPortal/wiki/*.md | wc -l` >= 4.

## DoD
1. tests green.
2. `git add knowledge/research/SpotifyPortal` then `git commit -m "papers(Portal): Spotify token-cut writeup"`. NEVER `git add -A`/`.`/`-a`, NEVER reset/checkout/stash/restore — shared tree.
3. verify: `git show HEAD --stat | grep -c SpotifyPortal` >= 1.
4. `bd close <your-id> --reason "Portal landed"` — only your own task.

## Scope & constraints
- cwd `/Users/sergii/.ai`. Do NOT run `fleet serve restart` / `fleet run`. Do NOT touch other research/, tutorials/, or specs/. Web reads only. No secrets.
