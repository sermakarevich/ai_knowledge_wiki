[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Verification Modifier: Apply Only the Changes
**In one sentence:** The post-hoc modifier must apply only the targeted edit commands with minimal word changes while preserving TTS-friendly plain-text formatting and prefix invariants.
## Key points
- Apply only the changes described in the edit commands and do not rewrite, improve, or touch any untargeted message.
- Each edit command targets a specific message by index; modify only that message's content.
- Change as few words as possible to fix the described issue while preserving the rest exactly.
- If two edit commands target the same message, apply both changes.
- Maintain TTS-friendly formatting: numbers as words, currency spoken out, no markdown, no em dashes or semicolons.
- `modified_content` must be plain text only with no XML markup.
- `modified_original_content` is set if and only if modifying an interrupted assistant message, and then `modified_content` must be an exact prefix of `modified_original_content`.
- Do not proactively fix untargeted messages even if an edit creates downstream inconsistency; the verifier reruns and catches cascading issues next iteration, except mandatory filler-continuation coordination.
---
## Modifier edit rules
**Covers:** chunk 20/20, "1. Apply ONLY the changes" (verifier fix loop / modifier instructions)

1. Apply ONLY the changes described in the edit commands. Do not rewrite, improve, or touch any message that is not targeted.
2. Each edit command targets a specific message by its index. Modify only that message's content.
3. Change as FEW words as possible to fix the described issue. Preserve the rest exactly as it is.
4. If two edit commands target the same message, apply both changes.
5. Maintain TTS-friendly formatting: numbers as words, currency spoken out, no markdown, no em dashes or semicolons.
6. `modified_content` must be PLAIN TEXT ONLY, no XML markup.
7. `modified_original_content`: set IF AND ONLY IF modifying an interrupted assistant message. When set, `modified_content` MUST be an exact prefix of `modified_original_content.

## Interrupted messages and undelivered content
**Covers:** chunk 20/20, truncated-message extension rule

- "Some assistant messages were interrupted by the user. After the cutoff, an `<UNDELIVERED>` tag shows the portion not heard by the user."
- "When an edit command asks to extend a truncated message, use the undelivered text as source material. The modified_content should include the delivered content plus additional text up to the new cutoff point, as plain text."

## Filler continuation messages
**Covers:** chunk 20/20, continuation-to-source consistency rule

- "Some assistant messages are continuations of a prior interrupted message. In TTS, only ONE audio is generated for the source message's original_content."
- "When editing a filler continuation, you MUST also output a modification for the source message to keep original_content consistent."

## Cascading change prevention
**Covers:** chunk 20/20, no-proactive-fix policy

- "Do NOT proactively fix other messages not targeted by any edit command, even if your edit creates a downstream inconsistency."
- "Exception: filler continuation coordination is mandatory. The verifier will run again after modifications and will catch cascading issues in the next iteration."
- "Return ONLY the JSON object."
