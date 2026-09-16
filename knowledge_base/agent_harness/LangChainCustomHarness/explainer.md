> [[digest|Digest]] | [[summary|Summary]]

# How to Build a Custom Agent Harness — In Plain Language

## What is this about?

Think of a talented new assistant who is very smart but starts every day with an empty desk. If you hand them the right folder at the right moment, they do great work. If you dump ten filing cabinets on their desk at once, or give them nothing at all, they struggle. A language model is like that assistant, and the "harness" is everything around it: the desk, the folders, the rules for when to fetch something or ask for help.

This piece says a useful agent follows a simple formula: `agent = model + harness`. The model does the thinking and talking, while the harness connects it to the real world — tools, files, memory — and delivers the right context at every step. LangChain's `create_agent` is deliberately kept small: give it a model, some tools, and a system prompt, and it runs the basic loop of "model thinks, calls a tool, reads the result, repeats." Everything else is added with small plug-in pieces called middleware.

The big idea is fit. Instead of buying one giant pre-packed toolkit with features you do not need, you start minimal and snap on only the pieces your job demands — memory for a returning customer, approvals for risky actions, summaries for long-running work. Each middleware piece handles one concern and combines freely with the others.

## Why does it matter?

Because an agent is only as good as the context it gets. Two teams can use the same model and get very different results, simply because one team's harness feeds the model the right information at the right time and the other does not. Context delivery, not just model choice, is the main lever of agent quality.

It also matters for cost and trust. Long sessions pile up history until it no longer fits or becomes expensive. Sensitive work needs privacy checks, approvals, and human review. Fragile work needs retries when something flickers. A fitted harness handles all of that outside the prompt, on every step, so the agent is more reliable, safer, and cheaper to run.

Finally, it matters for reuse. When customization lives in small, isolated middleware units instead of one tangled script, the same unit — say, a memory loader or a cost guard — can be reused across every agent in an organization. LangChain's own agents are presented as examples: each one is built on the same minimal `create_agent` base with a different middleware stack matched to its mission.

## How does it work?

1. **Start minimal.** You call `create_agent` with three things: a model, a set of tools, and a system prompt. That gives you a working agent that runs the core loop.
2. **Run the loop.** The model looks at the conversation, decides what to do next, optionally calls a tool, reads the tool's result, and continues until the task is done.
3. **Hook in middleware.** Middleware pieces attach to the loop at fixed points: when the agent starts, before and after each model call, before and after each tool call, and when the agent shuts down.
4. **Use the four levers.** Each middleware customizes behavior through deterministic rules (plain code that always runs the same way), tool lifecycle controls (which tools exist and how they run), custom state (extra notes carried across steps), and stream handlers (how partial output is delivered).
5. **Keep context fitting.** As the run grows, summarization and context editing trim old history so the conversation still fits. Memory middleware loads useful background at startup and saves lessons back at the end.
6. **Expand what the agent can do.** Filesystem, shell, and code-execution access unlock bigger solutions, while subagents give hard subtasks a fresh, clean workspace, with a todo list tracking long-run progress.
7. **Guard reliability, policy, and cost.** Retries with backoff and model fallbacks absorb temporary failures. Privacy, compliance, and approval checks run on every outside call. Human-in-the-loop gates pause before consequential actions. Call limits and prompt caching keep spending under control.

## Where can this be used?

A customer-service agent looks very different from a long-running coding agent, and the harness should reflect that. A support agent might lean on memory (remember this customer), policy checks (protect personal data), and approval gates (confirm a refund before acting).

A coding or research agent on a long task leans instead on summarization (keep a week-long session fitting), subagents with todo lists (split a big build into clean pieces), and shell or code-execution access (try things directly instead of describing them in words).

The same pattern extends to internal helpers: a sales helper, an async background worker, or a no-code agent builder can each start from the same minimal base and add only the middleware their mission needs. The article holds this up as the easiest path to a custom harness that truly fits.

## Conclusions & takeaways

The takeaway is simple: start with the smallest working agent, then fit the harness to the task's real needs for context, failures, rules, and environment. Small composable pieces beat one big fixed package, because you pay — in complexity, cost, and risk — only for what you use.

There are honest limits. A fitted harness takes judgment: pick too little and the agent is forgetful, fragile, or unsafe; pick too much and it is bloated and hard to maintain. Middleware does not make the model itself smarter — it only delivers better context and guardrails. And fit is task-specific by definition, so there is no universal stack: what helps a coding agent can be dead weight for a support agent.

If you remember one line, remember this: the model thinks, but the harness decides what it gets to think with.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Harness | All the scaffolding around the model — tools, context, rules — that turns answering into doing. |
| `create_agent` | LangChain's minimal starting agent: model plus tools plus system prompt, running the basic loop. |
| Middleware | A small plug-in that adds one behavior to the agent loop and combines with other plug-ins. |
| Model call | One turn where the model reads the context so far and decides what to say or do next. |
| Tool call | The agent using an outside ability, like searching, reading a file, or running code. |
| Context window | How much text the model can consider at once; long histories can overflow it. |
| Summarization | Compressing old conversation into a shorter recap so the run still fits. |
| Memory | Loading useful background at the start and saving lessons at the end so the agent improves. |
| Subagent | A helper agent given one subtask with a fresh workspace to avoid clutter. |
| Human-in-the-loop | Pausing before a risky step so a person can approve or correct it. |
| Prompt caching | Reusing repeated prompt pieces to save time and money. |
| Task-harness fit | Matching the harness pieces to the task's actual context, failure, policy, and environment needs. |
