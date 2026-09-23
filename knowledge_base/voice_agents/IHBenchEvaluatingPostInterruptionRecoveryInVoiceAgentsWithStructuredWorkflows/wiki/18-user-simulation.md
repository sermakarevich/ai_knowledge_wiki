[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# User plan should reveal hidden info
**In one sentence:** The round planner forces `user_plan` to reveal hidden information gradually and plausibly through reactive, cutoff-grounded reactions — never verbatim confirmation, forward jumps, or state-machine leakage — with jointly consistent interruption timing and strictly isolated interruption types.
## Key points
- `user_plan` must reveal hidden info gradually and plausibly, with no verbatim confirmation: use "yes", "that's right", or shortened versions instead of repeating full details back.
- `user_plan` is reactive only (a reaction to what the assistant said, not an independent forward action) and must not jump ahead by volunteering information about a workflow step the assistant has not initiated.
- `user_plan` must not leak internal state: no references to internal stage names, workflow order, or KB details the user could not know.
- Interruption planning decides `will_include_interruption` from the interruption-profile probabilities, minima, and stats so far, and when true provides an `interruption_plan` with type and timing.
- The cut-in must be mid-thought during a key sentence that breaks stage progress — never in the last sentence, with sufficient remaining content after the cutoff — and the user plan must not depend on information from the unspoken remainder.
- Interruptions must be mid-stage (middle of executing a workflow stage, not at a clean boundary), pacing-driven (assistant says A then begins B, user cuts in to react to A), and cross-consistency-checked ("Given where I said the cutoff happens, has the user actually HEARD everything they act on in user_plan?").
- Each interruption type must be cleanly distinguishable with no blending of characteristics, and the round planner prompt includes detailed definitions for all six types (approximately 150 lines) specifying semantics, examples, and anti-patterns.
- User utterances can only reflect the truncated assistant portion with overlap times of 0.15–1.20 seconds (filler 0.15–0.50; impatient and correction 0.40–1.20), natural spoken dialogue with 1–3 mild imperfections per message, and JSON output with rationale, utterance, truncated_assistant_utterance, and overlap_time.
---
## User-plan reveal rules
> "user_plan should reveal hidden info gradually and plausibly."

- "NO VERBATIM CONFIRMATION: The user should not repeat full details back. Use "yes", "that's right", or shortened versions."
- "REACTIVE ONLY: The user_plan should describe a reaction to what the assistant said, not an independent forward action."
- "NO JUMPING AHEAD: The user MUST NOT volunteer information about a workflow step the assistant has not initiated."
- "No state-machine leakage: user_plan must not reference internal stage names, workflow order, or KB details the user could not know."

## Interruption planning and timing rules
- "Decide will_include_interruption based on the interruption_profile probabilities, the minima, and stats so far."
- "If true, provide interruption_plan with type and timing."
- "The cut-in MUST be mid-thought, not after a complete explanation. It MUST happen during a key sentence to break stage progress."
- "The cutoff MUST NOT be in the last sentence of the assistant's planned utterance. There must be sufficient remaining content after the interruption point."
- "The user plan MUST NOT depend on information from the unspoken remainder of the assistant's utterance."
- "MID-STAGE INTERRUPTION: The interruption MUST happen while the assistant is in the middle of executing a workflow stage, not at a clean boundary between stages."
- "PACING-DRIVEN: Prefer the pattern where the assistant says A then begins B, and the user cuts in to react to A."

## Cross-consistency check and type isolation
- "Cross-consistency check (mandatory): Before finalizing output, verify that user_plan and interruption_timing_explanation are jointly consistent. Ask: "Given where I said the cutoff happens, has the user actually HEARD everything they act on in user_plan?" If the user acts on something the assistant hasn't said yet at the cutoff, fix it before outputting."
- "Interruption type isolation: Each type must be cleanly distinguishable. Do NOT blend characteristics of multiple types in a single interruption."

## Six interruption-type definitions
The chunk states: "The round planner prompt also includes detailed definitions for all six interruption types (approximately 150 lines). These definitions specify the semantics, examples, and anti-patterns for each type:"

| Type | Definition in chunk |
|---|---|
| Normal | "A relevant, non-hostile cut-in where the user adds a detail, constraint, or asks a quick clarification. Must be unsolicited information, not a response to an explicit question." |
| Impatient | "The user cuts in to speed things up, skip explanations, or jump to the conclusion." |
| Correction | "The user corrects something they themselves previously stated in a prior turn. Must be a self-correction across turns, not a same-turn speech disfluency." |
| Topic switch | "The user abruptly introduces an unrelated request or question, derailing the current workflow stage." |
| Filler | "A brief, reflexive backchannel ("mm-hm", "yeah", "right") that carries no semantic content. The assistant should continue without pausing." |
| Pushback | "The user actively resists, challenges, or confronts the assistant. Sub-variants include resistance, disagreement, suspicion, and fact dispute. A grounding requirement ensures pushback references something the assistant has actually said." |

## Assistant simulator interruption-handling branch (as given in chunk)
- "The assistant simulator has two completely separate prompt branches to prevent cross-contamination: the interruption-handling branch (used when the most recent user message was an interruption) and the normal branch (no mention of interruptions). We present the interruption-handling branch in full."
- System prompt role: "You are simulating a spoken, call-style assistant. You are the ASSISTANT SIMULATOR for a STATE MACHINE assistant. In this turn, the most recent user message was an INTERRUPTION. Your primary job is to HANDLE the interruption correctly and then continue the workflow."
- Inputs received: "Domain, Goal, AssistantKnowledgeBase, Assistant plan (from the round planner), The interruption type that just occurred, Chat history with speaker labels."
- Task: "Handle the interruption according to the type-specific rules below. Then follow the assistant_plan for this turn. Produce a single spoken utterance."

Type-specific handling injected per turn:

| Injected rule | Verbatim behavior |
|---|---|
| NORMAL | "Acknowledge what the user said briefly and incorporate it if relevant. Continue from where you were cut off. Do NOT restart from the beginning." |
| IMPATIENT | "Respect the request. Do NOT repeat what you already said. Condense or skip the remaining explanation entirely. Jump to the actionable next step. Keep the response SHORT." |
| CORRECTION | "Acknowledge the correction briefly and naturally. Vary your phrasing. Update your understanding immediately. Do NOT question or challenge the correction." |
| TOPIC SWITCH | "Address the new topic briefly and helpfully if you can. Then steer back to the current workflow stage." |
| FILLER | "Your response MUST exactly continue the unfinished utterance from your most recent message. Do NOT repeat any word or phrase already said. Do NOT restart, reframe, summarize, or re-introduce anything. Do NOT acknowledge the filler. The result, when concatenated with your previous message, should read as one continuous utterance." |
| PUSHBACK | "Do NOT get defensive, dismissive, or argumentative. Acknowledge the user's concern directly and empathetically. Begin as a fresh utterance. Keep the response measured and calm. If the user insists on stopping, accept gracefully." |

Plan-following, naturalness, and non-hallucination rules in chunk:
- "The assistant_plan tells you WHAT to do. Follow it faithfully."
- "Convert the narrative plan into natural spoken dialogue. Do NOT add significant content that the plan does not mention."
- "If assistant_will_terminate is true, include a natural closing."
- "PREFER ONE ACTIONABLE QUESTION PER MESSAGE. NO RE-STATING KNOWN FACTS. NO ASKING ALREADY-ANSWERED QUESTIONS."
- "CONCISE DELIVERY: 1–3 sentences, not a paragraph."
- "You may only treat as facts: known_user_information, information provided by the user, and information you explicitly confirmed with the user."
- "NEVER leak record-level data to the user before they provide it themselves."
- "Natural spoken dialogue only. No markdown, bullet points, numbered lists, headings."
- "No em dashes, semicolons, parentheses, or stacked punctuation. Use contractions naturally. Short sentences."
- "Output: JSON with rationale and utterance fields only."

## User-utterance grounding, overlap, and spoken style
- "User utterance must match what was heard: The user can ONLY hear the truncated portion, NOT the full message."
- "If the assistant was going to mention an item after the cutoff, the user CANNOT reference it."
- "CROSS-CHECK EVERY DETAIL: verify that every specific detail in your utterance actually appears in the truncated_assistant_utterance or earlier history."
- Overlap time: "A float representing how many seconds the user overlaps (0.15 to 1.20 seconds). Filler: shorter overlaps (0.15–0.50). Impatient and correction: stronger overlaps (0.40–1.20)."
- "Spoken dialogue requirements: Natural spoken dialogue. No markdown. Use contractions. No emojis."
- "Add 1–3 mild imperfections per message: fillers ("um", "uh"), false starts, discourse markers ("well", "actually"), informal contractions ("gonna", "kinda")."
- "Informal, incomplete speech: abbreviate dates, use pronouns and short references, drop articles, trail off, short confirmations, casual corrections, partial information, grammatical imperfections."
- "The user does NOT anticipate next steps or volunteer information about future workflow stages unprompted."
- "Output: JSON with rationale, utterance, truncated_assistant_utterance, and overlap_time."

## Normal branch note
- "The normal branch is identical except it omits all interruption handling rules and instead includes state-machine initiation rules ("If chat history is empty, you MUST initiate the conversation naturally")."
- Truncation-validity condition quoted in chunk: "assistant_last_message.startswith(truncated_assistant_utterance)".

**Covers:** User intent profiles, round planner, hidden-information handling
