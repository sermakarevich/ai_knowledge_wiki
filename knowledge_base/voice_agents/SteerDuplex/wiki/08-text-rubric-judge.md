> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Text Rubric Judge (D.4)
**In one sentence:** The text rubric judge scores one criterion at a time as "No Issues," "Minor Issues," or "Major Issues," explaining before rating and prioritizing content over delivery polish for speech.
## Key points
- Scores exactly one criterion at a time on a three-level scale: "No Issues," "Minor Issues," or "Major Issues".
- Explains its decision before giving the rating, and outputs JSON with reasoning placed before the rating.
- Receives criterion metadata (title, category, type, weight, and description) plus the latest user request and the assistant transcript.
- Treats explicit criteria as requiring direct answers, while implicit criteria may be inferred from context.
- Distinguishes objective criteria (factual correctness) from subjective criteria (quality).
- Ignores criterion weights during judging and tolerates minor formatting or phrasing differences.
- For speech, gives content priority over delivery polish.
---
## Text rubric judge (Section 3.3 / D.4)
**Covers:** Appendix D.4 Text Rubric Judge

The chunk defines the judge as scoring "one criterion at a time as "No Issues," "Minor Issues," or "Major Issues," explaining its decision before rating."

Inputs per judgment, verbatim from the chunk:

> "It receives criterion metadata (title, category, type, weight, and description), the latest user request, and the assistant transcript."

Interpretation rules, verbatim/paraphrased strictly from the chunk:

- "Explicit criteria require direct answers; implicit criteria may be inferred from context."
- "Objective criteria concern factual correctness, while subjective criteria concern quality."
- "The judge ignores criterion weights and tolerates minor formatting or phrasing differences."
- "For speech, content takes priority over delivery polish."
- "Output is JSON with reasoning before the rating."
