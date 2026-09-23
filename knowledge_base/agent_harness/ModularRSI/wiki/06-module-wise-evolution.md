> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# 1. Agent Loop — Five-Module Harness Architecture
**In one sentence:** The chunk defines a five-module harness in which Agent Loop is the outer execution coordinator whose central Loop control maintains execution state, schedules calls, handles retries, and decides whether to continue, while the other four modules exchange call/return inputs and outputs with it and the LLM and terminal environment act as external resources.
## Key points
- The outer box is Agent Loop and the central Loop control box is its runtime logic: maintaining execution state, scheduling calls, handling retries, and deciding whether to continue.
- Each of the other four modules exchanges inputs and outputs with this controller, with bidirectional module arrows indicating a call and its return; the arrows do not prescribe a fixed module-to-module execution sequence.
- The LLM and environment are external resources: the LLM generates responses, while the environment runs commands and stores files and processes; before execution, the composer selects one implementation for each module.
- A normal iteration is: Agent Loop asks Context Management to update conversation history (compressing when needed), sends the current prompt to the LLM, Tool Use parses the response into commands and a completion signal, executes commands in the environment, and returns results or errors.
- Observation Management reads the current terminal output and converts it into agent-readable feedback, which differs from Context Management because Context Management works on the accumulated conversation.
- Task Completion Detection returns a stop recommendation and a reason — the example detector requires two consecutive completion declarations — and Agent Loop maintains that count, issues the confirmation prompt after the first declaration, and follows the recommendation, while evolved loop variants can override it.
- Parsing errors can trigger a retry, and session failures or execution limits can end the run.
- `AgentLoop.run` takes `initial_prompt: str, original_instruction: str, observation: Observation, context_mgmt: ContextMgmt, tools: ToolSet, verification: VerificationLoop, chat: Chat, ctx: ModuleCtx` and returns `AgentLoopResult` (execution status, final text, and failure tag); each implementation is registered with a name, description, and configuration parameters, and the shared `ModuleCtx` provides task configuration, environment access, and recording services.
---
## A. Harness Architecture — Figure 5
Verbatim caption: "Figure 5: Architecture of the five-module harness."

The figure labels the top as "Agent Loop" alongside an "execution coordinator", with sub-boxes for Context Management, Loop control (model inference, state / retry / stop), Task Completion Detection (module call / return, runtime relationships), Tool Use (execute), Observation Management (read output), plus external LLM (prompt / response, state / decision) and Environment (terminal, files / processes).

Verbatim structural claims from the text:
- "Figure 5 shows how the five modules interact during task execution."
- "The outer box is Agent Loop, and the central Loop control box represents its runtime logic: maintaining execution state, scheduling calls, handling retries, and deciding whether to continue."
- "Each of the other four modules exchanges inputs and outputs with this controller."
- "The bidirectional module arrows indicate a call and its return."
- "The LLM and environment are external resources: the LLM generates responses, while the environment runs commands and stores files and processes."
- "Before execution, the composer selects one implementation for each module."
- "In a normal iteration, Agent Loop first asks Context Management to update the conversation history, compressing it when needed."
- "It then sends the current prompt to the LLM."
- "Tool Use parses the response into commands and a completion signal, executes the commands in the environment, and returns execution results or errors."
- "Observation Management reads the current terminal output and converts it into agent-readable feedback."
- "This differs from Context Management, which works on the accumulated conversation."
- "Agent Loop combines the feedback with tool results, updates its state, and passes that state to Task Completion Detection."
- "The figure shows these modules' relationships; the arrows do not prescribe a fixed module-to-module execution sequence."

## Task Completion Detection interaction
- "Task Completion Detection returns a stop recommendation and a reason."
- "For example, the detector requires two consecutive completion declarations."
- "Agent Loop maintains that count and issues the confirmation prompt after the first declaration; the detector checks whether the count meets its criterion."
- "The loop follows the recommendation, while evolved loop variants can override it."
- "If execution continues, the loop prepares the next prompt from the feedback."
- "Parsing errors can instead trigger a retry, and session failures or execution limits can end the run."

## A.1 Module Interface Excerpts — Listing 1 (1. Agent Loop)
Verbatim intro: "Listing 1 shows the main inputs and outputs of all five modules. The signatures follow the implementation; imports, setup methods, and method bodies are omitted."

Verbatim registration/context rule: "Each implementation is registered with a name, description, and configuration parameters. The shared ModuleCtx provides task configuration, environment access, and recording services."

Verbatim listing header: "Listing 1: Selected interfaces of the five harness modules. Ellipses denote omitted implementations."

Agent Loop excerpt as given in the chunk:

```
# 1. Agent Loop

# Input: task, conversation, and the other four modules.

# Output: execution status, final text, and failure tag.
class AgentLoop(Protocol):
    async def run(
        self, initial_prompt: str, original_instruction: str,
        observation: Observation, context_mgmt: ContextMgmt,
        tools: ToolSet, verification: VerificationLoop,
        chat: Chat, ctx: ModuleCtx,
    ) -> AgentLoopResult: ...
```

Note on chunk scope: the chunk body otherwise consists of a reference-list tail (Terminal-Bench, recursive self-evolving agents, harness-evolution citations, pp. 13–15 in the extracted text) with no evolution-result claims, so this page records only the Appendix A architecture and A.1 Agent Loop interface actually present.

**Covers:** pp. 13–16, Appendix A Harness Architecture (Figure 5) through A.1 Module Interface Excerpts (Listing 1, item 1. Agent Loop)
