# Loop Engineering Clearly Explained

**Article:** [Loop Engineering Clearly Explained (Akshay Pachaar, 2026)](https://x.com/akshay_pachaar/status/2069118430582866051)
**Source:** X (Twitter) Article by @akshay_pachaar | Jun 22, 2026

## Human Readable TL;DR

Imagine teaching someone to cook by giving them a step-by-step recipe for each dish. Loop engineering is more like building a kitchen where an intelligent system can figure out what to cook, check if it's done, and fix mistakes on its own. Instead of giving instructions word-by-word, you design the entire system that does the work without you.

## TL;DR

The article explains the paradigm shift from prompting agents to engineering autonomous loops. Boris Cherny (builder of Claude Code) states he no longer prompts his coding agent -- he runs loops. A basic agent loop (model inference -> tool execution -> context update) is solved and trivial. The real engineering challenges are: (1) defining proper termination conditions beyond simple "model says it's done," (2) preventing context rot in long-running loops through compaction and offloading, (3) designing non-overlapping, idempotent tools with agent-friendly error messages, and (4) incorporating critics (tests, validators) that can say no to prevent self-congratulation. When the harness matters more than the model, Teams have improved benchmarks using the same model by only changing the loop.

---

## Problem & Motivation

Over half of AI practitioners on social media are suddenly talking about the same idea: stop prompting agents, start engineering loops. The premise is that the model is becoming a commodity -- the loop around it is where real engineering value lies. The person who built one of the most popular coding agents (Claude Code) publicly stated he doesn't prompt anymore. This raises the question: what is he actually doing instead, and how can others replicate this approach?

---

## Main Original Ideas

1. **The Agent Loop Is Solved** -- The core while-loop (model reads context, proposes tool calls, tool executes, results added to context) is trivial -- six lines of code. Every serious agent framework converges on this same pattern. Nobody competes on the loop itself.

2. **Engineering Effort Moved Outside the Model** -- The work broke into four layers: prompt engineering (what you send), context engineering (what the model sees), harness engineering (code around the model running tools, tracking state, handling errors), and loop engineering (the autonomous cycle). Each layer wraps the one before it.

3. **The Harness Matters More Than the Model** -- Teams kept the model fixed, changed only the code around it (the harness), and jumped from the middle of a benchmark to the top five. Same brain, different loop. LangChain formalizes this as Agent = Model + Harness. If you're not the model, you're the harness.

4. **Four Hardest Parts of Loop Engineering** -- (a) knowing when to stop (terminal message vs. task completion), (b) keeping context clean (compaction, offloading, sub-agents), (c) designing tools the agent can actually use (few, non-overlapping, idempotent writes, agent-friendly errors), (d) incorporating a critic that can say no (separate maker from checker).

5. **The Designer's Role Shift** -- Your job changes from giving instructions to designing three things: the goal (success criteria the agent checks against), the loop (with sane brakes), and the verifier (so "done" is proven, not claimed).

---

## Key Findings

- The while-loop structure of agents is universally converged upon -- all serious implementations produce essentially the same six lines.
- Prompting is steering the agent move-by-move; loop engineering is building the system that steers itself.
- "Done" defined as an automated check (tests pass) before execution, not a vibe afterward.
- "Doom loop" occurs when a rotted context produces worse decisions which add more noise.
- Andrej Karpathy runs research loops overnight -- tweak a script, test it, keep what works, discard what doesn't, with himself nowhere in the loop.

---

## Suggestions & Future Directions

- Start with the basic loop, add max-iteration cap, timeout, and cost ceiling immediately.
- Define "done" as an automated check before execution, not a post-hoc estimate.
- Protect the context: compact long runs, offload big outputs, isolate messy subtasks into sub-agents.
- Audit tools: keep them few and focused, make writes idempotent, rewrite errors for the agent.
- Put a critic in the loop before going fully hands-off -- only trust the thing that says no.

---

## Author & Publisher

**Author:** Akshay Pachaar (@akshay_pachaar)
**Publisher:** X (Twitter) Article
**Date:** June 22, 2026

### Key Figures Referenced

- **Boris Cherny** -- Builder of Claude Code, who publicly stated "I don't prompt Claude anymore. I have loops that are running. My job is to write loops."
- **Andrej Karpathy** -- Captures the mindset: "Don't tell the model what to do, give it success criteria and watch it go."
- **LangChain** -- Agent = Model + Harness formalization.
