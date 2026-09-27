# verify wiki: MechanicsOfSwarm

You are the ONLY validation step. Source: `/Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/source/full.md` (spot-check against it, do not rewrite everything).

## Task
1. Read all 4 wiki pages in `/Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/wiki/` (ignore `images/`).
2. Check each against the contract: backlink line, `**In one sentence:**`, `## Key points` with >=3 real-claim bullets, full detail, `**Covers:**` footer; no sentence-per-line; no invented claims (spot-check numbers against `source/full.md`).
3. Fix bad pages YOURSELF with bounded rewrites (one rewrite per page max — cheaper than requeueing).
4. Run the digest skeleton builder: `python3 /Users/sergii/.ai/skills/summary/build_digest.py /Users/sergii/.ai/knowledge/research/MechanicsOfSwarm` — it exits 1 naming contract violations; fix those pages and rerun until green.

## Tests
- `test -s /Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/digest.md`
- `ls /Users/sergii/.ai/knowledge/research/MechanicsOfSwarm/wiki/*.md | wc -l` >= 4
- `python3 /Users/sergii/.ai/skills/summary/build_digest.py /Users/sergii/.ai/knowledge/research/MechanicsOfSwarm` exits 0

## DoD (close-out shape c — shared tree)
1. Tests green (exact commands above).
2. `git add` ONLY the files named above (never `git add -A` / `.` / `-a`; never reset/checkout/stash/restore — shared tree).
3. `git commit -m "<msg>"`.
4. Verify: `git show HEAD:<path> | grep -c "<token>"` >= 1.
5. `bd close <your-own-id> --reason "<done>"`. Close ONLY your own bead. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai. Touch ONLY the paths named above.
- Do not run `fleet serve restart` / `fleet run`. No live-LLM tests.
