> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Rubric Design: Fresh Start, Tone, and Judge Prompts

**In one sentence:** The chunk defines per-interruption recovery rubrics (fresh start, non-defensive tone, concern addressed) and the two strict JSON-output judge prompts plus the six-agent generation pipeline that enforce them.

## Key points

- Fresh start requires the response to start a new utterance rather than resuming or completing the assistant's previously cut-off sentence.
- Non-defensive tone forbids dismissive or argumentative language such as "we already told you," "that's just the rule," or blaming the user.
- Concern addressed requires explicitly engaging the user's stated concern about "why are we verifying my case again?" with a reason (e.g., privacy/protection or confirming identity) instead of ignoring it.
- Evaluation uses two judge prompts, both requiring structured JSON output: a comparative Task Fulfillment judge and an absolute pass/fail Recovery Quality judge.
- The Task Fulfillment judge picks winner A or B solely on the given criterion, ignoring naturalness, grammar, tone, length, or recovery style, and "more detail / longer" alone is not a valid reason.
- The Recovery Quality judge assesses each listed criterion independently and returns PASS only if every criterion is met, with no added criteria and no penalty for behaviors outside the list.
- The data generation pipeline uses six LLM-prompted agents whose user-prompt templates inject domain, goal, knowledge base, conversation history, and task-specific fields, then request JSON-only output.

---

## Recovery rubric criteria

The chunk lists numbered criteria (example shown for a verification-concern case):

1. **Fresh start:** "The response does not resume or complete the assistant's previously cut-off sentence and instead starts a new utterance."
2. **Non-defensive tone:** "The response contains no dismissive or argumentative language (e.g., no phrases like "we already told you," "that's just the rule," or blaming the user)."
3. **Concern addressed:** "The response explicitly acknowledges and engages with the user's stated concern about "why are we verifying my case again?" by giving a reason (e.g., privacy/protection or confirming identity) rather than ignoring the question."

## Evaluation prompts

"We present the two judge prompts used at evaluation time." — "Both require structured JSON output."

### H.1 Task Fulfillment Judge

System prompt role: "You are a strict judge for spoken dialogue systems." It evaluates "how well an assistant fulfills its task after being interrupted mid-utterance" given a conversation history, a single evaluation criterion, and two candidate responses (A and B), and must determine "which response better satisfies the evaluation criterion."

Transcript format (verbatim rules):

- "If an assistant message ends with <INTERRUPTED />, it was cut off at that exact point. The rest was never delivered."
- "A user message wrapped in <INTERRUPTION>...</INTERRUPTION> is what the user said while interrupting."

Judgment rules:

- "Judge ONLY based on the evaluation criterion. Not naturalness, grammar, tone, length, or recovery style."
- "If neither response satisfies the criterion, pick the one that comes closer."
- "'More detail', 'more comprehensive', 'more specific', or 'longer' are NOT valid reasons to prefer one response. Only prefer a response if it more directly and concretely satisfies the evaluation criterion."
- "You MUST pick a winner. You MUST name a concrete way the loser fails or falls short of the evaluation criterion."

Output: "<TaskFulfillmentJudgment> (rationale_a, rationale_b, comparison_rationale, choice ∈ {A, B})." — "The rationales for A and B must be independent and not" [chunk ends mid-sentence].

### Recovery Quality Judge

System prompt role: "You are a strict pass/fail judge for spoken dialogue systems. You evaluate whether an assistant's response correctly recovers from a user interruption." Inputs: "A conversation history where the assistant was interrupted," "A list of criteria that the response MUST satisfy for a PASS," and "The assistant's response to evaluate." Same transcript format for `<INTERRUPTED />` and `<INTERRUPTION>...</INTERRUPTION>`.

Judgment rules:

- "Assess each criterion independently. For each, determine if the response satisfies it (true/false) with a brief rationale."
- "Be strict: "close enough" is not a pass. The criterion must be clearly satisfied."
- "Do not introduce your own criteria beyond what is provided. Judge only on what is listed."
- "Do not penalize the response for behaviors not covered by the criteria."
- "The overall verdict MUST be mechanically consistent with the individual assessments: - PASS: ALL criteria are met (every assessment has met = true) - FAIL: ANY criterion is not met (any assessment has met = false). Do NOT override this rule for any reason."

Output: "<RecoveryQualityJudgment> with per-criterion assessments, overall_rationale, and verdict ∈ {pass, fail}."

## Generation pipeline prompts

"The data generation pipeline uses six LLM-prompted agents." — "We present the full system prompts for each, with minor formatting edits for readability." — "User prompt templates follow a consistent pattern: they inject the domain, goal, knowledge base, conversation history, and task-specific fields into the context, then request JSON-only output."

### I.1 System Message Writer

"The system message writer generates the assistant's operating instructions (system prompt) from the domain, goal, and knowledge base." — "The output is used directly as the assistant model's system prompt during both synthesis and evaluation." — "An example output is shown in Appendix G." System prompt begins: "You are a careful benchmark data generator."

**Covers:** Per-interruption rubrics, task-fulfillment and recovery-quality criteria (Appendix H evaluation prompts; Appendix I generation pipeline, I.1 System Message Writer)
