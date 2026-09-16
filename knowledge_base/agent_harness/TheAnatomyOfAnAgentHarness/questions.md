---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: The Anatomy of an Agent Harness

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What does "Agent = Model + Harness" mean, and what is the boundary rule for deciding what counts as the harness?

> [!tip]- Answer
> A raw model only maps inputs (text, images, audio, video) to text output, so everything else that makes it useful — state, tool execution, feedback loops, enforceable constraints — is the harness: every piece of code, configuration, and execution logic that isn't the model itself. The boundary rule is "if you're not the model, you're the harness," covering system prompts, tools/Skills/MCPs, bundled infrastructure (filesystem, sandbox, browser), orchestration logic, and hooks/middleware. See [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]].

### Q2. Why is the filesystem called the most foundational harness primitive — what jobs does it do, and what does git add on top?

> [!tip]- Answer
> The filesystem gives the agent a workspace for real data, code, and docs; offloads information that doesn't fit in context; persists work across sessions; and serves as a shared collaboration surface for multiple agents and humans. It won because the world already does work on filesystems, so models trained on billions of tokens of filesystem use already know how to operate them. Git adds versioning for tracking changes, rollback, and branching experiments. See [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]].

### Q3. What is the ReAct loop, and why do harnesses ship a general-purpose bash tool instead of pre-building a tool for every action?

> [!tip]- Answer
> ReAct (reasoning + acting) is a loop where the model reasons, takes an action via a tool call, observes the result, and repeats — but a harness can only execute tools it has logic for, so a fixed toolset caps what the agent can do. Shipping a bash/code-execution tool lets the model write and execute code on the fly, designing its own tools as needed: a big step toward giving the model a computer and letting it figure out the rest autonomously. See [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]].

### Q4. What problem do sandboxes solve, and which built-in observation tools let agents run self-verification loops?

> [!tip]- Answer
> Running agent-generated code locally is risky and a single local machine doesn't scale to large agent workloads, so sandboxes provide safe, isolated, on-demand execution with command allow-listing and network isolation, plus pre-installed runtimes, packages, CLIs, and browsers. Browsers, logs, screenshots, and test runners let agents observe their own work — write code, run tests, inspect logs, fix errors — forming self-verification loops that ground solutions instead of trusting first drafts. See [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]].

### Q5. Since model weights cannot be edited at runtime, how do memory files like AGENTS.md and search tools give agents lasting and up-to-date knowledge?

> [!tip]- Answer
> Without weight edits, the only way to add knowledge is context injection: memory-file standards like AGENTS.md are injected into context on agent start, and as agents add to or edit the file the harness reloads it — a form of continual learning across sessions. Knowledge cutoffs block post-training facts like updated library versions, so web search and MCP (Model Context Protocol) tools like Context7 inject fresh external knowledge on demand. See [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]].

### Q6. What is context rot, and how do the three harness defenses — compaction, tool-call offloading, and progressive-disclosure Skills — each attack it differently?

> [!tip]- Answer
> Context rot is how models get worse at reasoning and completing tasks as their context window fills up, which is why harnesses today are largely delivery mechanisms for good context engineering. Compaction intelligently summarizes and offloads the window when it nears full so work continues instead of API-erroring; tool-call offloading keeps only the head and tail tokens of large tool outputs in context and spills the full output to the filesystem; Skills use progressive disclosure so only short Skill front-matter loads at start instead of every tool and MCP server description. See [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]].

### Q7. Your coding agent keeps quitting early on a multi-day task and losing coherence across sessions. Which long-horizon harness mechanisms would you assemble, and how do they fit together?

> [!tip]- Answer
> Track all work in the filesystem plus git so millions of tokens of progress persist as a shared ledger that fresh windows and new agents can resume from. Add a Ralph Loop — a hook that intercepts the model's exit attempt and reinjects the original prompt in a clean context window against a completion goal — plus planning through a plan file in the filesystem and verification through hooks that run a test suite and loop back with error messages on failure. Together, durable state, continuation pressure, plans, and test feedback keep the agent coherent across many context windows. See [[wiki/01-the-anatomy-of-an-agent-harness|The Anatomy of an Agent Harness]].

### Q8. Should you default to the harness a model was post-trained with, or invest in a task-optimized harness — and what evidence settles it?

> [!tip]- Answer
> Invest in the task-optimized harness: post-training models with a harness in the loop overfits them to its own tools (e.g. Codex-5.3's apply_patch file-editing logic, where switching patch methods degrades performance although a truly intelligent model should adapt trivially), so the training harness is often not the best one — Opus 4.6 in Claude Code scores far below Opus 4.6 in other harnesses on the Terminal Bench 2.0 leaderboard. The authors climbed from Top 30 to Top 5 on Terminal Bench by changing only the harness, and harness engineering keeps paying off even as models absorb planning and verification natively, because a good environment, the right tools, durable state, and verification loops make any model more efficient. See [[wiki/02-the-coupling-of-model-training-and-harness-design|The Coupling of Model Training and Harness Design]].
