# React finalize-verify (Claude worker) — ONLY validation step

## Problem
All 3 chunk extracts for `HarnessEngineeringCourse` should be done. Verify every wiki page; requeue bad ones; build the digest skeleton.

## Fix
1. **Completeness gate.** List beads titled `HarnessEngineeringCourse component NN extract` (any suffix). If ANY still open/in-progress: create ONE successor verify bead (this same spec file, `--deps` the open ids), re-point the three synth beads at it (`bd dep add <synth> <new>`, `bd dep remove <synth> <own-id>`), close own bead `--reason "rearmed: chunks in flight"`, STOP.
2. **Verify each page** (`/Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/wiki/*.md`): exists, >40 lines, has `**In one sentence:**` + 5+ key bullets, covers the WHOLE chunk (read the TAIL — repetition-loop padding is a known failure), no meta-junk, format contract holds. Build GOOD/BAD lists.
3. **BAD non-empty:** per bad chunk count beads `HarnessEngineeringCourse component NN extract*` for attempts. Attempts < 3: delete bad page, create ONE retry (`--coder opencode --model opencode-go/muse-spark-1.3-contributor`, reuse `source/specs/NN-extract.md` verbatim). Attempts >= 3: write the page by hand from the chunk. Retries created → successor verify bead on them, re-point synths, close `--reason "rearmed: N requeued"`, STOP.
4. **Digest skeleton:** `python3 /Users/sergii/.ai/skills/summary/build_digest.py /Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse` (verbatim copy + FIVE_MOVES markers). Exit 1 → fix named pages, rerun.
5. Append verify section to `/Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/source/delegation_report.md`, then `bd close <own-id> --reason "all chunks verified; digest skeleton built"`.

## Tests
- `ls /Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/wiki/*.md | wc -l` >= 3; `test -f /Users/sergii/.ai/knowledge/research/HarnessEngineeringCourse/digest.md`.

## DoD
Tests green, report appended, close own bead only.

## Scope & constraints
- No git. No network. Cwd anywhere; all paths absolute above.
