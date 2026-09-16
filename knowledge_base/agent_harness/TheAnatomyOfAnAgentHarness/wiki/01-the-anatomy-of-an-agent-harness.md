[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Anatomy of an Agent Harness

**In one sentence:** An agent equals model plus harness, and harness engineering wraps the model with filesystems, code execution, sandboxes, memory/search, context-rot defenses, and long-horizon loops to turn model intelligence into useful autonomous work.

## Key points

- Agent = Model + Harness: a raw model only takes in text/images/audio/video and outputs text, so everything else (state, tool execution, feedback loops, enforceable constraints) is harness code, configuration, and execution logic.
- The filesystem is the most foundational harness primitive: it gives agents a workspace, offloads information that does not fit in context, persists work across sessions, and serves as a collaboration surface, with git adding versioning, rollback, and branching.
- Instead of pre-building a tool for every action, harnesses ship a bash/code-execution tool so the model can write and execute code on the fly inside a ReAct (reason → act via tool call → observe → repeat) loop.
- Sandboxes provide safe, isolated, scalable execution: run code, inspect files, and install dependencies off-local, with allow-listed commands and network isolation, plus pre-installed runtimes, CLIs, browsers, logs, screenshots, and test runners for self-verification loops.
- Memory without weight edits means context injection: memory-file standards like AGENTS.md are injected on agent start and reloaded as agents edit them (continual learning across sessions), while web search and MCP tools like Context7 supply post-cutoff knowledge such as new library versions.
- Context rot (reasoning degrades as the context window fills) is fought three ways: compaction (summarize/offload when the window nears full instead of API-erroring), tool-call offloading (keep head/tail tokens over a threshold, spill full output to filesystem), and Skills with progressive disclosure (only Skill front-matter loaded on start).
- Long-horizon autonomy compounds earlier primitives: filesystems plus git track millions of tokens of work across sessions and agents, Ralph Loops intercept exit attempts via hooks and reinject the original prompt in a clean window against a completion goal, and planning plus self-verification (plan files, test-suite hooks, self-evaluation) keep work on track.

---

## Can Someone Please Define a "Harness"?

**Covers:** harness definition section

| Claim | Detail from chunk |
|---|---|
| Formula | "Agent = Model + Harness" |
| Boundary rule | "If you're not the model, you're the harness." |
| Definition | "A harness is every piece of code, configuration, and execution logic that isn't the model itself." |
| Why it matters | "A raw model is not an agent. But it becomes one when a harness gives it things like state, tool execution, feedback loops, and enforceable constraints." |
| Concrete inclusions | System Prompts; Tools, Skills, MCPs + and their descriptions; Bundled Infrastructure (filesystem, sandbox, browser); Orchestration Logic (subagent spawning, handoffs, model routing); Hooks/Middleware for deterministic execution (compaction, continuation, lint checks) |
| Method | "The rest of this post walks through core harness components and derives why each piece exists working backwards from the core primitive of a model." |

Author/meta in chunk: Vivek Trivedy, March 10, 2026, 12 min. Key takeaways listed: "Break down complex objectives: Planning tools let agents decompose tasks, track progress, and adapt as they learn" and "Delegate work in parallel: Spawn subagents for independent subtasks, each with isolated context". TLDR verbatim: "TLDR: Agent = Model + Harness. Harness engineering is how we build systems around models to turn them into work engines. The model contains the intelligence and the harness makes that intelligence useful. We define what a harness is and derive the core components today's and tomorrow's agents need."

## Why Do We Need Harnesses — From a Model's Perspective

**Covers:** model-limits section

Models (mostly) take in data like text, images, audio, video and output text — "That's it." Out of the box they cannot:

- Maintain durable state across interactions
- Execute code
- Access realtime knowledge
- Setup environments and install packages to complete work

Mechanism example: the familiar "chatting" UX is a harness — a while loop tracking previous messages and appending new user messages. General principle: "convert a desired agent behavior into an actual feature in the harness."

## Working Backwards from Desired Agent Behavior to Harness Engineering

**Covers:** method section

- "Harness Engineering helps humans inject useful priors to guide agent behavior."
- As models grew more capable, harnesses "surgically extend and correct models to complete previously impossible tasks."
- Pattern followed throughout: "Behavior we want (or want to fix) → Harness Design to help the model achieve this."

## Filesystems for Durable Storage and Context Management

**Covers:** filesystem section

- Want: durable storage to interface with real data, offload information that doesn't fit in context, persist work across sessions.
- Before filesystems, users had to copy/paste content directly to the model — "clunky UX and doesn't work for autonomous agents."
- Why filesystems won: "The world was already using filesystems to do work so models were naturally trained on billions of tokens of how to use them," so "Harnesses ship with filesystem abstractions and tools for fs-ops."
- Unlocks: workspace to read data, code, documentation; incremental add/offload of intermediate outputs and state outlasting a single session; shared collaboration surface for multiple agents and humans ("Architectures like Agent Teams rely on this"); git adds versioning for tracking, rollback, and branching experiments.

## Bash + Code as a General Purpose Tool

**Covers:** code-execution section

- Want: agents that autonomously solve problems without humans pre-designing every tool.
- Constraint: "harnesses can only execute the tools they have logic for," while the dominant pattern is "a ReAct loop, where a model reasons, takes an action via a tool call, observes the result, and repeats in a while loop."
- Design: "Harnesses ship with a bash tool so models can solve problems autonomously by writing & executing code."
- Effect: "a big step towards giving models a computer and letting them figure out the rest autonomously"; the model "can design its own tools on the fly via code instead of being constrained to a fixed set of pre-configured tools"; code execution becomes "the default general-purpose strategy," with other tools still shipped alongside.

## Sandboxes and Tools to Execute & Verify Work

**Covers:** sandbox/environment section

- Want: an environment with the right defaults so agents can safely act, observe results, and make progress.
- Problem: running agent-generated code locally is risky and a single local environment doesn't scale to large agent workloads.
- Design: "Sandboxes give agents safe operating environments" — connect to a sandbox to run code, inspect files, install dependencies; secure isolated execution with command allow-listing and network isolation; on-demand creation, fan-out across tasks, teardown when done.
- Defaults are harness decisions: pre-installed language runtimes and packages, CLIs for git and testing, browsers for web interaction and verification.
- Observation/verification: "Tools like browsers, logs, screenshots, and test runners give agents a way to observe and analyze their work," enabling "self-verification loops where they can write application code, run tests, inspect logs, and fix errors."
- "The model doesn't configure its own execution environment out of the box."

## Memory & Search for Continual Learning

**Covers:** memory/search section

- Want: agents that remember what they've seen and access information that didn't exist at training time.
- Constraint: "Models have no additional knowledge beyond their weights and what's in their current context. Without access to edit model weights, the only way to 'add knowledge' is via context injection."
- Memory mechanism: "the filesystem is again a core primitive. Harnesses support memory file standards like AGENTS.md which get injected into context on agent start. As agents add and edit this file, harnesses load the updated file into context" — "a form of continual learning."
- Freshness mechanism: "Knowledge cutoffs mean that models can't directly access new data like updated library versions" so "Web Search and MCP tools like Context7 help agents access information beyond the knowledge cutoff"; "Web Search and tools for querying up-to-date context are useful primitives to bake into a harness."

## Battling Context Rot

**Covers:** context-management section

- Want: performance that doesn't degrade over the course of work.
- Definition: "Context Rot describes how models become worse at reasoning and completing tasks as their context window fills up"; "Context is a precious and scarce resource."
- Thesis: "Harnesses today are largely delivery mechanisms for good context engineering."
- Three defenses:
  1. Compaction: "intelligently offloads and summarizes the existing context window so the agent can continue working" (alternative — the API errors — "that's not good").
  2. Tool call offloading: "keeps the head and tail tokens of tool outputs above a threshold number of tokens and offloads the full output to the filesystem so the model can access it if needed."
  3. Skills via progressive disclosure: solve "too many tools or MCP servers loaded into context on agent start which degrades performance" — "The model didn't choose to have Skill front-matter loaded into context on start but the harness can support this to protect the model against context rot."

## Long Horizon Autonomous Execution

**Covers:** long-horizon section

- Want: complex work completed "autonomously, correctly, over long time horizons"; "Autonomous software creation is the holy grail for coding agents."
- Model gaps: "early stopping, issues decomposing complex problems, and incoherence as work stretches across multiple context windows."
- Compounding: "Long-horizon work requires durable state, planning, observation, and verification to keep working across multiple context windows."
- Filesystems and git: "Agents produce millions of tokens over a long task so the filesystem durably captures work"; git lets new agents get up to speed on latest work and history; for multi-agent work the filesystem "acts as a shared ledger of work."
- Ralph Loops: "a harness pattern that intercepts the model's exit attempt via a hook and reinjects the original prompt in a clean context window, forcing the agent to continue its work against a completion goal"; made possible by the filesystem (fresh context each iteration, state read from prior iteration).
- Planning and self-verification: "Planning is when a model decomposes a goal into a series of steps"; harnesses support it "via good prompting and injecting reminders how to use a plan file in the filesystem"; verification via hooks running "a pre-defined test suite" and looping back on failure "with the error message," or models prompted to self-evaluate; "Verification grounds solution in tests and creates a feedback signal for self-improvement."

## The Future of Harnesses

**Covers:** chunk ends here — heading present but body cut off in this chunk (next chunk continues the article)

- The chunk file terminates at the "## The Future of Harnesses" heading with no body text in this chunk; per the plan, future-harness directions belong to chunk 02.
