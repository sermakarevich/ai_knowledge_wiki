> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Score

**In one sentence:** A Score rates content against ordered descriptive levels and returns a fractional position plus per-level probabilities and confidence, so code can rank, threshold, and combine one-dimension judgments with explicit weights.

## Key points

- Use a Score when the answer is a position on a spectrum describable in steps (bug severity, customer happiness, candidate experience); for unordered fixed options use a Choice, for yes-or-no use a Noul.
- A Score answer is a `score` that can fall between two levels, a `probabilities` map over every level summing to 1, a `legend` mapping level numbers back to descriptions, and a `confidence` from 0 to 1 computed from the spread.
- The score is the probability-weighted mean of the level numbers: the reference bug report scores 0 × 0.0 + 1 × 0.70 + 2 × 0.30 = 1.30 at confidence 0.54, i.e. mostly level 1 with weight on level 2.
- Each level is judged on its own against the state — the model sees descriptions only, never level numbers or neighbors — so describe situations, not degrees ("Broken or degraded feature, but workaround exists", not "Moderately severe").
- Criteria take 2 to 10 levels; use as many as can be described distinctly, keep each Score to one dimension, and give rare must-act-on extremes their own level.
- Different distributions can yield the same score (all mass on level 1 vs. half on 0 and half on 2), so always read `probabilities` and `confidence` alongside the score before rounding or ranking.
- Split complex judgments into one Score per dimension, normalize each by dividing by its top level number `len(criteria) − 1`, and combine with weights in code — the reference priority is 0.6 × 0.62 + 0.3 × 0.725 + 0.1 × 1.0 = 0.6895 ≈ 0.69 (the Composite scoring pattern).

---

## Definition and when to use it

Verbatim definition from the source:

> "A Score is a System One question type for rating content against ordered, descriptive levels. The answer includes a score, a probability for each level, and confidence."

Selection rule: "Use a Score when the answer is a position on a spectrum you can describe in steps. For example, how severe a bug is, how happy a customer is, or how much Python experience a candidate has. If the answer is one of a fixed set of options with no order between them, use a [Choice](/primitives/choice). If it's a yes or no, use a [Noul](/primitives/noul)."

Example Score questions from the source:

```
"How severe is the bug being reported?"
  → 0: Cosmetic; no impact to functionality
  → 1: Broken or degraded feature, but workaround exists
  → 2: Blocking issue; no workaround exists

"How formal is this outfit based on the description"
  → 0: gym clothes → 1: casual → 2: business casual → 3: formal → 4: black tie

"How relevant is this candidate's experience to the job posting"
  → 0: completely unrelated → 1: adjacent field → 2: some direct experience → 3: deep, direct experience
```

## Request structure

Same three top-level fields as any question type: `state`, `model`, `questions`. Each Score question has:

| Field | Value |
|---|---|
| `type` | Always `"score"` |
| `instructions` | The question the model answers — what it is rating |
| `criteria` | An ordered array of level descriptions, low end to high end; at least two levels, up to 10 |

Reference request: state `'The export button crashes the settings page in Safari. It works in Chrome, but a few of our customers only use Safari.'`, model `jev-latest`, question id `bug_severity` with instructions `'How severe is the reported issue?'` and the three cosmetic/workaround/blocking levels. "You choose the question id ... This id is not sent to the model."

### Levels

"Each entry in `criteria` is a level: one point on the spectrum of possible answers, described in words. A level's number is its position in the `criteria` array, starting at 0." The model "gets the descriptions and nothing else, and each level is judged on its own against the state." The response `score` "is a position on the levels spectrum. For a three-level scale it runs from 0 to 2, and it can land between two levels." Typed SDK equivalent is Python `Score`; call via `system_one` or `https://api.typesafe.ai/v1/systemone`.

## Response structure

Response to the reference request (`usage`: `input_tokens` 332, `output_tokens` 18): `score` 1.3, `confidence` 0.54, `legend` mapping `"0"`, `"1"`, `"2"` back to the three descriptions, `probabilities` `{"0": 0.0, "1": 0.7, "2": 0.3}`.

Each Score answer has five values:

- `type`; `probabilities` (per level, keyed by level number as a string, summing to 1); `score` ("each level number multiplied by its probability, added up: 0 x 0.0 + 1 x 0.70 + 2 x 0.30 = 1.30"); `legend`; `confidence` ("A single peak on one level means high confidence. Probability spread over several levels means low confidence").
- Reading: "A score of 1.30 means mostly level 1 with some weight on level 2 ... the export is broken, and switching to Chrome is a workaround for most customers, but not for the ones who only use Safari."
- SDK note: "Using the Python SDK, `ScoreAnswer` has `score`, `confidence`, `probabilities`, and `legend` as typed fields. The SDK keys `probabilities` and `legend` by integer level rather than by string."

## Reading a Score

Five bug reports against `"How severe is the reported issue?"` (0 cosmetic / 1 workaround / 2 blocking):

| State | `score` | `confidence` | L0 | L1 | L2 |
|---|---|---|---|---|---|
| The export button is misaligned by a few pixels on the settings page. | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 |
| The PDF export button does nothing when clicked. I can still export to CSV and convert it myself, but that takes ages. | 1.0 | 1.0 | 0.0 | 1.0 | 0.0 |
| Export to PDF fails with a spinner that never finishes. Some of our team say CSV export still works for them, others say it fails too. | 1.12 | 0.81 | 0.0 | 0.88 | 0.12 |
| The export button crashes the settings page in Safari. It works in Chrome, but a few of our customers only use Safari. | 1.3 | 0.54 | 0.0 | 0.7 | 0.3 |
| Nobody on our team can log in since this morning. We get a 500 error on every attempt. | 2.0 | 1.0 | 0.0 | 0.0 | 1.0 |

Interpretation rules from the source:

- "confidence 1.0 means the returned distribution puts all its probability on one level. This describes the model's answer, not a guarantee that the answer is correct."
- "The score is a probability-weighted mean of the level numbers ... It does not measure the fraction of customers without a workaround."
- "Different distributions can produce the same score. A score of 1.0 can mean all probability is on level 1, or half is on each of levels 0 and 2. Read `probabilities` and `confidence` alongside the score."
- "A fractional score is a position. You can use it to rank reports by severity, or round it to the nearest level when your code needs one outcome."
- "Low confidence on a Score usually means one of three things. The levels overlap for this state, the question is measuring more than one thing, or the state doesn't say enough to place it."

## Writing good levels

- "Describe situations, not degrees. 'Broken or degraded feature, but workaround exists' gives the model something to match the state against. 'Moderately severe' doesn't. Concrete descriptions can help the model distinguish levels. Check the answers against known examples; higher confidence alone does not show that a description is better."
- "Every level is evaluated separately. The model doesn't see a level's number or its neighbours, so 'worse than the previous level' means nothing to it, and numbers in the descriptions or the instructions don't help." Evidence: with `criteria: ["0", "1", "2"]` the misaligned-button report scores 0.57 at confidence 0.35 (probabilities 0: 0.43, 1: 0.57, 2: 0.0), versus 0.0 at confidence 1.0 with descriptive levels — "With numbers only, the model has nothing to match against and splits the probability between 0 and 1."
- "Use as many levels as you can describe distinctly, up to 10. Three is fine. Don't add levels you can't describe distinctly."
- "Keep each Score to one dimension. If a description says 'punctual and smart and experienced', the question is measuring three things ... Split it into one Score per thing and combine them in code."
- "If the top of your scale has a rare extreme case you need to act on differently, give it its own level. A sentiment scale that ends at 'very angry' can add 'abusive or threatening'."
- "If there is no in-between at all, and the answer is one of a few discrete categories, use a [Choice](/primitives/choice) instead, or split the question into several [Noul](/primitives/noul) questions. It's important to test your levels against your own data. Two wordings of the same scale can behave differently on your data."

## Splitting a complex judgment into several Scores

"Send the Scores in one request. They are evaluated in parallel. Adding questions barely changes the response time and costs a few extra question tokens." Reference: three Scores on the spinner ticket — `severity` 1.24 at 0.63 (probabilities 0.0/0.76/0.24), `frustration` 1.45 at 0.33 (0.0/0.55/0.45 — civil wording but "third time" and "I'm done" split civil/very-angry), `report_quality` 3.0 at 1.0 (steps and browser version both stated; four-level scale). Response `usage`: `input_tokens` 468, `output_tokens` 43.

Combining: "Divide each score by its top level number, `len(criteria) - 1`, to put every score on 0 to 1. Then the weights mean what they say: 0.6 on severity and 0.3 on frustration makes severity count twice as much." Normalized: severity 0.62, frustration 0.725, report_quality 1.0; priority `0.6 × 0.62 + 0.3 × 0.725 + 0.1 × 1.0 = 0.6895`, rounded to `0.69`. "The weights live in your code, so you can see exactly how the number is made and change it when the ranking doesn't match what your team would do." This is the Composite scoring pattern.

## Structured level descriptions

"When the model keeps scoring between two neighbouring levels on inputs you think are clear, give each level an object instead of a string, with a field for what the level covers and a field with a few example situations. Use the same field names on every level." The spinner ticket with `{what, examples}` levels scores 1.06 at 0.91 confidence (probabilities 0.0/0.94/0.06) versus 1.12 at 0.81 with plain strings.

Safari-report comparison from the source:

| Level description | `score` | `confidence` |
|---|---|---|
| plain string: no object with examples | 1.30 | 0.54 |
| Added examples array with useful example: "export fails in one browser but works in another" | 1.07 | 0.90 |
| Added examples array with example unrelated to browsers: "search fails, but browsing categories still works" | 1.28 | 0.57 |

"Examples steer the model, and they only help when they look like your real inputs ... Higher confidence does not establish which answer is correct. Choose examples with known expected levels, then test the revised descriptions on separate inputs before keeping them."

**Covers:** https://docs.typesafe.ai/primitives/score
