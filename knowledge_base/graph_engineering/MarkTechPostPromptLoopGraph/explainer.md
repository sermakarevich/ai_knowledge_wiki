> [[index|Wiki]] | [[summary|Summary]]

# Prompt Engineering vs Loop Engineering vs Graph Engineering — In Plain Language

## What is this about?

Imagine you're managing work at three different scales. At the smallest scale, you write one really good instruction for one task — like giving someone a clear, well-worded request. That's "prompt engineering." At the next scale, you set up a whole routine that repeats a task automatically and checks its own work without you watching every step — like a thermostat that keeps checking the temperature and adjusting, instead of you manually turning a dial. That's "loop engineering." At the biggest scale, you have several of these automatic routines working together and handing tasks to each other — like a small office where different people (or robots) each have a job and pass work along. That's "graph engineering."

This article argues that people talk about these three as if you have to pick one, like choosing between three different tools. But they're not alternatives — they're layers that stack. You always have a prompt somewhere, even inside a loop; you always have loops somewhere, even inside a graph. The question isn't "which one should I use?" but "how many layers do I actually need for this job?"

## Why does it matter?

If you're building anything with AI agents — coding assistants, research bots, customer-support automations — it's tempting to reach for the fanciest setup because it sounds more sophisticated. But this article's point is that fancier is not free: a multi-agent "graph" setup can cost about 15 times more in computing resources than a single request, for roughly 90% better results on certain hard tasks. That trade is worth it sometimes and a waste of money other times. Knowing which layer you actually need — instead of guessing or defaulting to the most impressive-sounding one — saves real money and avoids building something more complicated (and more fragile) than the job requires.

## How does it work?

Think of it as climbing a ladder, one rung at a time, and only climbing when the rung below stops holding your weight:

1. **Start with a prompt.** If a person is reading and approving every single output before anything happens with it, you don't need automation at all — a well-written prompt and human judgment are enough.
2. **Check if you can tell "done" without a human.** Before automating repetition, you need some way — a test, a checklist, a second AI check — to mechanically decide whether an output is actually correct or complete. Without this, an automated loop just keeps running until it runs out of budget, not because the work is actually finished.
3. **If you can, build a loop.** A loop is a system that repeats: try something, check it, try again if needed — without a human clicking "approve" every time. Good loops include a separate "checker" step, since the same AI that did the work tends to grade its own homework too kindly, plus a written record of what happened so far, because the AI doesn't remember previous runs on its own.
4. **Only go to a graph if tasks truly need to run in parallel and don't fit one continuous train of thought.** A graph connects multiple loops/agents, each with its own job, in a structure the article breaks into two parts: who is responsible for what (a slow-changing org chart) and what is happening right now on this specific task (a fast-changing to-do map, with tasks splitting and merging).

The article is also candid that the "graph" idea is not brand new — a widely used tool called LangGraph, and some of Anthropic's own published patterns, already described systems this way years before "graph engineering" became a buzzword. What's newer is just that everyone is now using the same words (node, edge, state) for the same design decisions.

## Where can this be used?

- **Deciding how to build an internal AI tool:** before building an elaborate multi-agent pipeline, run through the checklist — do you actually have a way to check "done" automatically? Does the task really need to run in parallel across separate agents?
- **Debugging a misbehaving multi-agent system:** the article's reminder that sloppy instructions (not agent architecture) caused a real bug — one query spawning 50 unnecessary subagents — is a useful first thing to check before redesigning the whole system.
- **Budgeting compute for AI projects:** the 15x-cost-for-90%-gain trade-off is a concrete number to bring into a cost/benefit conversation with a team or manager before committing to a heavier architecture.
- **Designing multi-agent systems generally:** the reminder that data can silently fail to reach a step just because no connection was built for it is a specific bug pattern worth checking for during design review, not just during testing.

## Conclusions & takeaways

A month from now, remember this: don't reach for the most complex-sounding AI architecture by default. Climb the ladder only when the rung below genuinely runs out — no human reviewer, no automatic way to check correctness, task too big for one continuous train of thought, or a real need for parallel work. And remember that the extra structure (loops, graphs) doesn't replace good prompting or good task understanding — it just adds scaffolding around it, which is why the fancier setups are actually harder to get right, not easier.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Loop | An automated repeat-and-check cycle: an AI tries something, checks the result, and tries again, without a human approving each step. |
| Graph | Several loops/agents connected together, each doing a piece of a bigger task and passing work to each other. |
| Stop condition | The rule that tells an automated loop "you're actually done" — as opposed to just running out of a token/time budget. |
| Org graph | The slow-changing chart of which agents exist and who's responsible for what — like a company org chart. |
| Work graph | The fast-changing map of what's actively happening on one specific task right now — which parts are running, splitting, or merging. |
| Node | One step or agent in a graph — could be a single AI call, a tool, or a whole sub-agent. |
| Edge | The defined connection between two nodes that lets information (or control) pass from one to the other. |
| StateGraph | The specific building block in the LangGraph framework where you register nodes and edges before running the whole workflow. |
| Checker sub-agent | A separate AI (or process) whose only job is to grade another AI's output, because the original AI tends to over-praise its own work. |
