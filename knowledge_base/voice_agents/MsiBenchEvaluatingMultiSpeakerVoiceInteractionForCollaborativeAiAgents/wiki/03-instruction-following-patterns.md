[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Instruction-following patterns
**In one sentence:** The chunk completes selective disclosure as audience design, defines the speaker-authority constraint on authorization tracking, and introduces multi-speaker reasoning patterns for sequential constraint integration, request ownership, and constraint prioritization.
## Key points
- Selective disclosure measures audience design: the model must maintain a separate knowledge state per listener, withholding restricted values from that audience while preserving any legitimate non-disclosing action commissioned earlier.
- Speaker authority constraint tests authorization tracking when an unauthorized participant asks the assistant to execute an action controlled by another speaker through ownership, account, role, permission, or responsibility.
- Under speaker authority, the model must execute only the approved scope when the authorized speaker approved the exact action, refuse the unauthorized override when it was explicitly rejected, or check with the authorized speaker when genuinely undecided.
- Sequential constraint integration tests reasoning over interleaved speaker constraints: speakers interleave separate requests and corrections concerning different items, actions, or outcomes.
- Request ownership must be preserved through the compressed final handoff: a later line that resembles an override of someone else's request may actually correct the speaker's own request or add a separate one, and the model must not merge the threads into one plan.
- Constraint prioritization tests choosing a feasible action when an inviolable requirement conflicts with a tradeable preference: difficulty comes from reasoning about relative priority of deadlines, safety or policy rules, medical or accessibility needs, or physical impossibility.
- Under constraint prioritization the model must first satisfy the hard requirement with a feasible action, then retain soft preferences only where they remain compatible.
---
## Selective disclosure (tail)
**Covers:** Section 3.1 tail ("those facts in the final line")

The pattern measures audience design, "the ability to maintain a separate knowledge state per listener: the model must withhold the restricted values from that audience while preserving any legitimate non-disclosing action commissioned earlier."

## Speaker authority constraint
**Covers:** Section 3.1 (instruction-following patterns)

> "An unauthorized participant asks the assistant to execute an action controlled by another speaker through ownership, account, role, permission, or responsibility. The authorized speaker has explicitly approved the exact action, explicitly rejected it, or remained genuinely undecided."

"The pattern measures the ability to track authorization: the model must respectively execute only the approved scope, refuse the unauthorized override, or check with the authorized speaker before acting."

## Multi-speaker reasoning
**Covers:** Section 3.1–3.2 heading ("Multi-Speaker Reasoning")

### Sequential constraint integration
"Speakers interleave separate requests and corrections concerning different items, actions, or outcomes."

### Request ownership
"A later line may resemble an override of someone else's request while actually correcting the speaker's own request or adding a separate one. The pattern measures the ability to keep each remembered item attached to the speaker who produced it: the model must preserve request ownership through the compressed final handoff instead of merging the threads into one plan."

### Constraint prioritization
"An inviolable requirement conflicts with a tradeable preference, while other preferences may remain compatible. Difficulty stems from reasoning about the relative priority of multiple constraints — for example, a deadline, safety or policy rule, medical or accessibility need, or physical impossibility. The model must first choose a feasible action satisfying the hard requirement, then retain soft preferences only where they remain compatible."

## Data-generation pipeline (Figure 2)
**Covers:** Figure 2 caption

> "Figure 2: MSI-Bench data generation pipeline. Inputs fix speaker count, language, topic, interaction pattern, scene, and acoustic assets. Planning produces the cast, script, primary goal, and background-audio bed. Generation expands the script into a dialogue ending in an assistant-directed handoff, and derives the atomic rubrics and function catalog. Synthesis renders each line as speech and mixes it over the background."

**Covers:** chunk 03-those-facts-in-the-final-line (selective-disclosure tail through Figure 2 caption)
