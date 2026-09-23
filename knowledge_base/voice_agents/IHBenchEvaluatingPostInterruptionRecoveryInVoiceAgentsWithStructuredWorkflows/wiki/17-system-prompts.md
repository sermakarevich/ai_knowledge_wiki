> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# System Prompts: Assistant System-Message Template and Round Planner
**In one sentence:** The chunk specifies a complete operational system-message template for a state-machine call assistant with exactly one `{known_user_information}` placeholder, plus the round-planner system prompt and schemas that orchestrate one assistant turn and one possibly-interrupting user turn per round.
## Key points
- The system message is a TEMPLATE used directly as the call-based assistant's system prompt and must sound like a real internal product prompt while remaining complete and operational for goal execution, interruption handling, and hallucination avoidance.
- The template must contain exactly one placeholder, `{known_user_information}`, and the assistant may only use that plus information explicitly provided or confirmed by the user, never inventing facts.
- The assistant always speaks first and must drive a strict ordered workflow to a terminal outcome, applying skip conditions and handling refusals, interruptions, and inconsistencies without losing the workflow.
- Call direction is goal-prefixed: `[OUTBOUND]` opens by stating the reason for the call, while `[INBOUND]` greets, asks how it can help, and starts the structured workflow only after the user describes their problem.
- Required inclusions are domain name plus description, paraphrased goal preserving checkpoints and terminal outcome, detailed guidelines as "Operating rules", the known-user-information section, numbered stages each with name, description, skip_conditions, failure_handling, and terminate_conditions, and a completion definition with terminal success and hard-stop failure conditions.
- The round planner is the orchestrating agent receiving full conversation state and deciding both sides' next actions, including whether and where an interruption occurs, conditioning two downstream simulators.
- Assistant planning rules require stage tracking, no early termination except on explicit repeated refusal with no realistic continuation, one action per concise turn, no re-stating known information or re-asking answered questions, and interruption-unaware full-content plans except filler-continuation rounds where `assistant_plan` is null.
---
## System-message template role
| Requirement | Detail |
|---|---|
| Purpose | Output used directly as the assistant model's system prompt for a call-based assistant |
| Style | Must sound like a real internal product system prompt, not a spec dump |
| Completeness | Must contain all instructions needed to execute the goal correctly, handle interruptions, and avoid hallucination |
| Template constraint | Must contain exactly one placeholder: `{known_user_information}` |

**Covers:** System-message template purpose and placeholder rule

## State-machine requirements (fixed)
- The assistant always speaks first and drives a strict workflow to a terminal outcome.
- The assistant must complete the required stages in order, applying skip conditions when valid.
- The assistant must handle refusals, interruptions, and inconsistencies without losing the workflow.
- The assistant must not invent facts; it may only use `known_user_information` and information explicitly provided or confirmed by the user.

**Covers:** Fixed state-machine execution rules

## Call direction
| Prefix | Instruction |
|---|---|
| `[OUTBOUND]` | The assistant calls the user; the system message must instruct the assistant to open by stating the reason for the call |
| `[INBOUND]` | The user calls in; the system message must instruct the assistant to greet the caller and ask how it can help; the structured workflow begins only after the user describes their problem |

**Covers:** Outbound vs inbound opening behavior

## Inclusion requirements
1. Domain name + description (embedded naturally in the role description)
2. The goal (may be paraphrased, but must preserve all required checkpoints and the terminal outcome)
3. The detailed_guidelines (as "Operating rules" or similar)
4. A section for known user information containing the `{known_user_information}` placeholder
5. The stages (well-formatted as a numbered procedure), each with: name, description, skip_conditions, failure_handling, terminate_conditions
6. Completion definition: terminal success and hard-stop failure conditions

Additional constraints:
- Do NOT mention any meta-evaluation terms (benchmark, judge, rubric, verifier, dataset, etc.).
- Keep it strict but not robotic: do not instruct the assistant to narrate stage numbers to the user.
- Verbatim output instruction in chunk: "Return ONLY the JSON object."

**Covers:** Required template sections and constraints

## Round Planner: system prompt
Verbatim role definition:
> "You are a conversation ROUND PLANNER for an audio-call simulation."
> "You are planning ONE upcoming ROUND consisting of: - the assistant's next turn, and - the user's next turn (which may interrupt the assistant mid-utterance). If the assistant's next turn plan is to terminate the conversation, then the user will not have a next turn."

- Role: "The round planner is the orchestrating agent. It receives the full conversation state and decides what both the assistant and user should do next, including whether an interruption occurs and where."
- Purpose: "Your output conditions two downstream simulators (assistant simulator + user simulator). The assistant simulator will generate exact spoken wording from your assistant_plan. The user simulator will generate exact spoken wording and may generate an interruption spec from your interruption_plan."

Inputs received:
- Domain, Assistant goal, AssistantKnowledgeBase (detailed_guidelines, ordered stages, known_user_information)
- User intent (reaction_profile, description, interruption_profile with probabilities and minima, user_hidden_information)
- Conversation history, interruption_stats_so_far, and max_rounds

**Covers:** Round-planner role, single-round scope, inputs and downstream use

## Output schema
```
class InterruptionPlan(BaseModel):
    rationale: str
    interruption_type: Literal["normal","impatient",
        "correction","topic_switch","filler","pushback"]
    interruption_timing_explanation: str

class RoundPlan(BaseModel):
    rationale: str
    will_include_interruption: bool
    assistant_plan: str
    assistant_will_terminate: bool
    user_plan: Optional[str]
    interruption_plan: Optional[InterruptionPlan]
```

**Covers:** InterruptionPlan and RoundPlan schema

## Assistant planning rules
- Determine the current state machine stage from history and knowledge base requirements.
- Plan an assistant turn that advances the workflow toward the goal.
- "AVOID EARLY TERMINATION: Do NOT terminate unless the user has explicitly and repeatedly refused to proceed AND there is no realistic way to continue. Pushback or temporary refusal are NOT reasons to terminate."
- "CONCISE TURNS: Prefer covering one main action or question per turn rather than packing multiple items into a single message."
- "NO RE-STATING KNOWN INFORMATION: If information was already established, do not repeat it in full."
- "NO ASKING ALREADY-ANSWERED QUESTIONS: Before including a question, verify it has not already been answered."
- "INTERRUPTION-UNAWARE: The assistant_plan must describe the full intended content as if the assistant will NOT be interrupted."
- Filler continuation rounds: "If the previous user message was a FILLER interruption, the assistant's next utterance is already determined (the undelivered continuation). Set assistant_plan to null. Focus on planning the user's next message."

**Covers:** Assistant-turn planning rules and filler-continuation handling

## User planning rules
- "user_plan must be CONSISTENT WITH the intent's reaction_profile but should NOT express every trait in every turn. The personality surfaces naturally over the conversation arc."

**Covers:** User-turn consistency rule (chunk truncated here)

**Covers:** 16 You are writing a SYSTEM through I.2 Round Planner user-planning rules
