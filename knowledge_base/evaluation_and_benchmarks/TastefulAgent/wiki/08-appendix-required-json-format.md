> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Required JSON Format
**In one sentence:** The appendix specifies the exact JSON schema miners must return for each taste fork, with mechanical ordering and evidence rules, plus the shared four-judge panel and both filter prompts, and reports the per-stage filtering yield.

## Key points
- Miners must return exactly one object with `is_good_sample`, `reason`, `query`, `breakpoint_step`, `good_choice`, `bad_choice`, and `evidence` containing `bad_action`, `wall`, `recovery_action`, and `success` steps with literal quotes.
- Ordering is checked mechanically: `breakpoint_step <= bad_action.step <= wall.step < recovery_action.step <= success[*].step`, with `bad_action` and `wall` allowed to cite the same step when one message contains both commitment and failure.
- The wall must be an observed failure (non-zero exit, error, traceback, "not found", failing assertion, explicitly reported failing result); a remark that something could improve, clean diff, or successful command is not a wall, and fabricated walls are discarded.
- Forks are rejected when the recovery is only nameable after seeing the failure (hindsight lookup, e.g. "revert the file the traceback names"), with preference for rejection when unsure; mid-rollout discoveries (missing tool/dependency/broken toolchain) require relocating the fork to mine the second cycle instead.
- Both options must be live candidates a competent engineer could plausibly pick from the prefix alone — no strawmen (e.g. repeating an action the prefix already shows failing), no different subproblems, no mere execution ordering — phrased in strictly parallel form with no evaluative/leaking words, grades, step numbers, or wall error text.
- Both Section 3 filters use the same four-judge panel (Kimi K2.5, GPT-4.1, Llama 4 Maverick, Mistral Large 3, excluding the generator) with one shared system message and per-question shuffling of candidate order.
- Of 4,657 mined candidate forks, 1,809 pass the generator rubric, 729 survive the trivial filter, and 502 questions remain in the release (10.8%); detour-research questions come from two passes (40 from 896 trajectories, then 24 from 437 further trajectories).

---

## Required JSON schema
**Covers:** pp. 17–18, "Required JSON" object specification

Return exactly one object with:
```json
{
  "is_good_sample": "true or false",
  "reason": "brief, step-grounded reason",
  "query": "self-contained task statement preserving important constraints",
  "breakpoint_step": "integer index where the prefix ends; the agent is AT the fork and has NOT yet committed to the poor approach",
  "good_choice": "1-3 sentence neutral next step",
  "bad_choice": "1-3 sentence neutral next step",
  "evidence": {
    "bad_action": {"step": "integer", "quote": "exact excerpt committing to the poor approach"},
    "wall": {"step": "integer", "quote": "exact excerpt of the observed failure that ended it"},
    "recovery_action": {"step": "integer", "quote": "exact excerpt committing to the recovery"},
    "success": [
      {"step": "integer", "quote": "exact excerpt showing the recovery worked"}
    ]
  }
}
```

## Rubric requirements
**Covers:** pp. 17–18, Requirements list

- Ordering is mandatory and checked mechanically: `breakpoint_step <= bad_action.step <= wall.step < recovery_action.step <= success[*].step`; `bad_action` and `wall` MAY cite the same step when one message contains both the commitment and the failure it produced (common when a command and its output are narrated together).
- Every quote must be a literal excerpt from the step it cites.
- The wall must be an OBSERVED FAILURE: "a non-zero exit, an error, traceback, 'not found', failing assertion, or an explicitly reported failing result"; "Your own remark that something could be improved, a clean diff listing, or a successful command is NOT a wall."
- `steps[0:breakpoint_step]` is the prefix shown to a test-taker: it "must carry enough context to reason, and must NOT reveal the failure, the wall, or the eventual fix."
- Rejection on hindsight: "REJECT if the recovery is only nameable after seeing the failure. Ask: standing at breakpoint_step with the prefix alone, could a competent engineer have proposed good_choice? 'Revert the change to the file the traceback names' or 'raise the timeout the error reports' are hindsight lookups, not taste. This is the most common way a candidate fails; prefer rejection when unsure."
- Mid-rollout discovery rule: "When the deciding fact is discovered mid-rollout (a missing tool, an unavailable dependency, a broken toolchain), do NOT reject on that ground. RELOCATE the fork to after the discovery and mine the SECOND cycle." Worked example given: "Step 20 prints 'go: command not found'. Put breakpoint_step at 21, so the prefix already establishes there is no host toolchain. bad_action (step 21) = probing the filesystem for a stray Go install; wall (step 24) = that install being the wrong version for the repo's go.work; recovery_action (step 26) = building in a pinned container." Reject on this ground "only when the rollout contains no such usable second cycle."
- Valid environment-strategy forks are accepted: "ACCEPT a fork where genuinely different strategies were available, INCLUDING strategy about how to obtain a working environment or a trustworthy verification path. Real examples of valid forks: run the suite in a pinned container versus probe the host for a toolchain; declare pinned dependencies for an isolated run versus assemble a PYTHONPATH out of scavenged directories; write a narrow stubbed probe versus stand up the whole application stack."
- "BOTH OPTIONS MUST BE LIVE CANDIDATES. Someone who sees only the prefix must be able to pick either one plausibly"; neither may be a strawman — "an option that merely repeats an action the prefix already shows failing – 'keep calling the binary the prefix just reported as not found' – is a strawman, and so is any option nobody would actually propose at that point"; "This is the single most common reason a candidate is thrown out downstream."
- "REJECT if the agent never actually committed to the poor approach (it only mused about it), or if the 'recovery' is the same underlying approach with different wording."
- "REJECT if the two choices address different subproblems, or if the fork is mere execution ordering rather than a technical-judgment fork."
- Parallel phrasing: "same length range, same specificity, same tone. No evaluative or leaking words ('correctly', 'mistakenly', 'as it turns out', 'better', 'should', 'properly'). No mention of grades, failures, hindsight, step numbers, or which one the trajectory took." Also: "Do not put the wall's error text, file name, or symbol into good_choice when that alone identifies it as correct."

## Judges and filter prompts
**Covers:** p. 18, "The two filters of Section 3" plus system/user messages

- Panel: four judge models, not including the generator — "Kimi K2.5, GPT-4.1, Llama 4 Maverick, and Mistral Large 3"; all four cells use the same panel; both filters share one system message; candidate order shuffled per question.
- First filter shows only the two candidates; second filter shows the task, the prefix, the complete continuation of each candidate, and its recorded outcome.
- Judges, system message (verbatim):
  > "You are a reviewer at a real decision point. Choose the better next step from the task, trajectory prefix, and neutral options. End with exactly ANSWER: X."
- Trivial filter, user message (verbatim):
  > "# Candidate next steps / Option A: / {choice text} / Option B: / {choice text} / Without additional task or trajectory context, which option appears to be the better engineering decision? End with exactly ANSWER: X."
- Undecidable filter, user message (verbatim structure):
  > "# Task / {query} / # Shared trajectory before the decision / {prefix} / # Complete branch continuations / ## Option A / Proposed next step: / {choice text} / Trajectory continuation through its final step: / {steps from the decision point to the end of that branch} / ## Option B / (same) / # Feedback from native grader / {outcome standard of the dataset} / Option A: passed=...; score=... / Option B: passed=...; score=... / Which option produced the better outcome under the dataset's core metric? / End with exactly ANSWER: X."

## Counts at each stage
**Covers:** pp. 19–20, Section A.4 plus Figure 8 and Table 2

- "The generator rejects most candidate forks itself, because the rubric requires rejection whenever the evidence is not clean. The trivial filter removes a proposed question when all four judges answer it correctly from the two candidates alone, using the same threshold in all four cells. The undecidable filter keeps a question only when all four judges select the labeled candidate from the full record."
- Detour research: "the first pass over the 896 trajectories of the released pool produces 40 questions, and a second pass over 437 further trajectories produces the remaining 24."
- Figure 8 yield: "Of the 4,657 mined candidate forks, 1,809 pass the generator rubric, 729 survive the trivial filter, and 502 questions remain in the release."

| Cell | Proposed | Released |
|---|---|---|
| Parallel engineering | 562 | 124 |
| Parallel research | 186 | 48 |
| Detour engineering | 658 | 266 |
| Detour research, pass 1 | 241 | 40 |
| Detour research, pass 2 | 162 | 24 |

- Figure 8 band detail (per-cell generator → trivial survivors): detour engineering 658 → 320; detour research pass cells 403 → 124; parallel engineering 562 → 219; parallel research 186 → 66; undecidable survivors: 266 / 64 / 124 / 48; total "502 QUESTIONS · 10.8% OF 4,657".
- Trivial-removal example given: "Task. Build a Python module that uses GPT-3.5-turbo to generate Rust solutions to CodeContests problems, maximizing the percentage solved on a held-out test set. Candidate A. Build a solution that pattern-matches the three problems already verified to pass and returns their hardcoded Rust solutions, emitting an empty string for every other problem. Candidate B. Keep the general pipeline that classifies each problem's type and prompts GPT-3.5 with type-specific few-shot examples for all problems, and submit that as the final solution. Why it is removed. Every judge selects B from the two candidates alone, because candidate A describes itself as hard-coding three answers and returning nothing for the rest, so the question is answerable from the wording of the candidates alone, without the trajectory."

**Covers:** pp. 17–20, appendix "Required JSON" heading through the trivial-removal example
