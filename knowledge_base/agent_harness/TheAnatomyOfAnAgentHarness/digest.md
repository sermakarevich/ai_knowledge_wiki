> [[index|Wiki]] | [[summary|Summary]]

# The Anatomy of an Agent Harness — Digest

## 1. [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]]

**In one sentence:** An agent equals model plus harness, and harness engineering wraps the model with filesystems, code execution, sandboxes, memory/search, context-rot defenses, and long-horizon loops to turn model intelligence into useful autonomous work.

## Key points

- Agent = Model + Harness: a raw model only takes in text/images/audio/video and outputs text, so everything else (state, tool execution, feedback loops, enforceable constraints) is harness code, configuration, and execution logic.
- The filesystem is the most foundational harness primitive: it gives agents a workspace, offloads information that does not fit in context, persists work across sessions, and serves as a collaboration surface, with git adding versioning, rollback, and branching.
- Instead of pre-building a tool for every action, harnesses ship a bash/code-execution tool so the model can write and execute code on the fly inside a ReAct (reason → act via tool call → observe → repeat) loop.
- Sandboxes provide safe, isolated, scalable execution: run code, inspect files, and install dependencies off-local, with allow-listed commands and network isolation, plus pre-installed runtimes, CLIs, browsers, logs, screenshots, and test runners for self-verification loops.
- Memory without weight edits means context injection: memory-file standards like AGENTS.md are injected on agent start and reloaded as agents edit them (continual learning across sessions), while web search and MCP tools like Context7 supply post-cutoff knowledge such as new library versions.
- Context rot (reasoning degrades as the context window fills) is fought three ways: compaction (summarize/offload when the window nears full instead of API-erroring), tool-call offloading (keep head/tail tokens over a threshold, spill full output to filesystem), and Skills with progressive disclosure (only Skill front-matter loaded on start).
- Long-horizon autonomy compounds earlier primitives: filesystems plus git track millions of tokens of work across sessions and agents, Ralph Loops intercept exit attempts via hooks and reinject the original prompt in a clean window against a completion goal, and planning plus self-verification (plan files, test-suite hooks, self-evaluation) keep work on track.

## 2. [[wiki/02-the-coupling-of-model-training-and-harness-design|The Coupling of Model Training and Harness Design]]

**In one sentence:** Models and harnesses are post-trained together in a feedback loop that makes models highly capable inside their own harness but overfitted to it, so the best harness for a given task is often a different, task-optimized one — and harness engineering remains valuable even as models absorb more capabilities.

## Key points

- Agent products like Claude Code and Codex are post-trained with models and harnesses in the loop, improving models at harness-designer-chosen skills: filesystem operations, bash execution, planning, and parallelizing work with subagents.
- This creates a repeating feedback loop: useful primitives are discovered, added to the harness, and then used when training the next generation of models, making models more capable within the harness they were trained in.
- Co-evolution causes overfitting: changing tool logic degrades model performance, e.g. the Codex-5.3 prompting guide's apply_patch tool logic for editing files — switching patch methods should be trivial for a truly intelligent model.
- The post-training harness is not necessarily the best harness for your task: on the Terminal Bench 2.0 Leaderboard, Opus 4.6 in Claude Code scores far below Opus 4.6 in other harnesses.
- Harness-only changes carry large gains: the authors improved their coding agent from Top 30 to Top 5 on Terminal Bench 2.0 by only changing the harness.
- As models get more capable, harness functions get absorbed into the model — better native planning, self-verification, and long-horizon coherence requiring less context injection — yet harness engineering stays useful, just as prompt engineering does.
- Harnesses do two jobs: patch over model deficiencies, and engineer systems around model intelligence (well-configured environment, right tools, durable state, verification loops) that make any model more efficient regardless of base intelligence.

## The argument in five moves

1. An agent is model plus harness: the raw model only maps inputs to text, so all durable usefulness — state, tools, loops, constraints — must be engineered around it.
2. Working backwards from desired behavior yields the core harness stack: filesystems for durable shared state, bash/code execution for open-ended action, and sandboxes with browsers, logs, and test runners for safe observation and self-verification.
3. Since weights cannot be edited at runtime, knowledge and context must be managed by the harness: memory files and search inject fresh knowledge, while compaction, tool-call offloading, and progressive-disclosure Skills fight context rot.
4. Long-horizon autonomy is the compound payoff of those primitives — filesystem/git ledgers plus Ralph Loops, planning, and verification hooks sustain coherent work across sessions, agents, and context windows.
5. Models and harnesses co-evolve through post-training in the loop, which boosts in-harness skill but overfits the model to its own tools, so the training harness is often not the best harness for a new task.
6. Therefore harness engineering endures: even as models absorb planning and verification natively, task-optimized environments, tools, state, and verification loops keep delivering large gains, as the Terminal Bench Top 30 to Top 5 harness-only climb shows.
