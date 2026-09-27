# Manual review — chapter 03, answer_v1 (12 seeded traces)

Sample: 6 pass + 6 fail, `random.seed(42)`, ids sorted for reproducibility.

```
fails:   tkt-013, tkt-014, tkt-058, tkt-066, tkt-068, tkt-078
passes:  tkt-003, tkt-009, tkt-023, tkt-024, tkt-026, tkt-059
```

Each trace read via `viewer show --run answer_v1 <id>` and checked against the
gold answer points in `data/tickets/tickets.jsonl`.

| ticket | grader | mine | agree? |
|---|---|---|---|
| tkt-003 | pass   | pass | yes — 48-h collection + 5-day refund both stated |
| tkt-009 | pass   | pass | yes — $85.00 freight base stated |
| tkt-013 | fail   | fail | yes — omits the $25.00 expedited cost (missing_required_fact) |
| tkt-014 | fail   | fail | yes — asks for damage vs return clarification when ticket is a shipping/timeline Q (did_not_answer, missing_required_fact, wrong_section_retrieved) |
| tkt-058 | fail   | fail | yes — classifies snapped pole as major; gold says minor -> 15% discount (wrong_value, missing_required_fact) |
| tkt-066 | fail   | fail | yes — invents "bulk order" policy (unsupported_claim) |
| tkt-068 | fail   | fail | yes — conveys the 30-day rule (the gold fact) but invents a restocking fee (over_promise + unsupported_claim) |
| tkt-078 | fail   | fail | yes — privacy section never retrieved; 90-day audit fact absent (wrong_section_retrieved, unsupported_claim, missing_required_fact) |
| tkt-023 | pass   | pass | yes — "charged by your bank, not us" stated |
| tkt-024 | pass   | pass | yes — $5,000.00 credit limit + split-payment rule stated |
| tkt-026 | pass   | pass | yes — "5 to 10 business days" stated |
| tkt-059 | pass   | pass | yes — 48-h/3-photos + 10-day return both stated (grader read as pass even though the reply deflected on the manual-override ask; the two gold facts are the only criteria) |

## Result

n agree / disagree = **12 / 0**. No label flipped.

- **tkt-068** is the most instructive pass/fail near-miss: the reply *does*
  state the correct 30-day window (the reference-standard fact) but then invents
  a restocking fee and over-promises a resolution. Fail is correct on the
  fabrication; it confirms the taxonomy's `over_promise` mode is doing real
  work that the binary fact check alone would miss.
- **tkt-059** looks deflected (customer rejected the callback path), yet both
  gold facts are present, so it scores pass. The rubric is fact-grounded, not
  tone-grounded; a human customer would feel ignored. Worth a note in the
  findings, not a label change.
- **tkt-014** and **tkt-078** are the clearest retrieval-vs-generation splits:
  the gold section was never retrieved, and the model answered from whatever
  it had. `wrong_section_retrieved` is the right first-mode on those.

## Caveats (carried into `03_findings.md`)

- The grader sees the gold answer points; a human reviewer has to derive them
  from the handbook. Disagreement rates will only be higher with a real human
  reviewer on edge cases like tkt-059 / tkt-068.
- `viewer show` does not render the grader's raw signal fields (`missing_points`,
  `unsupported_claims`, `wrong_tone_or_promise`, `did_not_answer`) -- only the
  single-line note. Useful to see in chapter-03 context, but the raw flags are
  the grader's actual reasoning and should be visible on the viewer page.
