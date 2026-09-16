# AmuxHarnessGuide — delegation report

Source: https://amux.io/guides/harness-engineering/
Method: get_local (fleet extracts + Claude finalize).

## Verify (fleet-5myvy, 2026-09-12)

Completeness gate: all 3 `AmuxHarnessGuide chunk NN extract` beads closed (fleet-aqd3e, fleet-9t91q, fleet-x54w7). No requeue needed.

Page verification (exists, >40 lines, `**In one sentence:**` + ≥5 key bullets, tail coverage, no meta-junk, format contract):
- `wiki/01-concept-formula.md` — GOOD (117 lines, 7 key bullets, tail covers the 10-components table).
- `wiki/02-ratchet-build.md` — GOOD (120 lines, 7 key bullets, tail covers multi-agent orchestration + proof points).
- `wiki/03-evidence-practices.md` — GOOD (129 lines, 7 key bullets, tail covers FAQ + "August 2026" additions, no repetition-loop padding).

No BAD pages; no retries required.

Digest skeleton: `python3 skills/summary/build_digest.py .../AmuxHarnessGuide` → exit 0, wrote `digest.md` from 3 pages.

## Synth (fleet-gjqqb, 2026-09-12)

Completeness gate: explainer.md and questions.md present, digest.md has no `_TODO`, all deps (fleet-he9pu, fleet-mgzfo, fleet-x8u3b) closed. Proceeded.

Spot-check: explainer.md (9.3KB, 9 sections, jargon decoder, no repetition tail), questions.md (6 questions across all 3 digest sections, each ≥1), spine in digest.md (7 lines in FIVE_MOVES markers, within 5-7 range). All GOOD — no rewrite needed.

Wrote judgment-heavy files:
- `summary.md` — Article template, rung-1 shallow TL;DR.
- `critical_thinking.md` — flagged this guide as amux.io vendor content (its own FAQ maps every harness component onto its own product); distinguished corroborated framework claims (guides/sensors, ratchet principle, independently backed by OsmaniHarness) from unsourced round-number statistics (~70%/~100%, Atlan figures, IT-leader survey) and the self-interested amux-as-complete-harness claim. Verdict: Trial.
- `connections.md` — linked OsmaniHarness (closest sibling, independent corroboration), TheHarnessEffect (controlled evidence this guide's claims lack), ScalingTheHarnessInAgenticAI (same thesis, academic framing), SelfRefine (guides-without-sensors failure mode demonstrated empirically).
- `index.md` — OKF front-matter, reading ladder, wiki table, source line.
- Appended Q7 (evaluation) to questions.md linking critical_thinking.

Tests: `ls index.md summary.md critical_thinking.md connections.md` — all exist. Closing own bead.
