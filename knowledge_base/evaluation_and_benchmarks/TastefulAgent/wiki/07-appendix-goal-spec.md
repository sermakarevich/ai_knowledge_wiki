> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix Goal Spec
**In one sentence:** The "Goal" appendix section specifies acceptance/rejection filters for judgment-benchmark samples plus the detour-generator prompts that ask for one genuine detour (poor approach pursued, wall hit, recovery) written as two neutral parallel next steps.
## Key points
- If the better option is already identifiable from pre-decision differences, the sample must be rejected.
- The prefix from the good trajectory before the start step must contain enough task context, and important task constraints must be preserved in the query even if they appear early in a transcript.
- Choices must describe the actual branch decisions at the same specificity and tone, must not mention scores, pass/fail, grader results, branch names, or hindsight, and must not use praise, blame, confidence, caution, or other wording that makes one option an obvious strawman — rejecting the sample if neutral parallel wording is not possible.
- A choice must not carry a branch's self-reported or predicted target metric when its direction makes that choice mechanically preferable (e.g. merely claiming a lower predicted loss); the decision procedure or controllable action must be described instead.
- The reason must identify post-decision trajectory evidence connecting the decision to the native outcome, and the timeline must be reconstructed before accepting: a score or artifact already existing before the proposed cut cannot be credited to the proposed next step.
- The proposed action must be new at the cut — reject if the same action was already executed before the cut or if cited post-decision evidence repeats pre-cut evidence — and only completed experiment outputs count as evidence, not scripts followed by timeout, OOM, interruption, or missing output.
- Claims or predictions written into an answer are not observed outcomes, validators prove only format/budget/schema constraints rather than task performance, actual implemented actions (not plans or filenames) must be compared with rejection when both branches implement the same approach, and failures rooted in submission/finalization protocol, timeout, crash, missing dependency, hard-coded answer, task-version mismatch, or instruction noncompliance must be rejected.
- Every evidence quote must be a literal excerpt from the cited trajectory step and is checked mechanically after generation, while the detour generator treats rejection as correct and preferred whenever a clean detour cannot be demonstrated or the better approach is only nameable with hindsight.
---
## Acceptance filters
**Covers:** chunk lines 4–33 (pre-decision checks through evidence-quote rule)

- Reject when the better option is already identifiable from pre-decision differences.
- The prefix from good_traj before good_start_step must contain enough task context.
- Preserve important task constraints in query even if they appear early in a transcript.
- Choices must describe the actual branch decisions, at the same specificity and tone.
- Do not mention scores, pass/fail, grader results, branch names, or hindsight in choices.
- Verbatim: "Do not put a branch's self-reported or predicted target metric in a choice when its direction makes that choice mechanically preferable (for example, merely claiming a lower predicted loss). Describe the decision procedure or controllable action instead."
- Verbatim: "Do not use praise, blame, confidence, caution, or other wording that makes one option an obvious strawman. If neutral parallel wording is not possible, reject the sample."
- Verbatim: "In reason, identify the post-decision trajectory evidence connecting the decision to the native outcome. If the outcome gap is not causally attributable to the decision, reject."
- Verbatim: "Reconstruct the timeline before accepting. A score or artifact that already existed before the proposed cut cannot be credited to the proposed next step."
- Verbatim: "The proposed action must be new at the cut. Reject if the same action was already executed before the cut, or if cited post-decision evidence repeats evidence already present before the cut. Re-running the same command is not a causal decision fork."
- Verbatim: "An experiment contributes evidence only when its output shows a completed result. Starting a script followed by timeout, OOM, interruption, or missing output is not a successful experiment."
- Verbatim: "Writing a claimed or predicted objective value into the answer is not an observed task outcome. A format, budget, or schema validator proves only those constraints; it does not independently validate task performance. If no post-decision evidence connects the differing action to the measured objective, reject the sample."
- Verbatim: "Compare actual implemented actions, not plans or filenames. If both branches implement the same underlying approach, reject even if their wording differs."
- Verbatim: "Reject when failure is mainly submission/finalization protocol, timeout, crash, missing dependency, hard-coded answer, task-version mismatch, or instruction noncompliance."
- Verbatim: "Every evidence quote must be a literal excerpt from the cited trajectory step. Evidence is checked mechanically after generation."

## Detour generator prompts
**Covers:** chunk lines 35–74 (system message, user message, Goal/Task/Native outcome/trajectory fields)

System message, verbatim: "You build judgment benchmark items from one real agent trajectory. Return one JSON object only. Ground every claim in exact excerpts from the supplied steps. Treat rejection as a correct and preferred result whenever a clean detour cannot be demonstrated, or whenever the better approach is only nameable with hindsight."

User message goal, verbatim: "Find one genuine DETOUR in this single trajectory: the agent committed to a poor technical approach, pursued it, hit a wall, and recovered with a better approach that worked. Write the fork as two neutral, parallel candidate next steps."

Fork definitions from chunk:

| Field | Meaning in chunk |
|---|---|
| bad_choice | the poor approach the agent committed to first |
| good_choice | the better approach it recovered to |

Prompt placeholders/sections in chunk order: `# Goal`, `# Task` (`{query}`), `# Native outcome` (`{outcome_note}`), `# Complete trajectory` (`trajectory_id: {trajectory_id}`, `{trajectory}`).
