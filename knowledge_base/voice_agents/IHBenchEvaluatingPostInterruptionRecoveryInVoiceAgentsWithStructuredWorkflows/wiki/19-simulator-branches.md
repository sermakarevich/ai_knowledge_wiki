[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# User Simulator: The Normal Branch
**In one sentence:** The user simulator has interrupting and normal branches, where the normal branch omits interruption execution rules, truncation logic, and overlap time and produces only rationale and utterance.
## Key points
- The user simulator has two branches: the interrupting branch (when the round planner decided the user will interrupt) and the normal branch.
- The interrupting branch is substantially more complex because it must produce both the user's utterance and the exact truncation point in the assistant's message.
- The interrupting branch must also produce a realistic overlap time, in addition to the utterance and the truncated assistant utterance.
- The normal branch omits the interruption execution rules, truncation logic, and overlap time.
- The normal branch produces only rationale and utterance.
- Both branches share the same spoken dialogue requirements.
- Both branches share the rule that the user plan already encodes personality, and the simulator does not receive the raw user intent to prevent type contamination.
---
## The two branches
The chunk states:

> "The user simulator also has two branches: the interrupting branch (when the round planner decided the user will interrupt) and the normal branch."

> "The interrupting branch is substantially more complex because it must produce both the user's utterance and the exact truncation point in the assistant's message."

> "The normal branch omits the interruption execution rules, truncation logic, and overlap time. It produces only rationale and utterance."

## Shared rules
Both branches share the same spoken dialogue requirements and the rule that:

> "the user plan already encodes personality (the simulator does not receive the raw user intent to prevent type contamination)."

## Interrupting branch task (as shown on the same page)
The interrupting-branch system prompt excerpt defines the task as:

- Produce the user's next utterance that INTERRUPTS the assistant, consistent with the user plan.
- Produce a truncated version of the assistant's most recent utterance showing where the user cut in.
- Produce a realistic overlap time.

Stated execution rules include:

- "You MUST interrupt. This is not optional."
- "Your utterance must match the interruption type."
- "The interruption must occur mid-thought, not after the assistant finishes."

Stated truncation procedure:

1. Take the assistant's most recent utterance AS-IS.
2. Pick a cutoff word based on the timing explanation.
3. Copy every character from the start up to and including the cutoff word.
4. "Do NOT change, rephrase, reorder, add, or drop a single word or character."

**Covers:** I.4 User Simulator — normal vs. interrupting branches and utterance generation (chunk 19/20)
