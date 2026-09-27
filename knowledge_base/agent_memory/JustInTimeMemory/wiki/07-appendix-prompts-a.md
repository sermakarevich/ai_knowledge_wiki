> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix A: Prompts — Executor, Judge, and Distillation Prompts
**In one sentence:** Appendix A provides the verbatim executor prompts for WebShop and τ2-bench, the LLM-as-judge prompt for τ2-bench, and the ReasoningBank-style distillation prompts for the ablation study, with ALFWorld/WebShop executor and judge prompts following SkillOS.
## Key points
- The first WebShop executor prompt injects step count, recent observation/action history, current observation, and admissible actions, then requires step-by-step reasoning aided by past experiences before emitting the choice inside `<action> </action>` tags.
- The second WebShop executor variant ("Current Progress") uses `{available_actions}` in place of `{admissible_actions}` and adds explicit search guidance: search with a short core product query, never pack color/size/price into the query, and retry zero-result searches with a shorter broader query.
- The WebShop search guidance defines the terminal goal mechanism as inspecting/selecting a matching product and eventually clicking `[buy now]`.
- The τ2-bench executor prompt frames the agent as a customer-service agent that per turn either sends a user message or makes a tool call (never both), must output valid JSON only, and must explicitly discuss whether to use past experiences at each step.
- The τ2-bench LLM-as-judge prompt credits success only when tool results confirm the requested booking/cancellation/update/refund/fix succeeded, ignores the agent's own claims, requires evidenced process steps, and outputs exactly `{ "success": <true|false>, "reasoning": "<one or two sentences citing the specific tool results that prove success or failure>" }`.
- The ReasoningBank-style distillation prompts for ALFWorld and WebShop each cap extraction at 3 non-overlapping, generalizable memory items and enforce the output schema `# Memory Item i / ## Title / ## Description / ## Content`.
- Provenance is stated explicitly: ALFWorld and WebShop executor and judge prompts follow SkillOS (Ouyang et al., 2026a), the τ2-bench executor prompt comes from the official benchmark with a separately designed judge prompt, and the distillation prompts are only for the ablation study in Section 4.2.
---
## Executor Prompt (WebShop — step/history/admissible-actions variant)
Quoted verbatim from the chunk:
> "Prior to this step, you have already taken {step_count} step(s). Below are the most recent {history_length} observations and the corresponding actions you took: {action_history} You are now at step {current_step} and your current observation is: {current_observation} Your admissible actions of the current situation are: [{admissible_actions}]."
> "Now it's your turn to take an action. You should first reason step-by-step about the current situation with the help of past relevant experiences. Once you've finished your reasoning, you should choose an admissible action for current step and MUST present it within <action> </action> tags."
> "You are an expert agent operating in the WebShop e-commerce environment. Your task is to: {task_description}."
> "Here are past experiences and trajectories that might be helpful for your decision: {retrieved_context}"

## Executor Prompt (WebShop — Current Progress variant)
Quoted verbatim from the chunk:
> "Prior to this step, you have already taken {step_count} step(s). Below are the most recent {history_length} observations and the corresponding actions you took: {action_history} You are now at step {current_step} and your current observation is: {current_observation}. Your admissible actions of the current situation are: [ {available_actions} ]."
> "Now it's your turn to take one action for the current step. You should first reason step-by-step about the current situation with the help of past relevant experiences, then think carefully which admissible action best advances the shopping goal. Once you've finished your reasoning, you should choose an admissible action for current step and present it within <action> </action> tags."
> "WebShop search guidance: - Use search[<your query>] with a short core product query, such as the product type or category. - Do not put color, size, price, or every requested attribute into search[<your query>]. Handle those by opening a product page and selecting/clicking options when available. - If a search returns zero results, retry with a shorter broader product query, not a longer query. - The goal is to inspect/select a matching product and eventually click[buy now]."

## Executor Prompt (τ2-bench)
Quoted verbatim from the chunk:
> "<instructions> You are a customer service agent that helps the user according to the <policy> provided below. In each turn you can either: - Send a message to the user. - Make a tool call. You cannot do both at the same time. Try to be helpful and always follow the policy. Always make sure you generate valid JSON only. </instructions>"
> "<policy> [Content Omitted] </policy>"
> "Here are past experiences and trajectories that might be helpful for your decision. You can use it when you feel it's relevant. At each step, first reason about the current situation with the help of past relevant experiences, including explicitly discuss if you want to use past experiences or not, and then take action."
> Template slot: "{retrieved_context}"

## LLM-as-Judge Prompt (τ2-bench)
Quoted verbatim from the chunk:
> "You are an expert judge evaluating whether a customer-service agent successfully satisfied a customer's request. Output a single JSON object and nothing else."
> "# Task — You will be given (1) the customer's request and (2) the full conversation between the agent and the customer. The conversation contains [USER] lines (the customer), [AGENT] lines (the agent's messages, or its tool calls written as fn(arg=value)), and [TOOL] lines (the tool results). Determine whether the agent fully satisfied the customer's request."
> "## What "success" means — The agent must have actually carried out what the customer asked - the correct action (e.g. booking, cancellation, update, refund, troubleshooting fix) must be completed via the appropriate tool call, and the tool result must confirm it succeeded."
> "Credit only outcomes that the [TOOL] results confirm. Do not credit effects the agent merely stated, promised, or planned. Ignore the agent's own claims of completion; rely on the tool results."
> "If the request required following a process (verifying identity/eligibility, confirming before an irreversible action), that process must be evidenced in the transcript."
> "## Strictness — If the transcript is ambiguous about whether the request was fully satisfied, output success=false."
> "- Partial completion is failure: either the customer's request is fully satisfied or the conversation is a failure."
> "- A conversation that ends by giving up, escalating to a human, or hitting the step limit without completing the request is a failure."
> "# Output — Output exactly one JSON object with these fields and nothing else: { "success": <true|false>, "reasoning": "<one or two sentences citing the specific tool results that prove success or failure>" }"

## ReasoningBank-style Distillation Prompts for Ablation Study (ALFWorld and WebShop)
ALFWorld version, quoted verbatim:
> "You are an expert in household task planning. You will be given a task and a trajectory representing how an agent successfully completed the task in a household environment."
> "## Guidelines — Extract and summarize useful insights as memory items that would help an agent solve similar household tasks in the future."
> "## Important notes - Think about why the trajectory succeeded, then summarize the insights. - Extract *at most 3* memory items. - Do not repeat similar or overlapping items. - Focus on generalizable strategies (e.g., where to find objects, what order to do actions), not specific object names or locations."
> "## Output Format — Your output must strictly follow this Markdown format: ``` # Memory Item i ## Title <short title> ## Description <one sentence summary> ## Content <1-3 sentences of actionable insight> ```"

WebShop version, quoted verbatim:
> "You are an expert in online-shopping task planning. You will be given a task and a trajectory representing how an agent successfully completed a shopping task on a web store."
> "## Guidelines — Extract and summarize useful insights as memory items that would help an agent solve similar shopping tasks in the future."
> "## Important notes - Think about why the trajectory succeeded, then summarize the insights. - Extract *at most 3* memory items. - Do not repeat similar or overlapping items. - Focus on generalizable strategies, not specific product IDs, prices, or properties."
> Same Markdown output format as ALFWorld: "# Memory Item i / ## Title <short title> / ## Description <one sentence summary> / ## Content <1-3 sentences of actionable insight>".

## Prompts provenance note
Quoted verbatim from the chunk:
> "Prompts. All curator, executor, LLM-as-judge, and distillation prompts are provided in Appendix A. Our executor and judge prompts for ALFWorld and WebShop follow SkillOS (Ouyang et al., 2026a). For τ2-bench (Barres et al., 2025), we use the executor prompt from the official benchmark and design a separate judge prompt. The ReasoningBank-style distillation prompt used in the ablation study (Section 4.2) is also included."

**Covers:** Appendix A prompts (preprint pp. 15–17): WebShop executor variants, τ2-bench executor, τ2-bench LLM-as-judge, ReasoningBank-style distillation prompts (ALFWorld/WebShop), and provenance note
