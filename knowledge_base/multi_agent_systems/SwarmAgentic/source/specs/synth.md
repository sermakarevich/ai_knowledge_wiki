# synth explainer+questions+spine: SwarmAgentic

Mechanical synthesis from SMALL inputs. Read `/Users/sergii/.ai/knowledge/research/SwarmAgentic/digest.md` + the wiki pages' key-points blocks only.

## Task — write three artifacts
1. `/Users/sergii/.ai/knowledge/research/SwarmAgentic/explainer.md`: plain-language layer for a smart non-expert — What is this about? / Why does it matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder. No new claims beyond the digest.
2. `/Users/sergii/.ai/knowledge/research/SwarmAgentic/questions.md`: retrieval practice, >=1 question per digest section, answers in collapsed `<details>` blocks; ~half core recall with numbers, ~a third "why / what breaks if", rest transfer. LEAVE OUT the final evaluation question (finalize adds it).
3. Digest spine: replace the `<!-- FIVE_MOVES_START/END -->` placeholder in `/Users/sergii/.ai/knowledge/research/SwarmAgentic/digest.md` with `## The argument in five moves`: 5-7 numbered one-clause steps = the paper's overall arc. Touch NOTHING else in digest.md.

Prose rules: flowing paragraphs, never one sentence per line; first-use-only abbreviation expansion.

## Tests
- `test -s /Users/sergii/.ai/knowledge/research/SwarmAgentic/explainer.md /Users/sergii/.ai/knowledge/research/SwarmAgentic/questions.md`
- `grep -c '^### Q' /Users/sergii/.ai/knowledge/research/SwarmAgentic/questions.md` >= 3
- `grep -c 'five moves' /Users/sergii/.ai/knowledge/research/SwarmAgentic/digest.md` >= 1 (case-insensitive: `grep -ci 'five moves'`)

## DoD (close-out shape c — shared tree)
1. Tests green (exact commands above).
2. `git add` ONLY the files named above (never `git add -A` / `.` / `-a`; never reset/checkout/stash/restore — shared tree).
3. `git commit -m "<msg>"`.
4. Verify: `git show HEAD:<path> | grep -c "<token>"` >= 1.
5. `bd close <your-own-id> --reason "<done>"`. Close ONLY your own bead. Never exit rc=0 without closing.

## Scope & constraints
- cwd: /Users/sergii/.ai. Touch ONLY the paths named above.
- Do not run `fleet serve restart` / `fleet run`. No live-LLM tests.
