[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Voice Agent Tool Execution and Agentic Task-Completion Results
**In one sentence:** StepAudio 3 Realtime achieves a 56.0% macro task-success rate on τ-Voice — close to Grok's 56.5% and above Qwen (54.6%) and GPT (45.7%) — with the best telecom score (70.2%) and near-best airline score (60.0%) but weaker retail (37.7%), supported by training that grounds tool use in clarification, confirmation, and evidence from asynchronous backend execution.
## Key points
- Macro task-success rate on τ-Voice is 56.0% for StepAudio 3 Realtime, versus 56.5% for Grok Voice Think Fast 2.0 High, 54.6% for Qwen Audio 3.0 Realtime Plus, and 45.7% for GPT-Realtime-2.1 High.
- Telecom is StepAudio 3 Realtime's strongest domain at 70.2%, exceeding Grok by 6.5 percentage points and the highest among evaluated models.
- Airline score is 60.0%, within 2.0 percentage points of the best reported score of 62.0% (GPT-Realtime-2.1 High).
- Retail score is 37.7%, trailing Grok's 49.7%, leaving room for further improvement.
- Before committing to an external action, the model is trained to gather missing information through clarification or context retrieval and to obtain required confirmation.
- Backend tasks execute asynchronously while conversation continues: the model associates task-related input with the ongoing task, distinguishes it from unrelated dialogue, and incorporates results into conversational context.
- Training combines targeted voice-agent dialogues (routing, clarification, private-context retrieval, confirmation, execution-time updates, progress queries, result reporting) with filtered multi-step agent trajectories, plus negative examples against unnecessary tool invocation and unsupported claims.
---
## Table 9: Agentic task-completion results on τ-Voice
**Covers:** Table 9 with task-success rates on 0–100 scale

Scores are task-success rates on a 0–100 scale, with higher values indicating better performance. The macro average assigns equal weight to the airline, retail, and telecom domains. Bold marks the best result in each row, and underlining marks the second-best result.

| Domain | StepAudio 3 Realtime | Grok Voice Think Fast 2.0 High | Qwen Audio 3.0 Realtime Plus | GPT-Realtime-2.1 High |
|---|---|---|---|---|
| Airline | 60.0 | 56.0 | 61.3 | 62.0 |
| Retail | 37.7 | 49.7 | 49.0 | 45.6 |
| Telecom | 70.2 | 63.7 | 53.5 | 29.4 |
| Macro Average | 56.0 | 56.5 | 54.6 | 45.7 |

> "As shown in Table 9, StepAudio 3 Realtime achieves a macro task-success rate of 56.0%, close to Grok's 56.5% and above Qwen's 54.6% and GPT's 45.7%."
> "Across domains, StepAudio 3 Realtime achieves the highest telecom score among the evaluated models at 70.2%, exceeding Grok by 6.5 percentage points."
> "Its airline score of 60.0% is within 2.0 percentage points of the highest reported score of 62.0%."
> "Retail performance leaves room for further improvement, with a score of 37.7% compared with 49.7% for Grok."
> "Overall, StepAudio 3 Realtime achieves competitive performance on end-to-end task completion, with the highest telecom score among the evaluated models and an airline score close to the best reported result."

## Tool-use discipline before external action
**Covers:** clarification, retrieval, and confirmation requirements

Execution requires sufficiently specified intent and arguments. Before committing to an external action, the model is therefore trained to gather missing information through clarification with the user or context retrieval using an appropriate tool, and to obtain any required confirmation.

## Conversation during asynchronous execution
**Covers:** Section 7.2 — progress updates, topic shifts, ReAct pattern

Backend tasks execute asynchronously while the conversation continues. During execution, the user may request progress updates, provide additional requirements, or shift to another topic. The model is trained to associate task-related user input with the ongoing task while distinguishing it from unrelated dialogue. As results become available, they are incorporated into the conversational context to inform subsequent spoken responses.

For complex requests, reasoning supports constraint resolution and task planning, while tool and backend outputs provide evidence of what has actually been completed. This evidence guides subsequent reasoning and action, consistent with the interleaved interaction pattern of ReAct [34]. Think-While-Speaking supports spoken responses during deliberation, while asynchronous execution allows the conversation to continue during external task execution.

## Training for conversational tool use
**Covers:** Section 7.3 — targeted dialogues and multi-step trajectories

Training combines targeted voice-agent dialogues with real multi-step agent trajectories. The targeted dialogues cover request routing, clarification, private-context retrieval, confirmation before consequential actions, execution-time updates, progress queries, and result reporting. These dialogues train the model to ground claims about private information and completed work in user-provided context or evidence returned by tools. Negative examples discourage unnecessary tool invocation and unsupported claims of successful execution.

The multi-step trajectories complement these dialogues by exposing the model to longer sequences of reasoning and tool use. Trajectories are filtered and normalized, focusing on tool-call structure, argument consistency, evidence grounding, and suitability for spoken interaction.

## Evaluation setup: τ-Voice
**Covers:** Section 7.4 and Sections 8.1–8.3 agentic entries

StepAudio 3 Realtime is evaluated using the Artificial Analysis (AA) implementation of τ-Voice [35]. The benchmark assesses tool-grounded task completion in full-duplex spoken interaction under challenging conversational and acoustic conditions, including interruptions in which users revise their requests, backchannels, and diverse forms of background noise. These conditions require agents to track evolving requests and coordinate spoken interaction with tool use.

The benchmark covers customer-service tasks in the airline, retail, and telecom domains, with task success determined by whether the final database state matches the target state. Task-success rates are reported for each domain and their equally weighted macro average.

Evaluation-protocol details from Section 8.3: a τ-Voice task succeeds when the final database state matches its target; domain task-success rates average three trials where available, and the reported macro average gives equal weight to Airline, Retail, and Telecom [35].

The StepAudio 3 family is evaluated along six capability domains: speech recognition, audio understanding, dialogue and reasoning, full-duplex interaction, agentic task completion, and general text. The agentic task completion entry is defined as: "The Artificial Analysis implementation of τ-Voice [35] evaluates tool-grounded customer-service tasks in airline, retail, and telecom environments."

Agentic baselines per Section 8.2 use the same Qwen (Qwen Audio 3.0 Realtime Plus [54]) and Grok (Grok Voice Think Fast 2.0 High [55]) variants as full-duplex, with GPT-Realtime-2.1 High [56] replacing GPT-realtime-2. Model versions and effort labels follow the corresponding evaluation records.

**Covers:** streaming voice agent design and agentic task-completion results.
